"""
SNID SAGE - Application Controller
================================

Handles main application state management including button states,
UI updates, and general application flow control.
"""

import tkinter as tk
from tkinter import messagebox
import os
from snid_sage.interfaces.gui.utils.gui_helpers import GUIHelpers

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.app')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.app')


class AppController:
    """Controller for managing main application state and UI updates"""
    
    def __init__(self, gui_instance):
        """Initialize the app controller"""
        self.gui = gui_instance
        self.logger = getattr(gui_instance, 'logger', None)
        
        # Initialize variables immediately
        self.init_variables()
        
        # Defer workflow integration until after interface is created
        # This prevents timing issues with button registration
        self._workflow_initialized = False
        
        if self.logger:
            self.logger.debug("App controller initialized (workflow integration deferred)")
    
    def init_variables(self):
        """Initialize application state variables"""
        # Default SNID parameters - from the original GUI
        self.gui.params = {
            # Basic parameters
            'rlapmin': '5.0', 'zmin': '-0.01', 'zmax': '1.0',
            'lapmin': '0.3', 'verbose': '0',
            
            # Wavelength range and masking
            'wmin': '', 'wmax': '', 'wavelength_masks': '', 'aband_remove': '0',
            
            # Filtering and clipping
            'skyclip': '0', 'emclip_z': '-1.0', 'emwidth': '40',
            'savgol_window': '0', 'savgol_fwhm': '0.0', 'savgol_order': '3', 'apodize_percent': '10.0',
            
            # Template filtering
            'type_filter': '', 'age_min': '', 'age_max': '', 'max_output_templates': '10',
            
            # Advanced parameters
            'peak_window_size': '10', 'save_plots': '0', 'save_summary': '0'
        }
        
        # Application state
        self.gui.file_path = None
        self.gui.snid_results = None
        self.gui.snid_trace = None
        self.gui.available_matches = []
        self.gui.current_template = 0
        self.gui.current_view = 'original'
        self.gui.view_mode = 'flux'
        
        # Preprocessing state
        self.gui.preprocessed_wave = None
        self.gui.preprocessed_flux = None
        self.gui.processed_spectrum = None
        self.gui.skip_preprocessing_steps = []
        self.gui._last_loaded_file = None
        
        # Wavelength masking
        self.gui.mask_regions = []
        self.gui.mask_file = None
        self.gui.span_selector = None
        self.gui.is_masking_active = False
        self.gui.global_masking_active = False  # Global flag for masking state
        
        # Initialize mask regions from parameters
        if self.gui.params.get('wavelength_masks'):
            try:
                GUIHelpers.parse_wavelength_masks(self.gui.params['wavelength_masks'])
            except:
                pass  # Ignore errors during initialization
        
        # Line identification settings
        self.gui.line_search_delta = 50  # Å
        self.gui.line_search_species = ["H I", "He I", "He II", "Ca II"]
        self.gui.line_markers = []
        self.gui.nist_matches = []
        
        # Line comparison
        self.gui.show_obs_lines = False
        self.gui.show_tmpl_lines = False
        self.gui.line_comparison_data = None
        
        # Line detection parameters
        self.gui.line_detection_params = {
            'smoothing_window': 3,
            'noise_factor': 1.5,
            'use_smoothing': True,
            'solid_match_threshold': 100.0,
            'weak_match_threshold': 200.0
        }
        
        # Toggle state variables for actual SNID features

        
        # SNID parameter toggles
        self.gui.verbose_toggle = tk.BooleanVar(value=int(self.gui.params['verbose']))
        self.gui.skyclip_toggle = tk.BooleanVar(value=int(self.gui.params.get('skyclip', '0')))
        self.gui.aband_remove_toggle = tk.BooleanVar(value=int(self.gui.params.get('aband_remove', '0')))
        self.gui.save_plots_toggle = tk.BooleanVar(value=int(self.gui.params.get('save_plots', '0')))
        self.gui.save_summary_toggle = tk.BooleanVar(value=int(self.gui.params.get('save_summary', '0')))
        
        # Line display toggles
        self.gui.show_obs_lines_var = tk.BooleanVar(value=self.gui.show_obs_lines)
        self.gui.show_tmpl_lines_var = tk.BooleanVar(value=self.gui.show_tmpl_lines)
        
        # Filter toggles
        self.gui.savgol_filter_enabled = tk.BooleanVar(value=(
            int(self.gui.params.get('savgol_window', '0')) > 0 or 
            float(self.gui.params.get('savgol_fwhm', '0.0')) > 0.0
        ))
        
        # view_style StringVar is created in state_manager.py
        
        # Template navigation
        self.gui.max_templates = 10
        
        # Toggle state variables
        self.gui.real_time_analysis = tk.BooleanVar(value=True)
        self.gui.auto_save_results = tk.BooleanVar(value=False)
        self.gui.background_processing = tk.BooleanVar(value=True)
        self.gui.noise_reduction = tk.BooleanVar(value=False)
        self.gui.continuum_subtraction = tk.BooleanVar(value=True)
        self.gui.gpu_acceleration = tk.BooleanVar(value=True)
        self.gui.parallel_processing = tk.BooleanVar(value=False)
        self.gui.debug_mode = tk.BooleanVar(value=False)
        self.gui.verbose_logging = tk.BooleanVar(value=False)
        self.gui.show_confidence = tk.BooleanVar(value=True)
        self.gui.show_templates = tk.BooleanVar(value=False)
        self.gui.show_residuals = tk.BooleanVar(value=True)
        self.gui.show_statistics = tk.BooleanVar(value=False)
        
        # Analysis mode
        self.gui.analysis_mode = tk.StringVar(value="Advanced")
        self.gui.export_format = tk.StringVar(value="JSON")
        
        # Feature detection chips
        self.gui.feature_chips = {
            "Hydrogen": tk.BooleanVar(value=False),
            "Helium": tk.BooleanVar(value=False),
            "Silicon": tk.BooleanVar(value=False),
            "Iron": tk.BooleanVar(value=False),
            "Calcium": tk.BooleanVar(value=False)
        }
        
        # Type filter chips
        self.gui.type_chips = {
            "Type Ia": tk.BooleanVar(value=False),
            "Type Ib": tk.BooleanVar(value=False),
            "Type Ic": tk.BooleanVar(value=False),
            "Type II": tk.BooleanVar(value=False)
        }
        
        # Plot toggle chips
        self.gui.plot_chips = {
            "Grid": tk.BooleanVar(value=True),
            "Legend": tk.BooleanVar(value=True),
            "Annotations": tk.BooleanVar(value=False)
        }
        
        _LOGGER.info("✅ Application variables initialized")
    
    def update_button_states(self):
        """Update button states using workflow integrator only"""
        try:
            if hasattr(self.gui, 'workflow_integrator') and self.gui.workflow_integrator:
                _LOGGER.debug("🎯 Using workflow integrator for button state updates")
                self.gui.workflow_integrator._workflow_update_button_states()
            else:
                # This is normal during initialization - workflow integration is initialized later
                _LOGGER.debug("⏳ Workflow integrator not yet available - button states will be updated later")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error updating button states: {e}")
    
    def init_workflow_integration(self):
        """Initialize workflow integration after interface is fully created"""
        if self._workflow_initialized:
            return
            
        try:
            from snid_sage.interfaces.gui.utils.workflow_integration import integrate_workflow_with_gui
            self.gui.workflow_integrator = integrate_workflow_with_gui(self.gui)
            if self.gui.workflow_integrator:
                self._workflow_initialized = True
                if self.logger:
                    self.logger.info("🎯 Workflow system initialized successfully")
            else:
                if self.logger:
                    self.logger.error("❌ Failed to initialize workflow system")
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error initializing workflow system: {e}")
    
    def _initialize_workflow_system(self):
        """Legacy method - now defers to init_workflow_integration"""
        self.init_workflow_integration()
    
    def _enable_button_group(self, button_names):
        """Enable a group of buttons by name"""
        enabled_count = 0
        missing_count = 0
        for btn_name in button_names:
            if hasattr(self.gui, btn_name):
                button = getattr(self.gui, btn_name)
                if button and hasattr(button, 'configure'):
                    button.configure(state='normal')
                    enabled_count += 1
                else:
                    missing_count += 1
                    _LOGGER.warning(f"⚠️ Button {btn_name} exists but cannot be configured")
            else:
                missing_count += 1
                _LOGGER.warning(f"⚠️ Button {btn_name} not found in GUI")
        
        if enabled_count > 0:
            _LOGGER.info(f"✅ Enabled {enabled_count} buttons: {button_names}")
        if missing_count > 0:
            _LOGGER.warning(f"⚠️ {missing_count} buttons missing or non-configurable")
    
    def _disable_button_group(self, button_names):
        """Disable a group of buttons by name"""
        disabled_count = 0
        missing_count = 0
        for btn_name in button_names:
            if hasattr(self.gui, btn_name):
                button = getattr(self.gui, btn_name)
                if button and hasattr(button, 'configure'):
                    button.configure(state='disabled')
                    disabled_count += 1
                else:
                    missing_count += 1
                    _LOGGER.warning(f"⚠️ Button {btn_name} exists but cannot be configured")
            else:
                missing_count += 1
                _LOGGER.warning(f"⚠️ Button {btn_name} not found in GUI")
        
        if disabled_count > 0:
            _LOGGER.info(f"🚫 Disabled {disabled_count} buttons: {button_names}")
        if missing_count > 0:
            _LOGGER.warning(f"⚠️ {missing_count} buttons missing or non-configurable")
    
    def _update_analysis_plot_buttons(self, current_state):
        """Update analysis plot buttons that are stored in lists"""
        try:
            # Analysis plot buttons (right panel) - enabled when analysis is complete
            analysis_enabled = current_state.value in ["analyzed", "ai_ready"]
            
            if hasattr(self.gui, 'analysis_plot_buttons'):
                state = 'normal' if analysis_enabled else 'disabled'
                for btn in self.gui.analysis_plot_buttons:
                    if btn and hasattr(btn, 'configure') and hasattr(btn, 'winfo_exists'):
                        if btn.winfo_exists():
                            btn.configure(state=state)
            
            # Template-specific buttons - enabled when analysis is complete
            if hasattr(self.gui, 'template_buttons'):
                state = 'normal' if analysis_enabled else 'disabled'
                for btn in self.gui.template_buttons:
                    if btn and hasattr(btn, 'configure') and hasattr(btn, 'winfo_exists'):
                        if btn.winfo_exists():
                            btn.configure(state=state)
            
            # Legacy plot buttons support (if they still exist)
            if hasattr(self.gui, 'plot_buttons'):
                state = 'normal' if analysis_enabled else 'disabled'
                for btn in self.gui.plot_buttons:
                    if btn and hasattr(btn, 'configure') and hasattr(btn, 'winfo_exists'):
                        if btn.winfo_exists():
                            btn.configure(state=state)
                            
        except Exception as e:
            _LOGGER.error(f"❌ Error updating analysis plot buttons: {e}")
    
    def _apply_theme_after_state_change(self):
        """Theme is properly managed by the theme system"""
        pass
    
    def trigger_state_update(self):
        """Manually trigger a workflow state update (useful after data changes)"""
        try:
            if hasattr(self.gui, 'workflow_integrator') and self.gui.workflow_integrator:
                self.gui.workflow_integrator._workflow_update_button_states()
                _LOGGER.info("🔄 Manual workflow state update triggered")
            else:
                _LOGGER.debug("⏳ Workflow integrator not yet available - state update will be handled later")
                
        except Exception as e:
            _LOGGER.error(f"❌ Error triggering state update: {e}")
    
    def _restore_button_colors(self):
        """Button colors are managed by the workflow system"""
        pass
    
    def enable_plot_navigation(self):
        """Enable plot navigation controls"""
        try:
            if hasattr(self.gui, 'snid_results') and self.gui.snid_results:
                # Enable template navigation
                if hasattr(self.gui, 'prev_btn'):
                    self.gui.prev_btn.configure(state='normal', relief='raised', bd=2)
                if hasattr(self.gui, 'next_btn'):
                    self.gui.next_btn.configure(state='normal', relief='raised', bd=2)
                
                # Enable view controls
                if hasattr(self.gui, 'view_style'):
                    # View style controls should be enabled
                    pass
                
                _LOGGER.info("✅ Plot navigation enabled")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error enabling plot navigation: {e}")
    
    def _parse_age_range(self):
        """Parse age range from GUI parameters"""
        try:
            age_min_str = self.gui.params.get('age_min', '').strip()
            age_max_str = self.gui.params.get('age_max', '').strip()
            
            # Only apply age filtering if user explicitly provides values
            if not age_min_str and not age_max_str:
                return None  # No age filtering by default (faster analysis)
            
            age_min = float(age_min_str) if age_min_str else -1000
            age_max = float(age_max_str) if age_max_str else 10000
            return age_min, age_max
        except ValueError:
            return None  # Return None on error to skip age filtering
    
    def _parse_type_filter(self):
        """Parse type filter from GUI parameters"""
        try:
            type_filter = self.gui.params.get('type_filter', '').strip()
            if not type_filter:
                return None
            
            # Split by comma and clean up
            types = [t.strip() for t in type_filter.split(',') if t.strip()]
            return types if types else None
            
        except Exception:
            return None
    
    def toggle_additional_tools(self, event=None):
        """Toggle additional tools section visibility"""
        try:
            if hasattr(self.gui, 'additional_tools_frame'):
                # Toggle visibility of additional tools
                if self.gui.additional_tools_frame.winfo_viewable():
                    self.gui.additional_tools_frame.pack_forget()
                    _LOGGER.info("📦 Additional tools hidden")
                else:
                    self.gui.additional_tools_frame.pack(fill='x', pady=(5, 0))
                    _LOGGER.info("📦 Additional tools shown")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error toggling additional tools: {e}")
    
    def _on_click(self, event):
        """Handle plot clicks"""
        try:
            if hasattr(self.gui, 'ax') and event.inaxes == self.gui.ax:
                # Handle masking if active
                if hasattr(self.gui, 'is_masking_active') and self.gui.is_masking_active and event.button == 1:
                    _LOGGER.info(f"Click at wavelength: {event.xdata:.2f}")
                    
        except Exception as e:
            _LOGGER.error(f"❌ Error handling plot click: {e}")
    
    def _on_view_style_change(self, *args):
        """Handle view style changes"""
        try:
            if hasattr(self.gui, 'view_style'):
                style = self.gui.view_style.get()
                _LOGGER.info(f"🔄 View style changed to: {style}")
                
                if style == "Flux":
                    self.gui.current_view = 'flux'
                elif style == "Flat":
                    self.gui.current_view = 'flat'
                
                # Refresh the current view if we have results
                if hasattr(self.gui, 'snid_results') and self.gui.snid_results:
                    self.gui.refresh_current_view()
                    
        except Exception as e:
            _LOGGER.error(f"❌ Error handling view style change: {e}")
    
    def start_games_menu(self):
        """Start the games menu"""
        try:
            if hasattr(self.gui, 'games_integration') and self.gui.games_integration:
                self.gui.games_integration.show_games_menu()
            else:
                # Try direct import as fallback
                try:
                    from snid_sage.snid.games import show_game_menu
                    show_game_menu()
                except ImportError:
                    messagebox.showinfo("Games Unavailable", 
                                      "Games are not available.\n"
                                      "The games module could not be imported.")
                    
        except Exception as e:
            _LOGGER.error(f"❌ Error starting games menu: {e}")
            messagebox.showerror("Games Error", f"Failed to start games: {str(e)}")
    
    def center_window_safely(self):
        """Center window safely on screen"""
        try:
            self.gui.master.update_idletasks()
            width = self.gui.master.winfo_width()
            height = self.gui.master.winfo_height()
            screen_width = self.gui.master.winfo_screenwidth()
            screen_height = self.gui.master.winfo_screenheight()
            
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            
            # Ensure window is not positioned off-screen
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))
            
            self.gui.master.geometry(f"{width}x{height}+{x}+{y}")
            _LOGGER.info(f"✅ Window centered at {x}x{y}")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Could not center window: {e}")
    
    def schedule_keep_alive(self):
        """Schedule periodic keep-alive checks"""
        try:
            # Check if GUI is still alive
            if self.gui.master.winfo_exists():
                # Schedule next check
                self.gui.master.after(5000, self.schedule_keep_alive)  # Every 5 seconds
            
        except Exception as e:
            _LOGGER.error(f"Keep-alive error: {e}")
    
    def update_header_status(self, message):
        """Update the header status label with a message"""
        try:
            if hasattr(self.gui, 'header_status_label') and self.gui.header_status_label:
                self.gui.header_status_label.configure(text=message)
                self.gui.master.update_idletasks()
                _LOGGER.info(f"📢 Status: {message}")
            else:
                _LOGGER.info(f"📢 Status (no label): {message}")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error updating header status: {e}")
    
    def cleanup(self):
        """Clean up resources and prepare for shutdown"""
        try:
            _LOGGER.info("🧹 Cleaning up resources...")
            
            # Store configuration
            if hasattr(self.gui, 'params'):
                try:
                    # Save configuration before exit
                    config = self.gui.params.copy()
                    # Optionally write to file here
                    pass
                except:
                    pass
            
            # Clean up active components
            self._cleanup_active_components()
            
            # Clean up matplotlib
            self._cleanup_matplotlib()
            
            _LOGGER.info("✅ Cleanup completed")
            
        except Exception as e:
            _LOGGER.warning(f"Warning: Error during cleanup: {e}")
    
    def _cleanup_active_components(self):
        """Clean up active components"""
        try:
            # Cancel any running analysis
            if hasattr(self.gui, 'analysis_controller'):
                # The analysis controller handles its own cleanup
                pass
            
            # Close any open dialogs
            for widget in self.gui.master.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    try:
                        widget.destroy()
                    except:
                        pass
            
            # Clear large data structures
            if hasattr(self.gui, 'snid_results'):
                self.gui.snid_results = None
            if hasattr(self.gui, 'processed_spectrum'):
                self.gui.processed_spectrum = None
            
        except Exception as e:
            _LOGGER.error(f"❌ Error cleaning up active components: {e}")
    
    def _cleanup_matplotlib(self):
        """Clean up matplotlib"""
        try:
            # Close any open matplotlib figures
            import matplotlib.pyplot as plt
            plt.close('all')
            
        except Exception as e:
            _LOGGER.error(f"❌ Error cleaning up matplotlib: {e}")
    
    def cleanup_and_exit(self):
        """Clean up resources and exit application"""
        try:
            print("🧹 Cleaning up resources...")
            
            # Cancel any running analysis
            if hasattr(self.gui, 'analysis_controller'):
                # The analysis controller handles its own cleanup
                pass
            
            # Close any open dialogs
            for widget in self.gui.master.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    try:
                        widget.destroy()
                    except:
                        pass
            
            # Clear large data structures
            if hasattr(self.gui, 'snid_results'):
                self.gui.snid_results = None
            if hasattr(self.gui, 'processed_spectrum'):
                self.gui.processed_spectrum = None
            
            print("✅ Cleanup completed")
            
            # Destroy the main window
            self.gui.master.quit()
            self.gui.master.destroy()
            
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")
            # Force exit even if cleanup fails
            try:
                self.gui.master.quit()
            except:
                pass 
