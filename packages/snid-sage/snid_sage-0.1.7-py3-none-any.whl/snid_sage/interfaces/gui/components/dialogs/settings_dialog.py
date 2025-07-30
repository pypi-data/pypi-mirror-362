"""
SNID SAGE - GUI Settings Dialog
==============================

Beautiful and comprehensive dialog for configuring GUI settings including:
- Font size and display options
- Theme preferences
- Window resolution and DPI settings
- Plot display preferences
- Interface customization options

Part of the SNID SAGE GUI system following modern dialog patterns.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import Optional, Dict, Any, List, Callable
import os
from pathlib import Path


class GUISettingsDialog:
    """
    Modern GUI settings dialog for SNID SAGE interface configuration.
    
    Features beautiful gradient styling and comprehensive settings management.
    """
    
    def __init__(self, parent, current_settings=None):
        """
        Initialize GUI settings dialog.
        
        Args:
            parent: Parent window (main GUI instance)
            current_settings: Current settings values dict
        """
        self.parent = parent
        self.dialog = None
        self.result = None
        self.settings = current_settings or {}
        
        # Settings widgets
        self.widgets = {}
        self.font_samples = {}  # Font preview labels
        
        # Available fonts (filtered for readability)
        self.available_fonts = self._get_available_fonts()
        
        # Color scheme (matching parent theme)
        self.colors = self._get_theme_colors()
        
        # Settings change callbacks
        self.settings_changed_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
    def show(self) -> Optional[Dict[str, Any]]:
        """Show the dialog and return settings results"""
        self._create_dialog()
        self._setup_interface()
        self._load_current_values()
        
        # Center and show dialog
        self._center_dialog()
        self.dialog.grab_set()
        self.dialog.wait_window()
        
        return self.result
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """Get theme colors from parent or use defaults"""
        if hasattr(self.parent, 'theme_manager'):
            parent_colors = self.parent.theme_manager.get_current_colors()
            return {
                'bg_primary': parent_colors.get('bg_primary', '#f8fafc'),
                'bg_secondary': parent_colors.get('bg_secondary', '#e2e8f0'),
                'bg_tertiary': parent_colors.get('bg_tertiary', '#f1f5f9'),
                'text_primary': parent_colors.get('text_primary', '#1e293b'),
                'text_secondary': parent_colors.get('text_secondary', '#64748b'),
                'border': parent_colors.get('border', '#cbd5e1'),
                'accent_blue': '#3b82f6',
                'accent_purple': '#8b5cf6',
                'accent_green': '#10b981',
                'accent_orange': '#f59e0b',
                'accent_red': '#ef4444',
                'bg_info': '#dbeafe',
                'bg_success': '#dcfce7',
                'bg_warning': '#fef3c7',
                'shadow': '#94a3b8'
            }
        else:
            # Default light theme colors
            return {
                'bg_primary': '#f8fafc',
                'bg_secondary': '#e2e8f0', 
                'bg_tertiary': '#f1f5f9',
                'text_primary': '#1e293b',
                'text_secondary': '#64748b',
                'border': '#cbd5e1',
                'accent_blue': '#3b82f6',
                'accent_purple': '#8b5cf6',
                'accent_green': '#10b981',
                'accent_orange': '#f59e0b',
                'accent_red': '#ef4444',
                'bg_info': '#dbeafe',
                'bg_success': '#dcfce7',
                'bg_warning': '#fef3c7',
                'shadow': '#94a3b8'
            }
    
    def _get_available_fonts(self) -> List[str]:
        """Get list of available system fonts suitable for GUI"""
        try:
            # Get all available fonts
            all_fonts = list(font.families())
            
            # Preferred fonts for GUI (modern, readable)
            preferred_fonts = [
                'Segoe UI', 'Arial', 'Helvetica', 'Calibri', 'Verdana',
                'Tahoma', 'Geneva', 'Sans Serif', 'DejaVu Sans',
                'Liberation Sans', 'Ubuntu', 'Roboto', 'Open Sans'
            ]
            
            # Filter available fonts to include preferred ones first
            available_fonts = []
            
            # Add preferred fonts that are available
            for font_name in preferred_fonts:
                if font_name in all_fonts:
                    available_fonts.append(font_name)
            
            # Add other available fonts (excluding decorative/symbol fonts)
            for font_name in sorted(all_fonts):
                if (font_name not in available_fonts and 
                    not any(x in font_name.lower() for x in 
                           ['symbol', 'wingding', 'dingbat', 'icon', 'emoji'])):
                    available_fonts.append(font_name)
            
            return available_fonts[:50]  # Limit to reasonable number
            
        except Exception:
            # Fallback to basic fonts
            return ['Segoe UI', 'Arial', 'Helvetica', 'Calibri', 'Verdana']
    
    def _create_dialog(self):
        """Create the modern dialog window"""
        self.dialog = tk.Toplevel(self.parent.master if hasattr(self.parent, 'master') else self.parent)
        self.dialog.title("⚙️ GUI Settings")
        self.dialog.geometry("1200x850")  # Increased height to ensure buttons are visible
        self.dialog.resizable(True, True)
        self.dialog.minsize(1000, 750)  # Set minimum size to ensure all content is visible
        
        # Apply background color
        self.dialog.configure(bg=self.colors['bg_primary'])
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
        

        if hasattr(self.parent, 'theme_manager'):
            # Dialog themes itself independently, no need to apply main window theme
            pass
    
    def _center_dialog(self):
        """Center dialog on parent"""
        self.dialog.update_idletasks()
        
        try:
            # Try to get parent window for centering
            if hasattr(self.parent, 'master') and self.parent.master:
                parent_widget = self.parent.master
            elif hasattr(self.parent, 'winfo_x'):
                parent_widget = self.parent
            else:
                # Fallback: center on screen
                screen_width = self.dialog.winfo_screenwidth()
                screen_height = self.dialog.winfo_screenheight()
                x = (screen_width // 2) - (1200 // 2)
                y = (screen_height // 2) - (850 // 2)
                self.dialog.geometry(f"1200x850+{x}+{y}")
                return
            
            # Center on parent window
            x = parent_widget.winfo_x() + (parent_widget.winfo_width() // 2) - (1200 // 2)
            y = parent_widget.winfo_y() + (parent_widget.winfo_height() // 2) - (850 // 2)
            self.dialog.geometry(f"1200x850+{x}+{y}")
            
        except (AttributeError, tk.TclError):
            # Fallback: center on screen
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width // 2) - (1200 // 2)
            y = (screen_height // 2) - (850 // 2)
            self.dialog.geometry(f"1200x850+{x}+{y}")
    
    def _setup_interface(self):
        """Setup the modern dialog interface"""
        # Header with gradient effect
        self._create_header()
        
        # Main content with three columns
        self._create_main_content()
        
        # Footer with buttons
        self._create_footer()
    
    def _create_header(self):
        """Create colorful header"""
        header_frame = tk.Frame(self.dialog, bg=self.colors['accent_purple'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Add gradient effect
        gradient_frame = tk.Frame(header_frame, bg=self.colors['accent_blue'])
        gradient_frame.place(x=0, y=60, relwidth=1, height=20)
        
        # Header content
        content_frame = tk.Frame(header_frame, bg=self.colors['accent_purple'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Icon and title
        title_frame = tk.Frame(content_frame, bg=self.colors['accent_purple'])
        title_frame.pack(expand=True)
        
        title_label = tk.Label(title_frame, text="⚙️ GUI Settings",
                              font=('Segoe UI', 20, 'bold'),
                              bg=self.colors['accent_purple'], fg='white')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Customize interface appearance and behavior",
                                 font=('Segoe UI', 12, 'normal'),
                                 bg=self.colors['accent_purple'], fg='#e0e7ff')
        subtitle_label.pack(pady=(5, 0))
    
    def _create_main_content(self):
        """Create main content area with three columns"""
        # Container for content with scrolling if needed
        container = tk.Frame(self.dialog, bg=self.colors['bg_primary'])
        container.pack(fill='both', expand=True, padx=20, pady=(20, 10))  # Reduced bottom padding
        
        # Create three main columns
        left_column = tk.Frame(container, bg=self.colors['bg_primary'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 7))
        
        middle_column = tk.Frame(container, bg=self.colors['bg_primary'])  
        middle_column.pack(side='left', fill='both', expand=True, padx=(7, 7))
        
        right_column = tk.Frame(container, bg=self.colors['bg_primary'])  
        right_column.pack(side='left', fill='both', expand=True, padx=(7, 0))
        
        # Left column sections
        self._create_font_section(left_column)
        self._create_display_section(left_column)
        
        # Middle column sections
        self._create_window_section(middle_column)
        
        # Right column sections
        self._create_plot_section(right_column)
        self._create_performance_section(right_column)
    
    def _create_font_section(self, parent):
        """Create font and text settings section"""
        section_frame = self._create_colorful_section(parent, "🔤 Font & Text Settings", self.colors['bg_info'])
        
        # Font family selection
        font_frame = tk.Frame(section_frame, bg=self.colors['bg_info'])
        font_frame.pack(fill='x', pady=(5, 10))
        
        tk.Label(font_frame, text="Font Family:",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_info'], fg=self.colors['text_primary']).pack(anchor='w')
        
        # Use tk.OptionMenu instead of ttk.Combobox
        self.font_family_var = tk.StringVar()
        self.font_family_menu = tk.OptionMenu(font_frame, self.font_family_var, 
                                             *self.available_fonts,
                                             command=lambda x: self._on_font_changed())
        self.font_family_menu.config(
            font=('Segoe UI', 11, 'normal'),
            bg='white',
            fg=self.colors['text_primary'],
            activebackground=self.colors['bg_tertiary'],
            highlightthickness=0,
            relief='solid',
            bd=1,
            width=25,
            anchor='w'
        )
        self.font_family_menu.pack(anchor='w', pady=(5, 0))
        
        # Store the StringVar in widgets dict
        self.widgets['font_family'] = self.font_family_var
        
        # Font size slider
        self._create_slider_setting(section_frame, "font_size", "Font Size:", 8, 24, 1, 
                                   "Font size for GUI text elements", callback=self._on_font_changed)
        
        # Font preview
        preview_frame = tk.Frame(section_frame, bg=self.colors['bg_info'])
        preview_frame.pack(fill='x', pady=(10, 5))
        
        tk.Label(preview_frame, text="Preview:",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_info'], fg=self.colors['text_primary']).pack(anchor='w')
        
        self.font_samples['main'] = tk.Label(preview_frame, 
                                           text="The quick brown fox jumps over the lazy dog",
                                           bg='white', fg=self.colors['text_primary'],
                                           relief='solid', bd=1, pady=8, padx=10)
        self.font_samples['main'].pack(fill='x', pady=(5, 0))
    
    def _create_display_section(self, parent):
        """Create display and resolution settings section"""
        section_frame = self._create_colorful_section(parent, "🖥️ Display Settings", self.colors['bg_success'])
        
        # DPI scaling
        self._create_slider_setting(section_frame, "dpi_scale", "DPI Scaling:", 50, 200, 25,
                                   "Scale interface for high-DPI displays (%)")
        
        # Button size
        self._create_slider_setting(section_frame, "button_height", "Button Height:", 30, 60, 2,
                                   "Height of buttons in pixels")
        
        # Padding settings
        self._create_slider_setting(section_frame, "widget_padding", "Widget Padding:", 2, 20, 1,
                                   "Spacing between interface elements")
        
        # Icon size
        self._create_choice_setting(section_frame, "icon_size", "Icon Size:",
                                   ["Small", "Medium", "Large"], "Interface icon size")
    
    def _create_window_section(self, parent):
        """Create window behavior settings section"""
        section_frame = self._create_colorful_section(parent, "🪟 Window Behavior", 
                                                     self.colors['bg_info'])
        
        # Remember window position
        self._create_checkbox_setting(section_frame, "remember_position", "Remember Window Position",
                                     "Restore window position on startup")
        
        # Remember window size
        self._create_checkbox_setting(section_frame, "remember_size", "Remember Window Size", 
                                     "Restore window size on startup")
        
        # Minimize to tray
        self._create_checkbox_setting(section_frame, "minimize_to_tray", "Minimize to System Tray",
                                     "Hide to system tray instead of taskbar")
        
        # Auto-save settings
        self._create_checkbox_setting(section_frame, "auto_save_settings", "Auto-save Settings",
                                     "Automatically save changes to settings")
    
    def _create_plot_section(self, parent):
        """Create plot display settings section"""
        section_frame = self._create_colorful_section(parent, "📊 Plot Settings", 
                                                     self.colors['bg_success'])
        
        # Plot DPI
        self._create_slider_setting(section_frame, "plot_dpi", "Plot DPI:", 50, 300, 25,
                                   "Resolution for generated plots")
        
        # Animation speed
        self._create_slider_setting(section_frame, "animation_speed", "Animation Speed:", 0, 10, 1,
                                   "Speed of plot transitions and animations")
        
        # Grid opacity
        self._create_slider_setting(section_frame, "grid_opacity", "Grid Opacity:", 0, 100, 10,
                                   "Transparency of plot grid lines (%)")
    
    def _create_performance_section(self, parent):
        """Create performance settings section"""
        section_frame = self._create_colorful_section(parent, "⚡ Performance", 
                                                     self.colors['bg_warning'])
        
        # Reduce animations
        self._create_checkbox_setting(section_frame, "reduce_animations", "Reduce Animations",
                                     "Minimize visual effects for better performance")
    
    def _create_colorful_section(self, parent, title, bg_color):
        """Create a colorful section with title"""
        # Section container with margin
        section_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        section_container.pack(fill='x', pady=(10, 0))
        
        # Section frame with colored background
        section_frame = tk.Frame(section_container, bg=bg_color, relief='solid', bd=1)
        section_frame.pack(fill='x', padx=5)
        
        # Section title
        title_frame = tk.Frame(section_frame, bg=bg_color)
        title_frame.pack(fill='x', padx=15, pady=(10, 5))
        
        title_label = tk.Label(title_frame, text=title,
                              font=('Segoe UI', 14, 'bold'),
                              bg=bg_color, fg=self.colors['text_primary'])
        title_label.pack(anchor='w')
        
        # Content area
        content_frame = tk.Frame(section_frame, bg=bg_color)
        content_frame.pack(fill='x', padx=15, pady=(5, 15))
        
        return content_frame
    
    def _create_slider_setting(self, parent, key, label, min_val, max_val, resolution, tooltip, callback=None):
        """Create an entry setting with label and range display"""
        frame = tk.Frame(parent, bg=parent.cget('bg'))
        frame.pack(fill='x', pady=(5, 10))
        
        # Label and range display
        label_frame = tk.Frame(frame, bg=parent.cget('bg'))
        label_frame.pack(fill='x')
        
        tk.Label(label_frame, text=label,
                font=('Segoe UI', 12, 'bold'),
                bg=parent.cget('bg'), fg=self.colors['text_primary']).pack(side='left')
        
        range_label = tk.Label(label_frame, text=f"({min_val}-{max_val})",
                              font=('Segoe UI', 10, 'normal'),
                              bg=parent.cget('bg'), fg=self.colors['text_secondary'])
        range_label.pack(side='right')
        
        # Entry field with validation
        entry_frame = tk.Frame(frame, bg=parent.cget('bg'))
        entry_frame.pack(fill='x', pady=(5, 0))
        
        entry_var = tk.StringVar()
        entry = tk.Entry(entry_frame, textvariable=entry_var,
                        font=('Segoe UI', 12, 'normal'),
                        width=10, justify='center')
        entry.pack(side='left')
        
        # Determine if this should be integer-only (like font_size, button_height, etc.)
        integer_fields = {'font_size', 'button_height', 'widget_padding', 'animation_speed'}
        is_integer_field = key in integer_fields
        
        # Validation function
        def validate_value(event=None):
            try:
                value = float(entry_var.get())
                if min_val <= value <= max_val:
                    entry.config(bg='white', fg='black')
                    if callback:
                        callback()
                    return True
                else:
                    entry.config(bg='#ffeeee', fg='red')
                    return False
            except ValueError:
                entry.config(bg='#ffeeee', fg='red')
                return False
        
        # Bind validation
        entry_var.trace('w', lambda *args: validate_value())
        entry.bind('<FocusOut>', validate_value)
        entry.bind('<Return>', validate_value)
        
        # Helper methods for the entry
        def get_value():
            try:
                value = float(entry_var.get())
                if min_val <= value <= max_val:
                    # Return integer for integer fields, float for others
                    return int(value) if is_integer_field else value
                else:
                    return int(min_val) if is_integer_field else min_val  # Return default if invalid
            except ValueError:
                return int(min_val) if is_integer_field else min_val  # Return default if invalid
        
        def set_value(value):
            # Convert to int for display if it's an integer field
            if is_integer_field:
                entry_var.set(str(int(value)))
            else:
                entry_var.set(str(value))
            validate_value()
        
        # Store entry with custom methods
        entry.get = get_value
        entry.set = set_value
        entry._var = entry_var
        entry._min = min_val
        entry._max = max_val
        entry._resolution = resolution
        entry._is_integer = is_integer_field
        
        self.widgets[key] = entry
        self.widgets[f"{key}_range"] = range_label
        
        # Add tooltip
        self._add_tooltip(entry, f"{tooltip}\\nValid range: {min_val} to {max_val}")
        
        return entry
    
    def _create_choice_setting(self, parent, key, label, choices, tooltip):
        """Create a choice/combobox setting"""
        frame = tk.Frame(parent, bg=parent.cget('bg'))
        frame.pack(fill='x', pady=(5, 10))
        
        tk.Label(frame, text=label,
                font=('Segoe UI', 12, 'bold'),
                bg=parent.cget('bg'), fg=self.colors['text_primary']).pack(anchor='w')
        
        # Use tk.OptionMenu instead of ttk.Combobox
        var = tk.StringVar()
        option_menu = tk.OptionMenu(frame, var, *choices)
        option_menu.config(
            font=('Segoe UI', 11, 'normal'),
            bg='white',
            fg=self.colors['text_primary'],
            activebackground=self.colors['bg_tertiary'],
            highlightthickness=0,
            relief='solid',
            bd=1,
            width=20,
            anchor='w'
        )
        option_menu.pack(anchor='w', pady=(5, 0))
        
        self.widgets[key] = var
        self._add_tooltip(option_menu, tooltip)
    
    def _create_checkbox_setting(self, parent, key, label, tooltip):
        """Create a checkbox setting"""
        frame = tk.Frame(parent, bg=parent.cget('bg'))
        frame.pack(fill='x', pady=(5, 8))
        
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame, text=label, variable=var,
                                 font=('Segoe UI', 12, 'normal'),
                                 bg=parent.cget('bg'), fg=self.colors['text_primary'],
                                 activebackground=parent.cget('bg'),
                                 selectcolor='white', relief='flat')
        checkbox.pack(anchor='w')
        
        self.widgets[key] = var
        self._add_tooltip(checkbox, tooltip)
    
    def _create_footer(self):
        """Create footer with action buttons"""
        footer_frame = tk.Frame(self.dialog, bg=self.colors['bg_secondary'], height=80)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Button container with proper centering
        button_container = tk.Frame(footer_frame, bg=self.colors['bg_secondary'])
        button_container.place(relx=0.5, rely=0.5, anchor='center')  # Center the button container
        
        # Apply button
        apply_btn = tk.Button(button_container, text="✅ Apply Settings",
                             bg=self.colors['accent_green'], fg='white',
                             font=('Segoe UI', 12, 'bold'),
                             relief='raised', bd=2, pady=10, padx=20, cursor='hand2',
                             command=self._apply)
        apply_btn.pack(side='right', padx=(10, 0))
        
        # Cancel button
        cancel_btn = tk.Button(button_container, text="❌ Cancel",
                              bg=self.colors['shadow'], fg='white',
                              font=('Segoe UI', 12, 'normal'),
                              relief='raised', bd=2, pady=10, padx=20, cursor='hand2',
                              command=self._cancel)
        cancel_btn.pack(side='right', padx=(10, 0))
        
        # Reset to defaults button
        reset_btn = tk.Button(button_container, text="🔄 Reset to Defaults",
                             bg=self.colors['accent_orange'], fg='white',
                             font=('Segoe UI', 12, 'normal'),
                             relief='raised', bd=2, pady=10, padx=20, cursor='hand2',
                             command=self._reset_defaults)
        reset_btn.pack(side='left')
    
    def _load_current_values(self):
        """Load current settings into widgets"""
        # Default values
        defaults = self._get_default_settings()
        
        # Load values from current settings or defaults
        for key, widget in self.widgets.items():
            if key.endswith('_range'):  # Skip range labels
                continue
                
            value = self.settings.get(key, defaults.get(key))
            
            if hasattr(widget, 'set') and hasattr(widget, '_var'):  # Entry field (former slider)
                widget.set(value)
            elif isinstance(widget, tk.StringVar):
                # For StringVar (OptionMenu)
                widget.set(value if value else defaults.get(key, ''))
            elif isinstance(widget, tk.BooleanVar):
                widget.set(bool(value))
        
        # Update font preview
        self._update_font_preview()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default GUI settings"""
        return {
            'font_family': 'Segoe UI',
            'font_size': 12,
            'dpi_scale': 100,
            'button_height': 40,
            'widget_padding': 8,
            'icon_size': 'Medium',
            'remember_position': True,
            'remember_size': True,
            'minimize_to_tray': False,
            'auto_save_settings': True,
            'plot_dpi': 150,
            'animation_speed': 5,
            'grid_opacity': 30,
            'reduce_animations': False
        }
    
    def _on_font_changed(self, event=None):
        """Handle font changes to update preview"""
        self._update_font_preview()
    
    def _update_font_preview(self):
        """Update font preview with current settings"""
        try:
            # Get font family from StringVar or font_family_var
            if hasattr(self, 'font_family_var'):
                font_family = self.font_family_var.get()
            elif 'font_family' in self.widgets and isinstance(self.widgets['font_family'], tk.StringVar):
                font_family = self.widgets['font_family'].get()
            else:
                font_family = 'Segoe UI'
                
            font_size = int(self.widgets['font_size'].get())
            
            if font_family and 'main' in self.font_samples:
                preview_font = (font_family, font_size, 'normal')
                self.font_samples['main'].config(font=preview_font)
        except (ValueError, KeyError, tk.TclError):
            pass  # Ignore errors during font updates
    
    def _add_tooltip(self, widget, text):
        """Add tooltip to widget"""
        def on_enter(event):
            # Create tooltip window
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='#ffffcc', relief='solid', bd=1)
            
            label = tk.Label(tooltip, text=text, bg='#ffffcc', fg='black',
                           font=('Segoe UI', 9, 'normal'), wraplength=300,
                           justify='left', padx=8, pady=4)
            label.pack()
            
            # Position tooltip
            x = widget.winfo_rootx() + 25
            y = widget.winfo_rooty() + 25
            tooltip.geometry(f"+{x}+{y}")
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def _reset_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", 
                              "Are you sure you want to reset all settings to defaults?\n\n"
                              "This action cannot be undone."):
            defaults = self._get_default_settings()
            self.settings = defaults.copy()
            self._load_current_values()
    
    def _validate_and_collect(self) -> Dict[str, Any]:
        """Validate and collect all settings"""
        settings = {}
        
        for key, widget in self.widgets.items():
            if key.endswith('_range'):  # Skip range labels
                continue
                
            try:
                if hasattr(widget, 'get') and hasattr(widget, '_var'):  # Entry field (former slider)
                    settings[key] = widget.get()
                elif isinstance(widget, tk.StringVar):
                    settings[key] = widget.get()
                elif isinstance(widget, tk.BooleanVar):
                    settings[key] = widget.get()
            except (ValueError, tk.TclError):
                # Use default for invalid values
                defaults = self._get_default_settings()
                settings[key] = defaults.get(key)
        
        return settings
    
    def _apply(self):
        """Apply settings and close dialog"""
        try:
            self.result = self._validate_and_collect()
            
            # Notify callbacks about settings change
            for callback in self.settings_changed_callbacks:
                try:
                    callback(self.result)
                except Exception as e:
                    print(f"Settings callback error: {e}")
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Settings Error", 
                               f"Error applying settings:\n\n{str(e)}")
    
    def _cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.dialog.destroy()
    
    def add_settings_changed_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add callback for settings changes"""
        self.settings_changed_callbacks.append(callback)


def show_gui_settings_dialog(parent, current_settings=None) -> Optional[Dict[str, Any]]:
    """
    Show GUI settings dialog.
    
    Args:
        parent: Parent window
        current_settings: Current settings dict
        
    Returns:
        Settings dict if applied, None if cancelled
    """
    dialog = GUISettingsDialog(parent, current_settings)
    return dialog.show() 
