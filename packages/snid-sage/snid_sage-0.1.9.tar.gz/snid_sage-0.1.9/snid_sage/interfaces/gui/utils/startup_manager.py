"""
SNID SAGE - Startup Manager
============================

Handles GUI startup, initialization, and deferred component loading.
Moved from sage_gui.py to reduce main file complexity.

Part of the SNID SAGE GUI restructuring - Utils Module
"""

import tkinter as tk
from tkinter import messagebox
import platform
import sys
import os

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.startup')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.startup')


class StartupManager:
    """Manages GUI startup and initialization"""
    
    def __init__(self, gui_instance):
        """Initialize startup manager with reference to main GUI"""
        self.gui = gui_instance
    
    def show_startup_message(self):
        """Show a startup message to confirm GUI is working"""
        # Startup message disabled - GUI launches silently
        return
    
    def init_deferred_components(self):
        """Initialize components that require the GUI to be fully constructed"""
        try:
            _LOGGER.info("🔧 Initializing deferred components...")
            
            # Initialize controllers first
            from snid_sage.interfaces.gui.controllers.app_controller import AppController
            from snid_sage.interfaces.gui.controllers.file_controller import FileController
            from snid_sage.interfaces.gui.features.preprocessing.preprocessing_controller import PreprocessingController
            from snid_sage.interfaces.gui.features.analysis.analysis_controller import AnalysisController
            from snid_sage.interfaces.gui.features.analysis.line_detection import LineDetectionController
            from snid_sage.interfaces.gui.features.results.results_manager import ResultsManager
            
            self.gui.app_controller = AppController(self.gui)
            self.gui.file_controller = FileController(self.gui)
            self.gui.preprocessing_controller = PreprocessingController(self.gui)
            self.gui.analysis_controller = AnalysisController(self.gui)
            self.gui.line_detection_controller = LineDetectionController(self.gui)
            self.gui.results_manager = ResultsManager(self.gui)
            
            # Initialize LLM integration if available
            try:
                from snid_sage.interfaces.gui.features.results.llm_integration import LLMIntegration
                self.gui.llm_integration = LLMIntegration(self.gui)
                _LOGGER.info("✅ LLM integration initialized")
            except Exception as e:
                _LOGGER.warning(f"⚠️ LLM integration not available: {e}")
                self.gui.llm_integration = None
            
            # Initialize games integration if available
            try:
                from snid_sage.snid import games
                if hasattr(games, 'show_game_menu'):
                    from snid_sage.interfaces.gui.features.analysis.games_integration import GamesIntegration
                    self.gui.games_integration = GamesIntegration(self.gui)
                    _LOGGER.info("✅ Games integration initialized")
                else:
                    self.gui.games_integration = None
            except Exception as e:
                _LOGGER.warning(f"⚠️ Games integration not available: {e}")
                self.gui.games_integration = None
            
            # Template manager functionality is now handled by config manager in main GUI
            
            # Initialize plot components (these will be created when needed)
            self.gui.spectrum_plotter = None  # Will be initialized when matplotlib is ready
            self.gui.summary_plotter = None
            self.gui.interactive_tools = None
            self.gui.analysis_plotter = None
            
            # Initialize dialog components
            self.gui.mask_manager_dialog = None  # Created when needed
            
            _LOGGER.info("✅ All deferred components initialized successfully")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error initializing deferred components: {e}")
            import traceback
            traceback.print_exc()
    
    def init_plot_components(self):
        """Initialize plot controller and matplotlib components"""
        try:
            # Initialize plot controller
            from snid_sage.interfaces.gui.controllers.plot_controller import PlotController
            self.gui.plot_controller = PlotController(self.gui)
            
            # Initialize matplotlib plot
            self.gui.plot_controller.init_matplotlib_plot()
            
            # Setup plot event handlers
            if hasattr(self.gui, 'event_handlers'):
                self.gui.event_handlers.handle_plot_events()
            
            _LOGGER.info("✅ Plot components initialized")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error initializing plot components: {e}")
            import traceback
            traceback.print_exc()


