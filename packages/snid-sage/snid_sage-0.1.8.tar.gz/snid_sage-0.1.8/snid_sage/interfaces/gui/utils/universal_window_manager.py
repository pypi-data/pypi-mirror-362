"""
SNID SAGE Universal Window Manager
=================================

Provides standardized window management across all dialog components:
- Consistent fullscreen support (F11/Escape) for all dialogs
- Proper cross-platform window centering and sizing
- Responsive dialog sizing that adapts to screen resolution
- Window state management and restoration
- Unified dialog behavior across Windows, macOS, and Linux

This ensures all dialogs have consistent, professional window management.
"""

import tkinter as tk
from tkinter import ttk
import platform
from typing import Dict, Any, Optional, Tuple, Callable
from enum import Enum

# Import cross-platform utilities
try:
    from .cross_platform_window import CrossPlatformWindowManager
    CROSS_PLATFORM_AVAILABLE = True
except ImportError:
    CROSS_PLATFORM_AVAILABLE = False

# Import font management
try:
    from .unified_font_manager import get_font_manager, FontCategory
    FONT_MANAGER_AVAILABLE = True
except ImportError:
    FONT_MANAGER_AVAILABLE = False

# Import centralized logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.windows')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.windows')


class DialogSize(Enum):
    """Standard dialog sizes for consistency"""
    SMALL = (600, 500)       # Simple dialogs
    MEDIUM = (900, 700)      # Configuration dialogs
    LARGE = (1200, 800)      # Complex analysis dialogs
    XLARGE = (1400, 900)     # Full-featured dialogs
    FULLSCREEN = (-1, -1)    # Fullscreen mode


