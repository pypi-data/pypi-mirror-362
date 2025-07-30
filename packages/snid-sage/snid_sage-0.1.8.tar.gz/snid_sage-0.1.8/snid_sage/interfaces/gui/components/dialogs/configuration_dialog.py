"""
SNID SAGE - Modern SNID Options Dialog
======================================

Beautiful and colorful dialog for configuring SNID analysis parameters.
Focuses on the actual parameters that SNID accepts, with modern styling
and intuitive button-based type selection.

Part of the SNID SAGE GUI system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, List
import os
import glob
from pathlib import Path

# Import centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.configuration_dialog')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.configuration_dialog')

# Import the template info function
try:
    from snid_sage.snid.io import get_template_info
    from snid_sage.shared.utils.config.configuration_manager import ConfigurationManager
    HAS_TEMPLATE_SUPPORT = True
except ImportError:
    HAS_TEMPLATE_SUPPORT = False

# Import template finder for robust path discovery
try:
    from snid_sage.shared.utils.simple_template_finder import find_templates_directory as _find_templates_directory
except ImportError:
    _find_templates_directory = None


class ModernSNIDOptionsDialog:
    """
    Modern and colorful dialog for SNID analysis parameters.
    
    Features beautiful gradient styling and button-based type selection
    with three-column layout similar to Settings dialog.
    """
    
    def __init__(self, parent, current_params=None):
        """
        Initialize modern SNID options dialog.
        
        Args:
            parent: Parent window
            current_params: Current parameter values dict
        """
        self.parent = parent
        self.dialog = None
        self.result = None
        self.params = current_params or {}
        
        # Parameter widgets
        self.widgets = {}
        self.selected_types = set()  # Track selected supernova types
        self.type_buttons = {}  # Track type selection buttons
        
        # Template selection (simplified - no auto-discovery)
        self.selected_templates = set()
        self.template_mode = 'include'  # 'include' or 'exclude'
        
        # Color scheme
        self.colors = {
            'bg_primary': '#f8fafc',      # Light blue-gray
            'bg_secondary': '#e2e8f0',    # Darker blue-gray  
            'bg_accent': '#ddd6fe',       # Light purple
            'bg_success': '#dcfce7',      # Light green
            'bg_warning': '#fef3c7',      # Light yellow
            'bg_info': '#dbeafe',         # Light blue
            'text_primary': '#1e293b',    # Dark slate
            'text_secondary': '#64748b',  # Medium slate
            'text_accent': '#7c3aed',     # Purple
            'accent_blue': '#3b82f6',     # Blue
            'accent_purple': '#8b5cf6',   # Purple
            'accent_green': '#10b981',    # Green
            'accent_orange': '#f59e0b',   # Orange
            'accent_red': '#ef4444',      # Red
            'border': '#cbd5e1',          # Light border
            'shadow': '#94a3b8'           # Shadow color
        }
        
    def show(self) -> Optional[Dict[str, Any]]:
        """Show the dialog and return parameter results"""
        self._create_dialog()
        self._setup_interface()
        self._load_current_values()
        
        # Center and show dialog
        self._center_dialog()
        self.dialog.grab_set()
        self.dialog.wait_window()
        
        return self.result
    
    def _create_dialog(self):
        """Create the modern dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("⚙️ SNID Analysis Options")
        self.dialog.geometry("1300x900")
        self.dialog.resizable(True, True)
        self.dialog.minsize(1100, 800)  # Set minimum size to ensure all content is visible
        
        # CRITICAL: Use isolated theme application to prevent main window interference
        # Check if parent has theme manager for consistent colors
        if hasattr(self.parent, 'theme_manager'):
            # Use parent's theme colors but apply only to this dialog
            parent_colors = self.parent.theme_manager.get_current_colors()
            self.colors.update({
                'bg_primary': parent_colors.get('bg_primary', self.colors['bg_primary']),
                'bg_secondary': parent_colors.get('bg_secondary', self.colors['bg_secondary']),
                'text_primary': parent_colors.get('text_primary', self.colors['text_primary']),
                'text_secondary': parent_colors.get('text_secondary', self.colors['text_secondary']),
            })
            _LOGGER.debug(f"🎨 Dialog using parent theme colors: {parent_colors.get('bg_primary', 'default')}")
        
        # Apply background color
        self.dialog.configure(bg=self.colors['bg_primary'])
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
        
        # Dialog themes itself independently to prevent main window interference
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
                x = (screen_width // 2) - (1300 // 2)
                y = (screen_height // 2) - (900 // 2)
                self.dialog.geometry(f"1300x900+{x}+{y}")
                return
            
            # Center on parent window
            x = parent_widget.winfo_x() + (parent_widget.winfo_width() // 2) - (1300 // 2)
            y = parent_widget.winfo_y() + (parent_widget.winfo_height() // 2) - (900 // 2)
            self.dialog.geometry(f"1300x900+{x}+{y}")
            
        except (AttributeError, tk.TclError):
            # Fallback: center on screen
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width // 2) - (1300 // 2)
            y = (screen_height // 2) - (900 // 2)
            self.dialog.geometry(f"1300x900+{x}+{y}")
    
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
        header_frame = tk.Frame(self.dialog, bg=self.colors['accent_purple'], height=90)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        content_frame = tk.Frame(header_frame, bg=self.colors['accent_purple'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=18)
        
        # Icon and title
        title_frame = tk.Frame(content_frame, bg=self.colors['accent_purple'])
        title_frame.pack(expand=True)
        
        title_label = tk.Label(title_frame, text="⚙️ SNID Analysis Parameters",
                              font=('Segoe UI', 22, 'bold'),
                              bg=self.colors['accent_purple'], fg='white')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Configure supernova identification settings",
                                 font=('Segoe UI', 14, 'normal'),
                                 bg=self.colors['accent_purple'], fg='#e0e7ff')
        subtitle_label.pack(pady=(8, 0))
    
    def _create_main_content(self):
        """Create main content area with three columns"""
        # Container for content (no scrolling needed)
        container = tk.Frame(self.dialog, bg=self.colors['bg_primary'])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create three main columns
        left_column = tk.Frame(container, bg=self.colors['bg_primary'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 7))
        
        middle_column = tk.Frame(container, bg=self.colors['bg_primary'])  
        middle_column.pack(side='left', fill='both', expand=True, padx=(7, 7))
        
        right_column = tk.Frame(container, bg=self.colors['bg_primary'])  
        right_column.pack(side='left', fill='both', expand=True, padx=(7, 0))
        
        # Left column sections
        self._create_redshift_section(left_column)
        self._create_correlation_section(left_column)
        self._create_age_cuts_section(left_column)
        
        # Middle column sections
        self._create_type_selection_section(middle_column)
        self._create_template_button_section(middle_column)
        
        # Right column sections  
        self._create_max_templates_section(right_column)
        self._create_output_section(right_column)
    
    def _create_redshift_section(self, parent):
        """Create colorful redshift range section"""
        section_frame = self._create_colorful_section(parent, "🌌 Redshift Range", self.colors['bg_info'])
        
        # Redshift min
        self._create_float_entry(section_frame, "zmin", "Minimum Redshift:", 
                                default=-0.01, tooltip="Minimum redshift to consider")
        
        # Redshift max  
        self._create_float_entry(section_frame, "zmax", "Maximum Redshift:",
                                default=0.6, tooltip="Maximum redshift to consider")
    
    def _create_correlation_section(self, parent):
        """Create colorful correlation parameters section"""
        section_frame = self._create_colorful_section(parent, "🔗 Correlation Thresholds", self.colors['bg_success'])
        
        # RLAP minimum
        self._create_float_entry(section_frame, "rlapmin", "RLAP Minimum:",
                                default=5.0, tooltip="Minimum rlap value required for a match")
        
        # LAP minimum
        self._create_float_entry(section_frame, "lapmin", "Overlap Minimum:",
                                default=0.4, tooltip="Minimum overlap fraction required")
    
    def _create_age_cuts_section(self, parent):
        """Create age cuts section for left column"""
        section_frame = self._create_colorful_section(parent, "⏰ Age Cuts", self.colors['bg_warning'])
        
        # Age range
        age_frame = tk.Frame(section_frame, bg=self.colors['bg_warning'])
        age_frame.pack(fill='x', pady=(8, 18))
        
        age_title = tk.Label(age_frame, text="Age Range (days):", font=('Segoe UI', 14, 'bold'),
                            bg=self.colors['bg_warning'], fg=self.colors['text_primary'])
        age_title.pack(anchor='w', pady=(0, 12))
        
        # Age controls in a more compact layout
        age_controls = tk.Frame(age_frame, bg=self.colors['bg_warning'])
        age_controls.pack(fill='x')
        
        # Min age - side by side layout
        min_container = tk.Frame(age_controls, bg=self.colors['bg_warning'])
        min_container.pack(fill='x', pady=(0, 8))
        
        tk.Label(min_container, text="Minimum:", bg=self.colors['bg_warning'], fg=self.colors['text_primary'],
                font=('Segoe UI', 12, 'bold'), width=12, anchor='w').pack(side='left', padx=(0, 10))
        self.widgets['age_min'] = tk.Entry(min_container, font=('Segoe UI', 13), 
                                          bg='white', relief='solid', bd=1, width=15)
        self.widgets['age_min'].pack(side='left', ipady=4)
        
        # Max age - side by side layout
        max_container = tk.Frame(age_controls, bg=self.colors['bg_warning'])
        max_container.pack(fill='x')
        
        tk.Label(max_container, text="Maximum:", bg=self.colors['bg_warning'], fg=self.colors['text_primary'],
                font=('Segoe UI', 12, 'bold'), width=12, anchor='w').pack(side='left', padx=(0, 10))
        self.widgets['age_max'] = tk.Entry(max_container, font=('Segoe UI', 13),
                                          bg='white', relief='solid', bd=1, width=15)
        self.widgets['age_max'].pack(side='left', ipady=4)
    
    def _create_type_selection_section(self, parent):
        """Create supernova type selection section for middle column"""
        section_frame = self._create_colorful_section(parent, "🔬 Supernova Types", self.colors['bg_info'])
        
        # Supernova Type Selection with Buttons
        type_frame = tk.Frame(section_frame, bg=self.colors['bg_info'])
        type_frame.pack(fill='x', pady=(8, 12))
        
        type_title = tk.Label(type_frame, text="Supernova Types:", font=('Segoe UI', 14, 'bold'),
                             bg=self.colors['bg_info'], fg=self.colors['text_primary'])
        type_title.pack(anchor='w', pady=(0, 10))
        
        # Help text
        help_label = tk.Label(type_frame, text="All types start unselected (grey) = all templates used. Select specific types (green) to filter to only those:",
                             font=('Segoe UI', 11, 'normal'), bg=self.colors['bg_info'], fg=self.colors['text_secondary'])
        help_label.pack(anchor='w', pady=(0, 12))
        
        # Type buttons in a grid
        button_container = tk.Frame(type_frame, bg=self.colors['bg_info'])
        button_container.pack(fill='x')
        
        # Main supernova types with colors and their subtypes
        types_info = [
            ('Ia', self.colors['accent_blue'], ['Ia-norm', 'Ia-91T', 'Ia-91bg', 'Ia-csm', 'Ia-pec', 'Ia-02cx', 'Ia-03fg', 'Ia-02es', 'Ia-Ca-rich']),
            ('Ib', self.colors['accent_green'], ['Ib-norm', 'Ib-pec', 'IIb', 'Ibn', 'Ib-Ca-rich', 'Ib-csm']),
            ('Ic', self.colors['accent_orange'], ['Ic-norm', 'Ic-pec', 'Ic-Broad', 'Icn', 'Ic-Ca-rich', 'Ic-csm']),
            ('II', '#9370DB', ['IIP', 'II-pec', 'IIn', 'IIL', 'IIn-pec']),
            ('Galaxy', '#8A2BE2', ['Gal-E', 'Gal-S0', 'Gal-Sa', 'Gal-Sb', 'Gal-Sc', 'Gal-SB']),
            ('Star', '#FFD700', ['M-star', 'C-star']),
            ('AGN', '#FF6347', ['AGN-type1', 'QSO']),
            ('SLSN', '#20B2AA', ['SLSN-I', 'SLSN-Ib', 'SLSN-Ic', 'SLSN-II', 'SLSN-IIn']),
            ('LFBOT', '#84cc16', ['18cow', '20xnd']),
            ('TDE', '#f59e0b', ['TDE-H', 'TDE-He', 'TDE-H-He', 'TDE-Ftless']),
            ('KN', '#ef4444', ['17gfo']),
            ('GAP', '#6b7280', ['LRN', 'LBV', 'ILRT']),
        ]
        
        # Create type buttons in rows (3 per row)
        for i in range(0, len(types_info), 3):
            row_frame = tk.Frame(button_container, bg=self.colors['bg_info'])
            row_frame.pack(fill='x', pady=3)
            
            for j in range(3):
                if i + j < len(types_info):
                    type_name, color, subtypes = types_info[i + j]
                    self._create_type_button(row_frame, type_name, color, subtypes)
    
    def _create_max_templates_section(self, parent):
        """Create max templates section for right column"""
        section_frame = self._create_colorful_section(parent, "📊 Template Limits", self.colors['bg_accent'])
        
        # Max output templates
        self._create_int_entry(section_frame, "max_output_templates", "Max Output Templates:",
                              default=10, tooltip="Maximum number of best templates to output")
    
    def _create_type_button(self, parent, type_name, color, subtypes):
        """Create a toggle button for supernova type selection with tooltip showing subtypes"""
        
        btn = tk.Button(parent, text=type_name,
                       bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                       font=('Segoe UI', 12, 'bold'),
                       relief='raised', bd=2, padx=18, pady=12,
                       cursor='hand2')
        btn.pack(side='left', padx=6, pady=3, fill='x', expand=True)
        
        # Store button immediately
        self.type_buttons[type_name] = btn
        
        # Create the command function with proper closure
        def make_toggle_command(button_name, button_color):
            def toggle_command():
                self._handle_type_selection(button_name, button_color)
            return toggle_command
        
        # Set the command
        btn.config(command=make_toggle_command(type_name, color))
        
        # Create tooltip showing subtypes
        self._create_tooltip(btn, type_name, subtypes)
    
    def _handle_type_selection(self, clicked_type, clicked_color):
        """Handle type button selection with multi-selection logic"""
        
        # Check if this type is currently selected
        is_currently_selected = clicked_type in self.selected_types
        
        print(f"🔘 Button clicked: {clicked_type}")
        
        if is_currently_selected:
            # Deselect this type
            self.selected_types.remove(clicked_type)
            self.type_buttons[clicked_type].config(bg=self.colors['bg_secondary'], 
                                                 fg=self.colors['text_secondary'],
                                                 relief='raised')
            print(f"  ❌ Deselected {clicked_type}")
        else:
            # Select this type (always use green color)
            self.selected_types.add(clicked_type)
            self.type_buttons[clicked_type].config(bg=self.colors['accent_green'], 
                                                 fg='white', 
                                                 relief='raised')
            print(f"  ✅ Selected {clicked_type}")
        
        print(f"🎯 Final selection: {self.selected_types}")
        
        # Update template status to show any conflicts
        self._update_template_status()
    
    def _create_tooltip(self, widget, type_name, subtypes):
        """Create a tooltip that shows subtypes when hovering over a type button"""
        def show_tooltip(event):
            # Create tooltip window
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='#333333')
            
            # Position tooltip near cursor
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.geometry(f"+{x}+{y}")
            
            # Title
            title_label = tk.Label(tooltip, text=f"{type_name} Subtypes:",
                                  font=('Segoe UI', 11, 'bold'),
                                  bg='#333333', fg='white',
                                  padx=8, pady=8)
            title_label.pack(pady=(4, 0))
            
            # Subtypes list
            subtypes_text = '\n'.join(f"• {subtype}" for subtype in subtypes)
            subtypes_label = tk.Label(tooltip, text=subtypes_text,
                                     font=('Segoe UI', 10),
                                     bg='#333333', fg='#cccccc',
                                     justify='left',
                                     padx=8, pady=8)
            subtypes_label.pack(pady=(0, 4))
            
            # Store tooltip reference
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        # Bind hover events
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
    
    def _create_template_button_section(self, parent):
        """Create simple template selection button section"""
        if not HAS_TEMPLATE_SUPPORT:
            return  # Skip if template support not available
            
        section_frame = self._create_colorful_section(parent, "📝 Template Selection", self.colors['bg_success'])
        
        # Instructions
        info_label = tk.Label(section_frame, 
                            text="Choose specific templates for analysis (optional)",
                            font=('Segoe UI', 11, 'normal'),
                            bg=self.colors['bg_success'], fg=self.colors['text_secondary'],
                            wraplength=350, justify='left')
        info_label.pack(anchor='w', pady=(0, 10))
        
        # Template selection button
        template_btn = tk.Button(section_frame, text="🔍 Select Templates...",
                               font=('Segoe UI', 12, 'bold'),
                               bg=self.colors['accent_blue'], fg='white',
                               relief='raised', bd=2, padx=20, pady=10,
                               cursor='hand2', command=self._open_template_selector)
        template_btn.pack(pady=(0, 10))
        
        # Status label to show selected count
        self.template_status_label = tk.Label(section_frame, 
                                            text="Using all templates (default)",
                                            font=('Segoe UI', 10, 'italic'),
                                            bg=self.colors['bg_success'], fg=self.colors['text_secondary'])
        self.template_status_label.pack()
        
        # Update status if we have existing selections
        self._update_template_status()

    def _open_template_selector(self):
        """Open the template selection dialog"""
        try:
            template_dialog = TemplateSelectionDialog(self.dialog, self.selected_templates.copy(), self.template_mode)
            result = template_dialog.show()
            
            if result is not None:
                self.selected_templates = result['templates']
                self.template_mode = result['mode']
                self._update_template_status()
                
        except Exception as e:
            messagebox.showerror("Template Selection Error", f"Could not open template selector: {e}")
    
    def _update_template_status(self):
        """Update the template status label"""
        if hasattr(self, 'template_status_label'):
            if self.selected_templates:
                count = len(self.selected_templates)
                mode_text = "Including" if self.template_mode == 'include' else "Excluding"
                status_text = f"{mode_text} {count} selected template{'s' if count != 1 else ''}"
                
                # Add note about type filter override if types are also selected
                if self.selected_types and self.template_mode == 'include':
                    status_text += f"\n(Type filter ignored - template selection takes precedence)"
                
                self.template_status_label.config(text=status_text)
            else:
                self.template_status_label.config(text="Using all templates (default)")

    def _create_output_section(self, parent):
        """Create colorful output options section"""
        section_frame = self._create_colorful_section(parent, "💾 Output Options", self.colors['bg_accent'])
        
        # Output checkboxes with modern styling - simplified to just two options
        options = [
            ("save_plots", "📈 Save all plots", self.colors['accent_purple']),
            ("save_summary", "📄 Save analysis summary", self.colors['accent_blue'])
        ]
        
        for key, label, color in options:
            self._create_modern_checkbox(section_frame, key, label, color)
    
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
        title_frame.pack(fill='x', padx=15, pady=(12, 8))
        
        title_label = tk.Label(title_frame, text=title,
                              font=('Segoe UI', 16, 'bold'),
                              bg=bg_color, fg=self.colors['text_primary'])
        title_label.pack(anchor='w')
        
        # Content area
        content_frame = tk.Frame(section_frame, bg=bg_color)
        content_frame.pack(fill='x', padx=15, pady=(8, 18))
        
        return content_frame
    
    def _create_float_entry(self, parent, key, label, default=0.0, tooltip=""):
        """Create a modern float entry widget with side-by-side layout"""
        row_frame = tk.Frame(parent, bg=parent.cget('bg'))
        row_frame.pack(fill='x', pady=(8, 12))
        
        # Label on the left
        label_widget = tk.Label(row_frame, text=label, font=('Segoe UI', 14, 'bold'),
                               bg=parent.cget('bg'), fg=self.colors['text_primary'],
                               width=18, anchor='w')
        label_widget.pack(side='left', padx=(0, 15))
        
        # Entry with modern styling on the right
        self.widgets[key] = tk.Entry(row_frame, font=('Segoe UI', 14), 
                                    bg='white', fg=self.colors['text_primary'],
                                    relief='solid', bd=1, insertbackground=self.colors['accent_blue'],
                                    width=12)
        self.widgets[key].pack(side='left', ipady=6)
        
        # Set default
        self.widgets[key].insert(0, str(default))
    
    def _create_int_entry(self, parent, key, label, default=0, tooltip=""):
        """Create a modern integer entry widget with side-by-side layout"""
        row_frame = tk.Frame(parent, bg=parent.cget('bg'))
        row_frame.pack(fill='x', pady=(8, 12))
        
        # Label on the left
        label_widget = tk.Label(row_frame, text=label, font=('Segoe UI', 14, 'bold'),
                               bg=parent.cget('bg'), fg=self.colors['text_primary'],
                               width=18, anchor='w')
        label_widget.pack(side='left', padx=(0, 15))
        
        # Entry with modern styling on the right
        self.widgets[key] = tk.Entry(row_frame, font=('Segoe UI', 14),
                                    bg='white', fg=self.colors['text_primary'],
                                    relief='solid', bd=1, insertbackground=self.colors['accent_blue'],
                                    width=12)
        self.widgets[key].pack(side='left', ipady=6)
        
        # Set default
        self.widgets[key].insert(0, str(default))
    
    def _create_modern_checkbox(self, parent, key, label, color):
        """Create a modern checkbox with color"""
        self.widgets[key] = tk.BooleanVar()
        
        row_frame = tk.Frame(parent, bg=parent.cget('bg'))
        row_frame.pack(fill='x', pady=(8, 12))
        
        # Create a simple but modern checkbox with larger font
        checkbox = tk.Checkbutton(row_frame, text=label,
                                 variable=self.widgets[key],
                                 font=('Segoe UI', 13, 'bold'),
                                 bg=parent.cget('bg'), fg=self.colors['text_primary'],
                                 activebackground=parent.cget('bg'),
                                 selectcolor='white',
                                 relief='flat', bd=0,
                                 padx=5, pady=5)
        checkbox.pack(anchor='w')
        
        return checkbox
    
    def _create_footer(self):
        """Create modern footer with gradient buttons"""
        footer_frame = tk.Frame(self.dialog, bg=self.colors['bg_secondary'], height=90)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        button_container = tk.Frame(footer_frame, bg=self.colors['bg_secondary'])
        button_container.pack(expand=True, pady=25)
        
        # Reset button
        reset_btn = tk.Button(button_container, text="🔄 Reset to Defaults",
                             font=('Segoe UI', 14, 'bold'),
                             bg=self.colors['accent_orange'], fg='white',
                             relief='raised', bd=2, padx=30, pady=15,
                             cursor='hand2', command=self._reset_defaults)
        reset_btn.pack(side='left', padx=(0, 25))
        
        # Cancel button
        cancel_btn = tk.Button(button_container, text="❌ Cancel",
                              font=('Segoe UI', 14, 'bold'),
                              bg=self.colors['text_secondary'], fg='white',
                              relief='raised', bd=2, padx=30, pady=15,
                              cursor='hand2', command=self._cancel)
        cancel_btn.pack(side='left', padx=25)
        
        # Apply button  
        apply_btn = tk.Button(button_container, text="✅ Apply Settings",
                             font=('Segoe UI', 14, 'bold'),
                             bg=self.colors['accent_green'], fg='white',
                             relief='raised', bd=2, padx=30, pady=15,
                             cursor='hand2', command=self._apply)
        apply_btn.pack(side='left', padx=(25, 0))
    
    def _load_current_values(self):
        """Load current parameter values into widgets"""
        if not self.params:
            return
            
        # Load simple values
        for key in ['zmin', 'zmax', 'rlapmin', 'lapmin', 'max_output_templates']:
            if key in self.params and key in self.widgets:
                self.widgets[key].delete(0, 'end')
                self.widgets[key].insert(0, str(self.params[key]))
        
        # Load age range
        if 'age_min' in self.params and self.params['age_min']:
            self.widgets['age_min'].delete(0, 'end')
            self.widgets['age_min'].insert(0, str(self.params['age_min']))
        
        if 'age_max' in self.params and self.params['age_max']:
            self.widgets['age_max'].delete(0, 'end') 
            self.widgets['age_max'].insert(0, str(self.params['age_max']))
        
        # Load type filter (convert to button selections)
        if 'type_filter' in self.params and self.params['type_filter']:
            type_string = str(self.params['type_filter'])
            selected_types = [t.strip() for t in type_string.split(',') if t.strip()]
            
            # Clear previous selections
            self.selected_types.clear()
            
            # Reset all buttons to grey first
            for btn_name, btn in self.type_buttons.items():
                btn.config(bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'], relief='raised')
            
            # Select all types from the saved configuration (always use green)
            for type_name in selected_types:
                if type_name in self.type_buttons:
                    self.selected_types.add(type_name)
                    btn = self.type_buttons[type_name]
                    btn.config(bg=self.colors['accent_green'], fg='white', relief='raised')
        
        # Load template selections (include mode)
        if 'template_filter' in self.params and self.params['template_filter']:
            if isinstance(self.params['template_filter'], str):
                template_names = [t.strip() for t in self.params['template_filter'].split(',') if t.strip()]
            elif isinstance(self.params['template_filter'], list):
                template_names = self.params['template_filter']
            else:
                template_names = []
            
            # Set selected templates in include mode
            self.selected_templates = set(template_names)
            self.template_mode = 'include'
            self._update_template_status()
        
        # Load template selections (exclude mode)
        elif 'exclude_templates' in self.params and self.params['exclude_templates']:
            if isinstance(self.params['exclude_templates'], str):
                template_names = [t.strip() for t in self.params['exclude_templates'].split(',') if t.strip()]
            elif isinstance(self.params['exclude_templates'], list):
                template_names = self.params['exclude_templates']
            else:
                template_names = []
            
            # Set selected templates in exclude mode
            self.selected_templates = set(template_names)
            self.template_mode = 'exclude'
            self._update_template_status()

        # Load checkboxes
        for key in ['output_main', 'output_fluxed', 'output_flattened', 'save_plots', 'verbose']:
            if key in self.params and key in self.widgets:
                value = self.params[key]
                if isinstance(value, str):
                    value = value == '1' or value.lower() == 'true'
                self.widgets[key].set(bool(value))
    
    def _reset_defaults(self):
        """Reset all values to defaults"""
        defaults = {
            'zmin': -0.01,
            'zmax': 1.0,
            'rlapmin': 5.0,
            'lapmin': 0.3,
            'max_output_templates': 10,
            'age_min': '',
            'age_max': '',
            'save_plots': False,
            'save_summary': False
        }
        
        # Reset entry widgets
        for key, value in defaults.items():
            if key in self.widgets:
                widget = self.widgets[key]
                if isinstance(widget, tk.BooleanVar):
                    widget.set(value)
                else:
                    widget.delete(0, 'end')
                    widget.insert(0, str(value))
        
        # Reset type selections
        self.selected_types.clear()
        for type_name, btn in self.type_buttons.items():
            btn.config(bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'], relief='raised')
        
        # Reset template selections
        self.selected_templates.clear()
        self.template_mode = 'include'
        self._update_template_status()
    
    def _validate_and_collect(self):
        """Validate and collect parameter values"""
        try:
            result = {}
            
            # Collect float values
            for key in ['zmin', 'zmax', 'rlapmin', 'lapmin']:
                value = self.widgets[key].get().strip()
                if value:
                    result[key] = float(value)
                else:
                    raise ValueError(f"{key} cannot be empty")
            
            # Collect integer values
            for key in ['max_output_templates']:
                value = self.widgets[key].get().strip()
                if value:
                    result[key] = int(value)
                else:
                    raise ValueError(f"{key} cannot be empty")
            
            # Collect optional age range
            age_min = self.widgets['age_min'].get().strip()
            age_max = self.widgets['age_max'].get().strip()
            
            if age_min:
                result['age_min'] = float(age_min)
            if age_max:
                result['age_max'] = float(age_max)
            
            # Collect type filter from selected buttons
            # If specific templates are selected, don't apply type filter
            # to avoid conflicts (template selection takes precedence)
            if self.selected_types and not self.selected_templates:
                result['type_filter'] = ','.join(sorted(self.selected_types))
            
            # Collect template filter from selected templates
            if self.selected_templates:
                if self.template_mode == 'include':
                    result['template_filter'] = list(sorted(self.selected_templates))
                else:  # exclude mode
                    result['exclude_templates'] = list(sorted(self.selected_templates))
            
            # Collect checkboxes
            for key in ['save_plots', 'save_summary']:
                result[key] = self.widgets[key].get()
            
            # Basic validation
            if result['zmin'] >= result['zmax']:
                raise ValueError("Minimum redshift must be less than maximum redshift")
            
            if result['rlapmin'] <= 0:
                raise ValueError("RLAP minimum must be positive")
                
            if result['lapmin'] <= 0 or result['lapmin'] > 1:
                raise ValueError("Overlap minimum must be between 0 and 1")
            
            if result['max_output_templates'] <= 0:
                raise ValueError("Max output templates must be positive")
            
            if 'age_min' in result and 'age_max' in result and result['age_min'] >= result['age_max']:
                raise ValueError("Minimum age must be less than maximum age")
            
            return result
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return None
    
    def _apply(self):
        """Apply settings and close dialog"""
        result = self._validate_and_collect()
        if result is not None:
            self.result = result
            self.dialog.destroy()
    
    def _cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.dialog.destroy()




class TemplateSelectionDialog:
    """
    Dual-list template selection dialog with support for both inclusion and exclusion modes.
    
    Features:
    - Left list: Available templates (with search)
    - Right list: Selected templates
    - Move buttons: Add/Remove individual or all templates
    - Mode selection: Include specific templates OR exclude specific templates
    - Only unique template names (no duplicates)
    """
    
    def __init__(self, parent, current_selection=None, mode='include'):
        """
        Initialize template selection dialog
        
        Parameters:
        -----------
        parent : tk.Widget
            Parent widget
        current_selection : set, optional
            Current template selection
        mode : str, optional
            Selection mode: 'include' (default) or 'exclude'
        """
        self.parent = parent
        self.dialog = None
        self.result = None
        self.current_selection = current_selection or set()
        self.mode = mode  # 'include' or 'exclude'
        
        # Template data
        self.available_templates = []
        self.unique_templates = {}  # name -> {type, subtype, count}
        self.filtered_templates = []
        
        # UI widgets
        self.search_var = None
        self.available_listbox = None
        self.selected_listbox = None
        self.mode_var = None
        
        # Discover templates
        self._discover_templates()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """
        Show dialog and return template selection result
        
        Returns:
        --------
        Dict[str, Any] or None
            Dictionary with 'templates' (set of names) and 'mode' ('include'/'exclude'),
            or None if cancelled
        """
        if not self.unique_templates:
            messagebox.showwarning("No Templates", "No templates found in templates directory.")
            return None
            
        self._create_dialog()
        self._setup_interface()
        self._load_current_selection()
        
        # Center and show
        self._center_dialog()
        self.dialog.grab_set()
        self.dialog.wait_window()
        
        return self.result
    
    def _discover_templates(self):
        """Discover unique templates from templates directory"""
        if not HAS_TEMPLATE_SUPPORT:
            return
            
        # Find templates directory
        templates_dir = None
        try:
            config_manager = ConfigurationManager()
            config = config_manager.get_configuration()
            templates_dir = config.get('paths', {}).get('templates_dir', 'templates')
        except Exception:
            possible_dirs = ['templates', 'custom_templates', './templates', '../templates']
            for template_dir in possible_dirs:
                if os.path.exists(template_dir):
                    templates_dir = template_dir
                    break
        
        # After basic discovery, ensure the directory really contains template files
        if templates_dir and os.path.exists(templates_dir):
            # Validate presence of template files (.hdf5 or .lnw)
            has_templates = any(fname.endswith(('.hdf5', '.lnw')) for fname in os.listdir(templates_dir))
            if not has_templates:
                _LOGGER.debug(f"Path {templates_dir} exists but contains no template files. Looking elsewhere…")
                templates_dir = None

        if (not templates_dir or not os.path.exists(templates_dir)) and _find_templates_directory is not None:
            try:
                discovered_dir = _find_templates_directory()
                if discovered_dir and os.path.exists(discovered_dir):
                    templates_dir = str(discovered_dir)
                    _LOGGER.info(f"✅ Using fallback templates directory: {templates_dir}")
            except Exception as _e:
                _LOGGER.debug(f"Template finder fallback failed: {_e}")

        # Final guard – bail if we still have nothing usable
        if not templates_dir or not os.path.exists(templates_dir):
            return
            
        try:
            # Get template info
            template_info = get_template_info(templates_dir)
            
            # Create unique template dictionary (handle multiple epochs)
            self.unique_templates = {}
            for template in template_info.get('templates', []):
                name = template.get('name', 'Unknown')
                t_type = template.get('type', 'Unknown')
                subtype = template.get('subtype', 'Unknown')
                
                if name not in self.unique_templates:
                    self.unique_templates[name] = {
                        'type': t_type,
                        'subtype': subtype,
                        'count': 1
                    }
                else:
                    self.unique_templates[name]['count'] += 1
                    
        except Exception as e:
            print(f"Warning: Could not load template information: {e}")
            # Fallback to .lnw files
            try:
                template_files = glob.glob(os.path.join(templates_dir, '*.lnw'))
                for template_file in template_files:
                    name = os.path.splitext(os.path.basename(template_file))[0]
                    if name not in self.unique_templates:
                        self.unique_templates[name] = {
                            'type': 'Unknown',
                            'subtype': 'Unknown', 
                            'count': 1
                        }
                    else:
                        self.unique_templates[name]['count'] += 1
            except Exception:
                pass
        
        # Create display list
        self.available_templates = []
        for name, info in sorted(self.unique_templates.items()):
            count_str = f" [{info['count']} epochs]" if info['count'] > 1 else ""
            display_name = f"{name} ({info['type']}/{info['subtype']}){count_str}"
            self.available_templates.append({
                'name': name,
                'display_name': display_name,
                'type': info['type'],
                'subtype': info['subtype'],
                'count': info['count']
            })
        
        self.filtered_templates = self.available_templates.copy()
    
    def _create_dialog(self):
        """Create dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("🔍 Select Templates")
        self.dialog.geometry("900x600")
        self.dialog.resizable(True, True)
        self.dialog.minsize(800, 500)
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
    
    def _setup_interface(self):
        """Setup dialog interface"""
        # Header
        header_frame = tk.Frame(self.dialog, bg='#8b5cf6', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="🔍 Template Selection",
                               font=('Segoe UI', 18, 'bold'),
                               bg='#8b5cf6', fg='white')
        header_label.pack(expand=True)
        
        # Main content
        main_frame = tk.Frame(self.dialog, bg='#f8fafc')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Search section
        search_frame = tk.Frame(main_frame, bg='#f8fafc')
        search_frame.pack(fill='x', pady=(0, 15))
        
        search_label = tk.Label(search_frame, text="🔍 Search Templates:",
                               font=('Segoe UI', 12, 'bold'),
                               bg='#f8fafc', fg='#1e293b')
        search_label.pack(anchor='w')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=('Segoe UI', 11), relief='solid', bd=1)
        search_entry.pack(fill='x', pady=(5, 0))
        self.search_var.trace('w', self._on_search)
        
        # Mode selection
        mode_frame = tk.Frame(main_frame, bg='#f8fafc')
        mode_frame.pack(fill='x', pady=(0, 15))
        
        mode_label = tk.Label(mode_frame, text="Mode:",
                             font=('Segoe UI', 12, 'bold'),
                             bg='#f8fafc', fg='#1e293b')
        mode_label.pack(anchor='w')
        
        self.mode_var = tk.StringVar(value=self.mode)
        # Use tk.OptionMenu instead of ttk.Combobox to avoid Tkinter issues
        mode_option = tk.OptionMenu(mode_frame, self.mode_var, 
                                   'include', 'exclude')
        mode_option.config(font=('Segoe UI', 11), bg='white', relief='solid', 
                          bd=1, highlightthickness=0, activebackground='#e2e8f0')
        mode_option.pack(fill='x', pady=(5, 0))
        
        # Lists section
        lists_frame = tk.Frame(main_frame, bg='#f8fafc')
        lists_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Available templates (left)
        left_frame = tk.Frame(lists_frame, bg='#f8fafc')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        left_label = tk.Label(left_frame, text=f"📋 Available Templates ({len(self.available_templates)})",
                             font=('Segoe UI', 12, 'bold'),
                             bg='#f8fafc', fg='#1e293b')
        left_label.pack(anchor='w')
        
        # Available listbox with scrollbar
        left_list_frame = tk.Frame(left_frame, bg='#f8fafc')
        left_list_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.available_listbox = tk.Listbox(left_list_frame, font=('Segoe UI', 10),
                                          relief='solid', bd=1, selectmode='extended')
        left_scrollbar = tk.Scrollbar(left_list_frame, orient='vertical')
        self.available_listbox.config(yscrollcommand=left_scrollbar.set)
        left_scrollbar.config(command=self.available_listbox.yview)
        
        self.available_listbox.pack(side='left', fill='both', expand=True)
        left_scrollbar.pack(side='right', fill='y')
        
        # Selected templates (right)
        right_frame = tk.Frame(lists_frame, bg='#f8fafc')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.right_label = tk.Label(right_frame, text="✅ Selected Templates (0)",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#f8fafc', fg='#1e293b')
        self.right_label.pack(anchor='w')
        
        # Selected listbox with scrollbar
        right_list_frame = tk.Frame(right_frame, bg='#f8fafc')
        right_list_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.selected_listbox = tk.Listbox(right_list_frame, font=('Segoe UI', 10),
                                         relief='solid', bd=1, selectmode='extended')
        right_scrollbar = tk.Scrollbar(right_list_frame, orient='vertical')
        self.selected_listbox.config(yscrollcommand=right_scrollbar.set)
        right_scrollbar.config(command=self.selected_listbox.yview)
        
        self.selected_listbox.pack(side='left', fill='both', expand=True)
        right_scrollbar.pack(side='right', fill='y')

        # ---------------------------
        # 🌟 Increase font sizes for readability
        # ---------------------------
        larger_label_font = ('Segoe UI', 14, 'bold')
        medium_font = ('Segoe UI', 12)
        listbox_font = ('Segoe UI', 12)

        search_label.config(font=larger_label_font)
        mode_label.config(font=larger_label_font)
        left_label.config(font=larger_label_font)
        self.right_label.config(font=larger_label_font)

        search_entry.config(font=medium_font)
        mode_option.config(font=('Segoe UI', 13))

        self.available_listbox.config(font=listbox_font)
        self.selected_listbox.config(font=listbox_font)
        # ---------------------------
        
        # Control buttons (center)
        button_frame = tk.Frame(lists_frame, bg='#f8fafc', width=120)
        button_frame.pack(side='left', fill='y', padx=10)
        button_frame.pack_propagate(False)
        
        # Center buttons vertically
        center_frame = tk.Frame(button_frame, bg='#f8fafc')
        center_frame.pack(expand=True)
        
        add_btn = tk.Button(center_frame, text="→ Add",
                           font=('Segoe UI', 10, 'bold'),
                           bg='#10b981', fg='white',
                           relief='raised', bd=2, padx=15, pady=8,
                           cursor='hand2', command=self._add_selected)
        add_btn.pack(pady=5)
        
        add_all_btn = tk.Button(center_frame, text="→→ Add All",
                               font=('Segoe UI', 10, 'bold'),
                               bg='#059669', fg='white',
                               relief='raised', bd=2, padx=15, pady=8,
                               cursor='hand2', command=self._add_all)
        add_all_btn.pack(pady=5)
        
        remove_btn = tk.Button(center_frame, text="← Remove",
                              font=('Segoe UI', 10, 'bold'),
                              bg='#ef4444', fg='white',
                              relief='raised', bd=2, padx=15, pady=8,
                              cursor='hand2', command=self._remove_selected)
        remove_btn.pack(pady=5)
        
        remove_all_btn = tk.Button(center_frame, text="←← Remove All",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#dc2626', fg='white',
                                  relief='raised', bd=2, padx=15, pady=8,
                                  cursor='hand2', command=self._remove_all)
        remove_all_btn.pack(pady=5)
        
        # Double-click bindings
        self.available_listbox.bind('<Double-Button-1>', lambda e: self._add_selected())
        self.selected_listbox.bind('<Double-Button-1>', lambda e: self._remove_selected())
        
        # Footer buttons
        footer_frame = tk.Frame(self.dialog, bg='#e2e8f0', height=70)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        button_container = tk.Frame(footer_frame, bg='#e2e8f0')
        button_container.pack(expand=True, pady=15)
        
        cancel_btn = tk.Button(button_container, text="❌ Cancel",
                              font=('Segoe UI', 12, 'bold'),
                              bg='#64748b', fg='white',
                              relief='raised', bd=2, padx=25, pady=12,
                              cursor='hand2', command=self._cancel)
        cancel_btn.pack(side='left', padx=(0, 15))
        
        ok_btn = tk.Button(button_container, text="✅ OK",
                          font=('Segoe UI', 12, 'bold'),
                          bg='#10b981', fg='white',
                          relief='raised', bd=2, padx=25, pady=12,
                          cursor='hand2', command=self._ok)
        ok_btn.pack(side='left')
    
    def _center_dialog(self):
        """Center dialog on parent"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (900 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (600 // 2)
        self.dialog.geometry(f"900x600+{x}+{y}")
    
    def _load_current_selection(self):
        """Load current template selection"""
        # Populate available list
        self._update_available_list()
        
        # Populate selected list
        for template_name in sorted(self.current_selection):
            if template_name in self.unique_templates:
                info = self.unique_templates[template_name]
                count_str = f" [{info['count']} epochs]" if info['count'] > 1 else ""
                display_name = f"{template_name} ({info['type']}/{info['subtype']}){count_str}"
                self.selected_listbox.insert('end', display_name)
        
        self._update_counts()
    
    def _update_available_list(self):
        """Update available templates list"""
        self.available_listbox.delete(0, 'end')
        
        # Only show templates not already selected
        for template in self.filtered_templates:
            if template['name'] not in self.current_selection:
                self.available_listbox.insert('end', template['display_name'])
    
    def _update_counts(self):
        """Update count labels"""
        available_count = self.available_listbox.size()
        selected_count = self.selected_listbox.size()
        
        self.right_label.config(text=f"✅ Selected Templates ({selected_count})")
    
    def _on_search(self, *args):
        """Handle search input"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.filtered_templates = self.available_templates.copy()
        else:
            self.filtered_templates = []
            for template in self.available_templates:
                if (search_term in template['name'].lower() or 
                    search_term in template['type'].lower() or
                    search_term in template['subtype'].lower()):
                    self.filtered_templates.append(template)
        
        self._update_available_list()
    
    def _add_selected(self):
        """Add selected templates from available to selected"""
        selections = self.available_listbox.curselection()
        if not selections:
            return
            
        # Get selected template names
        for idx in reversed(selections):  # Reverse to maintain indices
            display_name = self.available_listbox.get(idx)
            
            # Find template name from display name
            template_name = None
            for template in self.filtered_templates:
                if template['display_name'] == display_name:
                    template_name = template['name']
                    break
            
            if template_name:
                self.current_selection.add(template_name)
                self.selected_listbox.insert('end', display_name)
                self.available_listbox.delete(idx)
        
        self._update_counts()
    
    def _add_all(self):
        """Add all available templates to selected"""
        # Add all filtered templates
        for template in self.filtered_templates:
            if template['name'] not in self.current_selection:
                self.current_selection.add(template['name'])
                self.selected_listbox.insert('end', template['display_name'])
        
        # Clear available list
        self.available_listbox.delete(0, 'end')
        self._update_counts()
    
    def _remove_selected(self):
        """Remove selected templates from selected list"""
        selections = self.selected_listbox.curselection()
        if not selections:
            return
            
        # Get selected template names and remove them
        for idx in reversed(selections):
            display_name = self.selected_listbox.get(idx)
            
            # Find template name
            template_name = None
            for name, info in self.unique_templates.items():
                count_str = f" [{info['count']} epochs]" if info['count'] > 1 else ""
                if display_name == f"{name} ({info['type']}/{info['subtype']}){count_str}":
                    template_name = name
                    break
            
            if template_name and template_name in self.current_selection:
                self.current_selection.remove(template_name)
                self.selected_listbox.delete(idx)
        
        # Refresh available list to show newly available templates
        self._update_available_list()
        self._update_counts()
    
    def _remove_all(self):
        """Remove all selected templates"""
        self.current_selection.clear()
        self.selected_listbox.delete(0, 'end')
        self._update_available_list()
        self._update_counts()
    
    def _ok(self):
        """Confirm selection and close"""
        # Return both the selected templates and the mode
        self.result = {
            'templates': self.current_selection.copy(),
            'mode': self.mode_var.get()
        }
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel selection and close"""
        self.result = None
        self.dialog.destroy()


def show_snid_options_dialog(parent, current_params=None) -> Optional[Dict[str, Any]]:
    """
    Show the modern SNID options dialog.
    
    Args:
        parent: Parent window
        current_params: Current parameter values dict
        
    Returns:
        Parameter dictionary if applied, None if cancelled
    """
    dialog = ModernSNIDOptionsDialog(parent, current_params)
    return dialog.show()


# Backward compatibility aliases
show_configuration_dialog = show_snid_options_dialog
SimpleSNIDOptionsDialog = ModernSNIDOptionsDialog  # Update the class alias
ModernConfigurationDialog = ModernSNIDOptionsDialog 
