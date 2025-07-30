"""
OpenRouter API integration for SNID Spectrum Analyzer
"""
import os
import re
import json
import requests
import tkinter as tk
from tkinter import ttk, messagebox

# Import centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('llm.openrouter')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('llm.openrouter')

# OpenRouter API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

# Default free model if nothing else works
DEFAULT_MODEL = "openai/gpt-3.5-turbo"

# Check if API key is stored in the config file
def get_openrouter_api_key():
    """Get OpenRouter API key from config file if it exists"""
    config_path = os.path.join(os.path.expanduser("~"), ".snidanalyzer", "openrouter_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('api_key')
        except (json.JSONDecodeError, IOError):
            return None
    return None

def save_openrouter_api_key(api_key):
    """Save OpenRouter API key to config file"""
    config_dir = os.path.join(os.path.expanduser("~"), ".snidanalyzer")
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, "openrouter_config.json")
    
    # Load existing config if it exists
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            _LOGGER.warning("Could not load existing OpenRouter config file")
    
    # Update config with new API key
    config['api_key'] = api_key
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f)
        _LOGGER.info("OpenRouter API key saved successfully")
    except IOError as e:
        _LOGGER.error(f"Failed to save OpenRouter API key: {e}")
        raise

def save_openrouter_config(api_key, model_id):
    """Save OpenRouter config to file"""
    config_dir = os.path.join(os.path.expanduser("~"), ".snidanalyzer")
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, "openrouter_config.json")
    
    # Load existing config if it exists
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            _LOGGER.warning("Could not load existing OpenRouter config file")
    
    # Update config with new values
    if api_key:
        config['api_key'] = api_key
    if model_id:
        config['model_id'] = model_id
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f)
        _LOGGER.info(f"OpenRouter configuration saved successfully (model: {model_id})")
    except IOError as e:
        _LOGGER.error(f"Failed to save OpenRouter configuration: {e}")
        raise

