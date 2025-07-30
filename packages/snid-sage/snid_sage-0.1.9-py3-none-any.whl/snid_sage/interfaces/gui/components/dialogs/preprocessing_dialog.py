"""
Advanced Preprocessing Dialog Component - Refactored Modular Design
=================================================================

Clean, modular preprocessing wizard using composition pattern.
Left panel: Step navigation and options
Right panel: Dual plots managed by PreviewPlotManager

Features:
- 6-step preprocessing workflow with split-panel UI
- Modular component architecture
- Real-time preview via PreviewCalculator
- Interactive continuum editing via InteractiveContinuumWidget
- Professional matplotlib visualization via PreviewPlotManager
- Enhanced UI with consistent fonts and adaptive text wrapping
"""

import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
import tkinter.font as tkfont  # ✅ Import for dynamic font scaling

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.preprocessing_dialog')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.preprocessing_dialog')

# Import modular components
from snid_sage.interfaces.gui.features.preprocessing.preview_calculator import PreviewCalculator
from snid_sage.interfaces.gui.components.plots.preview_plot_manager import PreviewPlotManager
from snid_sage.interfaces.gui.components.widgets.interactive_continuum_widget import InteractiveContinuumWidget

# Import unified systems for OS-native window controls
try:
    from snid_sage.interfaces.gui.utils.universal_window_manager import get_window_manager, DialogSize
    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError:
    UNIFIED_SYSTEMS_AVAILABLE = False

# Import SNID constants and preprocessing functions
from snid_sage.snid.snid import NW, MINW, MAXW
from snid_sage.snid.preprocessing import (
    init_wavelength_grid, get_grid_params, medfilt, medwfilt, 
    clip_aband, clip_sky_lines, clip_host_emission_lines,
    apply_wavelength_mask, log_rebin, fit_continuum, apodize
)


