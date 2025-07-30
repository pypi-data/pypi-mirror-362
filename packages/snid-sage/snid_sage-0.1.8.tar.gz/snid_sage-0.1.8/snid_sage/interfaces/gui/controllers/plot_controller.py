"""
Plot Controller for SNID SAGE GUI

Manages all plotting operations including:
- Plot initialization and theme application
- View switching between flux and flat views
- Template navigation and display
- Matplotlib configuration and management

Extracted from sage_gui.py to improve maintainability.
"""

import os
import numpy as np
import logging

# Defer matplotlib import until needed
_matplotlib_imported = False

# Import unified systems for consistent plot styling
try:
    from snid_sage.interfaces.gui.utils.no_title_plot_manager import apply_no_title_styling
    from snid_sage.interfaces.gui.utils.unified_font_manager import get_font_manager, FontCategory
    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError:
    UNIFIED_SYSTEMS_AVAILABLE = False

_LOGGER = logging.getLogger(__name__)

def _import_matplotlib():
    """Lazy import of matplotlib to speed up startup"""
    global _matplotlib_imported
    if not _matplotlib_imported:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        
        globals()['plt'] = plt
        globals()['FigureCanvasTkAgg'] = FigureCanvasTkAgg 
        globals()['NavigationToolbar2Tk'] = NavigationToolbar2Tk
        _matplotlib_imported = True
        return plt, FigureCanvasTkAgg, NavigationToolbar2Tk
    else:
        return globals()['plt'], globals()['FigureCanvasTkAgg'], globals()['NavigationToolbar2Tk']


