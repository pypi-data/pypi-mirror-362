"""
Multi-Step SN Emission Line Analysis Dialog

A modern, step-by-step workflow for supernova emission line analysis:
- Step 1: Interactive line identification and placement
- Step 2: Detailed peak analysis with FWHM measurements

Follows the design patterns of manual redshift and preprocessing dialogs.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import SpanSelector
import logging
from typing import Dict, List, Tuple, Optional, Any
import json
import datetime

# Set up logger
_LOGGER = logging.getLogger(__name__)

# Import supernova emission line constants - use the real comprehensive database
from snid_sage.shared.constants.physical import SUPERNOVA_EMISSION_LINES, SN_LINE_CATEGORIES, SPEED_OF_LIGHT_KMS

# Import line fitting utilities
from snid_sage.shared.utils.line_detection import (
    perform_line_fitting,
    is_line_in_spectrum_range,
    get_line_color,
    find_closest_line,
    add_nearby_lines,
    add_lines_by_type,
    add_lines_by_category,
    add_lines_by_origin,
    add_lines_by_strength,
    add_lines_by_type_and_phase,
    add_lines_by_phase,
    add_lines_by_name_pattern,
    add_lines_by_category_and_strength,
    add_lines_by_category_and_phase,
    add_lines_by_line_type,
    get_faint_overlay_lines,
    # Line preset functions
    get_type_ia_lines,
    get_type_ii_lines,
    get_type_ibc_lines,
    get_hydrogen_lines,
    get_helium_lines,
    get_silicon_lines,
    get_calcium_lines,
    get_oxygen_lines,
    get_iron_lines,
    get_main_galaxy_lines,
    get_strong_lines,
    get_early_type_ii,
    get_peak_type_ii,
    get_nebular_type_ii,
    get_type_iin_lines,
    get_type_iib_lines,
    get_balmer_lines,
    get_paschen_lines,
    get_halpha_only,
    get_hbeta_only,
    get_strong_hydrogen,
    get_fe_ii_lines,
    get_fe_iii_lines,
    get_early_iron,
    get_late_iron,
    get_early_sn_lines,
    get_maximum_lines,
    get_late_phase_lines,
    get_nebular_lines,
    get_diagnostic_lines,
    get_emission_lines,
    get_absorption_lines,
    get_very_strong_lines,
    get_common_lines,
    get_flash_lines,
    get_interaction_lines
)

# Import spectrum plotting utilities
from snid_sage.shared.utils.plotting import (
    plot_spectrum_with_lines,
    clear_plot_lines,
    show_faint_overlay_on_plot,
    clear_faint_overlay_from_plot,
    plot_focused_spectrum_region,
    plot_other_lines_in_range,
    plot_manual_points_with_contour,
    plot_fit_curve,
    style_spectrum_plot
)

# Enhanced interactive analysis no longer needed for simplified Step 2
INTERACTIVE_ANALYSIS_AVAILABLE = False

# Log how many lines we have available
_LOGGER.info(f"Loaded {len(SUPERNOVA_EMISSION_LINES)} emission lines for analysis")

# Import scipy for peak analysis (fallback gracefully)
try:
    from scipy import signal
    from scipy.optimize import curve_fit
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    _LOGGER.warning("scipy not available - peak analysis will be limited")


class MultiStepEmissionAnalysisDialog:
    """
    Modern two-step emission line analysis dialog
    
    Step 1: Interactive line identification and placement
    Step 2: Detailed peak analysis with FWHM measurements
    """
    
    def __init__(self, parent, spectrum_data: Dict[str, np.ndarray], theme_manager, 
                 galaxy_redshift: float = 0.0, cluster_median_redshift: float = 0.0):
        """Initialize the multi-step emission line analysis dialog"""
        self.parent = parent
        self.spectrum_data = spectrum_data
        self.theme_manager = theme_manager
        
        # Step management
        self.current_step = 1
        self.total_steps = 2
        self.step_names = [
            "Line Identification & Placement",
            "Peak Analysis & FWHM Measurement"
        ]
        
        # Data storage
        self.base_redshift = galaxy_redshift
        self.velocity_shift = 0.0
        self.current_redshift = cluster_median_redshift  # Start with SN redshift as working redshift
        self.cluster_median_redshift = cluster_median_redshift
        
        # Step 1 data - line selections
        self.sn_lines = {}  # line_name -> (observed_wavelength, line_data)
        self.galaxy_lines = {}
        self.line_history = []  # Track line addition history
        self.line_sources = {}  # line_name -> source_action mapping
        
        # Step 2 data - analysis results (legacy)
        self.selected_lines_for_analysis = set()  # Lines selected for analysis (legacy)
        self.line_measurements = {}  # line_name -> measurement_dict (legacy)
        self.analysis_parameters = {
            'method': 'auto',
            'baseline': 'auto',
            'sn_threshold': 5.0
        }
        
        # Step 2 new focused system
        self.available_lines = []  # List of line names available for analysis
        self.current_line_index = 0  # Index of currently selected line
        self.line_analysis_results = {}  # line_name -> result_text
        self.selected_manual_points = []  # Manual points for current line
        self.line_fit_results = {}  # line_name -> fit_data (params, curve, etc.)
        
        # UI state
        self.current_mode = 'sn'  # 'sn' or 'galaxy'
        self.dialog = None
        self.result = None
        
        # Plot components
        self.figure = None
        self.ax_main = None
        self.canvas = None
        self.toolbar = None
        self.line_artists = {}  # Store line and text artists
        
        # Simplified analysis system - no complex interactive components needed
        self.manual_selection_controller = None
        
        # UI variables
        self._updating_fields = False
        self.shift_pressed = False
        self.faint_line_artists = {}
        
        # Modern color scheme matching other dialogs
        self.colors = {
            'bg_main': theme_manager.get_color('bg_primary'),
            'bg_panel': theme_manager.get_color('bg_secondary'), 
            'bg_step': theme_manager.get_color('bg_tertiary'),
            'bg_control': theme_manager.get_color('bg_tertiary'),
            'bg_step_active': theme_manager.get_color('accent_primary'),
            'bg_current': theme_manager.get_color('accent_primary'),
            'button_bg': theme_manager.get_color('bg_tertiary'),
            'button_inactive': theme_manager.get_color('text_muted'),
            'button_active': theme_manager.get_color('accent_primary'),
            'text_primary': theme_manager.get_color('text_primary'),
            'text_secondary': theme_manager.get_color('text_secondary'),
            'accent': theme_manager.get_color('accent_primary'),
            'success': theme_manager.get_color('btn_success'),
            'warning': theme_manager.get_color('btn_warning'),
            'error': theme_manager.get_color('btn_danger'),
            'disabled': theme_manager.get_color('disabled')
        }
        
        _LOGGER.info("Multi-step emission analysis dialog initialized")
    
    def _update_status(self, message: str):
        """Update status message for interactive tools"""
        # For now, just log the message. Could be enhanced with a status bar
        _LOGGER.debug(f"Status: {message}")
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Show the dialog and return the results"""
        self._create_dialog()
        self._setup_interface()
        self._create_plots()
        self._update_step_display()
        
        # Calculate initial working redshift
        self._update_total_redshift()
        
        # Center and show dialog
        self._center_dialog()
        self.dialog.grab_set()
        self.dialog.wait_window()
        
        return self.result
    
    def _create_dialog(self):
        """Create the main dialog window"""
        # Determine proper Tkinter parent widget
        if hasattr(self.parent, 'tk'):
            parent_widget = self.parent
        elif hasattr(self.parent, 'master') and hasattr(self.parent.master, 'tk'):
            parent_widget = self.parent.master
        else:
            parent_widget = None  # Fallback to default root

        if parent_widget is not None:
            self.dialog = tk.Toplevel(parent_widget)
        else:
            self.dialog = tk.Toplevel()
        self.dialog.title("🔍 Line Analysis")
        self.dialog.geometry("1600x1000")
        self.dialog.resizable(True, True)
        self.dialog.minsize(1400, 900)
        
        # Apply background color
        self.dialog.configure(bg=self.colors['bg_main'])
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
        
        # Enable keyboard focus
        self.dialog.focus_set()
    
    def _center_dialog(self):
        """Center dialog on parent"""
        self.dialog.update_idletasks()
        
        try:
            # Center on parent window
            if hasattr(self.parent, 'master') and self.parent.master:
                parent_widget = self.parent.master
            else:
                parent_widget = self.parent
                
            x = parent_widget.winfo_x() + (parent_widget.winfo_width() // 2) - (1600 // 2)
            y = parent_widget.winfo_y() + (parent_widget.winfo_height() // 2) - (1000 // 2)
            self.dialog.geometry(f"1600x1000+{x}+{y}")
            
        except (AttributeError, tk.TclError):
            # Fallback: center on screen
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width // 2) - (1600 // 2)
            y = (screen_height // 2) - (1000 // 2)
            self.dialog.geometry(f"1600x1000+{x}+{y}")
    
    def _setup_interface(self):
        """Setup the dialog interface"""
        # Header with step indicator
        self._create_header()
        
        # Main content with split panel layout
        self._create_split_panel_layout()
        
        # Footer with navigation buttons
        self._create_footer()
    
    def _create_header(self):
        """Create header section with step indicator"""
        header_frame = tk.Frame(self.dialog, bg=self.colors['accent'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        content_frame = tk.Frame(header_frame, bg=self.colors['accent'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Title and step indicator
        title_frame = tk.Frame(content_frame, bg=self.colors['accent'])
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text="🔍 Line Analysis",
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.colors['accent'], fg='white')
        title_label.pack(side='left')
        
        # Step indicator on the right
        self.step_indicator = tk.Label(title_frame, 
                                 text=f"Step {self.current_step} of {self.total_steps}",
                                 font=('Segoe UI', 14, 'bold'),
                                 bg=self.colors['accent'], fg='#e0f2fe')
        self.step_indicator.pack(side='right')
        
        # Subtitle with current step description
        self.subtitle_label = tk.Label(content_frame, 
                                      text=self.step_names[self.current_step - 1],
                                      font=('Segoe UI', 12),
                                      bg=self.colors['accent'], fg='#e0f2fe')
        self.subtitle_label.pack(pady=(5, 0))
    
    def _create_split_panel_layout(self):
        """Create the main split-panel layout"""
        # Main container
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create left and right panels with percentage-based widths for Step 2
        if self.current_step == 2:
            # Step 2: Left panel gets 35% width for better readability
            left_panel_width = int(1600 * 0.35)  # 35% of dialog width
            self.left_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], width=left_panel_width, relief='raised', bd=1)
            self.left_panel.pack(side='left', fill='y', padx=(0, 5))
            self.left_panel.pack_propagate(False)
        else:
            # Step 1: Keep original fixed width
            self.left_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], width=320, relief='raised', bd=1)
            self.left_panel.pack(side='left', fill='y', padx=(0, 5))
            self.left_panel.pack_propagate(False)
        
        self.right_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], relief='raised', bd=1)
        self.right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Initialize panels (will be populated based on current step)
        self._create_left_panel()
        self._create_right_panel()
    
    def _create_left_panel(self):
        """Create the left control panel"""
        # Clear existing content
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        
        # Options area
        self.options_frame = tk.Frame(self.left_panel, bg=self.colors['bg_panel'])
        self.options_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Populate based on current step
        if self.current_step == 1:
            self._create_step1_options()
        elif self.current_step == 2:
            self._create_step2_options()
    
    def _create_right_panel(self):
        """Create the right visualization panel"""
        # Clear existing content
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Header
        viz_header = tk.Frame(self.right_panel, bg=self.colors['bg_panel'])
        viz_header.pack(fill='x', padx=15, pady=(15, 10))
        
        if self.current_step == 1:
            title_text = "📈 Interactive Spectrum Plot"
            subtitle_text = "Click on spectrum features to identify emission lines"
        else:
            title_text = "📊 Peak Analysis Results"
            subtitle_text = "FWHM measurements and line fitting results"
        
        title_label = tk.Label(viz_header, text=title_text, 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(viz_header, text=subtitle_text,
                                 font=('Segoe UI', 11),
                                 bg=self.colors['bg_panel'], fg=self.colors['text_secondary'])
        subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # Plot container
        self.plot_frame = tk.Frame(self.right_panel, bg=self.colors['bg_panel'])
        self.plot_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
    
    def _create_plots(self):
        """Create matplotlib plots in the plot frame"""
        if self.current_step == 1:
            self._create_step1_plot()
        elif self.current_step == 2:
            self._create_step2_plot()
        
        # Interactive tools no longer needed for simplified Step 2
        pass
    
    def _create_footer(self):
        """Create footer with navigation buttons"""
        footer_frame = tk.Frame(self.dialog, bg=self.colors['bg_step'], height=80)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        button_frame = tk.Frame(footer_frame, bg=self.colors['bg_step'])
        button_frame.pack(expand=True, pady=20)
        
        # Cancel button
        cancel_button = tk.Button(button_frame, text="❌ Cancel",
                                command=self._cancel,
                                bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 12, 'bold'),
                                relief='raised', bd=2,
                                width=14, height=2)
        cancel_button.pack(side='left', padx=15)
        
        # Help button in the center
        help_button = tk.Button(button_frame, text="❓ Help",
                               command=self._show_help,
                               bg=self.colors['accent'], fg='white',
                               font=('Segoe UI', 12, 'bold'),
                               relief='raised', bd=2,
                               width=14, height=2)
        help_button.pack(side='left', padx=15)
        
        # Navigation buttons (will be updated based on step)
        self.nav_frame = tk.Frame(button_frame, bg=self.colors['bg_step'])
        self.nav_frame.pack(side='right', padx=15)
        
        self._update_navigation_buttons()
    
    def _update_navigation_buttons(self):
        """Update navigation buttons based on current step"""
        # Clear existing navigation buttons
        for widget in self.nav_frame.winfo_children():
            widget.destroy()
        
        if self.current_step == 1:
            # Step 1: Continue to peak analysis
            continue_button = tk.Button(self.nav_frame, text="🔬 Peak Analysis →",
                                      command=self._proceed_to_step2,
                                      bg=self.colors['success'], fg='white',
                                      font=('Segoe UI', 12, 'bold'),
                                      relief='raised', bd=2,
                                      width=20, height=2)
            continue_button.pack()
            
        elif self.current_step == 2:
            # Step 2: Back and finish buttons
            back_button = tk.Button(self.nav_frame, text="← Line Selection",
                                  command=self._return_to_step1,
                                  bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                  font=('Segoe UI', 12, 'bold'),
                                  relief='raised', bd=2,
                                  width=16, height=2)
            back_button.pack(side='left', padx=(0, 10))
            
            finish_button = tk.Button(self.nav_frame, text="✅ Finish Analysis",
                                    command=self._finish_analysis,
                                    bg=self.colors['accent'], fg='white',
                                    font=('Segoe UI', 12, 'bold'),
                                    relief='raised', bd=2,
                                    width=18, height=2)
            finish_button.pack(side='right')
    
    def _update_step_display(self):
        """Update the display for the current step"""
        # Update header
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.configure(text=self.step_names[self.current_step - 1])
        
        # Update step indicator in header
        if hasattr(self, 'step_indicator'):
            self.step_indicator.configure(text=f"Step {self.current_step} of {self.total_steps}")
        
        # Update panels
        self._create_left_panel()
        self._create_right_panel()
        self._create_plots()
        
        # Update navigation
        self._update_navigation_buttons()
        
        _LOGGER.info(f"Updated to step {self.current_step}: {self.step_names[self.current_step - 1]}")
    
    # Navigation methods
    def _proceed_to_step2(self):
        """Proceed from Step 1 to Step 2 - Focused Line Analysis"""
        # Validate that we have some lines selected
        total_lines = len(self.sn_lines) + len(self.galaxy_lines)
        if total_lines == 0:
            messagebox.showwarning("No Lines Selected", 
                                 "Please select some emission lines before proceeding to focused analysis.\n\n"
                                 "Click on spectrum features or use the quick presets to add lines.")
            return
        
        # Clear any faint overlay before switching
        self._clear_faint_overlay()
        
        # Note: Button is now in the left panel, no cleanup needed
        
        # Move to step 2
        self.current_step = 2
        
        # Reset single-line focused system for new analysis
        self.available_lines = []
        self.current_line_index = 0
        self.line_analysis_results.clear()
        self.line_fit_results.clear()
        self.selected_manual_points.clear()
        
        # Update display
        self._update_step_display()
        
        _LOGGER.info(f"Proceeded to Step 2: Focused Line Analysis with {total_lines} lines available")
    
    def _return_to_step1(self):
        """Return from Step 2 to Step 1"""
        # Note: Button is now in the left panel, no cleanup needed
        
        # Preserve analysis selections and results
        self.current_step = 1
        self._update_step_display()
        _LOGGER.info("Returned to Step 1")
    
    def _finish_analysis(self):
        """Finish the analysis and return results"""
        # Compile final results
        self.result = {
            'selected_lines': {
                'sn_lines': self.sn_lines,
                'galaxy_lines': self.galaxy_lines
            },
            'redshift_info': {
                'base_redshift': self.base_redshift,
                'velocity_shift': self.velocity_shift,
                'total_redshift': self.current_redshift
            },
            'analysis_results': self.line_measurements,
            'analysis_parameters': self.analysis_parameters,
            'selected_for_analysis': list(self.selected_lines_for_analysis)
        }
        
        _LOGGER.info(f"Finished analysis with {len(self.line_measurements)} measured lines")
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel the dialog"""
        # Clear any faint overlay
        self._clear_faint_overlay()
        
        self.result = None
        _LOGGER.info("❌ Multi-step emission analysis cancelled")
        self.dialog.destroy()
    
    def _show_help(self):
        """Show comprehensive help dialog explaining all features"""
        help_text = """🔍 LINE ANALYSIS - COMPREHENSIVE HELP

