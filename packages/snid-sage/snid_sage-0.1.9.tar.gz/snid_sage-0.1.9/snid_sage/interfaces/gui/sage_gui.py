"""
SNID SAGE - Modern GUI Interface with Toggle Controls
====================================================

Comprehensive graphical user interface for SNID SAGE that combines modern design
with toggle switches and advanced features including LLM integration, line detection, and more.

Developed by Fiorenzo Stoppa for SNID SAGE
Based on the original Fortran SNID by Stéphane Blondin & John L. Tonry
"""

import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from pathlib import Path
import time
import numpy as np

# Import core SNID functionality - now with modular functions
from snid_sage.snid.snid import run_snid as python_snid, preprocess_spectrum, run_snid_analysis

# Import games for entertainment during analysis
try:
    from snid_sage.snid.games import show_game_menu, run_game_in_thread
    GAMES_AVAILABLE = True
except ImportError:
    GAMES_AVAILABLE = False

# Import SNID SAGE components

# Import new unified systems
from snid_sage.interfaces.gui.utils.unified_font_manager import get_font_manager, FontCategory, apply_font_to_widget
from snid_sage.interfaces.gui.utils.no_title_plot_manager import get_plot_manager, apply_no_title_styling
from snid_sage.interfaces.gui.utils.universal_window_manager import get_window_manager, DialogSize

# Import unified theme manager with workflow support
from snid_sage.interfaces.gui.utils.unified_theme_manager import UnifiedThemeManager

# Import platform configuration
from snid_sage.shared.utils.config.platform_config import get_platform_config

# Import new components
from snid_sage.interfaces.gui.components.plots import SpectrumPlotter, SummaryPlotter, InteractiveTools
from snid_sage.interfaces.gui.components.dialogs import MaskManagerDialog, AISummaryDialog, SNIDAnalysisDialog
from snid_sage.interfaces.gui.components.analysis import AnalysisPlotter

# Import new feature controllers
from snid_sage.interfaces.gui.features.preprocessing.preprocessing_controller import PreprocessingController
from snid_sage.interfaces.gui.features.analysis.analysis_controller import AnalysisController
from snid_sage.interfaces.gui.features.analysis.line_detection import LineDetectionController
from snid_sage.interfaces.gui.features.analysis.emission_line_overlay_controller import EmissionLineOverlayController
from snid_sage.interfaces.gui.features.results.llm_integration import LLMIntegration
from snid_sage.interfaces.gui.features.results.results_manager import ResultsManager

# Import new controllers
from snid_sage.interfaces.gui.controllers.app_controller import AppController
from snid_sage.interfaces.gui.controllers.file_controller import FileController
from snid_sage.interfaces.gui.controllers.plot_controller import PlotController
from snid_sage.interfaces.gui.controllers.view_controller import ViewController
from snid_sage.interfaces.gui.controllers.dialog_controller import DialogController

# Import utilities
from snid_sage.interfaces.gui.utils.gui_helpers import GUIHelpers
from snid_sage.interfaces.gui.utils.layout_utils import LayoutUtils
from snid_sage.interfaces.gui.utils.state_manager import StateManager
from snid_sage.interfaces.gui.utils.logo_manager import LogoManager
from snid_sage.interfaces.gui.utils.spectrum_reset_manager import SpectrumResetManager
from snid_sage.interfaces.gui.utils.import_manager import check_optional_features
from snid_sage.interfaces.gui.utils.startup_manager import (StartupManager, setup_dpi_awareness,
                               create_main_gui, destroy_gui_safely,
                               setup_controllers, bind_controller_events,
                               setup_window_properties, setup_cleanup_and_exit)

# Import new event handlers
from snid_sage.interfaces.gui.utils.event_handlers import EventHandlers
from snid_sage.interfaces.gui.utils.window_event_handlers import WindowEventHandlers

# Add plot theming utilities
from snid_sage.shared.utils.plotting.plot_theming import (
    create_plot_with_proper_theming,
    fix_hardcoded_plot_background,
    ensure_plot_theme_consistency
)

# Import centralized logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.sage')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.sage')


