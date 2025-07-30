"""
Event Handlers for SNID SAGE GUI
================================

This module contains event handling utilities for the SNID SAGE GUI,
including keyboard shortcuts, plot interactions, and window events.
"""

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.events')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.events')

class EventHandlers:
    """Collection of event handler utilities"""
    
    def __init__(self, gui_instance):
        """Initialize event handlers with reference to GUI instance"""
        self.gui = gui_instance
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for the GUI"""
        try:
            # File operations
            self.gui.master.bind("<Control-o>", lambda event: self.gui.browse_file())
            
            # Configuration
            self.gui.master.bind("<Control-Shift-O>", lambda event: self.gui.configure_options())
            
            # Analysis operations
            if hasattr(self.gui, 'run_snid_analysis_only'):
                self.gui.master.bind("<F5>", lambda event: self.gui.run_snid_analysis_only())
            if hasattr(self.gui, 'open_preprocessing_dialog'):
                self.gui.master.bind("<F6>", lambda event: self.gui.open_preprocessing_dialog())
            
            # Combined workflow - Quick preprocessing + analysis
            if hasattr(self.gui, 'run_quick_preprocessing_and_analysis'):
                # Use cross-platform shortcut system
                from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
                shortcuts = CrossPlatformWindowManager.get_keyboard_shortcuts()
                if 'quick_workflow' in shortcuts:
                    self.gui.master.bind(f"<{shortcuts['quick_workflow']}>", 
                                       lambda event: self.gui.run_quick_preprocessing_and_analysis())
            
            # Theme toggle
            # Dark mode toggle removed - light mode only
            
            # Template navigation - setup immediately if plot_controller exists, otherwise defer
            self.setup_template_navigation_shortcuts()
            
            # View switching
            if hasattr(self.gui, 'switch_mode'):
                self.gui.master.bind("<space>", lambda event: self.gui.switch_mode())
            
            # Reset functionality - OS aware
            if hasattr(self.gui, 'reset_gui_to_initial_state'):
                import platform
                if platform.system() == "Darwin":  # macOS
                    self.gui.master.bind("<Command-r>", lambda event: self.gui.reset_gui_to_initial_state())
                    self.gui.master.bind("<Command-R>", lambda event: self.gui.reset_gui_to_initial_state())
                else:  # Windows/Linux
                    self.gui.master.bind("<Control-r>", lambda event: self.gui.reset_gui_to_initial_state())
                    self.gui.master.bind("<Control-R>", lambda event: self.gui.reset_gui_to_initial_state())
            
            _LOGGER.info("✅ Keyboard shortcuts setup complete")
            _LOGGER.info("   📄 Ctrl+O: Open file")
            _LOGGER.info("   ⚙️ Ctrl+Shift+O: SNID Configuration")
            _LOGGER.info("   ▶️ F5: Run analysis only")
            _LOGGER.info("   🚀 Ctrl+Enter (Cmd+Enter on Mac): Quick preprocessing + analysis (combined workflow)")
            _LOGGER.info("   🔧 F6: Preprocessing")
            _LOGGER.info("   🔄 Ctrl+R (Cmd+R on Mac): Reset to initial state")
            _LOGGER.info("   🔄 Space: Switch mode (if available)")
            _LOGGER.info("   📊 ← → : Navigate templates (when results available)")
            _LOGGER.info("   🔄 ↑ ↓ : Cycle views (Flux/Flat)")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error setting up keyboard shortcuts: {e}")
    
    def setup_template_navigation_shortcuts(self):
        """Setup template navigation shortcuts (can be called multiple times)"""
        try:
            if hasattr(self.gui, 'plot_controller') and self.gui.plot_controller:
                # Ensure the main window can receive key events
                self.gui.master.focus_set()
                
                # Use only bind_all with proper state checking to avoid duplicate calls
                # This ensures navigation works regardless of focus and prevents multiple triggers
                self.gui.master.bind_all("<Left>", lambda event: self._handle_template_navigation(event, 'prev'))
                self.gui.master.bind_all("<Right>", lambda event: self._handle_template_navigation(event, 'next'))
                
                # Add up/down arrows for view mode cycling
                self.gui.master.bind_all("<Up>", lambda event: self._handle_view_cycling(event, 'up'))
                self.gui.master.bind_all("<Down>", lambda event: self._handle_view_cycling(event, 'down'))
                
                _LOGGER.info("✅ Template navigation shortcuts setup complete")
                _LOGGER.info("   ← → : Navigate templates (Previous/Next)")
                _LOGGER.info("   ↑ ↓ : Cycle views (Flux/Flat)")
                return True
            else:
                # plot_controller not available yet - will be setup later
                _LOGGER.debug("Plot controller not available yet - template navigation will be setup later")
                return False
                
        except Exception as e:
            _LOGGER.error(f"❌ Error setting up template navigation shortcuts: {e}")
            return False
    
    def _handle_template_navigation(self, event, direction):
        """Handle template navigation with focus and state checks"""
        try:
            # Only handle if we have plot_controller and SNID results
            if (hasattr(self.gui, 'plot_controller') and self.gui.plot_controller and
                hasattr(self.gui, 'snid_results') and self.gui.snid_results and
                hasattr(self.gui.snid_results, 'best_matches') and self.gui.snid_results.best_matches):
                
                # Preserve the current view mode before navigation
                current_view = None
                if hasattr(self.gui, 'view_style') and self.gui.view_style:
                    current_view = self.gui.view_style.get()
                    _LOGGER.info(f"🔒 Preserving view mode: {current_view}")
                
                # Set a flag to prevent default view changes during navigation
                if hasattr(self.gui.plot_controller, 'preserve_view_mode'):
                    self.gui.plot_controller.preserve_view_mode = current_view
                
                # Perform template navigation
                if direction == 'prev':
                    self.gui.plot_controller.prev_template()
                elif direction == 'next':
                    self.gui.plot_controller.next_template()
                
                # Ensure the view mode is maintained immediately after navigation
                if current_view and hasattr(self.gui, 'view_style') and self.gui.view_style:
                    # Set the view mode immediately to prevent flicker
                    self.gui.view_style.set(current_view)
                    _LOGGER.info(f"🔄 Maintained view mode: {current_view}")
                    
                    # Update segmented control buttons to reflect maintained view
                    if hasattr(self.gui, '_update_segmented_control_buttons'):
                        self.gui._update_segmented_control_buttons()
                        _LOGGER.debug(f"✅ Updated segmented control buttons after navigation")
                
                # Force theme reapplication after keyboard navigation
                # This ensures grid and background are properly styled in dark mode
                if hasattr(self.gui.plot_controller, '_apply_plot_theme'):
                    try:
                        self.gui.plot_controller._apply_plot_theme()
                        _LOGGER.debug(f"✅ Theme reapplied after keyboard navigation")
                    except Exception as theme_error:
                        _LOGGER.warning(f"⚠️ Warning reapplying theme: {theme_error}")
                
                # Clear the preservation flag
                if hasattr(self.gui.plot_controller, 'preserve_view_mode'):
                    self.gui.plot_controller.preserve_view_mode = None
                    
        except Exception as e:
            _LOGGER.error(f"❌ Error handling template navigation: {e}")
    
    def _handle_view_cycling(self, event, direction):
        """Handle view cycling between Flux and Flat with up/down arrows"""
        try:
            # Only handle if we have the view_style variable and plot_controller
            if (hasattr(self.gui, 'view_style') and self.gui.view_style and
                hasattr(self.gui, 'plot_controller') and self.gui.plot_controller):
                
                # Define the view cycle order
                view_modes = ["Flux", "Flat"]
                current_view = self.gui.view_style.get()
                
                try:
                    current_index = view_modes.index(current_view)
                except ValueError:
                    # If current view is not in the list, default to Flux
                    current_index = 0
                    current_view = "Flux"
                
                # Cycle through views
                if direction == 'up':
                    # Go to previous view (cycle backwards)
                    new_index = (current_index - 1) % len(view_modes)
                elif direction == 'down':
                    # Go to next view (cycle forwards)
                    new_index = (current_index + 1) % len(view_modes)
                else:
                    return
                
                new_view = view_modes[new_index]
                
                # Update the view style variable
                self.gui.view_style.set(new_view)
                
                # Trigger the view change through the plot controller
                self.gui.plot_controller._on_view_style_change()
                
                _LOGGER.info(f"🔄 View cycled: {current_view} → {new_view}")
                
        except Exception as e:
            _LOGGER.error(f"❌ Error handling view cycling: {e}")
    
    def _on_click(self, event):
        """Handle mouse clicks on the plot"""
        try:
            if not hasattr(self.gui, 'ax') or event.inaxes != self.gui.ax:
                return
            
            # Handle masking if active
            if hasattr(self.gui, 'is_masking_active') and self.gui.is_masking_active and event.button == 1:  # Left click
                _LOGGER.info(f"Click at wavelength: {event.xdata:.2f}")
                
                # Add click handling logic here
                if hasattr(self.gui, 'mask_manager_dialog') and self.gui.mask_manager_dialog:
                    # Delegate to mask manager
                    self.gui.mask_manager_dialog.handle_plot_click(event.xdata)
                
        except Exception as e:
            _LOGGER.error(f"❌ Error handling plot click: {e}")
    
    def _on_view_style_change(self, *args):
        """Handle changes to the view style segmented control"""
        try:
            if hasattr(self.gui, 'plot_controller'):
                self.gui.plot_controller._on_view_style_change(*args)
            else:
                # Fallback handling
                style = self.gui.view_style.get()
                if style == "Flux":
                    self.gui.current_view = 'flux'
                elif style == "Flat":
                    self.gui.current_view = 'flat'
                    
        except Exception as e:
            _LOGGER.error(f"Error handling view style change: {e}")
    
    def toggle_additional_tools(self, event=None):
        """Toggle additional tools - delegate to app controller"""
        if hasattr(self.gui, 'app_controller'):
            self.gui.app_controller.toggle_additional_tools(event)
        else:
            _LOGGER.warning("⚠️ App controller not available for toggle_additional_tools")
    
    def start_games_menu(self):
        """Start games menu - delegate to app controller"""
        if hasattr(self.gui, 'app_controller'):
            self.gui.app_controller.start_games_menu()
        else:
            messagebox.showinfo("Games", "Games not available yet.")
    
    def handle_window_close(self):
        """Handle window close event with proper cleanup"""
        try:
            _LOGGER.info("🛑 Shutting down SNID SAGE GUI...")
            
            # Cleanup app components
            if hasattr(self.gui, 'snid_runner') and self.gui.snid_runner:
                try:
                    self.gui.snid_runner.terminate_processes()
                    _LOGGER.info("✅ SNID processes terminated")
                except:
                    _LOGGER.warning("⚠️ Could not terminate SNID processes")
            
            # Close matplotlib figures properly
            if hasattr(self.gui, 'fig'):
                try:
                    plt.close(self.gui.fig)
                    plt.close('all')  # Close any remaining figures
                    _LOGGER.info("✅ Matplotlib figures closed")
                except:
                    _LOGGER.warning("⚠️ Could not close matplotlib figures")
            
            # Cleanup preprocessing dialog if open
            if hasattr(self.gui, 'preprocessing_dialog') and self.gui.preprocessing_dialog:
                try:
                    self.gui.preprocessing_dialog.destroy()
                    _LOGGER.info("✅ Preprocessing dialog closed")
                except:
                    pass
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Destroy the root window
            self.gui.master.quit()  # Exit mainloop
            self.gui.master.destroy()  # Destroy window
            _LOGGER.info("✅ GUI cleanup completed")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error during cleanup: {e}")
    
    def handle_plot_events(self):
        """Setup plot event handlers"""
        try:
            if hasattr(self.gui, 'canvas') and self.gui.canvas:
                # Connect mouse click events
                self.gui.canvas.mpl_connect('button_press_event', self._on_click)
                
                # Connect other plot events as needed
                # self.gui.canvas.mpl_connect('scroll_event', self._on_scroll)
                # self.gui.canvas.mpl_connect('key_press_event', self._on_key_press)
                
            _LOGGER.info("✅ Plot event handlers connected")
                
        except Exception as e:
            _LOGGER.error(f"❌ Error setting up plot event handlers: {e}")
    
    def schedule_keep_alive(self):
        """Schedule keep alive - delegate to app controller"""
        if hasattr(self.gui, 'app_controller'):
            self.gui.app_controller.schedule_keep_alive()
        else:
            # Basic fallback
            self.gui.master.after(5000, self.schedule_keep_alive)


class WindowEventHandlers:
    """Specialized event handlers for window management"""
    
    @staticmethod
    def center_window_safely(gui_instance):
        """Center window safely - delegate to app controller"""
        if hasattr(gui_instance, 'app_controller'):
            gui_instance.app_controller.center_window_safely()
        else:
            # Fallback for early initialization
            try:
                gui_instance.master.update_idletasks()
                width = gui_instance.master.winfo_width()
                height = gui_instance.master.winfo_height()
                screen_width = gui_instance.master.winfo_screenwidth()
                screen_height = gui_instance.master.winfo_screenheight()
                x = (screen_width // 2) - (width // 2)
                y = (screen_height // 2) - (height // 2)
                gui_instance.master.geometry(f"{width}x{height}+{x}+{y}")
            except Exception as e:
                _LOGGER.warning(f"Warning: Could not center window: {e}")
    
    @staticmethod
    def setup_window_properties(master):
        """Setup window properties for proper display"""
        try:
            # Handle DPI scaling on Windows
            import platform
            if platform.system() == "Windows":
                # Get system DPI awareness
                try:
                    import ctypes
                    from ctypes import windll
                    
                    # Set DPI awareness to prevent blurry text
                    windll.shcore.SetProcessDpiAwareness(1)
                    
                    # Get the actual DPI scale factor
                    dpi = windll.user32.GetDpiForWindow(master.winfo_id())
                    scale_factor = dpi / 96.0  # 96 is standard DPI
                    
                    # Adjust tkinter scaling
                    if scale_factor > 1.25:  # If high DPI scaling
                        master.tk.call('tk', 'scaling', 1.0)  # Reset to normal
                    else:
                        master.tk.call('tk', 'scaling', 1.0)
                        
                except Exception:
                    # Fallback: Just set normal scaling
                    master.tk.call('tk', 'scaling', 1.0)
            else:
                # For non-Windows systems
                master.tk.call('tk', 'scaling', 1.0)
                
        except Exception:
            pass
        
        # Set reasonable window size (not too large)
        master.geometry("1200x800")  # Smaller, more manageable size
        master.configure(bg='#f5f7fa')
        
        # Configure font settings for better readability (Cross-platform)
        try:
            # Get platform-appropriate default font
            try:
                from .cross_platform_window import CrossPlatformWindowManager
                default_font = CrossPlatformWindowManager.get_platform_font('default')
            except ImportError:
                # Fallback to Windows font
                default_font = ('Segoe UI', 12, 'normal')
            
            # Set default font for better text rendering
            master.option_add('*Font', default_font)
            
            # Configure specific font settings for common widgets
            master.option_add('*TLabel*Font', (default_font[0], default_font[1]))
            master.option_add('*TButton*Font', (default_font[0], default_font[1]))
            master.option_add('*TEntry*Font', (default_font[0], default_font[1]))
        except:
            pass
        
        # Set window properties for proper display
        master.resizable(True, True)
        master.minsize(900, 600)  # Reasonable minimum size
        master.maxsize(1920, 1080)  # Prevent excessive size
        
        # Ensure window state is normal
        master.state('normal')
        master.attributes('-topmost', False)
        master.wm_attributes('-disabled', False)
        master.overrideredirect(False) 
