"""
Redshift Mode Selection Dialog

This dialog appears after a user accepts a redshift in the manual redshift dialog,
giving them options for how to use that redshift in the SNID analysis.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
import logging

# Set up logger
_LOGGER = logging.getLogger(__name__)


class RedshiftModeDialog:
    """Dialog for selecting redshift analysis mode"""
    
    def __init__(self, parent, redshift_value: float):
        self.parent = parent
        self.redshift_value = redshift_value
        self.result = None
        self.dialog = None
        
        # Search range variables
        self.range_var = tk.StringVar(value="0.001")  # Default ±0.001 range
        
        # Color scheme
        self.colors = {
            'bg': '#f8fafc',
            'panel_bg': '#ffffff',
            'primary': '#3b82f6',   # Will be overridden to black for text
            'success': '#22c55e',   # Keep for button background
            'warning': '#f59e0b',   # Will be overridden to black
            'danger': '#ef4444',    # Will be overridden to black
            'text_primary': '#1e293b',
            'text_secondary': '#64748b',
            'border': '#e2e8f0',
            'hover': '#f1f5f9'
        }

        # Force all textual elements to black to match unified dialog style
        for key in ['primary', 'success', 'warning', 'danger', 'text_primary', 'text_secondary']:
            self.colors[key] = 'black'
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Show the dialog and return the result"""
        try:
            # Theme protection is now handled directly by the workflow-aware
            # theming system, so no global enable/disable toggles are required.

            self._create_dialog()
            self._center_dialog()

            # Make modal
            self.dialog.transient(self.parent)
            self.dialog.grab_set()

            # Wait for dialog to close
            self.dialog.wait_window()

            return self.result

        except Exception as e:
            # Propagate the exception after logging (no theme state to restore)
            _LOGGER.error(f"Error in RedshiftModeDialog.show: {e}")
            raise e
    
    def _create_dialog(self):
        """Create the dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Redshift Analysis Mode")
        self.dialog.configure(bg=self.colors['bg'])
        self.dialog.resizable(False, False)
        
        # Set window size (increased to accommodate all content and range inputs)
        self.dialog.geometry("600x500")
        
        # Create main frame
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        self._create_header(main_frame)
        self._create_mode_options(main_frame)
        self._create_buttons(main_frame)
    
    def _center_dialog(self):
        """Center the dialog on parent window"""
        self.dialog.update_idletasks()
        
        # Get dialog dimensions
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Calculate centered position
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        # Ensure dialog is within screen bounds
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_header(self, parent):
        """Create dialog header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🎯 Redshift Analysis Mode",
                              font=('Segoe UI', 20, 'bold'),  # Increased from 16 to 20
                              fg=self.colors['primary'],
                              bg=self.colors['bg'])
        title_label.pack()
        
        # Redshift value display
        redshift_label = tk.Label(header_frame,
                                 text=f"Redshift: z = {self.redshift_value:.6f}",
                                 font=('Segoe UI', 16, 'normal'),  # Increased from 12 to 16
                                 fg=self.colors['text_primary'],
                                 bg=self.colors['bg'])
        redshift_label.pack(pady=(5, 0))
        
        # Description
        desc_label = tk.Label(header_frame,
                             text="Choose how to use this redshift in SNID analysis:",
                             font=('Segoe UI', 14, 'normal'),  # Increased from 10 to 14
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg'])
        desc_label.pack(pady=(10, 0))
    
    def _create_mode_options(self, parent):
        """Create mode selection options"""
        options_frame = tk.Frame(parent, bg=self.colors['bg'])
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Mode selection variable
        self.mode_var = tk.StringVar(value="search")
        
        # Search around redshift option (moved to top)
        search_frame = tk.Frame(options_frame, bg=self.colors['panel_bg'], relief='solid', bd=1)
        search_frame.pack(fill='x', pady=(0, 10))
        
        search_radio = tk.Radiobutton(search_frame,
                                    text="🔍 Search Around Redshift",
                                    variable=self.mode_var,
                                    value="search",
                                    font=('Segoe UI', 15, 'bold'),  # Increased from 11 to 15
                                    fg=self.colors['success'],
                                    bg=self.colors['panel_bg'],
                                    selectcolor=self.colors['panel_bg'],
                                    activebackground=self.colors['panel_bg'])
        search_radio.pack(anchor='w', padx=15, pady=(10, 5))
        
        search_desc = tk.Label(search_frame,
                             text=f"• Search for best redshift near z = {self.redshift_value:.6f}\n"
                                  "• Standard SNID analysis with initial guess\n"
                                  "• Recommended for most cases",
                             font=('Segoe UI', 13, 'normal'),  # Increased from 9 to 13
                             fg=self.colors['text_secondary'],
                             bg=self.colors['panel_bg'],
                             justify='left')
        search_desc.pack(anchor='w', padx=35, pady=(0, 5))
        
        # Range configuration for search mode
        range_config_frame = tk.Frame(search_frame, bg=self.colors['panel_bg'])
        range_config_frame.pack(fill='x', padx=35, pady=(5, 10))
        
        range_label = tk.Label(range_config_frame,
                             text="Search Range (±):",
                             font=('Segoe UI', 13, 'bold'),  # Increased from 9 to 13
                             fg=self.colors['text_primary'],
                             bg=self.colors['panel_bg'])
        range_label.pack(side='left')
        
        range_entry = tk.Entry(range_config_frame,
                             textvariable=self.range_var,
                             font=('Segoe UI', 13, 'normal'),  # Increased from 9 to 13
                             width=8,
                             bg='white',
                             fg=self.colors['text_primary'],
                             relief='solid',
                             bd=1)
        range_entry.pack(side='left', padx=(10, 5))
        
        initial_range = float(self.range_var.get())
        range_info = tk.Label(range_config_frame,
                            text=f"(will search from z = {max(0.0, self.redshift_value - initial_range):.6f} to z = {self.redshift_value + initial_range:.6f})",
                            font=('Segoe UI', 12, 'italic'),  # Increased from 8 to 12
                            fg=self.colors['text_secondary'],
                            bg=self.colors['panel_bg'])
        range_info.pack(side='left', padx=(5, 0))
        
        # Update range info when range changes
        def update_range_info(*args):
            try:
                range_val = float(self.range_var.get())
                min_z = max(0.0, self.redshift_value - range_val)
                max_z = self.redshift_value + range_val
                range_info.config(text=f"(will search from z = {min_z:.6f} to z = {max_z:.6f})")
            except ValueError:
                range_info.config(text="(invalid range value)")
        
        self.range_var.trace('w', update_range_info)
        
        # Force exact redshift option (moved to bottom)
        force_frame = tk.Frame(options_frame, bg=self.colors['panel_bg'], relief='solid', bd=1)
        force_frame.pack(fill='x')
        
        force_radio = tk.Radiobutton(force_frame,
                                   text="🎯 Force Exact Redshift",
                                   variable=self.mode_var,
                                   value="force",
                                   font=('Segoe UI', 15, 'bold'),  # Increased from 11 to 15
                                   fg=self.colors['primary'],
                                   bg=self.colors['panel_bg'],
                                   selectcolor=self.colors['panel_bg'],
                                   activebackground=self.colors['panel_bg'])
        force_radio.pack(anchor='w', padx=15, pady=(10, 5))
        
        force_desc = tk.Label(force_frame,
                            text=f"• Use exactly z = {self.redshift_value:.6f} for all templates\n"
                                 "• Faster analysis (skips redshift search)\n"
                                 "• Best when redshift is precisely known",
                            font=('Segoe UI', 13, 'normal'),  # Increased from 9 to 13
                            fg=self.colors['text_secondary'],
                            bg=self.colors['panel_bg'],
                            justify='left')
        force_desc.pack(anchor='w', padx=35, pady=(0, 10))
    
    def _mark_button_as_workflow_managed(self, button: tk.Button, button_name: str = "dialog_button"):
        """Dialog buttons use simple fixed colors and don't interact with the workflow system"""
        pass
    
    def _create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill='x', pady=(20, 0))  # Added top padding for better separation
        
        # Cancel button
        cancel_btn = tk.Button(button_frame,
                              text="❌ Cancel",
                              font=('Segoe UI', 12, 'normal'),  # Reduced size to match preprocessing
                              bg='#6b7280',
                              fg='white',
                              relief='raised',
                              bd=2,
                              padx=20,  # Reduced padding
                              pady=8,   # Reduced padding
                              cursor='hand2',
                              command=self._cancel)
        cancel_btn.pack(side='left', padx=(0, 20))  # Canceled button at left
        
        # Apply button
        accept_btn = tk.Button(button_frame,
                              text="🚀 Apply & Proceed",
                              command=self._accept,
                              bg='#10b981',  # Proper green color for success/apply buttons
                              fg='white',
                              font=('Segoe UI', 15, 'bold'),
                              relief='raised',
                              bd=2,
                              padx=30,
                              pady=12,
                              cursor='hand2')
        accept_btn.pack(side='right')
        
        # Bind Enter key to accept
        self.dialog.bind('<Return>', lambda e: self._accept())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
        
        # Focus on accept button and make it default
        accept_btn.focus_set()
        self.dialog.bind('<Return>', lambda e: self._accept())  # Double-bind for safety
    
    def _accept(self):
        """Apply the current mode selection and proceed"""
        mode = self.mode_var.get()
        
        if mode == "force":
            self.result = {
                'redshift': self.redshift_value,
                'mode': 'force',
                'forced_redshift': self.redshift_value
            }
            _LOGGER.info(f"🎯 Selected forced redshift mode: z = {self.redshift_value:.6f}")
        else:  # search mode
            try:
                search_range = float(self.range_var.get())
            except ValueError:
                # Show error and return without closing
                tk.messagebox.showerror("Invalid Range", 
                                      "Please enter a valid numeric value for the search range.")
                return
            
            if search_range <= 0:
                tk.messagebox.showerror("Invalid Range", 
                                      "Search range must be greater than 0.")
                return
            
            if search_range > 1.0:
                confirm = tk.messagebox.askyesno("Large Range", 
                                               f"Search range ±{search_range:.6f} is very large.\n"
                                               f"This may take a long time. Continue?")
                if not confirm:
                    return
            
            self.result = {
                'redshift': self.redshift_value,
                'mode': 'search',
                'forced_redshift': None,
                'search_range': search_range,
                'min_redshift': max(0.0, self.redshift_value - search_range),
                'max_redshift': self.redshift_value + search_range
            }
            _LOGGER.info(f"🔍 Selected search mode around redshift: z = {self.redshift_value:.6f} ±{search_range:.6f}")
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel the dialog"""
        self.result = None
        _LOGGER.info("❌ Redshift mode selection cancelled")
        self.dialog.destroy()


def show_redshift_mode_dialog(parent, redshift_value: float) -> Optional[Dict[str, Any]]:
    """
    Show redshift mode selection dialog.
    
    Args:
        parent: Parent window
        redshift_value: The redshift value to configure
        
    Returns:
        Dictionary with mode configuration or None if cancelled
    """

    dialog = RedshiftModeDialog(parent, redshift_value)
    return dialog.show() 
