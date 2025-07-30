"""
SNID SAGE GUI View Controller
============================

View controller for the SNID SAGE GUI handling view switching and display modes.

Moved from sage_gui.py to reduce main file complexity.

Part of the SNID SAGE GUI restructuring - Controllers Module
"""

import tkinter as tk
from tkinter import messagebox

# Use centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.view_controller')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.view_controller')


class ViewController:
    """Manages view switching and display modes"""
    
    def __init__(self, gui_instance):
        """Initialize view controller with reference to main GUI"""
        self.gui = gui_instance
        self.current_view = 'flux'  # Default view mode
    
    def _on_view_style_change(self, *args):
        """Handle changes to the view style segmented control"""
        try:
            if not hasattr(self.gui, 'view_style'):
                return
                
            style = self.gui.view_style.get()
            _LOGGER.debug(f"View style change triggered: {style}")
            
            # NEW: Check if plot controller is available for proper state management
            if not hasattr(self.gui, 'plot_controller'):
                _LOGGER.warning("Plot controller not available")
                return
            
            # Handle view style changes - this will properly switch from analysis plots if needed
            if style == "Flux":
                self.current_view = 'flux'
                _LOGGER.debug(f"Flux View: Calling plot_controller.plot_flux_view()")
                # Check if we're switching from an analysis plot
                if self.gui.plot_controller.is_analysis_plot_active():
                    _LOGGER.debug("🔄 Switching from analysis plot to flux view")
                
                self.gui.plot_controller.plot_flux_view()
                    
            elif style == "Flat":
                self.current_view = 'flat'
                _LOGGER.debug(f"Flat View: Calling plot_controller.plot_flat_view()")
                # Check if we're switching from an analysis plot
                if self.gui.plot_controller.is_analysis_plot_active():
                    _LOGGER.debug("🔄 Switching from analysis plot to flat view")
                
                self.gui.plot_controller.plot_flat_view()
            elif style == "":
                # Empty string means view style was deactivated (analysis plot active)
                _LOGGER.debug("🔘 View style deactivated - analysis plot likely active")
                    
        except Exception as e:
            _LOGGER.error(f"Error handling view style change: {e}")
            _LOGGER.debug("View style change error details:", exc_info=True)
    
    def switch_mode(self):
        """Switch between flux and flat view modes"""
        try:
            if hasattr(self.gui, 'view_style'):
                current = self.gui.view_style.get()
                if current == "Flux":
                    self.gui.view_style.set("Flat")
                else:
                    self.gui.view_style.set("Flux")
                
                # Trigger view change
                self._on_view_style_change()
        except Exception as e:
            _LOGGER.error(f"Error switching mode: {e}")
    
    def refresh_current_view(self):
        """Refresh the current view"""
        try:
            if hasattr(self.gui, 'plot_controller'):
                self.gui.plot_controller.refresh_current_view()
            else:
                # Fallback to direct view update
                self._on_view_style_change()
        except Exception as e:
            _LOGGER.error(f"Error refreshing view: {e}")
    
    def plot_flux_view(self):
        """Plot flux view"""
        try:
            if hasattr(self.gui, 'view_style'):
                self.gui.view_style.set("Flux")
            self.current_view = 'flux'
            self._on_view_style_change()
        except Exception as e:
            _LOGGER.error(f"Error plotting flux view: {e}")
    
    def plot_flat_view(self):
        """Plot flattened view"""
        try:
            if hasattr(self.gui, 'view_style'):
                self.gui.view_style.set("Flat")
            self.current_view = 'flat'
            self._on_view_style_change()
        except Exception as e:
            _LOGGER.error(f"Error plotting flat view: {e}")
    
    def get_current_view(self):
        """Get the current view mode"""
        return self.current_view
    
    def set_view_mode(self, mode):
        """Set the view mode programmatically"""
        if mode.lower() in ['flux', 'flat']:
            self.current_view = mode.lower()
            if hasattr(self.gui, 'view_style'):
                self.gui.view_style.set(mode.capitalize())
            self._on_view_style_change()
        else:
            _LOGGER.warning(f"Unknown view mode: {mode}")
    
    def toggle_view_mode(self):
        """Toggle between flux and flat view modes"""
        if self.current_view == 'flux':
            self.set_view_mode('flat')
        else:
            self.set_view_mode('flux')
    
    def create_right_panel(self, parent):
        """Create right panel - currently not used but kept for compatibility"""
        # This method is intentionally minimal since the current layout uses only left and center panels
        pass
    
    def update_header_status(self, message):
        """Update header status message"""
        try:
            if hasattr(self.gui, 'state_manager'):
                self.gui.state_manager.update_header_status(message)
            elif hasattr(self.gui, 'header_status_label'):
                self.gui.header_status_label.configure(text=message)
                self.gui.master.update_idletasks()
                _LOGGER.debug(f"Status: {message}")
        except Exception as e:
            _LOGGER.error(f"Error updating header status: {e}")
    
    def enable_plot_navigation(self):
        """Enable plot navigation - delegate to app controller"""
        if hasattr(self.gui, 'app_controller'):
            self.gui.app_controller.enable_plot_navigation()
        else:
            _LOGGER.warning("App controller not initialized yet")
    
    def reset_to_initial_view(self):
        """Reset view controller to initial state"""
        try:
            _LOGGER.debug("Resetting view controller to initial state...")
            
            # Clear current view
            self.current_view = ''
            
            # Reset view style: leave both options OFF
            if hasattr(self.gui, 'view_style'):
                self.gui.view_style.set("")
            
            # Clear any view-specific state
            _LOGGER.debug("View controller reset to initial state")
            
        except Exception as e:
            _LOGGER.error(f"Error resetting view controller: {e}")
    
    def plot_original_spectrum(self):
        """Plot original spectrum - delegate to plot controller"""
        if hasattr(self.gui, 'plot_controller'):
            self.gui.plot_controller.plot_original_spectrum()
        else:
            _LOGGER.warning("Plot controller not initialized yet")
    
    def _plot_snid_results(self, flattened=False):
        """Plot SNID results - delegate to plot controller"""
        if hasattr(self.gui, 'plot_controller'):
            self.gui.plot_controller._plot_snid_results(flattened)
        else:
            _LOGGER.warning("Plot controller not initialized yet")
    
    def plot_preprocessed_spectrum(self, wave, flux):
        """Plot preprocessed spectrum - delegate to plot controller"""
        try:
            if hasattr(self.gui, 'plot_controller'):
                self.gui.plot_controller.plot_preprocessed_spectrum(wave, flux)
            else:
                # Fallback to basic matplotlib plot if plot controller not available
                _LOGGER.warning("Plot controller not initialized, using basic plot")
                if hasattr(self.gui, 'ax') and self.gui.ax:
                    self.gui.ax.clear()
                    self.gui.ax.plot(wave, flux, 'b-', linewidth=2, label='Preprocessed Spectrum')
                    self.gui.ax.set_xlabel('Wavelength (Å)')
                    self.gui.ax.set_ylabel('Flux')
                    self.gui.ax.set_title('Preprocessed Spectrum')
                    self.gui.ax.grid(True, alpha=0.3)
                    self.gui.ax.legend()
                    if hasattr(self.gui, 'canvas') and self.gui.canvas:
                        self.gui.canvas.draw()
                    _LOGGER.debug("Preprocessed spectrum plotted")
                    
                    # Update status
                    self.update_header_status("🔧 Preprocessed spectrum displayed")
                else:
                    _LOGGER.error("No plotting infrastructure available")
        except Exception as e:
            _LOGGER.error(f"Error plotting preprocessed spectrum: {e}")
            _LOGGER.debug("Preprocessed spectrum plotting error details:", exc_info=True) 
