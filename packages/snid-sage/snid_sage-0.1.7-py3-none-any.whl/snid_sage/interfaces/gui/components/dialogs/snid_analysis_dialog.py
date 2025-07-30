"""
SNID SAGE - Combined SNID Analysis Dialog
=========================================

A unified dialog that combines SNID options configuration and execution.
This replaces the separate "SNID Options" and "Run SNID" buttons with a single
"Analysis" button that opens this dialog.

Features:
- Default analysis mode (quick start with default settings)
- Advanced options mode (configure parameters then run)
- Modern tabbed interface
- Direct execution after configuration

Part of the SNID SAGE GUI system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, Callable
import threading
import time

# Import centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.snid_analysis_dialog')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.snid_analysis_dialog')

# Import the configuration dialog for advanced options
from snid_sage.interfaces.gui.components.dialogs.configuration_dialog import ModernSNIDOptionsDialog

# Import unified systems for OS-native window controls
try:
    from snid_sage.interfaces.gui.utils.universal_window_manager import get_window_manager, DialogSize
    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError:
    UNIFIED_SYSTEMS_AVAILABLE = False


class SNIDAnalysisDialog:
    """
    Combined SNID Analysis dialog with default and advanced modes.
    
    This dialog provides two main options:
    1. Run with Default Settings (default selected)
    2. Configure Advanced Options & Run
    """
    
    def __init__(self, parent, gui_instance):
        """
        Initialize the SNID Analysis dialog.
        
        Args:
            parent: Parent window
            gui_instance: Main GUI instance for accessing controllers and methods
        """
        self.parent = parent
        self.gui = gui_instance
        self.dialog = None
        self.result = None
        
        # Get unified window manager for OS-native controls
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager = get_window_manager()
        
        # Track selected mode
        self.selected_mode = tk.StringVar(value="default")
        
        # Color scheme matching preprocessing dialog
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
        
        # Force all dialog text to black for a unified monochrome appearance
        for key in ['primary', 'success', 'warning', 'danger', 'text_primary', 'text_secondary']:
            self.colors[key] = 'black'
        
        # Light theme colors are fixed to match preprocessing dialog
        # Don't override with parent theme to maintain consistency
    
    def show(self) -> Optional[str]:
        """Show the dialog and return the selected mode"""
        try:
    
            if hasattr(self.gui, 'theme_manager'):
                self.gui.theme_manager.disable_theme_application()
            elif hasattr(self.gui, 'master') and hasattr(self.gui.master, 'theme_manager'):
                self.gui.master.theme_manager.disable_theme_application()
            
            self._create_dialog()
            self._setup_interface()
            self._center_dialog()
            
            # Make it modal
            self.dialog.transient(self.gui.master)
            self.dialog.grab_set()
            
            # Focus the window
            self.dialog.focus_set()
            
            # Re-enable theme application after dialog is fully created
            if hasattr(self.gui, 'theme_manager'):
                self.gui.theme_manager.enable_theme_application()
            elif hasattr(self.gui, 'master') and hasattr(self.gui.master, 'theme_manager'):
                self.gui.master.theme_manager.enable_theme_application()
            
            # Wait for dialog to close
            self.dialog.wait_window()
            
            return self.result
            
        except Exception as e:
            # Ensure theme application is always re-enabled even if an error occurs
            try:
                if hasattr(self.gui, 'theme_manager'):
                    self.gui.theme_manager.enable_theme_application()
                elif hasattr(self.gui, 'master') and hasattr(self.gui.master, 'theme_manager'):
                    self.gui.master.theme_manager.enable_theme_application()
            except:
                pass
            raise e
    
    def _create_dialog(self):
        """Create the dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("SNID Analysis")
        self.dialog.geometry("600x480")
        self.dialog.configure(bg=self.colors['bg'])
        self.dialog.resizable(False, False)
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
    
    def _center_dialog(self):
        """Center the dialog on the parent"""
        self.dialog.update_idletasks()
        
        # Get dialog dimensions
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        
        # Get parent window position and size
        if hasattr(self.parent, 'master') and self.parent.master:
            parent_widget = self.parent.master
        else:
            parent_widget = self.parent
            
        try:
            parent_x = parent_widget.winfo_rootx()
            parent_y = parent_widget.winfo_rooty()
            parent_width = parent_widget.winfo_width()
            parent_height = parent_widget.winfo_height()
            
            # Calculate centered position
            x = parent_x + (parent_width - width) // 2
            y = parent_y + (parent_height - height) // 2
            
            # Ensure dialog is within screen bounds
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))
            
            self.dialog.geometry(f"{width}x{height}+{x}+{y}")
            
        except (AttributeError, tk.TclError):
            # Fallback: center on screen
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_interface(self):
        """Setup the dialog interface"""
        # Create main frame
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        self._create_header(main_frame)
        self._create_mode_options(main_frame)
        self._create_buttons(main_frame)
    
    def _create_header(self, parent):
        """Create dialog header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🚀 SNID Analysis",
                              font=('Segoe UI', 20, 'bold'),
                              fg=self.colors['primary'],
                              bg=self.colors['bg'])
        title_label.pack()
        
        # Description
        desc_label = tk.Label(header_frame,
                             text="Choose analysis mode and run supernova identification:",
                             font=('Segoe UI', 14, 'normal'),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg'])
        desc_label.pack(pady=(10, 0))
    
    def _create_mode_options(self, parent):
        """Create mode selection options using radio buttons"""
        options_frame = tk.Frame(parent, bg=self.colors['bg'])
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Mode selection variable
        self.mode_var = tk.StringVar(value="default")
        
        # Quick Analysis option
        quick_frame = tk.Frame(options_frame, bg=self.colors['panel_bg'], relief='solid', bd=1)
        quick_frame.pack(fill='x', pady=(0, 15))
        
        quick_radio = tk.Radiobutton(quick_frame,
                                   text="🚀 Quick Analysis (Default)",
                                   variable=self.mode_var,
                                   value="default",
                                   font=('Segoe UI', 15, 'bold'),
                                   fg=self.colors['success'],
                                   bg=self.colors['panel_bg'],
                                   selectcolor=self.colors['panel_bg'],
                                   activebackground=self.colors['panel_bg'])
        quick_radio.pack(anchor='w', padx=15, pady=(10, 5))
        
        quick_desc = tk.Label(quick_frame,
                            text="• Run SNID analysis with default parameters\n"
                                 "• Automatic redshift range and template matching\n"
                                 "• Fast and reliable for most cases\n"
                                 "• Perfect for standard supernova identification",
                            font=('Segoe UI', 13, 'normal'),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['panel_bg'],
                            justify='left')
        quick_desc.pack(anchor='w', padx=35, pady=(0, 10))
        
        # Advanced mode option
        advanced_frame = tk.Frame(options_frame, bg=self.colors['panel_bg'], relief='solid', bd=1)
        advanced_frame.pack(fill='x')
        
        advanced_radio = tk.Radiobutton(advanced_frame,
                                      text="⚙️ Configure Options & Run",
                                      variable=self.mode_var,
                                      value="advanced",
                                      font=('Segoe UI', 15, 'bold'),
                                      fg=self.colors['primary'],
                                      bg=self.colors['panel_bg'],
                                      selectcolor=self.colors['panel_bg'],
                                      activebackground=self.colors['panel_bg'])
        advanced_radio.pack(anchor='w', padx=15, pady=(10, 5))
        
        advanced_desc = tk.Label(advanced_frame,
                               text="• Configure advanced SNID parameters first\n"
                                    "• Custom redshift ranges and template filtering\n"
                                    "• Type restrictions and correlation settings\n"
                                    "• Then run analysis with custom settings",
                               font=('Segoe UI', 13, 'normal'),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['panel_bg'],
                               justify='left')
        advanced_desc.pack(anchor='w', padx=35, pady=(0, 10))
    
    def _mark_button_as_workflow_managed(self, button: tk.Button, button_name: str = "dialog_button"):
        """Dialog buttons use simple fixed colors and don't interact with the workflow system"""
        pass
    
    def _create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(side='bottom', fill='x', pady=(10, 0))
        
        # Cancel button
        cancel_btn = tk.Button(button_frame,
                              text="❌ Cancel",
                              font=('Segoe UI', 12, 'normal'),
                              bg='#6b7280',
                              fg='white',
                              relief='raised',
                              bd=2,
                              padx=20,
                              pady=8,
                              cursor='hand2',
                              command=self._cancel)
        cancel_btn.pack(side='left', padx=(0, 10))
        
        # Run button
        run_btn = tk.Button(button_frame,
                          text="🚀 Run SNID Analysis",
                          command=self._run_analysis,
                          bg='#22c55e', fg='white',
                          font=('Segoe UI', 12, 'bold'),
                          relief='raised', bd=2,
                          padx=25, pady=12,
                          cursor='hand2')
        run_btn.pack(side='right')
        
        # Bind Enter key to run analysis
        self.dialog.bind('<Return>', lambda e: self._run_analysis())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
        
        # Focus on run button and make it default
        run_btn.focus_set()
    
    def _run_analysis(self):
        """Execute the selected analysis mode"""
        mode = self.mode_var.get()
        
        if mode == "default":
            # Run with default settings
            self.result = "default"
            self.dialog.destroy()
            
            # Run analysis directly with default settings
            self._execute_default_analysis()
            
        elif mode == "advanced":
            # Open configuration dialog first, then run
            self.result = "advanced"
            self.dialog.destroy()
            
            # Show configuration dialog and then run
            self._execute_advanced_analysis()
    
    def _execute_default_analysis(self):
        """Execute SNID analysis with default settings"""
        try:
            # Check if GUI has analysis controller
            if hasattr(self.gui, 'analysis_controller'):
                # Update status
                if hasattr(self.gui, 'update_header_status'):
                    self.gui.update_header_status("🚀 Running SNID analysis with default settings...")
                
                # Run the analysis
                self.gui.analysis_controller.run_snid_analysis_only()
            else:
                # Fallback to direct method call
                if hasattr(self.gui, 'run_snid_analysis_only'):
                    self.gui.run_snid_analysis_only()
                else:
                    messagebox.showerror("Error", "Analysis controller not available.")
                    
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to run SNID analysis:\n{str(e)}")
    
    def _execute_advanced_analysis(self):
        """Execute SNID analysis with advanced configuration"""
        try:
            # First show the configuration dialog
            if hasattr(self.gui, 'dialog_controller'):
                # Use existing configuration system
                config_success = self.gui.dialog_controller.configure_options()
                
                # Only run analysis if configuration was successful (not cancelled)
                if config_success:
                    # Give a small delay to ensure configuration is applied
                    self.gui.master.after(100, self._run_after_configuration)
                else:
                    # Configuration was cancelled - don't run analysis
                    if hasattr(self.gui, 'update_header_status'):
                        self.gui.update_header_status("⚪ Analysis cancelled - configuration not applied")
            else:
                # Fallback to direct configuration dialog
                config_dialog = ModernSNIDOptionsDialog(self.gui.master, self.gui.params if hasattr(self.gui, 'params') else {})
                result = config_dialog.show()
                
                if result:
                    # Apply configuration and run
                    if hasattr(self.gui, 'params'):
                        self.gui.params.update(result)
                    
                    # Run analysis with new settings
                    self._execute_default_analysis()
                # If result is None (cancelled), don't run analysis
                    
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to configure analysis options:\n{str(e)}")
    
    def _run_after_configuration(self):
        """Run analysis after configuration dialog is closed"""
        try:
            # Update status
            if hasattr(self.gui, 'update_header_status'):
                self.gui.update_header_status("🚀 Running SNID analysis with custom settings...")
            
            # Run the analysis
            if hasattr(self.gui, 'analysis_controller'):
                self.gui.analysis_controller.run_snid_analysis_only()
            elif hasattr(self.gui, 'run_snid_analysis_only'):
                self.gui.run_snid_analysis_only()
            else:
                messagebox.showerror("Error", "Analysis controller not available.")
                
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to run SNID analysis:\n{str(e)}")
    
    def _cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()


def show_snid_analysis_dialog(parent, gui_instance) -> Optional[str]:
    """
    Show the SNID Analysis dialog.
    
    Args:
        parent: Parent window
        gui_instance: Main GUI instance
        
    Returns:
        Selected mode or None if cancelled
    """
    
    try:
        from snid_sage.interfaces.gui.utils.unified_theme_manager import get_unified_theme_manager
        theme_manager = get_unified_theme_manager()
        if theme_manager:
            theme_manager.disable_theme_application()
        
        dialog = SNIDAnalysisDialog(parent, gui_instance)
        return dialog.show()
        
    finally:
        if theme_manager:
            theme_manager.enable_theme_application() 
