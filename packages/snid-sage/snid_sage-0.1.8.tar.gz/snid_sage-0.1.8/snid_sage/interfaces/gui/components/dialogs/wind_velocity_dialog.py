"""
SNID SAGE - Wind Velocity Analysis Dialog
=========================================

Interactive dialog for measuring wind velocities from P-Cygni profiles in supernova spectra.
Allows users to interactively mark emission peaks and absorption minima to calculate wind velocities.

Features:
- Zoomed view of selected emission line
- Interactive marker placement for emission/absorption features
- Real-time wind velocity calculation using Doppler formula
- Results saving and export capabilities
- Integration with main emission line overlay system

Part of the SNID SAGE GUI system.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import Cursor
from typing import Dict, List, Optional, Tuple, Any
import json
from datetime import datetime
import os

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.wind_velocity')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.wind_velocity')

# Import physical constants
try:
    from snid_sage.shared.constants.physical import SPEED_OF_LIGHT_KMS
except ImportError:
    SPEED_OF_LIGHT_KMS = 299792.458

# Import unified systems for consistent styling
try:
    from snid_sage.interfaces.gui.utils.universal_window_manager import get_window_manager, DialogSize
    from snid_sage.interfaces.gui.utils.unified_font_manager import get_font_manager, FontCategory
    from snid_sage.interfaces.gui.utils.no_title_plot_manager import get_plot_manager
    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError:
    UNIFIED_SYSTEMS_AVAILABLE = False


class WindVelocityAnalysisDialog:
    """Interactive wind velocity analysis dialog for supernova emission lines"""
    
    def __init__(self, parent, line_name, line_data, spectrum_data, theme_manager, current_redshift=0.0):
        """
        Initialize the wind velocity analysis dialog
        
        Args:
            parent: Parent window
            line_name: Name of the emission line
            line_data: Dictionary containing line information
            spectrum_data: Dictionary containing wavelength and flux data
            theme_manager: Theme manager for consistent styling
            current_redshift: Current redshift for line positioning
        """
        self.parent = parent
        self.line_name = line_name
        self.line_data = line_data
        self.spectrum_data = spectrum_data
        self.theme_manager = theme_manager
        self.current_redshift = current_redshift
        
        # Get managers
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager = get_window_manager()
            self.font_manager = get_font_manager()
            self.plot_manager = get_plot_manager()
        
        # Analysis state
        self.marker_mode = None  # 'emission', 'absorption', or None
        self.emission_marker = None
        self.absorption_marker = None
        self.emission_wavelength = None
        self.absorption_wavelength = None
        self.wind_velocity = None
        
        # Measurement results storage
        self.measurement_results = []
        self.saved_measurements = []
        
        # UI components
        self.dialog = None
        self.fig = None
        self.ax = None
        self.canvas = None
        self.cursor = None
        
        # Zoom parameters
        self.zoom_range = 200  # ±200 Å around line
        self.zoomed_wave = None
        self.zoomed_flux = None
        
        self._setup_colors()
        self._prepare_spectrum_data()
        self._create_dialog()
        self._create_interface()
        self._plot_zoomed_spectrum()
        self._center_dialog()
        
        _LOGGER.info(f"Wind velocity analysis dialog opened for line: {line_name}")
    
    def _setup_colors(self):
        """Setup color scheme consistent with main overlay"""
        self.colors = {
            'bg_main': '#1e1e1e',
            'bg_panel': '#2d2d2d',
            'bg_control': '#3a3a3a',
            'button_bg': '#484848',
            'button_active': '#0078d4',
            'button_emission': '#ff4444',    # Red for emission marker
            'button_absorption': '#4444ff',  # Blue for absorption marker
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'success': '#107c10',
            'warning': '#ff8c00',
            'error': '#d13438',
            'marker_emission': '#ff4444',    # Red marker
            'marker_absorption': '#4444ff',  # Blue marker
            'line_color': '#44cccc',         # Cyan for spectrum line
            'grid_color': '#444444'
        }
    
    def _prepare_spectrum_data(self):
        """Prepare and filter spectrum data for the selected line"""
        try:
            # Get spectrum data
            wavelength = np.array(self.spectrum_data.get('wavelength', []))
            flux = np.array(self.spectrum_data.get('flux', []))
            
            if len(wavelength) == 0 or len(flux) == 0:
                raise ValueError("Empty spectrum data")
            
            # Calculate observed wavelength of the line
            rest_wavelength = self.line_data.get('wavelength', 0)
            observed_wavelength = rest_wavelength * (1 + self.current_redshift)
            
            # Define zoom range around the line
            wave_min = observed_wavelength - self.zoom_range
            wave_max = observed_wavelength + self.zoom_range
            
            # Filter spectrum to zoom range
            mask = (wavelength >= wave_min) & (wavelength <= wave_max)
            if not np.any(mask):
                # Expand range if no data in initial range
                self.zoom_range = 500
                wave_min = observed_wavelength - self.zoom_range
                wave_max = observed_wavelength + self.zoom_range
                mask = (wavelength >= wave_min) & (wavelength <= wave_max)
            
            self.zoomed_wave = wavelength[mask]
            self.zoomed_flux = flux[mask]
            self.observed_wavelength = observed_wavelength
            self.rest_wavelength = rest_wavelength
            
            _LOGGER.debug(f"Prepared spectrum data: {len(self.zoomed_wave)} points, range {wave_min:.1f}-{wave_max:.1f}Å")
            
        except Exception as e:
            _LOGGER.error(f"Error preparing spectrum data: {e}")
            self.zoomed_wave = np.array([])
            self.zoomed_flux = np.array([])
    
    def _create_dialog(self):
        """Create the main dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(f"🌪️ Wind Velocity Analysis - {self.line_name}")
        
        # Set window size and properties
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager.setup_dialog(self.dialog, f"🌪️ Wind Velocity Analysis - {self.line_name}", DialogSize.LARGE)
        else:
            self.dialog.geometry("1200x800")
            self.dialog.resizable(True, True)
        
        self.dialog.configure(bg=self.colors['bg_main'])
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Keyboard bindings
        self.dialog.bind('<F11>', self._toggle_fullscreen)
        self.dialog.bind('<Escape>', self._close_dialog)
        self.dialog.bind('<Key-e>', lambda e: self._set_marker_mode('emission'))
        self.dialog.bind('<Key-a>', lambda e: self._set_marker_mode('absorption'))
        self.dialog.bind('<Key-c>', lambda e: self._clear_markers())
        
        self.dialog.focus_set()
        
        # Window close protocol
        self.dialog.protocol("WM_DELETE_WINDOW", self._close_dialog)
    
    def _create_interface(self):
        """Create the user interface"""
        # Main container
        main_container = tk.Frame(self.dialog, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Top info panel
        self._create_info_panel(main_container)
        
        # Control panel
        self._create_control_panel(main_container)
        
        # Main content area with results and plot
        content_frame = tk.Frame(main_container, bg=self.colors['bg_main'])
        content_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Left results panel
        self._create_results_panel(content_frame)
        
        # Right plot area
        plot_frame = tk.Frame(content_frame, bg=self.colors['bg_panel'])
        plot_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self._create_plot(plot_frame)
    
    def _create_info_panel(self, parent):
        """Create information panel about the selected line"""
        info_frame = tk.Frame(parent, bg=self.colors['bg_control'], relief='raised', bd=1)
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Line information
        info_content = tk.Frame(info_frame, bg=self.colors['bg_control'])
        info_content.pack(fill='x', padx=15, pady=10)
        
        # Get font sizes
        if UNIFIED_SYSTEMS_AVAILABLE:
            header_font = self.font_manager.get_font(FontCategory.HEADER_MEDIUM)
            body_font = self.font_manager.get_font(FontCategory.BODY_NORMAL)
        else:
            header_font = ('Segoe UI', 14, 'bold')
            body_font = ('Segoe UI', 11)
        
        # Title
        title_label = tk.Label(info_content, text=f"🔬 Wind Velocity Analysis: {self.line_name}",
                              font=header_font, bg=self.colors['bg_control'], fg=self.colors['text_primary'])
        title_label.pack(anchor='w', pady=(0, 5))
        
        # Line details
        details_frame = tk.Frame(info_content, bg=self.colors['bg_control'])
        details_frame.pack(fill='x')
        
        # Rest wavelength
        rest_wave_text = f"Rest λ: {self.rest_wavelength:.2f} Å"
        tk.Label(details_frame, text=rest_wave_text, font=body_font,
                bg=self.colors['bg_control'], fg=self.colors['text_secondary']).pack(side='left')
        
        # Observed wavelength
        obs_wave_text = f"Observed λ: {self.observed_wavelength:.2f} Å"
        tk.Label(details_frame, text=obs_wave_text, font=body_font,
                bg=self.colors['bg_control'], fg=self.colors['text_secondary']).pack(side='left', padx=(20, 0))
        
        # Element/category
        category = self.line_data.get('category', 'unknown')
        element_text = f"Element: {category.title()}"
        tk.Label(details_frame, text=element_text, font=body_font,
                bg=self.colors['bg_control'], fg=self.colors['text_secondary']).pack(side='left', padx=(20, 0))
        
        # Current redshift
        redshift_text = f"Redshift: z = {self.current_redshift:.6f}"
        tk.Label(details_frame, text=redshift_text, font=body_font,
                bg=self.colors['bg_control'], fg=self.colors['text_secondary']).pack(side='right')
    
    def _create_control_panel(self, parent):
        """Create control panel with marker tools"""
        control_frame = tk.Frame(parent, bg=self.colors['bg_control'], relief='raised', bd=1)
        control_frame.pack(fill='x', pady=(0, 10))
        
        control_content = tk.Frame(control_frame, bg=self.colors['bg_control'])
        control_content.pack(fill='x', padx=15, pady=10)
        
        # Get fonts
        if UNIFIED_SYSTEMS_AVAILABLE:
            button_font = self.font_manager.get_font(FontCategory.BUTTON)
        else:
            button_font = ('Segoe UI', 11)
        
        # Instructions
        instructions = "📍 Click buttons below to activate marker mode, then click on spectrum to place markers"
        tk.Label(control_content, text=instructions, font=('Segoe UI', 10),
                bg=self.colors['bg_control'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 8))
        
        # Marker control buttons
        button_frame = tk.Frame(control_content, bg=self.colors['bg_control'])
        button_frame.pack(fill='x')
        
        # Emission marker button
        self.emission_btn = tk.Button(button_frame, text="📍 Mark Emission Peak (E)",
                                     font=button_font, bg=self.colors['button_emission'], fg='white',
                                     relief='flat', bd=0, pady=8, cursor='hand2',
                                     command=lambda: self._set_marker_mode('emission'))
        self.emission_btn.pack(side='left', padx=(0, 10))
        
        # Absorption marker button
        self.absorption_btn = tk.Button(button_frame, text="📍 Mark Absorption Min (A)",
                                       font=button_font, bg=self.colors['button_absorption'], fg='white',
                                       relief='flat', bd=0, pady=8, cursor='hand2',
                                       command=lambda: self._set_marker_mode('absorption'))
        self.absorption_btn.pack(side='left', padx=(0, 20))
        
        # Clear markers button
        self.clear_btn = tk.Button(button_frame, text="🗑️ Clear Markers (C)",
                                  font=button_font, bg=self.colors['button_bg'], fg=self.colors['text_primary'],
                                  relief='flat', bd=0, pady=8, cursor='hand2',
                                  command=self._clear_markers)
        self.clear_btn.pack(side='left', padx=(0, 20))
        
        # Mode indicator
        self.mode_label = tk.Label(button_frame, text="Mode: Click a button to start",
                                  font=('Segoe UI', 11, 'bold'), bg=self.colors['bg_control'], fg=self.colors['text_secondary'])
        self.mode_label.pack(side='right')
    
    def _create_results_panel(self, parent):
        """Create results display panel"""
        results_frame = tk.Frame(parent, bg=self.colors['bg_panel'], relief='raised', bd=1)
        results_frame.pack(side='left', fill='y', padx=(0, 10))
        results_frame.config(width=300)
        results_frame.pack_propagate(False)
        
        # Results header
        header_frame = tk.Frame(results_frame, bg=self.colors['bg_control'])
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        if UNIFIED_SYSTEMS_AVAILABLE:
            header_font = self.font_manager.get_font(FontCategory.HEADER_MEDIUM)
        else:
            header_font = ('Segoe UI', 13, 'bold')
        
        tk.Label(header_frame, text="🌪️ Wind Velocity Results", font=header_font,
                bg=self.colors['bg_control'], fg=self.colors['text_primary']).pack()
        
        # Current measurement section
        current_frame = tk.Frame(results_frame, bg=self.colors['bg_panel'])
        current_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(current_frame, text="Current Measurement:", font=('Segoe UI', 11, 'bold'),
                bg=self.colors['bg_panel'], fg=self.colors['text_primary']).pack(anchor='w')
        
        # Wavelength displays
        self.emission_wave_label = tk.Label(current_frame, text="Emission λ: --",
                                           font=('Segoe UI', 10), bg=self.colors['bg_panel'], fg=self.colors['text_secondary'])
        self.emission_wave_label.pack(anchor='w', pady=(5, 0))
        
        self.absorption_wave_label = tk.Label(current_frame, text="Absorption λ: --",
                                             font=('Segoe UI', 10), bg=self.colors['bg_panel'], fg=self.colors['text_secondary'])
        self.absorption_wave_label.pack(anchor='w')
        
        # Wind velocity display
        self.velocity_label = tk.Label(current_frame, text="Wind Velocity: --",
                                      font=('Segoe UI', 12, 'bold'), bg=self.colors['bg_panel'], fg=self.colors['success'])
        self.velocity_label.pack(anchor='w', pady=(10, 0))
        
        # Save current measurement button
        self.save_current_btn = tk.Button(current_frame, text="💾 Save Current",
                                         font=('Segoe UI', 10), bg=self.colors['success'], fg='white',
                                         relief='flat', bd=0, pady=5, cursor='hand2',
                                         command=self._save_current_measurement, state='disabled')
        self.save_current_btn.pack(fill='x', pady=(10, 0))
        
        # Separator
        separator = tk.Frame(results_frame, height=2, bg=self.colors['text_secondary'])
        separator.pack(fill='x', padx=20, pady=15)
        
        # Saved measurements section
        saved_frame = tk.Frame(results_frame, bg=self.colors['bg_panel'])
        saved_frame.pack(fill='both', expand=True, padx=10)
        
        tk.Label(saved_frame, text="Saved Measurements:", font=('Segoe UI', 11, 'bold'),
                bg=self.colors['bg_panel'], fg=self.colors['text_primary']).pack(anchor='w')
        
        # Measurements listbox
        list_frame = tk.Frame(saved_frame, bg=self.colors['bg_panel'])
        list_frame.pack(fill='both', expand=True, pady=(5, 10))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.measurements_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                              bg=self.colors['bg_control'], fg=self.colors['text_primary'],
                                              selectbackground=self.colors['button_active'],
                                              font=('Segoe UI', 9))
        self.measurements_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.measurements_listbox.yview)
        
        # Action buttons
        action_frame = tk.Frame(saved_frame, bg=self.colors['bg_panel'])
        action_frame.pack(fill='x', pady=(0, 10))
        
        self.export_btn = tk.Button(action_frame, text="📊 Export All",
                                   font=('Segoe UI', 10), bg=self.colors['button_active'], fg='white',
                                   relief='flat', bd=0, pady=5, cursor='hand2',
                                   command=self._export_measurements, state='disabled')
        self.export_btn.pack(fill='x', pady=(0, 5))
        
        self.clear_all_btn = tk.Button(action_frame, text="🗑️ Clear All",
                                      font=('Segoe UI', 10), bg=self.colors['error'], fg='white',
                                      relief='flat', bd=0, pady=5, cursor='hand2',
                                      command=self._clear_all_measurements, state='disabled')
        self.clear_all_btn.pack(fill='x')
    
    def _create_plot(self, parent):
        """Create the spectrum plot"""
        # Create matplotlib figure
        self.fig = plt.figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111)
        
        # Apply no-title styling if available
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.plot_manager.apply_no_title_styling(self.fig, self.ax)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add toolbar
        toolbar_frame = tk.Frame(parent, bg=self.colors['bg_panel'])
        toolbar_frame.pack(fill='x')
        
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Connect click events
        self.canvas.mpl_connect('button_press_event', self._on_plot_click)
        self.canvas.mpl_connect('motion_notify_event', self._on_plot_hover)
        
        # Add cursor for precise positioning
        self.cursor = Cursor(self.ax, useblit=True, color='yellow', linewidth=1)
    
    def _plot_zoomed_spectrum(self):
        """Plot the zoomed spectrum around the selected line"""
        if len(self.zoomed_wave) == 0:
            self.ax.text(0.5, 0.5, 'No spectrum data in range', transform=self.ax.transAxes,
                        ha='center', va='center', fontsize=14, color='red')
            self.canvas.draw()
            return
        
        # Clear previous plot
        self.ax.clear()
        
        # Plot spectrum
        self.ax.plot(self.zoomed_wave, self.zoomed_flux, color=self.colors['line_color'], 
                    linewidth=1.5, alpha=0.8, label='Spectrum')
        
        # Mark the rest wavelength position (corrected for redshift)
        self.ax.axvline(self.observed_wavelength, color='orange', linestyle='--', 
                       linewidth=2, alpha=0.7, label=f'{self.line_name} (rest)')
        
        # Styling
        self.ax.set_xlabel('Wavelength (Å)', fontsize=12, color=self.colors['text_primary'])
        self.ax.set_ylabel('Flux', fontsize=12, color=self.colors['text_primary'])
        self.ax.grid(True, alpha=0.3, color=self.colors['grid_color'])
        
        # Set dark background
        self.ax.set_facecolor('#2d2d2d')
        self.fig.patch.set_facecolor('#1e1e1e')
        
        # Color the tick labels
        self.ax.tick_params(colors=self.colors['text_primary'])
        
        # Legend
        self.ax.legend(loc='upper right', fancybox=True, framealpha=0.9)
        
        # Apply no-title styling
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.plot_manager.apply_no_title_styling(self.fig, self.ax)
        
        plt.tight_layout(pad=0.5)
        self.canvas.draw()
    
    def _set_marker_mode(self, mode):
        """Set the current marker mode"""
        self.marker_mode = mode
        
        # Update button states
        if mode == 'emission':
            self.emission_btn.config(bg=self.colors['button_active'])
            self.absorption_btn.config(bg=self.colors['button_absorption'])
            self.mode_label.config(text="Mode: Click to mark EMISSION peak", fg=self.colors['marker_emission'])
        elif mode == 'absorption':
            self.emission_btn.config(bg=self.colors['button_emission'])
            self.absorption_btn.config(bg=self.colors['button_active'])
            self.mode_label.config(text="Mode: Click to mark ABSORPTION minimum", fg=self.colors['marker_absorption'])
        else:
            self.emission_btn.config(bg=self.colors['button_emission'])
            self.absorption_btn.config(bg=self.colors['button_absorption'])
            self.mode_label.config(text="Mode: Click a button to start", fg=self.colors['text_secondary'])
        
        _LOGGER.debug(f"Marker mode set to: {mode}")
    
    def _on_plot_click(self, event):
        """Handle clicks on the spectrum plot"""
        if event.inaxes != self.ax or event.xdata is None or self.marker_mode is None:
            return
        
        click_wavelength = event.xdata
        
        if self.marker_mode == 'emission':
            self._place_emission_marker(click_wavelength)
        elif self.marker_mode == 'absorption':
            self._place_absorption_marker(click_wavelength)
        
        self._calculate_wind_velocity()
        self._update_results_display()
    
    def _place_emission_marker(self, wavelength):
        """Place emission peak marker"""
        # Remove existing emission marker
        if self.emission_marker is not None:
            try:
                self.emission_marker.remove()
            except:
                pass
        
        # Find flux at this wavelength for marker height
        flux_idx = np.argmin(np.abs(self.zoomed_wave - wavelength))
        marker_height = self.zoomed_flux[flux_idx]
        
        # Place new marker
        self.emission_marker = self.ax.scatter([wavelength], [marker_height], 
                                             c=self.colors['marker_emission'], s=100, 
                                             marker='^', zorder=5, label='Emission Peak')
        
        self.emission_wavelength = wavelength
        
        # Add vertical line
        self.ax.axvline(wavelength, color=self.colors['marker_emission'], 
                       linestyle=':', alpha=0.7, linewidth=2)
        
        self.canvas.draw()
        _LOGGER.debug(f"Emission marker placed at {wavelength:.2f} Å")
    
    def _place_absorption_marker(self, wavelength):
        """Place absorption minimum marker"""
        # Remove existing absorption marker
        if self.absorption_marker is not None:
            try:
                self.absorption_marker.remove()
            except:
                pass
        
        # Find flux at this wavelength for marker height
        flux_idx = np.argmin(np.abs(self.zoomed_wave - wavelength))
        marker_height = self.zoomed_flux[flux_idx]
        
        # Place new marker
        self.absorption_marker = self.ax.scatter([wavelength], [marker_height], 
                                               c=self.colors['marker_absorption'], s=100, 
                                               marker='v', zorder=5, label='Absorption Min')
        
        self.absorption_wavelength = wavelength
        
        # Add vertical line
        self.ax.axvline(wavelength, color=self.colors['marker_absorption'], 
                       linestyle=':', alpha=0.7, linewidth=2)
        
        self.canvas.draw()
        _LOGGER.debug(f"Absorption marker placed at {wavelength:.2f} Å")
    
    def _calculate_wind_velocity(self):
        """Calculate wind velocity from placed markers"""
        if self.emission_wavelength is None or self.absorption_wavelength is None:
            self.wind_velocity = None
            return
        
        # Calculate velocity using Doppler formula
        # v = c × |λ_emission - λ_absorption| / λ_rest
        delta_lambda = abs(self.emission_wavelength - self.absorption_wavelength)
        velocity_km_s = (delta_lambda / self.rest_wavelength) * SPEED_OF_LIGHT_KMS
        
        self.wind_velocity = velocity_km_s
        
        _LOGGER.debug(f"Calculated wind velocity: {velocity_km_s:.1f} km/s")
    
    def _update_results_display(self):
        """Update the results display with current measurements"""
        # Update wavelength labels
        if self.emission_wavelength is not None:
            self.emission_wave_label.config(text=f"Emission λ: {self.emission_wavelength:.2f} Å")
        else:
            self.emission_wave_label.config(text="Emission λ: --")
        
        if self.absorption_wavelength is not None:
            self.absorption_wave_label.config(text=f"Absorption λ: {self.absorption_wavelength:.2f} Å")
        else:
            self.absorption_wave_label.config(text="Absorption λ: --")
        
        # Update velocity label
        if self.wind_velocity is not None:
            self.velocity_label.config(text=f"Wind Velocity: {self.wind_velocity:.1f} km/s")
            self.save_current_btn.config(state='normal')
        else:
            self.velocity_label.config(text="Wind Velocity: --")
            self.save_current_btn.config(state='disabled')
    
    def _clear_markers(self):
        """Clear all markers and reset measurements"""
        # Remove markers from plot
        if self.emission_marker is not None:
            try:
                self.emission_marker.remove()
            except:
                pass
            self.emission_marker = None
        
        if self.absorption_marker is not None:
            try:
                self.absorption_marker.remove()
            except:
                pass
            self.absorption_marker = None
        
        # Clear measurements
        self.emission_wavelength = None
        self.absorption_wavelength = None
        self.wind_velocity = None
        
        # Reset mode
        self.marker_mode = None
        self._set_marker_mode(None)
        
        # Update display
        self._update_results_display()
        
        # Redraw plot
        self._plot_zoomed_spectrum()
        
        _LOGGER.debug("Markers cleared")
    
    def _save_current_measurement(self):
        """Save the current measurement to the results list"""
        if self.wind_velocity is None:
            return
        
        # Create measurement record
        measurement = {
            'timestamp': datetime.now().isoformat(),
            'line_name': self.line_name,
            'rest_wavelength': self.rest_wavelength,
            'emission_wavelength': self.emission_wavelength,
            'absorption_wavelength': self.absorption_wavelength,
            'wind_velocity': self.wind_velocity,
            'redshift': self.current_redshift
        }
        
        # Add to saved measurements
        self.saved_measurements.append(measurement)
        
        # Update listbox
        display_text = f"{len(self.saved_measurements)}. v = {self.wind_velocity:.1f} km/s"
        self.measurements_listbox.insert(tk.END, display_text)
        
        # Enable buttons
        self.export_btn.config(state='normal')
        self.clear_all_btn.config(state='normal')
        
        # Clear current measurement
        self._clear_markers()
        
        if self.wind_velocity is not None:
            _LOGGER.info(f"Saved wind velocity measurement: {self.wind_velocity:.1f} km/s for {self.line_name}")
        else:
            _LOGGER.info(f"Saved wind velocity measurement (no velocity calculated) for {self.line_name}")
    
    def _clear_all_measurements(self):
        """Clear all saved measurements"""
        if not self.saved_measurements:
            return
        
        result = messagebox.askyesno("Clear All Measurements", 
                                   "Are you sure you want to clear all saved measurements?",
                                   parent=self.dialog)
        
        if result:
            self.saved_measurements.clear()
            self.measurements_listbox.delete(0, tk.END)
            self.export_btn.config(state='disabled')
            self.clear_all_btn.config(state='disabled')
            
            _LOGGER.info("Cleared all wind velocity measurements")
    
    def _export_measurements(self):
        """Export measurements to file"""
        if not self.saved_measurements:
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            parent=self.dialog,
            title="Export Wind Velocity Measurements",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if not filename:
            return
        
        try:
            if filename.lower().endswith('.csv'):
                self._export_to_csv(filename)
            else:
                self._export_to_json(filename)
            
            messagebox.showinfo("Export Successful", 
                              f"Measurements exported to:\n{filename}",
                              parent=self.dialog)
            
            _LOGGER.info(f"Exported {len(self.saved_measurements)} measurements to {filename}")
            
        except Exception as e:
            _LOGGER.error(f"Error exporting measurements: {e}")
            messagebox.showerror("Export Error", f"Failed to export measurements:\n{str(e)}", 
                               parent=self.dialog)
    
    def _export_to_json(self, filename):
        """Export measurements to JSON format"""
        export_data = {
            'line_name': self.line_name,
            'line_data': self.line_data,
            'analysis_info': {
                'rest_wavelength': self.rest_wavelength,
                'redshift': self.current_redshift,
                'export_timestamp': datetime.now().isoformat()
            },
            'measurements': self.saved_measurements
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def _export_to_csv(self, filename):
        """Export measurements to CSV format"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Measurement_Number', 'Line_Name', 'Rest_Wavelength_A', 
                'Emission_Wavelength_A', 'Absorption_Wavelength_A', 
                'Wind_Velocity_km_s', 'Redshift', 'Timestamp'
            ])
            
            # Data
            for i, measurement in enumerate(self.saved_measurements, 1):
                writer.writerow([
                    i, measurement['line_name'], measurement['rest_wavelength'],
                    measurement['emission_wavelength'], measurement['absorption_wavelength'],
                    measurement['wind_velocity'], measurement['redshift'], 
                    measurement['timestamp']
                ])
    
    def _on_plot_hover(self, event):
        """Handle mouse hover over plot for coordinate display"""
        if event.inaxes != self.ax or event.xdata is None:
            return
        
        # Update cursor position in status (could add status bar if needed)
        pass
    
    def _toggle_fullscreen(self, event):
        """Toggle fullscreen mode"""
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager.toggle_fullscreen(self.dialog)
    
    def _center_dialog(self):
        """Center the dialog on screen"""
        if UNIFIED_SYSTEMS_AVAILABLE:
            self.window_manager.center_dialog("wind_velocity_dialog")
        else:
            self.dialog.update_idletasks()
            width = self.dialog.winfo_width()
            height = self.dialog.winfo_height()
            x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
            self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _close_dialog(self):
        """Close the dialog"""
        try:
            self.dialog.destroy()
            _LOGGER.info(f"Wind velocity analysis dialog closed for {self.line_name}")
        except:
            pass
    
    def get_results(self):
        """Get all saved measurement results"""
        return {
            'line_name': self.line_name,
            'measurements': self.saved_measurements,
            'total_measurements': len(self.saved_measurements)
        }


def show_wind_velocity_dialog(parent, line_name, line_data, spectrum_data, theme_manager, current_redshift=0.0):
    """
    Show the wind velocity analysis dialog
    
    Args:
        parent: Parent window
        line_name: Name of the emission line
        line_data: Dictionary containing line information
        spectrum_data: Dictionary containing wavelength and flux data
        theme_manager: Theme manager for consistent styling
        current_redshift: Current redshift for line positioning
    
    Returns:
        WindVelocityAnalysisDialog instance
    """
    return WindVelocityAnalysisDialog(parent, line_name, line_data, spectrum_data, theme_manager, current_redshift)