def setup_dpi_awareness():
    """Setup DPI awareness for all platforms (Cross-platform)"""
    try:
        # Try to use the cross-platform window manager
        try:
            from .cross_platform_window import CrossPlatformWindowManager
            success = CrossPlatformWindowManager.setup_dpi_awareness()
            if success:
                _LOGGER.info("✅ Cross-platform DPI awareness set")
                return
        except ImportError:
            _LOGGER.debug("Cross-platform window manager not available, using legacy approach")
        
        # Fallback to legacy Windows-only approach
        import platform
        if platform.system() == "Windows":
            import ctypes
            from ctypes import windll
            
            # Try the newer DPI awareness API first (Windows 10 version 1703+)
            try:
                windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor V2 DPI awareness
                _LOGGER.info("✅ DPI awareness set to per-monitor V2")
                return
            except:
                try:
                    windll.shcore.SetProcessDpiAwareness(1)  # Per-monitor V1 DPI awareness
                    _LOGGER.info("✅ DPI awareness set to per-monitor V1")
                    return
                except:
                    # Last resort: basic system DPI awareness (Windows Vista+)
                    try:
                        windll.user32.SetProcessDPIAware()  # System DPI awareness
                        _LOGGER.info("✅ Basic DPI awareness set")
                    except:
                        _LOGGER.warning("⚠️ Could not set DPI awareness")
        else:
            _LOGGER.debug("⚠️ DPI awareness setup skipped (not Windows or libraries not available)")
    except Exception as e:
        _LOGGER.warning(f"⚠️ DPI awareness setup failed: {e}")


def setup_window_properties(master):
    """Setup window properties for optimal display"""
    try:
        _LOGGER.info("✅ Windows-specific display properties set")
        
        # Configure window properties
        master.state('normal')
        master.attributes('-topmost', False) 
        master.overrideredirect(False)
        
        _LOGGER.info("✅ Window properties configured")
        
    except Exception as e:
        _LOGGER.warning(f"⚠️ Error setting window properties: {e}")


def setup_cleanup_and_exit(root, app):
    """Setup cleanup and exit handling"""
    
    def cleanup_and_exit():
        """Clean up and exit"""
        if app and hasattr(app, 'event_handlers'):
            app.event_handlers.handle_window_close()
        else:
            # Fallback cleanup
            _LOGGER.info("🛑 Shutting down SNID SAGE GUI...")
            try:
                if app:
                    if hasattr(app, 'snid_runner') and app.snid_runner:
                        try:
                            app.snid_runner.terminate_processes()
                        except:
                            pass
                    
                    if hasattr(app, 'fig'):
                        try:
                            import matplotlib.pyplot as plt
                            plt.close(app.fig)
                            plt.close('all')
                        except:
                            pass
                
                root.quit()
                root.destroy()
                _LOGGER.info("✅ GUI cleanup completed")
            except Exception as e:
                _LOGGER.warning(f"⚠️ Error during cleanup: {e}")
    
    # Set up proper exit handling
    root.protocol("WM_DELETE_WINDOW", cleanup_and_exit)
    
    # Handle Ctrl+C and other interrupts
    import signal
    def signal_handler(sig, frame):
        _LOGGER.info("\n🔴 Interrupt received - shutting down...")
        cleanup_and_exit()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    return cleanup_and_exit


def create_main_gui(app_instance):
    """Create and initialize the main GUI components"""
    try:
        # Initialize startup manager
        startup_manager = StartupManager(app_instance)
        
        # Initialize deferred components
        startup_manager.init_deferred_components()
        
        # Initialize plot components
        startup_manager.init_plot_components()
        
        _LOGGER.info("✅ Main GUI components created successfully")
        return True
        
    except Exception as e:
        _LOGGER.error(f"❌ Error creating main GUI: {e}")
        import traceback
        traceback.print_exc()
        return False