class PreprocessingDialog:
    """Clean, modular preprocessing dialog using component composition"""
    
    def __init__(self, parent, preprocessor):
        self.parent = parent
        self.preprocessor = preprocessor
        self.window = None
        
        # Get unified window manager for OS-native controls
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager = get_window_manager()
        
        # Current step and completion tracking
        self.current_step = 0
        self.total_steps = 6  # Updated to 6 steps: Masking+Clipping, Filtering, Rebinning+Scaling, Continuum, Apodization, Final Review
        self.step_names = [
            "Masking & Clipping Operations", "Savitzky-Golay Filtering", "Log-wavelength Rebinning & Flux Scaling",
            "Continuum Fitting & Interactive Editing", "Apodization", "Final Review"
        ]
        
        # Track processing state
        self.processing_complete = False
        
        # Add initialization flag to prevent rapid multiple plot updates
        self._initializing = True
        self._canvas_ready = False
        
        # Define consistent font scheme
        self._define_font_scheme()
        
        # Initialize modular components
        self._initialize_components()
        
        # UI variables for all steps
        self.init_step_variables()
        
        # Determine unified theme manager (if parent provides one)
        self.theme_manager = getattr(parent, 'theme_manager', None)
        
        # Color palette – prefer UnifiedThemeManager, otherwise fall back to hard-coded light palette
        if self.theme_manager is not None:
            tm = self.theme_manager.get_color  # shortcut
            self.colors = {
                'bg_main': tm('bg_primary'),
                'bg_panel': tm('bg_secondary'),
                'bg_step': tm('bg_tertiary'),
                'bg_step_active': tm('accent_primary'),
                'bg_current': tm('accent_primary'),
                'button_bg': tm('bg_tertiary'),
                'text_primary': tm('text_primary'),
                'text_secondary': tm('text_secondary'),
                'accent': tm('accent_primary'),
                'success': tm('btn_success'),
                'warning': tm('btn_warning'),
                'disabled': tm('disabled')
            }
        else:
            # Fallback (light) palette identical to UnifiedThemeManager defaults
            self.colors = {
                'bg_main': '#f8fafc',
                'bg_panel': '#ffffff',
                'bg_step': '#f1f5f9',
                'bg_step_active': '#3b82f6',
                'bg_current': '#3b82f6',
                'button_bg': '#f1f5f9',
                'text_primary': '#1e293b',
                'text_secondary': '#475569',
                'accent': '#3b82f6',
                'success': '#10b981',
                'warning': '#f59e0b',
                'disabled': '#e2e8f0'
            }
    
    def _define_font_scheme(self):
        """Define consistent font scheme for the entire dialog"""
        base_font_family = 'Segoe UI'
        self.fonts = {
            'title': (base_font_family, 16, 'bold'),           # Step titles
            'section_header': (base_font_family, 13, 'bold'),  # Section headers (LabelFrames)
            'body': (base_font_family, 13, 'normal'),          # Regular body text (increased from 12)
            'body_bold': (base_font_family, 13, 'bold'),       # Emphasized body text (increased from 12)
            'button': (base_font_family, 11, 'bold'),          # Buttons
            'small': (base_font_family, 12, 'normal'),         # Small text/help (increased from 10)
            'monospace': ('Consolas', 11, 'normal')            # Code/data display
        }
    
    def _initialize_components(self):
        """Initialize modular components"""
        # Initialize preview calculator
        if self.preprocessor.has_spectrum_data():
            self.preview_calc = PreviewCalculator(
                self.preprocessor.current_wave, 
                self.preprocessor.current_flux
            )
        else:
            self.preview_calc = None
        
        # Plot manager and interactive widget will be initialized after UI creation
        self.plot_manager = None
        self.interactive_widget = None
    
    def init_step_variables(self):
        """Initialize UI variables for all preprocessing steps"""
        # Step 0: Masking (NEW)
        self.mask_regions = []  # List of (start, end) tuples for mask regions
        self.mask_entry_var = tk.StringVar(value="")
        self.mask_input_var = tk.StringVar(value="")  # For manual mask input field
        
        # Step 1: Clipping (was Step 0)
        self.aband_var = tk.BooleanVar(value=False)
        self.sky_var = tk.BooleanVar(value=False)
        self.sky_width_var = tk.StringVar(value="40.0")
        
        # Step 2: Savitzky-Golay filtering (was Step 1)
        self.filter_type_var = tk.StringVar(value="none")
        self.fixed_savgol_var = tk.StringVar(value="11")
        self.polyorder_var = tk.StringVar(value="3")
        
        # Step 3: Log rebinning with flux scaling (required) (was Steps 2+3)
        self.log_rebin_var = tk.BooleanVar(value=True)  # Always true - required step
        
        # Step 5: Continuum fitting (was Step 4)
        self.continuum_type_var = tk.StringVar(value="spline")
        self.gauss_sigma_var = tk.StringVar(value="auto")  # Start with auto calculation
        self.spline_knots_var = tk.StringVar(value="13")
        
        # Step 6: Apodization (was Step 5)
        self.apodize_var = tk.BooleanVar(value=True)
        self.apod_percent_var = tk.StringVar(value="10.0")
        
        # Collect all variables for binding
        self.bind_variables = [
            self.mask_entry_var,  # Masking variable
            self.aband_var, self.sky_var, self.sky_width_var,
            self.filter_type_var, self.fixed_savgol_var, self.polyorder_var,
            self.continuum_type_var, self.gauss_sigma_var, self.spline_knots_var,
            self.apod_percent_var
        ]
    
    def bind_preview_updates(self):
        """Bind variable changes to preview updates"""
        def safe_update_preview(*args):
            try:
                # Only update if in correct mode
                if hasattr(self, 'current_step'):
                    self.update_preview()
            except Exception:
                pass

        # Bind all relevant variables
        # Masking variables
        self.mask_entry_var.trace('w', safe_update_preview)  # Add this for live mask updates
        
        # Clipping variables
        self.aband_var.trace('w', safe_update_preview)
        self.sky_var.trace('w', safe_update_preview)
        self.sky_width_var.trace('w', safe_update_preview)
        
        # Filtering variables
        self.filter_type_var.trace('w', safe_update_preview)
        self.fixed_savgol_var.trace('w', safe_update_preview)
        self.polyorder_var.trace('w', safe_update_preview)
        
        # Rebinning variables (includes scaling)
        self.log_rebin_var.trace('w', safe_update_preview)
        
        # Continuum fitting variables
        self.continuum_type_var.trace('w', safe_update_preview)
        self.gauss_sigma_var.trace('w', safe_update_preview)
        self.spline_knots_var.trace('w', safe_update_preview)
        
        # Apodization variables
        self.apodize_var.trace('w', safe_update_preview)
        self.apod_percent_var.trace('w', safe_update_preview)
    
    def show(self):
        """Display the preprocessing dialog"""
        if not self.preprocessor.has_spectrum_data():
            messagebox.showerror("Error", "No spectrum data loaded for preprocessing.")
            return
        
        # Create dialog window
        self.window = tk.Toplevel(self.parent)
        self.window.title("Advanced Preprocessing - SNID SAGE")
        self.window.configure(bg=self.colors['bg_main'])
        
        # Set window size and properties with OS-native controls
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager.setup_dialog(self.window, "🔧 Advanced Preprocessing - SNID SAGE", DialogSize.XLARGE)
        else:
            self.window.geometry("1400x900")
            self.window.resizable(True, True)
        
        # Create the split panel layout (this creates the plots)
        self.create_split_panel_layout()
        
        # Setup cleanup on close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Mark canvas as ready and finish initialization
        self._canvas_ready = True
        
        # Bind preview updates AFTER canvas is ready
        self.bind_preview_updates()
        
        # Finish initialization and allow updates
        self._initializing = False
        
        # Now do the initial preview update
        self.update_preview()
        
        # Add window resize handler AFTER initial setup to avoid immediate triggers
        self.window.bind('<Configure>', self._on_window_resize)
        
        # Make modal (only if not using unified window manager, as it handles this)
        if not UNIFIED_SYSTEMS_AVAILABLE:
            self.window.transient(self.parent)
            self.window.grab_set()
            # Center the window AFTER all setup is complete
            self.center_window()
        
        # Focus
        self.window.focus_set()
    
    def center_window(self):
        """Center dialog on parent window with fallback to screen centering (fallback method)"""
        if UNIFIED_SYSTEMS_AVAILABLE:
            # Window manager handles centering automatically
            return
            
        self.window.update_idletasks()
        
        try:
            # Center on parent window
            if hasattr(self.parent, 'master') and self.parent.master:
                parent_widget = self.parent.master
            else:
                parent_widget = self.parent
                
            x = parent_widget.winfo_x() + (parent_widget.winfo_width() // 2) - (1400 // 2)
            y = parent_widget.winfo_y() + (parent_widget.winfo_height() // 2) - (900 // 2)
            self.window.geometry(f"1400x900+{x}+{y}")
            
        except (AttributeError, tk.TclError):
            # Fallback: center on screen
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            x = (screen_width // 2) - (1400 // 2)
            y = (screen_height // 2) - (900 // 2)
            self.window.geometry(f"1400x900+{x}+{y}")
    
    def create_split_panel_layout(self):
        """Create the main split-panel layout"""
        # Main container
        main_frame = tk.Frame(self.window, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create left and right panels - increase left panel width for better text display
        self.left_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], width=450, relief='raised', bd=1)
        self.left_panel.pack(side='left', fill='y', padx=(0, 5))
        self.left_panel.pack_propagate(False)
        
        # 🔄 Bind resize event to adjust text wraplengths dynamically
        self.left_panel.bind('<Configure>', self._on_left_panel_resize)
        
        self.right_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], relief='raised', bd=1)
        self.right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Setup panels
        self.create_left_panel()
        self.create_right_panel()
    
    def create_left_panel(self):
        """Create the left navigation panel"""
        # Remove the header with step summary - go directly to options
        
        # Options area (fill entire left panel)
        self.options_frame = tk.Frame(self.left_panel, bg=self.colors['bg_panel'])
        self.options_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Control buttons at bottom
        self.create_control_buttons()
        
        # Initialize first step
        self.update_step_display()
    
    def create_control_buttons(self):
        """Create navigation and action buttons"""
        button_frame = tk.Frame(self.left_panel, bg=self.colors['bg_panel'])
        button_frame.pack(side='bottom', fill='x', padx=15, pady=15)
        
        # Action buttons only - no navigation buttons
        action_frame = tk.Frame(button_frame, bg=self.colors['bg_panel'])
        action_frame.pack(fill='x')
        
        # Apply Step button
        self.apply_btn = tk.Button(action_frame, text="Apply Step",
                                  command=self.apply_current_step,
                                  font=self.fonts['button'],
                                  bg=self.colors['success'], fg='white',
                                  relief='raised', bd=2, padx=20, pady=8)
        self.apply_btn.pack(side='left', padx=(0, 10))
        
        # Revert to Previous Step button
        self.revert_btn = tk.Button(action_frame, text="↺ Revert to Previous Step",
                                   command=self.revert_to_previous_step,
                                   font=self.fonts['button'],
                                   bg=self.colors['warning'], fg='white',
                                   relief='raised', bd=2, padx=15, pady=8)
        self.revert_btn.pack(side='left', padx=(0, 10))
        
        # Finish button (initially hidden)
        self.finish_btn = tk.Button(action_frame, text="Finish",
                                   command=self.finish_preprocessing,
                                   font=self.fonts['button'],
                                   bg=self.colors['accent'], fg='white',
                                   relief='raised', bd=2, padx=20, pady=8)
        self.finish_btn.pack(side='right')
    
    def create_right_panel(self):
        """Create the right visualization panel using PreviewPlotManager"""
        # Header
        viz_header = tk.Frame(self.right_panel, bg=self.colors['bg_panel'])
        # Trim padding: smaller horizontal margin and less vertical gap below header
        viz_header.pack(fill='x', padx=8, pady=(12, 4))
        
        title_label = tk.Label(viz_header, text="📊 Live Preview", 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
        title_label.pack(anchor='w')
        
        # Create plot container frame
        plot_frame = tk.Frame(self.right_panel, bg=self.colors['bg_panel'])
        plot_frame.pack(fill='both', expand=True)
        
        # Initialize plot manager
        self.plot_manager = PreviewPlotManager(plot_frame, self.colors)
        
        # Initialize interactive continuum widget
        if self.preview_calc:
            self.interactive_widget = InteractiveContinuumWidget(
                self.preview_calc, self.plot_manager, self.colors
            )
            self.interactive_widget.set_update_callback(self.update_preview)
        
        # Initialize interactive masking variables
        self.span_selector = None
        self.masking_active = False
    
    def update_step_display(self):
        """Update the UI to show options for the current step"""
        try:
            # Stop interactive masking when changing steps
            if hasattr(self, 'masking_active') and self.masking_active:
                self.stop_interactive_masking()
            
            # Clear the current options
            for widget in self.options_frame.winfo_children():
                widget.destroy()
            
            # Check if we've moved to step 0 (masking) - force preview update to clear previous step masks
            if self.current_step == 0:
                # Schedule the preview update after the UI has been updated
                self.window.after_idle(self.update_preview)
            
            # Create options for the current step
            self.create_step_options()
            
            # Apply unified styling and initial text wrapping
            self._apply_unified_styles()
            
            # Set initial wraplength based on current panel width
            if hasattr(self.left_panel, 'winfo_width'):
                try:
                    panel_width = self.left_panel.winfo_width()
                    if panel_width > 100:  # Valid width
                        effective_width = max(150, panel_width - 40)
                        self._update_wraplengths(effective_width)
                        self._last_wrap_width = panel_width
                except:
                    pass
            
            # Update navigation buttons
            self.update_button_states()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update step display: {e}")
    
    def create_step_options(self):
        """Create options panel for current step"""
        step_title = tk.Label(self.options_frame, 
                             text=f"Step {self.current_step + 1}: {self.step_names[self.current_step]}",
                             font=self.fonts['title'],
                             bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
        step_title.pack(anchor='w', pady=(0, 10))
        
        if self.current_step == 0:
            self.create_masking_options()
        elif self.current_step == 1:
            self.create_filtering_options()
        elif self.current_step == 2:
            self.create_rebinning_with_scaling_options()
        elif self.current_step == 3:
            self.create_continuum_options()
        elif self.current_step == 4:
            self.create_apodization_options()
        elif self.current_step == 5:
            self.create_final_review_options()
    
    def create_masking_options(self):
        """Create options for masking step"""
        # Description
        desc_label = tk.Label(self.options_frame,
                             text="Mask wavelength regions to exclude from analysis",
                             font=self.fonts['body'],
                             bg=self.colors['bg_panel'], fg=self.colors['text_secondary'])
        desc_label.pack(anchor='w', pady=(0, 10))

        # --- 1. Interactive masking section (moved to top) ---
        interactive_frame = tk.LabelFrame(
            self.options_frame,
            text="Interactive Masking",
            font=self.fonts['section_header'],
            bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
        )
        interactive_frame.pack(fill='x', pady=(0, 15))

        self.interactive_mask_btn = tk.Button(
            interactive_frame,
            text="📐 Interactive Select",
            bg=self.colors['accent'], fg='white',
            font=self.fonts['button'], relief='raised', bd=2,
            command=self.start_interactive_masking,
        )
        self.interactive_mask_btn.pack(pady=5)

        # Inline instructions with proper wrapping
        info_label = tk.Label(
            interactive_frame,
            text=(
                "📐 Drag across the top plot to add mask regions.\n"
                "Red shading shows each selection."
            ),
            font=self.fonts['small'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_secondary'],
            justify='center',
        )
        info_label.pack(pady=(4, 6))

        # --- 2. Manual mask input section ---
        input_frame = tk.LabelFrame(
            self.options_frame,
            text="Add Mask Region",
            font=self.fonts['section_header'],
            bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
        )
        input_frame.pack(fill='x', pady=(0, 15))

        # Entry for new mask (format: start:end)
        entry_frame = tk.Frame(input_frame, bg=self.colors['bg_panel'])
        entry_frame.pack(fill='x', padx=5, pady=5)

        tk.Label(
            entry_frame,
            text="Range (start:end):",
            bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
            font=self.fonts['body'],
        ).pack(side='left')

        mask_entry = tk.Entry(
            entry_frame,
            textvariable=self.mask_input_var,
            font=self.fonts['body'], width=20,
            bg=self.colors['bg_step'], fg=self.colors['text_primary'],
        )
        mask_entry.pack(side='left', padx=(8, 8))

        add_mask_btn = tk.Button(
            entry_frame,
            text="Add",
            bg=self.colors['success'], fg='white',
            font=self.fonts['button'], relief='raised', bd=2,
            command=self.add_mask_region,
        )
        add_mask_btn.pack(side='left')

        # Mask management buttons
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_panel'])
        button_frame.pack(fill='x', padx=5, pady=(0, 5))

        remove_btn = tk.Button(
            button_frame,
            text="Remove Selected",
            bg=self.colors['warning'], fg='white',
            font=self.fonts['button'], relief='raised', bd=2,
            command=self.remove_selected_mask,
        )
        remove_btn.pack(side='left', padx=(0, 5))

        clear_btn = tk.Button(
            button_frame,
            text="Clear All",
            bg=self.colors['warning'], fg='white',
            font=self.fonts['button'], relief='raised', bd=2,
            command=self.clear_all_masks,
        )
        clear_btn.pack(side='left', padx=(0, 5))

        # --- 3. Current masks display (moved to bottom) ---
        mask_list_frame = tk.LabelFrame(
            self.options_frame,
            text="Current Mask Regions",
            font=self.fonts['section_header'],
            bg=self.colors['bg_panel'],
            fg=self.colors['text_primary'],
        )
        mask_list_frame.pack(fill='x', pady=(0, 15))

        # Container for listbox + scrollbar
        mask_list_container = tk.Frame(mask_list_frame, bg=self.colors['bg_panel'])
        mask_list_container.pack(fill='both', expand=True, padx=5, pady=5)

        mask_scrollbar = tk.Scrollbar(mask_list_container, orient='vertical')
        mask_scrollbar.pack(side='right', fill='y')

        self.mask_listbox = tk.Listbox(
            mask_list_container,
            height=8,
            font=self.fonts['monospace'],
            bg=self.colors['bg_step'], fg=self.colors['text_primary'],
            yscrollcommand=mask_scrollbar.set,
        )
        self.mask_listbox.pack(side='left', fill='both', expand=True)

        mask_scrollbar.config(command=self.mask_listbox.yview)

        # Populate listbox AFTER it exists
        self.update_mask_listbox()

        # Separator and subsequent clipping section remain unchanged
        # Add separator
        separator = tk.Frame(self.options_frame, height=2, bg=self.colors['text_secondary'])
        separator.pack(fill='x', pady=(20, 15))
        
        # Clipping section (previously step 2, now integrated)
        clipping_frame = tk.LabelFrame(self.options_frame, text="Spectral Clipping",
                                      font=('Segoe UI', 13, 'bold'),
                                      bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
        clipping_frame.pack(fill='x', pady=(0, 10))
        
        # A-band clipping
        aband_check = tk.Checkbutton(clipping_frame,
                                    text="Remove telluric A-band (7575-7675Å)",
                                    variable=self.aband_var,
                                    font=('Segoe UI', 14, 'bold'),
                                    bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                                    selectcolor=self.colors['bg_step'],
                                    activebackground=self.colors['bg_panel'])
        aband_check.pack(anchor='w', padx=10, pady=5)
        
        # Sky lines clipping
        sky_frame = tk.Frame(clipping_frame, bg=self.colors['bg_panel'])
        sky_frame.pack(fill='x', padx=10, pady=5)
        
        sky_check = tk.Checkbutton(sky_frame,
                                  text="Remove sky lines",
                                  variable=self.sky_var,
                                  font=('Segoe UI', 14, 'bold'),
                                  bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                                  selectcolor=self.colors['bg_step'],
                                  activebackground=self.colors['bg_panel'])
        sky_check.pack(anchor='w')
        
        width_frame = tk.Frame(sky_frame, bg=self.colors['bg_panel'])
        width_frame.pack(fill='x', padx=(25, 0), pady=(5, 0))
        
        tk.Label(width_frame, text="Width:", 
                bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 12)).pack(side='left')
        
        sky_entry = tk.Entry(width_frame, textvariable=self.sky_width_var,
                            font=('Segoe UI', 12), width=8,
                            bg=self.colors['bg_step'], fg=self.colors['text_primary'])
        sky_entry.pack(side='left', padx=(8, 0))
        
        tk.Label(width_frame, text="Å",
                bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 12)).pack(side='left', padx=(3, 0))
    
    def add_mask_region(self):
        """Add a mask region from the input field"""
        try:
            mask_text = self.mask_input_var.get().strip()
            if ':' in mask_text:
                start, end = map(float, mask_text.split(':'))
                if start < end:
                    # Add to the text field
                    current_text = self.mask_entry_var.get().strip()
                    new_region = f"{start:.2f}-{end:.2f}"
                    if current_text:
                        new_text = f"{current_text}, {new_region}"
                    else:
                        new_text = new_region
                    self.mask_entry_var.set(new_text)
                    
                    # Update mask_regions list for calculations
                    self._sync_mask_regions_from_text()
                    
                    self.mask_input_var.set("")  # Clear input
                    self.update_mask_listbox()
                    self.update_preview()  # Update preview with new mask
                else:
                    messagebox.showerror("Invalid Range", "Start wavelength must be less than end wavelength.")
            else:
                messagebox.showerror("Invalid Format", "Please use format: start:end (e.g., 5500:5600)")
        except ValueError:
            messagebox.showerror("Invalid Values", "Please enter valid numerical wavelengths.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add mask: {str(e)}")
    
    def _sync_mask_regions_from_text(self):
        """Synchronize mask_regions list from the text field"""
        try:
            mask_text = self.mask_entry_var.get().strip()
            self.mask_regions = self._parse_mask_regions(mask_text)
        except Exception as e:
            self.mask_regions = []
    
    def remove_selected_mask(self):
        """Remove selected mask from the list"""
        try:
            selection = self.mask_listbox.curselection()
            if selection:
                index = selection[0]
                # Sync mask_regions from text first
                self._sync_mask_regions_from_text()
                
                if 0 <= index < len(self.mask_regions):
                    # Remove from mask_regions list
                    self.mask_regions.pop(index)
                    
                    # Update text field from mask_regions list
                    if self.mask_regions:
                        mask_text = ', '.join([f"{start:.2f}-{end:.2f}" for start, end in self.mask_regions])
                    else:
                        mask_text = ""
                    self.mask_entry_var.set(mask_text)
                    
                    self.update_mask_listbox()
                    self.update_preview()  # Update preview without mask
            else:
                messagebox.showwarning("No Selection", "Please select a mask region to remove.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove mask: {str(e)}")
    
    def clear_all_masks(self):
        """Clear all mask regions"""
        try:
            # Sync first to get current count
            self._sync_mask_regions_from_text()
            
            if self.mask_regions:
                result = messagebox.askyesno("Clear All Masks", 
                                           f"Are you sure you want to clear all {len(self.mask_regions)} mask regions?")
                if result:
                    self.mask_regions.clear()
                    self.mask_entry_var.set("")  # Clear text field
                    self.update_mask_listbox()
                    self.update_preview()  # Update preview without masks
            else:
                messagebox.showinfo("No Masks", "No mask regions to clear.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear masks: {str(e)}")
    
    def update_mask_listbox(self):
        """Update the mask regions listbox"""
        try:
            self.mask_listbox.delete(0, tk.END)
            
            # Parse current mask text and update mask_regions list
            self._sync_mask_regions_from_text()
            
            # Update listbox with parsed regions
            for start, end in self.mask_regions:
                self.mask_listbox.insert(tk.END, f"{start:.1f} - {end:.1f} Å")
                        
        except Exception as e:
            pass  # Silently handle errors
    
    def start_interactive_masking(self):
        """Start interactive masking mode"""
        try:
            # Check if we have a plot to work with
            if not hasattr(self, 'plot_manager') or not self.plot_manager:
                messagebox.showwarning("Plot Not Ready", "Please wait for the plot to load before using interactive masking.")
                return
                
            # Get the matplotlib axis from the plot manager
            ax = None
            if hasattr(self.plot_manager, 'ax1') and self.plot_manager.ax1 is not None:
                ax = self.plot_manager.ax1  # Use the top plot for selection
            elif hasattr(self.plot_manager, 'ax2') and self.plot_manager.ax2 is not None:
                ax = self.plot_manager.ax2  # Fallback to bottom plot
            
            if ax is None:
                messagebox.showwarning("Plot Not Ready", "Plot is not ready for interactive masking.")
                return
            
            # Import matplotlib widgets
            from matplotlib.widgets import SpanSelector
            
            # Start masking mode
            self.masking_active = True
            
            def onselect(xmin, xmax):
                """Callback for when user selects a region"""
                try:
                    if xmin != xmax:  # Valid selection
                        # Ensure correct order
                        start, end = min(xmin, xmax), max(xmin, xmax)
                        
                        # Get current mask text
                        current_text = self.mask_entry_var.get().strip()
                        
                        # Add new mask region
                        new_region = f"{start:.2f}-{end:.2f}"
                        if current_text:
                            new_text = f"{current_text}, {new_region}"
                        else:
                            new_text = new_region
                        
                        self.mask_entry_var.set(new_text)
                        
                        # Sync mask_regions from text
                        self._sync_mask_regions_from_text()
                        
                        # Update the listbox
                        self.update_mask_listbox()
                        
                        # Update preview
                        self.update_preview()
                        
                except Exception as e:
                    pass  # Silently handle errors
            
            # Create span selector with compatibility for different matplotlib versions
            try:
                # Try newer matplotlib API first
                self.span_selector = SpanSelector(
                    ax, 
                    onselect,
                    direction='horizontal',
                    useblit=True,
                    props=dict(alpha=0.3, facecolor='red', edgecolor='darkred'),
                    interactive=True,
                    minspan=1.0  # Minimum span in wavelength units
                )
            except (TypeError, AttributeError):
                # Fallback for older matplotlib versions
                try:
                    self.span_selector = SpanSelector(
                        ax, 
                        onselect,
                        'horizontal',
                        useblit=True,
                        rectprops=dict(alpha=0.3, facecolor='red'),
                        minspan=1.0
                    )
                except (TypeError, AttributeError):
                    # Most basic version for very old matplotlib
                    self.span_selector = SpanSelector(ax, onselect, 'horizontal')
            
            # Update the interactive button to show "Stop Interactive"
            self._update_interactive_button_state(True)
            
            # Suppress the former pop-up instructions window – users now see inline guidance.
            
        except ImportError:
            messagebox.showerror("Feature Unavailable", 
                               "Interactive masking requires matplotlib widgets.\n"
                               "Please ensure matplotlib is properly installed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start interactive masking: {str(e)}")
    
    def stop_interactive_masking(self):
        """Stop interactive masking mode"""
        try:
            if self.span_selector:
                self.span_selector.set_active(False)
                self.span_selector = None
        except Exception as e:
            pass  # Silently handle errors
            
        try:
            self.masking_active = False
            self._update_interactive_button_state(False)
        except Exception as e:
            pass  # Silently handle errors
    
    def _update_interactive_button_state(self, masking_active):
        """Update interactive masking button state"""
        try:
            if hasattr(self, 'interactive_mask_btn'):
                if masking_active:
                    self.interactive_mask_btn.configure(
                        text="🔴 Stop Interactive", 
                        command=self.stop_interactive_masking
                    )
                else:
                    self.interactive_mask_btn.configure(
                        text="🎯 Interactive Select", 
                        command=self.start_interactive_masking
                    )
        except Exception as e:
            pass  # Silently handle errors
    
    def create_filtering_options(self):
        """Create options for Savitzky-Golay filtering step"""
        # Filter type selection
        filter_frame = tk.LabelFrame(self.options_frame, text="Savitzky-Golay Filter Type",
                                    font=self.fonts['section_header'],
                                    bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
        filter_frame.pack(fill='x', pady=(0, 15))
        
        # No filtering
        tk.Radiobutton(filter_frame, text="No filtering",
                      variable=self.filter_type_var, value="none",
                      font=self.fonts['body'],
                      bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['bg_step'],
                      activebackground=self.colors['bg_panel']).pack(anchor='w', padx=15, pady=5)
        
        # Fixed width
        fixed_frame = tk.Frame(filter_frame, bg=self.colors['bg_panel'])
        fixed_frame.pack(fill='x', padx=15, pady=5)
        
        tk.Radiobutton(fixed_frame, text="Fixed window:",
                      variable=self.filter_type_var, value="fixed",
                      font=self.fonts['body'],
                      bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['bg_step'],
                      activebackground=self.colors['bg_panel']).pack(side='left')
        
        tk.Entry(fixed_frame, textvariable=self.fixed_savgol_var,
                font=self.fonts['body'], width=8,
                bg=self.colors['bg_step'], fg=self.colors['text_primary']).pack(side='left', padx=(8, 3))
        
        tk.Label(fixed_frame, text="pixels, order:",
                bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(side='left')
        
        self.polyorder_entry_fixed = tk.Entry(fixed_frame, textvariable=self.polyorder_var,
                font=self.fonts['body'], width=5,
                bg=self.colors['bg_step'], fg=self.colors['text_primary'])
        self.polyorder_entry_fixed.pack(side='left', padx=(4, 0))

        # Add helpful info
        help_frame = tk.Frame(filter_frame, bg=self.colors['bg_panel'])
        help_frame.pack(fill='x', padx=15, pady=(10, 8))
        
        help_text = tk.Label(help_frame,
                            text="💡 Savitzky-Golay smoothing preserves peak shapes better than median filtering.\n"
                                 "   Higher polynomial orders provide better fitting but may amplify noise.",
                            font=self.fonts['small'],
                            bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                            justify='left',
                            wraplength=300)  # Reduced to 300 for better wrapping
        help_text.pack(anchor='w')
    
    def create_rebinning_with_scaling_options(self):
        """Create options for log rebinning with flux scaling (required step)"""
        info_frame = tk.Frame(self.options_frame, bg=self.colors['accent'], relief='flat', bd=1)
        info_frame.pack(fill='x', pady=15)
        
        info_label = tk.Label(info_frame,
                             text="⚠️ Required Step\nConverts to logarithmic wavelength spacing\nand normalizes flux for template matching",
                             font=self.fonts['body_bold'],
                             bg=self.colors['accent'], fg='white',
                             justify='center')
        info_label.pack(pady=20)
        
        # Add description of what this step does
        description_frame = tk.Frame(self.options_frame, bg=self.colors['bg_panel'])
        description_frame.pack(fill='x', pady=15)
        
        description = tk.Label(description_frame,
                             text="This step performs two critical operations:\n"
                                  "1. Converts wavelength to logarithmic spacing (required for SNID)\n"
                                  "2. Normalizes flux to mean = 1.0 for consistent template matching",
                             font=self.fonts['body'],
                             bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                             justify='left')
        description.pack(anchor='w', pady=(8, 0))
    
    def create_continuum_options(self):
        """Create options for continuum fitting with integrated interactive editing"""
        # Continuum fitting method selection
        method_frame = tk.LabelFrame(self.options_frame, text="Continuum Fitting Method",
                                    font=self.fonts['section_header'],
                                    bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
        method_frame.pack(fill='x', pady=(0, 20))
        
        # Spline method (DEFAULT - appears first)
        spline_frame = tk.Frame(method_frame, bg=self.colors['bg_panel'])
        spline_frame.pack(fill='x', padx=15, pady=6)
        
        tk.Radiobutton(spline_frame, text="Spline, knots:",
                      variable=self.continuum_type_var, value="spline",
                      font=self.fonts['body'],
                      bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['bg_step'],
                      activebackground=self.colors['bg_panel']).pack(side='left')
        
        tk.Entry(spline_frame, textvariable=self.spline_knots_var,
                font=self.fonts['body'], width=10,
                bg=self.colors['bg_step'], fg=self.colors['text_primary']).pack(side='left', padx=(8, 0))
        
        # Gaussian filter
        gauss_frame = tk.Frame(method_frame, bg=self.colors['bg_panel'])
        gauss_frame.pack(fill='x', padx=15, pady=6)
        
        tk.Radiobutton(gauss_frame, text="Gaussian filter, σ:",
                      variable=self.continuum_type_var, value="gaussian",
                      font=self.fonts['body'],
                      bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['bg_step'],
                      activebackground=self.colors['bg_panel']).pack(side='left')
        
        tk.Entry(gauss_frame, textvariable=self.gauss_sigma_var,
                font=self.fonts['body'], width=10,
                bg=self.colors['bg_step'], fg=self.colors['text_primary']).pack(side='left', padx=(8, 3))
        
        tk.Label(gauss_frame, text="log-λ bins",
                bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(side='left')
        
        # Add helpful info about automatic calculation
        gauss_help_frame = tk.Frame(method_frame, bg=self.colors['bg_panel'])
        gauss_help_frame.pack(fill='x', padx=30, pady=(0, 6))
        
        help_text = tk.Label(gauss_help_frame,
                            text="💡 Use 'auto' for automatic sigma calculation based on spectrum characteristics.",
                            font=self.fonts['small'],
                            bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                            justify='left',
                            wraplength=300)  # Reduced to 300 for better wrapping
        help_text.pack(anchor='w')
        
        # Interactive continuum editing section
        if self.interactive_widget:
            interactive_frame = tk.LabelFrame(self.options_frame, text="Interactive Continuum Editing",
                                            font=self.fonts['section_header'],
                                            bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
            interactive_frame.pack(fill='x', pady=(0, 15))
            
            # Add message about edge handling
            edge_message_frame = tk.Frame(interactive_frame, bg=self.colors['bg_panel'])
            edge_message_frame.pack(fill='x', padx=15, pady=(10, 5))
            
            edge_message = tk.Label(edge_message_frame,
                                   text="💡 Note: Don't worry about the spectrum edges during continuum editing.\n"
                                        "   They will be properly handled in the next step (apodization).",
                                   font=self.fonts['small'],
                                   bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                                   justify='left',
                                   wraplength=280)  # Further reduced to 280 to prevent any cutoff
            edge_message.pack(anchor='w', padx=(5, 0))  # Added left padding to ensure no cutoff
            
            # Add interactive controls
            controls = self.interactive_widget.create_interactive_controls(interactive_frame)
            controls.pack(fill='x', padx=15, pady=15)
            
            # Initialize continuum points for the first time entering this step
            self._initialize_continuum_points_if_needed()
    
    def create_apodization_options(self):
        """Create options for apodization step"""
        apod_frame = tk.Frame(self.options_frame, bg=self.colors['bg_panel'])
        apod_frame.pack(fill='x', pady=8)
        
        tk.Checkbutton(apod_frame,
                      text="Apply apodization (taper spectrum ends)",
                      variable=self.apodize_var,
                      font=self.fonts['body_bold'],
                      bg=self.colors['bg_panel'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['bg_step'],
                      activebackground=self.colors['bg_panel']).pack(anchor='w')
        
        # Percentage control
        percent_frame = tk.Frame(self.options_frame, bg=self.colors['bg_panel'])
        percent_frame.pack(fill='x', pady=8, padx=(25, 0))
        
        tk.Label(percent_frame, text="Taper percentage:",
                bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(side='left')
        
        tk.Entry(percent_frame, textvariable=self.apod_percent_var,
                font=self.fonts['body'], width=10,
                bg=self.colors['bg_step'], fg=self.colors['text_primary']).pack(side='left', padx=(8, 3))
        
        tk.Label(percent_frame, text="%",
                bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(side='left')
        
        description = tk.Label(self.options_frame,
                              text="Smoothly tapers the spectrum edges to reduce artifacts\nin Fourier-based operations",
                              font=self.fonts['body'],
                              bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                              justify='left')
        description.pack(anchor='w', pady=(12, 0))
    
    def create_final_review_options(self):
        """Create options for final review step"""
        # Show completion message and summary
        completion_frame = tk.Frame(self.options_frame, bg=self.colors['success'], relief='flat', bd=1)
        completion_frame.pack(fill='x', pady=15)
        
        completion_label = tk.Label(completion_frame,
                                   text="✅ Preprocessing Complete!\nReady to Finish",
                                   font=self.fonts['title'],
                                   bg=self.colors['success'], fg='white',
                                   justify='center')
        completion_label.pack(pady=20)
        
        # Show summary of applied steps
        if self.preview_calc:
            summary = self.preview_calc.get_processing_summary()
            
            summary_frame = tk.LabelFrame(self.options_frame, text="Processing Summary",
                                         font=self.fonts['section_header'],
                                         bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
            summary_frame.pack(fill='x', pady=(0, 15))
            
            summary_text = f"Applied Steps: {summary['applied_steps']}\n"
            summary_text += f"Final Points: {summary['current_points']}\n"
            summary_text += f"Wavelength Range: {summary['wave_range'][0]:.1f} - {summary['wave_range'][1]:.1f} Å"
            
            summary_label = tk.Label(summary_frame,
                                    text=summary_text,
                                    font=self.fonts['monospace'],
                                    bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                                    justify='left')
            summary_label.pack(anchor='w', padx=15, pady=10)
        
        # Instructions
        instruction_label = tk.Label(self.options_frame,
                                    text="Review the final spectrum above.\nClick 'Finish' to complete preprocessing and return to main interface.",
                                    font=self.fonts['body'],
                                    bg=self.colors['bg_panel'], fg=self.colors['text_secondary'],
                                    justify='center')
        instruction_label.pack(pady=(15, 0))
    
    def update_preview(self, *args):
        """Update the preview plots using modular components"""
        # Prevent rapid multiple updates during initialization
        if self._initializing or not self._canvas_ready:
            return
            
        if not self.plot_manager or not self.preview_calc:
            return
        
        try:
            # Check if we're in interactive continuum mode
            if (self.current_step == 3 and self.interactive_widget and 
                self.interactive_widget.is_interactive_mode()):
                self._update_interactive_preview()
            else:
                self._update_standard_preview()
                
        except Exception as e:
            # Silently handle preview update errors
            pass
    
    def _update_standard_preview(self):
        """Update standard before/after preview"""
        # Get current state
        before_wave, before_flux = self.preview_calc.get_current_state()
        
        # Calculate preview for current step
        preview_wave, preview_flux = self.calculate_current_preview()
        
        # Sync mask regions and determine if we should show mask visualization
        self._sync_mask_regions_from_text()
        
        # Decide whether to show mask regions based on current step and application status
        mask_regions_to_show = None
        if self.current_step == 0:  # Step 1: Wavelength Masking
            # Only show masks for the FIRST step, and only if they haven't been applied yet
            if not self._is_step_applied(0) and self.mask_regions:
                # Show the current mask regions for visualization
                mask_regions_to_show = self.mask_regions
        
        # FIXED: Only show continuum points on step 3 (continuum fitting) AND continuum hasn't been applied yet
        # Once continuum is applied OR we move to later steps, use standard preview (no continuum overlay)
        if self.current_step == 3 and self.interactive_widget and not self._is_step_applied(3):
            # Update continuum points based on current method and parameters
            self._update_continuum_points_for_current_settings()
            
            # Get the continuum points and show interactive preview even if not in interactive mode
            continuum_points = self.interactive_widget.get_continuum_points()
            
            # Use interactive preview display to show continuum points
            interactive_mode = self.interactive_widget.is_interactive_mode() if self.interactive_widget else False
            self.plot_manager.update_interactive_preview(
                before_wave, before_flux, continuum_points, preview_wave, preview_flux, interactive_mode
            )
        else:
            # Update plots with or without mask visualization
            # This will be used for:
            # 1. All steps except step 3 (masking, filtering, rebinning, apodization)
            # 2. Step 3 AFTER continuum has been applied
            self.plot_manager.update_standard_preview(
                before_wave, before_flux, preview_wave, preview_flux, mask_regions=mask_regions_to_show
            )
    
    def _update_interactive_preview(self):
        """Update preview with interactive continuum overlay"""
        # Preserve current zoom limits on the top plot
        try:
            ax1 = self.plot_manager.get_top_axis()
            prev_xlim = ax1.get_xlim()
            prev_ylim = ax1.get_ylim()
        except Exception:
            prev_xlim = prev_ylim = None

        # Get current spectrum state
        current_wave, current_flux = self.preview_calc.get_current_state()

        # Get continuum points from interactive widget
        continuum_points = self.interactive_widget.get_continuum_points()

        # Get flattened preview
        preview_wave, preview_flux = self.interactive_widget.get_preview_data()

        # Update plots with interactive overlay
        interactive_mode = self.interactive_widget.is_interactive_mode() if self.interactive_widget else False
        self.plot_manager.update_interactive_preview(
            current_wave, current_flux, continuum_points, preview_wave, preview_flux, interactive_mode
        )

        # Restore previous zoom if user had zoomed in
        if prev_xlim and prev_ylim:
            try:
                ax1.set_xlim(prev_xlim)
                ax1.set_ylim(prev_ylim)
                self.plot_manager.canvas.draw_idle()
            except Exception:
                pass
    
    def calculate_current_preview(self):
        """Calculate preview for current step using PreviewCalculator"""
        if self.current_step == 0:  # Combined Masking & Clipping
            # Start with current state
            preview_wave, preview_flux = self.preview_calc.get_current_state()
            
            # Sync mask_regions from text before using them
            self._sync_mask_regions_from_text()
            
            # Apply masking first if any masks exist
            if self.mask_regions:
                preview_wave, preview_flux = self.preview_calc.preview_step("masking", mask_regions=self.mask_regions)
                
            # Then apply clipping operations on the masked result
            # FIXED: Apply both A-band and sky line clipping if both are selected
            if self.aband_var.get():
                # Create a temporary preview calculator for chained operations
                temp_calc = type(self.preview_calc)(preview_wave, preview_flux)
                preview_wave, preview_flux = temp_calc.preview_step("clipping", clip_type="aband")
            
            if self.sky_var.get():  # Changed from elif to if - both can be applied
                try:
                    width = float(self.sky_width_var.get())
                    temp_calc = type(self.preview_calc)(preview_wave, preview_flux)
                    preview_wave, preview_flux = temp_calc.preview_step("clipping", clip_type="sky", width=width)
                except ValueError:
                    pass
                    
            return preview_wave, preview_flux
            
        elif self.current_step == 1:  # Savitzky-Golay filtering (was step 2)
            filter_type = self.filter_type_var.get()
            if filter_type == "none":
                return self.preview_calc.get_current_state()
            
            try:
                polyorder = int(self.polyorder_var.get())
            except ValueError:
                polyorder = 3  # Default
                
            if filter_type == "fixed":
                try:
                    value = float(self.fixed_savgol_var.get())
                    return self.preview_calc.preview_step("savgol_filter", 
                                                        filter_type=filter_type, value=value, polyorder=polyorder)
                except ValueError:
                    return self.preview_calc.get_current_state()
            elif filter_type == "wavelength":
                try:
                    value = float(self.wave_savgol_var.get())
                    return self.preview_calc.preview_step("savgol_filter", 
                                                        filter_type=filter_type, value=value, polyorder=polyorder)
                except ValueError:
                    return self.preview_calc.get_current_state()
            
            return self.preview_calc.get_current_state()
            
        elif self.current_step == 2:  # Log rebinning with flux scaling
            return self.preview_calc.preview_step("log_rebin_with_scaling")
            
        elif self.current_step == 3:  # Continuum fitting
            method = self.continuum_type_var.get()
            if method == "gaussian":
                try:
                    sigma_str = self.gauss_sigma_var.get()
                    if sigma_str.lower() == "auto":
                        # Use automatic sigma calculation (None will trigger auto calculation)
                        return self.preview_calc.preview_step("continuum_fit", 
                                                            method="gaussian", sigma=None)
                    else:
                        sigma = float(sigma_str)
                        return self.preview_calc.preview_step("continuum_fit", 
                                                            method="gaussian", sigma=sigma)
                except ValueError:
                    pass
            elif method == "spline":
                try:
                    knotnum = int(self.spline_knots_var.get())
                    return self.preview_calc.preview_step("continuum_fit", 
                                                        method="spline", knotnum=knotnum)
                except ValueError:
                    pass
        
        elif self.current_step == 4:  # Apodization
            if self.apodize_var.get():
                try:
                    percent_str = self.apod_percent_var.get().strip()
                    if percent_str:  # Only try if not empty
                        percent = float(percent_str)
                        if 0 <= percent <= 50:  # Reasonable range
                            return self.preview_calc.preview_step("apodization", percent=percent)
                except ValueError:
                    pass  # Silently ignore invalid values during preview
                    
        # Fallback
        return self.preview_calc.get_current_state()

    def _parse_mask_regions(self, mask_text):
        """Parse mask text into list of (start, end) tuples"""
        try:
            regions = []
            if not mask_text.strip():
                return regions
            
            # Split by commas and parse each region
            parts = mask_text.split(',')
            for part in parts:
                part = part.strip()
                if not part:  # Skip empty parts
                    continue
                    
                # Look for separators: first try ':', then '-' 
                # But be careful with negative numbers (e.g., "-100.5-200.3")
                if ':' in part:
                    # Format: start:end
                    try:
                        start, end = map(float, part.split(':', 1))  # Split only on first ':'
                        if start < end:
                            regions.append((start, end))
                    except (ValueError, IndexError):
                        continue
                elif '-' in part:
                    # Format: start-end (but handle negative numbers)
                    # Strategy: find the last '-' that's not at the start and not following 'e' or 'E'
                    dash_pos = -1
                    for i in range(len(part)-1, 0, -1):  # Search from right to left, skip position 0
                        if part[i] == '-':
                            # Check if this dash is part of scientific notation
                            if i > 0 and part[i-1].lower() in 'e':
                                continue
                            dash_pos = i
                            break
                    
                    if dash_pos > 0:  # Found a valid separator dash
                        try:
                            start = float(part[:dash_pos])
                            end = float(part[dash_pos+1:])
                            if start < end:
                                regions.append((start, end))
                        except (ValueError, IndexError):
                            continue
                else:
                    continue  # Skip invalid formats
            
            return regions
        except:
            return []

    def _initialize_continuum_points_if_needed(self):
        """Initialize continuum points when first entering step 3"""
        if self.current_step == 3 and self.interactive_widget:
            # Check if we already have continuum points
            current_points = self.interactive_widget.get_continuum_points()
            if not current_points:
                # Initialize with current settings
                self._update_continuum_points_for_current_settings()
    
    def _update_continuum_points_for_current_settings(self):
        """Update continuum points based on current method and parameters"""
        if self.current_step == 3 and self.interactive_widget:
            # --- NEW: guard against overwriting manual edits ---
            if hasattr(self.interactive_widget, 'has_manual_changes') and \
               self.interactive_widget.has_manual_changes():
                return
            
            method = self.continuum_type_var.get()
            
            # Set the current method in the interactive widget
            self.interactive_widget.set_current_method(method)
            
            if method == "gaussian":
                try:
                    sigma_str = self.gauss_sigma_var.get()
                    if sigma_str.lower() == "auto":
                        # Use automatic sigma calculation
                        _LOGGER.debug("Automatic sigma calculation for Gaussian continuum")
                        self.interactive_widget.update_continuum_from_fit(None)
                    else:
                        sigma = float(sigma_str)
                        _LOGGER.debug(f"Gaussian continuum sigma={sigma}")
                        self.interactive_widget.update_continuum_from_fit(sigma)
                except ValueError:
                    # Use default auto calculation on invalid input
                    self.interactive_widget.update_continuum_from_fit(None)
            elif method == "spline":
                try:
                    knotnum = int(self.spline_knots_var.get())
                    _LOGGER.debug(f"Spline continuum with {knotnum} knots")
                    self.interactive_widget.update_continuum_from_fit(knotnum)
                except ValueError:
                    # Use default knot number on invalid input
                    self.interactive_widget.update_continuum_from_fit(13)

    def _restore_ui_state_for_step(self, step_index):
        """Restore UI state when reverting to a specific step"""
        try:
            # Reset step-specific UI elements to their default/unapplied state
            if step_index == 0:  # Masking & Clipping
                # Keep mask regions as they are (user might want to modify them)
                # Reset clipping checkboxes to unchecked state
                self.aband_var.set(False)
                self.sky_var.set(False)
                
            elif step_index == 1:  # Savitzky-Golay filtering
                # Reset filter type to "none"
                self.filter_type_var.set("none")
                self.polyorder_var.set("3")
                
            elif step_index == 2:  # Log rebinning with scaling
                # No UI state to reset for this step
                pass
                
            elif step_index == 3:  # Continuum fitting
                # Reset continuum method to default
                self.continuum_type_var.set("spline")
                self.gauss_sigma_var.set("auto")
                self.spline_knots_var.set("13")
                # Ensure interactive mode is disabled
                if hasattr(self, 'interactive_widget') and self.interactive_widget:
                    if self.interactive_widget.is_interactive_mode():
                        self.interactive_widget.disable_interactive_mode()
                
            elif step_index == 4:  # Apodization
                # Reset apodization checkbox and percentage
                self.apodize_var.set(False)
                self.apod_percent_var.set("10.0")
                
        except Exception as e:
            # Silently handle any errors in UI state restoration
            pass

    def _is_step_applied(self, step_index):
        """Check if a specific step has been applied"""
        if not self.preview_calc:
            return False
        return any(step.get('step_index') == step_index for step in self.preview_calc.applied_steps)

    def update_button_states(self):
        """Update navigation button states"""
        # Revert button - disabled for first step or if no steps have been applied
        if self.current_step == 0 or not self.preview_calc or not self.preview_calc.applied_steps:
            self.revert_btn.config(state='disabled')
        else:
            self.revert_btn.config(state='normal')
        
        # Handle final review step (step 5) specially
        if self.current_step == 5:  # Final Review step
            # In final review, hide Apply button and show Finish button
            self.apply_btn.config(text="Apply", state='disabled', 
                                bg=self.colors['disabled'], fg=self.colors['text_secondary'])
            self.finish_btn.config(state='normal')
        elif self.current_step == 4:  # Apodization step
            # Check if apodization has been applied
            apod_already_applied = self._is_step_applied(4)
            
            if apod_already_applied:
                # Apodization can only be applied once - disable the button
                self.apply_btn.config(text="Apodization Applied", state='disabled',
                                    bg=self.colors['disabled'], fg=self.colors['text_secondary'])
                self.finish_btn.config(state='disabled')
            else:
                # Before apodization is applied, show enabled Apply button
                self.apply_btn.config(text="Apply Step", state='normal', 
                                    bg=self.colors['success'], fg='white')
                self.finish_btn.config(state='disabled')
        else:
            # For all other steps, use regular Apply Step button
            self.apply_btn.config(text="Apply Step", state='normal',
                                bg=self.colors['success'], fg='white')
            # Hide finish button for non-final steps
            self.finish_btn.config(state='disabled')
    
    def revert_to_previous_step(self):
        """Revert processing by removing only the most recent applied step"""
        if not self.preview_calc or not self.preview_calc.applied_steps:
            return
        
        try:
            # Find the most recent step by step_index
            last_step_index = max(step.get('step_index', -1) for step in self.preview_calc.applied_steps)
            
            # Remove only steps with the highest step_index (most recent step)
            self.preview_calc.applied_steps = [
                step for step in self.preview_calc.applied_steps 
                if step.get('step_index', -1) < last_step_index
            ]
            
            # Reset the spectrum to the original state
            self.preview_calc.reset()
            
            # Reapply all remaining steps in order
            for step in self.preview_calc.applied_steps:
                step_type = step['type']
                kwargs = step.get('kwargs', {})
                step_index = step.get('step_index')
                
                if step_type == 'masking':
                    self.preview_calc.apply_step('masking', step_index=step_index, **kwargs)
                elif step_type == 'clipping':
                    self.preview_calc.apply_step('clipping', step_index=step_index, **kwargs)
                elif step_type == 'savgol_filter':
                    self.preview_calc.apply_step('savgol_filter', step_index=step_index, **kwargs)
                elif step_type == 'log_rebin_with_scaling':
                    self.preview_calc.apply_step('log_rebin_with_scaling', step_index=step_index, **kwargs)
                elif step_type == 'continuum_fit':
                    self.preview_calc.apply_step('continuum_fit', step_index=step_index, **kwargs)
                elif step_type == 'interactive_continuum':
                    self.preview_calc.apply_step('interactive_continuum', step_index=step_index, **kwargs)
                elif step_type == 'apodization':
                    self.preview_calc.apply_step('apodization', step_index=step_index, **kwargs)
            
            # Set current step to the beginning of the previous step (not the reverted step)
            self.current_step = max(0, last_step_index - 1)
            
            # Reset processing state if needed
            if self.current_step < self.total_steps - 1:
                self.processing_complete = False
            
            # Stop interactive masking if active
            if hasattr(self, 'masking_active') and self.masking_active:
                self.stop_interactive_masking()
            
            # Handle interactive continuum state restoration
            if self.current_step == 3 and self.interactive_widget:
                # If we're reverting from continuum step, check if we had interactive continuum applied
                had_interactive_continuum = any(
                    step.get('type') == 'interactive_continuum' 
                    for step in self.preview_calc.applied_steps
                )
                
                if had_interactive_continuum:
                    # Find the most recent interactive continuum step to restore continuum array
                    for step in reversed(self.preview_calc.applied_steps):
                        if step.get('type') == 'interactive_continuum':
                            manual_continuum = step.get('kwargs', {}).get('manual_continuum', [])
                            wave_grid = step.get('kwargs', {}).get('wave_grid', [])
                            if len(manual_continuum) > 0 and len(wave_grid) > 0:
                                self.interactive_widget.set_manual_continuum(wave_grid, manual_continuum)
                                # Don't automatically enable interactive mode - let user decide
                            break
                else:
                    # No interactive continuum in remaining steps, reset to fitted continuum
                    self._initialize_continuum_points_if_needed()
                
                # Ensure interactive mode is disabled after revert
                if self.interactive_widget.is_interactive_mode():
                    self.interactive_widget.disable_interactive_mode()
            
            # Restore UI state for the current step
            self._restore_ui_state_for_step(self.current_step)
            
            # Update the UI
            self.update_step_display()
            self.update_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to revert to previous step: {str(e)}")
    
    def finish_preprocessing(self):
        """Complete preprocessing and apply all changes"""
        try:
            # Apply any remaining steps
            if self.preview_calc:
                # Get final processed spectrum
                final_wave, final_flux = self.preview_calc.get_current_state()
                
                # Update the actual preprocessor with final results
                self.preprocessor.current_wave = final_wave
                self.preprocessor.current_flux = final_flux
                
                # CRITICAL: Pass processed spectrum back to GUI
                # Get the parent GUI from the preprocessor
                if hasattr(self.preprocessor, 'gui') and self.preprocessor.gui:
                    gui = self.preprocessor.gui
                    
                    # Create processed_spectrum dict compatible with SNID analysis
                    from snid_sage.snid.snid import init_wavelength_grid, get_grid_params
                    # log_rebin is no longer needed here – spectrum has been rebinned in Step 3
                    from snid_sage.snid.preprocessing import fit_continuum, clip_aband, clip_sky_lines
                    
                    # Fetch grid parameters for metadata (length, DWLOG, etc.)
                    NW_grid, W0, W1, DWLOG_grid = get_grid_params()
                    
                    # Spectrum is already on the canonical log-λ grid after Step 3
                    log_wave_grid, log_flux = final_wave, final_flux
                    
                    # Do NOT filter the data here! 
                    # The SNID analysis expects full NW_grid arrays with proper left_edge/right_edge indices
                    # Filtering should only happen during plotting, not during data storage
                    
                    # CRITICAL: Calculate left_edge/right_edge using the SAME method as standard SNID preprocessing
                    # Standard SNID uses: nonzero_mask = (log_flux > 0)
                    # But Advanced Preprocessing creates continuum-removed flux which can be negative!
                    # We need to use the reconstructed flux (log_flux + 1.0) * continuum for finding edges
                    
                    # First, get the continuum (we'll calculate it below)
                    # We need to calculate continuum first to reconstruct the proper flux for edge detection
                    
                    # Simplified approach: Use the continuum from preview_calc if available
                    continuum = None
                    
                    # Check if continuum fitting was applied and try to get continuum from preview_calc
                    continuum_applied = any(step['type'] in ['continuum_fit', 'interactive_continuum'] 
                                          for step in self.preview_calc.applied_steps)
                    
                    if continuum_applied and hasattr(self.preview_calc, 'get_continuum_from_fit'):
                        try:
                            # Try to get continuum from the preview calculator
                            _, continuum = self.preview_calc.get_continuum_from_fit()
                            if continuum is not None and len(continuum) != len(log_flux):
                                continuum = None  # Reset if size mismatch
                        except:
                            continuum = None
                    
                    # If no continuum or size mismatch, create a unity continuum
                    if continuum is None:
                        continuum = np.ones_like(log_flux)
                    
                    # For edge detection, we need the "raw" flux (not continuum-removed)
                    # If continuum was removed, reconstruct it; otherwise use the current flux
                    if continuum_applied:
                        # Reconstruct flux: (flat + 1) * continuum
                        reconstructed_flux = (log_flux + 1.0) * continuum
                    else:
                        # No continuum fitting applied, use the current flux as is
                        reconstructed_flux = log_flux.copy()
                    
                    # snid_sage.snid.py line ~260)
                    nonzero_mask = (reconstructed_flux > 0)
                    if np.any(nonzero_mask):
                        left_edge_filtered = np.argmax(nonzero_mask)
                        right_edge_filtered = len(reconstructed_flux) - 1 - np.argmax(nonzero_mask[::-1])
                    else:
                        left_edge_filtered = 0
                        right_edge_filtered = len(log_flux) - 1
                    
                    # Store the FULL arrays (do not filter!) but use proper left_edge/right_edge
                    # This is critical for SNID template correlation to work correctly
                
                # Continuum was already calculated above for edge detection
                # No need to recalculate - just use the continuum variable
                
                # Create processed_spectrum dict with required keys INCLUDING DWLOG
                # CRITICAL: Store FULL arrays for SNID analysis compatibility
                processed_spectrum = {
                    'log_wave': log_wave_grid,  # Full NW_grid array
                    'log_flux': reconstructed_flux,  # FIXED: Full reconstructed flux array (used by SNID analysis and Flux view)
                    'flat_flux': log_flux,  # FIXED: Full flattened array (continuum-removed, used by Flat view)
                    'tapered_flux': log_flux.copy(),  # Full array for SNID analysis (will be apodized later if needed)
                    'continuum': continuum,  # Full continuum array
                    'left_edge': left_edge_filtered,  # Proper index into full arrays
                    'right_edge': right_edge_filtered,  # Proper index into full arrays
                    'display_flux': reconstructed_flux,  # Full array for Flux view (filtering happens in plotting)
                    'display_flat': log_flux,  # Full array for Flat view (filtering happens in plotting)
                    'original_wave': final_wave,  # Keep original grid for reference
                    'original_flux': final_flux,
                    'input_spectrum': {'wave': final_wave, 'flux': final_flux},  # Store original input
                    'advanced_preprocessing': True,  # MARKER: This came from Advanced Preprocessing
                    'preprocessing_type': 'advanced',  # Additional marker for clarity
                    'grid_params': {
                        'NW': len(log_flux),  # This should be NW_grid (typically 8192)
                        'MINW': W0, 
                        'MAXW': W1,
                        'DWLOG': DWLOG_grid  # CRITICAL: This was missing!
                    }
                }
                
                # Set the processed spectrum in the GUI
                gui.processed_spectrum = processed_spectrum
                
                # CRITICAL: Clear original spectrum data after advanced preprocessing
                # According to spec: "Original flux spectrum is not available after preprocessing"
                if hasattr(gui, 'original_wave'):
                    gui.original_wave = None
                if hasattr(gui, 'original_flux'):
                    gui.original_flux = None
                
                _LOGGER.info("✅ Original spectrum data cleared after advanced preprocessing - only processed spectrum available now")
                
                # Set mask tracking to prevent analysis controller from overwriting  
                # Advanced preprocessing with standard SNID preprocessing
                current_masks = gui._parse_wavelength_masks(gui.params.get('wavelength_masks', ''))
                gui._last_preprocessing_masks = current_masks
                
                # Update GUI button states to enable SNID analysis
                if hasattr(gui, 'update_button_states'):
                    gui.update_button_states()
                
                # CRITICAL: Switch to Flat view to show the continuum-removed spectrum
                if hasattr(gui, 'view_style') and gui.view_style:
                    gui.view_style.set("Flat")
                    # Trigger the view change through the plot controller
                    if hasattr(gui, 'plot_controller') and gui.plot_controller:
                        gui.plot_controller._on_view_style_change()
                
                # Update status message
                if hasattr(gui, 'update_header_status'):
                    gui.update_header_status("✅ Advanced preprocessing complete - ready for analysis")
                
                # Force GUI refresh
                if hasattr(gui, 'master'):
                    gui.master.update_idletasks()
                
                # Set preprocess status label (if present) to show completion tick.
                if hasattr(gui, 'preprocess_status_label'):
                    gui.preprocess_status_label.configure(
                        text="✅ Preprocessed",
                        fg=gui.theme_manager.get_color('success') if hasattr(gui, 'theme_manager') else 'green',
                    )
                
                # No modal summary popup – inline status and label are sufficient.
            
            # CRITICAL: Set view to Flat mode after preprocessing since flattened spectrum is usually shown
            if hasattr(self.parent, 'view_style') and self.parent.view_style:
                self.parent.view_style.set("Flat")
                _LOGGER.info("🔄 View mode set to Flat after advanced preprocessing completion")
                
                # Update segmented control buttons
                if hasattr(self.parent, '_update_segmented_control_buttons'):
                    self.parent._update_segmented_control_buttons()
                    _LOGGER.debug("✅ Segmented control buttons updated for Flat view")
            
            self.on_close()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to complete preprocessing: {e}")
    
    def on_close(self):
        """Clean up resources when closing dialog"""
        try:
            # Clean up interactive masking first
            if hasattr(self, 'masking_active') and self.masking_active:
                self.stop_interactive_masking()
            
            # Clean up span selector
            if hasattr(self, 'span_selector') and self.span_selector:
                try:
                    self.span_selector.set_active(False)
                    self.span_selector = None
                except:
                    pass
            
            # Clean up modular components
            if self.plot_manager:
                self.plot_manager.cleanup()
            
            if self.interactive_widget:
                self.interactive_widget.cleanup()
            
            # Destroy window
            if self.window:
                self.window.destroy()
                
        except Exception as e:
            if self.window:
                self.window.destroy()
    
    def show_final_spectrum_plot(self):
        """Show final preprocessed spectrum plot including apodization"""
        try:
            # Get final processed spectrum (should include all steps including apodization)
            final_wave, final_flux = self.preview_calc.get_current_state()
            
            # Get original spectrum for comparison
            original_wave = self.preprocessor.original_wave if hasattr(self.preprocessor, 'original_wave') else self.preview_calc.original_wave
            original_flux = self.preprocessor.original_flux if hasattr(self.preprocessor, 'original_flux') else self.preview_calc.original_flux
            
            # Update plot manager to show final comparison
            self.plot_manager.show_final_spectrum_comparison(
                original_wave, original_flux, final_wave, final_flux
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display final spectrum: {e}")

    def _on_window_resize(self, event):
        """Handle window resize event to prevent layout issues"""
        try:
            # Only handle resize events for the main window, not child widgets
            if event.widget == self.window:
                # Only trigger if the window size actually changed significantly
                current_width = self.window.winfo_width()
                current_height = self.window.winfo_height()
                
                # Store previous dimensions if not already stored
                if not hasattr(self, '_last_width'):
                    self._last_width = current_width
                    self._last_height = current_height
                    return  # Don't trigger on first resize event
                
                # Only trigger if size changed by more than 50 pixels
                width_diff = abs(current_width - self._last_width)
                height_diff = abs(current_height - self._last_height)
                
                if width_diff > 50 or height_diff > 50:
                    self._last_width = current_width
                    self._last_height = current_height
                    
                    # Defer the layout update to prevent recursion
                    self.window.after_idle(self._handle_delayed_resize)
                    
        except Exception as e:
            pass  # Silently handle resize errors
    
    def _handle_delayed_resize(self):
        """Handle delayed resize to prevent rapid successive updates"""
        try:
            # Force plot manager to recalculate its layout
            if hasattr(self, 'plot_manager') and self.plot_manager:
                self.plot_manager.force_layout_update()
        except Exception as e:
            pass  # Silently handle delayed resize errors

    def apply_current_step(self):
        """Apply the current preprocessing step"""
        if not self.preview_calc:
            return
        
        # Get current step configuration and apply
        if self.current_step == 0:  # Combined Masking & Clipping
            # Sync mask_regions from text before applying
            self._sync_mask_regions_from_text()
            
            # Apply masking first
            if self.mask_regions:
                self.preview_calc.apply_step("masking", mask_regions=self.mask_regions, step_index=self.current_step)
            
            # Then apply clipping operations - both can be applied independently
            if self.aband_var.get():
                self.preview_calc.apply_step("clipping", clip_type="aband", step_index=self.current_step)
            
            if self.sky_var.get():
                try:
                    width = float(self.sky_width_var.get())
                    self.preview_calc.apply_step("clipping", clip_type="sky", width=width, step_index=self.current_step)
                except:
                    messagebox.showerror("Error", "Invalid sky line width value")
                    return
        
        elif self.current_step == 1:  # Savitzky-Golay filtering
            filter_type = self.filter_type_var.get()
            if filter_type != "none":
                try:
                    polyorder = int(self.polyorder_var.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid polynomial order value")
                    return
                    
                if filter_type == "fixed":
                    try:
                        value = float(self.fixed_savgol_var.get())
                        self.preview_calc.apply_step("savgol_filter", filter_type="fixed", value=value, polyorder=polyorder, step_index=self.current_step)
                    except ValueError:
                        messagebox.showerror("Error", "Invalid fixed window size value")
                        return
                elif filter_type == "wavelength":
                    try:
                        value = float(self.wave_savgol_var.get())
                        self.preview_calc.apply_step("savgol_filter", filter_type="wavelength", value=value, polyorder=polyorder, step_index=self.current_step)
                    except ValueError:
                        messagebox.showerror("Error", "Invalid wavelength FWHM value")
                        return
        
        elif self.current_step == 2:  # Log rebinning with flux scaling
            self.preview_calc.apply_step("log_rebin_with_scaling", step_index=self.current_step)
        
        elif self.current_step == 3:  # Continuum fitting
            # Store current state for step-back functionality before applying
            current_wave = self.preview_calc.current_wave.copy()
            current_flux = self.preview_calc.current_flux.copy()
            
            # If in interactive mode and have manual continuum, apply it
            if self.interactive_widget and self.interactive_widget.is_interactive_mode():
                # Manual continuum applied successfully; further debug output removed for production
                try:
                    # Get the manual continuum array directly (no interpolation needed)
                    wave_grid, manual_continuum = self.interactive_widget.get_manual_continuum_array()
                    
                    # Apply the same proper edge handling as the preview calculator
                    # Find where we have actual data in the original flux (before continuum removal)
                    positive_mask = self.preview_calc.current_flux > 0
                    
                    if not np.any(positive_mask):
                        # No positive flux - set to zeros
                        flat_flux = np.zeros_like(self.preview_calc.current_flux)
                    else:
                        positive_indices = np.where(positive_mask)[0]
                        i0, i1 = positive_indices[0], positive_indices[-1]
                        
                        # Apply continuum division with proper centering around 0 (matching fit_continuum behavior)
                        flat_flux = np.zeros_like(self.preview_calc.current_flux)  # Initialize with zeros
                        
                        # Only apply continuum division where we have valid data and positive continuum
                        valid_mask = positive_mask & (manual_continuum > 0)
                        
                        flat_flux[valid_mask] = (self.preview_calc.current_flux[valid_mask] / manual_continuum[valid_mask]) - 1.0
                        
                        # Zero out regions outside the valid data range (same as standard continuum fitting)
                        # This ensures apodization can correctly identify the data boundaries
                        flat_flux[:i0] = 0.0
                        flat_flux[i1+1:] = 0.0
                        
                        # Update the preview calculator with flattened spectrum
                        self.preview_calc.current_flux = flat_flux
                        
                        # Store the continuum for later reconstruction
                        self.preview_calc.stored_continuum = manual_continuum.copy()
                        self.preview_calc.continuum_method = "interactive"
                        self.preview_calc.continuum_kwargs = {'manual_continuum': manual_continuum.copy()}
                        
                        # CRITICAL: Mark that we're using manual continuum to prevent recalculation
                        self.preview_calc.manual_continuum_active = True
                        
                        self.preview_calc.applied_steps.append({
                            'type': 'interactive_continuum', 
                            'kwargs': {
                                'manual_continuum': manual_continuum.copy(),
                                'wave_grid': wave_grid.copy(),
                                'pre_continuum_wave': current_wave,
                                'pre_continuum_flux': current_flux
                            },
                            'step_index': self.current_step
                        })
                        
                        # CRITICAL DEBUG: Verify the flux reconstruction
                        # Calculate what the reconstructed flux should be: (flat + 1) * continuum
                        reconstructed_flux = (flat_flux + 1.0) * manual_continuum
                        
                        # Check the difference
                        valid_mask = (current_flux > 0) & (manual_continuum > 0)
                        if np.any(valid_mask):
                            diff = np.abs(reconstructed_flux[valid_mask] - current_flux[valid_mask])
                            max_diff = np.max(diff)
                            rel_diff = np.max(diff / current_flux[valid_mask]) * 100
                            if max_diff > 1e-10:
                                _LOGGER.debug("Flux reconstruction not exact; max diff %.3e (%.2f%%)" % (max_diff, rel_diff))
                        
                        # CRITICAL: Disable interactive mode after applying
                        self.interactive_widget.disable_interactive_mode()
                        
                except Exception as e:
                    _LOGGER.error(f"Manual continuum application failed: {e}")
                    messagebox.showerror("Error", f"Failed to apply continuum: {str(e)}")
                    return
            else:
                # Apply standard continuum fitting
                # Apply standard continuum fitting (production: minimal logging)
                method = self.continuum_type_var.get()
                if method == "gaussian":
                    try:
                        sigma_str = self.gauss_sigma_var.get()
                        if sigma_str.lower() == "auto":
                            # Use automatic sigma calculation
                            _LOGGER.debug("Automatic sigma calculation for Gaussian continuum")
                            self.preview_calc.apply_step("continuum_fit", method="gaussian", sigma=None, step_index=self.current_step)
                        else:
                            sigma = float(sigma_str)
                            _LOGGER.debug(f"Gaussian continuum sigma={sigma}")
                            self.preview_calc.apply_step("continuum_fit", method="gaussian", sigma=sigma, step_index=self.current_step)
                    except ValueError:
                        messagebox.showerror("Error", "Invalid sigma value. Use 'auto' or a numeric value.")
                        return
                elif method == "spline":
                    try:
                        knots = int(self.spline_knots_var.get())
                        _LOGGER.debug(f"Spline continuum with {knots} knots")
                        self.preview_calc.apply_step("continuum_fit", method="spline", knotnum=knots, step_index=self.current_step)
                    except:
                        messagebox.showerror("Error", "Invalid knot number")
                        return
                
                _LOGGER.debug("Standard continuum fitting completed")
        
        elif self.current_step == 4:  # Apodization
            # Check if already applied
            if self._is_step_applied(4):
                messagebox.showinfo("Already Applied", "Apodization has already been applied and cannot be reapplied.")
                return
            
            if self.apodize_var.get():
                try:
                    percent_str = self.apod_percent_var.get().strip()
                    if not percent_str:
                        messagebox.showerror("Error", "Please enter an apodization percentage value")
                        return
                    
                    percent = float(percent_str)
                    if percent < 0 or percent > 50:
                        messagebox.showerror("Error", "Apodization percentage must be between 0 and 50")
                        return
                    
                    self.preview_calc.apply_step("apodization", percent=percent, step_index=self.current_step)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid apodization percentage: '{self.apod_percent_var.get()}'\nPlease enter a number between 0 and 50")
                    return
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to apply apodization: {str(e)}")
                    return
            # If apodization is not selected, the step is effectively skipped
        
        # Step 6 (Final Review) has no apply action - it's just for viewing and finishing
        
        # Stop interactive masking if it's active (for any step)
        if hasattr(self, 'masking_active') and self.masking_active:
            self.stop_interactive_masking()
        
        # Ensure interactive continuum mode is disabled after applying any step
        # This prevents confusion in subsequent steps like apodization
        if hasattr(self, 'interactive_widget') and self.interactive_widget:
            if self.interactive_widget.is_interactive_mode():
                self.interactive_widget.disable_interactive_mode()
        
        # For non-final steps, move to next step automatically after applying
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update_step_display()
        
        # Update preview and button states after applying step
        self.update_preview()
        self.update_button_states()

    def _apply_unified_styles(self):
        """Ensure buttons use raised relief and enlarge fonts in the left panel for better readability"""
        try:
            self._apply_styles_recursive(self.options_frame)
        except Exception:
            pass  # Silently ignore styling issues – they are non-critical

    def _apply_styles_recursive(self, widget):
        """Recursively walk the widget tree and apply style tweaks"""
        for child in widget.winfo_children():
            # 1) Make every button raised like in the main GUI
            if isinstance(child, tk.Button):
                try:
                    child.configure(relief='raised', bd=2)
                except Exception:
                    pass
            
            # 2) Ensure proper text wrapping for labels with longer text
            if isinstance(child, (tk.Label, tk.Checkbutton, tk.Radiobutton)):
                try:
                    # Get current text and only apply wrapping to longer text
                    text = child.cget('text') if hasattr(child, 'cget') else ''
                    if len(text) > 50 and hasattr(self, '_last_wrap_width'):
                        effective_width = max(150, self._last_wrap_width - 40)
                        child.configure(wraplength=effective_width)
                except Exception:
                    pass
            
            # Recurse into children of this widget
            self._apply_styles_recursive(child)

    def _on_left_panel_resize(self, event):
        """Callback to update wraplength for labels/radio/check buttons when the left panel size changes"""
        try:
            new_width = event.width
            # Avoid excessive updates by checking for significant change
            if not hasattr(self, '_last_wrap_width') or abs(new_width - self._last_wrap_width) > 10:
                self._last_wrap_width = new_width
                # Leave adequate horizontal padding (40px total) so text doesn't touch edges
                effective_width = max(150, new_width - 40)
                self._update_wraplengths(effective_width)
        except Exception:
            pass  # Fail-safe – UI robustness over detailed error handling

    def _update_wraplengths(self, wrap_len: int):
        """Recursively apply a consistent wraplength to all textual widgets inside the options frame"""
        # Safety guard – ensure positive wraplength with adequate margin
        wrap_len = max(100, wrap_len)

        def recurse(widget):
            for child in widget.winfo_children():
                # Recursively process the entire widget tree
                recurse(child)
                # Apply to widgets that support wraplength (Label, Checkbutton, Radiobutton, ttk.Label)
                if isinstance(child, (tk.Label, tk.Checkbutton, tk.Radiobutton, ttk.Label)):
                    try:
                        # Only update wraplength if the widget doesn't have very short text
                        text = child.cget('text') if hasattr(child, 'cget') else ''
                        if len(text) > 50:  # Only wrap longer text to prevent unnecessary wrapping
                            child.configure(wraplength=wrap_len)
                    except (tk.TclError, AttributeError):
                        # Some themed widgets may not expose wraplength or text – ignore
                        pass
        recurse(self.options_frame)
