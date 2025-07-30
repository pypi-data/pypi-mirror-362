"""
Enhanced AI Assistant Dialog - Simplified Interface

This module provides a modern AI assistant interface with:
- Single comprehensive summary generation
- Chat interface in separate tab
- Simplified settings
- User metadata input form
- Enhanced SNID context awareness
- Larger fonts throughout
"""

import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
import threading
from datetime import datetime
import json
import os
from typing import Dict, Any, Optional

# Import centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.enhanced_ai_assistant_dialog')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.enhanced_ai_assistant_dialog')

# Import unified systems
try:
    from snid_sage.interfaces.gui.utils.universal_window_manager import get_window_manager, DialogSize
    from snid_sage.interfaces.gui.utils.unified_font_manager import get_font_manager, FontCategory, apply_font_to_widget
    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError:
    UNIFIED_SYSTEMS_AVAILABLE = False


class EnhancedAIAssistantDialog:
    """
    Enhanced AI Assistant Dialog with simplified interface.
    
    Features:
    - Single comprehensive summary generation
    - Chat interface in separate tab
    - Settings menu
    - User metadata input
    - Enhanced SNID context
    """
    
    def __init__(self, gui_instance):
        """Initialize the enhanced AI assistant dialog."""
        self.gui = gui_instance
        self.window = None
        self.is_generating = False
        self.current_snid_results = None
        self.dialog_id = None
        
        # Initialize unified systems
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager = get_window_manager()
            self.font_manager = get_font_manager()
        else:
            self.window_manager = None
            self.font_manager = None
        
        # Modern color scheme - consistent with other dialogs
        self.colors = {
            'bg_primary': '#f8fafc',      # Main background
            'bg_secondary': '#ffffff',    # Cards, dialogs
            'bg_tertiary': '#f1f5f9',     # Subtle backgrounds
            'bg_disabled': '#e2e8f0',     # Disabled elements
            'text_primary': '#1e293b',    # Main text
            'text_secondary': '#475569',  # Secondary text
            'text_muted': '#94a3b8',      # Disabled/muted text
            'text_on_accent': '#ffffff',  # Text on colored backgrounds
            'border': '#cbd5e1',          # Borders and separators
            'hover': '#f1f5f9',           # Hover backgrounds
            'active': '#e2e8f0',          # Active/pressed states
            'focus': '#3b82f6',           # Focus indicators
            'accent_primary': '#3b82f6',  # Default accent/selection colour (blue)
            'accent_secondary': '#8b5cf6', # Purple accent
            'success': '#10b981',         # Green
            'warning': '#f59e0b',         # Orange
            'danger': '#ef4444',          # Red
            'disabled': '#e2e8f0',        # Disabled state colour
            'btn_primary': '#3b82f6',     # Blue - main actions
            'btn_primary_hover': '#2563eb',
            'btn_secondary': '#6b7280',   # Gray - secondary actions
            'btn_secondary_hover': '#4b5563',
            'btn_success': '#10b981',     # Green - positive actions
            'btn_success_hover': '#059669',
            'btn_warning': '#f59e0b',     # Orange - warning actions
            'btn_warning_hover': '#d97706',
            'btn_danger': '#ef4444',      # Red - destructive actions
            'btn_danger_hover': '#dc2626',
            'btn_info': '#6366f1',        # Indigo - info actions
            'btn_info_hover': '#4f46e5',
            'btn_accent': '#8b5cf6',      # Purple - special features
            'btn_accent_hover': '#7c3aed',
            'btn_neutral': '#9ca3af',     # Default button color
            'btn_neutral_hover': '#6b7280',
        }
        
        # User metadata for summary enhancement
        self.user_metadata = {
            'object_name': '',
            'telescope_instrument': '',
            'observation_date': '',
            'observer': '',
            'specific_request': ''
        }
        
        # Chat conversation history
        self.conversation_history = []
        
        # UI Components
        self.notebook = None
        self.summary_text_widget = None
        self.chat_display = None
        self.chat_input = None
        self.metadata_widgets = {}
        
        # AI generation settings
        self.max_tokens_var = tk.IntVar(value=3000)
        self.temperature_var = tk.DoubleVar(value=0.7)
        
    def show(self, snid_results=None):
        """Show the enhanced AI assistant dialog."""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.current_snid_results = snid_results
        
        self.window = tk.Toplevel(self.gui.master)
        
        # Use universal window manager if available
        if self.window_manager:
            _LOGGER.debug("🪟 Using universal window manager for AI Assistant dialog")
            self.dialog_id = self.window_manager.setup_dialog(
                self.window, 
                "🤖 SNID AI Assistant",
                size=DialogSize.LARGE,
                min_size=(1000, 800),
                resizable=True,
                modal=False,  # Changed to False to enable Windows buttons like Galaxy dialog
                parent=self.gui.master,
                enable_fullscreen=True
            )
        else:
            _LOGGER.debug("⚠️ Falling back to manual window setup for AI Assistant dialog")
            # Fallback setup with OS-aware window controls
            self.window.title("🤖 SNID AI Assistant")
            self.window.geometry("1200x900")
            # Removed transient() and grab_set() to enable Windows buttons like Galaxy dialog
            
            # Enable standard window controls (minimize, maximize, close)
            self.window.resizable(True, True)
            self.window.minsize(800, 600)
        
        self.window.configure(bg=self.colors['bg_primary'])
        
        # Setup cleanup
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Create main interface
        self._create_main_interface()
        
        if not self.window_manager:
            self._center_window()
    
    def _create_main_interface(self):
        """Create the main interface with tabbed layout."""
        # Main container
        main_container = tk.Frame(self.window, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Create header with settings menu
        self._create_header_with_settings(main_container)
        
        # Create tabbed interface
        self._create_tabbed_interface(main_container)
    
    def _create_header_with_settings(self, parent):
        """Create header with title and settings menu in top-right."""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 25))
        
        # Left side - Configuration button and status indicator
        title_section = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_section.pack(side='left', fill='x', expand=True)
        
        # Configuration button with icon (same red as redshift button)
        config_btn = tk.Button(title_section, 
                               text="⚙️ Configure AI",
                               bg="#FF6361",  # Same red as redshift button (ButtonColors.CORAL)
                               fg="white",
                               relief='raised', bd=2,
                               padx=15, pady=8,
                               command=self._configure_ai_backend)
        if self.font_manager:
            apply_font_to_widget(config_btn, FontCategory.BODY_SMALL, 'bold')
        else:
            config_btn.configure(font=('Segoe UI', 12, 'bold'))
        config_btn.pack(side='left')
        
        # Status indicator next to configure button
        self._create_status_indicator(title_section)
        
        # Right side - AI Summary and Chat buttons (removed Info button)
        buttons_section = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        buttons_section.pack(side='right')
        
        # AI Summary button
        self.summary_btn = tk.Button(buttons_section, 
                                   text="⭐ AI Summary",
                                   bg=self.colors['btn_accent'],
                                   fg=self.colors['text_on_accent'],
                                   relief='raised', bd=2,
                                   padx=15, pady=8,  # Reduced padding
                                   command=lambda: self._switch_tab('summary'))
        if self.font_manager:
            apply_font_to_widget(self.summary_btn, FontCategory.BODY_SMALL, 'bold')
        else:
            self.summary_btn.configure(font=('Segoe UI', 12, 'bold'))  # Reduced font size
        self.summary_btn.pack(side='left', padx=(0, 8))
        
        # Chat button
        self.chat_btn = tk.Button(buttons_section, 
                                text="💬 Chat",
                                bg=self.colors['btn_secondary'],
                                fg=self.colors['text_on_accent'],
                                relief='raised', bd=2,
                                padx=15, pady=8,  # Reduced padding
                                command=lambda: self._switch_tab('chat'))
        if self.font_manager:
            apply_font_to_widget(self.chat_btn, FontCategory.BODY_SMALL)
        else:
            self.chat_btn.configure(font=('Segoe UI', 12))  # Reduced font size
        self.chat_btn.pack(side='left', padx=(0, 8))
    
    def _create_status_indicator(self, parent):
        """Create AI backend status indicator."""
        # Check if LLM is available
        llm_available = hasattr(self.gui, 'llm_integration') and self.gui.llm_integration.llm_available
        
        if llm_available:
            status_text = "🟢 AI Ready"
            status_color = self.colors['btn_success']
        else:
            status_text = "🔴 AI Not Configured"
            status_color = self.colors['btn_danger']
        
        status_label = tk.Label(parent, text=status_text,
                               fg=status_color,
                               bg=self.colors['bg_primary'])
        if self.font_manager:
            apply_font_to_widget(status_label, FontCategory.BODY_SMALL)
        else:
            status_label.configure(font=('Segoe UI', 11))  # Reduced from 13
        status_label.pack(side='left', padx=(10, 0))
    
    def _create_tabbed_interface(self, parent):
        """Create the tabbed interface for summary and chat."""
        # Create custom tabbed interface using tk widgets instead of ttk to avoid styling conflicts
        self.tab_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        self.tab_container.pack(fill='both', expand=True)
        
        # Create content frame (no tab buttons needed since they're in header)
        self.tab_content_frame = tk.Frame(self.tab_container, bg=self.colors['bg_primary'])
        self.tab_content_frame.pack(fill='both', expand=True)
        
        # Create tab content frames
        self.tab_frames = {}
        self.tab_frames['summary'] = self._create_summary_tab()
        self.tab_frames['chat'] = self._create_chat_tab()
        
        # Show summary tab by default
        self._switch_tab('summary')
    
    def _switch_tab(self, tab_name):
        """Switch to the specified tab."""
        # Hide all tab content
        for frame in self.tab_frames.values():
            frame.pack_forget()
        
        # Reset all header button styles
        self.summary_btn.config(
            bg=self.colors['btn_secondary'],
            fg=self.colors['text_on_accent'],
            relief='raised', bd=2
        )
        self.chat_btn.config(
            bg=self.colors['btn_secondary'],
            fg=self.colors['text_on_accent'],
            relief='raised', bd=2
        )
        
        # Show selected tab content
        self.tab_frames[tab_name].pack(in_=self.tab_content_frame, fill='both', expand=True)
        
        # Highlight selected header button
        if tab_name == 'summary':
            self.summary_btn.config(
                bg=self.colors['btn_accent'],
                fg=self.colors['text_on_accent'],
                relief='raised', bd=2
            )
        elif tab_name == 'chat':
            self.chat_btn.config(
                bg=self.colors['btn_accent'],
                fg=self.colors['text_on_accent'],
                relief='raised', bd=2
            )
    
    def _create_summary_tab(self):
        """Create the summary tab."""
        summary_frame = tk.Frame(self.tab_content_frame, bg=self.colors['bg_secondary'])
        
        # Create metadata section (only for summary tab)
        self._create_metadata_section(summary_frame)
        
        # Summary generation controls
        self._create_summary_controls(summary_frame)
        
        # Summary display area
        self._create_summary_display(summary_frame)
        
        return summary_frame
    
    def _create_chat_tab(self):
        """Create the chat tab."""
        chat_frame = tk.Frame(self.tab_content_frame, bg=self.colors['bg_secondary'])
        
        # Chat display area
        self._create_chat_display(chat_frame)
        
        # Chat input area
        self._create_chat_input(chat_frame)
        
        return chat_frame
    
    def _create_chat_display(self, parent):
        """Create chat display area."""
        display_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        display_frame.pack(fill='both', expand=True, padx=20, pady=(20, 10))
        
        # Title
        title_label = tk.Label(display_frame, text="💬 AI Chat Assistant",
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 16, 'bold'))  # Reduced from 18
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Chat display with scrollbar
        chat_container = tk.Frame(display_frame, bg=self.colors['bg_secondary'])
        chat_container.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(chat_container)
        scrollbar.pack(side='right', fill='y')
        
        self.chat_display = tk.Text(chat_container,
                                   wrap='word',
                                   bg=self.colors['bg_primary'],
                                   fg=self.colors['text_primary'],
                                   yscrollcommand=scrollbar.set,
                                   relief='solid', bd=1,
                                   font=('Segoe UI', 12))  # Reduced from 14
        self.chat_display.pack(fill='both', expand=True, side='left')
        scrollbar.config(command=self.chat_display.yview)
        
        # Add welcome message
        self._add_chat_message("🤖 AI Assistant", 
                              "Hello! I'm here to help you analyze your supernova spectral identification results. Ask me anything about your SNID analysis, classification confidence, redshift reliability, or request scientific summaries!", 
                              is_user=False)
    
    def _create_chat_input(self, parent):
        """Create chat input area."""
        input_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        input_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        # Input text area
        text_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        text_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(text_frame, text="Your Message:",
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                font=('Segoe UI', 12)).pack(anchor='w')  # Reduced from 14
        
        # Text input with scrollbar
        input_container = tk.Frame(text_frame, bg=self.colors['bg_secondary'])
        input_container.pack(fill='x', pady=(5, 0))
        
        input_scrollbar = tk.Scrollbar(input_container)
        input_scrollbar.pack(side='right', fill='y')
        
        self.chat_input = tk.Text(input_container,
                                 height=3,
                                 wrap='word',
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_primary'],
                                 yscrollcommand=input_scrollbar.set,
                                 relief='solid', bd=1,
                                 font=('Segoe UI', 12))  # Reduced from 14
        self.chat_input.pack(fill='x', side='left', expand=True)
        input_scrollbar.config(command=self.chat_input.yview)
        
        # Bind Enter key to send message
        self.chat_input.bind('<Return>', self._on_chat_enter)
        self.chat_input.bind('<Shift-Return>', lambda e: None)  # Allow Shift+Enter for new line
        
        # Send button
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        button_frame.pack(fill='x')
        
        self.send_btn = tk.Button(button_frame,
                                 text="🚀 Send Message",
                                 bg=self.colors['btn_accent'],
                                 fg=self.colors['text_on_accent'],
                                 relief='raised', bd=2,
                                 padx=20, pady=8,  # Reduced from 25, 12
                                 command=self._send_chat_message,
                                 font=('Segoe UI', 12, 'bold'))  # Reduced from 14
        self.send_btn.pack(side='left')
        
        # --- NEW: Chat generation settings (tokens & temperature) ---
        settings_frame = tk.Frame(button_frame, bg=self.colors['bg_secondary'])
        settings_frame.pack(side='left', padx=(15, 0))

        # Max tokens control for chat
        tk.Label(settings_frame, text="Chat Tokens:", bg=self.colors['bg_secondary'], fg=self.colors['text_primary'], font=('Segoe UI', 11)).pack(side='left', padx=(0,4))
        self.chat_max_tokens_var = tk.IntVar(value=2000)  # Higher default for chat
        tk.Spinbox(settings_frame, from_=500, to=8000, increment=500, width=6, textvariable=self.chat_max_tokens_var, font=('Segoe UI', 11)).pack(side='left', padx=(0,10))

        # Temperature control for chat
        tk.Label(settings_frame, text="Temp:", bg=self.colors['bg_secondary'], fg=self.colors['text_primary'], font=('Segoe UI', 11)).pack(side='left', padx=(0,4))
        self.chat_temperature_var = tk.DoubleVar(value=0.7)
        tk.Spinbox(settings_frame, from_=0.0, to=1.0, increment=0.05, format="%.2f", width=4, textvariable=self.chat_temperature_var, font=('Segoe UI', 11)).pack(side='left', padx=(0,15))
        
        # Clear chat button
        clear_btn = tk.Button(button_frame,
                             text="🗑️ Clear Chat",
                             bg=self.colors['btn_danger'],
                             fg=self.colors['text_on_accent'],
                             relief='raised', bd=2,
                             padx=15, pady=8,  # Reduced from 20, 12
                             command=self._clear_chat,
                             font=('Segoe UI', 12))  # Reduced from 14
        clear_btn.pack(side='right')
    
    def _create_metadata_section(self, parent):
        """Create user metadata input section."""
        metadata_frame = tk.LabelFrame(parent, text="📋 Observation Details",
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['text_primary'],
                                      relief='raised', bd=2,
                                      font=('Segoe UI', 14, 'bold'))  # Reduced from 16
        metadata_frame.pack(fill='x', padx=20, pady=(5, 10))
        
        # Create grid for metadata inputs
        grid_frame = tk.Frame(metadata_frame, bg=self.colors['bg_secondary'])
        grid_frame.pack(fill='x', padx=15, pady=15)
        
        # Object name
        tk.Label(grid_frame, text="Object Name:",
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                font=('Segoe UI', 12)).grid(row=0, column=0, sticky='w', padx=(0, 15))  # Reduced from 14
        
        self.metadata_widgets['object_name'] = tk.Entry(grid_frame, width=20,
                                                       bg=self.colors['bg_primary'],
                                                       fg=self.colors['text_primary'],
                                                       relief='solid', bd=1,
                                                       font=('Segoe UI', 12))  # Reduced from 14
        self.metadata_widgets['object_name'].grid(row=0, column=1, sticky='w', padx=(0, 25))
        
        # Telescope/Instrument
        tk.Label(grid_frame, text="Telescope/Instrument:",
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                font=('Segoe UI', 12)).grid(row=0, column=2, sticky='w', padx=(0, 15))  # Reduced from 14
        
        self.metadata_widgets['telescope_instrument'] = tk.Entry(grid_frame, width=25,
                                                               bg=self.colors['bg_primary'],
                                                               fg=self.colors['text_primary'],
                                                               relief='solid', bd=1,
                                                               font=('Segoe UI', 12))  # Reduced from 14
        self.metadata_widgets['telescope_instrument'].grid(row=0, column=3, sticky='w', padx=(0, 25))
        
        # Observation date
        tk.Label(grid_frame, text="Observation Date:",
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                font=('Segoe UI', 12)).grid(row=0, column=4, sticky='w', padx=(0, 15))  # Reduced from 14
        
        self.metadata_widgets['observation_date'] = tk.Entry(grid_frame, width=20,
                                                            bg=self.colors['bg_primary'],
                                                            fg=self.colors['text_primary'],
                                                            relief='solid', bd=1,
                                                            font=('Segoe UI', 12))  # Reduced from 14
        self.metadata_widgets['observation_date'].grid(row=0, column=5, sticky='w')
        
        # Observer
        tk.Label(grid_frame, text="Observer:",
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                font=('Segoe UI', 12)).grid(row=0, column=6, sticky='w', padx=(25, 15))  # Reduced from 14
        
        self.metadata_widgets['observer'] = tk.Entry(grid_frame, width=20,
                                                    bg=self.colors['bg_primary'],
                                                    fg=self.colors['text_primary'],
                                                    relief='solid', bd=1,
                                                    font=('Segoe UI', 12))  # Reduced from 14
        self.metadata_widgets['observer'].grid(row=0, column=7, sticky='w')
        
        # Specific request
        notes_frame = tk.Frame(metadata_frame, bg=self.colors['bg_secondary'])
        notes_frame.pack(fill='both', expand=True, padx=15, pady=(15, 15))
        
        tk.Label(notes_frame, text="Specific Request (e.g., 'Format as AstroNote for TNS', 'Journal-style summary', etc.):",
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                font=('Segoe UI', 12)).pack(anchor='w')  # Reduced from 14
        
        # Text input with scrollbar for specific request
        notes_container = tk.Frame(notes_frame, bg=self.colors['bg_secondary'])
        notes_container.pack(fill='both', expand=True, pady=(8, 0))
        
        notes_scrollbar = tk.Scrollbar(notes_container)
        notes_scrollbar.pack(side='right', fill='y')
        
        self.metadata_widgets['specific_request'] = tk.Text(notes_container, height=6,
                                                           bg=self.colors['bg_primary'],
                                                           fg=self.colors['text_primary'],
                                                           wrap='word',
                                                           relief='solid', bd=1,
                                                           yscrollcommand=notes_scrollbar.set,
                                                           font=('Segoe UI', 11))  # Reduced from 13
        self.metadata_widgets['specific_request'].pack(fill='both', side='left', expand=True)
        notes_scrollbar.config(command=self.metadata_widgets['specific_request'].yview)
    
    def _create_summary_controls(self, parent):
        """Create simplified summary generation controls."""
        controls_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        controls_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Generation button
        button_frame = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        button_frame.pack(fill='x')
        
        self.generate_btn = tk.Button(button_frame, 
                                     text="✨ Generate AI Summary",
                                     bg=self.colors['btn_accent'],
                                     fg=self.colors['text_on_accent'],
                                     relief='raised', bd=2,
                                     padx=20, pady=10,  # Reduced from 25, 12
                                     command=self._generate_summary)
        if self.font_manager:
            apply_font_to_widget(self.generate_btn, FontCategory.BODY_SMALL, 'bold')
        else:
            self.generate_btn.configure(font=('Segoe UI', 14, 'bold'))  # Reduced from 16
        self.generate_btn.pack(side='left')
        
        # Export buttons
        export_frame = tk.Frame(button_frame, bg=self.colors['bg_secondary'])
        export_frame.pack(side='right')
        
        copy_btn = tk.Button(export_frame, text="📋 Copy",
                            bg=self.colors['btn_info'],
                            fg=self.colors['text_on_accent'],
                            relief='raised', bd=2,
                            padx=12, pady=6,  # Reduced from 15, 8
                            command=self._copy_summary)
        copy_btn.configure(font=('Segoe UI', 12))  # Reduced from 14
        copy_btn.pack(side='left', padx=(0, 8))
        
        save_btn = tk.Button(export_frame, text="💾 Save",
                            bg=self.colors['btn_success'],
                            fg=self.colors['text_on_accent'],
                            relief='raised', bd=2,
                            padx=12, pady=6,  # Reduced from 15, 8
                            command=self._save_summary)
        save_btn.configure(font=('Segoe UI', 12))  # Reduced from 14
        save_btn.pack(side='left')
        
        # --- NEW: Generation settings (tokens & temperature) ---
        settings_frame = tk.Frame(button_frame, bg=self.colors['bg_secondary'])
        settings_frame.pack(side='left', padx=(15, 0))

        # Max tokens control
        tk.Label(settings_frame, text="Tokens:", bg=self.colors['bg_secondary'], fg=self.colors['text_primary'], font=('Segoe UI', 11)).pack(side='left', padx=(0,4))
        tk.Spinbox(settings_frame, from_=256, to=4096, increment=256, width=6, textvariable=self.max_tokens_var, font=('Segoe UI', 11)).pack(side='left', padx=(0,10))

        # Temperature control
        tk.Label(settings_frame, text="Temp:", bg=self.colors['bg_secondary'], fg=self.colors['text_primary'], font=('Segoe UI', 11)).pack(side='left', padx=(0,4))
        tk.Spinbox(settings_frame, from_=0.0, to=1.0, increment=0.05, format="%.2f", width=4, textvariable=self.temperature_var, font=('Segoe UI', 11)).pack(side='left')
    
    def _create_summary_display(self, parent):
        """Create summary display area."""
        display_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        display_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        # Scrollable text widget
        text_frame = tk.Frame(display_frame, bg=self.colors['bg_secondary'])
        text_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.summary_text_widget = tk.Text(text_frame,
                                          wrap='word',
                                          bg=self.colors['bg_primary'],
                                          fg=self.colors['text_primary'],
                                          yscrollcommand=scrollbar.set,
                                          relief='solid', bd=1)
        if self.font_manager:
            apply_font_to_widget(self.summary_text_widget, FontCategory.BODY_SMALL)
        else:
            self.summary_text_widget.configure(font=('Segoe UI', 12))  # Reduced from 14
        self.summary_text_widget.pack(fill='both', expand=True)
        scrollbar.config(command=self.summary_text_widget.yview)
        
        # Initial placeholder text
        placeholder_text = """🤖 Welcome to the SNID AI Assistant!

This tool analyzes your supernova spectral identification results and generates professional scientific summaries.

What this tool can do:
• Analyze SNID template matching results
• Evaluate classification confidence and alternatives
• Assess redshift reliability and systematic effects
• Identify key spectral features and their physics
• Generate TNS-compatible AstroNote reports
• Provide scientific context and follow-up recommendations

To get started:
1. Fill in the observation details above (optional but recommended)
2. Select your preferred analysis type
3. Click "Generate AI Summary"

The AI has access to your current SNID analysis results and will provide context-aware analysis based on the spectral matching pipeline output."""
        
        self.summary_text_widget.insert('1.0', placeholder_text)
        self.summary_text_widget.config(state='disabled')
    
    def _add_chat_message(self, sender, message, is_user=True):
        """Add a message to the chat display."""
        self.chat_display.config(state='normal')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format message
        if is_user:
            prefix = f"[{timestamp}] 👤 You:\n"
            self.chat_display.insert(tk.END, prefix)
            self.chat_display.insert(tk.END, f"{message}\n\n")
        else:
            prefix = f"[{timestamp}] 🤖 AI Assistant:\n"
            self.chat_display.insert(tk.END, prefix)
            self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def _on_chat_enter(self, event):
        """Handle Enter key in chat input."""
        if event.state & 0x1:  # Shift key pressed
            return  # Allow Shift+Enter for new line
        else:
            self._send_chat_message()
            return 'break'  # Prevent default Enter behavior
    
    def _send_chat_message(self):
        """Send chat message to AI."""
        message = self.chat_input.get('1.0', tk.END).strip()
        if not message:
            return
        
        # Check if AI backend is available
        if not hasattr(self.gui, 'llm_integration') or not self.gui.llm_integration.llm_available:
            messagebox.showerror("Error", "AI backend is not configured.\n\nPlease configure an AI backend in the settings menu.")
            return
        
        # Add user message to chat
        self._add_chat_message("You", message, is_user=True)
        
        # Clear input
        self.chat_input.delete('1.0', tk.END)
        
        # Disable send button
        self.send_btn.config(state='disabled', text="🤖 Thinking...")
        
        # Send to AI in background thread
        threading.Thread(target=self._chat_with_ai_thread, args=(message,), daemon=True).start()
    
    def _chat_with_ai_thread(self, message):
        """Chat with AI in background thread."""
        try:
            # Collect user metadata for enhanced context
            self._collect_user_metadata()
            
            # Get user-configured token and temperature settings
            try:
                max_tokens = int(self.chat_max_tokens_var.get())
            except Exception:
                max_tokens = 2000
            try:
                temperature = float(self.chat_temperature_var.get())
            except Exception:
                temperature = 0.7

            # Clamp to valid ranges
            max_tokens = max(500, min(max_tokens, 8000))
            temperature = max(0.0, min(temperature, 1.0))
            
            # Build context from SNID results using the simplified integration
            context = ""
            if hasattr(self.gui, 'llm_integration'):
                # Format the SNID results as context with user metadata
                context = self.gui.llm_integration.format_snid_results_for_llm(self.user_metadata)
            
            # Get AI response with enhanced context including user metadata
            if hasattr(self.gui, 'llm_integration'):
                response = self.gui.llm_integration.chat_with_llm(
                    message=message,
                    context=context,
                    user_metadata=self.user_metadata,
                    max_tokens=max_tokens
                )
                
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": message})
                self.conversation_history.append({"role": "assistant", "content": response})
                
                # Update UI on main thread
                self.window.after(0, self._on_chat_response, response)
            else:
                raise Exception("LLM integration not available")
                
        except Exception as e:
            error_msg = f"Error communicating with AI: {str(e)}"
            self.window.after(0, self._on_chat_error, error_msg)
    
    def _build_chat_context(self, user_message):
        """Build context-aware chat message."""
        context_parts = []
        
        # Add SNID results context if available
        if self.current_snid_results:
            context_parts.append("I'm analyzing SNID spectral identification results.")
            
            # Add basic classification info
            if 'result' in self.current_snid_results:
                result = self.current_snid_results['result']
                if hasattr(result, 'consensus_type'):
                    context_parts.append(f"Current classification: {result.consensus_type}")
                if hasattr(result, 'redshift'):
                    context_parts.append(f"Redshift: {result.redshift:.4f}")
        
        # Add user metadata context
        if any(self.user_metadata.values()):
            context_parts.append("Observation details:")
            for key, value in self.user_metadata.items():
                if value:
                    context_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        # Combine context with user message
        if context_parts:
            context_str = "\n".join(context_parts)
            return f"Context: {context_str}\n\nQuestion: {user_message}"
        else:
            return user_message
    
    def _on_chat_response(self, response):
        """Handle AI chat response."""
        self.send_btn.config(state='normal', text="🚀 Send Message")
        self._add_chat_message("AI Assistant", response, is_user=False)
    
    def _on_chat_error(self, error_msg):
        """Handle AI chat error."""
        self.send_btn.config(state='normal', text="🚀 Send Message")
        self._add_chat_message("AI Assistant", f"❌ Error: {error_msg}", is_user=False)
    
    def _clear_chat(self):
        """Clear chat history."""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            self.chat_display.config(state='normal')
            self.chat_display.delete('1.0', tk.END)
            self.chat_display.config(state='disabled')
            self.conversation_history.clear()
            
            # Add welcome message back
            self._add_chat_message("🤖 AI Assistant", 
                                  "Chat cleared! How can I help you with your spectral analysis?", 
                                  is_user=False)
    
    def _configure_ai_backend(self):
        """Open AI backend configuration dialog (OpenRouter)"""
        try:
            # Import the configuration dialog creator directly
            from snid_sage.interfaces.llm.openrouter.openrouter_llm import configure_openrouter_dialog
            
            # Open the dialog with the assistant window as the parent so it appears on top
            dialog = configure_openrouter_dialog(self.window)
            
            # When the dialog closes, re-check configuration so status indicator refreshes
            def on_close():
                try:
                    if hasattr(self.gui, 'llm_integration'):
                        # Re-validate configuration after short delay (write may be async)
                        self.window.after(500, self._refresh_ai_status)
                except Exception as exc:
                    messagebox.showwarning("Configuration", f"Error checking configuration: {exc}")
                finally:
                    dialog.destroy()
            
            dialog.protocol("WM_DELETE_WINDOW", on_close)
        except ImportError as e:
            messagebox.showerror("Configuration Error", f"OpenRouter configuration module not available:\n\n{e}")
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Error opening OpenRouter configuration:\n\n{e}")
    
    def _update_status_indicator(self):
        """Update the AI status indicator."""
        # This would update the status indicator in the header
        # Implementation depends on keeping a reference to the status label
        pass
    
    def _refresh_ai_status(self):
        """Refresh the AI status after configuration changes."""
        try:
            if hasattr(self.gui, 'llm_integration'):
                # Try to call the LLM integration's configuration check method
                if hasattr(self.gui.llm_integration, '_check_configuration_success'):
                    self.gui.llm_integration._check_configuration_success()
                else:
                    # Fallback: just check if LLM is available
                    if hasattr(self.gui.llm_integration, 'llm_available'):
                        if self.gui.llm_integration.llm_available:
                            print("✅ AI backend is configured and available")
                        else:
                            print("⚠️ AI backend is not configured")
        except Exception as e:
            print(f"⚠️ Error refreshing AI status: {e}")
    
    def _generate_summary(self):
        """Generate AI summary based on current settings."""
        if not hasattr(self.gui, 'llm_integration') or not self.gui.llm_integration.llm_available:
            messagebox.showerror("Error", "AI backend is not configured.\n\nPlease configure an AI backend in the settings menu.")
            return
        
        if self.is_generating:
            messagebox.showwarning("Generation in Progress", "Please wait for the current generation to complete.")
            return
        
        # Get user metadata
        self._collect_user_metadata()
        
        # Update UI
        self.is_generating = True
        self.generate_btn.config(text="⏳ Generating...", state='disabled')
        
        # Clear previous results
        self.summary_text_widget.config(state='normal')
        self.summary_text_widget.delete('1.0', tk.END)
        self.summary_text_widget.insert('1.0', "🤖 Generating AI analysis...\n\nPlease wait while I analyze your SNID results...")
        self.summary_text_widget.config(state='disabled')
        
        # Generate in background thread
        threading.Thread(target=self._generate_summary_thread, daemon=True).start()
    
    def _collect_user_metadata(self):
        """Collect user metadata from form."""
        # Only collect metadata if the widgets exist (i.e., if we're on the summary tab)
        if hasattr(self, 'metadata_widgets') and self.metadata_widgets:
            for key, widget in self.metadata_widgets.items():
                if isinstance(widget, tk.Text):
                    self.user_metadata[key] = widget.get('1.0', tk.END).strip()
                else:
                    self.user_metadata[key] = widget.get().strip()
    
    def _generate_summary_thread(self):
        """Generate summary in background thread."""
        try:
            # Retrieve user-defined generation settings
            try:
                max_tokens = int(self.max_tokens_var.get())
            except Exception:
                max_tokens = 3000
            try:
                temperature = float(self.temperature_var.get())
            except Exception:
                temperature = 0.7

            # Clamp to valid ranges
            max_tokens = max(256, min(max_tokens, 4096))
            temperature = max(0.0, min(temperature, 1.0))

            # Generate summary using LLM integration
            if hasattr(self.gui, 'llm_integration'):
                result = self.gui.llm_integration.generate_summary(
                    user_metadata=self.user_metadata,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                # Handle both tuple return and single string return for compatibility
                if isinstance(result, tuple):
                    summary_text = result[0]  # Get just the summary text from tuple
                else:
                    summary_text = result  # Backward compatibility if it returns just string
            else:
                raise Exception("LLM integration not available")
            
            # Update UI on main thread
            self.window.after(0, self._on_summary_complete, summary_text)
            
        except Exception as e:
            error_msg = f"Failed to generate summary: {str(e)}"
            self.window.after(0, self._on_summary_error, error_msg)
    
    def _build_enhanced_context(self):
        """Build enhanced context for LLM analysis."""
        context = {
            'tool_description': """You are analyzing results from Python SNID (SuperNova IDentification), a spectral template matching pipeline for supernova classification. This tool performs cross-correlation analysis between observed spectra and template libraries to identify supernova types and estimate redshifts.""",
            'snid_results': self.current_snid_results,
            'user_metadata': self.user_metadata,
            'analysis_capabilities': [
                "Template cross-correlation matching",
                "Redshift estimation via spectral fitting",
                "Type classification with confidence assessment",
                "Spectral line identification",
                "Quality metrics and reliability assessment"
            ]
        }
        return context
    
    def _on_summary_complete(self, summary_text):
        """Handle summary generation completion."""
        self.is_generating = False
        self.generate_btn.config(text="✨ Generate AI Summary", state='normal')
        
        # Display results
        self.summary_text_widget.config(state='normal')
        self.summary_text_widget.delete('1.0', tk.END)
        self.summary_text_widget.insert('1.0', summary_text)
        self.summary_text_widget.config(state='disabled')
    
    def _on_summary_error(self, error_msg):
        """Handle summary generation error."""
        self.is_generating = False
        self.generate_btn.config(text="✨ Generate AI Summary", state='normal')
        
        # Display error
        self.summary_text_widget.config(state='normal')
        self.summary_text_widget.delete('1.0', tk.END)
        self.summary_text_widget.insert('1.0', f"❌ Error generating summary:\n\n{error_msg}")
        self.summary_text_widget.config(state='disabled')
        
        messagebox.showerror("Generation Error", error_msg)
    
    def _copy_summary(self):
        """Copy summary to clipboard."""
        summary_text = self.summary_text_widget.get('1.0', tk.END).strip()
        if summary_text:
            self.window.clipboard_clear()
            self.window.clipboard_append(summary_text)
            messagebox.showinfo("Copied", "Summary copied to clipboard!")
        else:
            messagebox.showwarning("No Content", "No summary to copy.")
    
    def _save_summary(self):
        """Save summary to file."""
        summary_text = self.summary_text_widget.get('1.0', tk.END).strip()
        if not summary_text:
            messagebox.showwarning("No Content", "No summary to save.")
            return
        
        # Get default filename
        object_name = self.user_metadata.get('object_name', 'unknown_object')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{object_name}_ai_summary_{timestamp}.txt"
        
        # Save dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialvalue=default_filename
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(summary_text)
                messagebox.showinfo("Saved", f"Summary saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
    
    def _center_window(self):
        """Center the window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def _on_window_close(self):
        """Handle window close event."""
        if self.is_generating:
            if messagebox.askyesno("Generation in Progress", 
                                 "AI generation is in progress. Do you want to close anyway?"):
                self.window.destroy()
        else:
            self.window.destroy()


# Backward compatibility alias
AISummaryDialog = EnhancedAIAssistantDialog 