def destroy_gui_safely(root, app=None):
    """Safely destroy the GUI with proper cleanup"""
    try:
        _LOGGER.info("🛑 Starting safe GUI destruction...")
        
        # Stop any running processes
        if app and hasattr(app, 'snid_runner') and app.snid_runner:
            try:
                app.snid_runner.terminate_processes()
                _LOGGER.info("✅ SNID processes terminated")
            except Exception as e:
                _LOGGER.warning(f"⚠️ Error terminating processes: {e}")
        
        # Close matplotlib figures
        if app and hasattr(app, 'fig'):
            try:
                import matplotlib.pyplot as plt
                plt.close(app.fig)
                plt.close('all')
                _LOGGER.info("✅ Matplotlib figures closed")
            except Exception as e:
                _LOGGER.warning(f"⚠️ Error closing plots: {e}")
        
        # Cleanup other resources
        if app:
            # Template manager cleanup no longer needed (handled by config manager)
                    
            if hasattr(app, 'llm_integration'):
                try:
                    app.llm_integration = None
                except:
                    pass
        
        # Destroy the root window
        try:
            root.quit()
            root.destroy()
            _LOGGER.info("✅ GUI destroyed safely")
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error destroying GUI: {e}")
            
    except Exception as e:
        _LOGGER.error(f"❌ Error in safe GUI destruction: {e}")
        import traceback
        traceback.print_exc()


def setup_controllers(app_instance):
    """Setup all controllers for the application"""
    try:
        _LOGGER.info("🔧 Setting up controllers...")
        
        # Initialize core controllers
        from snid_sage.interfaces.gui.controllers.app_controller import AppController
        from snid_sage.interfaces.gui.controllers.file_controller import FileController
        
        app_instance.app_controller = AppController(app_instance)
        app_instance.file_controller = FileController(app_instance)
        
        # Initialize feature controllers
        from snid_sage.interfaces.gui.features.preprocessing.preprocessing_controller import PreprocessingController
        from snid_sage.interfaces.gui.features.analysis.analysis_controller import AnalysisController
        
        app_instance.preprocessing_controller = PreprocessingController(app_instance)
        app_instance.analysis_controller = AnalysisController(app_instance)
        
        # Initialize optional controllers
        try:
            from snid_sage.interfaces.gui.features.analysis.line_detection import LineDetectionController
            app_instance.line_detection_controller = LineDetectionController(app_instance)
        except ImportError:
            app_instance.line_detection_controller = None
            
        try:
            from snid_sage.interfaces.gui.features.results.results_manager import ResultsManager
            app_instance.results_manager = ResultsManager(app_instance)
        except ImportError:
            app_instance.results_manager = None
        
        _LOGGER.info("✅ Controllers setup completed")
        return True
        
    except Exception as e:
        _LOGGER.error(f"❌ Error setting up controllers: {e}")
        import traceback
        traceback.print_exc()
        return False


def bind_controller_events(app_instance):
    """Bind events between controllers"""
    try:
        _LOGGER.info("🔧 Binding controller events...")
        
        # Bind file controller events
        if hasattr(app_instance, 'file_controller') and app_instance.file_controller:
            # File loading events
            app_instance.file_controller.on_file_loaded = getattr(app_instance, 'on_file_loaded', lambda *args: None)
            app_instance.file_controller.on_file_error = getattr(app_instance, 'on_file_error', lambda *args: None)
        
        # Bind analysis controller events 
        if hasattr(app_instance, 'analysis_controller') and app_instance.analysis_controller:
            # Analysis events
            app_instance.analysis_controller.on_analysis_complete = getattr(app_instance, 'on_analysis_complete', lambda *args: None)
            app_instance.analysis_controller.on_analysis_error = getattr(app_instance, 'on_analysis_error', lambda *args: None)
            app_instance.analysis_controller.on_analysis_progress = getattr(app_instance, 'on_analysis_progress', lambda *args: None)
        
        # Bind preprocessing controller events
        if hasattr(app_instance, 'preprocessing_controller') and app_instance.preprocessing_controller:
            # Preprocessing events
            app_instance.preprocessing_controller.on_preprocessing_complete = getattr(app_instance, 'on_preprocessing_complete', lambda *args: None)
            app_instance.preprocessing_controller.on_preprocessing_error = getattr(app_instance, 'on_preprocessing_error', lambda *args: None)
        
        _LOGGER.info("✅ Controller events bound successfully")
        return True
        
    except Exception as e:
        _LOGGER.error(f"❌ Error binding controller events: {e}")
        import traceback
        traceback.print_exc()
        return False 
