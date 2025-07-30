#!/usr/bin/env python3
"""
SNID SAGE Fast GUI Launcher
===========================

Simplified fast launcher that shows a loading screen immediately while
loading heavy components in the background.

This is the single entry point for the SNID SAGE GUI that prioritizes
immediate window appearance followed by background loading.
"""

import sys
import os
import argparse
import time
import tkinter as tk
from tkinter import messagebox
import threading
from pathlib import Path

# Import dynamic version
try:
    from snid_sage import __version__
except ImportError:
    __version__ = "unknown"

# Suppress third-party library output unless in verbose/debug mode
def suppress_third_party_output():
    """Suppress console output from third-party libraries"""
    # Suppress pygame welcome message
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    
    # Suppress other common library output
    import warnings
    warnings.filterwarnings('ignore')

def parse_arguments():
    """Parse command line arguments for the GUI launcher"""
    parser = argparse.ArgumentParser(
        description="SNID SAGE GUI with Fast Startup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    snid-sage                    # Fast startup (default)
    snid-sage --verbose          # With loading progress
    snid-sage --debug            # Full debug output
    snid-sage --quiet            # Minimal output
    
Environment Variables:
    SNID_DEBUG=1        # Enable debug mode
    SNID_VERBOSE=1      # Enable verbose mode
        """
    )
    
    # Import logging configuration to add standard arguments
    try:
        from snid_sage.shared.utils.logging import add_logging_arguments
        add_logging_arguments(parser)
    except ImportError:
        # Fallback to basic arguments if logging system not available
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Enable verbose output')
        parser.add_argument('--debug', '-d', action='store_true',
                          help='Enable debug output')
        parser.add_argument('--quiet', '-q', action='store_true',
                          help='Quiet mode (errors/warnings only)')
        parser.add_argument('--silent', action='store_true',
                          help='Silent mode (critical errors only)')
    
    return parser.parse_args()

def setup_dpi_awareness():
    """Set up DPI awareness before creating any windows"""
    try:
        import platform
        if platform.system() == 'Windows':
            try:
                import ctypes
                # Try to set DPI awareness
                try:
                    # Windows 10 version 1703 and later
                    ctypes.windll.shcore.SetProcessDpiAwareness(1)
                except:
                    try:
                        # Windows Vista and later fallback
                        ctypes.windll.user32.SetProcessDPIAware()
                    except:
                        pass
            except:
                pass
    except:
        pass

class FastGUILauncher:
    """Fast GUI launcher that prioritizes immediate window appearance"""
    
    def __init__(self, args):
        self.args = args
        self.verbose = args.verbose or args.debug
        self.debug = args.debug
        self.root = None
        self.app = None
        self.logger = None
        
        # Track loading progress
        self.loading_complete = False
        self.background_loading_done = False
        
        # Progress bar tracking
        self.total_steps = 7  # Number of distinct loading phases we update for
        self.progress_index = 0  # Current completed step count
        
        # Version checking
        self.version_check_result = None
        
    def log(self, message):
        """Log message if verbose mode enabled"""
        if self.verbose:
            print(f"🚀 {message}")
    
    def show_loading_window(self):
        """Show loading window immediately with proper DPI setup"""
        self.log("Creating loading window...")
        start_time = time.time()
        
        # Create root window but keep it hidden initially
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window initially
        self.root.title(f"SNID SAGE v{__version__} - Loading...")
        
        # Configure window properties BEFORE showing
        self.root.configure(bg='#1e1e1e')  # Dark background first
        
        # Set proper window size with DPI awareness
        self.root.geometry("900x600")
        self.root.minsize(800, 550)
        
        # Create loading screen with better styling
        loading_frame = tk.Frame(self.root, bg='#1e1e1e')
        loading_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Skip logo; instead leave vertical space equivalent
        spacer_logo = tk.Frame(loading_frame, height=60, bg='#1e1e1e')
        spacer_logo.pack()
        
        # Use system fonts or fall back gracefully
        try:
            title_font = ('Segoe UI', 32, 'bold')
            subtitle_font = ('Segoe UI', 14)
            status_font = ('Segoe UI', 11)
            version_font = ('Segoe UI', 12)
            progress_font = ("Consolas", 12)
            tip_font = ('Segoe UI', 9)
        except:
            # Fallback to default system fonts if Segoe UI not available
            title_font = ('Arial', 32, 'bold')
            subtitle_font = ('Arial', 14)
            status_font = ('Arial', 11)
            version_font = ('Arial', 12)
            progress_font = ("Courier", 12)
            tip_font = ('Arial', 9)
        
        # Title, version, subtitle
        title_label = tk.Label(
            loading_frame,
            text="SNID-SAGE",
            font=title_font,
            fg='#ffffff',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(20, 10))

        version_label = tk.Label(
            loading_frame,
            text=f"v{__version__}",
            font=version_font,
            fg='#888888',
            bg='#1e1e1e'
        )
        version_label.pack(pady=(0, 5))

        subtitle_label = tk.Label(
            loading_frame,
            text="SuperNova IDentification – Spectral Analysis with Guided Expertise",
            font=subtitle_font,
            fg='#cccccc',
            bg='#1e1e1e'
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Loading status
        self.status_label = tk.Label(
            loading_frame,
            text="🚀 Initializing...",
            font=status_font,
            fg='#4CAF50',
            bg='#1e1e1e',
            anchor='center'
        )
        self.status_label.pack(pady=(20, 10))

        # Animated ASCII loading bar
        self._bar_length = 30
        self._bar_pos = 0
        self.progress_bar_label = tk.Label(
            loading_frame,
            text="░" * self._bar_length,
            font=progress_font,
            fg="#4CAF50",
            bg="#1e1e1e",
        )
        self.progress_bar_label.pack(pady=15)

        # Loading tip
        tip_label = tk.Label(
            loading_frame,
            text="🔬 Preparing spectrum analysis tools...",
            font=tip_font,
            fg='#888888',
            bg='#1e1e1e'
        )
        tip_label.pack(pady=(30, 0))
        
        # Calculate window position BEFORE showing
        self.root.update_idletasks()  # This calculates sizes without showing
        
        # Get screen dimensions and center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = 900
        window_height = 600
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Ensure window stays on screen
        x = max(0, min(x, screen_width - window_width))
        y = max(0, min(y, screen_height - window_height))
        
        # Set final position before showing
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # NOW show the window
        self.root.deiconify()  # Show the window
        self.root.update()  # Force update to ensure it's visible
        
        window_time = time.time() - start_time
        self.log(f"Loading window created in {window_time:.3f}s")
        
        # Set up window icon after the window is shown
        self.root.after(50, self._setup_window_icon_deferred)
        
        return self.root
    
    def _setup_window_icon_deferred(self):
        """Set up window icon after the window is already visible"""
        try:
            png_icon_path = Path(__file__).parent.parent.parent / "images" / "icon.png"
            if png_icon_path.exists():
                from PIL import Image, ImageTk
                img = Image.open(png_icon_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                icon = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, icon)
                self.log("Window icon set successfully")
            else:
                self.log("icon.png not found, using default window icon")
        except Exception as e:
            self.log(f"Could not set window icon: {e}")
    
    def update_progress(self, status, progress_text=None):
        """Update loading progress"""
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.config(text=status)
        
        # Advance progress bar
        if not self.loading_complete and hasattr(self, 'progress_bar_label'):
            self.progress_index = min(self.progress_index + 1, self.total_steps)
            filled_len = int(self._bar_length * self.progress_index / self.total_steps)
            filled = "▓" * filled_len
            empty = "░" * (self._bar_length - filled_len)
            self.progress_bar_label.config(text=filled + empty)

        if hasattr(self, 'root') and self.root:
            self.root.update_idletasks()
    
    def load_components_background(self):
        """Load heavy components in background thread"""
        try:
            self.log("Starting background component loading...")
            
            # Configure logging first
            self.update_progress("⚙️ Configuring logging...")
            try:
                from snid_sage.shared.utils.logging import configure_from_args
                from snid_sage.shared.utils.logging import get_logger
                
                configure_from_args(self.args, gui_mode=True)
                self.logger = get_logger('gui.launcher')
                self.log("Logging configured")
            except ImportError:
                self.log("Logging system not available (using fallback)")
            
            # Check for updates (async, won't block loading)
            self.update_progress("🔄 Checking for updates...")
            self.start_version_check()
            
            # Load matplotlib
            self.update_progress("📊 Loading matplotlib...")
            import matplotlib
            matplotlib.use('TkAgg')  # Set backend early
            self.log("Matplotlib loaded")
            
            # Load numpy
            self.update_progress("🔢 Loading numpy...")
            import numpy as np
            self.log("Numpy loaded")
            
            # Check dependencies
            self.update_progress("🔍 Checking dependencies...")
            deps_ok = self.check_dependencies_fast()
            if not deps_ok:
                error_msg = "Dependencies check failed"
                suggestion = "Try running: pip install -e . --force-reinstall"
                
                if self.logger:
                    self.logger.error(f"❌ {error_msg}")
                    self.logger.info(f"💡 {suggestion}")
                else:
                    self.log(f"❌ {error_msg}")
                    self.log(f"💡 {suggestion}")
                
                self.root.after(100, lambda: messagebox.showerror("Dependencies Error", 
                    f"{error_msg}\n\n{suggestion}"))
                return
            
            # Load SNID core components
            self.update_progress("🔬 Loading SNID engine...")
            from snid_sage.snid.snid import run_snid, preprocess_spectrum, run_snid_analysis
            self.log("SNID core loaded")
            
            # Now we can safely create the real GUI
            self.update_progress("🖥️ Initializing interface...")
            
            # Mark loading as complete; fill progress bar fully
            self.loading_complete = True
            if hasattr(self, 'progress_bar_label'):
                self.progress_bar_label.config(text="▓" * self._bar_length)
            
            # Schedule GUI creation on main thread
            self.root.after(100, self.create_real_gui)
            
        except Exception as e:
            # Handle errors gracefully
            error_msg = f"❌ Error loading components: {e}"
            self.log(error_msg)
            self.update_progress(error_msg)
            
            # Show error dialog
            self.root.after(100, lambda: messagebox.showerror("Loading Error", 
                f"Error loading SNID components:\n{e}\n\nTry restarting or check installation."))
    
    def start_version_check(self):
        """Start asynchronous version checking"""
        try:
            from snid_sage.shared.utils.version_checker import VersionChecker
            
            checker = VersionChecker(timeout=3.0)  # Quick timeout for startup
            checker.check_for_updates_async(self.on_version_check_complete)
            self.log("Version check started asynchronously")
            
        except ImportError:
            self.log("Version checker not available")
        except Exception as e:
            self.log(f"Error starting version check: {e}")
    
    def on_version_check_complete(self, version_info):
        """Called when version check completes"""
        try:
            self.version_check_result = version_info
            
            if version_info.get('update_available', False):
                current = version_info['current_version']
                latest = version_info['latest_version']
                self.log(f"Update available: {current} -> {latest}")
                
                # Schedule showing update dialog after GUI is ready
                if self.root:
                    self.root.after(2000, lambda: self.show_update_dialog(version_info))
            elif version_info.get('error'):
                self.log(f"Version check error: {version_info['error']}")
            else:
                self.log("Version is up to date")
                
        except Exception as e:
            self.log(f"Error processing version check result: {e}")
    
    def show_update_dialog(self, version_info):
        """Show update notification dialog"""
        try:
            from snid_sage.shared.utils.version_checker import format_update_message
            
            message = format_update_message(version_info)
            
            # Create a simple info dialog
            result = messagebox.askyesno(
                "Update Available",
                f"{message}\n\nWould you like to open the upgrade instructions?",
                icon='info'
            )
            
            if result:
                # Open documentation or PyPI page
                import webbrowser
                webbrowser.open("https://pypi.org/project/snid-sage/")
                
        except Exception as e:
            self.log(f"Error showing update dialog: {e}")
    
    def check_dependencies_fast(self):
        """Lightweight dependency check without heavy imports"""
        try:
            # Use importlib for faster checking
            import importlib.util
            
            modules_to_check = [
                'tkinter', 'matplotlib', 'numpy', 
                'snid_sage.snid.snid', 'snid_sage.interfaces.gui.sage_gui'
            ]
            
            missing_deps = []
            for module in modules_to_check:
                spec = importlib.util.find_spec(module)
                if spec is None:
                    missing_deps.append(module)
                    if self.logger:
                        self.logger.error(f"{module} not available")
            
            if missing_deps:
                if self.logger:
                    self.logger.error(f"Missing dependencies: {', '.join(missing_deps)}")
                return False
            else:
                if self.logger:
                    self.logger.info("All dependencies available")
                return True
                
        except Exception as e:
            self.log(f"Error checking dependencies: {e}")
            return False
    
    def create_real_gui(self):
        """Create the real GUI after components are loaded"""
        try:
            self.log("Creating real GUI interface...")
            
            # Import and create the real GUI
            from snid_sage.interfaces.gui.sage_gui import ModernSNIDSageGUI
            
            # Clear loading screen
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Important: Reconfigure the root window for the main GUI
            self.root.configure(bg='')  # Reset background
            
            # Set a flag to prevent the GUI from auto-centering (since we already positioned it)
            self.root._fast_launcher_positioned = True
            
            # Create the real application
            self.app = ModernSNIDSageGUI(self.root)
            
            # Update title
            self.root.title(f"SNID SAGE v{__version__} - Ready")
            
            # Ensure the window stays in place
            self.root.update_idletasks()
            
            self.log("GUI fully loaded and ready!")
            
        except Exception as e:
            self.log(f"Error creating real GUI: {e}")
            if self.logger:
                self.logger.error(f"Error creating real GUI: {e}")
            messagebox.showerror("GUI Error", f"Failed to create GUI:\n{e}")
    
    def run(self):
        """Run the fast GUI launcher"""
        start_time = time.time()
        
        # Step 1: Set up DPI awareness FIRST
        setup_dpi_awareness()
        self.log("DPI awareness configured")
        
        # Step 2: Show loading window immediately
        root = self.show_loading_window()
        
        # Performance check
        window_time = time.time() - start_time
        if window_time > 2.0:
            self.log(f"⚠️ Window appearance took {window_time:.3f}s (slower than expected)")
        elif window_time < 0.5:
            self.log(f"🚀 Window appeared in {window_time:.3f}s (excellent)")
        else:
            self.log(f"✅ Window appeared in {window_time:.3f}s (good)")
        
        # Step 3: Start background loading
        loading_thread = threading.Thread(target=self.load_components_background, daemon=True)
        loading_thread.start()
        
        total_startup_time = time.time() - start_time
        self.log(f"Total startup time to window appearance: {total_startup_time:.3f}s")
        
        # Start main loop
        try:
            root.mainloop()
        except KeyboardInterrupt:
            self.log("Keyboard interrupt received")
        except Exception as e:
            self.log(f"GUI error: {e}")
        
        return 0

def main():
    """Main entry point for SNID SAGE GUI with fast startup"""
    
    # Suppress third-party library output FIRST, before any imports
    suppress_third_party_output()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Create and run the fast launcher
    launcher = FastGUILauncher(args)
    return launcher.run()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 