class PlotController:
    """Controller for managing all plotting operations"""
    
    def __init__(self, gui_instance):
        """Initialize plot controller"""
        self.gui = gui_instance
        self.current_view = 'flux'
        self.current_template = 0
        
        # NEW: Plot state management for ensuring proper swapping
        self.current_plot_type = None  # Track current plot type ('spectrum', 'gmm', 'redshift_age', etc.)
        self.last_spectrum_view = 'flux'  # Remember last spectrum view (flux/flat)
        self.plot_stack = []  # Track plot history for proper restoration
        
    def init_matplotlib_plot(self):
        """Initialize matplotlib plot area"""
        try:
            # Configure matplotlib backend before any operations
            self._ensure_matplotlib_backend_configured()
            
            # Import matplotlib components
            plt, FigureCanvasTkAgg, NavigationToolbar2Tk = _import_matplotlib()
            
            # Check if matplotlib components already exist and are valid
            if self._matplotlib_components_valid():
                _LOGGER.debug("✅ Matplotlib components already exist and are valid - reusing")
                return
            
            # Close any orphaned matplotlib figures to prevent window splitting
            plt.close('all')
            
            # Create matplotlib figure - increased size for better GMM plot visibility
            self.gui.fig = plt.Figure(figsize=(12, 8), dpi=100, tight_layout=True)
            self.gui.ax = self.gui.fig.add_subplot(111)
            
            # Create canvas
            if hasattr(self.gui, 'init_matplotlib_plot_area'):
                plot_frame = self.gui.init_matplotlib_plot_area
                
                # Destroy any existing toolbar and canvas to prevent widget conflicts
                if hasattr(self.gui, 'toolbar') and self.gui.toolbar:
                    try:
                        if self.gui.toolbar.winfo_exists():
                            self.gui.toolbar.destroy()
                        _LOGGER.debug("🧹 Old toolbar destroyed")
                    except Exception as e:
                        _LOGGER.debug(f"Warning cleaning up old toolbar: {e}")
                    finally:
                        self.gui.toolbar = None
                        
                if hasattr(self.gui, 'canvas') and self.gui.canvas:
                    try:
                        old_widget = self.gui.canvas.get_tk_widget()
                        if old_widget and old_widget.winfo_exists():
                            old_widget.destroy()
                        _LOGGER.debug("🧹 Old canvas destroyed")
                    except Exception as e:
                        _LOGGER.debug(f"Warning cleaning up old canvas: {e}")
                
                # Create canvas with explicit parent to prevent window splitting
                self.gui.canvas = FigureCanvasTkAgg(self.gui.fig, master=plot_frame)
                canvas_widget = self.gui.canvas.get_tk_widget()
                
                # Configure canvas widget to stay embedded and fill all available space
                canvas_widget.configure(highlightthickness=0)
                canvas_widget.pack(fill='both', expand=True, padx=0, pady=0)
                
                # Ensure canvas stays within the GUI
                canvas_widget.focus_set()
                
                # Draw the canvas
                self.gui.canvas.draw()
                
                # Add toolbar and store reference for proper cleanup
                self.gui.toolbar = NavigationToolbar2Tk(self.gui.canvas, plot_frame)
                self.gui.toolbar.update()
                
                # Exclude the toolbar and its children from global theming so the icons keep their native colours
                try:
                    self.gui.toolbar._workflow_managed = True  # Skip UnifiedThemeManager styling
                    for child in self.gui.toolbar.winfo_children():
                        child._workflow_managed = True
                        # Also mark grandchildren just in case
                        for grand in child.winfo_children():
                            grand._workflow_managed = True
                except Exception:
                    pass
                
                # Apply theme to plot
                self._apply_plot_theme()
                
                _LOGGER.info("✅ Matplotlib plot initialized with embedded canvas")
            else:
                _LOGGER.debug("⚠️ Plot area not ready yet")
                
        except Exception as e:
            _LOGGER.error(f"Error initializing matplotlib plot: {e}")
            import traceback
            traceback.print_exc()
    
    def _matplotlib_components_valid(self):
        """Check if matplotlib components exist and are properly connected"""
        try:
            # Check if all essential components exist (including toolbar)
            if not (hasattr(self.gui, 'fig') and hasattr(self.gui, 'ax') and 
                    hasattr(self.gui, 'canvas') and hasattr(self.gui, 'toolbar')):
                return False
            
            # Check if components are not None
            if not (self.gui.fig and self.gui.ax and self.gui.canvas and self.gui.toolbar):
                return False
            
            # Check if axis belongs to figure
            if self.gui.ax not in self.gui.fig.axes:
                return False
            
            # Check if canvas is connected to figure
            if self.gui.canvas.figure != self.gui.fig:
                return False
            
            # Check if canvas widget exists and is valid
            try:
                widget = self.gui.canvas.get_tk_widget()
                if not widget or not widget.winfo_exists():
                    return False
            except Exception:
                return False
            
            # Check if toolbar widget exists and is valid
            try:
                if not self.gui.toolbar.winfo_exists():
                    return False
            except Exception:
                return False
            
            return True
            
        except Exception as e:
            _LOGGER.debug(f"Error checking matplotlib component validity: {e}")
            return False
    
    def _apply_plot_theme(self):
        """Apply current theme to matplotlib plot"""
        try:
            if hasattr(self.gui, 'theme_manager') and hasattr(self.gui, 'fig') and self.gui.fig:
                colors = self.gui.theme_manager.get_current_colors()
                
                # Update figure and axes backgrounds
                self.gui.fig.patch.set_facecolor(colors.get('plot_bg', '#ffffff'))
                if hasattr(self.gui, 'ax') and self.gui.ax:
                    self.gui.ax.set_facecolor(colors.get('plot_bg', '#ffffff'))
                    
                    # Update text colors
                    self.gui.ax.tick_params(colors=colors.get('plot_text', '#000000'), 
                                          labelcolor=colors.get('plot_text', '#000000'))
                    
                    # Update axis label colors
                    if hasattr(self.gui.ax, 'xaxis') and self.gui.ax.xaxis.label:
                        self.gui.ax.xaxis.label.set_color(colors.get('plot_text', '#000000'))
                    if hasattr(self.gui.ax, 'yaxis') and self.gui.ax.yaxis.label:
                        self.gui.ax.yaxis.label.set_color(colors.get('plot_text', '#000000'))
                    if hasattr(self.gui.ax, 'title'):
                        self.gui.ax.title.set_color(colors.get('plot_text', '#000000'))
                    
                    # Update tick label colors and size explicitly
                    try:
                        import matplotlib.pyplot as plt
                        plt.setp(self.gui.ax.get_xticklabels(), color=colors.get('plot_text', '#000000'))
                        plt.setp(self.gui.ax.get_yticklabels(), color=colors.get('plot_text', '#000000'))
                        # Ensure larger, readable tick font size
                        try:
                            tick_size = get_font_manager().get_matplotlib_font_dict(FontCategory.PLOT_AXIS).get('size', 12) + 1
                        except Exception:
                            tick_size = 14  # Fallback size
                        self.gui.ax.tick_params(axis='both', labelsize=tick_size)
                    except Exception:
                        # Still set tick size even if color update fails
                        try:
                            self.gui.ax.tick_params(axis='both', labelsize=14)
                        except Exception:
                            pass
                    
                    # Increase axis label font sizes for consistency
                    label_font_size = tick_size + 2
                    try:
                        self.gui.ax.xaxis.label.set_fontsize(label_font_size)
                        self.gui.ax.yaxis.label.set_fontsize(label_font_size)
                    except Exception:
                        pass
                    
                    # Ensure grid is properly styled and visible
                    grid_color = colors.get('plot_grid', '#cccccc')
                    self.gui.ax.grid(True, alpha=0.4, color=grid_color, linestyle='--', linewidth=0.7)
                    self.gui.ax.set_axisbelow(True)  # Ensure grid appears behind data
                    
                    # Update spines (plot borders)
                    for spine_name, spine in self.gui.ax.spines.items():
                        spine.set_color(grid_color)
                        spine.set_linewidth(0.8)
                    
                    # Hide top and right spines for cleaner look
                    self.gui.ax.spines['top'].set_visible(False)
                    self.gui.ax.spines['right'].set_visible(False)
                    
                    # Update legend if present
                    legend = self.gui.ax.get_legend()
                    if legend:
                        legend.get_frame().set_facecolor(colors.get('plot_bg', '#ffffff'))
                        legend.get_frame().set_edgecolor(grid_color)
                        legend.get_frame().set_alpha(0.9)
                        legend.get_frame().set_linewidth(0.5)
                        for text in legend.get_texts():
                            text.set_color(colors.get('plot_text', '#000000'))
                
                # Force canvas redraw to apply changes
                if hasattr(self.gui, 'canvas'):
                    self.gui.canvas.draw_idle()
                    
        except Exception as e:
            _LOGGER.error(f"Error applying plot theme: {e}")
    
    def enable_plot_navigation(self):
        """Enable plot navigation - delegate to app controller"""
        if hasattr(self.gui, 'app_controller'):
            self.gui.app_controller.enable_plot_navigation()
    
    def reset_view_state(self):
        """Reset plot controller view state to initial values"""
        try:
            _LOGGER.debug("🔄 Resetting plot controller view state...")
            
            # Reset view and template navigation
            self.current_view = 'flux'
            self.current_template = 0
            
            # NEW: Reset plot state management
            self.current_plot_type = None
            self.last_spectrum_view = 'flux'
            self.plot_stack = []
            
            # Clear any cached plot data
            if hasattr(self, 'cached_plots'):
                self.cached_plots = {}
            
            # Reset plot state but don't clear the actual plot
            # (that's handled by the spectrum reset manager)
            
            _LOGGER.debug("✅ Plot controller view state reset")
            
        except Exception as e:
            _LOGGER.error(f"Error resetting plot controller view state: {e}")
    
    def plot_flux_view(self):
        """Plot flux view"""
        try:
            # NEW: Set plot type for proper state management
            self._set_plot_type('spectrum_flux')
            
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                self.init_matplotlib_plot()
                
            # Check if we have a valid axis
            if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                _LOGGER.error("No valid matplotlib axis available")
                return
                
            self.gui.ax.clear()
            
            # CRITICAL: Ensure view style is set to Flux
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                if self.gui.view_style.get() != "Flux":
                    # Set flag to prevent recursion during programmatic change
                    self.gui._programmatic_view_change = True
                    try:
                        self.gui.view_style.set("Flux")
                        if hasattr(self.gui, '_update_segmented_control_buttons'):
                            self.gui._update_segmented_control_buttons()
                        _LOGGER.debug("🔄 View style corrected to Flux")
                    finally:
                        self.gui._programmatic_view_change = False
            
            if hasattr(self.gui, 'snid_results') and self.gui.snid_results:
                # Plot flux SNID results
                self._plot_snid_results(flattened=False)
            elif hasattr(self.gui, 'processed_spectrum') and self.gui.processed_spectrum:
                # Plot preprocessed spectrum flux version
                log_wave = self.gui.processed_spectrum.get('log_wave', [])
                
                # Use display_flux if available (reconstructed flux), otherwise fall back to log_flux
                if 'display_flux' in self.gui.processed_spectrum:
                    flux_data = self.gui.processed_spectrum['display_flux']
                    spectrum_label = 'Preprocessed Spectrum (Flux View)'
                    _LOGGER.debug(f"📊 Flux View: Using display_flux (scaled flux on log grid)")
                else:
                    flux_data = self.gui.processed_spectrum.get('log_flux', [])
                    spectrum_label = 'Preprocessed Spectrum'
                    _LOGGER.debug(f"📊 Flux View: Fallback to log_flux")
                
                # Validate data before plotting
                if len(log_wave) > 0 and len(flux_data) > 0 and log_wave is not None and flux_data is not None:
                    # Filter out zero-padded regions
                    from snid_sage.interfaces.gui.utils.gui_helpers import GUIHelpers
                    filtered_wave, filtered_flux = GUIHelpers.filter_nonzero_spectrum(
                        log_wave, flux_data, self.gui.processed_spectrum
                    )
                    
                    # Validate filtered data
                    if filtered_wave is not None and filtered_flux is not None and len(filtered_wave) > 0 and len(filtered_flux) > 0:
                        # Get theme colors if available
                        if hasattr(self.gui, 'theme_manager'):
                            spectrum_color = '#0078d4'  # Consistent blue color matching original spectrum
                        else:
                            spectrum_color = '#0078d4'  # Default blue
                        
                        self.gui.ax.plot(filtered_wave, filtered_flux, color=spectrum_color, 
                                       linewidth=2, alpha=0.8, label=spectrum_label)
                        self.gui.ax.set_xlabel('Wavelength (Å)')
                        self.gui.ax.set_ylabel('Flux')
                        # Apply no-title styling per user requirement
                        if UNIFIED_SYSTEMS_AVAILABLE:
                            apply_no_title_styling(self.gui.fig, self.gui.ax, "Wavelength (Å)", "Flux", 
                                                 getattr(self.gui, 'theme_manager', None))
                        self.gui.ax.grid(True, alpha=0.3)
                        # Place legend in upper right for consistency
                        self._safe_add_legend(self.gui.ax, loc='upper right')
                        
                        # Refresh canvas
                        if hasattr(self.gui, 'canvas'):
                            self.gui.canvas.draw()
                        
                        # Track that we're showing a spectrum plot
                        self.gui.current_plot_type = 'spectrum'
                        
                        _LOGGER.info("✅ Flux view plotted successfully")
                    else:
                        _LOGGER.warning("⚠️ Filtered flux data is invalid or empty")
                        self._show_no_data_message("No valid flux data available after filtering")
                else:
                    _LOGGER.warning("⚠️ No flux data available")
                    self._show_no_data_message("No flux data available")
            elif hasattr(self.gui, 'original_wave') and hasattr(self.gui, 'original_flux'):
                # Validate original data before plotting
                if (self.gui.original_wave is not None and self.gui.original_flux is not None and 
                    len(self.gui.original_wave) > 0 and len(self.gui.original_flux) > 0):
                    # Plot original spectrum
                    self.gui.ax.plot(self.gui.original_wave, self.gui.original_flux,
                                     color='#0078d4', linewidth=2, alpha=0.8)
                    self.gui.ax.set_xlabel('Wavelength (Å)')
                    self.gui.ax.set_ylabel('Flux')
                    # Apply no-title styling per user requirement
                    if UNIFIED_SYSTEMS_AVAILABLE:
                        apply_no_title_styling(self.gui.fig, self.gui.ax, "Wavelength (Å)", "Flux", 
                                             getattr(self.gui, 'theme_manager', None))
                    self.gui.ax.grid(True, alpha=0.3)
                    # Place legend in upper right for consistency
                    self._safe_add_legend(self.gui.ax, loc='upper right')
                else:
                    _LOGGER.debug("No original spectrum data available on startup (expected)")
                    self._show_no_data_message("Original spectrum data is invalid")
            else:
                # No data available
                self._show_no_data_message("No spectrum data available")
            
            self._apply_plot_theme()
            if hasattr(self.gui, 'canvas'):
                self.gui.canvas.draw()
                
        except Exception as e:
            _LOGGER.error(f"Error plotting flux view: {e}")
            self._show_error_message(f"Error plotting flux view: {str(e)}")
    
    def _show_no_data_message(self, message):
        """Show a no data message on the plot"""
        try:
            if hasattr(self.gui, 'ax') and self.gui.ax is not None:
                self.gui.ax.text(0.5, 0.5, message, 
                               ha='center', va='center', transform=self.gui.ax.transAxes,
                               fontsize=14)
        except Exception as e:
            _LOGGER.error(f"Error showing no data message: {e}")
    
    def _show_error_message(self, message):
        """Show an error message on the plot"""
        try:
            if hasattr(self.gui, 'ax') and self.gui.ax is not None:
                self.gui.ax.clear()
                self.gui.ax.text(0.5, 0.5, f'Plot Error:\n{message}', 
                               ha='center', va='center', transform=self.gui.ax.transAxes,
                               fontsize=12, color='red')
        except Exception as e:
            _LOGGER.error(f"Error showing error message: {e}")

    def _safe_add_legend(self, ax, loc='upper right'):
        """Safely add legend only if there are labeled artists (prevents matplotlib warnings)."""
        try:
            if ax is None:
                return
            if hasattr(ax, 'get_legend_handles_labels'):
                handles, labels = ax.get_legend_handles_labels()
                valid_handles = []
                valid_labels = []
                for handle, label in zip(handles, labels):
                    if label and not label.startswith('_'):
                        valid_handles.append(handle)
                        valid_labels.append(label)
                if valid_handles and valid_labels:
                    ax.legend(valid_handles, valid_labels, loc=loc)
                # If no valid labels, don't add legend (prevents warning)
        except Exception as e:
            _LOGGER.debug(f"Error adding legend: {e}")
            # Silently fail to avoid disrupting the main functionality
    
    def plot_flat_view(self):
        """Plot flattened view"""
        try:
            # NEW: Set plot type for proper state management
            self._set_plot_type('spectrum_flat')
            
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                self.init_matplotlib_plot()
                
            # Check if we have a valid axis
            if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                _LOGGER.error("No valid matplotlib axis available")
                return
                
            self.gui.ax.clear()
            
            # CRITICAL: Ensure view style is set to Flat
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                if self.gui.view_style.get() != "Flat":
                    # Set flag to prevent recursion during programmatic change
                    self.gui._programmatic_view_change = True
                    try:
                        self.gui.view_style.set("Flat")
                        if hasattr(self.gui, '_update_segmented_control_buttons'):
                            self.gui._update_segmented_control_buttons()
                        _LOGGER.debug("🔄 View style corrected to Flat")
                    finally:
                        self.gui._programmatic_view_change = False
            
            if hasattr(self.gui, 'snid_results') and self.gui.snid_results:
                # Plot flattened SNID results
                self._plot_snid_results(flattened=True)
            elif hasattr(self.gui, 'processed_spectrum') and self.gui.processed_spectrum:
                # Plot processed spectrum flat version (continuum-removed)
                log_wave = self.gui.processed_spectrum.get('log_wave', [])
                
                # Use display_flat if available (proper flattened), otherwise fall back to flat_flux
                if 'display_flat' in self.gui.processed_spectrum:
                    flat_data = self.gui.processed_spectrum['display_flat']
                    spectrum_label = 'Flattened Spectrum (Continuum Removed)'
                    _LOGGER.debug(f"📊 Flat View: Using display_flat (continuum-removed)")
                else:
                    flat_data = self.gui.processed_spectrum.get('flat_flux', [])
                    spectrum_label = 'Flattened Spectrum'
                    _LOGGER.debug(f"📊 Flat View: Fallback to flat_flux")
                
                # Validate data before plotting
                if len(log_wave) > 0 and len(flat_data) > 0 and log_wave is not None and flat_data is not None:
                    # Filter out zero-padded regions
                    from snid_sage.interfaces.gui.utils.gui_helpers import GUIHelpers
                    filtered_wave, filtered_flux = GUIHelpers.filter_nonzero_spectrum(
                        log_wave, flat_data, self.gui.processed_spectrum
                    )
                    
                    # Validate filtered data
                    if filtered_wave is not None and filtered_flux is not None and len(filtered_wave) > 0 and len(filtered_flux) > 0:
                        # Get theme colors if available
                        if hasattr(self.gui, 'theme_manager'):
                            spectrum_color = '#0078d4'  # Consistent blue color matching original spectrum
                        else:
                            spectrum_color = '#0078d4'  # Default blue
                        
                        self.gui.ax.plot(filtered_wave, filtered_flux, color=spectrum_color, 
                                       linewidth=2, alpha=0.8, label=spectrum_label)
                        self.gui.ax.set_xlabel('Wavelength (Å)')
                        self.gui.ax.set_ylabel('Flattened Flux')
                        # Apply no-title styling per user requirement
                        if UNIFIED_SYSTEMS_AVAILABLE:
                            apply_no_title_styling(self.gui.fig, self.gui.ax, "Wavelength (Å)", "Flattened Flux", 
                                                 getattr(self.gui, 'theme_manager', None))
                        self.gui.ax.grid(True, alpha=0.3)
                        # Place legend in upper right for consistency
                        self._safe_add_legend(self.gui.ax, loc='upper right')
                        
                        _LOGGER.debug("Flattened view plotted successfully")
                    else:
                        _LOGGER.warning("⚠️ Filtered flat data is invalid or empty")
                        self._show_no_data_message("No valid flattened data available after filtering")
                else:
                    _LOGGER.warning("⚠️ No flattened data available")
                    self._show_no_data_message("No flattened data available\nRun preprocessing first")
            else:
                # No data available
                self._show_no_data_message("No preprocessed data available\nRun preprocessing first")
            
            self._apply_plot_theme()
            if hasattr(self.gui, 'canvas'):
                self.gui.canvas.draw()
                
        except Exception as e:
            _LOGGER.error(f"Error plotting flat view: {e}")
            self._show_error_message(f"Error plotting flat view: {str(e)}")
    
    def plot_original_spectrum(self):
        """Plot original spectrum"""
        try:
            # NEW: Set plot type for proper state management
            self._set_plot_type('spectrum_flux')
            
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                self.init_matplotlib_plot()
                
            # Check if we have a valid axis
            if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                _LOGGER.error("No valid matplotlib axis available")
                return
                
            self.gui.ax.clear()
            
            # CRITICAL: Ensure view style is set to Flux for original spectrum
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                if self.gui.view_style.get() != "Flux":
                    # Set flag to prevent recursion during programmatic change
                    self.gui._programmatic_view_change = True
                    try:
                        self.gui.view_style.set("Flux")
                        if hasattr(self.gui, '_update_segmented_control_buttons'):
                            self.gui._update_segmented_control_buttons()
                        _LOGGER.debug("🔄 View style corrected to Flux for original spectrum")
                    finally:
                        self.gui._programmatic_view_change = False
            
            if (hasattr(self.gui, 'original_wave') and hasattr(self.gui, 'original_flux') and
                self.gui.original_wave is not None and self.gui.original_flux is not None and
                len(self.gui.original_wave) > 0 and len(self.gui.original_flux) > 0):
                
                # FIXED: Use the same nice blue color as the preprocessing plots
                if hasattr(self.gui, 'theme_manager'):
                    spectrum_color = '#0078d4'  # Nice blue matching preprocessing dialog
                else:
                    spectrum_color = '#0078d4'  # Default to same blue
                
                self.gui.ax.plot(self.gui.original_wave, self.gui.original_flux, 
                               color=spectrum_color, linewidth=2, alpha=0.8)
                self.gui.ax.set_xlabel('Wavelength (Å)')
                self.gui.ax.set_ylabel('Flux')
                # Apply no-title styling per user requirement
                if UNIFIED_SYSTEMS_AVAILABLE:
                    apply_no_title_styling(self.gui.fig, self.gui.ax, "Wavelength (Å)", "Flux", 
                                         getattr(self.gui, 'theme_manager', None))
                self.gui.ax.grid(True, alpha=0.3)
                # Place legend in upper right for consistency
                self._safe_add_legend(self.gui.ax, loc='upper right')
                
                self._apply_plot_theme()
                if hasattr(self.gui, 'canvas'):
                    self.gui.canvas.draw()
                    
                # Track that we're showing a spectrum plot
                self.gui.current_plot_type = 'spectrum'
                
                _LOGGER.debug("Original spectrum plotted successfully")
            else:
                _LOGGER.warning("⚠️ No original spectrum data available")
                self._show_no_data_message("No spectrum loaded\nLoad a spectrum file first")
                self._apply_plot_theme()
                if hasattr(self.gui, 'canvas'):
                    self.gui.canvas.draw()
            
        except Exception as e:
            _LOGGER.error(f"Error plotting original spectrum: {e}")
            self._show_error_message(f"Error plotting original spectrum: {str(e)}")
    
    def _plot_snid_results(self, flattened=False):
        """Plot SNID results with template overlays"""
        try:
            if not hasattr(self.gui, 'snid_results') or not self.gui.snid_results:
                _LOGGER.warning("⚠️ No SNID results available")
                return
            
            # Initialize or get spectrum plotter component
            if not hasattr(self.gui, 'spectrum_plotter') or not self.gui.spectrum_plotter:
                try:
                    from snid_sage.interfaces.gui.components.plots.spectrum_plotter import SpectrumPlotter
                    self.gui.spectrum_plotter = SpectrumPlotter(self.gui)
                    _LOGGER.debug("✅ Spectrum plotter initialized for template overlays")
                except Exception as e:
                    _LOGGER.error(f"Could not initialize spectrum plotter: {e}")
                    return
            
            # Delegate to spectrum plotter for proper template overlay
            if flattened:
                _LOGGER.debug("📊 Plotting flattened view with template overlay")
                self.gui.spectrum_plotter.plot_flattened_spectra()
            else:
                _LOGGER.debug("📊 Plotting flux view with template overlay")
                self.gui.spectrum_plotter.plot_original_spectra()
                
        except Exception as e:
            _LOGGER.error(f"Error plotting SNID results: {e}")
            _LOGGER.debug("SNID results plotting error details:", exc_info=True)
            
            # Fallback to error display
            if hasattr(self.gui, '_plot_error'):
                self.gui._plot_error(f"Error plotting SNID results: {str(e)}")
            
            self._apply_plot_theme()
            if hasattr(self.gui, 'canvas'):
                self.gui.canvas.draw()
    
    def plot_preprocessed_spectrum(self, wave, flux):
        """Plot preprocessed spectrum"""
        try:
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                self.init_matplotlib_plot()
                
            # Check if we have a valid axis
            if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                _LOGGER.error("No valid matplotlib axis available")
                return
                
            # Validate input data
            if wave is None or flux is None:
                _LOGGER.error("Invalid data: wave or flux is None")
                self._show_error_message("Invalid preprocessed spectrum data: None values")
                return
                
            if len(wave) == 0 or len(flux) == 0:
                _LOGGER.error("Invalid data: wave or flux is empty")
                self._show_error_message("Invalid preprocessed spectrum data: empty arrays")
                return
                
            if len(wave) != len(flux):
                _LOGGER.error(f"Data mismatch: wave length ({len(wave)}) != flux length ({len(flux)})")
                self._show_error_message("Invalid preprocessed spectrum data: mismatched array lengths")
                return
                
            # Filter out zero-padded regions before plotting
            wave, flux = self.gui._filter_nonzero_spectrum(wave, flux)
            
            self.gui.ax.clear()
            
            # Get theme colors if available
            if hasattr(self.gui, 'theme_manager'):
                spectrum_color = '#0078d4'  # Consistent blue color matching original spectrum
            else:
                spectrum_color = '#0078d4'  # Default blue
            
            # Plot the preprocessed spectrum
            self.gui.ax.plot(wave, flux, color=spectrum_color, linewidth=1.5, alpha=0.8)
            self.gui.ax.set_xlabel('Wavelength (Å)')
            self.gui.ax.set_ylabel('Flux')
            # Apply no-title styling per user requirement
            if UNIFIED_SYSTEMS_AVAILABLE:
                apply_no_title_styling(self.gui.fig, self.gui.ax, "Wavelength (Å)", "Flux", 
                                     getattr(self.gui, 'theme_manager', None))
            self.gui.ax.grid(True, alpha=0.3)
            
            # Apply theme styling
            self._apply_plot_theme()
            
            # Track that we're showing a spectrum plot
            self.gui.current_plot_type = 'spectrum'
            
            # Refresh canvas
            if hasattr(self.gui, 'canvas'):
                self.gui.canvas.draw()
                
            _LOGGER.debug("Preprocessed spectrum plotted successfully")
            
        except Exception as e:
            _LOGGER.error(f"Error plotting preprocessed spectrum: {e}")
            _LOGGER.debug("Preprocessed spectrum plotting error details:", exc_info=True)
            self._show_error_message(f"Error plotting preprocessed spectrum: {str(e)}")
    
    def prev_template(self):
        """Navigate to previous template"""
        try:
            if hasattr(self.gui, 'snid_results') and self.gui.snid_results and hasattr(self.gui, 'current_template'):
                if hasattr(self.gui.snid_results, 'best_matches') and self.gui.snid_results.best_matches:
                    if self.gui.current_template > 0:
                        self.gui.current_template -= 1
                        self.show_template()
                        _LOGGER.debug(f"📖 Showing template {self.gui.current_template + 1}")
                    
        except Exception as e:
            _LOGGER.error(f"Error navigating to previous template: {e}")
            _LOGGER.debug("Template navigation error details:", exc_info=True)
    
    def next_template(self):
        """Navigate to next template"""
        try:
            if hasattr(self.gui, 'snid_results') and self.gui.snid_results and hasattr(self.gui, 'current_template'):
                if hasattr(self.gui.snid_results, 'best_matches') and self.gui.snid_results.best_matches:
                    max_templates = len(self.gui.snid_results.best_matches)
                    if self.gui.current_template < max_templates - 1:
                        self.gui.current_template += 1
                        self.show_template()
                        _LOGGER.debug(f"📖 Showing template {self.gui.current_template + 1}")
                    
        except Exception as e:
            _LOGGER.error(f"Error navigating to next template: {e}")
            _LOGGER.debug("Template navigation error details:", exc_info=True)
    
    def show_template(self):
        """Show current template with proper overlay"""
        try:
            if not hasattr(self.gui, 'snid_results') or not self.gui.snid_results:
                _LOGGER.warning("⚠️ No SNID results to show")
                return
                
            if not hasattr(self.gui.snid_results, 'best_matches') or not self.gui.snid_results.best_matches:
                _LOGGER.warning("⚠️ No template matches to show")
                return
            
            # Ensure current template index is valid
            max_templates = len(self.gui.snid_results.best_matches)
            if not hasattr(self.gui, 'current_template'):
                self.gui.current_template = 0
            else:
                self.gui.current_template = max(0, min(self.gui.current_template, max_templates - 1))
            
            # Get current template info for logging
            current_match = self.gui.snid_results.best_matches[self.gui.current_template]
            template_name = current_match.get('name', 'Unknown')
            template = current_match.get('template', {})
            template_subtype = template.get('subtype', current_match.get('type', 'Unknown'))
            redshift = current_match.get('redshift', 0.0)
            rlap = current_match.get('rlap', 0.0)
            
            _LOGGER.debug(f"📊 Showing template {self.gui.current_template + 1}/{max_templates}: {template_name} "
                  f"(Subtype: {template_subtype}, z={redshift:.4f}, RLAP={rlap:.2f})")
            
            # Determine target view with proper precedence
            target_view = "Flux"  # Default
            
            # Check for preserved view mode first (highest precedence)
            if hasattr(self, 'preserve_view_mode') and self.preserve_view_mode:
                target_view = self.preserve_view_mode
                _LOGGER.debug(f"🔒 Using preserved view mode: {target_view}")
            # Then check current GUI view style
            elif hasattr(self.gui, 'view_style') and self.gui.view_style:
                target_view = self.gui.view_style.get()
                _LOGGER.debug(f"📊 Using current view style: {target_view}")
            
            # Ensure view_style variable matches the target view
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                current_view_style = self.gui.view_style.get()
                if current_view_style != target_view:
                    _LOGGER.info(f"🔄 Correcting view_style from {current_view_style} to {target_view}")
                    # Set flag to prevent recursion during programmatic change
                    self.gui._programmatic_view_change = True
                    try:
                        self.gui.view_style.set(target_view)
                        
                        # Update segmented control buttons
                        if hasattr(self.gui, '_update_segmented_control_buttons'):
                            self.gui._update_segmented_control_buttons()
                    finally:
                        self.gui._programmatic_view_change = False
            
            # Show the template in the appropriate view
            if target_view == "Flat":
                # Refresh flat view with template overlay
                _LOGGER.debug("🔄 Refreshing flat view for new template")
                self._plot_snid_results(flattened=True)
            else:
                # Default to flux view with template overlay
                _LOGGER.debug("🔄 Refreshing flux view for new template")
                self._plot_snid_results(flattened=False)
            
            # Apply theme after template change to ensure grid/background consistency
            self._apply_plot_theme()
            
            # Update GUI status if possible
            if hasattr(self.gui, 'update_header_status'):
                status_msg = f"📊 Template {self.gui.current_template + 1}/{max_templates}: {template_name} ({template_subtype})"
                self.gui.update_header_status(status_msg)
                    
        except Exception as e:
            _LOGGER.error(f"Error showing template: {e}")
            _LOGGER.debug("Template showing error details:", exc_info=True)
    
    def refresh_current_view(self):
        """Refresh the current view with proper template overlays"""
        try:
            # Determine the current view style
            current_style = "Flux"  # Default
            if hasattr(self.gui, 'view_style'):
                current_style = self.gui.view_style.get()
            
            _LOGGER.debug(f"🔄 Refreshing view: {current_style}")
            
            if hasattr(self.gui, 'snid_results') and self.gui.snid_results:
                # We have SNID results - show template overlays
                if current_style == "Flux":
                    _LOGGER.debug("📊 Refreshing flux view with template overlay")
                    self._plot_snid_results(flattened=False)
                elif current_style == "Flat":
                    _LOGGER.debug("📊 Refreshing flat view with template overlay")
                    self._plot_snid_results(flattened=True)
                else:
                    # Default to flux view
                    _LOGGER.debug("📊 Refreshing flux view (default) with template overlay")
                    self._plot_snid_results(flattened=False)
                    
            elif hasattr(self.gui, 'processed_spectrum') and self.gui.processed_spectrum:
                # We have preprocessed data but no SNID results yet
                if current_style == "Flux":
                    _LOGGER.debug("📊 Refreshing flux view (preprocessed, no templates)")
                    self.plot_flux_view()
                elif current_style == "Flat":
                    _LOGGER.debug("📊 Refreshing flat view (preprocessed, no templates)")
                    self.plot_flat_view()
                else:
                    self.plot_flux_view()  # Default
                    
            elif hasattr(self.gui, 'original_wave') and hasattr(self.gui, 'original_flux'):
                # We only have original spectrum data
                _LOGGER.debug("📊 Refreshing original spectrum view")
                self.plot_original_spectrum()
                
            else:
                # No data available
                _LOGGER.warning("⚠️ No data available to refresh")
                if hasattr(self.gui, 'ax') and self.gui.ax:
                    self.gui.ax.clear()
                    theme = self.gui.theme_manager.get_current_theme() if hasattr(self.gui, 'theme_manager') else {}
                    text_color = theme.get('text_color', 'black')
                    self.gui.ax.text(0.5, 0.5, 'No preprocessed data available', 
                                   ha='center', va='center', transform=self.gui.ax.transAxes,
                                   fontsize=14, color=text_color)
                    # No title per user requirement
                    self._apply_plot_theme()
                    if hasattr(self.gui, 'canvas'):
                        self.gui.canvas.draw()
                
        except Exception as e:
            _LOGGER.error(f"Error refreshing current view: {e}")
            _LOGGER.debug("Current view refreshing error details:", exc_info=True)
    
    def _on_view_style_change(self, *args):
        """Handle changes to the view style segmented control"""
        try:
            style = self.gui.view_style.get()
            _LOGGER.debug(f"🔄 View style change triggered: {style}")
            
            # Update internal state
            if style == "Flux":
                self.gui.current_view = 'flux'
                self.plot_flux_view()
            elif style == "Flat":
                self.gui.current_view = 'flat'
                self.plot_flat_view()
            
            # Update segmented control buttons to ensure consistency
            if hasattr(self.gui, '_update_segmented_control_buttons'):
                self.gui._update_segmented_control_buttons()
                _LOGGER.debug(f"✅ Segmented control buttons updated for: {style}")
                    
        except Exception as e:
            _LOGGER.error(f"Error handling view style change: {e}")

    def _ensure_matplotlib_backend_configured(self):
        """Ensure matplotlib is properly configured to stay embedded"""
        try:
            import matplotlib
            import matplotlib.pyplot as plt
            
            # Force TkAgg backend and turn off interactive mode to prevent external windows
            matplotlib.use('TkAgg', force=True)
            plt.ioff()  # Turn off interactive mode
            
            # Configure matplotlib to not create separate windows
            import matplotlib as mpl
            mpl.rcParams['figure.raise_window'] = False
            mpl.rcParams['tk.window_focus'] = False
            
            _LOGGER.debug("✅ Matplotlib backend configured for embedded display")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Warning configuring matplotlib backend: {e}") 

    def _set_plot_type(self, plot_type):
        """Set the current plot type and handle view state transitions"""
        try:
            # Store previous plot type in stack for potential restoration
            previous_plot_type = self.current_plot_type
            if self.current_plot_type and self.current_plot_type != plot_type:
                self.plot_stack.append(self.current_plot_type)
                
            self.current_plot_type = plot_type
            _LOGGER.debug(f"🔄 Plot type changed to: {plot_type}")
            
            # NEW: Check if we need to reinitialize matplotlib due to complex plot transitions
            needs_reinit = self._needs_matplotlib_reinit(previous_plot_type, plot_type)
            if needs_reinit:
                _LOGGER.debug(f"🔧 Reinitializing matplotlib for transition: {previous_plot_type} → {plot_type}")
                self._force_matplotlib_reinit()
            
            # Handle view style button state based on plot type
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                if plot_type in ['spectrum_flux', 'spectrum_flat']:
                    # Spectrum plots - ensure view style is set correctly
                    expected_view = 'Flux' if plot_type == 'spectrum_flux' else 'Flat'
                    if self.gui.view_style.get() != expected_view:
                        # Set flag to prevent recursion during programmatic change
                        self.gui._programmatic_view_change = True
                        try:
                            self.gui.view_style.set(expected_view)
                            self._update_segmented_control()
                        finally:
                            self.gui._programmatic_view_change = False
                elif plot_type in ['gmm_clustering', 'redshift_age', 'subtype_proportions']:
                    # Analysis plots - deactivate view style buttons since they're not applicable
                    self._deactivate_view_style()
                    
        except Exception as e:
            _LOGGER.error(f"Error setting plot type: {e}")
    
    def _needs_matplotlib_reinit(self, previous_plot_type, new_plot_type):
        """Check if matplotlib needs reinitialization for this plot transition"""
        # Complex plots that create 3D axes or multiple subplots
        complex_plots = ['gmm_clustering', 'subtype_proportions', 'redshift_age']
        spectrum_plots = ['spectrum_flux', 'spectrum_flat']
        
        # Need reinit when going FROM complex plots TO spectrum plots
        if previous_plot_type in complex_plots and new_plot_type in spectrum_plots:
            return True
            
        # Also check if current axis is wrong type for the target plot
        if new_plot_type in spectrum_plots and hasattr(self.gui, 'ax') and self.gui.ax:
            # Check if we have a 3D axis when we need 2D
            axis_type = str(type(self.gui.ax))
            if 'Axes3D' in axis_type or '3d' in axis_type.lower():
                _LOGGER.debug(f"🔧 Detected 3D axis for 2D plot: {axis_type}")
                return True
                
            # Check if we have multiple subplots when we need a single plot
            if hasattr(self.gui, 'fig') and self.gui.fig:
                num_axes = len(self.gui.fig.axes)
                if num_axes > 1:
                    _LOGGER.debug(f"🔧 Detected multiple axes ({num_axes}) for single plot")
                    return True
        
        return False
    
    def _force_matplotlib_reinit(self):
        """Force complete matplotlib reinitialization"""
        try:
            # Clear and close the current figure
            if hasattr(self.gui, 'fig') and self.gui.fig:
                self.gui.fig.clear()
                
            # Import matplotlib to close any orphaned figures
            import matplotlib.pyplot as plt
            plt.close('all')
            
            # Clear references to force fresh initialization
            if hasattr(self.gui, 'ax'):
                self.gui.ax = None
            if hasattr(self.gui, 'fig'):
                self.gui.fig = None
                
            # CRITICAL: Destroy toolbar first to prevent accumulation
            if hasattr(self.gui, 'toolbar') and self.gui.toolbar:
                try:
                    if self.gui.toolbar.winfo_exists():
                        self.gui.toolbar.destroy()
                    _LOGGER.debug("🧹 Old toolbar destroyed during reinit")
                except Exception as e:
                    _LOGGER.debug(f"Warning cleaning up old toolbar during reinit: {e}")
                finally:
                    self.gui.toolbar = None
                    
            if hasattr(self.gui, 'canvas'):
                # Destroy the old canvas widget
                try:
                    old_widget = self.gui.canvas.get_tk_widget()
                    if old_widget and old_widget.winfo_exists():
                        old_widget.destroy()
                    _LOGGER.debug("🧹 Old canvas destroyed during reinit")
                except Exception as e:
                    _LOGGER.debug(f"Warning cleaning up old canvas: {e}")
                self.gui.canvas = None
            
            # Force reinitialization
            self.init_matplotlib_plot()
            _LOGGER.debug("✅ Matplotlib reinitialized successfully")
            
        except Exception as e:
            _LOGGER.error(f"Error forcing matplotlib reinitialization: {e}")
    
    def _deactivate_view_style(self):
        """Deactivate view style buttons for non-spectrum plots"""
        try:
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                # Store current spectrum view before deactivating
                current_view = self.gui.view_style.get()
                if current_view in ['Flux', 'Flat']:
                    self.last_spectrum_view = current_view.lower()
                
                # Clear view style selection
                # Set flag to prevent recursion during programmatic change
                self.gui._programmatic_view_change = True
                try:
                    self.gui.view_style.set("")
                    self._update_segmented_control()
                    _LOGGER.debug("🔘 View style deactivated for analysis plot")
                finally:
                    self.gui._programmatic_view_change = False
                
        except Exception as e:
            _LOGGER.debug(f"View style deactivation failed: {e}")
    
    def _update_segmented_control(self):
        """Update segmented control button appearance"""
        try:
            if hasattr(self.gui, '_update_segmented_control_buttons'):
                self.gui._update_segmented_control_buttons()
        except Exception as e:
            _LOGGER.debug(f"Segmented control update failed: {e}")
    
    def _ensure_spectrum_view_on_return(self):
        """Ensure we return to the correct spectrum view when switching back from analysis plots"""
        try:
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                # If view style is empty, restore last spectrum view
                if not self.gui.view_style.get() and self.last_spectrum_view:
                    view_to_set = self.last_spectrum_view.capitalize()
                    # Set flag to prevent recursion during programmatic change
                    self.gui._programmatic_view_change = True
                    try:
                        self.gui.view_style.set(view_to_set)
                        self._update_segmented_control()
                        _LOGGER.debug(f"🔄 Restored spectrum view to: {view_to_set}")
                    finally:
                        self.gui._programmatic_view_change = False
        except Exception as e:
            _LOGGER.debug(f"Error restoring spectrum view: {e}")
    
    # NEW: Analysis plot methods with proper state management
    def plot_gmm_clustering(self):
        """Plot GMM clustering analysis with proper state management"""
        try:
            # Set plot type to deactivate spectrum view buttons
            self._set_plot_type('gmm_clustering')
            
            # Initialize matplotlib if needed
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                self.init_matplotlib_plot()
                
            if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                _LOGGER.error("No valid matplotlib axis available for GMM clustering")
                return
            
            # Delegate to analysis plotter
            if hasattr(self.gui, 'analysis_plotter'):
                self.gui.analysis_plotter.plot_gmm_clustering()
            else:
                _LOGGER.error("Analysis plotter not available")
                self._show_error_message("Analysis plotter not available")
                
        except Exception as e:
            _LOGGER.error(f"Error plotting GMM clustering: {e}")
            self._show_error_message(f"Error plotting GMM clustering: {str(e)}")
    
    def plot_redshift_age(self):
        """Plot redshift vs age analysis with proper state management"""
        try:
            # Set plot type to deactivate spectrum view buttons
            self._set_plot_type('redshift_age')
            
            # Initialize matplotlib if needed
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                self.init_matplotlib_plot()
                
            if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                _LOGGER.error("No valid matplotlib axis available for redshift vs age")
                return
            
            # Delegate to analysis plotter
            if hasattr(self.gui, 'analysis_plotter'):
                self.gui.analysis_plotter.plot_redshift_age()
            else:
                _LOGGER.error("Analysis plotter not available")
                self._show_error_message("Analysis plotter not available")
                
        except Exception as e:
            _LOGGER.error(f"Error plotting redshift vs age: {e}")
            self._show_error_message(f"Error plotting redshift vs age: {str(e)}")
    
    def plot_subtype_proportions(self):
        """Plot subtype proportions with proper state management"""
        try:
            # Set plot type to deactivate spectrum view buttons
            self._set_plot_type('subtype_proportions')
            
            # Initialize matplotlib if needed
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                self.init_matplotlib_plot()
                
            if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                _LOGGER.error("No valid matplotlib axis available for subtype proportions")
                return
            
            # Delegate to analysis plotter
            if hasattr(self.gui, 'analysis_plotter'):
                self.gui.analysis_plotter.plot_subtype_proportions()
            else:
                _LOGGER.error("Analysis plotter not available")
                self._show_error_message("Analysis plotter not available")
                
        except Exception as e:
            _LOGGER.error(f"Error plotting subtype proportions: {e}")
            self._show_error_message(f"Error plotting subtype proportions: {str(e)}")
    
    def show_cluster_summary(self):
        """Show cluster summary dialog (does not change plot area)"""
        try:
            # NOTE: Cluster summary is a DIALOG, not a plot replacement
            # Do NOT set plot type or deactivate view style buttons
            
            # Call the original cluster summary method directly
            if hasattr(self.gui, 'snid_results') and self.gui.snid_results:
                if hasattr(self.gui, 'show_results_summary'):
                    self.gui.show_results_summary(self.gui.snid_results)
                    _LOGGER.debug("📊 Opened cluster summary dialog")
                else:
                    _LOGGER.error("Results summary method not available")
                    self._show_error_message("Results summary method not available")
            else:
                from tkinter import messagebox
                messagebox.showwarning("No Analysis Results", 
                                     "No SNID-SAGE analysis results available.\n"
                                     "Run SNID-SAGE analysis first to generate results.")
                
        except Exception as e:
            _LOGGER.error(f"Error showing cluster summary: {e}")
            self._show_error_message(f"Error showing cluster summary: {str(e)}")
    
    def return_to_spectrum_view(self):
        """Return to spectrum view from analysis plots"""
        try:
            # Restore spectrum view state
            self._ensure_spectrum_view_on_return()
            
            # Determine which spectrum view to show
            if self.last_spectrum_view == 'flat':
                self.plot_flat_view()
            else:
                self.plot_flux_view()
                
        except Exception as e:
            _LOGGER.error(f"Error returning to spectrum view: {e}")
    
    def is_analysis_plot_active(self):
        """Check if an analysis plot is currently active"""
        return self.current_plot_type in ['gmm_clustering', 'redshift_age', 'subtype_proportions']
    
    def is_spectrum_plot_active(self):
        """Check if a spectrum plot is currently active"""
        return self.current_plot_type in ['spectrum_flux', 'spectrum_flat']
