"""
SNID SAGE - Manual Galaxy Redshift Dialog
=========================================

Interactive dialog for manual galaxy redshift determination.
Allows users to identify galaxy lines by clicking on the spectrum
and calculates redshift based on the identified lines.

Part of the SNID SAGE GUI system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
# REMOVED: Global matplotlib imports that were causing theme interference
# matplotlib imports are now inside methods where they're used
from typing import Dict, List, Tuple, Optional, Any
import math
import matplotlib

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.manual_redshift')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.manual_redshift')

# Import galaxy line constants
try:
    from snid_sage.shared.constants.physical import GALAXY_LINES, SPEED_OF_LIGHT_KMS
except ImportError:
    # Fallback if constants not available
    GALAXY_LINES = {
        'H-α': {'wavelength': 6564.614, 'type': 'emission', 'strength': 'strong', 'color': '#ff4444'},
        '[OIII] 5007': {'wavelength': 5008.239, 'type': 'emission', 'strength': 'strong', 'color': '#44ff44'},
        'Ca II K': {'wavelength': 3933.664, 'type': 'absorption', 'strength': 'strong', 'color': '#888888'},
    }
    SPEED_OF_LIGHT_KMS = 299792.458


# Most common galaxy lines for redshift determination (ordered by commonality/reliability)
COMMON_GALAXY_LINES = {
    'H-α': {'wavelength': 6564.614, 'type': 'emission', 'strength': 'very_strong', 'color': '#ff4444'},
    '[OIII] 5007': {'wavelength': 5008.239, 'type': 'emission', 'strength': 'very_strong', 'color': '#44ff44'}, 
    'H-β': {'wavelength': 4862.721, 'type': 'emission', 'strength': 'strong', 'color': '#ff6666'},
    'Ca II K': {'wavelength': 3933.664, 'type': 'absorption', 'strength': 'strong', 'color': '#888888'},
    'Ca II H': {'wavelength': 3968.470, 'type': 'absorption', 'strength': 'strong', 'color': '#aaaaaa'}
}

# --- Matplotlib backend alignment -------------------------------------------
# Ensure we use the same backend strategy as the preprocessing preview dialog.
# This *must* happen before importing pyplot to avoid a backend switch later
# which can subtly disturb Tkinter styling.

# Reuse already-imported matplotlib symbol from earlier import
try:
    if matplotlib.get_backend() != 'TkAgg':
        matplotlib.use('TkAgg')  # Align with preprocessing dialog
except Exception as _mat_use_err:
    # Backend is already set via pyplot import elsewhere; ignore
    pass

# Clean any stray figures just like preprocessing's PreviewPlotManager does
try:
    import matplotlib.pyplot as _plt
    _plt.close('all')
except Exception:
    pass

# -----------------------------------------------------------------------------

class ManualRedshiftDialog:
    """
    Interactive dialog for manual galaxy redshift determination.
    
    Features:
    - Display spectrum with navigation tools
    - Select galaxy lines from a comprehensive list
    - Click on spectrum to identify lines
    - Real-time redshift calculation
    - Visual feedback with line markers
    - Multiple line identification for accuracy
    """
    
    def __init__(self, parent, spectrum_data: Dict[str, np.ndarray], current_redshift: float = 0.0,
                 include_auto_search: bool = False, auto_search_callback=None):
        """
        Initialize manual redshift dialog.
        
        Args:
            parent: Parent window
            spectrum_data: Dictionary with 'wavelength' and 'flux' arrays
            current_redshift: Current redshift estimate (if any)
        """
        self.parent = parent
        self.spectrum_data = spectrum_data
        self.current_redshift = current_redshift
        
        # Dialog and UI components
        self.dialog = None
        self.result = None
        
        # Plotting components
        self.figure = None
        self.ax_main = None  # Main spectrum plot
        self.ax_zoom = None  # Precision zoom plot
        self.canvas = None
        self.toolbar = None
        
        # Redshift adjustment via drag
        self.overlay_active = False
        self.overlay_redshift = current_redshift if current_redshift > 0 else 0.0
        self.dragging = False
        self.drag_start_x = None
        self.drag_start_redshift = None
        self.precision_mode = False  # Toggle for ultra-precise dragging
        
        # Zoom window controls
        self.zoom_line = 'H-α'  # Default line to focus on
        self.zoom_width = 150  # Angstroms around the line (changed from 100 to 150)
        self.show_zoom = True
        
        # UI state
        self.calculated_redshift = 0.0
        
        # Add update throttling to prevent rapid successive updates (like PreviewPlotManager)
        self._last_update_time = 0
        self._update_throttle_ms = 50  # Minimum 50ms between updates
        
        # Theme-aware color scheme (light palette)
        self.theme_manager = getattr(parent, 'theme_manager', None)

        if self.theme_manager is not None:
            tm = self.theme_manager.get_color
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
                'disabled': tm('disabled'),
                'precision': '#ff6b35'  # keep distinctive orange for precision drag
            }
        else:
            # Fallback light palette (same as UnifiedThemeManager defaults)
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
                'disabled': '#e2e8f0',
                'precision': '#ff6b35'
            }
        
        # Auto search functionality
        self.include_auto_search = include_auto_search
        self.auto_search_callback = auto_search_callback
        

        
        # Remember which spectrum view (Flux / Flat) was active before opening
        self._initial_view_style = None
        try:
            if hasattr(self.parent, 'view_style'):
                self._initial_view_style = self.parent.view_style.get()
        except Exception:
            pass
        
    def show(self) -> Optional[float]:
        """Show the dialog and return the determined redshift"""
        try:
            # No need to disable theme here - handled by show_manual_redshift_dialog()
            
            self._create_dialog()
            self._setup_interface()
            
            # Center the dialog BEFORE adding content to prevent positioning issues
            self._center_dialog()
            
            # Now set up the plots and display after positioning is stable
            self._plot_spectrum()
            self._update_redshift_display()
            
            # Mark initialization as complete to enable resize handlers
            self._initializing = False
            
            # Make modal AFTER everything is set up to prevent focus-related positioning issues
            self.dialog.grab_set()
            
            # Ensure dialog stays focused and centered
            self.dialog.focus_force()

            self.dialog.wait_window()

            return self.result
            
        except Exception as e:
            raise e
    
    def _create_dialog(self):
        """Create the dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Galaxy redshift determination")
        self.dialog.geometry("1400x900")  # Increased from 1200x800
        self.dialog.resizable(True, True)
        self.dialog.minsize(1200, 800)  # Increased minimum size
        
        # Apply background color
        self.dialog.configure(bg=self.colors['bg_main'])
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
        
        # Add initialization flag to prevent resize handler interference
        self._initializing = True
        
        # Add window resize handler to prevent plot glitches (will be enabled after initialization)
        self.dialog.bind('<Configure>', self._on_window_resize)
        
        # Don't set focus yet - do this after centering
        
        _LOGGER.info("🌌 Manual redshift dialog created")
    
    def _center_dialog(self):
        """Center dialog at screen center instead of on parent as requested"""
        # Ensure dialog is fully initialized before positioning
        self.dialog.update_idletasks()
        
        # Always center on screen as requested - independent positioning
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width // 2) - (1400 // 2)
        y = (screen_height // 2) - (900 // 2)
        
        # Ensure position is within screen bounds
        x = max(0, min(x, screen_width - 1400))
        y = max(0, min(y, screen_height - 900))
        
        # Set position without triggering events
        self.dialog.geometry(f"1400x900+{x}+{y}")
        
        # Prevent further automatic repositioning
        self.dialog.wm_resizable(True, True)  # Ensure it's still resizable
    
    def _setup_interface(self):
        """Setup the dialog interface"""
        # Main content with split panel layout matching preprocessing dialog
        self._create_split_panel_layout()
        
        # Footer with buttons
        self._create_footer()
    
    def _create_split_panel_layout(self):
        """Create the main split-panel layout matching preprocessing dialog"""
        # Main container
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create left and right panels - make left panel much smaller to give more space to the plot
        self.left_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], width=350, relief='raised', bd=1)  # Reduced from 500 to 350
        self.left_panel.pack(side='left', fill='y', padx=(0, 5))
        self.left_panel.pack_propagate(False)
        
        self.right_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], relief='raised', bd=1)
        self.right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Setup panels
        self._create_left_panel()
        self._create_right_panel()
    
    def _create_left_panel(self):
        """Create the reorganized precision control panel with larger fonts"""
        
        # 1. MANUAL SEARCH - Interactive adjustment (moved to top priority)
        controls_frame = tk.LabelFrame(self.left_panel, text="🎛️ Interactive Search", 
                                     bg=self.colors['bg_step'],
                                     fg=self.colors['text_primary'],
                                     font=('Segoe UI', 16, 'bold'))
        controls_frame.pack(fill='x', padx=10, pady=(20, 15))
        
        # Create two-column layout for controls
        controls_row = tk.Frame(controls_frame, bg=self.colors['bg_step'])
        controls_row.pack(fill='x', padx=10, pady=15)
        
        # Left column - Overlay toggle
        overlay_col = tk.Frame(controls_row, bg=self.colors['bg_step'])
        overlay_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        overlay_label = tk.Label(overlay_col, text="Reference Lines:",
                               bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 12, 'bold'))
        overlay_label.pack(pady=(0, 8))
        
        self.overlay_button = tk.Button(overlay_col, text="🎯 Show Lines",
                                      command=self._toggle_overlay,
                                      bg='#8b5cf6', fg='white',  # Purple for interactive feature
                                      font=('Segoe UI', 12, 'bold'),
                                      relief='raised', bd=2, height=2, width=12)
        self.overlay_button.pack(pady=(10, 5))
        
        # Right column - Precision mode
        precision_col = tk.Frame(controls_row, bg=self.colors['bg_step'])
        precision_col.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        precision_label = tk.Label(precision_col, text="Drag Sensitivity:",
                                 bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                 font=('Segoe UI', 12, 'bold'))
        precision_label.pack(pady=(0, 8))
        
        self.precision_button = tk.Button(precision_col, text="⚡ Normal",
                                        command=self._toggle_precision_mode,
                                        bg='#f59e0b', fg='white',  # Amber/orange for precision control
                                        font=('Segoe UI', 12, 'bold'),
                                        relief='raised', bd=2, height=2, width=12)
        self.precision_button.pack(pady=(10, 5))
        
        # 2. DIRECT REDSHIFT INPUT - Moved to second position  
        input_frame = tk.LabelFrame(self.left_panel, text="⌨️ Manual Search", 
                                  bg=self.colors['bg_step'],
                                  fg=self.colors['text_primary'],
                                  font=('Segoe UI', 16, 'bold'))
        input_frame.pack(fill='x', padx=10, pady=(0, 15))
        
        # Input label
        input_label = tk.Label(input_frame, text="Enter known redshift (auto-shows lines):",
                             bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 13, 'bold'))
        input_label.pack(pady=(15, 8), padx=10)
        
        # Input field and apply button in same row - centered
        input_row = tk.Frame(input_frame, bg=self.colors['bg_step'])
        input_row.pack(padx=10, pady=(0, 15))  # Remove fill='x' to allow centering
        
        # Redshift input field
        self.redshift_input_var = tk.StringVar()
        self.redshift_entry = tk.Entry(input_row, textvariable=self.redshift_input_var,
                                     font=('Courier New', 14, 'bold'),
                                     width=12, justify='center',
                                     bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                     insertbackground=self.colors['accent'])
        self.redshift_entry.pack(side='left', padx=(0, 10))
        
        # Apply button
        apply_button = tk.Button(input_row, text="▶ Apply",
                               command=self._apply_direct_redshift,
                               bg='#3b82f6', fg='white',  # Blue for apply action
                               font=('Segoe UI', 12, 'bold'),
                               relief='raised', bd=2, width=8)
        apply_button.pack(side='right', padx=(10, 20))
        
        # Bind Enter key to apply
        self.redshift_entry.bind('<Return>', lambda e: self._apply_direct_redshift())
        
        # 3. AUTO SEARCH BUTTON if functionality is enabled
        if self.include_auto_search:
            # Auto search section
            auto_frame = tk.LabelFrame(self.left_panel, text="🚀 Automatic Search", 
                                     bg=self.colors['bg_step'],
                                     fg=self.colors['text_primary'],
                                     font=('Segoe UI', 16, 'bold'))
            auto_frame.pack(fill='x', padx=10, pady=(0, 15))
            
            # Auto search label
            auto_label = tk.Label(auto_frame, text="Let SNID find the best redshift match:",
                                bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 13, 'bold'))
            auto_label.pack(pady=(15, 8), padx=10)
            
            # Auto search button - smaller and more proportional
            auto_button_frame = tk.Frame(auto_frame, bg=self.colors['bg_step'])
            auto_button_frame.pack(pady=(0, 15))
            
            self.auto_search_button = tk.Button(auto_button_frame, text="🔍 Auto Search",
                                               command=self._perform_auto_search,
                                               bg='#10b981', fg='white',  # Consistent green color
                                               font=('Segoe UI', 12, 'bold'),
                                               relief='raised', bd=2, height=1, width=20)
            self.auto_search_button.pack()
        
        # 4. FOCUS LINE SELECTION - Line type choice
        zoom_frame = tk.LabelFrame(self.left_panel, text="🔍 Focus Line Selection", 
                                 bg=self.colors['bg_step'],
                                 fg=self.colors['text_primary'],
                                 font=('Segoe UI', 16, 'bold'))
        zoom_frame.pack(fill='x', padx=10, pady=(0, 15))
        
        # Line selection for zoom
        zoom_label = tk.Label(zoom_frame, text="Select line for precision zoom:",
                            bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                            font=('Segoe UI', 13, 'bold'))
        zoom_label.pack(pady=(15, 8), padx=10)
        
        # Line selection and zoom width on same row
        line_row = tk.Frame(zoom_frame, bg=self.colors['bg_step'])
        line_row.pack(fill='x', padx=10, pady=(0, 15))
        
        # StringVar holding the currently selected focus line
        self.zoom_line_var = tk.StringVar(value=self.zoom_line)

        # Available focus-line options
        line_options = list(COMMON_GALAXY_LINES.keys())

        # Classic Tk OptionMenu with improved styling
        self.zoom_menu = tk.OptionMenu(
            line_row,
            self.zoom_line_var,
            *line_options,
            command=lambda _sel: self._on_zoom_line_changed())

        # Style the OptionMenu to match the dialog's colour scheme
        self.zoom_menu.config(
            font=('Segoe UI', 12, 'bold'),  # Match Normal/Hide Lines font
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent'],
            activeforeground='white',
            relief='raised',
            bd=2,
            highlightthickness=0,
            width=12,  # Same size as Normal/Hide Lines buttons
            height=2,  # Make it taller
            cursor='hand2'
        )
        
        # Style the dropdown menu items with larger font
        menu = self.zoom_menu['menu']
        menu.config(
            font=('Segoe UI', 14, 'bold'),  # Larger font for dropdown items
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent'],
            activeforeground='white',
            bd=1,
            relief='solid'
        )
        
        self.zoom_menu.pack(side='left', padx=(0, 15))
        
        # Right side - Zoom width controls
        width_label = tk.Label(line_row, text="Width:",
                             bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 12, 'bold'))
        width_label.pack(side='left', padx=(0, 5))
        
        self.zoom_width_var = tk.StringVar(value=str(self.zoom_width))
        width_spinbox = tk.Spinbox(line_row, from_=50, to=300, increment=25,
                                 textvariable=self.zoom_width_var, width=10,  # Made bigger as requested
                                 font=('Segoe UI', 14, 'bold'),  # Bigger font as requested
                                 command=self._on_zoom_width_changed)
        width_spinbox.pack(side='left', padx=(0, 5))
        
        unit_label = tk.Label(line_row, text="Å",
                            bg=self.colors['bg_step'], fg=self.colors['text_secondary'],
                            font=('Segoe UI', 12, 'bold'))
        unit_label.pack(side='left')
        
        # 5. CURRENT REDSHIFT - Results display (moved to bottom)
        redshift_frame = tk.LabelFrame(self.left_panel, text="📊 Current Redshift", 
                                     bg=self.colors['bg_step'],
                                     fg=self.colors['text_primary'],
                                     font=('Segoe UI', 16, 'bold'))
        redshift_frame.pack(fill='x', padx=10, pady=(0, 20))
        
        self.redshift_label = tk.Label(redshift_frame, 
                                     text="",  # Empty until user sets a value
                                     bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                     font=('Courier New', 18, 'bold'))
        self.redshift_label.pack(pady=15)
    
    def _create_right_panel(self):
        """Create the right visualization panel"""
        # Create plot container frame - maximize space by removing title header
        plot_frame = tk.Frame(self.right_panel, bg=self.colors['bg_panel'])
        plot_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Setup the plot in the frame
        self._setup_plot_in_frame(plot_frame)
    
    def _create_results_display(self):
        """Create the results display area"""
        # Current selection with larger font
        self.selection_label = tk.Label(self.results_frame, 
                                      text="No line selected",
                                      bg=self.colors['bg_step'], fg=self.colors['text_secondary'],
                                      font=('Segoe UI', 12, 'bold'))  # Increased font size
        self.selection_label.pack(pady=(15, 8))  # Increased padding
        
        # Identified lines list with larger font
        lines_label = tk.Label(self.results_frame, text="Identified Lines:",
                             bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                             font=('Segoe UI', 12, 'bold'))  # Increased font size
        lines_label.pack(pady=(15, 8))  # Increased padding
        
        # Scrollable list of identified lines with dark theme and larger font
        listbox_frame = tk.Frame(self.results_frame, bg=self.colors['bg_step'])
        listbox_frame.pack(fill='x', padx=15, pady=8)  # Increased padding
        
        self.lines_listbox = tk.Listbox(listbox_frame, height=7,  # Increased height
                                       bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                       selectbackground=self.colors['accent'],
                                       font=('Courier', 11))  # Increased font size
        # Use plain tk.Scrollbar instead of ttk.Scrollbar to prevent unwanted global ttk theme changes
        scrollbar_lines = tk.Scrollbar(listbox_frame, orient='vertical', command=self.lines_listbox.yview,
                                       bg=self.colors['bg_step'], troughcolor=self.colors['bg_main'], relief='flat', bd=0)
        self.lines_listbox.configure(yscrollcommand=scrollbar_lines.set)
        
        self.lines_listbox.pack(side='left', fill='both', expand=True)
        scrollbar_lines.pack(side='right', fill='y')
        
        # Redshift results with larger fonts
        self.redshift_label = tk.Label(self.results_frame, 
                                     text="Calculated z: Not available",
                                     bg=self.colors['bg_step'], fg=self.colors['accent'],
                                     font=('Segoe UI', 13, 'bold'))  # Increased font size
        self.redshift_label.pack(pady=(15, 8))  # Increased padding
        
        self.uncertainty_label = tk.Label(self.results_frame, 
                                        text="Uncertainty: Not available", 
                                        bg=self.colors['bg_step'], fg=self.colors['text_secondary'],
                                        font=('Segoe UI', 11))  # Increased font size
        self.uncertainty_label.pack(pady=(0, 8))  # Added padding
        
        # Overlay redshift display (for auto-mode)
        self.overlay_redshift_label = tk.Label(self.results_frame, 
                                             text="Overlay z: Not active",
                                             bg=self.colors['bg_step'], fg=self.colors['accent'],
                                             font=('Segoe UI', 11, 'bold'))
        self.overlay_redshift_label.pack(pady=(8, 8))
        
        # Control buttons with larger fonts
        button_frame = tk.Frame(self.results_frame, bg=self.colors['bg_step'])
        button_frame.pack(fill='x', padx=15, pady=15)  # Increased padding
        
        clear_button = tk.Button(button_frame, text="🗑️ Clear All",
                               command=self._clear_all_lines,
                               bg=self.colors['warning'], fg='white',
                               font=('Segoe UI', 11, 'bold'),  # Increased font size
                               relief='raised', bd=2,
                               height=2)  # Increased height
        clear_button.pack(side='left', padx=(0, 8))  # Increased padding
        
        remove_button = tk.Button(button_frame, text="❌ Remove Last",
                                command=self._remove_last_line,
                                bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 11, 'bold'),  # Increased font size
                                relief='raised', bd=2,
                                height=2)  # Increased height
        remove_button.pack(side='right')
    
    def _setup_plot_in_frame(self, plot_frame):
        """Setup matplotlib plot for spectrum visualization using proper sizing like preprocessing dialog"""
        # Ensure backend consistency
        if matplotlib.get_backend() != 'TkAgg':
            matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        plt.close('all')
        
        try:
            # Create figure with dynamic sizing (like PreviewPlotManager)
            self.figure = matplotlib.figure.Figure(facecolor=self.colors['bg_panel'], edgecolor='none')
            self.figure.patch.set_facecolor(self.colors['bg_panel'])
            
            # Create grid layout: main plot (70%) and zoom plot (30%)
            gs = self.figure.add_gridspec(1, 2, width_ratios=[7, 3], hspace=0.1, wspace=0.3)
            
            # Main spectrum plot
            self.ax_main = self.figure.add_subplot(gs[0])
            self._setup_isolated_axis(self.ax_main)
            
            # Precision zoom plot
            self.ax_zoom = self.figure.add_subplot(gs[1])
            self._setup_isolated_axis(self.ax_zoom)
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            # Create and embed canvas with proper configuration (following PreviewPlotManager pattern)
            self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
            canvas_widget = self.canvas.get_tk_widget()
            
            # Configure canvas widget for proper filling
            canvas_widget.configure(
                bg=self.colors['bg_panel'], 
                highlightthickness=0,
                bd=0
            )

            canvas_widget.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Force widget to update and calculate proper size (key fix from PreviewPlotManager)
            canvas_widget.update_idletasks()
            
            # Get actual canvas dimensions for proper figure sizing
            canvas_width = canvas_widget.winfo_width()
            canvas_height = canvas_widget.winfo_height()
            
            # Set figure size based on actual canvas size (convert pixels to inches)
            if canvas_width > 1 and canvas_height > 1:
                dpi = self.figure.dpi
                fig_width = max(6, canvas_width / dpi)
                fig_height = max(4, canvas_height / dpi)
                self.figure.set_size_inches(fig_width, fig_height)
            
            # Adjust subplot layout to fill available space efficiently (key fix!)
            self.figure.subplots_adjust(
                left=0.08,    # Small left margin
                right=0.95,   # Small right margin  
                top=0.93,     # Small top margin
                bottom=0.12,  # Space for bottom labels
                hspace=0.1,   # Minimal space between plots (since we only have 1 row)
                wspace=0.3    # Space between main and zoom plots
            )
            
            # Draw once everything is properly configured
            self.canvas.draw()
            
            # Connect events for dragging
            self.canvas.mpl_connect('button_press_event', self._on_mouse_press)
            self.canvas.mpl_connect('button_release_event', self._on_mouse_release)
            self.canvas.mpl_connect('motion_notify_event', self._on_mouse_motion)
            
        finally:
            pass
    
    def _force_layout_recalculation(self):
        """Force matplotlib to recalculate layout geometry for dynamic resizing"""
        try:
            # Get current canvas dimensions
            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.update_idletasks()
            
            width = canvas_widget.winfo_width()
            height = canvas_widget.winfo_height()
            
            # Only proceed if we have reasonable dimensions
            if width > 100 and height > 100:
                # Update figure size to match canvas
                dpi = self.figure.dpi
                fig_width = width / dpi
                fig_height = height / dpi
                
                # Set new figure size
                self.figure.set_size_inches(fig_width, fig_height, forward=False)
                
                # Readjust subplot layout for new size
                self.figure.subplots_adjust(
                    left=0.08,
                    right=0.95,
                    top=0.93,
                    bottom=0.12,
                    hspace=0.1,   # Minimal space for single row
                    wspace=0.3    # Space between main and zoom plots
                )
                
                # Use draw_idle for smooth updates
                self.canvas.draw_idle()
                
        except Exception as e:
            # Just continue without layout update
            pass
    
    def _setup_isolated_axis(self, ax):
        """Setup axis with custom styling for dialog"""
        # Set all properties explicitly without any theme manager calls
        ax.set_facecolor(self.colors['bg_main'])
        
        # Configure all text elements with explicit colors
        ax.tick_params(
            axis='both',
            colors=self.colors['text_primary'], 
            labelcolor=self.colors['text_primary'],
            labelsize=9,
            direction='out',
            length=4,
            width=0.8
        )
        
        # Configure spines explicitly
        for spine_name in ['bottom', 'top', 'right', 'left']:
            spine = ax.spines[spine_name]
            spine.set_color(self.colors['text_primary'])
            spine.set_linewidth(0.8)
            spine.set_alpha(0.8)
        
        # Configure grid explicitly
        ax.grid(True, alpha=0.3, color=self.colors['text_secondary'], 
                linewidth=0.5, linestyle='-')
        ax.set_axisbelow(True)
        
        # Set label properties that will be used later
        ax.xaxis.label.set_color(self.colors['text_primary'])
        ax.yaxis.label.set_color(self.colors['text_primary'])
        ax.xaxis.label.set_fontsize(11)
        ax.yaxis.label.set_fontsize(11)

    def _plot_spectrum(self):
        """Plot the galaxy spectrum with complete isolation from theme system"""
        try:
            # Throttle updates to prevent rapid successive calls (like PreviewPlotManager)
            import time
            current_time = time.time() * 1000  # Convert to milliseconds
            if current_time - self._last_update_time < self._update_throttle_ms:
                return
            self._last_update_time = current_time
            
            _LOGGER.info("🎯 Starting spectrum plotting...")
            
            # Validate spectrum data
            if not self.spectrum_data or 'wavelength' not in self.spectrum_data or 'flux' not in self.spectrum_data:
                _LOGGER.error("❌ Invalid spectrum data")
                return
            
            wavelength = self.spectrum_data['wavelength']
            flux = self.spectrum_data['flux']
            
            if wavelength is None or flux is None or len(wavelength) == 0 or len(flux) == 0:
                _LOGGER.error("❌ Empty spectrum arrays")
                return
                
            if len(wavelength) != len(flux):
                _LOGGER.error(f"❌ Mismatched array lengths: wave={len(wavelength)}, flux={len(flux)}")
                return
            
            _LOGGER.info(f"✅ Spectrum data valid: {len(wavelength)} points")
            
            # Check matplotlib components
            if self.ax_main is None or self.ax_zoom is None or self.canvas is None:
                _LOGGER.error("❌ Matplotlib components not initialized")
                return
            
            # Clear plots WITHOUT triggering any theme updates (like PreviewPlotManager)
            self.ax_main.clear()
            self.ax_zoom.clear()
            
            # Re-apply isolated styling after clear to ensure consistent appearance
            self._setup_isolated_axis(self.ax_main)
            self._setup_isolated_axis(self.ax_zoom)
            
            # ================================
            # Main spectrum plot
            # ================================
            _LOGGER.info("📊 Plotting main spectrum...")
            
            # Plot with explicit colors - no theme lookup
            self.ax_main.plot(wavelength, flux, 
                            color=self.colors['text_primary'], 
                            linewidth=1, 
                            alpha=0.8, 
                            label='Galaxy Spectrum')
            
            # Set labels with explicit styling
            self.ax_main.set_xlabel('Wavelength (Å)', 
                                  fontsize=11, 
                                  color=self.colors['text_primary'])
            self.ax_main.set_ylabel('Flux', 
                                  fontsize=11, 
                                  color=self.colors['text_primary'])
            
            if self.overlay_active:
                _LOGGER.info("📍 Drawing overlay lines...")
                self._draw_overlay_lines()
            
            # ================================
            # PRECISION ZOOM PLOT - Isolated
            # ================================
            if self.overlay_active and self.zoom_line in COMMON_GALAXY_LINES:
                _LOGGER.info("🔍 Setting up zoom window...")
                self._plot_zoom_window()
            else:
                # Show inactive zoom window with explicit styling
                self.ax_zoom.text(0.5, 0.5, 
                                '🔍 Precision View\n\nActivate overlay to\nenable zoom window\n\nSelect focus line\nfrom left panel', 
                                transform=self.ax_zoom.transAxes, 
                                ha='center', va='center',
                                fontsize=11, 
                                color=self.colors['text_secondary'],
                                bbox=dict(boxstyle="round,pad=0.5", 
                                        facecolor=self.colors['bg_step'], 
                                        alpha=0.8, 
                                        edgecolor=self.colors['accent']))
            
            # Draw canvas WITHOUT triggering any global updates (use draw_idle for smoother updates)
            _LOGGER.info("🎨 Drawing canvas...")
            self.canvas.draw_idle()
            
            _LOGGER.info("✅ Spectrum plotting completed successfully")
            
            # Update display
            self._update_redshift_display()
            
        except Exception as e:
            _LOGGER.error(f"❌ Error in _plot_spectrum: {e}")
            import traceback
            _LOGGER.error(f"   Traceback: {traceback.format_exc()}")

    def _plot_zoom_window(self):
        """Plot the precision zoom window with isolated styling"""
        line_info = COMMON_GALAXY_LINES[self.zoom_line]
        rest_wave = line_info['wavelength']
        obs_wave = rest_wave * (1 + self.overlay_redshift)
        
        # Define focus color explicitly - no theme lookup
        focus_color = '#00ff44'  # Bright green for focus line
        
        # Calculate zoom window bounds
        half_width = self.zoom_width / 2
        zoom_min = obs_wave - half_width
        zoom_max = obs_wave + half_width
        
        # Extract zoom region from spectrum
        wavelength = self.spectrum_data['wavelength']
        flux = self.spectrum_data['flux']
        
        mask = (wavelength >= zoom_min) & (wavelength <= zoom_max)
        if not np.any(mask):
            # No data in zoom region - use explicit styling
            self.ax_zoom.text(0.5, 0.5, 
                            f'⚠️ No data in zoom region\n{zoom_min:.1f} - {zoom_max:.1f} Å', 
                            transform=self.ax_zoom.transAxes, 
                            ha='center', va='center',
                            fontsize=10, 
                            color=self.colors['warning'])
            return
        
        zoom_wave = wavelength[mask]
        zoom_flux = flux[mask]
        
        # Plot zoomed spectrum with explicit colors
        self.ax_zoom.plot(zoom_wave, zoom_flux, 
                         color=self.colors['text_primary'], 
                         linewidth=2, 
                         alpha=0.9, 
                         label='Zoomed Spectrum')
        
        # Draw the reference line with explicit styling
        self.ax_zoom.axvline(obs_wave, 
                           color=focus_color, 
                           linestyle='-', 
                           alpha=1.0, 
                           linewidth=4,
                           label=f'{self.zoom_line} Reference')
        
        # Add crosshairs for precision alignment
        y_center = np.mean(zoom_flux)
        self.ax_zoom.axhline(y_center, 
                           color=self.colors['accent'], 
                           linestyle=':', 
                           alpha=0.6, 
                           linewidth=1)
        
        # Labels with explicit styling
        self.ax_zoom.set_xlabel('Wavelength (Å)', 
                              fontsize=9, 
                              color=self.colors['text_primary'])
        self.ax_zoom.set_ylabel('Flux', 
                              fontsize=9, 
                              color=self.colors['text_primary'])
        
        # Set zoom window limits
        self.ax_zoom.set_xlim(zoom_min, zoom_max)
        
        # Add text box with precision info - all explicit styling
        info_text = f'z = {self.overlay_redshift:.6f}'
        self.ax_zoom.text(0.98, 0.98, info_text, 
                        transform=self.ax_zoom.transAxes, 
                        ha='right', va='top', 
                        fontsize=9,
                        bbox=dict(boxstyle="round,pad=0.4", 
                                facecolor=focus_color, 
                                alpha=0.9, 
                                edgecolor='white', 
                                linewidth=2),
                        color='white', 
                        fontweight='bold')

    def _draw_overlay_lines(self):
        """Draw overlay lines with isolated styling - no theme lookups"""
        wavelength = self.spectrum_data['wavelength']
        
        # Define colors explicitly
        focus_color = '#00ff44'  # Bright green for focus line
        reference_color = '#888888'  # Grey for all other lines
        
        # Draw overlay lines for all galaxy lines
        for line_name, line_info in COMMON_GALAXY_LINES.items():
            rest_wave = line_info['wavelength']
            obs_wave = rest_wave * (1 + self.overlay_redshift)
            
            # Only show if within the spectrum range
            if wavelength.min() <= obs_wave <= wavelength.max():
                # Color and style based on whether this is the focus line
                if line_name == self.zoom_line:
                    # FOCUS LINE - explicit styling
                    color = focus_color
                    linewidth = 4
                    alpha = 1.0
                    linestyle = '-'
                    label_alpha = 1.0
                    bbox_alpha = 0.8
                else:
                    # REFERENCE LINES - explicit styling
                    color = reference_color
                    linewidth = 2
                    alpha = 0.7
                    linestyle = '--'
                    label_alpha = 0.8
                    bbox_alpha = 0.4
                
                # Draw overlay line with explicit parameters
                self.ax_main.axvline(obs_wave, 
                                   color=color, 
                                   linestyle=linestyle, 
                                   alpha=alpha, 
                                   linewidth=linewidth)
                
                # Add label with explicit styling
                y_pos = self.ax_main.get_ylim()[1] * 0.9
                if line_name == self.zoom_line:
                    label_text = line_name  # Remove FOCUS indicator as requested
                    font_weight = 'bold'
                    font_size = 9
                else:
                    label_text = line_name
                    font_weight = 'normal'
                    font_size = 8
                
                # Explicit bbox properties
                bbox_props = dict(boxstyle="round,pad=0.3", 
                                facecolor=color, 
                                alpha=bbox_alpha, 
                                edgecolor='white' if line_name == self.zoom_line else 'none',
                                linewidth=1 if line_name == self.zoom_line else 0)
                
                # Draw text with all explicit parameters
                self.ax_main.text(obs_wave, y_pos, label_text, 
                                rotation=90, 
                                ha='right', 
                                va='top', 
                                fontsize=font_size, 
                                fontweight=font_weight,
                                color='white' if line_name == self.zoom_line else color, 
                                alpha=label_alpha, 
                                bbox=bbox_props)
    
    def _update_redshift_display(self):
        """Update the redshift display with high precision"""
        # Show value only when a non-zero redshift is available
        if self.overlay_redshift > 0:
            self.redshift_label.config(text=f"z = {self.overlay_redshift:.6f}", fg=self.colors['text_primary'])
        else:
            self.redshift_label.config(text="", fg=self.colors['text_primary'])
        self.calculated_redshift = self.overlay_redshift
    
    def _update_line_button_states(self):
        """Update button states - simplified for overlay mode"""
        pass  # No longer needed with overlay-only interface
    
    def _update_line_selection_display(self):
        """Update line selection display - simplified for overlay mode"""
        pass  # No longer needed with overlay-only interface
    
    def _calculate_redshift(self):
        """Calculate redshift - simplified for overlay mode"""
        self.calculated_redshift = self.overlay_redshift
        self._update_redshift_display()
    
    def _apply_direct_redshift(self):
        """Apply directly input redshift value"""
        input_text = self.redshift_input_var.get().strip()
        
        if not input_text:
            messagebox.showwarning("Invalid Input", "Please enter a redshift value.")
            return
        
        try:
            # Parse the input redshift
            new_redshift = float(input_text)
            
            # Validate range
            if new_redshift < 0.0:
                messagebox.showwarning("Invalid Range", 
                                     "Redshift must be non-negative (z ≥ 0).")
                return
            
            if new_redshift > 5.0:
                confirm = messagebox.askyesno("High Redshift", 
                                            f"Redshift z = {new_redshift:.6f} is very high.\n"
                                            f"Are you sure this is correct?")
                if not confirm:
                    return
            
            # Apply the new redshift
            self.overlay_redshift = new_redshift
            
            # Clear the input field
            self.redshift_input_var.set("")
            
            # Automatically activate overlay if not already active
            if not self.overlay_active:
                self._toggle_overlay()
            
            # Update the display
            self._plot_spectrum()
            self._update_redshift_display()
            
            _LOGGER.info(f"⌨️ Applied direct redshift input: z = {new_redshift:.6f}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", 
                               f"'{input_text}' is not a valid number.\n"
                               f"Please enter a numeric redshift value (e.g., 0.1, 0.025).")

    def _perform_auto_search(self):
        """Perform automatic redshift search and apply the best result"""
        if not self.auto_search_callback:
            messagebox.showerror("Auto Search Error", "Auto search functionality not available.")
            return
        
        try:
            # Create progress dialog
            progress_dialog = tk.Toplevel(self.dialog)
            progress_dialog.title("Automatic Redshift Search")
            progress_dialog.geometry("500x300")
            progress_dialog.transient(self.dialog)
            progress_dialog.grab_set()
            
            # Center progress dialog
            progress_dialog.update_idletasks()
            x = self.dialog.winfo_x() + (self.dialog.winfo_width() // 2) - (500 // 2)
            y = self.dialog.winfo_y() + (self.dialog.winfo_height() // 2) - (300 // 2)
            progress_dialog.geometry(f"500x300+{x}+{y}")
            
            # Progress dialog content
            progress_frame = tk.Frame(progress_dialog, bg=self.colors['bg_main'])
            progress_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            title_label = tk.Label(progress_frame, text="🔍 Automatic Redshift Search",
                                 font=('Segoe UI', 16, 'bold'),
                                 bg=self.colors['bg_main'], fg=self.colors['text_primary'])
            title_label.pack(pady=(0, 20))
            
            status_label = tk.Label(progress_frame, text="Initializing...",
                                  font=('Segoe UI', 12),
                                  bg=self.colors['bg_main'], fg=self.colors['text_secondary'])
            status_label.pack(pady=(0, 20))
            
            # Replace ttk.Progressbar (which triggers global ttk styling and resets button colours)
            # with a lightweight Canvas-based animated bar that has no side-effects on ttk themes.
            progress_canvas = tk.Canvas(progress_frame, width=400, height=20,
                                       bg=self.colors['bg_step'], highlightthickness=0, bd=0)
            progress_canvas.pack(pady=(0, 20))

            bar_width = 80  # Width of the moving indicator
            bar = progress_canvas.create_rectangle(0, 0, bar_width, 20,
                                                   fill=self.colors['accent'], width=0)

            def _animate_bar():
                if not progress_dialog.winfo_exists():
                    return  # Dialog closed – stop animation

                # Move the bar across the canvas in a ping-pong fashion
                x1, y1, x2, y2 = progress_canvas.coords(bar)
                if x2 >= 400:
                    # Reset to start
                    progress_canvas.coords(bar, 0, 0, bar_width, 20)
                else:
                    progress_canvas.move(bar, 8, 0)  # Move 8 px per frame

                progress_canvas.after(40, _animate_bar)

            # Start animation
            progress_canvas.after(40, _animate_bar)
            
            # Status update function
            def update_status(message):
                status_label.config(text=message)
                progress_dialog.update()
            
            # Run the search in a separate thread
            import threading
            
            result_container = {'result': None, 'error': None}
            
            def run_search():
                try:
                    result_container['result'] = self.auto_search_callback(update_status)
                except Exception as e:
                    result_container['error'] = str(e)
            
            # Start the search thread
            search_thread = threading.Thread(target=run_search)
            search_thread.daemon = True
            search_thread.start()
            
            # Wait for completion (with timeout)
            max_wait_time = 60  # 60 seconds timeout
            wait_count = 0
            while search_thread.is_alive() and wait_count < max_wait_time * 10:
                progress_dialog.update()
                self.dialog.after(100)  # Wait 100ms
                wait_count += 1
            
            # Close progress dialog once search completes or times out
            if progress_dialog.winfo_exists():
                progress_dialog.destroy()
            
            # Show timeout error if thread is still running.
            if search_thread.is_alive():
                messagebox.showerror(
                    "Search Timeout",
                    "Automatic redshift search timed out after 60 seconds.")
                return
            
            # Handle errors
            if result_container['error']:
                messagebox.showerror("Search Error", 
                                   f"Auto search failed:\n{result_container['error']}")
                return
            
            # Process results
            result = result_container['result']
            if not result or not result.get('success'):
                messagebox.showwarning("No Results", 
                                     "No suitable redshift matches found.\n"
                                     "Please try manual redshift determination.")
                return
            
            # Show results and ask user if they want to apply
            best_z = result['redshift']
            best_rlap = result['rlap']
            best_template = result['template']
            confidence = result['confidence']
            
            # Create results message
            confidence_text = {
                'high': 'High (RLAP ≥ 8.0)',
                'medium': 'Medium (5.0 ≤ RLAP < 8.0)',
                'low': 'Low (3.0 ≤ RLAP < 5.0)',
                'very_low': 'Very Low (RLAP < 3.0)'
            }.get(confidence, 'Unknown')
            
            message = (f"🎯 Auto Search Results:\n\n"
                      f"Best Redshift: z = {best_z:.6f}\n"
                      f"RLAP Score: {best_rlap:.1f}\n"
                      f"Template: {best_template}\n"
                      f"Confidence: {confidence_text}\n\n"
                      f"Apply this redshift to the spectrum?")
            
            response = messagebox.askyesno("Auto Search Complete", message)
            
            if response:
                # Apply the automatically found redshift
                self.overlay_redshift = best_z
                _LOGGER.info(f"🚀 Applied auto-search redshift: z = {best_z:.4f} (RLAP: {best_rlap:.1f})")
                
                # Activate overlay if not already active
                if not self.overlay_active:
                    self.overlay_active = True
                    self.overlay_button.config(text="🔍 Hide Lines")
                
                # Refresh the display
                self._plot_spectrum()
                self._update_redshift_display()
                
                # Update input field with 6 decimal precision to match the actual value
                self.redshift_input_var.set(f"{best_z:.6f}")
                
                # Show confirmation that redshift has been applied
                # Use a custom dialog to maintain focus on the Galaxy redshift dialog
                self._show_redshift_applied_confirmation(best_z)
            
        except Exception as e:
            _LOGGER.error(f"Error in auto search: {e}")
            messagebox.showerror("Auto Search Error", f"Failed to perform auto search:\n{str(e)}")
    
    def _clear_all_lines(self):
        """Clear all - reset redshift in overlay mode"""
        self.overlay_redshift = 0.0
        self._plot_spectrum()
        _LOGGER.info("🗑️ Reset redshift to default")
    
    def _remove_last_line(self):
        """Remove last - reset redshift in overlay mode"""
        self.overlay_redshift = 0.0
        self._plot_spectrum()
        _LOGGER.info("❌ Reset redshift to default")
    
    def _mark_button_as_workflow_managed(self, button: tk.Button, button_name: str = "dialog_button"):
        """Dialog buttons use simple fixed colors and don't interact with the workflow system"""
        pass
    
    def _show_redshift_applied_confirmation(self, redshift_value: float):
        """Show confirmation dialog that maintains focus on the Galaxy redshift dialog"""
        # Create a custom confirmation dialog that won't steal focus from the main dialog
        confirmation_dialog = tk.Toplevel(self.dialog)
        confirmation_dialog.title("Redshift Applied")
        confirmation_dialog.geometry("500x200")
        confirmation_dialog.transient(self.dialog)  # Make it a child of the main dialog
        confirmation_dialog.grab_set()  # Make it modal to the main dialog
        
        # Center the confirmation dialog over the main dialog
        confirmation_dialog.update_idletasks()
        x = self.dialog.winfo_x() + (self.dialog.winfo_width() // 2) - (500 // 2)
        y = self.dialog.winfo_y() + (self.dialog.winfo_height() // 2) - (200 // 2)
        confirmation_dialog.geometry(f"500x200+{x}+{y}")
        
        # Configure the dialog appearance
        confirmation_dialog.configure(bg=self.colors['bg_main'])
        confirmation_dialog.resizable(False, False)
        
        # Create content frame
        content_frame = tk.Frame(confirmation_dialog, bg=self.colors['bg_main'], padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Success icon and title
        title_label = tk.Label(content_frame, text="✅ Redshift Applied Successfully",
                             font=('Segoe UI', 16, 'bold'),
                             bg=self.colors['bg_main'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 15))
        
        # Redshift value with 6 decimal precision
        redshift_label = tk.Label(content_frame, 
                                text=f"Redshift: z = {redshift_value:.6f}",
                                font=('Courier New', 14, 'bold'),
                                bg=self.colors['bg_main'], fg=self.colors['accent'])
        redshift_label.pack(pady=(0, 15))
        
        # Instructions
        instruction_label = tk.Label(content_frame,
                                   text="The redshift has been applied to the spectrum.\n"
                                        "Click '✅ Accept Redshift' to confirm and close the dialog.",
                                   font=('Segoe UI', 12),
                                   bg=self.colors['bg_main'], fg=self.colors['text_secondary'],
                                   justify='center')
        instruction_label.pack(pady=(0, 20))
        
        # OK button
        ok_button = tk.Button(content_frame, text="OK",
                            command=confirmation_dialog.destroy,
                            bg=self.colors['accent'], fg='white',
                            font=('Segoe UI', 12, 'bold'),
                            relief='raised', bd=2,
                            width=10, height=1)
        ok_button.pack()
        
        # Focus the OK button and make it the default
        ok_button.focus_set()
        confirmation_dialog.bind('<Return>', lambda e: confirmation_dialog.destroy())
        confirmation_dialog.bind('<Escape>', lambda e: confirmation_dialog.destroy())
        
        # Ensure the main dialog stays on top after this dialog closes
        confirmation_dialog.protocol("WM_DELETE_WINDOW", confirmation_dialog.destroy)
        
        # Bring the main dialog back to front when this dialog closes
        def on_confirmation_close():
            confirmation_dialog.destroy()
            self.dialog.lift()  # Bring the main dialog to front
            self.dialog.focus_force()  # Force focus back to the main dialog
        
        confirmation_dialog.protocol("WM_DELETE_WINDOW", on_confirmation_close)
        ok_button.config(command=on_confirmation_close)
    
    def _create_footer(self):
        """Create footer with action buttons"""
        footer_frame = tk.Frame(self.dialog, bg=self.colors['bg_step'], height=80)  # Increased height
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        button_frame = tk.Frame(footer_frame, bg=self.colors['bg_step'])
        button_frame.pack(expand=True, pady=20)  # Increased padding
        
        # Cancel button with consistent gray color
        cancel_button = tk.Button(button_frame, text="❌ Cancel",
                                command=self._cancel,
                                bg='#64748b', fg='white',  # Consistent gray color
                                font=('Segoe UI', 12, 'bold'),  # Increased font size
                                relief='raised', bd=2,
                                width=14, height=2)  # Increased size
        cancel_button.pack(side='left', padx=15)  # Increased padding
        
        # Help button with consistent blue color
        help_button = tk.Button(button_frame, text="❓ Help",
                              command=self._show_help,
                              bg='#3b82f6', fg='white',  # Consistent blue color
                              font=('Segoe UI', 12, 'bold'),  # Increased font size
                              relief='raised', bd=2,
                              width=14, height=2)  # Increased size
        help_button.pack(side='left', padx=15)  # Increased padding
        
        # Accept button with consistent green color
        accept_button = tk.Button(button_frame, text="✅ Accept Redshift",
                                command=self._accept,
                                bg='#10b981', fg='white',  # Consistent green color
                                font=('Segoe UI', 12, 'bold'),  # Increased font size
                                relief='raised', bd=2,
                                width=18, height=2)  # Increased size
        accept_button.pack(side='right', padx=15)  # Increased padding
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """Manual Galaxy Redshift Determination Help

How to use this tool:

METHOD 1 - DIRECT INPUT (When redshift is known):
1. Enter the known redshift value in the "Direct Input" field
2. Click "Apply" or press Enter
3. Reference lines will automatically move to match
4. Accept the redshift when satisfied

METHOD 2 - INTERACTIVE ADJUSTMENT:
1. Toggle "Show Reference Lines" to activate overlay
2. Choose a focus line for the zoom window
3. Drag on the main spectrum plot to adjust redshift
4. Watch the zoom window for precise alignment
5. Accept when reference lines align with spectrum features

PRECISION MODES:
• Normal Mode: Fast adjustment (5×10⁻⁴ sensitivity)
• Precision Mode: Ultra-fine adjustment (1×10⁻⁵ sensitivity)

FOCUS LINES:
• H-α (6565 Å): Strong emission line, most reliable
• [OIII] 5007 (5008 Å): Strong emission line
• Ca II K (3934 Å): Strong galaxy absorption line

Tips:
• Use Direct Input when you know the redshift from literature
• Use Interactive mode for visual line matching
• Strong emission lines like H-α are most reliable for alignment
• The zoom window helps with precise fine-tuning
• Reference lines show expected positions at current redshift
"""
        
        messagebox.showinfo("Manual Redshift Help", help_text)
    
    def _accept(self):
        """Accept the current redshift"""
        if self.overlay_redshift <= 0:
            messagebox.showwarning("No Redshift", 
                                 "Please adjust the overlay redshift first.")
            return
        
        # Show redshift mode selection dialog
        from snid_sage.interfaces.gui.components.dialogs.redshift_mode_dialog import show_redshift_mode_dialog
        
        mode_result = show_redshift_mode_dialog(self.dialog, self.overlay_redshift)
        if mode_result is not None:
            self.result = mode_result  # This will contain both redshift and mode info
            _LOGGER.info(f"✅ Accepted redshift configuration: z = {self.overlay_redshift:.6f}, Mode: {mode_result.get('mode', 'search')}")
            self._cleanup_matplotlib()
            self.dialog.destroy()
    
    def _cancel(self):
        """Cancel the dialog"""
        self.result = None
        _LOGGER.info("❌ Manual redshift determination cancelled")
        self._cleanup_matplotlib()
        self.dialog.destroy()
    
    def _cleanup_matplotlib(self):
        """Clean up matplotlib resources to prevent memory leaks"""
        try:
            # Close any matplotlib figures
            import matplotlib.pyplot as plt
            if hasattr(self, 'figure') and self.figure:
                plt.close(self.figure)
            plt.close('all')
            
            # Clear references
            self.figure = None
            self.ax_main = None
            self.ax_zoom = None
            self.canvas = None
            
        except Exception as e:
            _LOGGER.debug(f"Cleanup warning: {e}")

    def _toggle_overlay(self):
        """Toggle overlay display"""
        self.overlay_active = not self.overlay_active
        
        if self.overlay_active:
            self.overlay_button.config(text="🔍 Hide Lines")
            _LOGGER.info("🎯 Reference lines overlay activated")
        else:
            self.overlay_button.config(text="🎯 Show Lines")
            _LOGGER.info("🎯 Reference lines overlay deactivated")
        
        # Update the plot
        self._plot_spectrum()
        self._update_redshift_display()

    def _on_mouse_press(self, event):
        """Handle mouse press events for redshift adjustment"""
        if event.button != 1:
            return
        
        # Only allow dragging on the main plot
        if event.inaxes != self.ax_main:
            return
        
        # Don't interfere with toolbar operations
        if hasattr(self.toolbar, 'mode') and self.toolbar.mode in ['zoom rect', 'pan']:
            return
        
        self.dragging = True
        self.drag_start_x = event.xdata
        self.drag_start_redshift = self.overlay_redshift
        
        # Visual feedback for drag start
        self.canvas.get_tk_widget().config(cursor='hand2')

    def _on_mouse_release(self, event):
        """Handle mouse release events for redshift adjustment"""
        if not self.dragging:
            return
        
        if event.button != 1:
            return
        
        if event.inaxes != self.ax_main:
            return
        
        self.dragging = False
        
        # Calculate sensitivity based on precision mode
        if self.precision_mode:
            sensitivity = 0.00001  # Ultra-precise: 1×10⁻⁵
        else:
            sensitivity = 0.0005   # Normal: 5×10⁻⁴ (reduced from 0.001)
        
        # Calculate new redshift
        delta_x = event.xdata - self.drag_start_x
        new_redshift = self.drag_start_redshift + (delta_x * sensitivity)
        new_redshift = max(0.0, min(2.0, new_redshift))  # Limit to 0-2
        
        self.overlay_redshift = new_redshift
        
        # Reset cursor
        self.canvas.get_tk_widget().config(cursor='')
        
        # Update the plot
        self._plot_spectrum()
        
        _LOGGER.info(f"🎯 Redshift adjusted to z = {self.overlay_redshift:.6f} [{'PRECISION' if self.precision_mode else 'NORMAL'} mode]")

    def _on_mouse_motion(self, event):
        """Handle mouse motion events for real-time redshift adjustment"""
        if not self.dragging:
            return
            
        if event.inaxes != self.ax_main:
            return
        
        # Calculate sensitivity based on precision mode
        if self.precision_mode:
            sensitivity = 0.00001  # Ultra-precise: 1×10⁻⁵
        else:
            sensitivity = 0.0005   # Normal: 5×10⁻⁴
        
        # Calculate new redshift in real-time
        delta_x = event.xdata - self.drag_start_x
        new_redshift = self.drag_start_redshift + (delta_x * sensitivity)
        new_redshift = max(0.0, min(2.0, new_redshift))  # Limit to 0-2
        
        self.overlay_redshift = new_redshift
        
        # Update the plot for real-time feedback
        self._plot_spectrum()

    def _update_identified_lines_display(self):
        """Update the identified lines display - no longer used"""
        pass  # Simplified interface doesn't need this

    def _toggle_precision_mode(self):
        """Toggle precision mode with colorful theme changes"""
        self.precision_mode = not self.precision_mode
        
        if self.precision_mode:
            self.precision_button.config(text="🔬 Precision", bg='#dc2626')  # Red for precision mode (high attention)
            _LOGGER.info("🔬 Precision mode activated - Ultra-fine sensitivity (1×10⁻⁵)")
        else:
            self.precision_button.config(text="⚡ Normal", bg='#f59e0b')  # Amber for normal mode
            _LOGGER.info("⚡ Normal mode activated - Standard sensitivity (5×10⁻⁴)")
        
        # Update the plot to show mode change
        if self.overlay_active:
            self._plot_spectrum()

    def _on_zoom_line_changed(self, *args):
        """Handle zoom line selection change (supports both event and direct-call)"""
        self.zoom_line = self.zoom_line_var.get()
        self._plot_spectrum()
        self._update_redshift_display()

    def _on_zoom_width_changed(self):
        """Handle zoom width change"""
        self.zoom_width = int(self.zoom_width_var.get())
        self._plot_spectrum()
        self._update_redshift_display()
    
    def _on_window_resize(self, event):
        """Handle window resize events to prevent plot glitches"""
        try:
            # Skip resize handling during initialization to prevent positioning issues
            if hasattr(self, '_initializing') and self._initializing:
                return
                
            # Only respond to main window resize events, not child widget events
            if event.widget == self.dialog:
                # Use after_idle to delay the layout update until after the resize is complete
                self.dialog.after_idle(self._handle_delayed_resize)
        except Exception as e:
            _LOGGER.debug(f"Window resize handler warning: {e}")
    
    def _handle_delayed_resize(self):
        """Handle delayed resize to recalculate plot layout"""
        try:
            # Only update if we have valid plot components and not initializing
            if (hasattr(self, 'canvas') and self.canvas and
                not (hasattr(self, '_initializing') and self._initializing)):
                # Force layout recalculation to prevent plot overlap
                self._force_layout_recalculation()
        except Exception as e:
            _LOGGER.debug(f"Delayed resize handler warning: {e}")


def show_manual_redshift_dialog(parent, spectrum_data: Dict[str, np.ndarray], 
                               current_redshift: float = 0.0,
                               include_auto_search: bool = False,
                               auto_search_callback=None) -> Optional[float]:
    """
    Show manual redshift dialog and return the determined redshift.
    
    Args:
        parent: Parent window
        spectrum_data: Dictionary with 'wavelength' and 'flux' arrays
        current_redshift: Current redshift estimate (if any)
        include_auto_search: Whether to include automatic search functionality
        auto_search_callback: Callback function for automatic search
        
    Returns:
        Determined redshift or None if cancelled
    """
    dialog = ManualRedshiftDialog(
        parent,
        spectrum_data,
        current_redshift,
        include_auto_search,
        auto_search_callback,
    )

    return dialog.show() 
