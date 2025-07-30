"""
Window Event Handlers for SNID SAGE GUI

Specialized event handlers for window management including:
- Window centering and positioning
- DPI awareness setup
- Window properties configuration
- Display-related fixes

Extracted from sage_gui.py to improve maintainability.
"""

import tkinter as tk
import platform

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.window')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.window')

# Import the new cross-platform window manager
try:
    from .cross_platform_window import CrossPlatformWindowManager
    _CROSS_PLATFORM_AVAILABLE = True
except ImportError:
    _CROSS_PLATFORM_AVAILABLE = False
    _LOGGER.warning("Cross-platform window manager not available, falling back to legacy code")


class WindowEventHandlers:
    """Specialized event handlers for window management"""
    
    @staticmethod
    def center_window_safely(gui_instance):
        """Center window safely - with proper error handling (Cross-platform)"""
        try:
            # Check if window was already positioned by fast launcher
            if hasattr(gui_instance.master, '_fast_launcher_positioned'):
                _LOGGER.debug("Skipping window centering - already positioned by fast launcher")
                return
                
            if _CROSS_PLATFORM_AVAILABLE:
                # Use the new cross-platform manager
                CrossPlatformWindowManager.center_window(gui_instance.master)
            else:
                # Fallback to legacy code
                gui_instance.master.update_idletasks()
                
                # Get current window size
                width = gui_instance.master.winfo_width()
                height = gui_instance.master.winfo_height()
                
                # Get screen dimensions
                screen_width = gui_instance.master.winfo_screenwidth()
                screen_height = gui_instance.master.winfo_screenheight()
                
                # Calculate center position
                x = (screen_width // 2) - (width // 2)
                y = (screen_height // 2) - (height // 2)
                
                # Ensure window stays on screen
                x = max(0, min(x, screen_width - width))
                y = max(0, min(y, screen_height - height))
                
                # Set window position
                gui_instance.master.geometry(f"{width}x{height}+{x}+{y}")
                _LOGGER.debug(f"✅ Window centered at {x},{y} (size: {width}x{height})")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Could not center window: {e}")
    
    @staticmethod
    def setup_window_properties(master):
        """Setup window properties for proper display (Cross-platform)"""
        try:
            # Set initial window size and properties
            master.geometry("1200x800")  # Reasonable default size
            master.title("SNID SAGE v1.0.0 - Modern Interface")
            
            # Hide window initially to prevent flickering during setup
            master.withdraw()
            
            if _CROSS_PLATFORM_AVAILABLE:
                # Use the new cross-platform manager
                CrossPlatformWindowManager.setup_window_properties(master)
                # Note: Icon is set separately in sage_gui.py to avoid duplicate warnings
            else:
                # Fallback to legacy code
                master.minsize(800, 600)
                
                # Handle DPI scaling on Windows
                if platform.system() == "Windows":
                    try:
                        # Disable automatic DPI scaling for better control
                        master.tk.call('tk', 'scaling', 1.0)
                        
                        # Set window attributes for better rendering
                        master.wm_attributes('-alpha', 1.0)  # Ensure full opacity
                        
                        _LOGGER.debug("✅ Windows-specific display properties set")
                    except Exception as e:
                        _LOGGER.warning(f"⚠️ Could not set Windows display properties: {e}")
                
                # Set window icon if available
                try:
                    import os
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.dirname(os.path.dirname(current_dir))
                    icon_path = os.path.join(project_root, 'images', 'icon.ico')
                    if os.path.exists(icon_path):
                        master.iconbitmap(icon_path)
                        _LOGGER.debug("✅ Window icon set")
                except Exception as e:
                    _LOGGER.warning(f"⚠️ Could not set window icon: {e}")
            
            _LOGGER.debug("✅ Window properties configured")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error setting up window properties: {e}")
    
    @staticmethod
    def setup_dpi_awareness():
        """Setup DPI awareness before creating any windows (Cross-platform)"""
        try:
            if _CROSS_PLATFORM_AVAILABLE:
                # Use the new cross-platform manager
                return CrossPlatformWindowManager.setup_dpi_awareness()
            else:
                # Fallback to legacy Windows-only code
                if platform.system() == "Windows":
                    import ctypes
                    from ctypes import windll
                    
                    try:
                        # Try the newer DPI awareness API first (Windows 10 version 1703+)
                        windll.shcore.SetProcessDpiAwarenessContext(-4)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
                        _LOGGER.debug("✅ DPI awareness set to per-monitor V2")
                        return True
                    except Exception:
                        try:
                            # Fallback to older API (Windows 8.1+)
                            windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
                            _LOGGER.debug("✅ DPI awareness set to per-monitor V1")
                            return True
                        except Exception:
                            try:
                                # Last resort: basic system DPI awareness (Windows Vista+)
                                windll.user32.SetProcessDPIAware()
                                _LOGGER.debug("✅ Basic DPI awareness set")
                                return True
                            except Exception:
                                _LOGGER.warning("⚠️ Could not set DPI awareness")
                                return False
                else:
                    _LOGGER.debug("⚠️ DPI awareness setup skipped (not Windows)")
                    return True
                    
        except Exception as e:
            _LOGGER.warning(f"⚠️ DPI awareness setup failed: {e}")
            return False
    
    @staticmethod
    def handle_window_close(gui_instance):
        """Handle window close event with proper cleanup"""
        try:
            _LOGGER.info("🛑 Shutting down SNID SAGE GUI...")
            
            # Use event handlers if available
            if hasattr(gui_instance, 'event_handlers'):
                gui_instance.event_handlers.handle_window_close()
            else:
                # Fallback cleanup
                if hasattr(gui_instance, 'snid_runner') and gui_instance.snid_runner:
                    try:
                        gui_instance.snid_runner.terminate_processes()
                    except:
                        pass
                
                if hasattr(gui_instance, 'fig'):
                    try:
                        import matplotlib.pyplot as plt
                        plt.close(gui_instance.fig)
                        plt.close('all')
                    except:
                        pass
                
                gui_instance.master.quit()
                gui_instance.master.destroy()
                _LOGGER.info("✅ GUI cleanup completed")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error during window close handling: {e}")
    
    @staticmethod
    def configure_window_for_theme(master, is_dark_mode=False):
        """Configure window appearance - light mode only"""
        try:
            if _CROSS_PLATFORM_AVAILABLE:
                # Use the new cross-platform manager (always light mode)
                CrossPlatformWindowManager.setup_window_theme(master, False)
            else:
                # Fallback to legacy Windows-only code (light mode)
                if platform.system() == "Windows":
                    # Light mode configuration  
                    try:
                        import ctypes
                        from ctypes import windll
                        windll.dwmapi.DwmSetWindowAttribute(
                            ctypes.windll.user32.GetParent(master.winfo_id()), 
                            20, 
                            ctypes.byref(ctypes.c_int(0)),  # Always light mode
                            ctypes.sizeof(ctypes.c_int)
                        )
                        _LOGGER.debug("✅ Light mode title bar enabled")
                    except Exception as e:
                        _LOGGER.warning(f"⚠️ Could not set light mode title bar: {e}")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error configuring window theme: {e}") 
