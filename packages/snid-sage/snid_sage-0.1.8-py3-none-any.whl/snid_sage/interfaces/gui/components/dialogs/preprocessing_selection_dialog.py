"""
SNID SAGE - Preprocessing Selection Dialog
========================================

Simple dialog to choose between quick and advanced preprocessing options.
Uses radio button style similar to redshift selection dialog.
"""

import tkinter as tk
from tkinter import ttk
import logging

_LOGGER = logging.getLogger(__name__)


class PreprocessingSelectionDialog:
    """Dialog for selecting preprocessing mode"""
    
    def __init__(self, parent_gui):
        """Initialize preprocessing selection dialog
        
        Parameters:
        -----------
        parent_gui : ModernSNIDSageGUI
            Reference to the main GUI instance
        """
        self.gui = parent_gui
        self.window = None
        self.selection = None
        
        # Color scheme matching redshift dialog
        self.colors = {
            'bg': '#f8fafc',
            'panel_bg': '#ffffff',
            'primary': '#3b82f6',
            'success': '#22c55e',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'text_primary': '#1e293b',
            'text_secondary': '#64748b',
            'border': '#e2e8f0',
            'hover': '#f1f5f9'
        }
        
        # Override all text-related colours to black for a consistent monochrome look
        for key in ['primary', 'success', 'warning', 'danger', 'text_primary', 'text_secondary']:
            self.colors[key] = 'black'
    
    def show(self):
        """Show the preprocessing selection dialog"""
        if self.window:
            return
        
        self._create_dialog()
        self._center_window()
        
        # Make it modal
        self.window.transient(self.gui.master)
        self.window.grab_set()
        
        # Focus the window
        self.window.focus_set()
        
        # Wait for dialog to close
        self.window.wait_window()
    
    def _create_dialog(self):
        """Create the dialog window"""
        self.window = tk.Toplevel(self.gui.master)
        self.window.title("Preprocess Spectrum")
        self.window.geometry("600x480")  # Previously 550
        self.window.configure(bg=self.colors['bg'])
        self.window.resizable(False, False)
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Create main frame
        main_frame = tk.Frame(self.window, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        self._create_header(main_frame)
        self._create_mode_options(main_frame)
        self._create_buttons(main_frame)
    
    def _center_window(self):
        """Center the window on the parent"""
        self.window.update_idletasks()
        
        # Get dialog dimensions
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Get parent window position and size
        parent_x = self.gui.master.winfo_rootx()
        parent_y = self.gui.master.winfo_rooty()
        parent_width = self.gui.master.winfo_width()
        parent_height = self.gui.master.winfo_height()
        
        # Calculate centered position
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        # Ensure dialog is within screen bounds
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_header(self, parent):
        """Create dialog header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🔧 Spectrum Preprocessing",
                              font=('Segoe UI', 20, 'bold'),
                              fg=self.colors['primary'],
                              bg=self.colors['bg'])
        title_label.pack()
        
        # Description
        desc_label = tk.Label(header_frame,
                             text="Choose your preprocessing approach:",
                             font=('Segoe UI', 14, 'normal'),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg'])
        desc_label.pack(pady=(10, 0))
    
    def _create_mode_options(self, parent):
        """Create mode selection options using radio buttons"""
        options_frame = tk.Frame(parent, bg=self.colors['bg'])
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Mode selection variable
        self.mode_var = tk.StringVar(value="quick")
        
        # Quick preprocessing option
        quick_frame = tk.Frame(options_frame, bg=self.colors['panel_bg'], relief='solid', bd=1)
        quick_frame.pack(fill='x', pady=(0, 15))  # Increased bottom padding for spacing
        
        quick_radio = tk.Radiobutton(quick_frame,
                                   text="⚡ Quick Preprocessing",
                                   variable=self.mode_var,
                                   value="quick",
                                   font=('Segoe UI', 15, 'bold'),
                                   fg=self.colors['success'],
                                   bg=self.colors['panel_bg'],
                                   selectcolor=self.colors['panel_bg'],
                                   activebackground=self.colors['panel_bg'])
        quick_radio.pack(anchor='w', padx=15, pady=(10, 5))
        
        quick_desc = tk.Label(quick_frame,
                            text="• Apply default SNID preprocessing steps automatically\n"
                                 "• Clipping operations, log-wavelength rebinning\n"
                                 "• Flux scaling, continuum fitting, apodization\n"
                                 "• Fast and straightforward - recommended for most cases",
                            font=('Segoe UI', 13, 'normal'),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['panel_bg'],
                            justify='left')
        quick_desc.pack(anchor='w', padx=35, pady=(0, 10))
        
        # Advanced preprocessing option
        advanced_frame = tk.Frame(options_frame, bg=self.colors['panel_bg'], relief='solid', bd=1)
        advanced_frame.pack(fill='x')
        
        advanced_radio = tk.Radiobutton(advanced_frame,
                                      text="🔧 Advanced Preprocessing",
                                      variable=self.mode_var,
                                      value="advanced",
                                      font=('Segoe UI', 15, 'bold'),
                                      fg=self.colors['primary'],
                                      bg=self.colors['panel_bg'],
                                      selectcolor=self.colors['panel_bg'],
                                      activebackground=self.colors['panel_bg'])
        advanced_radio.pack(anchor='w', padx=15, pady=(10, 5))
        
        advanced_desc = tk.Label(advanced_frame,
                               text="• Step-by-step interactive preprocessing wizard\n"
                                    "• Manual parameter control and interactive masking\n"
                                    "• Live preview with custom filtering options\n"
                                    "• Full control over each preprocessing step",
                               font=('Segoe UI', 13, 'normal'),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['panel_bg'],
                               justify='left')
        advanced_desc.pack(anchor='w', padx=35, pady=(0, 10))
    
    def _create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(side='bottom', fill='x', pady=(10, 0))
        
        # Cancel button
        cancel_btn = tk.Button(button_frame,
                              text="❌ Cancel",
                              font=('Segoe UI', 12, 'normal'),  # Reduced from 15 to 12
                              bg='#6b7280',
                              fg='white',
                              relief='raised',
                              bd=2,
                              padx=20,  # Reduced from 25 to 20
                              pady=8,   # Reduced from 12 to 8
                              cursor='hand2',
                              command=self.on_cancel)
        cancel_btn.pack(side='left', padx=(0, 15))  # Reduced spacing from 20 to 15
        
        # Apply button (made smaller to match redshift dialog)
        apply_btn = tk.Button(button_frame,
                             text="🚀 Start Preprocessing",
                             font=('Segoe UI', 12, 'bold'),
                             bg="#22c55e",  # Bright green background for emphasis
                             fg='white',
                             relief='raised',
                             bd=2,      # Reduced from 3 to 2
                             padx=20,   # Reduced from 30 to 20
                             pady=8,    # Reduced from 15 to 8
                             cursor='hand2',
                             command=self.on_apply)
        apply_btn.pack(side='right')
        
        # Bind Enter key to apply
        self.window.bind('<Return>', lambda e: self.on_apply())
        self.window.bind('<Escape>', lambda e: self.on_cancel())
        
        # Focus on apply button and make it default
        apply_btn.focus_set()
    
    def on_apply(self):
        """Handle apply button"""
        mode = self.mode_var.get()
        
        if mode == "quick":
            self.selection = 'quick'
            self.close_dialog()
            
            # Run quick preprocessing without showing the completion message
            if hasattr(self.gui, 'preprocessing_controller'):
                self.gui.preprocessing_controller.run_quick_snid_preprocessing_silent()
            else:
                _LOGGER.error("Preprocessing controller not available")
        
        elif mode == "advanced":
            self.selection = 'advanced'
            self.close_dialog()
            
            # Open advanced preprocessing dialog
            if hasattr(self.gui, 'preprocessing_controller'):
                self.gui.preprocessing_controller.run_manual_preprocessing_wizard()
            else:
                _LOGGER.error("Preprocessing controller not available")
    
    def on_cancel(self):
        """Handle cancel button"""
        self.selection = None
        self.close_dialog()
    
    def close_dialog(self):
        """Close the dialog"""
        if self.window:
            self.window.grab_release()
            self.window.destroy()
            self.window = None 