This dialog provides a two-step workflow for analyzing supernova emission lines:

═══════════════════════════════════════════════════════════════════════════════
STEP 1: LINE IDENTIFICATION & PLACEMENT
═══════════════════════════════════════════════════════════════════════════════

🌍 REDSHIFT CONTROLS:
• Host z: Enter the host galaxy redshift (if known)
• vₑₓₚ: Ejecta velocity offset in km/s (±50,000 km/s max)
• The working redshift combines SN redshift + ejecta velocity effect
• Lines are automatically positioned based on the working redshift

🎯 LINE SELECTION MODE:
• 🌟 SN Lines: Add supernova-specific emission lines
• 🌌 Galaxy Lines: Add host galaxy emission lines
• Switch between modes to organize your line selections

⚡ QUICK LINE PRESETS:
• Type Ia/II/Ib/c Lines: Common supernova type lines
• Element Shortcuts: Hydrogen, Helium, Iron, Silicon, etc.
• Phase Shortcuts: Early, Maximum, Late, Nebular phases
• Strength Shortcuts: Very Strong, Strong, Common lines
• Special Shortcuts: Flash ionization, Interaction lines

📋 ADDED LINES TRACKER:
• Shows all selected lines with their sources
• 🌟 = SN lines, 🌌 = Galaxy lines
• Right-click to remove selected lines
• Clear All button to start fresh

INTERACTIVE SPECTRUM PLOT:
• Double-click on spectrum: Add nearby emission lines
• Right-click: Remove closest line
• Hold Shift: Show all available lines as faint overlay
• Lines are color-coded and positioned at observed wavelengths

═══════════════════════════════════════════════════════════════════════════════
STEP 2: PEAK ANALYSIS & FWHM MEASUREMENT
═══════════════════════════════════════════════════════════════════════════════

🎯 CURRENT LINE ANALYSIS:
• Dropdown menu to select specific lines for detailed analysis
• Previous/Next buttons to navigate between lines
• Line counter shows current position

🔍 ZOOM & ANALYSIS CONTROLS:
• Zoom Range: Set wavelength range around line (±15Å, ±30Å, ±50Å, Full)
• Analysis Method:
  - Auto Detection: Automatic peak finding and fitting
  - Gaussian Fit: Fit Gaussian curve to line profile
  - Empirical Analysis: Statistical analysis of line properties
  - Manual Points: Click to define peak contour manually

📊 CURRENT LINE ANALYSIS:
• 🔬 Analyze Current Line: Perform analysis on selected line
• Manual Selection Controls (for Manual Points mode):
  - Clear Points: Remove all manual selections
  - Auto Contour: Automatically detect peak boundaries
  - Point counter shows number of selected points

MANUAL POINT SELECTION (Manual Points mode):
• Left Click: Smart peak detection on spectrum
• Ctrl+Click: Add free-floating point anywhere
• Shift+Click: Add point snapped to spectrum curve
• Right Click: Remove closest point
• Auto Contour: Automatically detect peak boundaries

📋 ALL LINES SUMMARY:
• Shows analysis results for all lines
• Copy Summary: Copy results to clipboard
• Refresh: Update summary display

═══════════════════════════════════════════════════════════════════════════════
KEYBOARD SHORTCUTS & INTERACTIONS
═══════════════════════════════════════════════════════════════════════════════

STEP 1:
• Double-click spectrum: Add nearby lines
• Right-click spectrum: Remove closest line
• Hold Shift: Show all available lines as overlay
• Enter in redshift/velocity fields: Apply changes

STEP 2:
• Enter in zoom field: Apply zoom range
• Ctrl+Click: Add free-floating point (Manual Points mode)
• Shift+Click: Add spectrum-snapped point (Manual Points mode)
• Right-click: Remove closest point (Manual Points mode)