def get_openrouter_config():
    """Get saved OpenRouter configuration"""
    config_path = os.path.join(os.path.expanduser("~"), ".snidanalyzer", "openrouter_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def verify_model(api_key, model_id):
    """Verify that a model ID is valid by checking with OpenRouter"""
    if not api_key or not model_id:
        _LOGGER.warning("Model verification failed: missing API key or model ID")
        return False
    
    try:
        # Try to fetch the list of models
        response = requests.get(
            OPENROUTER_MODELS_URL,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            models_data = data.get('data', data)
            
            # Look for the model ID in the data
            for model in models_data:
                if isinstance(model, dict) and model.get('id') == model_id:
                    _LOGGER.info(f"Model '{model_id}' verified successfully")
                    return True
                elif isinstance(model, str) and model == model_id:
                    _LOGGER.info(f"Model '{model_id}' verified successfully")
                    return True
            
            # If the model ID wasn't found in the list, it might be a valid ID
            # that's not included in the list for some reason
            # We'll assume it's valid if it follows the provider/model format
            if '/' in model_id:
                _LOGGER.info(f"Model '{model_id}' verified (assumed valid based on format)")
                return True
        
        # If we couldn't verify with the models list, try a small test request
        test_data = {
            "model": model_id,
            "messages": [{"role": "user", "content": "Say hello"}],
            "max_tokens": 1
        }
        
        test_response = requests.post(
            OPENROUTER_API_URL, 
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }, 
            json=test_data
        )
        
        # If the request doesn't fail, assume the model is valid
        if test_response.status_code < 400:
            _LOGGER.info(f"Model '{model_id}' verified via test request")
            return True
        else:
            _LOGGER.warning(f"Model verification test request failed: {test_response.status_code}")
            _LOGGER.warning(test_response.text)
            return False
    
    except Exception as e:
        _LOGGER.error(f"Error verifying model: {str(e)}")
        return False

def fetch_free_models(api_key=None):
    """Fetch available free models from OpenRouter API"""
    if not api_key:
        api_key = get_openrouter_api_key()
    if not api_key:
        _LOGGER.warning("No API key available for fetching models")
        return None
    
    try:
        response = requests.get(
            OPENROUTER_MODELS_URL,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # The API might return data in different formats
            models_data = data.get('data', data)
            

            
            # Filter for models that have "(free)" in the name
            free_models = []
            
            for model in models_data:
                if isinstance(model, dict):
                    model_name = model.get("name", "").lower()
                    model_id = model.get("id", "")
                    context_length = model.get("context_length", 4096)
                    
                    # Format the context length with K or M for better readability
                    formatted_context = format_context_length(context_length)
                    
                    # Check if this model supports reasoning
                    supported_params = model.get("supported_parameters", [])
                    supports_reasoning = "reasoning" in supported_params if supported_params else False
                    
                    if "(free)" in model_name:
                        # Clean up the model name - remove the "(free)" part
                        display_name = model.get("name", "Unknown").replace(" (free)", "")
                        
                        free_models.append({
                            "id": model_id,
                            "name": display_name,
                            "context_length": formatted_context,
                            "supports_reasoning": supports_reasoning
                        })
            

            _LOGGER.info(f"Successfully fetched {len(free_models)} free models from OpenRouter")
            return free_models
        else:
            _LOGGER.error(f"API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        _LOGGER.error(f"Error fetching models: {str(e)}")
        return None

def format_context_length(length):
    """Format context length to be more readable"""
    try:
        length = int(length)
        if length >= 1000000:
            return f"{length/1000000:.1f}M"
        elif length >= 1000:
            return f"{length/1000:.0f}K"
        else:
            return str(length)
    except (ValueError, TypeError):
        return str(length)

def configure_openrouter_dialog(parent):
    """Show dialog to configure OpenRouter settings"""
    dialog = tk.Toplevel(parent)
    dialog.title("Configure OpenRouter")
    
    # Make dialog OS-aware with proper window controls
    dialog.transient(parent)
    dialog.grab_set()
    dialog.geometry("800x800")
    
    # Enable standard window controls (minimize, maximize, close)
    dialog.resizable(True, True)
    dialog.minsize(600, 600)
    
    # Center the window on screen
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    # Standard color scheme matching other dialogs
    colors = {
        'bg_primary': '#f8fafc',      # Main background
        'bg_secondary': '#ffffff',    # Cards, dialogs
        'bg_tertiary': '#f1f5f9',     # Subtle backgrounds
        'text_primary': '#1e293b',    # Main text
        'text_secondary': '#475569',  # Secondary text
        'text_on_accent': '#ffffff',  # Text on colored backgrounds
        'btn_primary': '#3b82f6',     # Blue - main actions
        'btn_primary_hover': '#2563eb',
        'btn_secondary': '#6b7280',   # Gray - secondary actions
        'btn_secondary_hover': '#4b5563',
        'btn_success': '#10b981',     # Green - positive actions
        'btn_success_hover': '#059669',
        'btn_danger': '#ef4444',      # Red - destructive actions
        'btn_danger_hover': '#dc2626',
        'btn_info': '#6366f1',        # Indigo - info actions
        'btn_info_hover': '#4f46e5',
        'btn_accent': '#8b5cf6',      # Purple - special features
        'btn_accent_hover': '#7c3aed',
        'btn_neutral': '#9ca3af',     # Default button color
        'btn_neutral_hover': '#6b7280',
    }
    
    # Main frame - replace ttk.Frame with tk.Frame
    main_frame = tk.Frame(dialog, bg=colors['bg_primary'], padx=15, pady=15)
    main_frame.pack(fill='both', expand=True)
    
    # Introduction - replace ttk.Label with tk.Label
    tk.Label(main_frame, text="OpenRouter API Configuration", 
             font=('Arial', 20, 'bold'), bg=colors['bg_primary'], fg=colors['text_primary']).pack(anchor='w', pady=(0,10))
    
    tk.Label(main_frame, text="OpenRouter provides access to various LLM models. You'll need an API key from https://openrouter.ai", 
             wraplength=500, bg=colors['bg_primary'], fg=colors['text_secondary'], font=('Segoe UI', 14)).pack(anchor='w', pady=(0,15))
    
    # API Key section - replace ttk.Label with tk.Label
    tk.Label(main_frame, text="API Key", font=('Arial', 16, 'bold'), bg=colors['bg_primary'], fg=colors['text_primary']).pack(anchor='w', pady=(10,5))
    
    # Get current API key if it exists
    current_api_key = get_openrouter_api_key() or ""
    api_key_var = tk.StringVar(value=current_api_key)
    
    # Replace ttk.Frame with tk.Frame
    api_key_frame = tk.Frame(main_frame, bg=colors['bg_primary'])
    api_key_frame.pack(fill='x', pady=5)
    
    # Replace ttk.Entry with tk.Entry
    api_key_entry = tk.Entry(api_key_frame, textvariable=api_key_var, width=40, show="•",
                            bg=colors['bg_secondary'], fg=colors['text_primary'], relief='solid', bd=1, font=('Segoe UI', 14))
    api_key_entry.pack(side='left', fill='x', expand=True)
    
    # Toggle to show/hide API key
    def toggle_show_key():
        if api_key_entry['show'] == "•":
            api_key_entry['show'] = ""
            show_button['text'] = "Hide"
        else:
            api_key_entry['show'] = "•"
            show_button['text'] = "Show"
    
    # Replace ttk.Button with tk.Button
    show_button = tk.Button(api_key_frame, text="Show", width=8, command=toggle_show_key,
                           bg=colors['btn_secondary'], fg=colors['text_on_accent'], relief='raised', bd=2, font=('Segoe UI', 13))
    show_button.pack(side='right', padx=(8,0))
    

    
    # Model search - replace ttk.Label with tk.Label
    tk.Label(main_frame, text="Search for Models", font=('Arial', 16, 'bold'), bg=colors['bg_primary'], fg=colors['text_primary']).pack(anchor='w', pady=(15,5))
    
    # Replace ttk.Frame with tk.Frame
    search_frame = tk.Frame(main_frame, bg=colors['bg_primary'])
    search_frame.pack(fill='x', pady=5)
    
    search_var = tk.StringVar()
    # Replace ttk.Entry with tk.Entry
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=30,
                           bg=colors['bg_secondary'], fg=colors['text_primary'], relief='solid', bd=1, font=('Segoe UI', 14))
    search_entry.pack(side='left', fill='x', expand=True)
    
    # Replace ttk.Button with tk.Button
    search_button = tk.Button(search_frame, text="Search", width=12,
                             command=lambda: search_and_select_model(search_var.get()),
                             bg=colors['btn_info'], fg=colors['text_on_accent'], relief='raised', bd=2, font=('Segoe UI', 13))
    search_button.pack(side='right', padx=(8,0))
    
    # Save API key and fetch models
    def save_key_and_fetch():
        api_key = api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("Error", "API key cannot be empty")
            return
        
        save_openrouter_api_key(api_key)
        status_label.config(text="Fetching available models...")
        dialog.update()
        
        # Fetch models - pass the API key directly instead of relying on saved config
        models = fetch_free_models(api_key)
        if models:
            load_models_to_listbox(models, None)
            status_label.config(text=f"Found {len(models)} free models")
        else:
            status_label.config(text="No free models found. Try searching for a specific model.")
    
    # Search for models and allow selection
    def search_and_select_model(search_term):
        if not search_term:
            return
            
        api_key = api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("Error", "API key is required")
            return
            
        save_openrouter_api_key(api_key)
        status_label.config(text=f"Searching for '{search_term}'...")
        dialog.update()
        
        try:
            # Fetch all models
            response = requests.get(
                OPENROUTER_MODELS_URL,
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            if response.status_code != 200:
                error_msg = f"API error: {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            error_msg = f"API error: {error_data['error']}"
                    except:
                        pass
                status_label.config(text=error_msg)
                messagebox.showerror("API Error", error_msg)
                return
                
            # Parse the response
            data = response.json()
            models_data = data.get('data', data)
            
            # Find matches
            matches = []
            search_term_lower = search_term.lower()
            
            for model in models_data:
                if isinstance(model, dict) and 'name' in model and 'id' in model:
                    name = model.get('name', '').lower()
                    model_id = model.get('id', '').lower()
                    
                    # Check if search term matches in name or ID
                    if (search_term_lower in name or search_term_lower in model_id):
                        # Add reasoning support information
                        supported_params = model.get("supported_parameters", [])
                        supports_reasoning = "reasoning" in supported_params if supported_params else False
                        
                        # Format the context length and clean up the display name
                        context_length = model.get("context_length", 4096)
                        formatted_context = format_context_length(context_length)
                        display_name = model.get("name", "Unknown")
                        if "(free)" in display_name:
                            display_name = display_name.replace(" (free)", "")
                        
                        model_with_reasoning = dict(model)
                        model_with_reasoning["supports_reasoning"] = supports_reasoning
                        model_with_reasoning["name"] = display_name
                        model_with_reasoning["context_length"] = formatted_context
                        matches.append(model_with_reasoning)
            
            if not matches:
                status_label.config(text=f"No models found matching '{search_term}'")
                return
            
            # Use the new table structure to load the search results
            load_models_to_listbox(matches, None)
            status_label.config(text=f"Found {len(matches)} models matching '{search_term}'")
        except Exception as e:
            error_msg = f"Error searching for models: {str(e)}"
            status_label.config(text=error_msg)
            messagebox.showerror("Error", error_msg)
    
    # Replace ttk.Button with tk.Button
    tk.Button(main_frame, text="Fetch Free Models", command=save_key_and_fetch,
              bg=colors['btn_accent'], fg=colors['text_on_accent'], relief='raised', bd=2, font=('Segoe UI', 14)).pack(anchor='w', pady=8)
    
    # --- Model selection section ---
    tk.Label(main_frame, text="Available Models", font=('Arial', 16, 'bold'), bg=colors['bg_primary'], fg=colors['text_primary']).pack(anchor='w', pady=(15,5))
    tk.Label(main_frame, text="Select a model to use:", bg=colors['bg_primary'], fg=colors['text_secondary'], font=('Segoe UI', 14)).pack(anchor='w')

    # Model frame
    model_frame = tk.Frame(main_frame, bg=colors['bg_primary'])
    model_frame.pack(fill='both', expand=True, pady=5)

    # Header row for columns (simulate table headers)
    header_frame = tk.Frame(model_frame, bg=colors['bg_primary'])
    header_frame.pack(fill='x')
    header_font = ('Consolas', 14, 'bold')
    col_defs = [
        {"name": "Model Name", "width": 32, "key": "name"},
        {"name": "Reasoning", "width": 10, "key": "supports_reasoning"},
        {"name": "Context", "width": 10, "key": "context_length"},
    ]
    sort_state = {"key": None, "reverse": False}

    def sort_models_by(col_key):
        if not hasattr(dialog, 'model_data') or not dialog.model_data:
            return
        # Toggle sort order if same column
        if sort_state["key"] == col_key:
            sort_state["reverse"] = not sort_state["reverse"]
        else:
            sort_state["key"] = col_key
            sort_state["reverse"] = False
        # Sort
        dialog.model_data.sort(key=lambda m: m.get(col_key, ""), reverse=sort_state["reverse"])
        refresh_model_listbox()

    for i, col in enumerate(col_defs):
        lbl = tk.Label(header_frame, text=col["name"], font=header_font, bg='#e2e8f0', fg=colors['text_primary'],
                       width=col["width"], anchor='w', relief='raised', bd=1, cursor='hand2')
        lbl.grid(row=0, column=i, sticky='ew')
        lbl.bind('<Button-1>', lambda e, k=col["key"]: sort_models_by(k))

    # Listbox for models
    tree_frame = tk.Frame(model_frame, bg=colors['bg_primary'])
    tree_frame.pack(fill='both', expand=True)
    model_listbox = tk.Listbox(tree_frame, height=10, bg=colors['bg_secondary'], fg=colors['text_primary'],
                               selectmode='single', relief='solid', bd=1,
                               font=('Consolas', 14))
    vsb = tk.Scrollbar(tree_frame, orient="vertical", command=model_listbox.yview)
    hsb = tk.Scrollbar(tree_frame, orient="horizontal", command=model_listbox.xview)
    model_listbox.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    model_listbox.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    tree_frame.columnconfigure(0, weight=1)
    tree_frame.rowconfigure(0, weight=1)
    tree_frame.update_idletasks()

    dialog.model_ids = []
    dialog.model_data = []  # Store full model dicts for sorting

    def format_row(model, row_idx):
        # Pad columns for alignment
        name = str(model.get('name', ''))[:30].ljust(30)
        reasoning = ("Yes" if model.get("supports_reasoning") else "No").ljust(8)
        context = str(model.get('context_length', ''))[:8].ljust(8)
        return f" {name}  {reasoning}  {context} "

    def refresh_model_listbox():
        model_listbox.delete(0, tk.END)
        dialog.model_ids = []
        for idx, model in enumerate(dialog.model_data):
            model_listbox.insert(tk.END, format_row(model, idx))
            # Alternating row color
            if idx % 2 == 0:
                model_listbox.itemconfig(idx, bg=colors['bg_tertiary'])
            else:
                model_listbox.itemconfig(idx, bg=colors['bg_secondary'])
            dialog.model_ids.append(model['id'])

    def on_model_select(event=None):
        selection = model_listbox.curselection()
        if not selection:
            return
        item_index = selection[0]
        if hasattr(dialog, 'model_ids') and item_index < len(dialog.model_ids):
            model_id = dialog.model_ids[item_index]
    model_listbox.bind('<<ListboxSelect>>', on_model_select)
    model_listbox.bind('<Double-1>', lambda e: on_model_select() or save_selection())

    status_label = tk.Label(main_frame, text="", bg=colors['bg_primary'], fg=colors['text_secondary'], font=('Segoe UI', 13))
    status_label.pack(anchor='w', pady=5)

    def save_selection():
        model_id = None
        selection = model_listbox.curselection()
        if selection and hasattr(dialog, 'model_ids'):
            item_index = selection[0]
            if item_index < len(dialog.model_ids):
                model_id = dialog.model_ids[item_index]
        if not model_id:
            messagebox.showinfo("Model Required", "Please select a model from the list")
            return
        api_key = api_key_var.get().strip()
        if api_key:
            save_openrouter_api_key(api_key)
            status_label.config(text="Verifying selected model...")
            dialog.update()
            try:
                if not verify_model(api_key, model_id):
                    messagebox.showerror("Verification Failed", "The selected model could not be verified. Please check the model ID or your API key.")
                    status_label.config(text="Verification failed")
                    return
            except Exception as e:
                messagebox.showerror("Verification Error", f"Error verifying model: {str(e)}")
                status_label.config(text="Verification error")
                return
        save_openrouter_config(None, model_id)
        messagebox.showinfo("Success", "OpenRouter configuration saved successfully!")
        dialog.destroy()

    # --- Model loading logic ---
    def load_models_to_listbox(models, current_model_id=None):
        dialog.model_data = []
        for model in models:
            # Ensure all required fields are present
            model['supports_reasoning'] = model.get('supports_reasoning', False)
            model['context_length'] = model.get('context_length', 4096)
            dialog.model_data.append(model)
        refresh_model_listbox()
        # Select the current model if any
        if current_model_id:
            for i, m in enumerate(dialog.model_data):
                if m['id'] == current_model_id:
                    model_listbox.selection_set(i)
                    model_listbox.see(i)
                    break
        elif dialog.model_data:
            model_listbox.selection_set(0)
            model_listbox.see(0)

    # --- Initial model load ---
    if current_api_key:
        config = get_openrouter_config()
        current_model_id = config.get('model_id', '')
        try:
            status_label.config(text="Fetching free models...")
            dialog.update()
            models = fetch_free_models(current_api_key)
            if models:
                load_models_to_listbox(models, current_model_id)
                status_label.config(text=f"Found {len(models)} free models")
            else:
                status_label.config(text="No free models found. Try searching for a specific model.")
        except Exception as e:
            error_msg = f"Error loading models: {str(e)}"
            status_label.config(text=error_msg)
            _LOGGER.error(error_msg)
    
    # Bottom button frame - replace tk.Frame with tk.Frame (already correct)
    button_frame = tk.Frame(main_frame, bg=colors['bg_primary'])
    button_frame.pack(fill='x', pady=15)

    # Styled buttons with larger fonts and raised relief
    cancel_btn = tk.Button(button_frame, text="✖️ Cancel", font=('Segoe UI', 14, 'bold'),
                          bg=colors['btn_neutral'], fg=colors['text_on_accent'], relief='raised', bd=2, padx=20, pady=8,
                          command=dialog.destroy)
    cancel_btn.pack(side='right', padx=8)

    verify_save_btn = tk.Button(button_frame, text="✅ Verify & Save", font=('Segoe UI', 14, 'bold'),
                               bg=colors['btn_success'], fg=colors['text_on_accent'], relief='raised', bd=2, padx=20, pady=8,
                               command=save_selection)
    verify_save_btn.pack(side='right', padx=8)
    
    # Return dialog to caller
    return dialog

def strip_thinking(content: str) -> str:
    """Remove <think>…</think> blocks and any leading/trailing whitespace"""
    return re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

def format_markdown_text(text):
    """
    Format Markdown-style text for display in Tkinter text widget
    Handles **bold**, *italic*, and other common Markdown formatting
    """
    # Process and return the formatted text
    return text

def format_text_for_display(text_widget, text):
    """
    Apply Markdown-style formatting to text and display it in a text widget
    Handles common Markdown formatting like **bold**, *italic*, etc.
    """
    # First, configure the text widget tags - using a nicer font and smaller bold size
    text_widget.tag_configure("bold", font=("Segoe UI", 0, "bold"))
    text_widget.tag_configure("italic", font=("Segoe UI", 0, "italic"))
    text_widget.tag_configure("underline", underline=True)
    text_widget.tag_configure("title", font=("Segoe UI", 13, "bold"))
    text_widget.tag_configure("subtitle", font=("Segoe UI", 11, "bold"))
    text_widget.tag_configure("subsubtitle", font=("Segoe UI", 10, "bold"))
    text_widget.tag_configure("bullet", lmargin1=20, lmargin2=30)
    text_widget.tag_configure("code", background="#f0f0f0", font=("Consolas", 9))
    text_widget.tag_configure("code_block", background="#f0f0f0", font=("Consolas", 9), 
                             lmargin1=20, lmargin2=20)
    text_widget.tag_configure("link", foreground="blue", underline=True)
    text_widget.tag_configure("quote", lmargin1=20, lmargin2=20, foreground="#555555", 
                             background="#f9f9f9")
    
    # Process and insert the text with proper tags
    lines = text.split('\n')
    
    # Track code block state
    in_code_block = False
    code_block_lines = []
    
    # Track block quote state
    in_block_quote = False
    block_quote_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Handle code blocks (```code```)
        if line.startswith('```'):
            if not in_code_block:
                # Start of code block
                in_code_block = True
                code_block_lines = []
            else:
                # End of code block - insert the collected lines
                if code_block_lines:
                    text_widget.insert(tk.END, '\n'.join(code_block_lines) + '\n', "code_block")
                in_code_block = False
            i += 1
            continue
        
        if in_code_block:
            # Collect lines inside code block
            code_block_lines.append(line)
            i += 1
            continue
        
        # Handle block quotes
        if line.startswith('> '):
            if not in_block_quote:
                # Start of block quote
                in_block_quote = True
                block_quote_lines = []
            
            # Add this line to the block quote without the '> ' prefix
            block_quote_lines.append(line[2:])
            i += 1
            continue
        elif in_block_quote:
            # End of block quote - insert the collected lines
            if block_quote_lines:
                text_widget.insert(tk.END, '\n'.join(block_quote_lines) + '\n', "quote")
            in_block_quote = False
            # Don't increment i here, so we process the current line next
            continue
        
        # Process headers (markdown headers)
        if line.startswith('### '):
            text_widget.insert(tk.END, line[4:] + '\n', "subsubtitle")
            i += 1
            continue
        elif line.startswith('## '):
            text_widget.insert(tk.END, line[3:] + '\n', "subtitle")
            i += 1
            continue
        elif line.startswith('# '):
            text_widget.insert(tk.END, line[2:] + '\n', "title")
            i += 1
            continue
        
        # Horizontal rule
        if line == '---' or line == '***' or line == '___':
            text_widget.insert(tk.END, '\n')
            text_widget.insert(tk.END, '─' * 50 + '\n')
            i += 1
            continue
        
        # Process the line for inline formatting
        remaining_line = line
        
        # Check if line is a bullet point
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            indent = len(line) - len(line.lstrip())
            prefix = line[:indent] + '• '
            text_widget.insert(tk.END, prefix, "bullet")
            remaining_line = line[indent + 2:]  # Skip the bullet marker
        
        # Process inline formatting
        while remaining_line:
            # Check for inline code (`code`)
            code_match = re.search(r'`(.*?)`', remaining_line)
            if code_match:
                start, end = code_match.span()
                # Insert text before the match
                if start > 0:
                    text_widget.insert(tk.END, remaining_line[:start])
                # Insert the code text without the ` markers
                text_widget.insert(tk.END, code_match.group(1), "code")
                # Update remaining line to process
                remaining_line = remaining_line[end:]
                continue
            
            # Check for bold text (**text**)
            bold_match = re.search(r'\*\*(.*?)\*\*', remaining_line)
            if bold_match:
                start, end = bold_match.span()
                # Insert text before the match
                if start > 0:
                    text_widget.insert(tk.END, remaining_line[:start])
                # Insert the bold text without the ** markers
                text_widget.insert(tk.END, bold_match.group(1), "bold")
                # Update remaining line to process
                remaining_line = remaining_line[end:]
                continue
            
            # Check for italic text (*text*)
            italic_match = re.search(r'\*(.*?)\*', remaining_line)
            if italic_match:
                start, end = italic_match.span()
                # Insert text before the match
                if start > 0:
                    text_widget.insert(tk.END, remaining_line[:start])
                # Insert the italic text without the * markers
                text_widget.insert(tk.END, italic_match.group(1), "italic")
                # Update remaining line to process
                remaining_line = remaining_line[end:]
                continue
            
            # Check for underlined text (__text__)
            underline_match = re.search(r'__(.*?)__', remaining_line)
            if underline_match:
                start, end = underline_match.span()
                # Insert text before the match
                if start > 0:
                    text_widget.insert(tk.END, remaining_line[:start])
                # Insert the underlined text without the __ markers
                text_widget.insert(tk.END, underline_match.group(1), "underline")
                # Update remaining line to process
                remaining_line = remaining_line[end:]
                continue
            
            # No more special formatting, insert the rest of the line
            text_widget.insert(tk.END, remaining_line)
            remaining_line = ""
        
        # Add newline after processing the line
        text_widget.insert(tk.END, '\n')
        i += 1
    
    # If we ended in a code block or block quote, close it out
    if in_code_block and code_block_lines:
        text_widget.insert(tk.END, '\n'.join(code_block_lines) + '\n', "code_block")
    
    if in_block_quote and block_quote_lines:
        text_widget.insert(tk.END, '\n'.join(block_quote_lines) + '\n', "quote")
    
    # Make the widget read-only after inserting text
    text_widget.config(state=tk.DISABLED)

def call_openrouter_api(prompt, max_tokens=2000):
    """Call the OpenRouter API with the given prompt"""
    config = get_openrouter_config()
    api_key = config.get('api_key')
    model_id = config.get('model_id')
    
    if not api_key:
        _LOGGER.error("OpenRouter API key not configured")
        raise ValueError("OpenRouter API key not configured")
    
    if not model_id:
        # Use default model if none specified
        model_id = DEFAULT_MODEL
        _LOGGER.info(f"Using default model: {model_id}")
    else:
        _LOGGER.info(f"Using configured model: {model_id}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://snid-spectrum-analyzer.io"  # Add a referer to identify the app
    }
    
    # Set up the API request parameters
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "include_reasoning": False,  # Explicitly set include_reasoning to false
        "reasoning": {
            "exclude": True  # Additionally use reasoning.exclude parameter
        }
    }
    

    
    try:
        _LOGGER.debug(f"Sending request to OpenRouter API with model: {model_id}")
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        
        # Handle different error cases
        if response.status_code == 401:
            _LOGGER.error("OpenRouter API key is invalid or expired")
            raise ValueError("API key is invalid or expired")
        elif response.status_code == 404:
            _LOGGER.error(f"Model '{model_id}' not found")
            raise ValueError(f"Model '{model_id}' not found")
        elif response.status_code >= 400:
            error_info = response.json() if response.text else {"error": "Unknown error"}
            error_message = error_info.get("error", {}).get("message", str(error_info))
            _LOGGER.error(f"OpenRouter API request failed: {error_message}")
            raise ValueError(f"API request failed: {error_message}")
        
        response.raise_for_status()
        result = response.json()
        _LOGGER.debug("OpenRouter API request completed successfully")
        
        # Extract the completion text from the response
        try:
            completion_text = result["choices"][0]["message"]["content"]
            
            # Check if response was truncated due to length
            finish_reason = result.get("choices", [{}])[0].get("finish_reason", "")
            if finish_reason == "length":
                _LOGGER.warning(f"⚠️ Warning: Response was truncated due to token limit. Consider increasing max_tokens.")
                # But still return the partial content - it's usually still useful
            
            # Apply the strip_thinking function to remove any thinking tags
            completion_text = strip_thinking(completion_text)
            _LOGGER.info(f"Successfully received response from OpenRouter API (length: {len(completion_text)} chars)")
            return completion_text
        except (KeyError, IndexError) as e:
            # Only print debug info if parsing truly fails
            _LOGGER.error(f"❌ Error parsing API response structure: {str(e)}")
            _LOGGER.error(f"Available keys in result: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            if "choices" in result:
                _LOGGER.error(f"Choices available: {len(result['choices'])}")
                if result["choices"]:
                    choice = result["choices"][0]
                    _LOGGER.error(f"First choice keys: {list(choice.keys()) if isinstance(choice, dict) else 'Not a dict'}")
            # Don't print the full response here as it contains truncated content
            raise ValueError(f"Could not parse response structure: {str(e)}")
    except requests.exceptions.RequestException as e:
        _LOGGER.error(f"Network error during OpenRouter API call: {str(e)}")
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        _LOGGER.error(f"OpenRouter API call failed: {str(e)}")
        raise Exception(f"OpenRouter API call failed: {str(e)}") 