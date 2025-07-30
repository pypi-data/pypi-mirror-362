"""
Enhanced OpenRouter Summarization Interface for SNID Spectrum Analyzer with advanced features
"""
import os
import sys
import json
import logging
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add parent directory to path if running as standalone
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from .openrouter_llm import (
    get_openrouter_config,
    save_openrouter_config,
    OPENROUTER_API_URL,
    format_text_for_display,
    strip_thinking
)

from ..analysis.llm_utils import (
    build_enhanced_context,
    ASTROSAGE_SYSTEM_PROMPT
)

# Configure logging
logger = logging.getLogger(__name__)

class EnhancedOpenRouterSummary:
    """Enhanced summarization interface with advanced features"""
    
    def __init__(self, api_key=None, model_id=None):
        """Initialize the enhanced summarization interface"""
        # Load config if not provided
        config = get_openrouter_config()
        self.api_key = api_key or config.get('api_key')
        self.model_id = model_id or config.get('model_id')
        
        # Track the last generation ID and response metadata
        self.last_generation_id = None
        self.last_response_metadata = {}
        

        self.stream_callback = None
    
    def generate_summary(self, data, analysis_type='comprehensive', 
                        custom_instructions=None, max_tokens=3000, 
                        temperature=0.7, stream_callback=None):
        """Generate enhanced summary with different analysis types
        
        Args:
            data: Either raw text data or structured SNID results dict
            analysis_type: Type of analysis ('comprehensive', 'quick_summary', 'classification_focus', 'redshift_analysis')
            custom_instructions: Custom instructions to override defaults
            max_tokens: Maximum tokens for response
            temperature: Model temperature

            
        Returns:
            tuple: (summary_text, error_message, metadata)
        """
        if not self.api_key:
            return None, "API key not configured", {}
        
        if not self.model_id:
            return None, "Model not configured", {}
        
        if not data:
            return None, "Data to summarize cannot be empty", {}
        
        # Always treat data as formatted text since it comes from format_snid_results_for_llm
        # This prevents the text repetition issue
        prompt = self._create_simple_prompt(str(data), analysis_type, custom_instructions)
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://snid-spectrum-analyzer.io",
            "X-Title": "SNID SAGE - Supernova Analysis"
        }
        
        # Build request data
        messages = []
        if prompt.get('system'):
            messages.append({"role": "system", "content": prompt['system']})
        messages.append({"role": "user", "content": prompt['user']})
        
        request_data = {
            "model": self.model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": bool(stream_callback),
            "reasoning": {
                "exclude": True  # Exclude reasoning tokens
            }
        }
        
        try:
            if stream_callback:
                # Note: Stream callback provided but streaming not implemented
                logger.warning("Streaming not yet implemented for OpenRouter")
                return self._handle_regular_response(headers, request_data)
            else:
                return self._handle_regular_response(headers, request_data)
                
        except Exception as e:
            logger.error(f"Error in generate_summary: {str(e)}")
            return None, f"Error: {str(e)}", {}
    
    def _create_simple_prompt(self, data: str, analysis_type: str, custom_instructions: str = None) -> Dict[str, str]:
        """Create simple prompt from text data"""
        # Use the simplified system prompt
        system_msg = ASTROSAGE_SYSTEM_PROMPT
        
        # Build the user message with clear structure
        user_msg = f"Please analyze the following supernova spectroscopy data:\n\n{data}"
        
        # Add specific formatting instructions if provided
        if custom_instructions:
            user_msg += f"\n\nSpecific formatting request: {custom_instructions}"
        
        return {
            'system': system_msg,
            'user': user_msg
        }
    
    def _handle_regular_response(self, headers: Dict, request_data: Dict):
        """Handle regular (non-streaming) API response"""
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=request_data)
        
        # Check for errors
        if response.status_code != 200:
            error_info = response.json() if response.text else {"error": "Unknown error"}
            error_message = error_info.get("error", {}).get("message", str(error_info))
            logger.error(f"API error: {error_message}")
            return None, f"API error: {error_message}", {}
        
        # Extract the response
        result = response.json()
        logger.debug(f"API response: {json.dumps(result, indent=2)}")
        
        # Get generation ID and metadata
        generation_id = result.get('id', 'unknown')
        self.last_generation_id = generation_id
        
        # Extract metadata
        metadata = {
            'generation_id': generation_id,
            'model': result.get('model', self.model_id),
            'usage': result.get('usage', {}),
            'timestamp': datetime.now().isoformat()
        }
        self.last_response_metadata = metadata
        
        # Extract the completion
        try:
            summary_text = result["choices"][0]["message"]["content"]
            summary_text = strip_thinking(summary_text)
            return summary_text, None, metadata
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected response structure: {e}")
            return None, f"Failed to parse response: {str(e)}", metadata
    

        
        # Fall back to regular response for now
        request_data['stream'] = False
        return self._handle_regular_response(headers, request_data)