═══════════════════════════════════════════════════════════════════════════════
"""
        
        # Create help dialog
        help_dialog = tk.Toplevel(self.dialog)
        help_dialog.title("❓ Line Analysis Help")
        help_dialog.geometry("800x700")
        help_dialog.resizable(True, True)
        help_dialog.configure(bg=self.colors['bg_main'])
        
        # Make it modal
        help_dialog.transient(self.dialog)
        help_dialog.grab_set()
        
        # Center on parent
        help_dialog.update_idletasks()
        x = self.dialog.winfo_x() + (self.dialog.winfo_width() // 2) - (800 // 2)
        y = self.dialog.winfo_y() + (self.dialog.winfo_height() // 2) - (700 // 2)
        help_dialog.geometry(f"800x700+{x}+{y}")
        
        # Create scrollable text widget
        main_frame = tk.Frame(help_dialog, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="❓ Line Analysis Help",
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg_main'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 10))
        
        # Text widget with scrollbar
        text_frame = tk.Frame(main_frame, bg=self.colors['bg_main'])
        text_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        help_text_widget = tk.Text(text_frame, 
                                  yscrollcommand=scrollbar.set,
                                  bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                  font=('Consolas', 16), wrap='word',
                                  padx=10, pady=10)
        help_text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=help_text_widget.yview)
        
        # Insert help text
        help_text_widget.insert('1.0', help_text)
        help_text_widget.config(state='disabled')  # Make read-only
        
        # Close button
        close_button = tk.Button(main_frame, text="✅ Close Help",
                                command=help_dialog.destroy,
                                bg=self.colors['success'], fg='white',
                                font=('Segoe UI', 12, 'bold'),
                                relief='raised', bd=2,
                                width=15, height=2)
        close_button.pack(pady=10)
        
        # Focus on help dialog
        help_dialog.focus_set()
    
    # ==========================================
    # STEP 1 IMPLEMENTATION: Line Identification
    # ==========================================
    
    def _create_step1_options(self):
        """Create Step 1 options for line identification"""
        # 1. REDSHIFT CONTROLS - Three specific fields (moved to top)
        redshift_frame = tk.LabelFrame(self.options_frame, text="🌍 Redshift Controls", 
                                      bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                      font=('Segoe UI', 16, 'bold'))
        redshift_frame.pack(fill='x', pady=(0, 15))
        
        # Initialize redshift variables with source tracking
        self.galaxy_redshift_var = tk.StringVar()
        self.sn_redshift_var = tk.StringVar(value=f"{self.cluster_median_redshift:.6f}")
        self.wind_velocity_var = tk.StringVar(value="0")
        
        # Track redshift sources
        self.galaxy_redshift_source = "Not set"
        self.sn_redshift_source = "Unknown"
        
        # Determine galaxy redshift source and value
        if self.base_redshift > 0.0001:  # Only populate if significant redshift was provided
            self.galaxy_redshift_var.set(f"{self.base_redshift:.6f}")
            # Check if this came from manual redshift specification
            if hasattr(self.parent, 'galaxy_redshift_result') and self.parent.galaxy_redshift_result:
                if self.parent.galaxy_redshift_result.get('method') == 'manual':
                    self.galaxy_redshift_source = "Manual redshift specification"
                elif self.parent.galaxy_redshift_result.get('method') == 'auto':
                    self.galaxy_redshift_source = f"Auto-detected (RLAP {self.parent.galaxy_redshift_result.get('rlap', 0):.1f})"
                else:
                    self.galaxy_redshift_source = "User specified"
            else:
                self.galaxy_redshift_source = "User specified"
        else:
            self.galaxy_redshift_var.set("")  # Empty if no redshift set
            self.galaxy_redshift_source = "Not set"
        
        # Determine SN redshift source - get from winning cluster's weighted redshift
        if hasattr(self.parent, 'snid_results') and self.parent.snid_results:
            # Try to get the weighted redshift from winning cluster
            if (hasattr(self.parent.snid_results, 'clustering_results') and 
                self.parent.snid_results.clustering_results and
                self.parent.snid_results.clustering_results.get('success')):
                
                clustering_results = self.parent.snid_results.clustering_results
                winning_cluster = None
                
                # Priority: user_selected_cluster > best_cluster
                if 'user_selected_cluster' in clustering_results:
                    winning_cluster = clustering_results['user_selected_cluster']
                    self.sn_redshift_source = "User-selected cluster (weighted)"
                elif 'best_cluster' in clustering_results:
                    winning_cluster = clustering_results['best_cluster']
                    self.sn_redshift_source = "Best cluster (weighted)"
                
                if winning_cluster:
                    # Use the enhanced/weighted redshift from the cluster
                    weighted_z = winning_cluster.get('enhanced_redshift', 
                                                   winning_cluster.get('weighted_mean_redshift', 
                                                                     self.cluster_median_redshift))
                    self.cluster_median_redshift = weighted_z
                    self.sn_redshift_var.set(f"{weighted_z:.6f}")
                    _LOGGER.info(f"Using weighted cluster redshift: {weighted_z:.6f} from {self.sn_redshift_source}")
                else:
                    self.sn_redshift_source = "Best match (no clustering)"
            else:
                self.sn_redshift_source = "Best match"
        else:
            self.sn_redshift_source = "Default"
        
        # Create main redshift info frame
        main_redshift_frame = tk.Frame(redshift_frame, bg=self.colors['bg_step'])
        main_redshift_frame.pack(fill='both', padx=15, pady=(10, 5))
        
        # Single redshift field for galaxy/host
        redshift_input_frame = tk.Frame(main_redshift_frame, bg=self.colors['bg_step'])
        redshift_input_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(redshift_input_frame, text="Host z:",
                bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                font=('Segoe UI', 14, 'bold')).pack(side='left', padx=(0, 10))
        
        self.galaxy_redshift_entry = tk.Entry(redshift_input_frame, textvariable=self.galaxy_redshift_var,
                                            font=('Courier New', 14), width=10,
                                            bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                            insertbackground=self.colors['text_primary'])
        self.galaxy_redshift_entry.pack(side='left', padx=(0, 10))
        
        # Redshift source info label
        self.redshift_source_label = tk.Label(redshift_input_frame, 
                                            text=f"({self.galaxy_redshift_source})",
                                            bg=self.colors['bg_step'], 
                                            fg=self.colors['text_secondary'],
                                            font=('Segoe UI', 11, 'italic'))
        self.redshift_source_label.pack(side='left')
        
        # Ejecta velocity field with improved label
        velocity_frame = tk.Frame(main_redshift_frame, bg=self.colors['bg_step'])
        velocity_frame.pack(fill='x', pady=(0, 10))
        
        # Velocity label: vₑₓₚ  (v with subscript 'exp')
        tk.Label(velocity_frame, text="vₑₓₚ =",
                bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                font=('Segoe UI', 14, 'bold')).pack(side='left', padx=(0, 10))
        
        self.wind_velocity_entry = tk.Entry(velocity_frame, textvariable=self.wind_velocity_var,
                                          font=('Courier New', 14), width=8,
                                          bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                          insertbackground=self.colors['text_primary'])
        self.wind_velocity_entry.pack(side='left', padx=(0, 5))
        
        tk.Label(velocity_frame, text="km/s",
                bg=self.colors['bg_step'], fg=self.colors['text_secondary'],
                font=('Segoe UI', 12)).pack(side='left')
        
        # Explanatory label showing redshift source and hint about ejecta shift
        self.redshift_info_label = tk.Label(main_redshift_frame,
                                          text="",
                                          bg=self.colors['bg_step'],
                                          fg=self.colors['text_secondary'],
                                          font=('Segoe UI', 10, 'italic'),
                                          wraplength=280,  # Wrap text to fit in window
                                          justify='left')
        self.redshift_info_label.pack(fill='x', padx=5, pady=(10, 5))
        self._update_redshift_source_display()
        
        # Hide detailed SN/working redshift frames (retain objects for backend calculations)
        try:
            sn_info_frame.pack_forget()
            working_info_frame.pack_forget()
        except:
            pass
        
        # Store hidden labels for internal updates
        self.sn_redshift_label = tk.Label()
        self.working_redshift_label = tk.Label()
        
        # Bind real-time updates for redshift and velocity changes
        self.galaxy_redshift_var.trace('w', self._on_galaxy_redshift_change)
        self.wind_velocity_var.trace('w', self._on_wind_velocity_change)
        
        # 2. LINE SELECTION MODE (moved below redshift controls)
        mode_frame = tk.LabelFrame(self.options_frame, text="🎯 Line Selection Mode", 
                                 bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                 font=('Segoe UI', 16, 'bold'))
        mode_frame.pack(fill='x', pady=(0, 15))
        
        # Mode selection buttons
        mode_buttons_frame = tk.Frame(mode_frame, bg=self.colors['bg_step'])
        mode_buttons_frame.pack(padx=15, pady=15)
        
        self.sn_button = tk.Button(mode_buttons_frame, text="🌟 SN Lines",
                                  command=self._set_sn_mode,
                                  font=('Segoe UI', 13, 'bold'), 
                                  bg=self.colors['button_active'], fg='white',
                                  relief='raised', bd=2, width=15, height=1)
        self.sn_button.pack(side='left', padx=(0, 5))
        
        self.galaxy_button = tk.Button(mode_buttons_frame, text="🌌 Galaxy Lines",
                                      command=self._set_galaxy_mode,
                                      font=('Segoe UI', 13, 'bold'),
                                      bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                      relief='raised', bd=2, width=15, height=1)
        self.galaxy_button.pack(side='left')
        
        # 3. QUICK LINE PRESETS
        presets_frame = tk.LabelFrame(self.options_frame, text="⚡ Quick Line Presets", 
                                    bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 16, 'bold'))
        presets_frame.pack(fill='x', pady=(0, 15))
        
        # Advanced preset system with submenus
        preset_control_frame = tk.Frame(presets_frame, bg=self.colors['bg_step'])
        preset_control_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(preset_control_frame, text="Quick Line Selection:",
                bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 5))
        
        # Create custom dropdown button with submenu support
        self.current_selection = "Choose preset..."
        self.shortcuts_button = tk.Button(preset_control_frame, text=self.current_selection,
                                        font=('Segoe UI', 13), width=28,
                                        bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                        relief='raised', bd=1, anchor='w',
                                        command=self._show_main_dropdown)
        self.shortcuts_button.pack(fill='x', pady=(0, 5))
        
        # Define shortcut options with submenu structure
        self.shortcut_options = {
            "Choose preset...": [],
            "─── SN Type Shortcuts ───": [],
            "Type Ia Lines ►": self._get_type_ia_lines,
            "Type II Lines ►": self._show_type_ii_submenu,
            "Type Ib/c Lines ►": self._get_type_ibc_lines,
            "Early SN Lines": self._get_early_sn_lines,
            "Maximum Light Lines": self._get_maximum_lines,
            "Late Phase Lines": self._get_late_phase_lines,
            "Nebular Lines": self._get_nebular_lines,
            "─── Element Shortcuts ───": [],
            "Hydrogen Lines ►": self._show_hydrogen_submenu,
            "Helium Lines": self._get_helium_lines,
            "Silicon Lines": self._get_silicon_lines,
            "Iron Lines ►": self._show_iron_submenu,
            "Calcium Lines": self._get_calcium_lines,
            "Oxygen Lines": self._get_oxygen_lines,
            "─── Galaxy Shortcuts ───": [],
            "Main Galaxy Lines": self._get_main_galaxy_lines,
            "Diagnostic Lines": self._get_diagnostic_lines,
            "Emission Lines": self._get_emission_lines,
            "Absorption Lines": self._get_absorption_lines,
            "─── Strength Shortcuts ───": [],
            "Very Strong Lines": self._get_very_strong_lines,
            "Strong Lines": self._get_strong_lines,
            "All Common Lines": self._get_common_lines,
            "─── Special Shortcuts ───": [],
            "Flash Ionization": self._get_flash_lines,
            "Interaction Lines": self._get_interaction_lines,
            "Clear All Lines": self._clear_all_lines
        }
        
        # Type II submenus
        self.type_ii_options = {
            "All Type II Lines": self._get_type_ii_lines,
            "Early Type II": self._get_early_type_ii,
            "Peak Type II": self._get_peak_type_ii,
            "Nebular Type II": self._get_nebular_type_ii,
            "Type IIn (Narrow)": self._get_type_iin_lines,
            "Type IIb (Broad)": self._get_type_iib_lines
        }
        
        # Hydrogen submenus 
        self.hydrogen_options = {
            "All Hydrogen Lines": self._get_hydrogen_lines,
            "Balmer Series": self._get_balmer_lines,
            "Paschen Series": self._get_paschen_lines,
            "H-alpha Only": self._get_halpha_only,
            "H-beta Only": self._get_hbeta_only,
            "Strong H Lines": self._get_strong_hydrogen
        }
        
        # Iron submenus
        self.iron_options = {
            "All Iron Lines": self._get_iron_lines,
            "Fe II Lines": self._get_fe_ii_lines,
            "Fe III Lines": self._get_fe_iii_lines,
            "Early Fe Lines": self._get_early_iron,
            "Late Fe Lines": self._get_late_iron
        }
        
        # 4. ADDED LINES TRACKER
        tracker_frame = tk.LabelFrame(self.options_frame, text="📋 Added Lines Tracker", 
                                    bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 16, 'bold'))
        tracker_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Tracking list with scrollbar
        tracker_list_frame = tk.Frame(tracker_frame, bg=self.colors['bg_step'])
        tracker_list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        tracker_scrollbar = tk.Scrollbar(tracker_list_frame, bg=self.colors['bg_step'])
        tracker_scrollbar.pack(side='right', fill='y')
        
        # Listbox
        self.tracker_listbox = tk.Listbox(tracker_list_frame, 
                                        yscrollcommand=tracker_scrollbar.set,
                                        bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                        font=('Consolas', 12), selectmode='extended',
                                        height=8)
        self.tracker_listbox.pack(side='left', fill='both', expand=True)
        tracker_scrollbar.config(command=self.tracker_listbox.yview)
        
        # Tracker control buttons
        tracker_buttons_frame = tk.Frame(tracker_frame, bg=self.colors['bg_step'])
        tracker_buttons_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        remove_button = tk.Button(tracker_buttons_frame, text="🗑️ Remove",
                                command=self._remove_selected_from_tracker,
                                bg=self.colors['error'], fg='white',
                                font=('Segoe UI', 12, 'bold'),
                                relief='raised', bd=2, width=15)
        remove_button.pack(side='left', padx=(0, 5))
        
        clear_button = tk.Button(tracker_buttons_frame, text="Clear All",
                               command=self._clear_all_lines,
                               bg=self.colors['warning'], fg='white',
                               font=('Segoe UI', 12, 'bold'),
                               relief='raised', bd=2, width=15)
        clear_button.pack(side='right')
        
        # Status display
        self.status_frame = tk.Frame(self.options_frame, bg=self.colors['bg_step'], relief='sunken', bd=1)
        self.status_frame.pack(fill='x')
        
        self.status_label = tk.Label(self.status_frame, 
                                   text="Mode: SN Lines | Selected: 0 SN, 0 Galaxy | Double-click: Add | Right-click: Remove | Hold Shift: Show All",
                                   font=('Segoe UI', 12),
                                   bg=self.colors['bg_step'], fg=self.colors['text_secondary'])
        self.status_label.pack(pady=5)
    
    def _create_step1_plot(self):
        """Create the interactive spectrum plot for Step 1"""
        # Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Create matplotlib figure with optimized layout
        self.figure = plt.figure(figsize=(16, 8), dpi=150)
        self.figure.patch.set_facecolor('white')
        
        # Use balanced layout - not too tight to avoid cutting labels
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.12)
        
        # Single main plot
        self.ax_main = self.figure.add_subplot(111)
        self.ax_main.set_facecolor('white')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=2, pady=2)
        
        # Add navigation toolbar (without analyze button for Step 1)
        toolbar_frame = tk.Frame(self.plot_frame, bg=self.colors['bg_panel'])
        toolbar_frame.pack(fill='x', pady=(2, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        self.toolbar.config(bg=self.colors['bg_panel'])
        
        # Connect click events
        self.canvas.mpl_connect('button_press_event', self._on_plot_click)
        self.canvas.mpl_connect('motion_notify_event', self._on_plot_hover)
        self.canvas.mpl_connect('key_press_event', self._on_key_press)
        self.canvas.mpl_connect('key_release_event', self._on_key_release)
        
        # Enable keyboard focus for the canvas
        self.canvas.get_tk_widget().focus_set()
        
        # Plot the spectrum
        self._plot_spectrum()
        
        # Apply tight layout with more generous padding
        try:
            self.figure.tight_layout(pad=1.5)
        except Exception as e:
            _LOGGER.debug(f"Tight layout warning: {e}")
        
        self.canvas.draw()
    
    def _plot_spectrum(self):
        """Plot the spectrum data"""
        if not self.spectrum_data or 'wavelength' not in self.spectrum_data or 'flux' not in self.spectrum_data:
            return
        
        # Clear the plot
        self.ax_main.clear()
        
        # Plot spectrum (keep in observed wavelengths - lines will be redshifted to match)
        wavelength = self.spectrum_data['wavelength']
        flux = self.spectrum_data['flux']
        
        self.ax_main.plot(wavelength, flux, 'k-', linewidth=1, alpha=0.8)
        
        # Set labels and styling for white background
        self.ax_main.set_xlabel('Wavelength (Å)', color='black', fontsize=12)
        self.ax_main.set_ylabel('Flux', color='black', fontsize=12)
        self.ax_main.tick_params(colors='black')
        self.ax_main.grid(True, alpha=0.3, color='gray')
        
        # Update line overlays
        self._update_plot_lines()
        
        # Apply tight layout and refresh canvas
        try:
            self.figure.tight_layout(pad=1.5)
        except Exception as e:
            _LOGGER.debug(f"Tight layout warning: {e}")
        
        self.canvas.draw()
    
    def _update_plot_lines(self):
        """Update line overlays on the plot"""
        # Clear existing lines
        clear_plot_lines(self.ax_main)
        
        # Plot spectrum with lines using imported utility
        plot_spectrum_with_lines(self.ax_main, self.spectrum_data, self.sn_lines, self.galaxy_lines)
        
        # Refresh canvas
        if hasattr(self, 'canvas'):
            self.canvas.draw()
    
    # Step 1 Event Handlers
    def _set_sn_mode(self):
        """Switch to SN line selection mode"""
        self.current_mode = 'sn'
        self.sn_button.configure(bg=self.colors['button_active'], fg='white')
        self.galaxy_button.configure(bg=self.colors['button_inactive'], fg='white')
        self._update_status()
        _LOGGER.info("Switched to SN line selection mode")
    
    def _set_galaxy_mode(self):
        """Switch to galaxy line selection mode"""
        self.current_mode = 'galaxy'
        self.galaxy_button.configure(bg=self.colors['button_active'], fg='white')
        self.sn_button.configure(bg=self.colors['button_inactive'], fg='white')
        self._update_status()
        _LOGGER.info("Switched to galaxy line selection mode")
    
    def _update_status(self):
        """Update status label"""
        mode_text = "SN Lines" if self.current_mode == 'sn' else "Galaxy Lines"
        sn_count = len(self.sn_lines)
        galaxy_count = len(self.galaxy_lines)
        
        status_text = f"Mode: {mode_text} | Selected: {sn_count} SN, {galaxy_count} Galaxy | Double-click: Add | Right-click: Remove | Hold Shift: Show All"
        self.status_label.configure(text=status_text)
        
        # Update tracker display
        self._update_tracking_display()
    
    def _on_galaxy_redshift_change(self, *args):
        """Handle real-time galaxy redshift changes"""
        if self._updating_fields:
            return
        
        try:
            redshift_str = self.galaxy_redshift_var.get()
            if not redshift_str:
                # If galaxy redshift is cleared, update source label
                self.redshift_source_label.configure(text="(Not set)")
                self.galaxy_redshift_source = "Not set"
                return
                
            new_base_redshift = float(redshift_str)
            if new_base_redshift < 0:
                # Reset to 0 if negative
                self._updating_fields = True
                self.galaxy_redshift_var.set("0.000000")
                self._updating_fields = False
                new_base_redshift = 0.0
                
            self.base_redshift = new_base_redshift
            
            # Update source label to indicate manual entry
            if self.galaxy_redshift_source not in ["Manual redshift specification", "Auto-detected"]:
                self.galaxy_redshift_source = "User entered"
                self.redshift_source_label.configure(text=f"({self.galaxy_redshift_source})")
            self._update_redshift_source_display()
            
            # Update all lines with new galaxy redshift
            self._update_all_lines()
            
        except ValueError:
            # Invalid input, ignore but highlight
            self.galaxy_redshift_entry.configure(bg='#ffcccc')  # Light red background
            return
        
        # Reset background if valid
        self.galaxy_redshift_entry.configure(bg=self.colors['bg_main'])
    

    
    def _on_wind_velocity_change(self, *args):
        """Handle velocity offset changes"""
        if self._updating_fields:
            return
        
        try:
            velocity_str = self.wind_velocity_var.get()
            if not velocity_str:
                return
                
            velocity_km_s = float(velocity_str)
            
            # Clamp to reasonable limits (±50,000 km/s ~ ±0.167c)
            if abs(velocity_km_s) > 50000:
                velocity_km_s = 50000 if velocity_km_s > 0 else -50000
                self._updating_fields = True
                self.wind_velocity_var.set(str(int(velocity_km_s)))
                self._updating_fields = False
                 
            # Update working redshift using the new calculation method
            self._update_total_redshift()
            
        except ValueError:
            # Invalid input, ignore but highlight
            try:
                velocity_entry = self.wind_velocity_var.get()
                if hasattr(self, 'wind_velocity_entry'):
                    self.wind_velocity_entry.configure(bg='#ffcccc')
            except:
                pass
            return
    
    def _set_wind_velocity_preset(self, v_value):
        """Set wind velocity to a preset value"""
        self._updating_fields = True
        self.wind_velocity_var.set(str(v_value))
        self._updating_fields = False
        self._update_total_redshift()
        _LOGGER.info(f"Set wind velocity preset to {v_value} km/s")

    def _calculate_distance_info(self, redshift):
        """Calculate distance information for a given redshift"""
        if redshift <= 0:
            return ""
        
        try:
            # Simple distance calculation (approximate for small z)
            if redshift < 0.1:
                # Non-relativistic approximation: v = cz, d = v/H0
                # Assuming H0 = 70 km/s/Mpc
                distance_mpc = (redshift * 299792.458) / 70  # Mpc
                return f"≈ {distance_mpc:.1f} Mpc"
            else:
                # For larger redshifts, just indicate the distance scale
                return f"High redshift (z > 0.1)"
        except:
            return ""

    def _update_total_redshift(self):
        """Update the working redshift based on SN redshift + wind velocity effect"""
        try:
            # Get SN redshift (base for calculation) - this is fixed from analysis
            sn_z = self.cluster_median_redshift
            
            # Get wind velocity in km/s
            wind_velocity = float(self.wind_velocity_var.get()) if self.wind_velocity_var.get() else 0.0
            
            # Convert wind velocity to redshift shift using v = cz approximation
            # Δz = v/c (non-relativistic approximation)
            c_km_s = 299792.458  # Speed of light in km/s
            wind_redshift_shift = wind_velocity / c_km_s
            
            # Calculate working redshift as SN redshift + wind effect
            self.current_redshift = sn_z + wind_redshift_shift
            
            # Ensure non-negative
            if self.current_redshift < 0:
                self.current_redshift = 0.0
            
            # Update the display
            self.working_redshift_label.configure(text=f"z = {self.current_redshift:.6f}")
            
            # Update all line positions based on new working redshift
            self._update_all_lines()
            
            _LOGGER.debug(f"Updated working redshift: SN z={sn_z:.6f} + wind Δz={wind_redshift_shift:.6f} = z={self.current_redshift:.6f}")
            
        except (ValueError, AttributeError) as e:
            _LOGGER.warning(f"Error updating working redshift: {e}")
            # Fallback to SN redshift only
            try:
                self.current_redshift = self.cluster_median_redshift
                self.working_redshift_label.configure(text=f"z = {self.current_redshift:.6f}")
            except:
                pass
    

    
    def _update_all_lines(self):
        """Update all line positions when redshift changes"""
        # Get the galaxy redshift if set
        galaxy_z = 0.0
        try:
            galaxy_z_str = self.galaxy_redshift_var.get()
            if galaxy_z_str:
                galaxy_z = float(galaxy_z_str)
        except:
            galaxy_z = 0.0
        
        # Update SN lines using working redshift (SN z + wind effect)
        updated_sn_lines = {}
        for line_name, (old_wavelength, line_data) in self.sn_lines.items():
            rest_wavelength = line_data['wavelength']
            new_obs_wavelength = rest_wavelength * (1 + self.current_redshift)
            updated_sn_lines[line_name] = (new_obs_wavelength, line_data)
        self.sn_lines = updated_sn_lines
        
        # Update galaxy lines using galaxy redshift if available, otherwise use working redshift
        updated_galaxy_lines = {}
        redshift_for_galaxy = galaxy_z if galaxy_z > 0.0001 else self.current_redshift
        
        for line_name, (old_wavelength, line_data) in self.galaxy_lines.items():
            rest_wavelength = line_data['wavelength']
            new_obs_wavelength = rest_wavelength * (1 + redshift_for_galaxy)
            updated_galaxy_lines[line_name] = (new_obs_wavelength, line_data)
        self.galaxy_lines = updated_galaxy_lines
        
        # Log the redshift usage
        _LOGGER.debug(f"Updated lines: SN lines use working z={self.current_redshift:.6f}, Galaxy lines use z={redshift_for_galaxy:.6f}")
        
        # Redraw plot
        self._update_plot_lines()
    
    def _on_plot_click(self, event):
        """Handle clicks on the spectrum plot"""
        if event.inaxes != self.ax_main:
            return
        
        click_wavelength = event.xdata
        if click_wavelength is None:
            return
        
        # Double left-click: Add nearby lines
        if event.button == 1 and event.dblclick:
            self._add_nearby_lines(click_wavelength)
        # Right-click: Remove closest line
        elif event.button == 3:  # Right click
            self._remove_line_at_position(click_wavelength)
    
    def _on_plot_hover(self, event):
        """Handle hover events on the spectrum plot"""
        # Could implement hover information display here
        pass
    
    def _on_key_press(self, event):
        """Handle key press events"""
        if event.key == 'shift':
            self.shift_pressed = True
            self._show_faint_overlay()
    
    def _on_key_release(self, event):
        """Handle key release events"""
        if event.key == 'shift':
            self.shift_pressed = False
            self._clear_faint_overlay()
    
    def _show_faint_overlay(self):
        """Show all available lines in very faint colors as overlay"""
        if not hasattr(self, 'ax_main') or self.ax_main is None:
            return
        
        try:
            # Clear any existing faint overlay
            self._clear_faint_overlay()
            
            # Show faint overlay using imported utility
            self.faint_line_artists = show_faint_overlay_on_plot(
                self.ax_main, self.current_mode, self.current_redshift, 
                self.spectrum_data, self.sn_lines, self.galaxy_lines, alpha=0.45)
            
            # Refresh canvas
            self.canvas.draw_idle()
            
        except Exception as e:
            _LOGGER.error(f"Error showing faint overlay: {e}")
    
    def _clear_faint_overlay(self):
        """Clear the faint overlay lines"""
        try:
            if hasattr(self, 'faint_line_artists'):
                clear_faint_overlay_from_plot(self.faint_line_artists)
                
                # Refresh canvas
                if hasattr(self, 'canvas'):
                    self.canvas.draw_idle()
                    
        except Exception as e:
            _LOGGER.error(f"Error clearing faint overlay: {e}")
    
    def _remove_line_at_position(self, wavelength, tolerance=10.0):
        """Remove line closest to the clicked position"""
        closest_line = find_closest_line(wavelength, self.sn_lines, self.galaxy_lines, tolerance)
        
        if closest_line:
            line_name, line_data, distance = closest_line
            
            # Remove from appropriate collection and tracking
            if line_name in self.sn_lines:
                del self.sn_lines[line_name]
            if line_name in self.galaxy_lines:
                del self.galaxy_lines[line_name]
            if line_name in self.line_sources:
                del self.line_sources[line_name]
            
            self._update_plot_lines()
            self._update_status()
            _LOGGER.info(f"Removed line: {line_name}")
    

    
    def _add_nearby_lines(self, wavelength, tolerance=12.0):
        """Add emission lines near the clicked wavelength"""
        added_lines = []
        
        # Determine which redshift to use based on mode
        redshift_to_use = self.current_redshift  # Default to working redshift
        
        if self.current_mode == 'galaxy':
            # For galaxy mode, check if galaxy redshift is set
            try:
                galaxy_z_str = self.galaxy_redshift_var.get()
                if galaxy_z_str:
                    galaxy_z = float(galaxy_z_str)
                    if galaxy_z > 0.0001:
                        redshift_to_use = galaxy_z
            except:
                pass
        
        # Get nearby lines using imported utility
        nearby_lines = add_nearby_lines(wavelength, redshift_to_use, self.current_mode,
                                       self.sn_lines, self.galaxy_lines, tolerance)
        
        # Add up to 3 closest lines
        for line_name, line_data, distance, obs_wavelength in nearby_lines:
            if self.current_mode == 'sn':
                if line_name not in self.sn_lines:
                    self.sn_lines[line_name] = (obs_wavelength, line_data)
                    self.line_sources[line_name] = f"Click @ {wavelength:.1f}Å"
                    added_lines.append(line_name)
            else:
                if line_name not in self.galaxy_lines:
                    self.galaxy_lines[line_name] = (obs_wavelength, line_data)
                    self.line_sources[line_name] = f"Click @ {wavelength:.1f}Å"
                    added_lines.append(line_name)
        
        # Track this action
        if added_lines:
            action_name = f"Click @ {wavelength:.1f}Å ({len(added_lines)} lines)"
            self.line_history.append((action_name, added_lines, self.current_mode))
            self._update_plot_lines()
            self._update_status()
        
        _LOGGER.info(f"Added {len(added_lines)} {self.current_mode} lines near {wavelength:.1f}Å")
    

    
    def _show_main_dropdown(self):
        """Show the main dropdown menu"""
        self._show_dropdown_menu(self.shortcuts_button, self.shortcut_options)
    
    def _show_dropdown_menu(self, parent_widget, options_dict):
        """Show a dropdown menu with the given options - improved version to avoid black menu issues"""
        try:
            # Create menu with minimal styling to avoid black menu issue
            menu = tk.Menu(self.dialog, tearoff=0)
            
            # Only apply basic styling that's less likely to cause issues
            try:
                # Try applying colors, but fall back gracefully
                menu.configure(
                    font=('Segoe UI', 11),
                    relief='raised',
                    borderwidth=1
                )
                
                # Apply colors only if they seem safe
                if hasattr(self.colors, 'get'):
                    bg_color = '#f0f0f0'  # Safe light gray background
                    fg_color = '#000000'  # Safe black text
                    active_bg = '#0078d4'  # Safe blue highlight
                    active_fg = '#ffffff'  # Safe white text
                    
                    menu.configure(
                        bg=bg_color,
                        fg=fg_color,
                        activebackground=active_bg,
                        activeforeground=active_fg
                    )
                    
            except (tk.TclError, AttributeError) as e:
                # If any color configuration fails, just use system defaults
                _LOGGER.debug(f"Using system default menu colors: {e}")
            
            # Add menu items
            for option_text, action in options_dict.items():
                try:
                    if option_text.startswith("───"):
                        # Separator header
                        menu.add_separator()
                        menu.add_command(label=option_text, state='disabled')
                        menu.add_separator()
                    elif option_text.endswith("►"):
                        # Submenu item
                        menu.add_command(label=option_text, 
                                       command=lambda a=action: self._handle_submenu_selection(a))
                    elif callable(action):
                        # Regular action
                        menu.add_command(label=option_text, command=action)
                    else:
                        # Disabled item
                        menu.add_command(label=option_text, state='disabled')
                except Exception as item_error:
                    _LOGGER.debug(f"Error adding menu item {option_text}: {item_error}")
                    continue
            
            # Calculate position and show menu
            try:
                x = parent_widget.winfo_rootx()
                y = parent_widget.winfo_rooty() + parent_widget.winfo_height()
                
                # Ensure menu appears on screen
                screen_width = self.dialog.winfo_screenwidth()
                screen_height = self.dialog.winfo_screenheight()
                
                if x + 300 > screen_width:  # Assume menu width ~300px
                    x = screen_width - 300
                if y + 400 > screen_height:  # Assume menu height ~400px
                    y = parent_widget.winfo_rooty() - 400
                
                menu.post(x, y)
                
                # Try to focus the menu (optional)
                try:
                    menu.focus_set()
                except:
                    pass
                    
            except Exception as post_error:
                _LOGGER.warning(f"Error posting menu: {post_error}")
                # Fallback: show options in a messagebox
                option_list = [key for key in options_dict.keys() if not key.startswith("───")]
                messagebox.showinfo("Menu Options", 
                                  "Available options:\n" + "\n".join(option_list[:10]))
                
        except Exception as e:
            _LOGGER.error(f"Critical error in dropdown menu: {e}")
            # Final fallback: simple messagebox
            messagebox.showinfo("Quick Options", 
                              "Menu temporarily unavailable. Please use manual line addition by clicking on the spectrum.")
    
    def _handle_submenu_selection(self, submenu_action):
        """Handle selection of submenu items"""
        if submenu_action == self._show_type_ii_submenu:
            self._show_dropdown_menu(self.shortcuts_button, self.type_ii_options)
        elif submenu_action == self._show_hydrogen_submenu:
            self._show_dropdown_menu(self.shortcuts_button, self.hydrogen_options)
        elif submenu_action == self._show_iron_submenu:
            self._show_dropdown_menu(self.shortcuts_button, self.iron_options)
        else:
            # Direct action
            submenu_action()
    
    def _show_type_ii_submenu(self):
        """Show Type II submenu"""
        pass  # Handled by _handle_submenu_selection
    
    def _show_hydrogen_submenu(self):
        """Show Hydrogen submenu"""
        pass  # Handled by _handle_submenu_selection
    
    def _show_iron_submenu(self):
        """Show Iron submenu"""
        pass  # Handled by _handle_submenu_selection
    
    def _get_type_ia_lines(self):
        """Add Type Ia supernova lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_type_ia_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("SN Type Ia", lines_to_add, 'sn')
    
    def _get_type_ii_lines(self):
        """Add Type II supernova lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_type_ii_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("SN Type II", lines_to_add, 'sn')
    
    def _get_type_ibc_lines(self):
        """Add Type Ib/c supernova lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_type_ibc_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("SN Type Ib/c", lines_to_add, 'sn')
    
    def _get_hydrogen_lines(self):
        """Add hydrogen lines"""
        lines_to_add = get_hydrogen_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Hydrogen Lines", lines_to_add, self.current_mode)
    
    def _get_helium_lines(self):
        """Add helium lines"""
        lines_to_add = get_helium_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Helium Lines", lines_to_add, self.current_mode)
    
    def _get_main_galaxy_lines(self):
        """Add main galaxy emission lines"""
        self.current_mode = 'galaxy'
        self._set_galaxy_mode()
        
        # Get galaxy redshift if available
        galaxy_z = 0.0
        try:
            galaxy_z_str = self.galaxy_redshift_var.get()
            if galaxy_z_str:
                galaxy_z = float(galaxy_z_str)
        except:
            galaxy_z = 0.0
            
        # Use galaxy redshift if available, otherwise use working redshift
        redshift_to_use = galaxy_z if galaxy_z > 0.0001 else self.current_redshift
        
        lines_to_add = get_main_galaxy_lines(redshift_to_use, self.spectrum_data)
        self._add_bulk_lines("Galaxy Lines", lines_to_add, 'galaxy')
    
    def _get_strong_lines(self):
        """Add only strong lines"""
        lines_to_add = get_strong_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Strong Lines", lines_to_add, self.current_mode)
    
    # Type II Submenu Methods
    def _get_early_type_ii(self):
        """Add early Type II lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_early_type_ii(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Early Type II", lines_to_add, 'sn')
    
    def _get_peak_type_ii(self):
        """Add peak Type II lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_peak_type_ii(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Peak Type II", lines_to_add, 'sn')
    
    def _get_nebular_type_ii(self):
        """Add nebular Type II lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_nebular_type_ii(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Nebular Type II", lines_to_add, 'sn')
    
    def _get_type_iin_lines(self):
        """Add Type IIn lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_type_iin_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Type IIn", lines_to_add, 'sn')
    
    def _get_type_iib_lines(self):
        """Add Type IIb lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_type_iib_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Type IIb", lines_to_add, 'sn')
    
    # Hydrogen Submenu Methods
    def _get_balmer_lines(self):
        """Add Balmer series hydrogen lines"""
        lines_to_add = get_balmer_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Balmer Series", lines_to_add, self.current_mode)
    
    def _get_paschen_lines(self):
        """Add Paschen series hydrogen lines"""
        lines_to_add = get_paschen_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Paschen Series", lines_to_add, self.current_mode)
    
    def _get_halpha_only(self):
        """Add only H-alpha line"""
        lines_to_add = get_halpha_only(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("H-alpha", lines_to_add, self.current_mode)
    
    def _get_hbeta_only(self):
        """Add only H-beta line"""
        lines_to_add = get_hbeta_only(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("H-beta", lines_to_add, self.current_mode)
    
    def _get_strong_hydrogen(self):
        """Add strong hydrogen lines"""
        lines_to_add = get_strong_hydrogen(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Strong Hydrogen", lines_to_add, self.current_mode)
    
    # Iron Submenu Methods
    def _get_iron_lines(self):
        """Add all iron lines"""
        lines_to_add = get_iron_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Iron Lines", lines_to_add, self.current_mode)
    
    def _get_fe_ii_lines(self):
        """Add Fe II lines"""
        lines_to_add = get_fe_ii_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Fe II Lines", lines_to_add, self.current_mode)
    
    def _get_fe_iii_lines(self):
        """Add Fe III lines"""
        lines_to_add = get_fe_iii_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Fe III Lines", lines_to_add, self.current_mode)
    
    def _get_early_iron(self):
        """Add early iron lines"""
        lines_to_add = get_early_iron(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Early Iron", lines_to_add, self.current_mode)
    
    def _get_late_iron(self):
        """Add late iron lines"""
        lines_to_add = get_late_iron(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Late Iron", lines_to_add, self.current_mode)
    
    # Additional Methods
    def _get_early_sn_lines(self):
        """Add early phase supernova lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_early_sn_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Early SN", lines_to_add, 'sn')
    
    def _get_maximum_lines(self):
        """Add maximum light lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_maximum_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Maximum Light", lines_to_add, 'sn')
    
    def _get_late_phase_lines(self):
        """Add late phase lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_late_phase_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Late Phase", lines_to_add, 'sn')
    
    def _get_nebular_lines(self):
        """Add nebular lines"""
        self.current_mode = 'sn'
        self._set_sn_mode()
        lines_to_add = get_nebular_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Nebular", lines_to_add, 'sn')
    
    def _get_silicon_lines(self):
        """Add silicon lines"""
        lines_to_add = get_silicon_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Silicon Lines", lines_to_add, self.current_mode)
    
    def _get_calcium_lines(self):
        """Add calcium lines"""
        lines_to_add = get_calcium_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Calcium Lines", lines_to_add, self.current_mode)
    
    def _get_oxygen_lines(self):
        """Add oxygen lines"""
        lines_to_add = get_oxygen_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Oxygen Lines", lines_to_add, self.current_mode)
    
    def _get_diagnostic_lines(self):
        """Add galaxy diagnostic lines"""
        self.current_mode = 'galaxy'
        self._set_galaxy_mode()
        
        # Get galaxy redshift if available
        galaxy_z = 0.0
        try:
            galaxy_z_str = self.galaxy_redshift_var.get()
            if galaxy_z_str:
                galaxy_z = float(galaxy_z_str)
        except:
            galaxy_z = 0.0
            
        # Use galaxy redshift if available, otherwise use working redshift
        redshift_to_use = galaxy_z if galaxy_z > 0.0001 else self.current_redshift
        
        lines_to_add = get_diagnostic_lines(redshift_to_use, self.spectrum_data)
        self._add_bulk_lines("Diagnostic Lines", lines_to_add, 'galaxy')
    
    def _get_emission_lines(self):
        """Add emission lines only"""
        lines_to_add = get_emission_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Emission Lines", lines_to_add, self.current_mode)
    
    def _get_absorption_lines(self):
        """Add absorption lines only"""
        lines_to_add = get_absorption_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Absorption Lines", lines_to_add, self.current_mode)
    
    def _get_very_strong_lines(self):
        """Add very strong lines"""
        lines_to_add = get_very_strong_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Very Strong Lines", lines_to_add, self.current_mode)
    
    def _get_common_lines(self):
        """Add all common lines"""
        lines_to_add = get_common_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Common Lines", lines_to_add, self.current_mode)
    
    def _get_flash_lines(self):
        """Add flash ionization lines"""
        lines_to_add = get_flash_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Flash Ionization", lines_to_add, self.current_mode)
    
    def _get_interaction_lines(self):
        """Add interaction/CSM lines"""
        lines_to_add = get_interaction_lines(self.current_redshift, self.spectrum_data)
        self._add_bulk_lines("Interaction Lines", lines_to_add, self.current_mode)
    

    
    def _is_line_in_spectrum_range(self, line_data):
        """Check if line is within spectrum wavelength range"""
        return is_line_in_spectrum_range(line_data, self.current_redshift, self.spectrum_data)
    
    def _add_bulk_lines(self, action_name, lines_dict, mode):
        """Add multiple lines and track the action"""
        added_lines = []
        
        for line_name, (obs_wavelength, line_data) in lines_dict.items():
            if mode == 'sn':
                if line_name not in self.sn_lines:
                    self.sn_lines[line_name] = (obs_wavelength, line_data)
                    self.line_sources[line_name] = action_name
                    added_lines.append(line_name)
            else:
                if line_name not in self.galaxy_lines:
                    self.galaxy_lines[line_name] = (obs_wavelength, line_data)
                    self.line_sources[line_name] = action_name
                    added_lines.append(line_name)
        
        # Track this bulk action
        if added_lines:
            self.line_history.append((action_name, added_lines, mode))
            self._update_plot_lines()
            self._update_status()
            # Reflect latest preset/action on the Quick Preset button label
            self.current_selection = action_name
            if hasattr(self, 'shortcuts_button'):
                try:
                    self.shortcuts_button.configure(text=action_name)
                except Exception:
                    pass
        
        _LOGGER.info(f"Added {len(added_lines)} lines via {action_name}")
    
    def _update_tracking_display(self):
        """Update the line tracking listbox"""
        # Clear current items
        self.tracker_listbox.delete(0, tk.END)
        
        # Add SN lines
        for line_name, (obs_wavelength, line_data) in self.sn_lines.items():
            rest_wavelength = line_data.get('wavelength', 0)
            source = self.line_sources.get(line_name, 'Manual')
            display_text = f"🌟 {line_name} ({rest_wavelength:.1f}Å) - {source}"
            self.tracker_listbox.insert(tk.END, display_text)
        
        # Add galaxy lines
        for line_name, (obs_wavelength, line_data) in self.galaxy_lines.items():
            rest_wavelength = line_data.get('wavelength', 0)
            source = self.line_sources.get(line_name, 'Manual')
            display_text = f"🌌 {line_name} ({rest_wavelength:.1f}Å) - {source}"
            self.tracker_listbox.insert(tk.END, display_text)
    
    def _remove_selected_from_tracker(self):
        """Remove selected lines from tracker"""
        selected_indices = self.tracker_listbox.curselection()
        if not selected_indices:
            return
        
        # Get all line names
        all_line_names = list(self.sn_lines.keys()) + list(self.galaxy_lines.keys())
        
        # Remove selected lines
        for index in reversed(selected_indices):  # Reverse to maintain indices
            if index < len(all_line_names):
                line_name = all_line_names[index]
                if line_name in self.sn_lines:
                    del self.sn_lines[line_name]
                if line_name in self.galaxy_lines:
                    del self.galaxy_lines[line_name]
                if line_name in self.line_sources:
                    del self.line_sources[line_name]
        
        self._update_plot_lines()
        self._update_status()
    
    def _clear_all_lines(self):
        """Clear all selected lines"""
        self.sn_lines.clear()
        self.galaxy_lines.clear()
        self.line_sources.clear()
        self.line_history.clear()
        
        self._update_plot_lines()
        self._update_status()
        _LOGGER.info("Cleared all lines")

    # ==========================================
    # STEP 2 IMPLEMENTATION: Peak Analysis
    # ==========================================
    
    def _create_step2_options(self):
        """Create simplified Step 2 panel – all controls in one quadrant"""

        # Clear any previous widgets (safety for re-entry)
        for w in self.options_frame.winfo_children():
            w.destroy()

        main_frame = tk.LabelFrame(self.options_frame, text="🎯 Current Line Analysis", 
                                   bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                                   font=('Segoe UI', 14, 'bold'))
        main_frame.pack(fill='both', expand=True)

        # ---------- Line selector ----------
        selector = tk.Frame(main_frame, bg=self.colors['bg_step'])
        selector.pack(fill='x', padx=15, pady=(15, 10))

        tk.Label(selector, text="Select Line:", bg=self.colors['bg_step'],
                 fg=self.colors['text_primary'], font=('Segoe UI', 13, 'bold')).pack(side='left')

        self.current_line_var = tk.StringVar()
        self.line_dropdown_button = tk.Button(selector, textvariable=self.current_line_var,
                                              font=('Segoe UI', 12), width=28,
                                              bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                              relief='sunken', bd=1, anchor='w',
                                              command=self._show_line_selection_menu)
        self.line_dropdown_button.pack(side='right')

        self.current_line_var.set("Select a line…")

        # Navigation controls
        nav = tk.Frame(main_frame, bg=self.colors['bg_step'])
        nav.pack(fill='x', padx=15, pady=(0, 10))

        self.prev_line_button = tk.Button(nav, text="◀ Previous", command=self._previous_line,
                                          bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                          font=('Segoe UI', 10, 'bold'), width=10)
        self.prev_line_button.pack(side='left')

        self.line_counter_label = tk.Label(nav, text="Line 1 of 0", bg=self.colors['bg_step'],
                                           fg=self.colors['text_primary'], font=('Segoe UI', 11, 'bold'))
        self.line_counter_label.pack(side='left', expand=True)

        self.next_line_button = tk.Button(nav, text="Next ▶", command=self._next_line,
                                          bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                          font=('Segoe UI', 10, 'bold'), width=10)
        self.next_line_button.pack(side='right')

        # ---------- Zoom range ----------
        zoom = tk.Frame(main_frame, bg=self.colors['bg_step'])
        zoom.pack(fill='x', padx=15, pady=(0, 10))

        tk.Label(zoom, text="Zoom (±Å):", bg=self.colors['bg_step'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 12, 'bold')).pack(side='left')

        self.zoom_range_var = tk.StringVar(value="300")
        zoom_entry = tk.Entry(zoom, textvariable=self.zoom_range_var, font=('Courier New', 11),
                              width=6, bg=self.colors['bg_main'], fg=self.colors['text_primary'])
        zoom_entry.pack(side='right')
        zoom_entry.bind('<Return>', self._on_zoom_changed)

        # -------- Manual point controls ----------
        self.points_controls_frame = tk.Frame(main_frame, bg=self.colors['bg_step'])
        self.points_controls_frame.pack(fill='x', padx=15, pady=(10, 5))

        tk.Label(self.points_controls_frame, text="Manual Selection:", bg=self.colors['bg_step'],
                 fg=self.colors['text_primary'], font=('Segoe UI', 11, 'bold')).pack(side='left')

        # Instructions
        self.instructions_frame = tk.Frame(main_frame, bg=self.colors['bg_step'])
        self.instructions_frame.pack(fill='x', padx=15)

        instructions = (
            "Manual Selection – HOW TO:\n"
            "• Click multiple times along the central peak of the line\n"
            "• Hold Ctrl and click to add anchor points outside spectrum region\n"
            "• Right-click to remove closest point\n"
            "• Use 'Auto Contour' for automatic peak detection"
        )
        self.instructions_label = tk.Label(self.instructions_frame, text=instructions, justify='left',
                                           bg=self.colors['bg_step'], fg=self.colors['text_secondary'],
                                           font=('Segoe UI', 10), wraplength=350)
        self.instructions_label.pack(anchor='w', padx=5, pady=5)
        
        # Add analyze button after instructions
        analyze_frame = tk.Frame(main_frame, bg=self.colors['bg_step'])
        analyze_frame.pack(fill='x', padx=15, pady=(10, 5))
        
        self.analyze_current_button = tk.Button(analyze_frame, text="🔬 Analyze Current Line",
                                                command=self._analyze_current_line,
                                                bg=self.colors['success'], fg='white',
                                                font=('Segoe UI', 12, 'bold'), relief='raised', bd=2,
                                                width=20, height=2)
        self.analyze_current_button.pack(pady=5)

        # Results box
        results = tk.Frame(main_frame, bg=self.colors['bg_step'])
        results.pack(fill='both', expand=False, padx=15, pady=(5, 10))

        self.current_result_text = tk.Text(results, height=4, bg=self.colors['bg_main'], fg=self.colors['text_primary'],
                                           font=('Courier New', 10), wrap='word')
        self.current_result_text.pack(fill='x')
        self.current_result_text.insert('1.0', "Select a line, pick points, then hit 'Analyze Current Line' in the plot toolbar…")
        self.current_result_text.config(state='disabled')

        # Summary (optional but still useful) – keep inside same quadrant
        summary = tk.LabelFrame(main_frame, text="📋 Summary", bg=self.colors['bg_step'],
                                fg=self.colors['text_primary'], font=('Segoe UI', 12, 'bold'))
        summary.pack(fill='both', expand=True, padx=15, pady=(0, 10))

        summary_frame = tk.Frame(summary, bg=self.colors['bg_step'])
        summary_frame.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(summary_frame, bg=self.colors['bg_step'])
        scrollbar.pack(side='right', fill='y')

        self.summary_text = tk.Text(summary_frame, yscrollcommand=scrollbar.set, height=6,
                                    bg=self.colors['bg_main'], fg=self.colors['text_primary'], font=('Consolas', 10),
                                    wrap='word', state='disabled')
        self.summary_text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.summary_text.yview)

        # Needed variables for downstream logic
        self.method_var = tk.StringVar(value='manual_points')  # Hidden but kept for compatibility
        self.method_options = {'Manual Points': 'manual_points'}

        # Initialise bookkeeping
        self.available_lines = []
        self.current_line_index = 0
        self.line_analysis_results = {}
        self.selected_manual_points = []

        # Populate dropdown
        self._populate_line_dropdown()
        
        # Set up dynamic text wrapping
        self._setup_dynamic_text_wrapping()

        # END new simplified layout
        return  # Skip legacy code below
    
    def _create_step2_plot(self):
        """Create the focused single-line plot for Step 2"""
        # Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Create single main plot for focused line analysis with optimized layout
        self.figure = plt.figure(figsize=(16, 8), dpi=150)
        self.figure.patch.set_facecolor('white')
        
        # Use balanced layout - not too tight to avoid cutting labels
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.12)
        
        # Single main plot
        self.ax_main = self.figure.add_subplot(111)
        self.ax_main.set_facecolor('white')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=2, pady=2)
        
        # Add navigation toolbar (without analyze button - it will be inside the plot)
        toolbar_frame = tk.Frame(self.plot_frame, bg=self.colors['bg_panel'])
        toolbar_frame.pack(fill='x', pady=(2, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        self.toolbar.config(bg=self.colors['bg_panel'])
        
        # Set up click handler for point selection
        self.canvas.mpl_connect('button_press_event', self._on_plot_click_step2)
        
        # Plot the focused spectrum
        self._plot_focused_line()
        
        # Apply tight layout with more generous padding
        try:
            self.figure.tight_layout(pad=1.5)
        except Exception as e:
            _LOGGER.debug(f"Tight layout warning: {e}")
        
        self.canvas.draw()
    
    def _plot_focused_line(self):
        """Plot spectrum focused on the current selected line"""
        if not self.spectrum_data or 'wavelength' not in self.spectrum_data:
            return
        
        if not self.available_lines or self.current_line_index >= len(self.available_lines):
            # No lines available, show full spectrum
            self._plot_full_spectrum()
            return
        
        # Only show analyze button in Step 2
        show_analyze_button = (self.current_step == 2)
        
        # Get current line
        current_line_name = self.available_lines[self.current_line_index]
        current_wavelength, line_data, line_origin = self._get_line_info(current_line_name)
        
        # Clear the plot
        self.ax_main.clear()
        
        # Get zoom range
        try:
            zoom_range = float(self.zoom_range_var.get())
        except:
            zoom_range = 300.0
        
        # Calculate wavelength range
        wl_min = current_wavelength - zoom_range
        wl_max = current_wavelength + zoom_range
        
        # Get spectrum data
        wavelength = self.spectrum_data['wavelength']
        flux = self.spectrum_data['flux']
        
        # Filter to zoom range
        mask = (wavelength >= wl_min) & (wavelength <= wl_max)
        wl_zoom = wavelength[mask]
        flux_zoom = flux[mask]
        
        if len(wl_zoom) == 0:
            # No data in range, show message
            self.ax_main.text(0.5, 0.5, f"No spectrum data in range\n{wl_min:.1f} - {wl_max:.1f} Å",
                            transform=self.ax_main.transAxes, ha='center', va='center',
                            fontsize=14, color='red')
        else:
            # Plot spectrum in zoom range
            self.ax_main.plot(wl_zoom, flux_zoom, 'k-', linewidth=1.5, alpha=0.8)
            
            # Highlight the current line
            color = get_line_color(line_data, line_origin)
            self.ax_main.axvline(current_wavelength, color=color, linestyle='-', 
                               alpha=0.9, linewidth=3, label=current_line_name)
            
            # Show any other lines in this range
            plot_other_lines_in_range(self.ax_main, self.available_lines, self.sn_lines, 
                                    self.galaxy_lines, wl_min, wl_max, current_line_name)
            
            # Show selected manual points with enhanced visualization
            if hasattr(self, 'selected_manual_points') and self.selected_manual_points:
                visible_points = [(x, y) for x, y in self.selected_manual_points if wl_min <= x <= wl_max]
                
                if visible_points:
                    # Sort points by wavelength for connecting lines
                    visible_points.sort(key=lambda p: p[0])
                    x_points = [p[0] for p in visible_points]
                    y_points = [p[1] for p in visible_points]
                    
                    # Draw connecting lines between points to show peak contour
                    if len(visible_points) > 1:
                        self.ax_main.plot(x_points, y_points, 'r--', linewidth=2, alpha=0.6, 
                                        label='Manual Contour')
                    
                    # Draw individual points with enhanced styling
                    for i, (x, y) in enumerate(visible_points):
                        # Use different colors/shapes for different types of points
                        if i == 0 or i == len(visible_points) - 1:
                            # Boundary points - square markers
                            self.ax_main.plot(x, y, 'rs', markersize=10, alpha=0.8, 
                                           markeredgecolor='darkred', markeredgewidth=2)
                        else:
                                                         # Peak/interior points - circle markers  
                             self.ax_main.plot(x, y, 'ro', markersize=10, alpha=0.8,
                                            markeredgecolor='darkred', markeredgewidth=2)
            
            # Show fit curve if available
            if (hasattr(self, 'line_fit_results') and 
                current_line_name in self.line_fit_results):
                
                fit_data = self.line_fit_results[current_line_name]
                fit_wl = fit_data['fit_wavelength']
                fit_flux = fit_data['fit_flux']
                
                # Filter fit curve to visible range
                fit_mask = (fit_wl >= wl_min) & (fit_wl <= wl_max)
                if np.any(fit_mask):
                    fit_wl_visible = fit_wl[fit_mask]
                    fit_flux_visible = fit_flux[fit_mask]
                    
                    # Choose color based on fit method
                    fit_color = '#00aa00' if fit_data['method'] == 'gaussian' else '#0066cc'
                    fit_label = f"{fit_data['method'].title()} Fit"
                    
                    self.ax_main.plot(fit_wl_visible, fit_flux_visible, 
                                    color=fit_color, linewidth=3, alpha=0.8,
                                    label=fit_label, linestyle='-')
            
            # Add title and labels
            title_text = f"Line Analysis: {current_line_name} ({current_wavelength:.1f} Å)"
            
            # Add fit info to title if available
            if (hasattr(self, 'line_fit_results') and 
                current_line_name in self.line_fit_results):
                fit_data = self.line_fit_results[current_line_name]
                if 'r_squared' in fit_data:
                    title_text += f" | R² = {fit_data['r_squared']:.3f}"
                    
            self.ax_main.set_title(title_text, fontsize=14, fontweight='bold', pad=20)
            
        # Styling
        self.ax_main.set_xlabel('Wavelength (Å)', color='black', fontsize=12)
        self.ax_main.set_ylabel('Flux', color='black', fontsize=12)
        self.ax_main.tick_params(colors='black')
        self.ax_main.grid(True, alpha=0.3)
        
        # Legend intentionally suppressed to declutter the view

        # Note: Button is now in the left panel, not inside the plot
        
        # Apply tight layout and refresh canvas
        try:
            self.figure.tight_layout(pad=1.5)
        except Exception as e:
            _LOGGER.debug(f"Tight layout warning: {e}")
        
        # Refresh canvas
        self.canvas.draw()
    
    def _plot_full_spectrum(self):
        """Plot the full spectrum when no line is selected"""
        wavelength = self.spectrum_data['wavelength']
        flux = self.spectrum_data['flux']
        self.ax_main.plot(wavelength, flux, 'k-', linewidth=1, alpha=0.8)
        
        # Show all available lines as reference
        for line_name in self.available_lines:
            obs_wavelength, line_data, line_origin = self._get_line_info(line_name)
            color = get_line_color(line_data, line_origin)
            linestyle = '-' if line_origin == 'sn' else '--'
            self.ax_main.axvline(obs_wavelength, color=color, linestyle=linestyle, 
                               alpha=0.6, linewidth=1)
        
        self.ax_main.set_title("Select a line to focus analysis", fontsize=14, fontweight='bold')
    

    
    def _get_line_info(self, line_name):
        """Get wavelength, line_data, and origin for a line"""
        if line_name in self.sn_lines:
            obs_wavelength, line_data = self.sn_lines[line_name]
            return obs_wavelength, line_data, 'sn'
        elif line_name in self.galaxy_lines:
            obs_wavelength, line_data = self.galaxy_lines[line_name]
            return obs_wavelength, line_data, 'galaxy'
        else:
            # Should not happen, but fallback
            return 0.0, {}, 'unknown'
    
    # === NEW SINGLE-LINE FOCUSED METHODS ===
    
    def _show_line_selection_menu(self):
        """Show custom line selection menu to replace TTK Combobox"""
        if not self.available_lines:
            messagebox.showinfo("No Lines", "No lines available for analysis.\n\nPlease return to Step 1 and add some lines first.")
            return
        
        # Create line selection options
        line_options = {}
        for i, line_name in enumerate(self.available_lines):
            if line_name in self.sn_lines:
                obs_wavelength, line_data = self.sn_lines[line_name]
                display_text = f"🌟 {line_name} ({line_data.get('wavelength', 0):.1f}Å)"
            elif line_name in self.galaxy_lines:
                obs_wavelength, line_data = self.galaxy_lines[line_name]
                display_text = f"🌌 {line_name} ({line_data.get('wavelength', 0):.1f}Å)"
            else:
                display_text = line_name
                
            line_options[display_text] = lambda idx=i: self._select_line_by_index(idx)
        
        # Show the custom dropdown menu
        self._show_dropdown_menu(self.line_dropdown_button, line_options)
    
    def _select_line_by_index(self, index):
        """Select a line by its index in the available lines list"""
        if 0 <= index < len(self.available_lines):
            self.current_line_index = index
            line_name = self.available_lines[index]
            self.current_line_var.set(line_name)
            self._update_line_counter()
            self._update_line_navigation_buttons()
            self._plot_focused_line()
            self._clear_selected_points()
            self._update_current_result_display()
    
    def _populate_line_dropdown(self):
        """Populate the line dropdown with available lines"""
        # Get all available lines
        self.available_lines = list(self.sn_lines.keys()) + list(self.galaxy_lines.keys())
        
        # Update dropdown button text
        if self.available_lines:
            # Select first line by default
            self.current_line_index = 0
            self.current_line_var.set(self.available_lines[0])
            self._update_line_counter()
            self._update_line_navigation_buttons()
        else:
            self.current_line_var.set("No lines selected")
            self.current_line_index = 0
    
    def _on_line_selection_changed(self, event=None):
        """Handle line selection change"""
        if not self.available_lines:
            return
            
        selected_line = self.current_line_var.get()
        if selected_line in self.available_lines:
            self.current_line_index = self.available_lines.index(selected_line)
            self._update_line_counter()
            self._update_line_navigation_buttons()
            self._plot_focused_line()
            self._clear_selected_points()
            self._update_current_result_display()
    
    def _previous_line(self):
        """Navigate to previous line"""
        if not self.available_lines:
            return
            
        self.current_line_index = (self.current_line_index - 1) % len(self.available_lines)
        self.current_line_var.set(self.available_lines[self.current_line_index])
        self._update_line_counter()
        self._update_line_navigation_buttons()
        self._plot_focused_line()
        self._clear_selected_points()
        self._update_current_result_display()
    
    def _next_line(self):
        """Navigate to next line"""
        if not self.available_lines:
            return
            
        self.current_line_index = (self.current_line_index + 1) % len(self.available_lines)
        self.current_line_var.set(self.available_lines[self.current_line_index])
        self._update_line_counter()
        self._update_line_navigation_buttons()
        self._plot_focused_line()
        self._clear_selected_points()
        self._update_current_result_display()
    
    def _update_line_counter(self):
        """Update the line counter display"""
        # Only update if label exists (Step 2 specific)
        if not hasattr(self, 'line_counter_label'):
            return
            
        if self.available_lines:
            current = self.current_line_index + 1
            total = len(self.available_lines)
            self.line_counter_label.config(text=f"Line {current} of {total}")
        else:
            self.line_counter_label.config(text="No lines available")
    
    def _update_line_navigation_buttons(self):
        """Update line navigation button states (Step 2 specific)"""
        # Only update if buttons exist (Step 2 specific)
        if not hasattr(self, 'prev_line_button') or not hasattr(self, 'next_line_button'):
            return
            
        if len(self.available_lines) <= 1:
            self.prev_line_button.config(state='disabled')
            self.next_line_button.config(state='disabled')
        else:
            self.prev_line_button.config(state='normal')
            self.next_line_button.config(state='normal')
    
    def _set_zoom(self, zoom_value):
        """Set zoom range and refresh plot"""
        self.zoom_range_var.set(str(zoom_value))
        self._plot_focused_line()
    
    def _on_zoom_changed(self, event=None):
        """Handle zoom range change"""
        self._plot_focused_line()
    
    def _show_method_selection_menu(self):
        """Show custom method selection menu to replace TTK Combobox"""
        # Create method selection options
        method_menu_options = {}
        for display_name, internal_value in self.method_options.items():
            method_menu_options[display_name] = lambda val=internal_value, disp=display_name: self._select_method(val, disp)
        
        # Show the custom dropdown menu
        self._show_dropdown_menu(self.method_dropdown_button, method_menu_options)
    
    def _select_method(self, internal_value, display_name):
        """Select a method and update the interface"""
        self.method_var.set(display_name)
        self._on_method_changed(internal_value)
    
    def _on_method_changed(self, method_value=None):
        """Handle analysis method change"""
        if method_value is None:
            # Get internal method value from display name
            display_name = self.method_var.get()
            method_value = self.method_options.get(display_name, 'manual_points')
        
        # Show/hide manual point controls and instructions based on method
        if method_value == 'manual_points':
            self.points_controls_frame.pack(side='right', padx=(20, 0))
            if hasattr(self, 'instructions_frame'):
                self.instructions_frame.pack(fill='x', padx=15, pady=(5, 0))
                self.instructions_label.pack(anchor='w', pady=5)
        else:
            self.points_controls_frame.pack_forget()
            if hasattr(self, 'instructions_frame'):
                self.instructions_frame.pack_forget()
            
        # Clear any existing manual points when switching methods
        if hasattr(self, 'selected_manual_points'):
            self.selected_manual_points.clear()
            self._update_selected_points_display()
            
        # Clear fit results when switching methods
        if hasattr(self, 'line_fit_results') and self.available_lines:
            current_line_name = self.available_lines[self.current_line_index]
            if current_line_name in self.line_fit_results:
                del self.line_fit_results[current_line_name]
            
        # Refresh plot if needed
        if hasattr(self, 'ax_main'):
            self._plot_focused_line()
    
    def _zoom_full(self):
        """Show full spectrum"""
        if not self.spectrum_data or 'wavelength' not in self.spectrum_data:
            return
            
        self.ax_main.clear()
        self._plot_full_spectrum()
        
        # Styling
        self.ax_main.set_xlabel('Wavelength (Å)', color='black', fontsize=12)
        self.ax_main.set_ylabel('Flux', color='black', fontsize=12)
        self.ax_main.tick_params(colors='black')
        self.ax_main.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def _on_plot_click_step2(self, event):
        """Enhanced plot clicks for intuitive manual point selection with free-floating points"""
        if event.inaxes != self.ax_main:
            return
            
        # Note: Button is now in the left panel, not in the plot
            
        # Only proceed with point selection if in manual points mode
        if self.method_var.get() not in ('manual_points', 'Manual Points'):
            return
            
        x_click, y_click = event.xdata, event.ydata
        if x_click is None or y_click is None:
            return
        
        if event.button == 1:  # Left click
            if event.key == 'control':  # Ctrl+Click: Add free-floating point
                self._add_manual_point(x_click, y_click)
            elif event.key == 'shift':  # Shift+Click: Snap to spectrum curve
                self._add_spectrum_snapped_point(x_click, y_click)
            else:  # Simple click: Smart peak detection on spectrum
                self._smart_peak_selection_on_spectrum(x_click, y_click)
                
        elif event.button == 3:  # Right click: Remove closest point
            self._remove_closest_point(x_click)
    
    def _add_spectrum_snapped_point(self, x_click, y_click):
        """Add point snapped to the actual spectrum curve"""
        # Get spectrum data to snap to actual flux values
        wavelength = self.spectrum_data['wavelength']
        flux = self.spectrum_data['flux']
        
        try:
            zoom_range = float(self.zoom_range_var.get())
        except:
            zoom_range = 300.0
            
        current_line_name = self.available_lines[self.current_line_index]
        current_wavelength, _, _ = self._get_line_info(current_line_name)
        
        # Filter to zoom range
        wl_min = current_wavelength - zoom_range
        wl_max = current_wavelength + zoom_range
        mask = (wavelength >= wl_min) & (wavelength <= wl_max)
        wl_zoom = wavelength[mask]
        flux_zoom = flux[mask]
        
        if len(wl_zoom) == 0:
            return
            
        # Find closest spectrum point to click
        distances = np.abs(wl_zoom - x_click)
        closest_idx = np.argmin(distances)
        snap_x = wl_zoom[closest_idx]
        snap_y = flux_zoom[closest_idx]
        
        self._add_manual_point(snap_x, snap_y)
    
    def _smart_peak_selection_on_spectrum(self, x_click, y_click):
        """Smart peak detection using spectrum data"""
        wavelength = self.spectrum_data['wavelength']
        flux = self.spectrum_data['flux']
        
        try:
            zoom_range = float(self.zoom_range_var.get())
        except:
            zoom_range = 300.0
            
        current_line_name = self.available_lines[self.current_line_index]
        current_wavelength, _, _ = self._get_line_info(current_line_name)
        
        # Filter to zoom range
        wl_min = current_wavelength - zoom_range
        wl_max = current_wavelength + zoom_range
        mask = (wavelength >= wl_min) & (wavelength <= wl_max)
        wl_zoom = wavelength[mask]
        flux_zoom = flux[mask]
        
        if len(wl_zoom) == 0:
            return
            
        # Find closest spectrum point to click
        distances = np.abs(wl_zoom - x_click)
        closest_idx = np.argmin(distances)
        snap_x = wl_zoom[closest_idx]
        snap_y = flux_zoom[closest_idx]
        
        self._smart_peak_selection(snap_x, snap_y, wl_zoom, flux_zoom)
    
    def _add_manual_point(self, x, y):
        """Add a single manual point"""
        # Avoid duplicate points (within 1 Angstrom)
        for existing_x, existing_y in self.selected_manual_points:
            if abs(existing_x - x) < 1.0:
                return  # Too close to existing point
                
        self.selected_manual_points.append((x, y))
        self._update_selected_points_display()
        self._plot_focused_line()
        
    def _smart_peak_selection(self, click_x, click_y, wl_zoom, flux_zoom):
        """Smart peak detection around clicked point for blended peak analysis"""
        if len(wl_zoom) < 5:
            # Fallback to simple point addition
            self._add_manual_point(click_x, click_y)
            return
            
        # Find the clicked point index
        click_idx = np.argmin(np.abs(wl_zoom - click_x))
        
        # Try to detect local peak boundaries around the click
        peak_points = []
        
        # Method 1: Find local peak boundaries using slope changes
        try:
            # Calculate gradient (slope) of the spectrum
            gradient = np.gradient(flux_zoom)
            
            # Find where gradient changes sign around click point
            left_boundary = click_idx
            right_boundary = click_idx
            
            # Look for gradient sign changes to find peak boundaries
            # Go left until we find where it starts going up (negative to positive gradient)
            for i in range(click_idx, max(0, click_idx - 20), -1):
                if i > 0 and gradient[i-1] < 0 and gradient[i] >= 0:
                    left_boundary = i
                    break
                elif i > 0 and flux_zoom[i] < flux_zoom[click_idx] * 0.7:  # 70% of peak height
                    left_boundary = i
                    break
                    
            # Go right until we find where it starts going down (positive to negative gradient)  
            for i in range(click_idx, min(len(flux_zoom)-1, click_idx + 20)):
                if i < len(gradient)-1 and gradient[i] > 0 and gradient[i+1] <= 0:
                    right_boundary = i
                    break
                elif flux_zoom[i] < flux_zoom[click_idx] * 0.7:  # 70% of peak height
                    right_boundary = i
                    break
                    
            # Add boundary points for peak contour
            if left_boundary != click_idx:
                peak_points.append((wl_zoom[left_boundary], flux_zoom[left_boundary]))
                
            # Add peak center if it's not too close to boundaries
            if abs(left_boundary - click_idx) > 2 and abs(right_boundary - click_idx) > 2:
                peak_points.append((wl_zoom[click_idx], flux_zoom[click_idx]))
                
            if right_boundary != click_idx:
                peak_points.append((wl_zoom[right_boundary], flux_zoom[right_boundary]))
                
        except Exception:
            # Fallback: simple addition if smart detection fails
            peak_points = [(click_x, click_y)]
            
        # Add detected points
        for x, y in peak_points:
            self._add_manual_point(x, y)
            
    def _remove_closest_point(self, click_x):
        """Remove the closest manually selected point"""
        if not self.selected_manual_points:
            return
            
        # Find closest point
        distances = [abs(x - click_x) for x, y in self.selected_manual_points]
        closest_idx = np.argmin(distances)
        
        # Remove closest point
        removed_point = self.selected_manual_points.pop(closest_idx)
        self._update_selected_points_display()
        self._plot_focused_line()
        
    def _auto_select_peak_contour(self):
        """Automatically select a contour around the current line peak"""
        if not self.available_lines or self.current_line_index >= len(self.available_lines):
            return
            
        current_line_name = self.available_lines[self.current_line_index]
        current_wavelength, _, _ = self._get_line_info(current_line_name)
        
        # Get spectrum data
        wavelength = self.spectrum_data['wavelength']
        flux = self.spectrum_data['flux']
        
        try:
            zoom_range = float(self.zoom_range_var.get())
        except:
            zoom_range = 300.0
            
        # Filter to zoom range
        wl_min = current_wavelength - zoom_range
        wl_max = current_wavelength + zoom_range
        mask = (wavelength >= wl_min) & (wavelength <= wl_max)
        wl_zoom = wavelength[mask]
        flux_zoom = flux[mask]
        
        if len(wl_zoom) < 10:
            return
            
        # Find the peak near the line position
        center_idx = np.argmin(np.abs(wl_zoom - current_wavelength))
        search_range = min(10, len(flux_zoom)//4)
        
        search_start = max(0, center_idx - search_range)
        search_end = min(len(flux_zoom), center_idx + search_range + 1)
        local_flux = flux_zoom[search_start:search_end]
        local_peak_idx = np.argmax(local_flux) + search_start
        
        # Clear existing points
        self.selected_manual_points.clear()
        
        # Use smart peak selection at the detected peak
        peak_x = wl_zoom[local_peak_idx]
        peak_y = flux_zoom[local_peak_idx]
        self._smart_peak_selection(peak_x, peak_y, wl_zoom, flux_zoom)
    


    def _clear_selected_points(self):
        """Clear manually selected points"""
        self.selected_manual_points = []
        self._update_selected_points_display()
        if hasattr(self, 'ax_main'):
            self._plot_focused_line()
    
    def _update_selected_points_display(self):
        """Update the selected points counter"""
        # Only update if label exists (Step 2 specific)
        if not hasattr(self, 'selected_points_label'):
            return
            
        count = len(self.selected_manual_points)
        self.selected_points_label.config(text=f"{count} points")
    
    def _analyze_current_line(self):
        """Analyze the currently selected line"""
        if not self.available_lines or self.current_line_index >= len(self.available_lines):
            messagebox.showwarning("No Line Selected", "Please select a line to analyze.")
            return
        
        current_line_name = self.available_lines[self.current_line_index]
        current_wavelength, line_data, line_origin = self._get_line_info(current_line_name)
        
        # Simple analysis based on method
        method = self.method_var.get()
        result_text = f"Analysis of {current_line_name}:\n"
        result_text += f"Wavelength: {current_wavelength:.2f} Å\n"
        result_text += f"Method: {method}\n\n"
        
        try:
            if method == 'manual_points' and self.selected_manual_points:
                # Enhanced manual points analysis
                result_text += f"Manual points selected: {len(self.selected_manual_points)}\n"
                
                # Sort points by wavelength
                sorted_points = sorted(self.selected_manual_points, key=lambda p: p[0])
                wavelengths = [x for x, y in sorted_points]
                fluxes = [y for x, y in sorted_points]
                
                if len(wavelengths) >= 2:
                    width = max(wavelengths) - min(wavelengths)
                    result_text += f"Selected width: {width:.2f} Å\n"
                    
                    # Convert to velocity
                    c_km_s = 299792.458  # Speed of light in km/s
                    velocity_width = (width / current_wavelength) * c_km_s
                    result_text += f"Velocity width: {velocity_width:.1f} km/s\n"
                    
                    # Additional analysis for manual contour
                    if len(fluxes) >= 3:
                        peak_flux = max(fluxes)
                        peak_idx = fluxes.index(peak_flux)
                        peak_wl = wavelengths[peak_idx]
                        
                        result_text += f"Peak flux: {peak_flux:.3f}\n"
                        result_text += f"Peak wavelength: {peak_wl:.2f} Å\n"
                        
                        # Estimate FWHM using manual contour
                        half_max = peak_flux / 2
                        # Find points closest to half maximum
                        left_points = [(w, f) for w, f in zip(wavelengths[:peak_idx], fluxes[:peak_idx])]
                        right_points = [(w, f) for w, f in zip(wavelengths[peak_idx+1:], fluxes[peak_idx+1:])]
                        
                        if left_points and right_points:
                            # Find interpolated half-max points
                            left_wl = wavelengths[0]  # Fallback
                            right_wl = wavelengths[-1]  # Fallback
                            
                            # Better interpolation could be added here
                            estimated_fwhm = right_wl - left_wl
                            estimated_fwhm_vel = (estimated_fwhm / current_wavelength) * c_km_s
                            
                            result_text += f"Estimated FWHM: {estimated_fwhm:.2f} Å ({estimated_fwhm_vel:.1f} km/s)\n"
                    
                    result_text += f"Wavelength range: {min(wavelengths):.2f} - {max(wavelengths):.2f} Å\n"
                else:
                    result_text += "Need at least 2 points for width measurement.\n"
            else:
                # Automatic analysis with fitting
                try:
                    zoom_range = float(self.zoom_range_var.get())
                except:
                    zoom_range = 300.0
                
                fit_result = perform_line_fitting(self.spectrum_data, current_wavelength, method, zoom_range)
                
                if fit_result:
                    # Store fit results for visualization
                    self.line_fit_results[current_line_name] = fit_result
                    
                    # Add fit results to analysis text
                    result_text += fit_result['analysis_text']
                else:
                    result_text += "Fitting failed - insufficient data or poor signal.\n"
                    
            # Store result
            self.line_analysis_results[current_line_name] = result_text
            
            # Update current result display
            self.current_result_text.config(state='normal')
            self.current_result_text.delete('1.0', tk.END)
            self.current_result_text.insert('1.0', result_text)
            self.current_result_text.config(state='disabled')
            
            # Update summary
            self._refresh_summary()
            
        except Exception as e:
            error_text = f"Analysis failed: {str(e)}\n"
            self.current_result_text.config(state='normal')
            self.current_result_text.delete('1.0', tk.END)
            self.current_result_text.insert('1.0', error_text)
            self.current_result_text.config(state='disabled')
    
    def _update_current_result_display(self):
        """Update the current result display when line changes"""
        if not self.available_lines or self.current_line_index >= len(self.available_lines):
            return
        
        current_line_name = self.available_lines[self.current_line_index]
        
        if current_line_name in self.line_analysis_results:
            # Show existing result
            result_text = self.line_analysis_results[current_line_name]
        else:
            # Show default message
            result_text = f"Line: {current_line_name}\nClick 'Analyze Current Line' to see results..."
        
        self.current_result_text.config(state='normal')
        self.current_result_text.delete('1.0', tk.END)
        self.current_result_text.insert('1.0', result_text)
        self.current_result_text.config(state='disabled')
    
    def _refresh_summary(self):
        """Refresh the all-lines summary"""
        summary_text = "Analysis Summary\n"
        summary_text += "=" * 40 + "\n\n"
        
        if not self.line_analysis_results:
            summary_text += "No analyses completed yet.\n"
        else:
            for line_name, result in self.line_analysis_results.items():
                summary_text += f"• {line_name}:\n"
                # Extract key info from result
                lines = result.split('\n')
                for line in lines:
                    if 'FWHM:' in line or 'Velocity width:' in line:
                        summary_text += f"  {line}\n"
                summary_text += "\n"
        
        self.summary_text.config(state='normal')
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert('1.0', summary_text)
        self.summary_text.config(state='disabled')
    
    def _copy_summary_to_clipboard(self):
        """Copy summary to clipboard"""
        content = self.summary_text.get('1.0', tk.END)
        self.dialog.clipboard_clear()
        self.dialog.clipboard_append(content)
        messagebox.showinfo("Copied", "Summary copied to clipboard!")
    
    # === LEGACY METHOD OVERRIDES ===
    
    def _populate_analysis_selection(self):
        """Legacy method - now redirects to line dropdown population"""
        self._populate_line_dropdown()
    
    def _select_all_for_analysis(self):
        """Legacy method - not used in single-line mode"""
        pass
    
    def _select_none_for_analysis(self):
        """Legacy method - not used in single-line mode"""
        pass
    
    def _update_analysis_selection(self):
        """Legacy method - not used in single-line mode"""
        pass
    
    def _run_analysis(self):
        """Legacy method - redirects to current line analysis"""
        self._analyze_current_line()
    
    def _display_analysis_results(self):
        """Legacy method - redirects to summary refresh"""
        self._refresh_summary()
    
    def _update_results_display(self, text):
        """Legacy method - redirects to current result display"""
        if hasattr(self, 'current_result_text'):
            self.current_result_text.config(state='normal')
            self.current_result_text.delete(1.0, tk.END)
            self.current_result_text.insert(1.0, text)
            self.current_result_text.config(state='disabled')
    
    def _copy_results_to_clipboard(self):
        """Legacy method - redirects to summary copy"""
        self._copy_summary_to_clipboard()
    
    def _update_redshift_source_display(self):
        """Update the explanatory redshift info label"""
        info_text = f"Source: {self.galaxy_redshift_source}. SN lines shifted by vₑₓₚ."
        self.redshift_info_label.configure(text=info_text)
    
    def _setup_dynamic_text_wrapping(self):
        """Set up dynamic text wrapping for the dialog"""
        # Bind resize event to adjust text wraplengths
        if hasattr(self, 'options_frame'):
            self.options_frame.bind('<Configure>', self._on_options_frame_resize)
            
            # Set initial wraplength based on current frame width
            initial_width = self.options_frame.winfo_width()
            if initial_width > 50:  # Only if frame has been properly initialized
                self._update_text_wraplengths(initial_width - 40)  # Leave 40px margin
    
    def _on_options_frame_resize(self, event):
        """Handle resize events for the options frame"""
        try:
            new_width = event.width
            # Avoid excessive updates by checking for significant change
            if not hasattr(self, '_last_wrap_width') or abs(new_width - self._last_wrap_width) > 10:
                self._last_wrap_width = new_width
                # Leave adequate horizontal padding (40px total) so text doesn't touch edges
                effective_width = max(150, new_width - 40)
                self._update_text_wraplengths(effective_width)
        except Exception:
            pass  # Fail-safe – UI robustness over detailed error handling
    
    def _update_text_wraplengths(self, wrap_len):
        """Update wraplength for text widgets in the options frame"""
        # Safety guard – ensure positive wraplength with adequate margin
        wrap_len = max(100, wrap_len)
        
        def recurse(widget):
            for child in widget.winfo_children():
                # Recursively process the entire widget tree
                recurse(child)
                # Apply to widgets that support wraplength (Label, Checkbutton, Radiobutton)
                if isinstance(child, (tk.Label, tk.Checkbutton, tk.Radiobutton)):
                    try:
                        # Only update wraplength if the widget doesn't have very short text
                        text = child.cget('text') if hasattr(child, 'cget') else ''
                        if len(text) > 50:  # Only wrap longer text to prevent unnecessary wrapping
                            child.configure(wraplength=wrap_len)
                    except (tk.TclError, AttributeError):
                        # Some themed widgets may not expose wraplength or text – ignore
                        pass
        if hasattr(self, 'options_frame'):
            recurse(self.options_frame)



def show_multi_step_emission_dialog(parent, spectrum_data: Dict[str, np.ndarray], 
                                   theme_manager, galaxy_redshift: float = 0.0,
                                   cluster_median_redshift: float = 0.0) -> Optional[Dict[str, Any]]:
    """
    Show multi-step emission line analysis dialog.
    
    Args:
        parent: Parent window
        spectrum_data: Dictionary with 'wavelength' and 'flux' arrays
        theme_manager: Theme manager for consistent styling
        galaxy_redshift: Initial galaxy redshift estimate
        cluster_median_redshift: Cluster median redshift for reference
        
    Returns:
        Analysis results dictionary or None if cancelled
    """
    dialog = MultiStepEmissionAnalysisDialog(parent, spectrum_data, theme_manager, 
                                           galaxy_redshift, cluster_median_redshift)
    return dialog.show() 
