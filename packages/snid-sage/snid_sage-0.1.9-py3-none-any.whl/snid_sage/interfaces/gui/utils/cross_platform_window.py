"""
Cross-Platform Window Manager for SNID SAGE
==========================================

Provides platform-agnostic window management functionality to ensure
consistent behavior across Windows, macOS, and Linux systems.

This module abstracts OS-specific window operations including:
- DPI awareness setup
- Fullscreen management  
- Window theming
- Icon management
- Font selection
- Keyboard shortcuts
"""

import os
import sys
import platform
import tkinter as tk
from pathlib import Path
from typing import Dict, Optional, Tuple, Any

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.cross_platform')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.cross_platform')


class CrossPlatformWindowManager:
    """
    Cross-platform window management utilities for consistent behavior
    across Windows, macOS, and Linux systems.
    """
    
    # Platform constants
    WINDOWS = "Windows"
    MACOS = "Darwin" 
    LINUX = "Linux"
    
    # Font mappings for each platform
    PLATFORM_FONTS = {
        WINDOWS: {
            'default': ('Segoe UI', 12, 'normal'),
            'title': ('Segoe UI', 16, 'bold'),
            'small': ('Segoe UI', 10, 'normal'),
            'code': ('Consolas', 11, 'normal')
        },
        MACOS: {
            'default': ('SF Pro Display', 12, 'normal'),
            'title': ('SF Pro Display', 16, 'bold'),
            'small': ('SF Pro Display', 10, 'normal'),
            'code': ('SF Mono', 11, 'normal')
        },
        LINUX: {
            'default': ('Ubuntu', 12, 'normal'),
            'title': ('Ubuntu', 16, 'bold'),
            'small': ('Ubuntu', 10, 'normal'),
            'code': ('Ubuntu Mono', 11, 'normal')
        }
    }
    
    # Keyboard shortcuts for each platform
    PLATFORM_SHORTCUTS = {
        WINDOWS: {
            'fullscreen': 'F11',
            'quit': 'Ctrl+Q',
            'preferences': 'Ctrl+P',
            'close': 'Alt+F4',
            'minimize': 'Ctrl+M',
            'copy': 'Ctrl+C',
            'paste': 'Ctrl+V',
            'select_all': 'Ctrl+A',
            'quick_workflow': 'Control-Return'
        },
        MACOS: {
            'fullscreen': 'Cmd+Ctrl+F',
            'quit': 'Cmd+Q', 
            'preferences': 'Cmd+Comma',
            'close': 'Cmd+W',
            'minimize': 'Cmd+M',
            'copy': 'Cmd+C',
            'paste': 'Cmd+V',
            'select_all': 'Cmd+A',
            'quick_workflow': 'Command-Return'
        },
        LINUX: {
            'fullscreen': 'F11',
            'quit': 'Ctrl+Q',
            'preferences': 'Ctrl+P',
            'close': 'Ctrl+W',
            'minimize': 'Ctrl+M',
            'copy': 'Ctrl+C',
            'paste': 'Ctrl+V',
            'select_all': 'Ctrl+A',
            'quick_workflow': 'Control-Return'
        }
    }
    
    @classmethod
    def get_platform(cls) -> str:
        """Get the current platform name"""
        return platform.system()
    
    @classmethod
    def is_windows(cls) -> bool:
        """Check if running on Windows"""
        return cls.get_platform() == cls.WINDOWS
    
    @classmethod
    def is_macos(cls) -> bool:
        """Check if running on macOS"""
        return cls.get_platform() == cls.MACOS
    
    @classmethod
    def is_linux(cls) -> bool:
        """Check if running on Linux"""
        return cls.get_platform() == cls.LINUX
    
    @classmethod
    def setup_dpi_awareness(cls) -> bool:
        """
        Setup DPI awareness for high-resolution displays
        Returns True if successful, False otherwise
        """
        try:
            if cls.is_windows():
                return cls._setup_windows_dpi()
            elif cls.is_macos():
                return cls._setup_macos_dpi()
            elif cls.is_linux():
                return cls._setup_linux_dpi()
            else:
                _LOGGER.warning(f"Unknown platform: {cls.get_platform()}")
                return False
        except Exception as e:
            _LOGGER.warning(f"DPI awareness setup failed: {e}")
            return False
    
    @classmethod
    def _setup_windows_dpi(cls) -> bool:
        """Setup Windows-specific DPI awareness"""
        try:
            import ctypes
            from ctypes import windll
            
            # Try newest API first (Windows 10 1703+)
            try:
                windll.shcore.SetProcessDpiAwarenessContext(-4)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
                _LOGGER.debug("✅ Windows DPI awareness: Per-monitor V2")
                return True
            except Exception:
                pass
            
            # Fallback to older API (Windows 8.1+)
            try:
                windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
                _LOGGER.debug("✅ Windows DPI awareness: Per-monitor V1")
                return True
            except Exception:
                pass
            
            # Last resort (Windows Vista+)
            try:
                windll.user32.SetProcessDPIAware()
                _LOGGER.debug("✅ Windows DPI awareness: Basic")
                return True
            except Exception:
                pass
            
            _LOGGER.warning("⚠️ Could not set Windows DPI awareness")
            return False
            
        except ImportError:
            _LOGGER.warning("⚠️ Windows DPI libraries not available")
            return False
    
    @classmethod
    def _setup_macos_dpi(cls) -> bool:
        """Setup macOS-specific display handling"""
        try:
            # macOS handles retina displays automatically through the system
            # We just need to ensure proper scaling
            _LOGGER.debug("✅ macOS display handling: Automatic retina support")
            return True
        except Exception as e:
            _LOGGER.warning(f"⚠️ macOS display setup failed: {e}")
            return False
    
    @classmethod
    def _setup_linux_dpi(cls) -> bool:
        """Setup Linux-specific display handling"""
        try:
            # Linux DPI handling varies by desktop environment
            # Set environment variables for better scaling
            scale_factor = os.environ.get('GDK_SCALE', '1')
            _LOGGER.debug(f"✅ Linux display handling: GDK_SCALE={scale_factor}")
            return True
        except Exception as e:
            _LOGGER.warning(f"⚠️ Linux display setup failed: {e}")
            return False
    
    @classmethod
    def setup_window_properties(cls, window: tk.Tk) -> None:
        """Setup cross-platform window properties"""
        try:
            # Basic window properties
            window.resizable(True, True)
            window.minsize(800, 600)
            
            # Platform-specific window setup
            if cls.is_windows():
                cls._setup_windows_window(window)
            elif cls.is_macos():
                cls._setup_macos_window(window)
            elif cls.is_linux():
                cls._setup_linux_window(window)
            
            _LOGGER.debug("✅ Window properties configured")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error setting up window properties: {e}")
    
    @classmethod
    def _setup_windows_window(cls, window: tk.Tk) -> None:
        """Setup Windows-specific window properties"""
        try:
            # Disable automatic DPI scaling for better control
            window.tk.call('tk', 'scaling', 1.0)
            window.wm_attributes('-alpha', 1.0)
            _LOGGER.debug("✅ Windows window properties set")
        except Exception as e:
            _LOGGER.warning(f"⚠️ Windows window setup failed: {e}")
    
    @classmethod
    def _setup_macos_window(cls, window: tk.Tk) -> None:
        """Setup macOS-specific window properties and event handling"""
        try:
            # macOS-specific window attributes
            window.createcommand('tk::mac::ShowPreferences', lambda: None)
            
            # Enable proper mouse event handling for Mac
            cls._setup_macos_mouse_events(window)
            
            # Enable trackpad gesture support
            cls._setup_macos_trackpad_support(window)
            
            _LOGGER.debug("✅ macOS window properties and event handling set")
        except Exception as e:
            _LOGGER.warning(f"⚠️ macOS window setup failed: {e}")
    
    @classmethod
    def _setup_macos_mouse_events(cls, window: tk.Tk) -> None:
        """Setup Mac-specific mouse event handling for better click detection"""
        try:
            # Configure proper button mappings for Mac
            # Mac trackpads and mice have different button mappings
            
            # Ensure proper right-click detection on Mac
            # Button-2 is right-click on Mac (not Button-3 like on Linux/Windows)
            def mac_right_click_handler(event):
                # Convert Mac right-click to standard right-click event
                original_button = event.button
                event.button = 3  # Convert to standard right-click
                
                # Re-trigger the event with the corrected button number
                # This ensures other handlers receive the standardized event
                if hasattr(event.widget, 'event_generate'):
                    try:
                        event.widget.event_generate("<Button-3>", 
                                                   x=event.x, y=event.y,
                                                   rootx=event.x_root, rooty=event.y_root)
                    except:
                        pass  # Fallback to just modifying the event
                
                return event
            
            # Enhanced global right-click binding for all widget types
            widget_classes = [
                "Button", "Checkbutton", "Radiobutton", "Label", "Frame",
                "Listbox", "Text", "Entry", "Canvas", "Toplevel", "Menu",
                "Menubutton", "Scale", "Spinbox", "Scrollbar"
            ]
            
            for widget_class in widget_classes:
                # Bind Mac-specific Button-2 events to all widget classes
                window.bind_class(widget_class, "<Button-2>", mac_right_click_handler, add="+")
                
                # Also ensure Control+Click is handled as right-click on Mac
                window.bind_class(widget_class, "<Control-Button-1>", mac_right_click_handler, add="+")
            
            _LOGGER.debug("✅ Enhanced Mac mouse event handling configured")
        except Exception as e:
            _LOGGER.warning(f"⚠️ Mac mouse event setup failed: {e}")
    
    @classmethod 
    def _setup_macos_trackpad_support(cls, window: tk.Tk) -> None:
        """Setup Mac trackpad gesture and sensitivity support"""
        try:
            # Improve trackpad sensitivity and gesture detection
            
            # Configure trackpad click sensitivity
            window.option_add('*Button.highlightThickness', '0')
            window.option_add('*Button.borderWidth', '0')
            
            # Enable proper focus handling for trackpad clicks
            def improve_focus_handling(event):
                widget = event.widget
                if hasattr(widget, 'focus_set'):
                    widget.focus_set()
                return "break"  # Prevent default handling
            
            # Bind focus improvement to common click events
            window.bind_class("Button", "<Button-1>", improve_focus_handling, add="+")
            window.bind_class("Checkbutton", "<Button-1>", improve_focus_handling, add="+")
            window.bind_class("Radiobutton", "<Button-1>", improve_focus_handling, add="+")
            
            # Improve trackpad scroll sensitivity
            def improve_scroll_handling(event):
                # Mac trackpad scroll events are often too sensitive
                # Scale down the delta for better control
                if hasattr(event, 'delta'):
                    event.delta = int(event.delta * 0.5)  # Reduce sensitivity
                return event
            
            window.bind_class("Canvas", "<MouseWheel>", improve_scroll_handling, add="+")
            window.bind_class("Text", "<MouseWheel>", improve_scroll_handling, add="+")
            window.bind_class("Listbox", "<MouseWheel>", improve_scroll_handling, add="+")
            
            _LOGGER.debug("✅ Mac trackpad support configured")
        except Exception as e:
            _LOGGER.warning(f"⚠️ Mac trackpad setup failed: {e}")
    
    @classmethod
    def _setup_linux_window(cls, window: tk.Tk) -> None:
        """Setup Linux-specific window properties"""
        try:
            # Linux window manager hints
            window.wm_attributes('-type', 'normal')
            _LOGGER.debug("✅ Linux window properties set")
        except Exception as e:
            _LOGGER.warning(f"⚠️ Linux window setup failed: {e}")
    
    @classmethod
    def setup_fullscreen(cls, window: tk.Tk, enable: bool = True) -> bool:
        """
        Setup fullscreen mode in a cross-platform way
        Returns True if successful
        """
        try:
            if cls.is_macos():
                # macOS has special fullscreen behavior
                if enable:
                    window.attributes('-fullscreen', True)
                    window.attributes('-zoomed', True)  # Also maximize
                else:
                    window.attributes('-fullscreen', False)
                    window.attributes('-zoomed', False)
            else:
                # Windows and Linux standard approach
                window.attributes('-fullscreen', enable)
            
            _LOGGER.debug(f"✅ Fullscreen {'enabled' if enable else 'disabled'}")
            return True
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Fullscreen setup failed: {e}")
            return False
    
    @classmethod
    def toggle_fullscreen(cls, window: tk.Tk) -> bool:
        """Toggle fullscreen mode"""
        try:
            current_state = window.attributes('-fullscreen')
            return cls.setup_fullscreen(window, not current_state)
        except Exception as e:
            _LOGGER.warning(f"⚠️ Fullscreen toggle failed: {e}")
            return False
    
    @classmethod
    def setup_window_theme(cls, window: tk.Tk, dark_mode: bool = False) -> None:
        """Setup platform-specific window theming - light mode only"""
        try:
            if cls.is_windows():
                cls._setup_windows_theme(window)
            elif cls.is_macos():
                cls._setup_macos_theme(window)
            elif cls.is_linux():
                cls._setup_linux_theme(window)
                
            _LOGGER.debug(f"✅ Window theme configured (light mode)")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Window theme setup failed: {e}")
    
    @classmethod
    def _setup_windows_theme(cls, window: tk.Tk) -> None:
        """Setup Windows-specific theming - light mode"""
        try:
            import ctypes
            from ctypes import windll
            
            # Windows 10+ light mode title bar
            window_id = windll.user32.GetParent(window.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                window_id, 
                20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
                ctypes.byref(ctypes.c_int(0)),  # Always light mode (0)
                ctypes.sizeof(ctypes.c_int)
            )
            _LOGGER.debug("✅ Windows title bar theme set to light mode")
            
        except Exception as e:
            _LOGGER.debug(f"Windows theme setup failed (not critical): {e}")
    
    @classmethod
    def _setup_macos_theme(cls, window: tk.Tk) -> None:
        """Setup macOS-specific theming - light mode"""
        try:
            # macOS automatically handles system theme
            _LOGGER.debug("✅ macOS theme handled by system")
        except Exception as e:
            _LOGGER.debug(f"macOS theme setup failed (not critical): {e}")
    
    @classmethod
    def _setup_linux_theme(cls, window: tk.Tk) -> None:
        """Setup Linux-specific theming - light mode"""
        try:
            # Linux theming depends on desktop environment
            _LOGGER.debug("✅ Linux theme handled by desktop environment")
        except Exception as e:
            _LOGGER.debug(f"Linux theme setup failed (not critical): {e}")
    
    @classmethod
    def get_platform_icon_path(cls, icon_name: str, icons_dir: str) -> Optional[str]:
        """
        Get platform-appropriate icon path (PNG only)
        """
        icon_path = os.path.join(icons_dir, f"{icon_name}.png")
        if os.path.exists(icon_path):
            return icon_path
        return None

    @classmethod
    def set_window_icon(cls, window: tk.Tk, icon_name: str = 'icon') -> bool:
        """Set window icon using images/icon.png if available (high quality PNG only)"""
        try:
            from snid_sage.shared.utils.simple_template_finder import find_images_directory
            icons_dir = find_images_directory()
            if not icons_dir:
                return False
            icon_path = cls.get_platform_icon_path(icon_name, str(icons_dir))
            if icon_path:
                from PIL import Image, ImageTk
                img = Image.open(icon_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                icon = ImageTk.PhotoImage(img)
                window.iconphoto(True, icon)
                window._snid_icon_set = True
                return True
            return False
        except Exception:
            return False
    
    @classmethod
    def get_platform_font(cls, font_type: str = 'default') -> Tuple[str, int, str]:
        """
        Get appropriate font for current platform
        
        Args:
            font_type: Type of font ('default', 'title', 'small', 'code')
            
        Returns:
            Tuple of (font_family, size, style)
        """
        platform_name = cls.get_platform()
        fonts = cls.PLATFORM_FONTS.get(platform_name, cls.PLATFORM_FONTS[cls.LINUX])
        return fonts.get(font_type, fonts['default'])
    
    @classmethod
    def get_keyboard_shortcuts(cls) -> Dict[str, str]:
        """Get platform-appropriate keyboard shortcuts"""
        platform_name = cls.get_platform()
        return cls.PLATFORM_SHORTCUTS.get(platform_name, cls.PLATFORM_SHORTCUTS[cls.LINUX])
    
    @classmethod
    def center_window(cls, window: tk.Tk, width: Optional[int] = None, height: Optional[int] = None) -> None:
        """Center window on screen with proper error handling"""
        try:
            window.update_idletasks()
            
            # Get window dimensions
            if width is None:
                width = window.winfo_width()
            if height is None:
                height = window.winfo_height()
            
            # Get screen dimensions
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            
            # Calculate center position
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            
            # Ensure window stays on screen
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))
            
            window.geometry(f"{width}x{height}+{x}+{y}")
            _LOGGER.debug(f"✅ Window centered at {x},{y} (size: {width}x{height})")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Could not center window: {e}")
    
    @classmethod
    def bind_platform_shortcuts(cls, window: tk.Tk, callbacks: Dict[str, Any]) -> None:
        """Bind platform-appropriate keyboard shortcuts"""
        try:
            shortcuts = cls.get_keyboard_shortcuts()
            
            for action, callback in callbacks.items():
                if action in shortcuts and callback:
                    window.bind(f"<{shortcuts[action]}>", callback)
            
            _LOGGER.debug("✅ Platform shortcuts bound")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Shortcut binding failed: {e}")
    
    @classmethod
    def setup_mac_event_bindings(cls, widget, right_click_callback=None, click_callback=None) -> bool:
        """
        Setup Mac-specific event bindings for a widget to fix click detection issues
        
        Args:
            widget: The tkinter widget to bind events to
            right_click_callback: Callback for right-click events
            click_callback: Callback for regular click events
            
        Returns:
            True if successful, False otherwise
        """
        if not cls.is_macos():
            return False
            
        try:
            # Handle right-click events properly on Mac
            if right_click_callback:
                def mac_right_click(event):
                    # Mac uses Button-2 for right-click, convert to standard event
                    event.button = 3  # Convert to standard right-click button
                    try:
                        return right_click_callback(event)
                    except Exception as e:
                        _LOGGER.debug(f"Right-click callback error: {e}")
                        return None
                
                # Comprehensive right-click binding for Mac
                widget.bind("<Button-2>", mac_right_click, add="+")  # Trackpad/Magic Mouse right-click
                widget.bind("<Button-3>", right_click_callback, add="+")  # External mouse right-click
                widget.bind("<Control-Button-1>", mac_right_click, add="+")  # Control+click = right-click on Mac
                
                # Also handle context menu events
                widget.bind("<Button-2>", lambda e: widget.tk.call('::tk::mac::contextualMenuBind', widget, e.x_root, e.y_root) if hasattr(widget.tk, 'call') else None, add="+")
            
            # Handle regular click events with improved sensitivity
            if click_callback:
                def improved_click(event):
                    # Ensure widget gets focus to improve responsiveness
                    if hasattr(widget, 'focus_set'):
                        try:
                            widget.focus_set()
                        except:
                            pass
                    
                    # Add visual feedback for better user experience
                    cls._add_visual_click_feedback(widget)
                    
                    try:
                        return click_callback(event)
                    except Exception as e:
                        _LOGGER.debug(f"Click callback error: {e}")
                        return None
                
                widget.bind("<Button-1>", improved_click, add="+")
            
            # Add trackpad-specific improvements
            cls._add_trackpad_improvements(widget)
            
            _LOGGER.debug(f"✅ Enhanced Mac event bindings set for {widget.__class__.__name__}")
            return True
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Mac event binding failed: {e}")
            return False
    
    @classmethod
    def _add_trackpad_improvements(cls, widget) -> None:
        """Add trackpad-specific improvements to a widget"""
        try:
            # Improve trackpad click detection
            def enhance_click_response(event):
                # Add visual feedback for trackpad clicks
                if hasattr(widget, 'configure'):
                    # Brief highlight to show click was registered
                    original_bg = widget.cget('bg') if 'bg' in widget.keys() else None
                    if original_bg:
                        widget.configure(bg='lightblue')
                        widget.after(50, lambda: widget.configure(bg=original_bg))
                return "continue"  # Allow other handlers to run
            
            # Add enhanced click feedback for trackpad users
            widget.bind("<Button-1>", enhance_click_response, add="+")
            
            # Improve trackpad scroll handling if applicable
            if hasattr(widget, 'yview'):  # Scrollable widget
                def better_scroll(event):
                    # Reduce scroll sensitivity for trackpad
                    if hasattr(event, 'delta'):
                        # Scale down trackpad scroll speed
                        delta = int(event.delta * 0.3)
                        widget.yview_scroll(-1 * (delta // 120), "units")
                        return "break"  # Prevent default handling
                    return "continue"
                
                widget.bind("<MouseWheel>", better_scroll, add="+")
            
        except Exception as e:
            _LOGGER.debug(f"Trackpad improvements failed (non-critical): {e}")
    
    @classmethod 
    def get_config_directory(cls, app_name: str = 'SNID_SAGE') -> str:
        """Get platform-appropriate configuration directory"""
        try:
            if cls.is_windows():
                config_dir = os.path.join(os.environ.get('APPDATA', ''), app_name)
            elif cls.is_macos():
                config_dir = os.path.expanduser(f'~/Library/Application Support/{app_name}')
            else:  # Linux
                config_dir = os.path.expanduser(f'~/.config/{app_name.lower()}')
            
            # Create directory if it doesn't exist
            os.makedirs(config_dir, exist_ok=True)
            _LOGGER.debug(f"✅ Config directory: {config_dir}")
            return config_dir
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Failed to get config directory: {e}")
            # Fallback to current directory
            return os.getcwd()
    
    @classmethod
    def handle_window_close(cls, window: tk.Tk, cleanup_callback: Optional[Any] = None) -> None:
        """Handle window close event with proper cleanup"""
        try:
            _LOGGER.info("🛑 Shutting down application...")
            
            if cleanup_callback:
                cleanup_callback()
            
            # Close any matplotlib figures
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass
            
            # Destroy window
            window.quit()
            window.destroy()
            
            _LOGGER.info("✅ Application shutdown complete")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error during window close: {e}")
            # Force exit if normal cleanup fails
            sys.exit(0)

    @classmethod
    def integrate_mac_improvements_globally(cls, root_window: tk.Tk) -> bool:
        """
        Integrate Mac improvements globally across the entire GUI application
        
        Args:
            root_window: The main tkinter window
            
        Returns:
            True if improvements were applied, False otherwise
        """
        if not cls.is_macos():
            return False
            
        try:
            # Apply global Mac improvements
            cls._apply_global_mac_bindings(root_window)
            cls._setup_global_trackpad_improvements(root_window)
            cls._improve_mac_widget_responsiveness(root_window)
            
            _LOGGER.info("✅ Global Mac improvements integrated successfully")
            return True
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Global Mac integration failed: {e}")
            return False
    
    @classmethod
    def _apply_global_mac_bindings(cls, root_window: tk.Tk) -> None:
        """Apply Mac-specific event bindings globally"""
        try:
            # Enhanced global right-click handler for Mac
            def global_mac_right_click(event):
                try:
                    # Store original button for debugging
                    original_button = event.button
                    
                    # Convert Mac Button-2 to standard Button-3
                    event.button = 3  
                    
                    # Re-trigger the event with corrected button
                    widget = event.widget
                    if hasattr(widget, 'event_generate'):
                        try:
                            # Create new standardized right-click event
                            widget.event_generate("<Button-3>", 
                                                x=event.x, y=event.y, 
                                                rootx=event.x_root, rooty=event.y_root)
                        except Exception as regen_error:
                            _LOGGER.debug(f"Event regeneration failed: {regen_error}")
                            
                    return "break"  # Prevent default handling
                    
                except Exception as e:
                    _LOGGER.debug(f"Global right-click handler error: {e}")
                    return "continue"  # Allow other handlers to try
            
            # Enhanced global click responsiveness improver
            def global_mac_click_improver(event):
                try:
                    widget = event.widget
                    
                    # Ensure focus for better responsiveness
                    if hasattr(widget, 'focus_set'):
                        try:
                            widget.focus_set()
                        except:
                            pass  # Some widgets can't receive focus
                            
                    # Add brief visual feedback (non-blocking)
                    try:
                        cls._add_visual_click_feedback(widget)
                    except:
                        pass  # Visual feedback is optional
                        
                    return "continue"  # Allow other handlers to process
                    
                except Exception as e:
                    _LOGGER.debug(f"Global click improver error: {e}")
                    return "continue"
            
            # Comprehensive Control+Click handling (Mac right-click alternative)
            def global_mac_control_click(event):
                try:
                    # Convert Control+Click to right-click on Mac
                    event.button = 3  
                    
                    widget = event.widget
                    if hasattr(widget, 'event_generate'):
                        try:
                            widget.event_generate("<Button-3>", 
                                                x=event.x, y=event.y, 
                                                rootx=event.x_root, rooty=event.y_root)
                        except:
                            pass
                            
                    return "break"
                    
                except Exception as e:
                    _LOGGER.debug(f"Control+click handler error: {e}")
                    return "continue"
            
            # Enhanced widget class list for comprehensive coverage
            widget_classes = [
                "Button", "Checkbutton", "Radiobutton", "Label", 
                "Canvas", "Frame", "Toplevel", "Text", "Listbox",
                "Entry", "Scale", "Spinbox", "Menubutton", "Menu",
                "Scrollbar", "PanedWindow", "LabelFrame"
            ]
            
            for widget_class in widget_classes:
                try:
                    # Multiple right-click binding strategies for Mac
                    root_window.bind_class(widget_class, "<Button-2>", global_mac_right_click, add="+")
                    root_window.bind_class(widget_class, "<Control-Button-1>", global_mac_control_click, add="+")
                    
                    # Improve general click responsiveness  
                    root_window.bind_class(widget_class, "<Button-1>", global_mac_click_improver, add="+")
                    
                except Exception as bind_error:
                    _LOGGER.debug(f"Failed to bind events to {widget_class}: {bind_error}")
                    continue  # Continue with other widget classes
            
            _LOGGER.debug("✅ Enhanced global Mac bindings applied")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Global Mac bindings failed: {e}")

    @classmethod
    def _setup_global_trackpad_improvements(cls, root_window: tk.Tk) -> None:
        """Setup global trackpad improvements"""
        try:
            # Enhanced global trackpad scroll handler
            def global_trackpad_scroll(event):
                try:
                    # Reduce trackpad scroll sensitivity globally
                    if hasattr(event, 'delta') and event.delta != 0:
                        # Scale down scroll speed for better control
                        scaled_delta = int(event.delta * 0.3)  # Reduced sensitivity
                        
                        # Find the appropriate scrollable parent
                        widget = event.widget
                        scrollable_widget = None
                        
                        # Check current widget first
                        if hasattr(widget, 'yview'):
                            scrollable_widget = widget
                        else:
                            # Search parent hierarchy for scrollable widget
                            current = widget
                            while current and current.master:
                                current = current.master
                                if hasattr(current, 'yview'):
                                    scrollable_widget = current
                                    break
                        
                        if scrollable_widget:
                            try:
                                scrollable_widget.yview_scroll(-1 * (scaled_delta // 120), "units")
                                return "break"  # Handled, prevent default
                            except:
                                pass  # Let default handling proceed
                                
                except Exception as e:
                    _LOGGER.debug(f"Trackpad scroll handler error: {e}")
                    
                return "continue"  # Allow default handling as fallback
            
            # Apply to scrollable and container widgets
            scrollable_classes = ["Text", "Listbox", "Canvas", "Frame", "Toplevel", "PanedWindow"]
            for widget_class in scrollable_classes:
                try:
                    root_window.bind_class(widget_class, "<MouseWheel>", global_trackpad_scroll, add="+")
                except Exception as e:
                    _LOGGER.debug(f"Failed to bind scroll events to {widget_class}: {e}")
                    continue
            
            _LOGGER.debug("✅ Enhanced global trackpad improvements applied")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Global trackpad improvements failed: {e}")

    @classmethod
    def _improve_mac_widget_responsiveness(cls, root_window: tk.Tk) -> None:
        """Improve overall widget responsiveness on Mac"""
        try:
            # Configure global options for better Mac performance
            try:
                root_window.option_add('*highlightThickness', '0')
                root_window.option_add('*Button.borderWidth', '1')
                root_window.option_add('*Button.relief', 'flat')
                root_window.option_add('*Button.highlightBackground', 'systemWindowBackgroundColor')
            except Exception as e:
                _LOGGER.debug(f"Option configuration failed: {e}")
            
            # Improve focus handling and keyboard navigation
            def improve_focus_chain(event):
                try:
                    widget = event.widget
                    # Ensure proper focus chain for keyboard navigation
                    if hasattr(widget, 'tk_focusNext'):
                        next_widget = widget.tk_focusNext()
                        if next_widget and hasattr(next_widget, 'focus_set'):
                            # Pre-configure next widget for faster focus switching
                            pass
                            
                except Exception as e:
                    _LOGGER.debug(f"Focus chain improvement error: {e}")
                    
                return "continue"
            
            try:
                root_window.bind_class("all", "<Tab>", improve_focus_chain, add="+")
            except Exception as e:
                _LOGGER.debug(f"Tab binding failed: {e}")
            
            _LOGGER.debug("✅ Enhanced Mac widget responsiveness applied")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Mac responsiveness improvements failed: {e}")
    
    @classmethod
    def _add_visual_click_feedback(cls, widget) -> None:
        """Add visual feedback for clicks to improve user experience on Mac"""
        try:
            if hasattr(widget, 'configure') and 'bg' in widget.keys():
                original_bg = widget.cget('bg')
                
                # Brief visual feedback
                def restore_color():
                    try:
                        widget.configure(bg=original_bg)
                    except:
                        pass
                
                try:
                    # Quick flash to show click was registered
                    widget.configure(bg='#e8f4fd')  # Light blue flash
                    widget.after(75, restore_color)
                except:
                    pass  # Ignore if widget doesn't support background color
                    
        except Exception as e:
            # Non-critical, don't log as error
            pass


# Convenience functions for backward compatibility
def setup_dpi_awareness() -> bool:
    """Convenience function for DPI setup"""
    return CrossPlatformWindowManager.setup_dpi_awareness()

def get_platform_font(font_type: str = 'default') -> Tuple[str, int, str]:
    """Convenience function for font selection"""
    return CrossPlatformWindowManager.get_platform_font(font_type)

def get_config_directory(app_name: str = 'SNID_SAGE') -> str:
    """Convenience function for config directory"""
    return CrossPlatformWindowManager.get_config_directory(app_name)

def center_window(window: tk.Tk, width: Optional[int] = None, height: Optional[int] = None) -> None:
    """Convenience function for window centering"""
    return CrossPlatformWindowManager.center_window(window, width, height) 