class EnhancedSummaryUI:
    """Modern, enhanced UI for the OpenRouter summarization functionality"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AstroSage Enhanced Summary Interface")
        
        # Make dialog OS-aware with proper window controls
        self.root.geometry("1200x900")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#ffffff',
            'bg_secondary': '#f8f9fa',
            'bg_tertiary': '#e9ecef',
            'accent_primary': '#0d6efd',
            'accent_secondary': '#6f42c1',
            'success': '#198754',
            'warning': '#fd7e14',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'border': '#dee2e6'
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._configure_styles()
        
        # Initialize the enhanced summarization interface
        self.summary = EnhancedOpenRouterSummary()
        
        # UI state
        self.is_generating = False
        self.current_analysis_type = tk.StringVar(value='comprehensive')
        self.current_model_info = tk.StringVar()
        
        self.create_enhanced_ui()
        self.update_model_info()
    
    def _configure_styles(self):
        """Configure modern ttk styles"""
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 16, 'bold'),
                           foreground=self.colors['text_primary'])
        
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground=self.colors['text_secondary'])
        
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 10),
                           padding=(12, 8))
        
        self.style.configure('Accent.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           padding=(16, 10))
    
    def create_enhanced_ui(self):
        """Create the enhanced user interface"""
        # Configure root
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Create main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header(main_container)
        
        # Create main content area with notebook
        self.create_content_area(main_container)
        
        # Create status bar
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """Create modern header with title and controls"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title with icon
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(side='left')
        
        tk.Label(title_frame, text="🤖", font=('Segoe UI', 24),
                bg=self.colors['bg_primary']).pack(side='left', padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="AstroSage Enhanced Analysis",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_primary'])
        title_label.pack(side='left')
        
        # Model info and controls
        controls_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        controls_frame.pack(side='right')
        
        # Model info display
        self.model_label = tk.Label(controls_frame, textvariable=self.current_model_info,
                                   font=('Segoe UI', 9),
                                   fg=self.colors['text_secondary'],
                                   bg=self.colors['bg_primary'])
        self.model_label.pack(anchor='e')
        
        # Configuration button
        config_btn = tk.Button(controls_frame, text="⚙️ Configure",
                              font=('Segoe UI', 9),
                              bg=self.colors['bg_tertiary'], 
                              fg=self.colors['text_primary'],
                              relief='flat', bd=1, padx=12, pady=4,
                              command=self.show_config_dialog)
        config_btn.pack(anchor='e', pady=(5, 0))
    
    def create_content_area(self, parent):
        """Create main content area with tabbed interface"""
        # Create notebook for different analysis types
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, pady=(0, 15))
        
        # Analysis tabs
        self.create_analysis_tab("🔬 Comprehensive", 'comprehensive')
        self.create_analysis_tab("⚡ Quick Summary", 'quick_summary') 
        self.create_analysis_tab("📊 Classification", 'classification_focus')
        self.create_analysis_tab("🌌 Redshift Analysis", 'redshift_analysis')
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def create_analysis_tab(self, tab_name, analysis_type):
        """Create an individual analysis tab"""
        # Create tab frame
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=tab_name)
        
        # Create content for this tab
        content_frame = tk.Frame(tab_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Input section
        input_section = self.create_input_section(content_frame, analysis_type)
        
        # Options section
        options_section = self.create_options_section(content_frame, analysis_type)
        
        # Results section
        results_section = self.create_results_section(content_frame, analysis_type)
        
        # Store references for each tab
        setattr(self, f"{analysis_type}_input", input_section['input_widget'])
        setattr(self, f"{analysis_type}_instructions", input_section['instructions_widget'])
        setattr(self, f"{analysis_type}_results", results_section['results_widget'])
        setattr(self, f"{analysis_type}_options", options_section)
    
    def create_input_section(self, parent, analysis_type):
        """Create input section for a tab"""
        # Input frame
        input_frame = tk.LabelFrame(parent, text="📝 Data Input", 
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'])
        input_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Data input area
        input_widget = scrolledtext.ScrolledText(input_frame, 
                                               wrap=tk.WORD, 
                                               height=12,
                                               font=('Consolas', 10),
                                               bg='white',
                                               fg=self.colors['text_primary'])
        input_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add example data based on analysis type
        example_data = self.get_example_data(analysis_type)
        input_widget.insert('1.0', example_data)
        
        # Instructions section
        inst_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        inst_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(inst_frame, text="Custom Instructions (optional):",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']).pack(anchor='w')
        
        instructions_widget = tk.Text(inst_frame, height=3, wrap=tk.WORD,
                                    font=('Segoe UI', 9),
                                    bg='white',
                                    fg=self.colors['text_primary'])
        instructions_widget.pack(fill='x', pady=(5, 0))
        
        return {
            'input_widget': input_widget,
            'instructions_widget': instructions_widget
        }
    
    def create_options_section(self, parent, analysis_type):
        """Create options section for a tab"""
        options_frame = tk.LabelFrame(parent, text="⚙️ Analysis Options",
                                    font=('Segoe UI', 11, 'bold'),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'])
        options_frame.pack(fill='x', pady=(0, 10))
        
        # Options grid
        options_grid = tk.Frame(options_frame, bg=self.colors['bg_secondary'])
        options_grid.pack(fill='x', padx=10, pady=10)
        
        # Max tokens
        tk.Label(options_grid, text="Max Tokens:", 
                font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']).grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        max_tokens_var = tk.IntVar(value=3000)
        tk.Spinbox(options_grid, from_=500, to=8000, width=8, 
                  textvariable=max_tokens_var,
                  font=('Segoe UI', 10)).grid(row=0, column=1, sticky='w')
        
        # Temperature
        tk.Label(options_grid, text="Temperature:",
                font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']).grid(row=0, column=2, sticky='w', padx=(20, 10))
        
        temperature_var = tk.DoubleVar(value=0.7)
        tk.Spinbox(options_grid, from_=0.0, to=2.0, increment=0.1, width=8,
                  textvariable=temperature_var, format="%.1f",
                  font=('Segoe UI', 10)).grid(row=0, column=3, sticky='w')
        
        # Generate button
        generate_btn = tk.Button(options_grid, 
                               text=f"🚀 Generate {analysis_type.replace('_', ' ').title()}",
                               font=('Segoe UI', 11, 'bold'),
                               bg=self.colors['accent_primary'],
                               fg='white',
                               relief='flat', bd=0, padx=20, pady=8,
                               command=lambda: self.generate_analysis(analysis_type))
        generate_btn.grid(row=0, column=4, sticky='e', padx=(20, 0))
        
        # Store options for this tab
        return {
            'max_tokens': max_tokens_var,
            'temperature': temperature_var,
            'generate_button': generate_btn
        }
    
    def create_results_section(self, parent, analysis_type):
        """Create results section for a tab"""
        results_frame = tk.LabelFrame(parent, text="📊 Analysis Results",
                                    font=('Segoe UI', 11, 'bold'),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'])
        results_frame.pack(fill='both', expand=True)
        
        # Results display with enhanced formatting
        results_widget = scrolledtext.ScrolledText(results_frame,
                                                 wrap=tk.WORD,
                                                 font=('Segoe UI', 11),
                                                 bg='white',
                                                 fg=self.colors['text_primary'],
                                                 padx=15, pady=15,
                                                 spacing1=4, spacing2=2, spacing3=4)
        results_widget.pack(fill='both', expand=True, padx=10, pady=(10, 5))
        
        # Action buttons frame
        actions_frame = tk.Frame(results_frame, bg=self.colors['bg_secondary'])
        actions_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Copy button
        copy_btn = tk.Button(actions_frame, text="📋 Copy",
                           font=('Segoe UI', 10),
                           bg=self.colors['bg_tertiary'],
                           fg=self.colors['text_primary'],
                           relief='flat', bd=1, padx=12, pady=6,
                           command=lambda: self.copy_results(analysis_type))
        copy_btn.pack(side='left', padx=(0, 10))
        
        # Save button
        save_btn = tk.Button(actions_frame, text="💾 Save",
                           font=('Segoe UI', 10),
                           bg=self.colors['success'],
                           fg='white',
                           relief='flat', bd=0, padx=12, pady=6,
                           command=lambda: self.save_results(analysis_type))
        save_btn.pack(side='left')
        
        # Clear button
        clear_btn = tk.Button(actions_frame, text="🗑️ Clear",
                            font=('Segoe UI', 10),
                            bg=self.colors['warning'],
                            fg='white',
                            relief='flat', bd=0, padx=12, pady=6,
                            command=lambda: self.clear_results(analysis_type))
        clear_btn.pack(side='right')
        
        return {
            'results_widget': results_widget,
            'copy_button': copy_btn,
            'save_button': save_btn,
            'clear_button': clear_btn
        }
    
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        self.status_bar = tk.Frame(parent, bg=self.colors['bg_tertiary'], height=30)
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        self.status_text = tk.Label(self.status_bar, text="Ready",
                                  font=('Segoe UI', 9),
                                  bg=self.colors['bg_tertiary'],
                                  fg=self.colors['text_secondary'])
        self.status_text.pack(side='left', padx=10, pady=5)
        
        # Progress bar (initially hidden)
        self.progress_bar = ttk.Progressbar(self.status_bar, mode='indeterminate')
    
    def get_example_data(self, analysis_type):
        """Get example data for different analysis types"""
        examples = {
            'comprehensive': """SNID Analysis Results:

Best match: sn1994D.lnw (Type Ia-norm) z=0.0156 ± 0.0008
Age: +5.2 days, rlap=12.4, lap=8.7

Alternative matches:
1. sn1992A.lnw (Type Ia-norm) rlap=11.8
2. sn1996X.lnw (Type Ia-norm) rlap=10.9  
3. sn1991bg.lnw (Type Ia-91bg) rlap=8.2

Spectrum properties:
- Wavelength coverage: 3800-7200 Å
- S/N estimate: 15.3
- Strong Si II 6150Å absorption
- Ca II H&K visible at 3934,3968Å
- No clear He I lines detected""",

            'quick_summary': """Quick SNID match: Type Ia supernova, z=0.012, age ~3 days post-max, rlap=9.5""",

            'classification_focus': """Template matching results for classification:

Primary: Type Ia-norm (rlap=12.1, confident match)
Secondary: Type Ia-91T (rlap=7.8, possible but weaker)  
Tertiary: Type Ia-91bg (rlap=4.2, unlikely)

Key spectral features:
- Strong Si II 6150Å absorption (characteristic of Type Ia)
- Ca II IR triplet present
- No obvious He I lines (rules out Type Ib/c)
- No hydrogen Balmer series (rules out Type II)""",

            'redshift_analysis': """Redshift determination analysis:

Cross-correlation result: z = 0.0142 ± 0.0012
Host galaxy features: z_host = 0.0138 ± 0.0008  
Line fitting (Si II): z = 0.0145 ± 0.0015

Consistency check: All methods agree within 2σ
Systematic effects: Minimal host contamination
Distance modulus: μ = 35.8 ± 0.3 mag (assuming flat ΛCDM)"""
        }
        
        return examples.get(analysis_type, examples['comprehensive'])
    
    def on_tab_changed(self, event):
        """Handle tab change event"""
        current_tab = self.notebook.index(self.notebook.select())
        tab_types = ['comprehensive', 'quick_summary', 'classification_focus', 'redshift_analysis']
        
        if current_tab < len(tab_types):
            self.current_analysis_type.set(tab_types[current_tab])
            self.update_status(f"Switched to {tab_types[current_tab].replace('_', ' ').title()} analysis")
    
    def generate_analysis(self, analysis_type):
        """Generate analysis for the specified type"""
        if self.is_generating:
            self.update_status("⚠️ Analysis already in progress...")
            return
        
        # Get input data
        input_widget = getattr(self, f"{analysis_type}_input")
        instructions_widget = getattr(self, f"{analysis_type}_instructions")
        options = getattr(self, f"{analysis_type}_options")
        
        data = input_widget.get('1.0', tk.END).strip()
        custom_instructions = instructions_widget.get('1.0', tk.END).strip()
        max_tokens = options['max_tokens'].get()
        temperature = options['temperature'].get()
        
        if not data:
            messagebox.showwarning("Input Required", "Please enter data to analyze.")
            return
        
        # Update UI for generation
        self.is_generating = True
        options['generate_button'].config(state='disabled', text="🔄 Generating...")
        self.update_status("🤖 Generating analysis...")
        self.progress_bar.pack(side='right', padx=10, pady=5)
        self.progress_bar.start(10)
        
        # Run generation in thread
        thread = threading.Thread(
            target=self._generate_in_thread,
            args=(data, analysis_type, custom_instructions, max_tokens, temperature)
        )
        thread.daemon = True
        thread.start()
    
    def _generate_in_thread(self, data, analysis_type, custom_instructions, max_tokens, temperature):
        """Generate analysis in background thread"""
        try:
            # Generate summary
            result, error, metadata = self.summary.generate_summary(
            data=data, 
                analysis_type=analysis_type,
                custom_instructions=custom_instructions or None,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
            # Update UI on main thread
            self.root.after(0, self._on_generation_complete, 
                           analysis_type, result, error, metadata)
            
        except Exception as e:
            self.root.after(0, self._on_generation_error, analysis_type, str(e))
    
    def _on_generation_complete(self, analysis_type, result, error, metadata):
        """Handle completion of generation"""
        # Update UI state
        self.is_generating = False
        options = getattr(self, f"{analysis_type}_options")
        options['generate_button'].config(state='normal', 
                                        text=f"🚀 Generate {analysis_type.replace('_', ' ').title()}")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        if error:
            self.update_status(f"❌ Error: {error}")
            messagebox.showerror("Generation Error", f"Failed to generate analysis:\n\n{error}")
        else:
            # Display results with formatting
            results_widget = getattr(self, f"{analysis_type}_results")
            results_widget.config(state='normal')
            results_widget.delete('1.0', tk.END)
            
            try:
                # Use enhanced text formatting
                format_text_for_display(results_widget, result)
            except:
                # Fallback to plain text
                results_widget.insert('1.0', result)
            
            results_widget.config(state='disabled')
            
            # Update status with metadata
            token_info = metadata.get('usage', {})
            status_msg = f"✅ Analysis complete"
            if token_info.get('total_tokens'):
                status_msg += f" ({token_info['total_tokens']} tokens)"
            
            self.update_status(status_msg)
    
    def _on_generation_error(self, analysis_type, error_msg):
        """Handle generation error"""
        self.is_generating = False
        options = getattr(self, f"{analysis_type}_options")
        options['generate_button'].config(state='normal',
                                        text=f"🚀 Generate {analysis_type.replace('_', ' ').title()}")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        self.update_status(f"❌ Error: {error_msg}")
        messagebox.showerror("Generation Error", f"Failed to generate analysis:\n\n{error_msg}")
    
    def copy_results(self, analysis_type):
        """Copy results to clipboard"""
        results_widget = getattr(self, f"{analysis_type}_results")
        content = results_widget.get('1.0', tk.END).strip()
        
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.update_status("📋 Results copied to clipboard")
        else:
            self.update_status("⚠️ No results to copy")
    
    def save_results(self, analysis_type):
        """Save results to file"""
        results_widget = getattr(self, f"{analysis_type}_results")
        content = results_widget.get('1.0', tk.END).strip()
        
        if not content:
            self.update_status("⚠️ No results to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialname=f"astrosage_analysis_{analysis_type}_{timestamp}.txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ],
            title="Save Analysis Results"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"AstroSage {analysis_type.replace('_', ' ').title()} Analysis\n")
                    f.write("="*60 + "\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(content)
                
                self.update_status(f"💾 Results saved to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save results:\n\n{str(e)}")
                self.update_status(f"❌ Save failed: {str(e)}")
    
    def clear_results(self, analysis_type):
        """Clear results"""
        results_widget = getattr(self, f"{analysis_type}_results")
        results_widget.config(state='normal')
        results_widget.delete('1.0', tk.END)
        results_widget.config(state='disabled')
        self.update_status("🗑️ Results cleared")
    
    def show_config_dialog(self):
        """Show configuration dialog"""
        # Import and show the configuration dialog
        try:
            from .openrouter_llm import configure_openrouter_dialog
            configure_openrouter_dialog(self.root)
            self.update_model_info()
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to open configuration:\n\n{str(e)}")
    
    def update_model_info(self):
        """Update model information display"""
        config = get_openrouter_config()
        model_id = config.get('model_id', 'Not configured')
        if len(model_id) > 30:
            model_id = model_id[:27] + "..."
        self.current_model_info.set(f"Model: {model_id}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_text.config(text=message)
        self.root.update_idletasks()


# Backward compatibility
class OpenRouterSummary(EnhancedOpenRouterSummary):
    """Backward compatibility wrapper"""
    pass

class SummaryUI(EnhancedSummaryUI):
    """Backward compatibility wrapper"""
    pass


# Convenience function for integration
def summarize_data(data, analysis_type='comprehensive', custom_instructions=None, 
                  api_key=None, model_id=None):
    """Simplified function for programmatic use"""
    summary = EnhancedOpenRouterSummary(api_key=api_key, model_id=model_id)
    result, error, metadata = summary.generate_summary(
        data=data,
        analysis_type=analysis_type,
        custom_instructions=custom_instructions
    )
    
    if error:
        raise Exception(f"Summary generation failed: {error}")
    
    return result, metadata


# Run the UI if executed directly
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run the UI
    root = tk.Tk()
    app = SummaryUI(root)
    root.mainloop() 