class UniversalWindowManager:
    """
    Universal window management system providing consistent behavior
    across all dialog components in SNID SAGE.
    """
    
    def __init__(self):
        """Initialize the universal window manager"""
        self.platform = platform.system()
        self.font_manager = get_font_manager() if FONT_MANAGER_AVAILABLE else None
        
        # Track dialog states for proper management
        self.dialog_states = {}  # dialog_id -> state_info
        
        # Screen information cache
        self._screen_info = None
        
        _LOGGER.info(f"🪟 Universal Window Manager initialized for {self.platform}")
    
    def _get_screen_info(self) -> Dict[str, int]:
        """Get screen dimensions and DPI information"""
        if self._screen_info is None:
            try:
                # Create temporary root to get screen info
                temp_root = tk.Tk()
                temp_root.withdraw()
                
                self._screen_info = {
                    'width': temp_root.winfo_screenwidth(),
                    'height': temp_root.winfo_screenheight(),
                    'dpi': temp_root.winfo_fpixels('1i')
                }
                
                temp_root.destroy()
                
            except Exception as e:
                _LOGGER.debug(f"Could not get screen info: {e}")
                # Fallback values
                self._screen_info = {
                    'width': 1920,
                    'height': 1080,
                    'dpi': 96
                }
        
        return self._screen_info
    
    def calculate_optimal_size(self, requested_size: DialogSize, 
                              min_size: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        """
        Calculate optimal dialog size based on screen resolution and DPI
        
        Args:
            requested_size: Standard dialog size enum
            min_size: Optional minimum size constraint
            
        Returns:
            Optimal (width, height) in pixels
        """
        screen_info = self._get_screen_info()
        screen_width = screen_info['width']
        screen_height = screen_info['height']
        dpi_scale = max(1.0, screen_info['dpi'] / 96.0)
        
        if requested_size == DialogSize.FULLSCREEN:
            return (screen_width, screen_height)
        
        # Get base size
        base_width, base_height = requested_size.value
        
        # Apply DPI scaling
        scaled_width = int(base_width * dpi_scale)
        scaled_height = int(base_height * dpi_scale)
        
        # Ensure dialog fits on screen (80% max)
        max_width = int(screen_width * 0.8)
        max_height = int(screen_height * 0.8)
        
        optimal_width = min(scaled_width, max_width)
        optimal_height = min(scaled_height, max_height)
        
        # Apply minimum size constraints
        if min_size:
            optimal_width = max(optimal_width, min_size[0])
            optimal_height = max(optimal_height, min_size[1])
        
        return (optimal_width, optimal_height)
    
    def setup_dialog(self, dialog: tk.Toplevel, 
                    title: str,
                    size: DialogSize = DialogSize.MEDIUM,
                    min_size: Optional[Tuple[int, int]] = None,
                    resizable: bool = True,
                    modal: bool = True,
                    parent: Optional[tk.Widget] = None,
                    enable_fullscreen: bool = True) -> str:
        """
        Setup a dialog with standardized window management
        
        Args:
            dialog: The Toplevel dialog window
            title: Dialog title
            size: Standard dialog size
            min_size: Optional minimum size
            resizable: Whether dialog is resizable
            modal: Whether dialog should be modal
            parent: Parent widget for centering
            enable_fullscreen: Whether to enable F11 fullscreen
            
        Returns:
            Dialog ID for state tracking
        """
        # Generate unique dialog ID
        dialog_id = f"{title}_{id(dialog)}"
        
        # Calculate optimal size
        optimal_width, optimal_height = self.calculate_optimal_size(size, min_size)
        
        # Configure dialog
        dialog.title(title)
        dialog.geometry(f"{optimal_width}x{optimal_height}")
        dialog.resizable(resizable, resizable)
        
        if min_size:
            dialog.minsize(min_size[0], min_size[1])
        
        # Store dialog state
        self.dialog_states[dialog_id] = {
            'dialog': dialog,
            'normal_geometry': f"{optimal_width}x{optimal_height}",
            'is_fullscreen': False,
            'parent': parent,
            'enable_fullscreen': enable_fullscreen
        }
        
        # Setup fullscreen bindings if enabled
        if enable_fullscreen:
            self._setup_fullscreen_bindings(dialog, dialog_id)
        
        # Make modal if requested
        if modal and parent:
            dialog.transient(parent)
            dialog.grab_set()
        
        # Center the dialog
        self.center_dialog(dialog_id)
        
        _LOGGER.debug(f"🪟 Dialog setup complete: {dialog_id} ({optimal_width}x{optimal_height})")
        
        return dialog_id
    
    def _setup_fullscreen_bindings(self, dialog: tk.Toplevel, dialog_id: str):
        """Setup fullscreen keyboard bindings for a dialog"""
        # Bind F11 for fullscreen toggle
        dialog.bind('<F11>', lambda e: self.toggle_fullscreen(dialog_id))
        
        # Bind Escape to exit fullscreen
        dialog.bind('<Escape>', lambda e: self.exit_fullscreen(dialog_id))
        
        # Make dialog focusable for keyboard events
        dialog.focus_set()
        
        _LOGGER.debug(f"🪟 Fullscreen bindings setup for {dialog_id}")
    
    def center_dialog(self, dialog_id: str):
        """Center a dialog on its parent or screen"""
        if dialog_id not in self.dialog_states:
            return
        
        state = self.dialog_states[dialog_id]
        dialog = state['dialog']
        parent = state['parent']
        
        # Ensure dialog is updated
        dialog.update_idletasks()
        
        try:
            dialog_width = dialog.winfo_width()
            dialog_height = dialog.winfo_height()
            
            if parent and hasattr(parent, 'winfo_x'):
                # Center on parent
                parent_x = parent.winfo_x()
                parent_y = parent.winfo_y()
                parent_width = parent.winfo_width()
                parent_height = parent.winfo_height()
                
                x = parent_x + (parent_width - dialog_width) // 2
                y = parent_y + (parent_height - dialog_height) // 2
            else:
                # Center on screen
                screen_info = self._get_screen_info()
                x = (screen_info['width'] - dialog_width) // 2
                y = (screen_info['height'] - dialog_height) // 2
            
            # Ensure dialog is within screen bounds
            screen_info = self._get_screen_info()
            x = max(0, min(x, screen_info['width'] - dialog_width))
            y = max(0, min(y, screen_info['height'] - dialog_height))
            
            dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
            
        except Exception as e:
            _LOGGER.debug(f"Could not center dialog {dialog_id}: {e}")
    
    def toggle_fullscreen(self, dialog_id: str) -> bool:
        """
        Toggle fullscreen mode for a dialog
        
        Args:
            dialog_id: Dialog identifier
            
        Returns:
            True if now fullscreen, False if windowed
        """
        if dialog_id not in self.dialog_states:
            return False
        
        state = self.dialog_states[dialog_id]
        dialog = state['dialog']
        
        if state['is_fullscreen']:
            return self.exit_fullscreen(dialog_id)
        else:
            return self.enter_fullscreen(dialog_id)
    
    def enter_fullscreen(self, dialog_id: str) -> bool:
        """Enter fullscreen mode for a dialog"""
        if dialog_id not in self.dialog_states:
            return False
        
        state = self.dialog_states[dialog_id]
        dialog = state['dialog']
        
        try:
            # Store current geometry
            dialog.update_idletasks()
            current_geo = dialog.geometry()
            state['normal_geometry'] = current_geo
            
            # Apply fullscreen using cross-platform method if available
            if CROSS_PLATFORM_AVAILABLE:
                success = CrossPlatformWindowManager.setup_fullscreen(dialog, True)
            else:
                # Fallback method
                dialog.attributes('-fullscreen', True)
                success = True
            
            if success:
                state['is_fullscreen'] = True
                _LOGGER.debug(f"🖥️ Dialog {dialog_id} entered fullscreen")
                return True
            
        except Exception as e:
            _LOGGER.debug(f"Could not enter fullscreen for {dialog_id}: {e}")
        
        return False
    
    def exit_fullscreen(self, dialog_id: str) -> bool:
        """Exit fullscreen mode for a dialog"""
        if dialog_id not in self.dialog_states:
            return False
        
        state = self.dialog_states[dialog_id]
        dialog = state['dialog']
        
        if not state['is_fullscreen']:
            return False
        
        try:
            # Exit fullscreen using cross-platform method if available
            if CROSS_PLATFORM_AVAILABLE:
                success = CrossPlatformWindowManager.setup_fullscreen(dialog, False)
            else:
                # Fallback method
                dialog.attributes('-fullscreen', False)
                dialog.state('normal')
                success = True
            
            if success:
                # Restore normal geometry
                if state['normal_geometry']:
                    dialog.geometry(state['normal_geometry'])
                
                state['is_fullscreen'] = False
                _LOGGER.debug(f"🪟 Dialog {dialog_id} exited fullscreen")
                return False
            
        except Exception as e:
            _LOGGER.debug(f"Could not exit fullscreen for {dialog_id}: {e}")
        
        return True
    
    def add_fullscreen_button(self, parent_frame: tk.Widget, dialog_id: str) -> tk.Button:
        """
        Add a fullscreen toggle button to a dialog
        
        Args:
            parent_frame: Frame to add button to
            dialog_id: Dialog identifier
            
        Returns:
            The created button widget
        """
        # Create button with proper font
        button_text = "🖥️ Fullscreen (F11)"
        
        if self.font_manager:
            font_tuple = self.font_manager.get_font(FontCategory.BUTTON)
            button = tk.Button(parent_frame, text=button_text,
                             font=font_tuple,
                             command=lambda: self.toggle_fullscreen(dialog_id))
        else:
            button = tk.Button(parent_frame, text=button_text,
                             command=lambda: self.toggle_fullscreen(dialog_id))
        
        return button
    
    def cleanup_dialog(self, dialog_id: str):
        """Cleanup dialog state when dialog is destroyed"""
        if dialog_id in self.dialog_states:
            del self.dialog_states[dialog_id]
            _LOGGER.debug(f"🗑️ Cleaned up dialog state: {dialog_id}")
    
    def get_dialog_state(self, dialog_id: str) -> Optional[Dict[str, Any]]:
        """Get current state of a dialog"""
        return self.dialog_states.get(dialog_id)
    
    def apply_consistent_styling(self, dialog: tk.Toplevel, theme_manager=None):
        """Apply consistent styling to a dialog"""
        try:
            if theme_manager:
                # Apply theme colors
                colors = theme_manager.get_current_colors()
                dialog.configure(bg=colors.get('bg_primary', '#ffffff'))
                
                # Apply theme to dialog after creation
                # Dialog themes itself independently, no need to apply main window theme
            
            # Apply font scaling if available
            if self.font_manager:
                # The font manager will be used by child widgets
                pass
                
        except Exception as e:
            _LOGGER.debug(f"Could not apply consistent styling: {e}")


# Global window manager instance
_WINDOW_MANAGER = None

def get_window_manager() -> UniversalWindowManager:
    """Get the global window manager instance"""
    global _WINDOW_MANAGER
    if _WINDOW_MANAGER is None:
        _WINDOW_MANAGER = UniversalWindowManager()
    return _WINDOW_MANAGER


def setup_dialog(dialog: tk.Toplevel, title: str, size: DialogSize = DialogSize.MEDIUM,
                min_size: Optional[Tuple[int, int]] = None, **kwargs) -> str:
    """Convenience function to setup a dialog with standard management"""
    return get_window_manager().setup_dialog(dialog, title, size, min_size, **kwargs)


def add_fullscreen_support(parent_frame: tk.Widget, dialog_id: str) -> tk.Button:
    """Convenience function to add fullscreen button"""
    return get_window_manager().add_fullscreen_button(parent_frame, dialog_id) 