class ModernSNIDSageGUI:
    """
    Modern SNID SAGE GUI Interface with Toggle Controls
    
    This class provides a comprehensive spectrum analysis environment that combines
    modern design aesthetics with toggle switches and all the advanced functionality 
    needed for supernova identification and analysis.
    """
    
    def __init__(self, master):
        """Initialize the Modern SNID SAGE GUI"""
        self.master = master
        # Import version dynamically
        try:
            from snid_sage import __version__
        except ImportError:
            __version__ = "unknown"
        
        self.master.title(f"SNID SAGE v{__version__} - Modern Interface")
        
        # Initialize recursion protection flag for view style changes
        self._programmatic_view_change = False
        
        # Initialize GUI logger (auto-configures if needed)
        try:
            from snid_sage.shared.utils.logging import get_logger
            self.logger = get_logger('gui.sage')
        except ImportError:
            self.logger = None
        
        # Setup window properties using the new event handler
        WindowEventHandlers.setup_window_properties(self.master)
        
        # Apply comprehensive Mac improvements globally
        from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
        CrossPlatformWindowManager.integrate_mac_improvements_globally(self.master)
        
        # Initialize unified systems first
        self.font_manager = get_font_manager()
        self.plot_manager = get_plot_manager()
        self.window_manager = get_window_manager()
        
        # Initialize core utilities and managers first
        self.state_manager = StateManager(self)
        self.logo_manager = LogoManager(self)
        self.event_handlers = EventHandlers(self)
        self.startup_manager = StartupManager(self)
        self.view_controller = ViewController(self)
        self.dialog_controller = DialogController(self)
        
        # Initialize platform configuration
        self.platform_config = get_platform_config()
        
        # Initialize unified theme manager first - critical for subsequent components
        self.theme_manager = UnifiedThemeManager(self.master)
        
        # Enhanced macOS coordination: Apply Mac-specific button handling improvements
        if self.platform_config and self.platform_config.is_macos:
            self._setup_enhanced_macos_button_coordination()
        
        # Initialize GUI settings controller
        try:
            from snid_sage.interfaces.gui.features.configuration.gui_settings_controller import GUISettingsController
            self.gui_settings_controller = GUISettingsController(self)
            if self.logger:
                self.logger.debug("GUI settings controller initialized")
        except ImportError:
            self.gui_settings_controller = None
            if self.logger:
                self.logger.warning("GUI settings controller not available")
        
        # Register for theme change callbacks to update plots
        self.theme_manager.add_theme_changed_callback(self._on_theme_changed_comprehensive)
        
        # Setup global plot theming
        try:
            from snid_sage.shared.utils.plotting import setup_plot_theme
            setup_plot_theme(self.theme_manager)
            if self.logger:
                self.logger.debug("Global plot theme setup completed")
        except ImportError:
            if self.logger:
                self.logger.warning("Shared plotting utilities not available - using basic theme setup")
        
        # Initialize configuration manager for templates directory
        from snid_sage.shared.utils.config.configuration_manager import ConfigurationManager
        self.config_manager = ConfigurationManager()
        self.current_config = self.config_manager.load_config()
        
        # Store templates directory for fast access
        self.templates_dir = self.current_config['paths']['templates_dir']
        
        # Initialize variables and state using state manager
        self.state_manager.init_variables()
        self.state_manager.init_llm()
        
        # Load logos using logo manager
        self.logo_manager.load_logos()
        
        # Initialize spectrum reset manager for clean state management
        self.spectrum_reset_manager = SpectrumResetManager(self)
        
        # Create the modern interface
        self.create_interface()
        
        # CRITICAL: Initialize controllers immediately instead of deferring
        self.init_controllers_immediately()
        
        # Apply theme to main window only to avoid interfering with workflow buttons
        # This prevents the dialog creation race condition identified in previous analysis
        self.theme_manager._apply_theme_to_main_window_only()
        
        # THEN update button states to ensure proper initial appearance
        self.update_button_states()
        
        # Don't apply theme again after button states are set
        # This prevents overriding the workflow button colors that were just set
        # The workflow system handles button colors, theme should only handle other elements
        if self.logger:
            self.logger.debug("🎨 Skipped second theme application to preserve workflow button colors")
        
        # Update segmented control buttons after initialization
        self.master.after(100, self._ensure_initial_button_states)
        
        # Setup keyboard shortcuts using event handlers
        self.event_handlers.setup_keyboard_shortcuts()
        
        # Setup window icon before showing
        try:
            from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            CrossPlatformWindowManager.set_window_icon(self.master, 'icon')
            if self.logger:
                self.logger.debug("✅ Window icon set successfully (PNG only)")
        except Exception as e:
            if self.logger:
                self.logger.warning(f"⚠️ Could not set window icon: {e}")

        # Show window and center it properly
        self.master.deiconify()  # Show window
        self.master.update_idletasks()  # Update geometry
        
        # Apply startup settings before showing
        if self.gui_settings_controller:
            self.gui_settings_controller.apply_settings(self.gui_settings_controller.get_current_settings())
            # EXPLICIT FIX: Ensure window is solid (no transparency) regardless of settings
            try:
                self.master.attributes('-alpha', 1.0)  # Force 100% opacity
                if self.logger:
                    self.logger.debug("✅ Window opacity explicitly set to 100% (solid)")
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Could not set window opacity: {e}")

        # Remove fast-launcher positioning flag so centering logic can run again
        if hasattr(self.master, '_fast_launcher_positioned'):
            try:
                delattr(self.master, '_fast_launcher_positioned')
                if self.logger:
                    self.logger.debug("Removed _fast_launcher_positioned flag to allow re-centering")
            except Exception as e:
                if self.logger:
                    self.logger.debug(f"Could not remove fast launcher flag: {e}")

        # Always center the window (ignore any previously saved positions)
        self.master.after(400, lambda: WindowEventHandlers.center_window_safely(self))
        
        # Defer only the heavy, non-critical operations
        self.master.after(100, self.init_remaining_components)
        
        # Initialize plot controller and matplotlib plot after interface is ready
        self.master.after(300, self.init_plot_components)
        
        # Show startup confirmation after everything is ready
        self.master.after(1000, self.show_startup_message)
        
        if self.logger:
            self.logger.info("Modern SNID SAGE GUI initialized successfully!")
            self.logger.debug("Initial theme applied - disabled buttons should be grey")
        
        # Window handling
        if hasattr(self, 'window_event_handlers'):
            self.window_event_handlers.setup()
        
        # Connect proper cleanup to window close
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def init_controllers_immediately(self):
        """Initialize all controllers immediately to ensure they're always available"""
        try:
            if self.logger:
                self.logger.debug("Initializing controllers immediately...")
            
            # Initialize core controllers first
            from snid_sage.interfaces.gui.controllers.app_controller import AppController
            from snid_sage.interfaces.gui.controllers.file_controller import FileController
            self.app_controller = AppController(self)
            self.file_controller = FileController(self)
            if self.logger:
                self.logger.debug("Core controllers (app, file) initialized")
            
            # Initialize feature controllers
            from snid_sage.interfaces.gui.features.preprocessing.preprocessing_controller import PreprocessingController
            from snid_sage.interfaces.gui.features.analysis.analysis_controller import AnalysisController
            from snid_sage.interfaces.gui.features.analysis.line_detection import LineDetectionController
            from snid_sage.interfaces.gui.features.analysis.emission_line_overlay_controller import EmissionLineOverlayController
            from snid_sage.interfaces.gui.features.results.results_manager import ResultsManager
            
            self.preprocessing_controller = PreprocessingController(self)
            self.analysis_controller = AnalysisController(self)
            self.line_detection_controller = LineDetectionController(self)
            self.emission_line_overlay_controller = EmissionLineOverlayController(self)
            self.results_manager = ResultsManager(self)
            if self.logger:
                self.logger.debug("Feature controllers initialized")
            
            if self.logger:
                self.logger.debug("All critical controllers initialized immediately")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error initializing controllers: {e}", exc_info=True)
            else:
                print(f"❌ Error initializing controllers: {e}")
                import traceback
                traceback.print_exc()
    
    def init_remaining_components(self):
        """Initialize remaining optional components after critical ones are ready"""
        try:
            # Initialize workflow integration after interface is created
            if hasattr(self, 'app_controller'):
                self.app_controller.init_workflow_integration()
                # Update button states after workflow integration is initialized
                if hasattr(self.app_controller, '_workflow_initialized') and self.app_controller._workflow_initialized:
                    self.app_controller.update_button_states()
            
            # Initialize plotting components
            try:
                from snid_sage.interfaces.gui.components.plots.summary_plotter import SummaryPlotter
                self.summary_plotter = SummaryPlotter(self)
                if self.logger:
                    self.logger.debug("Summary plotter initialized")
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Summary plotter not available: {e}")
                self.summary_plotter = None
            
            # Initialize spectrum plotter for template overlays
            try:
                from snid_sage.interfaces.gui.components.plots.spectrum_plotter import SpectrumPlotter
                self.spectrum_plotter = SpectrumPlotter(self)
                if self.logger:
                    self.logger.debug("Spectrum plotter initialized")
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Spectrum plotter not available: {e}")
                self.spectrum_plotter = None
            
            # Initialize LLM if available
            try:
                from snid_sage.interfaces.gui.features.results.llm_integration import LLMIntegration
                self.llm_integration = LLMIntegration(self)
                if self.logger:
                    self.logger.debug("LLM integration initialized")
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"LLM integration not available: {e}")
                self.llm_integration = None
                
            # Initialize games if available
            try:
                from snid_sage.interfaces.gui.features.analysis.games_integration import GamesIntegration
                self.games_integration = GamesIntegration(self)
                if self.logger:
                    self.logger.debug("Games integration initialized")
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Games integration not available: {e}")
                self.games_integration = None
            
            # Initialize optional plot features
            try:
        
                # from snid_sage.interfaces.gui.utils.plot_navigator import PlotNavigator
                # self.plot_navigator = PlotNavigator(self)
                # if self.logger: self.logger.debug("Plot navigator initialized")
                self.plot_navigator = None
                if self.logger:
                    self.logger.debug("Plot navigator not implemented yet")
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Plot navigator not available: {e}")
                self.plot_navigator = None
            
            # Add theme change callback for watercolor toggle sync
            self.theme_manager.add_theme_changed_callback(self._on_theme_changed)
            
            if self.logger:
                self.logger.debug("Remaining components initialized")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error initializing remaining components: {e}", exc_info=True)
            else:
                print(f"❌ Error initializing remaining components: {e}")
                import traceback
                traceback.print_exc()
    
    # =============================================================================
    # DELEGATED METHODS - These maintain the same function names but delegate to appropriate controllers
    # =============================================================================
    
    def get_templates_dir(self):
        """Get the SNID templates directory"""
        return self.templates_dir
    
    # Startup and initialization methods - delegate to startup manager
    def show_startup_message(self):
        """Show a startup message to confirm GUI is working"""
        self.startup_manager.show_startup_message()
    
    def init_deferred_components(self):
        """Initialize components that require the GUI to be fully constructed"""
        # Redirect to the new method for compatibility
        self.init_remaining_components()
    
    def init_plot_components(self):
        """Initialize plot controller and matplotlib plot after interface is ready"""
        try:
            from snid_sage.interfaces.gui.controllers.plot_controller import PlotController
            self.plot_controller = PlotController(self)
            
            # Initialize matplotlib plot with proper theming
            self.plot_controller.init_matplotlib_plot()
            
            # Ensure plot uses proper theming
            if hasattr(self, 'fig') and hasattr(self, 'ax'):
                fix_hardcoded_plot_background(self.fig, self.ax, self.theme_manager)
            
            # Initialize analysis plotter for advanced plotting
            from snid_sage.interfaces.gui.components.analysis.analysis_plotter import AnalysisPlotter
            self.analysis_plotter = AnalysisPlotter(self)
            
            # Setup template navigation shortcuts now that plot_controller is available
            if hasattr(self, 'event_handlers'):
                self.event_handlers.setup_template_navigation_shortcuts()
            
            # Initialize interactive tools after matplotlib is ready
            from snid_sage.interfaces.gui.components.plots.interactive_tools import InteractiveTools
            self.interactive_tools = InteractiveTools(self)
            
            # Initialize mask regions if not already done
            if not hasattr(self, 'mask_regions'):
                self.mask_regions = []
            
            if self.logger:
                self.logger.debug("Plot and interactive components initialized")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error initializing plot components: {e}", exc_info=True)
            else:
                print(f"❌ Error initializing plot components: {e}")
                import traceback
                traceback.print_exc()
    
    # Preprocessing methods - delegate to preprocessing controller
    def run_quick_snid_preprocessing(self):
        """Run quick SNID preprocessing - delegate to preprocessing controller"""
        if hasattr(self, 'preprocessing_controller'):
            self.preprocessing_controller.run_quick_snid_preprocessing()
        else:
            messagebox.showerror("Error", "Preprocessing controller not initialized.")
    
    def run_manual_preprocessing_wizard(self):
        """Run manual preprocessing wizard - delegate to preprocessing controller"""
        if hasattr(self, 'preprocessing_controller'):
            self.preprocessing_controller.run_manual_preprocessing_wizard()
        else:
            messagebox.showerror("Error", "Preprocessing controller not initialized.")
    
    def run_snid_preprocessing_only(self, skip_steps=None):
        """Run SNID preprocessing only - delegate to preprocessing controller"""
        if hasattr(self, 'preprocessing_controller'):
            return self.preprocessing_controller.run_snid_preprocessing_only(skip_steps)
        else:
            messagebox.showerror("Error", "Preprocessing controller not initialized.")
            return None
    
    def open_preprocessing_selection(self):
        """Open preprocessing selection dialog - delegate to dialog controller"""
        if hasattr(self, 'dialog_controller'):
            self.dialog_controller.open_preprocessing_selection()
        else:
            messagebox.showerror("Error", "Dialog controller not initialized.")

    def run_quick_preprocessing_and_analysis(self):
        """
        Run quick preprocessing followed by quick analysis in one go.
        
        This is a convenience method that combines both operations for a streamlined workflow.
        Perfect for users who want to quickly process and analyze their spectrum with default settings.
        
        Keyboard shortcut: Ctrl+Enter (Windows/Linux) or Cmd+Enter (Mac)
        """
        if not self.file_path:
            messagebox.showwarning("No Spectrum", "Please load a spectrum file first.")
            return
        
        try:
            # Update header status to show we're starting the combined workflow
            self.update_header_status("🚀 Starting quick preprocessing + analysis workflow...")
            
            # Step 1: Run quick preprocessing (silent version to avoid duplicate status messages)
            if hasattr(self, 'preprocessing_controller'):
                self.preprocessing_controller.run_quick_snid_preprocessing_silent()
                
                # Wait a brief moment for preprocessing to complete and update states
                self.master.update_idletasks()
                
                # Check if preprocessing was successful by verifying we have processed spectrum
                if hasattr(self, 'processed_spectrum') and self.processed_spectrum is not None:
                    # Step 2: Run quick analysis with default settings
                    self.update_header_status("✅ Preprocessing complete - now running SNID analysis...")
                    
                    # Brief delay to ensure UI updates are visible
                    self.master.after(500, self._run_analysis_after_preprocessing)
                else:
                    self.update_header_status("❌ Preprocessing failed - analysis cannot proceed")
                    messagebox.showerror("Workflow Error", 
                                       "Quick preprocessing failed. Cannot proceed with analysis.\n"
                                       "Please check your spectrum file and try preprocessing manually.")
            else:
                messagebox.showerror("Error", "Preprocessing controller not initialized.")
                
        except Exception as e:
            error_msg = f"Combined preprocessing + analysis workflow failed: {str(e)}"
            self.update_header_status(f"❌ {error_msg}")
            messagebox.showerror("Workflow Error", error_msg)
    
    def _run_analysis_after_preprocessing(self):
        """Helper method to run analysis after preprocessing is complete"""
        try:
            if hasattr(self, 'analysis_controller'):
                # Run the analysis
                self.analysis_controller.run_snid_analysis_only()
                self.update_header_status("🎉 Combined workflow complete - preprocessing + analysis finished!")
            else:
                messagebox.showerror("Error", "Analysis controller not initialized.")
        except Exception as e:
            error_msg = f"Analysis phase failed: {str(e)}"
            self.update_header_status(f"❌ {error_msg}")
            messagebox.showerror("Analysis Error", error_msg)

    # Line detection methods - delegate to line detection controller
    def auto_detect_and_compare_lines(self):
        """Auto-detect spectral lines - delegate to line detection controller"""
        if hasattr(self, 'line_detection_controller'):
            self.line_detection_controller.auto_detect_and_compare_lines()
        else:
            messagebox.showerror("Error", "Line detection controller not initialized.")
    
    def search_nist_for_lines(self):
        """Search NIST database - delegate to line detection controller"""
        if hasattr(self, 'line_detection_controller'):
            self.line_detection_controller.search_nist_for_lines()
        else:
            messagebox.showerror("Error", "Line detection controller not initialized.")
    
    def clear_line_markers(self):
        """Clear line markers - delegate to line detection controller"""
        if hasattr(self, 'line_detection_controller'):
            self.line_detection_controller.clear_line_markers()
        else:
            print("⚠️ Line detection controller not initialized")
    
    def open_emission_line_overlay(self):
        """Open emission line overlay dialog - delegate to emission line overlay controller"""
        if hasattr(self, 'emission_line_overlay_controller'):
            self.emission_line_overlay_controller.open_emission_line_overlay()
        else:
            messagebox.showerror("Error", "Emission line overlay controller not initialized.")
    
    def open_redshift_selection(self):
        """Open combined redshift selection dialog - delegate to line detection controller"""
        if hasattr(self, 'line_detection_controller'):
            self.line_detection_controller.open_combined_redshift_selection()
        else:
            messagebox.showerror("Error", "Line detection controller not initialized.")
    
    def _show_unified_ai_dialog(self):
        """Show the enhanced AI assistant dialog with configuration, summary, and chat"""
        try:
            from snid_sage.interfaces.gui.components.dialogs.enhanced_ai_assistant_dialog import EnhancedAIAssistantDialog
            
            # Pass current SNID results if available
            snid_results = getattr(self, 'snid_results', None)
            dialog = EnhancedAIAssistantDialog(self)
            dialog.show(snid_results=snid_results)
        except Exception as e:
            messagebox.showerror("AI Assistant Error", f"Error opening AI Assistant: {str(e)}")
            if self.logger:
                self.logger.error(f"Error opening enhanced AI assistant dialog: {e}")
    
    def _show_enhanced_ai_assistant(self):
        """Show the enhanced AI assistant dialog with improved UI"""
        try:
            from snid_sage.interfaces.gui.components.dialogs.enhanced_ai_assistant_dialog import EnhancedAIAssistantDialog
            
            # Pass current SNID results if available
            snid_results = getattr(self, 'snid_results', None)
            dialog = EnhancedAIAssistantDialog(self)
            dialog.show(snid_results=snid_results)
            
        except Exception as e:
            messagebox.showerror("AI Assistant Error", f"Error opening Enhanced AI Assistant: {str(e)}")
            if self.logger:
                self.logger.error(f"Error opening enhanced AI assistant: {e}")

    def open_snid_analysis_dialog(self):
        """Open the unified SNID Analysis dialog"""
        try:
            # Create and show the dialog
            dialog = SNIDAnalysisDialog(self.master, self)
            result = dialog.show()
            
            if result:
                # Dialog handles execution, so we just update status
                self.update_header_status("🚀 SNID Analysis dialog opened")
            else:
                self.update_header_status("SNID Analysis cancelled")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open SNID Analysis dialog:\n{str(e)}")
            if self.logger:
                self.logger.error(f"Failed to open SNID Analysis dialog: {e}")
    
    # App control methods - delegate to app controller
    def update_button_states(self):
        """Update button states - delegate to app controller"""
        if hasattr(self, 'app_controller'):
            self.app_controller.update_button_states()
        else:
            print("⚠️ App controller not available for button state updates")
    
    def _restore_button_colors(self):
        """Restore button colors - delegate to app controller"""
        if hasattr(self, 'app_controller'):
            self.app_controller._restore_button_colors()
    
    def enable_plot_navigation(self):
        """Enable plot navigation - delegate to view controller"""
        self.view_controller.enable_plot_navigation()
    
    def _parse_wavelength_masks(self, mask_str):
        """Parse wavelength masks - use utility function"""
        return GUIHelpers.parse_wavelength_masks(mask_str)
    
    def _parse_age_range(self):
        """Parse age range - delegate to app controller"""
        if hasattr(self, 'app_controller'):
            return self.app_controller._parse_age_range()
        else:
            return -20, 300  # Default fallback
    
    def _parse_type_filter(self):
        """Parse type filter - delegate to app controller"""
        if hasattr(self, 'app_controller'):
            return self.app_controller._parse_type_filter()
        else:
            return None  # Default fallback
    
    def _parse_template_filter(self):
        """Parse template filter from parameters"""
        template_filter = self.params.get('template_filter', None)
        
        # DEBUG: Log what we're parsing
        if hasattr(self, 'logger') and self.logger:
            self.logger.info(f"DEBUG: _parse_template_filter called")
            self.logger.info(f"DEBUG: template_filter param: {template_filter}")
            self.logger.info(f"DEBUG: template_filter type: {type(template_filter)}")
        
        if template_filter:
            if isinstance(template_filter, list):
                if hasattr(self, 'logger') and self.logger:
                    self.logger.info(f"DEBUG: Returning list: {template_filter}")
                return template_filter
            elif isinstance(template_filter, str):
                result = [t.strip() for t in template_filter.split(',') if t.strip()]
                if hasattr(self, 'logger') and self.logger:
                    self.logger.info(f"DEBUG: Parsed string to list: {result}")
                return result
        
        if hasattr(self, 'logger') and self.logger:
            self.logger.info(f"DEBUG: Returning None (no template filter)")
        return None
    
    def configure_options(self):
        """Configure options - delegate to dialog controller"""
        self.dialog_controller.configure_options()
    
    def toggle_additional_tools(self, event=None):
        """Toggle additional tools - delegate to event handlers"""
        if hasattr(self, 'event_handlers'):
            self.event_handlers.toggle_additional_tools(event)
    
    def _on_click(self, event):
        """Handle plot clicks - delegate to event handlers"""
        if hasattr(self, 'event_handlers'):
            self.event_handlers._on_click(event)
    
    def start_games_menu(self):
        """Start games menu - delegate to event handlers"""
        if hasattr(self, 'event_handlers'):
            self.event_handlers.start_games_menu()
    
    def center_window_safely(self):
        """Center window safely - delegate to window event handlers"""
        WindowEventHandlers.center_window_safely(self)
    
    def schedule_keep_alive(self):
        """Schedule keep alive - delegate to event handlers"""
        if hasattr(self, 'event_handlers'):
            self.event_handlers.schedule_keep_alive()
    
    # Utility functions - delegate to GUIHelpers
    def _safe_float(self, value, default=0.0):
        """Safely convert to float - use utility function"""
        return GUIHelpers.safe_float(value, default)
    
    def _safe_int(self, value, default=0):
        """Safely convert to int - use utility function"""
        return GUIHelpers.safe_int(value, default)
    
    def _safe_bool(self, value, default=False):
        """Safely convert to bool - use utility function"""
        return GUIHelpers.safe_bool(value, default)
    
    def _filter_nonzero_spectrum(self, wave, flux, processed_spectrum=None):
        """Filter nonzero spectrum - use utility function"""
        return GUIHelpers.filter_nonzero_spectrum(wave, flux, processed_spectrum)
    
    # View methods - delegate to view controller
    def _on_view_style_change(self, *args):
        """Handle changes to the view style segmented control"""
        # NEW: Prevent recursion during programmatic updates
        if hasattr(self, '_programmatic_view_change') and self._programmatic_view_change:
            if hasattr(self, 'logger') and self.logger:
                self.logger.debug("🚫 Skipping _on_view_style_change during programmatic update")
            return
            
        if hasattr(self, 'plot_controller'):
            self.plot_controller._on_view_style_change(*args)
        else:
            print("⚠️ Plot controller not initialized yet")
    
    def create_right_panel(self, parent):
        """Create right panel - delegate to view controller"""
        self.view_controller.create_right_panel(parent)
    
    def switch_mode(self):
        """Switch between flux and flat view modes"""
        self.view_controller.switch_mode()
    
    def refresh_current_view(self):
        """Refresh the current view - delegate to view controller"""
        self.view_controller.refresh_current_view()
    
    def plot_flux_view(self):
        """Plot flux view - delegate to view controller"""
        self.view_controller.plot_flux_view()
    
    def plot_flat_view(self):
        """Plot flattened view - delegate to view controller"""
        self.view_controller.plot_flat_view()
    
    def plot_original_spectrum(self):
        """Plot original spectrum - delegate to view controller"""
        self.view_controller.plot_original_spectrum()
    
    def plot_original_spectra(self):
        """Plot original spectra - alias for compatibility"""
        # This is called by analysis_controller - delegate to spectrum plotter for template overlays
        try:
            if hasattr(self, 'snid_results') and self.snid_results:
                # Ensure view is set to Flux when showing SNID results
                if hasattr(self, 'view_style') and self.view_style:
                    # Set flag to prevent recursion during programmatic change
                    self._programmatic_view_change = True
                    try:
                        self.view_style.set("Flux")
                        if self.logger:
                            self.logger.debug("🔄 View style set to Flux for SNID results display")
                        
                        # Update segmented control buttons
                        if hasattr(self, '_update_segmented_control_buttons'):
                            self._update_segmented_control_buttons()
                            if self.logger:
                                self.logger.debug("✅ Segmented control buttons updated for Flux view")
                    finally:
                        self._programmatic_view_change = False
                
                # We have SNID results - use template overlay functionality
                if hasattr(self, 'spectrum_plotter') and self.spectrum_plotter:
                    if self.logger:
                        self.logger.debug("Plotting flux view with template overlay (via spectrum plotter)")
                    self.spectrum_plotter.plot_original_spectra()
                elif hasattr(self, 'plot_controller') and self.plot_controller:
                    if self.logger:
                        self.logger.debug("Plotting flux view with template overlay (via plot controller)")
                    self.plot_controller._plot_snid_results(flattened=False)
                else:
                    # Fallback to view controller
                    if self.logger:
                        self.logger.debug("Plotting flux view (fallback to view controller)")
                    self.view_controller.plot_original_spectrum()
            else:
                # No SNID results - just plot the spectrum
                if self.logger:
                    self.logger.debug("Plotting original spectrum (no templates)")
                self.view_controller.plot_original_spectrum()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error in plot_original_spectra: {e}")
            # Fallback to view controller
            self.view_controller.plot_original_spectrum()
    
    def _plot_snid_results(self, flattened=False):
        """Plot SNID results - delegate to view controller"""
        self.view_controller._plot_snid_results(flattened)
    
    def plot_preprocessed_spectrum(self, wave, flux):
        """Plot preprocessed spectrum - delegate to spectrum plotter component"""
        try:
            # If we have a spectrum plotter component, use it
            if hasattr(self, 'spectrum_plotter') and self.spectrum_plotter:
                self.spectrum_plotter.plot_preprocessed_spectrum(wave, flux)
            # Otherwise, delegate to view controller as fallback
            elif hasattr(self, 'view_controller'):
                self.view_controller.plot_preprocessed_spectrum(wave, flux)
            else:
                # Basic fallback if components not available
                if self.logger:
                    self.logger.warning("Plotting components not available, using basic plot")
                if hasattr(self, 'ax') and self.ax:
                    self.ax.clear()
                    self.ax.plot(wave, flux, 'b-', linewidth=2)
                    # Apply no-title styling per user requirement
                    apply_no_title_styling(self.fig, self.ax, "Wavelength (Å)", "Flux", self.theme_manager)
                    if hasattr(self, 'canvas') and self.canvas:
                        self.canvas.draw()
                    if self.logger:
                        self.logger.debug("Preprocessed spectrum plotted")
                else:
                    if self.logger:
                        self.logger.error("No plotting infrastructure available")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error plotting preprocessed spectrum: {e}")
                self.logger.debug("Preprocessed spectrum plotting error details:", exc_info=True)
    
    def update_header_status(self, message):
        """Update header status message"""
        self.view_controller.update_header_status(message)
    
    def get_effective_redshift_range(self):
        """Get effective redshift range based on manual redshift or default parameters"""
        # Check if we have a manually determined redshift
        manual_redshift = self.params.get('redshift')
        
        if manual_redshift is not None:
            try:
                z_manual = float(manual_redshift)
                
                # Get custom range from galaxy_redshift_result if available
                z_range = 0.01  # Default range
                if hasattr(self, 'galaxy_redshift_result') and self.galaxy_redshift_result:
                    mode_result = self.galaxy_redshift_result.get('mode_result', {})
                    if isinstance(mode_result, dict):
                        z_range = mode_result.get('search_range', 0.01)
                
                zmin_effective = max(-0.01, z_manual - z_range)  # Don't go below -0.01
                zmax_effective = z_manual + z_range
                
                self.logger.info(f"🎯 Using manual redshift z={z_manual:.4f}, constraining search to {zmin_effective:.4f} - {zmax_effective:.4f} (±{z_range:.4f})")
                return zmin_effective, zmax_effective, True  # True indicates manual constraint
                
            except (ValueError, TypeError):
                self.logger.warning(f"⚠️ Invalid manual redshift value: {manual_redshift}, using default range")
        
        # Fall back to default parameter range
        zmin_default = self._safe_float(self.params.get('zmin', ''), -0.01)
        zmax_default = self._safe_float(self.params.get('zmax', ''), 1.0)
        
        return zmin_default, zmax_default, False  # False indicates no manual constraint
    
    def update_redshift_status(self, redshift=None, method=None, **kwargs):
        """Update the redshift status label"""
        if not hasattr(self, 'redshift_status_label'):
            return
            
        if redshift is None:
            # No redshift chosen – keep optional note
            self.redshift_status_label.configure(
                text="Optional: no redshift selected",
                fg=self.theme_manager.get_color('text_secondary')
            )
        else:
            # Compose status text with check-mark
            if 'zmin' in kwargs and 'zmax' in kwargs:
                status_text = f"✅ z = {kwargs['zmin']:.4f} – {kwargs['zmax']:.4f}"
            else:
                # Fixed single redshift
                status_text = f"✅ z = {redshift:.4f}"

            # Append origin suffix
            if method == 'manual':
                status_text += " (manual)"
            elif method == 'auto':
                rlap = kwargs.get('rlap', '')
                if rlap:
                    status_text += f" (auto, rlap {rlap:.1f})"
                else:
                    status_text += " (auto)"

            # Update label colour to primary text (black) for consistency
            self.redshift_status_label.configure(
                text=status_text,
                fg=self.theme_manager.get_color('text_primary')
            )
    
    def clear_redshift_status(self):
        """Clear the redshift status and remove manual redshift constraint"""
        # Clear the manual redshift parameter
        if 'redshift' in self.params:
            del self.params['redshift']
        
        # Clear any stored redshift results
        if hasattr(self, 'galaxy_redshift_result'):
            delattr(self, 'galaxy_redshift_result')
        
        # Update status display
        self.update_redshift_status()
        
        # Update configuration display to show default range
        try:
            from snid_sage.interfaces.gui.utils.layout_utils import LayoutUtils
            LayoutUtils.update_config_display(self)
        except ImportError:
            pass  # Graceful fallback if import fails
        
        self.logger.info("🗑️ Cleared manual redshift constraint")

    # Interface creation and initialization
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts - delegate to event handlers"""
        if hasattr(self, 'event_handlers'):
            self.event_handlers.setup_keyboard_shortcuts()
    
    def init_variables(self):
        """Initialize application state variables - delegate to state manager"""
        self.state_manager.init_variables()
    
    def init_llm(self):
        """Initialize LLM settings - delegate to state manager"""
        self.state_manager.init_llm()
    
    def create_interface(self):
        """Create the modern interface - delegate to layout utils"""
        try:
            # Create the main layout structure
            main_container, header_frame, content_frame = LayoutUtils.create_main_layout(self, self.master)
            
            if main_container and header_frame and content_frame:
                # Create the two-panel layout within the content frame (removed right panel)
                LayoutUtils.create_left_panel(self, content_frame)
                LayoutUtils.create_center_panel(self, content_frame)
                # LayoutUtils.create_right_panel(self, content_frame)  # Right panel removed
                
                _LOGGER.info("✅ Interface created successfully")
            else:
                raise Exception("Failed to create main layout structure")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating interface: {e}")
                self.logger.debug("Interface creation error details:", exc_info=True)
            print(f"ERROR: Error creating interface: {e}")
    
    def browse_file(self):
        """Browse for a spectrum file - delegate to file controller"""
        if hasattr(self, 'file_controller'):
            self.file_controller.browse_file()
        else:
            # Fallback for early initialization
            from tkinter import messagebox
            messagebox.showinfo("File Loading", "File controller is initializing...\n"
                              "Please wait for initialization to complete.")

    # Plot methods - delegate to plot controller
    def init_matplotlib_plot(self):
        """Initialize matplotlib plot with proper theming - delegate to plot controller"""
        if hasattr(self, 'plot_controller'):
            self.plot_controller.init_matplotlib_plot()
            
            # Ensure plot uses proper theming
            if hasattr(self, 'fig') and hasattr(self, 'ax'):
                fix_hardcoded_plot_background(self.fig, self.ax, self.theme_manager)
        else:
            if self.logger:
                self.logger.debug("Plot controller not initialized yet")
    
    def _apply_plot_theme(self):
        """Apply current theme to matplotlib plot - delegate to plot controller"""
        if hasattr(self, 'plot_controller'):
            self.plot_controller._apply_plot_theme()
        else:
            if self.logger:
                self.logger.debug("Plot controller not initialized yet")
    
    def prev_template(self):
        """Navigate to previous template - delegate to plot controller"""
        if hasattr(self, 'plot_controller'):
            self.plot_controller.prev_template()
        else:
            if self.logger:
                self.logger.debug("Plot controller not initialized yet")
    
    def next_template(self):
        """Navigate to next template - delegate to plot controller"""
        if hasattr(self, 'plot_controller'):
            self.plot_controller.next_template()
        else:
            if self.logger:
                self.logger.debug("Plot controller not initialized yet")
    
    def show_template(self):
        """Show current template - delegate to plot controller"""
        if hasattr(self, 'plot_controller'):
            self.plot_controller.show_template()
        else:
            if self.logger:
                self.logger.debug("Plot controller not initialized yet")

    # Logo methods - delegate to logo manager
    def load_logos(self):
        """Load logos - delegate to logo manager"""
        if hasattr(self, 'logo_manager'):
            self.logo_manager.load_logos()
    
    def update_logo(self, dark_mode_enabled=None):
        """Update logo - delegate to logo manager"""
        if hasattr(self, 'logo_manager'):
            self.logo_manager.update_logo(dark_mode_enabled)
    
    @property
    def current_logo(self):
        """Get current logo - delegate to logo manager"""
        if hasattr(self, 'logo_manager'):
            return self.logo_manager.get_current_logo()
        return None
    
    @property
    def logo_label(self):
        """Get logo label - delegate to logo manager"""
        if hasattr(self, 'logo_manager'):
            return self.logo_manager.logo_label
        return None
    
    @logo_label.setter
    def logo_label(self, value):
        """Set logo label - delegate to logo manager"""
        if hasattr(self, 'logo_manager'):
            self.logo_manager.set_logo_label(value)

    # Analysis methods - delegate to analysis controller
    def run_snid_analysis_only(self):
        """Run SNID analysis only - delegate to analysis controller"""
        if hasattr(self, 'analysis_controller'):
            self.analysis_controller.run_snid_analysis_only()
        else:
            messagebox.showerror("Error", "Analysis controller not initialized.")
    
    def run_snid_analysis(self):
        """Run full SNID analysis - delegate to analysis controller"""
        if hasattr(self, 'analysis_controller'):
            self.analysis_controller.run_snid_analysis_only()
        else:
            messagebox.showerror("Error", "Analysis controller not initialized.")
    
    # Advanced plotting methods - delegate to appropriate plotters




    def plot_both_views(self):
        """Plot both flux and flat views side by side"""
        try:
            # Delegate to view controller for plotting both views
            if hasattr(self, 'view_controller'):
                self.view_controller.plot_both_views()
            else:
                print("⚠️ View controller not initialized")
        except Exception as e:
            self.logger.error(f"Error plotting both views: {e}")
            import traceback
            traceback.print_exc()
            self._plot_error(f"Error plotting both views: {str(e)}")

    def plot_gmm_clustering(self):
        """Plot GMM clustering analysis using the plot controller"""
        try:
            # Delegate to plot controller for proper state management
            if hasattr(self, 'plot_controller'):
                self.plot_controller.plot_gmm_clustering()
            else:
                self.logger.error("Plot controller not available")
                self._plot_error("Plot controller not available")
            
        except Exception as e:
            self.logger.error(f"Error plotting GMM clustering: {e}")
            import traceback
            traceback.print_exc()
            self._plot_error(f"Error plotting GMM clustering: {str(e)}")

    def plot_redshift_age(self):
        """Plot redshift vs age analysis using the plot controller"""
        try:
            # Delegate to plot controller for proper state management
            if hasattr(self, 'plot_controller'):
                self.plot_controller.plot_redshift_age()
            else:
                self.logger.error("Plot controller not available")
                self._plot_error("Plot controller not available")
            
        except Exception as e:
            self.logger.error(f"Error plotting redshift vs age: {e}")
            import traceback
            traceback.print_exc()
            self._plot_error(f"Error plotting redshift vs age: {str(e)}")

    def plot_subtype_proportions(self):
        """Plot subtype proportions within selected cluster using the plot controller"""
        try:
            # Delegate to plot controller for proper state management
            if hasattr(self, 'plot_controller'):
                self.plot_controller.plot_subtype_proportions()
            else:
                self.logger.error("Plot controller not available")
                self._plot_error("Plot controller not available")
            
        except Exception as e:
            self.logger.error(f"Error plotting subtype proportions: {e}")
            import traceback
            traceback.print_exc()
            self._plot_error(f"Error plotting subtype proportions: {str(e)}")
    
    def show_cluster_summary(self):
        """Show unified analysis results summary (same as results summary)"""
        try:
            # Check if we have results available
            if not hasattr(self, 'snid_results') or not self.snid_results:
                messagebox.showwarning("No Analysis Results", 
                                                     "No SNID-SAGE analysis results available.\n"
                "Run SNID-SAGE analysis first to generate results.")
                return
            
            # Show the unified results summary (includes clustering info if available)
            self.show_results_summary(self.snid_results)
            
            if self.logger:
                self.logger.info("📊 Opened unified analysis results summary")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error showing analysis summary: {e}")
            messagebox.showerror("Analysis Summary Error", f"Failed to show analysis summary: {str(e)}")

    def show_results_summary(self, result):
        """Show results summary - delegate to analysis controller for simple text-based summary"""
        if hasattr(self, 'analysis_controller') and self.analysis_controller:
            self.analysis_controller.show_results_summary(result)
        else:
            print("⚠️ Analysis controller not initialized")
    
    def update_results_display(self, result):
        """Update results display - delegate to analysis controller"""
        if hasattr(self, 'analysis_controller'):
            self.analysis_controller.update_results_display(result)
        else:
            print("⚠️ Analysis controller not initialized")
    
    # Dialog methods - delegate to dialog controller
    def open_preprocessing_dialog(self):
        """Open preprocessing dialog - delegate to dialog controller"""
        self.dialog_controller.open_preprocessing_dialog()
    
    def _open_settings_dialog(self):
        """Open the GUI settings dialog"""
        try:
            if self.gui_settings_controller:
                result = self.gui_settings_controller.show_settings_dialog()
                if result:
                    if self.logger:
                        self.logger.info("GUI settings updated successfully")
                    
                    # Update header status to reflect settings change
                    self.update_header_status("⚙️ Settings updated - Changes applied to interface")
                    
                    # Only update matplotlib plots, never touch GUI buttons
                    if hasattr(self, 'theme_manager'):
                        self.theme_manager._update_all_plots()  # Direct call to avoid button interference
                        if self.logger:
                            self.logger.info("🎨 Updated matplotlib theme only, preserved button colors")
                else:
                    if self.logger:
                        self.logger.debug("Settings dialog cancelled")
            else:
                if self.logger:
                    self.logger.error("GUI settings controller not available")
                messagebox.showerror("Settings Error", 
                                   "Settings controller not available.\n\n"
                                   "Please restart the application to access settings.")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error opening settings dialog: {e}")
            messagebox.showerror("Settings Error", 
                               f"Error opening settings dialog:\n\n{str(e)}")
    
    def _show_shortcuts_dialog(self):
        """Show the keyboard shortcuts dialog"""
        try:
            from snid_sage.interfaces.gui.components.dialogs.shortcuts_dialog import ShortcutsDialog
            shortcuts_dialog = ShortcutsDialog(self.master, self.theme_manager)
            shortcuts_dialog.show()
            
            if self.logger:
                self.logger.info("✅ Shortcuts dialog opened")
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error opening shortcuts dialog: {e}")
            messagebox.showerror("Shortcuts Error", 
                               f"Error opening shortcuts dialog:\n\n{str(e)}")
    
    def _on_theme_changed(self, theme_name):
        """Handle theme changes - simplified for light mode only"""
        try:
            # Update logo manager (now always light mode)
            if hasattr(self, 'logo_manager'):
                self.logo_manager.update_logo(False)  # Always light mode
                
        except Exception as e:
            print(f"❌ Error handling theme change: {e}")
    
    def _on_theme_changed_comprehensive(self, theme_name):
        """Comprehensive theme change handler that updates all plots and components"""
        try:
            if self.logger:
                self.logger.debug(f"🎨 Theme changed to: {theme_name}")
            
            # Call the original theme handler
            self._on_theme_changed(theme_name)
            
            # Update global plot theme
            try:
                from snid_sage.shared.utils.plotting import setup_plot_theme
                setup_plot_theme(self.theme_manager)
            except ImportError:
                pass
            
            # Update current matplotlib plot if it exists
            if hasattr(self, 'fig') and self.fig and hasattr(self, 'ax') and self.ax:
                try:
                    self.theme_manager.update_matplotlib_plot(self.fig, self.ax)
                    if hasattr(self, 'canvas') and self.canvas:
                        self.canvas.draw_idle()
                    if self.logger:
                        self.logger.debug("🎨 Updated main matplotlib plot for new theme")
                except Exception as e:
                    if self.logger:
                        self.logger.warning(f"Warning: Could not update main plot theme: {e}")
            
            # Update plots in dialog windows and components
            self._update_component_themes(theme_name)
            
            # Update only matplotlib figures, never touch GUI buttons
            self.theme_manager._update_all_plots()
            
            if self.logger:
                self.logger.debug(f"🎨 Comprehensive theme change completed: {theme_name}")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error in comprehensive theme change handler: {e}")
            else:
                print(f"❌ Error in comprehensive theme change handler: {e}")
    
    def _update_component_themes(self, theme_name):
        """Update themes in all components that have plots"""
        try:
            # Update preprocessing dialog plots if open
            if hasattr(self, 'preprocessing_controller') and self.preprocessing_controller:
                try:
                    self.preprocessing_controller.update_theme(theme_name)
                except:
                    pass
            
            # Update analysis plots
            if hasattr(self, 'analysis_controller') and self.analysis_controller:
                try:
                    self.analysis_controller.update_theme(theme_name)
                except:
                    pass
            
            # Update plot controller
            if hasattr(self, 'plot_controller') and self.plot_controller:
                try:
                    self.plot_controller.update_theme(theme_name)
                except:
                    pass
            
            # Update other components with plots
            for component_name in ['line_detection_controller', 'results_manager']:
                if hasattr(self, component_name):
                    component = getattr(self, component_name)
                    if hasattr(component, 'update_theme'):
                        try:
                            component.update_theme(theme_name)
                        except:
                            pass
            
            if self.logger:
                self.logger.debug("🎨 Updated component themes")
                
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Warning: Could not update all component themes: {e}")
    
    def _apply_plot_theme(self):
        """Apply current theme to the main matplotlib plot"""
        try:
            if hasattr(self, 'fig') and self.fig and hasattr(self, 'ax') and self.ax:
                self.theme_manager.update_matplotlib_plot(self.fig, self.ax)
                if self.logger:
                    self.logger.debug("🎨 Applied plot theme to main plot")
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Warning: Could not apply plot theme: {e}")

    def toggle_interactive_masking(self):
        """Toggle interactive masking mode - delegate to interactive tools"""
        try:
            if hasattr(self, 'interactive_tools') and self.interactive_tools:
                self.interactive_tools.toggle_interactive_masking()
            else:
                print("⚠️ Interactive tools not initialized yet")
                # Initialize interactive tools if not already done
                if hasattr(self, 'fig') and self.fig and hasattr(self, 'ax') and self.ax:
                    from snid_sage.interfaces.gui.components.plots.interactive_tools import InteractiveTools
                    self.interactive_tools = InteractiveTools(self)
                    self.interactive_tools.toggle_interactive_masking()
                else:
                    from tkinter import messagebox
                    messagebox.showwarning("Not Ready", 
                                         "Please load a spectrum first before using interactive masking.")
        except Exception as e:
            print(f"❌ Error toggling interactive masking: {e}")
            from tkinter import messagebox
            messagebox.showerror("Masking Error", f"Failed to toggle interactive masking: {str(e)}")

    def start_interactive_masking_dialog(self, dialog_window=None):
        """Start interactive masking with optional dialog window"""
        try:
            if hasattr(self, 'interactive_tools') and self.interactive_tools:
                if dialog_window:
                    self.interactive_tools.start_interactive_masking_dialog(dialog_window)
                else:
                    self.interactive_tools.start_interactive_masking()
            else:
                # Initialize interactive tools if not already done
                if hasattr(self, 'fig') and self.fig and hasattr(self, 'ax') and self.ax:
                    from snid_sage.interfaces.gui.components.plots.interactive_tools import InteractiveTools
                    self.interactive_tools = InteractiveTools(self)
                    if dialog_window:
                        self.interactive_tools.start_interactive_masking_dialog(dialog_window)
                    else:
                        self.interactive_tools.start_interactive_masking()
                else:
                    from tkinter import messagebox
                    messagebox.showwarning("Not Ready", 
                                         "Please load a spectrum first before using interactive masking.")
        except Exception as e:
            _LOGGER.error(f"❌ Error starting interactive masking dialog: {e}")
            from tkinter import messagebox
            messagebox.showerror("Masking Error", f"Failed to start interactive masking: {str(e)}")

    def update_plot_with_masks(self):
        """Update the plot to show current mask regions"""
        try:
            if hasattr(self, 'interactive_tools') and self.interactive_tools:
                # Sync mask regions with interactive tools
                if hasattr(self, 'mask_regions'):
                    self.interactive_tools.set_masks(self.mask_regions)
                self.interactive_tools._update_mask_display()
            else:
                _LOGGER.warning("⚠️ Interactive tools not available for mask display")
        except Exception as e:
            _LOGGER.error(f"❌ Error updating plot with masks: {e}")

    # Plot utility methods - needed by plotting components
    def _finalize_plot(self):
        """Finalize plot with consistent styling and theme"""
        try:
            if not hasattr(self, 'fig') or not self.fig:
                return
            
            # Apply current theme to all plot elements
            self._apply_plot_theme()
            
            # Handle multiple axes if they exist
            axes = self.fig.get_axes()
            if not axes:
                return
            
            # Update primary axis reference (for single-axis compatibility)
            if axes:
                self.ax = axes[0]
                
                # If we had an active span selector, we need to recreate it for the new axis
                if hasattr(self, 'is_masking_active') and self.is_masking_active and hasattr(self, 'span_selector') and self.span_selector:
                    try:
                        # Deactivate old span selector
                        self.span_selector.set_active(False)
                        self.span_selector = None
                        # The span selector will be recreated next time interactive masking is started
                    except:
                        pass  # Ignore errors during cleanup
            
            # Tight layout and draw
            self.fig.tight_layout()
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.draw()
            
        except Exception as e:
            _LOGGER.error(f"Error finalizing plot: {e}")
            # Fallback to basic draw
            try:
                if hasattr(self, 'canvas') and self.canvas:
                    self.canvas.draw()
            except:
                pass

    def _finalize_plot_standard(self):
        """Finalize plot with standardized styling and theme"""
        try:
            if not hasattr(self, 'fig') or not self.fig:
                return
            
            # Apply current theme to all plot elements
            self._apply_plot_theme()
            
            # Handle multiple axes if they exist
            axes = self.fig.get_axes()
            if not axes:
                return
            
            # Update primary axis reference (for single-axis compatibility)
            if axes:
                self.ax = axes[0]
            
            # Apply tight layout and draw
            self.fig.tight_layout()
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.draw()
            
        except Exception as e:
            _LOGGER.error(f"Error finalizing standardized plot: {e}")
            # Fallback to basic finalize
            self._finalize_plot()

    def _plot_error(self, error_message):
        """Display an error message on the plot"""
        try:
            if not hasattr(self, 'ax') or not self.ax:
                print(f"Plot error (no axis): {error_message}")
                return
            
            self.ax.clear()
            
            # Get theme colors
            theme = self.theme_manager.get_current_theme()
            text_color = theme.get('text_color', 'black')
            danger_color = theme.get('danger_color', 'red')
            bg_color = theme.get('bg_primary', 'white')
            
            self.ax.text(0.5, 0.5, error_message, 
                       ha='center', va='center', transform=self.ax.transAxes,
                       fontsize=12, color=danger_color,
                       bbox=dict(boxstyle='round,pad=0.5', facecolor=bg_color, alpha=0.8))
            # No title per user requirement
            
            # Remove axis ticks and labels for clean error display
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            
            self._finalize_plot()
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error displaying plot error: {e}")
                self._logger.error(f"Original plot error: {error_message}")
            else:
                # Fallback - just print to console if no logger
                print(f"Error displaying plot error: {e}")
                print(f"Original plot error: {error_message}")

    def _clear_plot_with_theme(self):
        """Clear plot and apply theme colors"""
        try:
            if hasattr(self, 'ax') and self.ax:
                self.ax.clear()
            if hasattr(self, 'fig') and self.fig:
                # Apply theme to figure background
                theme = self.theme_manager.get_current_theme()
                self.fig.patch.set_facecolor(theme.get('bg_color', 'white'))
                if hasattr(self, 'ax') and self.ax:
                    self.ax.set_facecolor(theme.get('plot_bg_color', 'white'))
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error clearing plot with theme: {e}")
            else:
                print(f"Error clearing plot with theme: {e}")

    def _standardize_plot_styling(self, title="", xlabel="Wavelength (Å)", ylabel="Flux", clear_plot=True):
        """Standardize plot styling with current theme and no titles"""
        try:
            if clear_plot and hasattr(self, 'ax') and self.ax:
                self.plot_manager.clear_and_optimize(self.ax)
            
            # Apply no-title styling using the plot manager
            if hasattr(self, 'ax') and self.ax and hasattr(self, 'fig'):
                apply_no_title_styling(self.fig, self.ax, xlabel, ylabel, self.theme_manager)
                self.plot_manager.finalize_plot(self.fig, self.ax)
            
            theme = self.theme_manager.get_current_theme()
            return theme.get('bg_color', 'white'), theme.get('text_color', 'black'), theme.get('grid_color', 'gray')
            
        except Exception as e:
            if hasattr(self, 'logger') and self.logger:
                self.logger.error(f"Error standardizing plot styling: {e}")
            else:
                print(f"Error standardizing plot styling: {e}")
            return 'white', 'black', 'gray'

    def get_current_spectrum(self):
        """
        Get the current spectrum data (wavelength and flux arrays)
        
        Returns:
            tuple: (wavelength, flux) numpy arrays, or (None, None) if no spectrum loaded
            
        Behavior:
        1. After loading: Returns original flux spectrum only
        2. After preprocessing: Returns flux version (display_flux or reconstructed from flat)
        3. Original spectrum is NOT available after preprocessing (replaced)
        """
        try:
            # Priority 1: If we have processed spectrum, return the flux version (not original)
            if hasattr(self, 'processed_spectrum') and self.processed_spectrum:
                log_wave = self.processed_spectrum.get('log_wave')
                
                # Use display_flux if available (best quality reconstructed flux)
                if 'display_flux' in self.processed_spectrum:
                    return log_wave.copy(), self.processed_spectrum['display_flux'].copy()
                
                # Fallback: reconstruct flux from flat_flux and continuum
                elif ('flat_flux' in self.processed_spectrum and 
                      'continuum' in self.processed_spectrum):
                    flat_flux = self.processed_spectrum['flat_flux']
                    continuum = self.processed_spectrum['continuum']
                    # Reconstruct: (flat + 1) * continuum
                    reconstructed_flux = (flat_flux + 1.0) * continuum
                    return log_wave.copy(), reconstructed_flux.copy()
                
                # Last resort: use log_flux if available
                elif 'log_flux' in self.processed_spectrum:
                    return log_wave.copy(), self.processed_spectrum['log_flux'].copy()
            
            # Priority 2: If no processed spectrum, use original (only available before preprocessing)
            if hasattr(self, 'original_wave') and hasattr(self, 'original_flux'):
                if self.original_wave is not None and self.original_flux is not None:
                    return self.original_wave.copy(), self.original_flux.copy()
            
            # If no spectrum data available
            return None, None
            
        except Exception as e:
            if hasattr(self, 'logger') and self.logger:
                self.logger.error(f"Error getting current spectrum: {e}")
            return None, None

    def has_spectrum_loaded(self):
        """
        Check if a spectrum is currently loaded
        
        Returns:
            bool: True if spectrum is loaded, False otherwise
            
        Behavior:
        - After loading (before preprocessing): Checks for original_wave/flux
        - After preprocessing: Checks for processed_spectrum
        - This method returns True if ANY spectrum data is available
        """
        # Check for processed spectrum (after preprocessing)
        if hasattr(self, 'processed_spectrum') and self.processed_spectrum is not None:
            # Verify it has the required keys
            if ('log_wave' in self.processed_spectrum and 
                self.processed_spectrum['log_wave'] is not None):
                return True
        
        # Check for original spectrum (before preprocessing)
        if (hasattr(self, 'original_wave') and self.original_wave is not None and
            hasattr(self, 'original_flux') and self.original_flux is not None):
            return True
        
        # No spectrum data available
        return False
    
    def reset_gui_to_initial_state(self):
        """
        Reset the GUI to its initial state (like when first opened)
        
        This method provides the functionality for the Reset button, clearing all
        data, analysis results, and plots while preserving user settings.
        """
        try:
            if self.logger:
                self.logger.info("🔄 Reset button clicked - starting GUI reset to initial state")
            
            # Use the spectrum reset manager for comprehensive reset
            if hasattr(self, 'spectrum_reset_manager'):
                self.spectrum_reset_manager.reset_gui_to_initial_state()
            else:
                # Fallback if reset manager not available
                self._fallback_reset_to_initial()
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error during GUI reset: {e}")
            else:
                print(f"Error during GUI reset: {e}")
    
    def _fallback_reset_to_initial(self):
        """Fallback reset method if spectrum reset manager is not available"""
        try:
            if self.logger:
                self.logger.warning("⚠️ Using fallback reset method")
            
            # Clear plots
            if hasattr(self, 'ax') and self.ax:
                self.ax.clear()
                if hasattr(self, 'canvas') and self.canvas:
                    self.canvas.draw()
            
            # Reset basic state
            self.snid_results = None
            self.processed_spectrum = None
            
            # Reset file status
            if hasattr(self, 'file_status_label'):
                self.file_status_label.configure(
                    text="No spectrum loaded",
                    fg=self.theme_manager.get_color('text_secondary')
                )
            
            # Reset state and update buttons
            if hasattr(self, 'state_manager'):
                self.state_manager.set_state('initial')
            
            self.update_button_states()
            
            if self.logger:
                self.logger.info("✅ Basic GUI reset completed (fallback method)")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error in fallback reset: {e}")
    
    def _ensure_initial_button_states(self):
        """Ensure segmented control buttons are in the correct initial state"""
        try:
            # Ensure both Flux and Flat are OFF on startup
            if hasattr(self, 'view_style') and self.view_style:
                # Do nothing if already blank; otherwise clear selection
                if self.view_style.get() != "":
                    self.view_style.set("")
                    if self.logger:
                        self.logger.debug("🔄 Cleared initial view_style selection; both buttons OFF")
                
                # Update segmented control buttons
                if hasattr(self, '_update_segmented_control_buttons'):
                    self._update_segmented_control_buttons()
                    if self.logger:
                        self.logger.debug("✅ Segmented control buttons refreshed for no-selection state")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error ensuring initial button states: {e}")
    
    def _setup_enhanced_macos_button_coordination(self):
        """Setup enhanced macOS button coordination for better color association"""
        try:
            if self.logger:
                self.logger.debug("🍎 Setting up enhanced macOS button coordination")
            
            # Store reference for macOS-specific handling
            self._macos_button_coordination_active = True
            
            # Schedule periodic color maintenance once the workflow system is initialized
            def schedule_color_maintenance():
                try:
                    if hasattr(self, 'workflow_integrator') and self.workflow_integrator:
                        # Trigger enhanced macOS color maintenance
                        if hasattr(self.workflow_integrator, '_schedule_macos_color_maintenance'):
                            self.workflow_integrator._schedule_macos_color_maintenance()
                            if self.logger:
                                self.logger.debug("✅ macOS color maintenance scheduled")
                    else:
                        # Retry later if workflow not ready
                        self.master.after(1000, schedule_color_maintenance)
                except Exception as e:
                    if self.logger:
                        self.logger.debug(f"macOS color maintenance scheduling failed: {e}")
            
            # Schedule the color maintenance setup
            self.master.after(2000, schedule_color_maintenance)
            
            # Add enhanced button update callback for macOS
            def enhanced_macos_button_update():
                try:
                    # Ensure button colors are correct after any state changes
                    if hasattr(self, 'workflow_integrator') and self.workflow_integrator:
                        if hasattr(self.workflow_integrator, '_verify_macos_button_colors'):
                            self.workflow_integrator._verify_macos_button_colors()
                except Exception as e:
                    if self.logger:
                        self.logger.debug(f"Enhanced macOS button update failed: {e}")
            
            # Store the callback for potential cleanup
            self._macos_button_update_callback = enhanced_macos_button_update
            
            # Apply global macOS window optimizations for better button responsiveness
            try:
                from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
                
                # Apply additional window-level optimizations
                self.master.option_add('*Button.highlightThickness', '0')
                self.master.option_add('*Button.borderWidth', '1')
                
                if self.logger:
                    self.logger.debug("✅ macOS window-level button optimizations applied")
                    
            except Exception as optimization_error:
                if self.logger:
                    self.logger.debug(f"macOS window optimizations failed: {optimization_error}")
            
            if self.logger:
                self.logger.debug("🍎 Enhanced macOS button coordination setup complete")
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error setting up macOS button coordination: {e}")

    def __del__(self):
        """Destructor to clean up matplotlib figures and prevent hanging"""
        try:
            self.cleanup_matplotlib()
        except:
            pass
    
    def cleanup_matplotlib(self):
        """Clean up matplotlib figures to prevent terminal hanging"""
        try:
            # Clean up toolbar first to prevent widget accumulation
            if hasattr(self, 'toolbar') and self.toolbar:
                try:
                    if self.toolbar.winfo_exists():
                        self.toolbar.destroy()
                    if hasattr(self, 'logger') and self.logger:
                        self.logger.debug("🧹 Toolbar destroyed during cleanup")
                except Exception as e:
                    if hasattr(self, 'logger') and self.logger:
                        self.logger.debug(f"Warning cleaning up toolbar: {e}")
                finally:
                    self.toolbar = None
            
            # Clean up canvas
            if hasattr(self, 'canvas') and self.canvas:
                try:
                    canvas_widget = self.canvas.get_tk_widget()
                    if canvas_widget and canvas_widget.winfo_exists():
                        canvas_widget.destroy()
                    if hasattr(self, 'logger') and self.logger:
                        self.logger.debug("🧹 Canvas destroyed during cleanup")
                except Exception as e:
                    if hasattr(self, 'logger') and self.logger:
                        self.logger.debug(f"Warning cleaning up canvas: {e}")
                finally:
                    self.canvas = None
            
            import matplotlib.pyplot as plt
            # Close all matplotlib figures
            plt.close('all')
            
            # Clear any matplotlib backends
            try:
                import matplotlib
                matplotlib.pyplot.ioff()  # Turn off interactive mode
            except:
                pass
                
            if hasattr(self, 'logger') and self.logger:
                self.logger.debug("🧹 Matplotlib cleanup completed")
        except Exception as e:
            if hasattr(self, 'logger') and self.logger:
                self.logger.warning(f"Warning during matplotlib cleanup: {e}")
    
    def on_closing(self):
        """Handle GUI closing event properly"""
        try:
            if hasattr(self, 'logger') and self.logger:
                self.logger.info("🔄 GUI closing initiated...")
            
            # Clean up matplotlib first
            self.cleanup_matplotlib()
            
            # Clean up theme manager dialogs
            if hasattr(self, 'theme_manager') and self.theme_manager:
                self.theme_manager.active_dialogs.clear()
            
            # Destroy the window
            self.master.quit()
            self.master.destroy()
            
        except Exception as e:
            # Force exit if cleanup fails
            try:
                self.master.quit()
                self.master.destroy()
            except:
                pass


def main(verbosity_args=None):
    """
    Main function to run the Modern SNID SAGE GUI
    
    Args:
        verbosity_args: Optional argparse.Namespace with verbosity settings
    """
    
    # Configure logging for GUI with proper defaults
    logger = None
    try:
        from snid_sage.shared.utils.logging import configure_from_args
        from snid_sage.shared.utils.logging import get_logger, VerbosityLevel
        
        if verbosity_args:
            # Use provided verbosity arguments
            configure_from_args(verbosity_args, gui_mode=True)
        else:
            # Auto-configure for GUI mode with QUIET as default (not NORMAL)
            from snid_sage.shared.utils.logging import configure_logging
            configure_logging(verbosity=VerbosityLevel.QUIET, gui_mode=True)
            
        logger = get_logger('gui.main')
        logger.info("SNID SAGE GUI starting with configured verbosity...")
        
    except ImportError:
        # Fallback if logging system not available
        logger = None
    
    # Log startup or fallback to print if verbose
    if logger:
        logger.info("Starting SNID SAGE GUI initialization...")
    elif verbosity_args and (getattr(verbosity_args, 'verbose', False) or getattr(verbosity_args, 'debug', False)):
        print("🚀 Starting SNID SAGE GUI initialization...")
    
    # Set DPI awareness before creating any windows (Windows-specific fix)
    if logger:
        logger.debug("Setting up DPI awareness...")
    setup_dpi_awareness()
    
    # Create the root window
    if logger:
        logger.debug("Creating root window...")
    elif verbosity_args and getattr(verbosity_args, 'debug', False):
        print("🏗️ Creating root window...")
    
    root = tk.Tk()
    
    # Additional Windows-specific display improvements
    setup_window_properties(root)
    
    # Create the application
    if logger:
        logger.debug("Creating application instance...")
    elif verbosity_args and getattr(verbosity_args, 'debug', False):
        print("🏗️ Creating application instance...")
    
    app = None
    try:
        app = ModernSNIDSageGUI(root)
        if logger:
            logger.info("GUI created successfully!")
        elif verbosity_args and (getattr(verbosity_args, 'verbose', False) or getattr(verbosity_args, 'debug', False)):
            print("✅ GUI created successfully!")
    except Exception as e:
        error_msg = f"Error creating GUI: {e}"
        if logger:
            logger.error(error_msg)
            logger.debug("GUI creation traceback:", exc_info=True)
        else:
            print(f"❌ {error_msg}")
            if verbosity_args and getattr(verbosity_args, 'debug', False):
                import traceback
                traceback.print_exc()
        
        if app:
            try:
                app.master.destroy()
            except:
                pass
        root.destroy()
        return 1
    
    # Setup cleanup and exit handling
    cleanup_and_exit = setup_cleanup_and_exit(root, app)
    
    try:
        if logger:
            logger.info("Starting GUI main loop...")
            logger.debug("GUI is ready and should be visible")
        elif verbosity_args and (getattr(verbosity_args, 'verbose', False) or getattr(verbosity_args, 'debug', False)):
            print("🚀 Starting GUI main loop...")
            print("📋 GUI is ready! If you see this message, the window should be visible.")
            print("💡 If the window is not visible, try Alt+Tab to find it or check your taskbar.")
        
        # Start the main loop
        root.mainloop()
        
        if logger:
            logger.debug("Main loop ended normally")
        elif verbosity_args and getattr(verbosity_args, 'debug', False):
            print("📋 Main loop ended normally")
        
    except KeyboardInterrupt:
        if logger:
            logger.info("Keyboard interrupt received")
        else:
            print("\n🔴 Keyboard interrupt received")
        cleanup_and_exit()
    except Exception as e:
        error_msg = f"GUI error: {e}"
        if logger:
            logger.error(error_msg)
            logger.debug("GUI error traceback:", exc_info=True)
        else:
            print(f"❌ {error_msg}")
            if verbosity_args and getattr(verbosity_args, 'debug', False):
                import traceback
                traceback.print_exc()
        cleanup_and_exit()
        return 1
    
    if logger:
        logger.info("SNID SAGE GUI session ended")
    elif verbosity_args and (getattr(verbosity_args, 'verbose', False) or getattr(verbosity_args, 'debug', False)):
        print("✅ SNID SAGE GUI session ended")
    
    return 0


if __name__ == "__main__":
    import sys
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
