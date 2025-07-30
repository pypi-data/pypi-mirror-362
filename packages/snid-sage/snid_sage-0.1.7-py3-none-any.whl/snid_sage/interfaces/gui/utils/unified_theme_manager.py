"""
SNID SAGE Unified Theme Manager
===============================

Centralized theme management system that consolidates all theming functionality:
- GUI widget theming
- Matplotlib plot theming  
- Button color management
- Dark/light mode synchronization
- Dialog window theming
- Platform-specific styling

This replaces the fragmented theme systems with a single, coordinated approach.
"""

import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import Dict, Any, Optional, Callable, Union, List, Tuple
from enum import Enum
import logging
import traceback

# Import centralized logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.unified_theme')
except ImportError:
    _LOGGER = logging.getLogger('gui.unified_theme')

# Import platform configuration
try:
    from snid_sage.shared.utils.config.platform_config import get_platform_config
    _PLATFORM_CONFIG = get_platform_config()
except ImportError:
    _PLATFORM_CONFIG = None
    _LOGGER.warning("Platform configuration not available - using default styling")


class ThemeMode(Enum):
    """Theme mode enumeration"""
    LIGHT = "light"
    DARK = "dark"


class ButtonType(Enum):
    """Button type categories for consistent theming"""
    PRIMARY = "primary"           # Main actions (Analysis, Load)
    SECONDARY = "secondary"       # Supporting actions (Navigation)
    SUCCESS = "success"          # Positive actions (Preprocessing)
    WARNING = "warning"          # Caution actions (Clear, Masks)
    DANGER = "danger"            # Destructive actions (Delete, Cancel)
    INFO = "info"                # Information actions (Results, Charts)
    ACCENT = "accent"            # Special features (AI, LLM)
    NEUTRAL = "neutral"          # Default/Unknown buttons


class UnifiedThemeManager:
    """
    Unified theme manager that handles all GUI and plot theming consistently.
    
    This manager ensures that:
    - All GUI widgets follow the same theme
    - All matplotlib plots have consistent backgrounds and colors
    - Dark/light toggle affects everything simultaneously
    - Button colors are logical and consistent
    - Dialog windows inherit proper theming
    """
    
    def __init__(self, master_widget: tk.Widget):
        """Initialize the unified theme manager"""
        self.master = master_widget
        self.current_mode = ThemeMode.LIGHT
        self.active_dialogs = []
        self.theme_callbacks = []
        
        # Flag to disable theme application during dialog creation
        self._theme_application_enabled = True
        
        # Platform-specific configuration
        self.platform_config = _PLATFORM_CONFIG
        self.gui_config = self.platform_config.get_gui_config() if self.platform_config else {}
        self.styling_config = self.platform_config.get_styling_config() if self.platform_config else {}
        
        # Apply platform-specific fixes
        if self.platform_config:
            self.platform_config.apply_platform_fixes()
        
        # Import matplotlib here to avoid issues during testing
        try:
            global plt
            import matplotlib.pyplot as plt
            self.matplotlib_available = True
            
            # Set platform-specific matplotlib backend
            if self.platform_config:
                backend = self.platform_config.get_dependency_config().get('matplotlib_backend', 'TkAgg')
                try:
                    plt.switch_backend(backend)
                except:
                    plt.switch_backend('TkAgg')  # Fallback
        except ImportError:
            self.matplotlib_available = False
        
        # Define platform-aware theme palette
        self.theme_colors = self._get_platform_theme_colors()
        
        _LOGGER.info("🎨 Unified Theme Manager initialized")
    
    def _get_platform_theme_colors(self) -> Dict[str, str]:
        """Get platform-specific theme colors"""
        # Base theme colors (Windows-style)
        base_colors = {
            # Backgrounds
            'bg_primary': '#f8fafc',      # Main background
            'bg_secondary': '#ffffff',    # Cards, dialogs
            'bg_tertiary': '#f1f5f9',     # Subtle backgrounds
            'bg_disabled': '#e2e8f0',     # Disabled elements
            
            # Text colors
            'text_primary': '#1e293b',    # Main text
            'text_secondary': '#475569',  # Secondary text
            'text_muted': '#94a3b8',      # Disabled/muted text
            'text_on_accent': '#ffffff',  # Text on colored backgrounds
            
            # Interactive elements
            'border': '#cbd5e1',          # Borders and separators
            'hover': '#f1f5f9',           # Hover backgrounds
            'active': '#e2e8f0',          # Active/pressed states
            'focus': '#3b82f6',           # Focus indicators
            'accent_primary': '#3b82f6',  # Default accent/selection colour (blue)
            'disabled': '#e2e8f0',        # Disabled state colour
            
            # Button colors by type
            'btn_primary': '#3b82f6',     # Blue - main actions
            'btn_primary_hover': '#2563eb',
            'btn_secondary': '#6b7280',   # Gray - secondary actions
            'btn_secondary_hover': '#4b5563',
            'btn_success': '#10b981',     # Green - positive actions
            'btn_success_hover': '#059669',
            'btn_warning': '#f59e0b',     # Orange - warning actions
            'btn_warning_hover': '#d97706',
            'btn_danger': '#ef4444',      # Red - destructive actions
            'btn_danger_hover': '#dc2626',
            'btn_info': '#6366f1',        # Indigo - info actions
            'btn_info_hover': '#4f46e5',
            'btn_accent': '#8b5cf6',      # Purple - special features
            'btn_accent_hover': '#7c3aed',
            'btn_neutral': '#9ca3af',     # Default button color
            'btn_neutral_hover': '#6b7280',
            
            # Matplotlib colors
            'plot_bg': '#ffffff',
            'plot_text': '#1e293b',
            'plot_grid': '#e2e8f0',
            'plot_line': '#0078d4',           # Default plot line color (consistent blue)
            'plot_line_primary': '#0078d4',   # Consistent blue for all spectrum plots
            'plot_line_secondary': '#10b981',
            'plot_line_accent': '#8b5cf6',
        }
        
        # Apply platform-specific adjustments
        if self.platform_config and self.platform_config.is_macos:
            # macOS-specific color adjustments for native appearance
            base_colors.update({
                'bg_primary': '#f5f5f5',      # Slightly warmer background
                'bg_secondary': '#ffffff',    # Pure white for cards
                'bg_tertiary': '#ececec',     # Subtle backgrounds
                'border': '#d1d1d1',          # Softer borders
                'hover': '#e8e8e8',           # Native hover color
                'active': '#d4d4d4',          # Native active color
                'focus': '#007aff',           # macOS system blue
                'accent_primary': '#007aff',  # macOS system blue
                
                # Adjust button colors for macOS
                'btn_primary': '#007aff',     # macOS system blue
                'btn_primary_hover': '#0056b3',
                'btn_success': '#28a745',     # macOS green
                'btn_success_hover': '#1e7e34',
                'btn_warning': '#ffc107',     # macOS orange
                'btn_warning_hover': '#e0a800',
                'btn_danger': '#dc3545',      # macOS red
                'btn_danger_hover': '#c82333',
                'btn_info': '#17a2b8',        # macOS teal
                'btn_info_hover': '#138496',
            })
        elif self.platform_config and self.platform_config.is_linux:
            # Linux-specific color adjustments
            base_colors.update({
                'bg_primary': '#f6f6f6',      # GTK-style background
                'border': '#c0c0c0',          # GTK-style borders
                'focus': '#4a90e2',           # GTK-style focus
                'accent_primary': '#4a90e2',  # GTK-style accent
            })
        
        return base_colors
    
    def get_current_colors(self) -> Dict[str, str]:
        """Get current theme color palette - always light mode"""
        return self.theme_colors.copy()
    
    def get_color(self, color_name: str) -> str:
        """Get specific color from light theme"""
        return self.theme_colors.get(color_name, '#000000')
    
    def is_dark_mode(self) -> bool:
        """Check if current theme is dark mode - always False"""
        return False
    
    def toggle_theme(self) -> str:
        """Legacy method - always returns light"""
        return 'light'
    
    def set_theme(self, theme_mode: Union[str, ThemeMode]) -> bool:
        """Set theme - always light mode"""
        return True
    
    def _apply_theme_globally(self):
        """Apply theme globally - Use specific methods instead"""
        _LOGGER.warning("🚫 Use apply_theme() or _apply_theme_to_main_window_only() instead")
        return
    
    def _apply_theme_to_widget_tree(self, widget: tk.Widget):
        """Apply theme to widget and all children with protection against workflow button interference"""
        try:
            # Don't theme workflow-managed buttons
            if isinstance(widget, tk.Button):
                if self._is_workflow_managed(widget):
                    return
                
            # Also check button text patterns
            try:
                button_text = widget.cget('text').lower()
                workflow_patterns = [
                    'load', 'browse', 'redshift', 'analysis', 'snid', 'results',
                    'preprocess', 'preprocessing', 'cluster', 'clustering', 'gmm', 
                    'configuration', 'settings', 'template', 'mask', 'emission',
                    'line', 'summary', 'chat', 'llm', 'ai', 'export', 'save',
                    'clear', 'reset', 'accept', 'cancel', 'apply', 'ok'
                ]
                if any(pattern in button_text for pattern in workflow_patterns):
                    return
            except:
                pass
            
            # Apply theme to current widget only if it's safe
            colors = self.get_current_colors()
            self._theme_widget(widget, colors)
            
            # Recursively apply to children with protection
            try:
                for child in widget.winfo_children():
                    self._apply_theme_to_widget_tree(child)
            except tk.TclError:
                # Widget may have been destroyed during iteration
                pass
                
        except Exception as e:
            # Don't let theme errors break the application
            pass
    
    def _theme_widget(self, widget: tk.Widget, colors: Dict[str, str]):
        """Apply theme to a specific widget based on its type"""
        try:
            widget_class = widget.__class__.__name__
            
            if widget_class == 'Frame':
                self._theme_frame(widget, colors)
            elif widget_class == 'Label':
                self._theme_label(widget, colors)
            elif widget_class == 'Button':
                self._theme_button(widget, colors)
            elif widget_class == 'Entry':
                self._theme_entry(widget, colors)
            elif widget_class == 'Text':
                self._theme_text(widget, colors)
            elif widget_class == 'Listbox':
                self._theme_listbox(widget, colors)
            elif widget_class == 'Canvas':
                self._theme_canvas(widget, colors)
            elif widget_class == 'Toplevel':
                self._theme_toplevel(widget, colors)
                
        except tk.TclError:
            # Widget may have been destroyed or not support certain options
            pass
    
    def _theme_frame(self, widget: tk.Frame, colors: Dict[str, str]):
        """Theme Frame widgets with platform-specific styling"""
        config = {'bg': colors['bg_primary']}
        
        # Apply platform-specific frame styling
        if self.platform_config and self.platform_config.is_macos:
            # macOS frames have no borders and use system background
            config.update({
                'relief': 'flat',
                'borderwidth': 0,
                'highlightthickness': 0,
            })
        elif self.platform_config and self.platform_config.is_windows:
            # Windows frames can have subtle borders
            config.update({
                'relief': 'flat',
                'borderwidth': 0,
            })
        
        widget.configure(**config)
    
    def _theme_label(self, widget: tk.Label, colors: Dict[str, str]):
        """Theme Label widgets with platform-specific styling"""
        config = {
            'bg': colors['bg_primary'],
            'fg': colors['text_primary']
        }
        
        # Apply platform-specific label styling
        if self.platform_config and self.platform_config.is_macos:
            # macOS labels should blend with background
            config.update({
                'relief': 'flat',
                'borderwidth': 0,
            })
        
        widget.configure(**config)
    
    def _theme_button(self, widget: tk.Button, colors: Dict[str, str]):
        """Button theming DISABLED - workflow system manages all button colors"""
        # All button theming is now handled by the workflow system

        pass
    
    def _classify_button_type(self, button_text: str) -> ButtonType:
        """Classify button type based on text content for appropriate theming"""
        text = button_text.lower()
        
        # Primary actions - main functionality
        if any(word in text for word in ['analyze', 'search', 'find', 'open', 'connect']):
            return ButtonType.PRIMARY
            
        # Success actions - positive outcomes
        if any(word in text for word in ['save', 'export', 'apply', 'confirm', 'ok', 'accept']):
            return ButtonType.SUCCESS
            
        # Warning actions - caution required
        if any(word in text for word in ['clear', 'reset', 'remove', 'delete']):
            return ButtonType.WARNING
            
        # Danger actions - destructive
        if any(word in text for word in ['cancel', 'abort', 'stop', 'quit', 'exit']):
            return ButtonType.DANGER
            
        # Info actions - informational
        if any(word in text for word in ['help', 'about', 'info', 'details', 'view']):
            return ButtonType.INFO
            
        # Accent actions - special features
        if any(word in text for word in ['ai', 'llm', 'chat', 'generate', 'advanced']):
            return ButtonType.ACCENT
            
        # Default to neutral
        return ButtonType.NEUTRAL
    
    def _theme_entry(self, widget: tk.Entry, colors: Dict[str, str]):
        """Theme Entry widgets with platform-specific styling"""
        config = {
            'bg': colors['bg_secondary'],
            'fg': colors['text_primary'],
            'insertbackground': colors['text_primary'],
            'highlightbackground': colors['border'],
            'highlightcolor': colors['focus']
        }
        
        # Apply platform-specific entry styling
        if self.platform_config and self.platform_config.is_macos:
            # macOS entries have rounded corners and focus rings
            config.update({
                'relief': 'solid',
                'borderwidth': 1,
                'highlightthickness': 2,
                'selectbackground': colors['focus'],
                'selectforeground': colors['text_on_accent'],
            })
        elif self.platform_config and self.platform_config.is_windows:
            # Windows entries have flat appearance
            config.update({
                'relief': 'solid',
                'borderwidth': 1,
                'highlightthickness': 1,
            })
        
        widget.configure(**config)
    
    def _theme_text(self, widget: tk.Text, colors: Dict[str, str]):
        """Theme Text widgets with platform-specific styling"""
        config = {
            'bg': colors['bg_secondary'],
            'fg': colors['text_primary'],
            'insertbackground': colors['text_primary'],
            'highlightbackground': colors['border'],
            'highlightcolor': colors['focus']
        }
        
        # Apply platform-specific text styling
        if self.platform_config and self.platform_config.is_macos:
            # macOS text widgets have native scrollbars and focus rings
            config.update({
                'relief': 'solid',
                'borderwidth': 1,
                'highlightthickness': 2,
                'selectbackground': colors['focus'],
                'selectforeground': colors['text_on_accent'],
                'wrap': 'word',
            })
        elif self.platform_config and self.platform_config.is_windows:
            # Windows text widgets have standard appearance
            config.update({
                'relief': 'solid',
                'borderwidth': 1,
                'highlightthickness': 1,
            })
        
        widget.configure(**config)
    
    def _theme_listbox(self, widget: tk.Listbox, colors: Dict[str, str]):
        """Theme Listbox widgets"""
        widget.configure(
            bg=colors['bg_secondary'],
            fg=colors['text_primary'],
            selectbackground=colors['focus'],
            selectforeground=colors['text_on_accent']
        )
    
    def _theme_canvas(self, widget: tk.Canvas, colors: Dict[str, str]):
        """Theme Canvas widgets"""
        widget.configure(bg=colors['bg_primary'])
    
    def _theme_toplevel(self, widget: tk.Toplevel, colors: Dict[str, str]):
        """Theme Toplevel (dialog) widgets"""
        widget.configure(bg=colors['bg_primary'])
    
    def _setup_matplotlib_theme(self):
        """Configure matplotlib with current theme colors"""
        if not self.matplotlib_available:
            return
            
        try:
            colors = self.get_current_colors()
            
            # Configure matplotlib rcParams for consistent theming
            plt.style.use('default')  # Reset to default first
            
            # Set global matplotlib parameters
            mpl.rcParams.update({
                'figure.facecolor': colors['plot_bg'],
                'axes.facecolor': colors['plot_bg'],
                'axes.edgecolor': colors['plot_grid'],
                'axes.labelcolor': colors['plot_text'],
                'axes.axisbelow': True,
                'axes.grid': True,
                'axes.spines.left': True,
                'axes.spines.bottom': True,
                'axes.spines.top': False,
                'axes.spines.right': False,
                'axes.linewidth': 0.8,
                'grid.color': colors['plot_grid'],
                'grid.linestyle': '-',
                'grid.linewidth': 0.5,
                'grid.alpha': 0.3,
                'xtick.color': colors['plot_text'],
                'ytick.color': colors['plot_text'],
                'xtick.labelsize': 10,
                'ytick.labelsize': 10,
                'text.color': colors['plot_text'],
                'font.size': 10,
                'legend.facecolor': colors['plot_bg'],
                'legend.edgecolor': colors['plot_grid'],
                'legend.fontsize': 9,
                'lines.linewidth': 1.5,
                'lines.color': colors['plot_line'],
                'patch.facecolor': colors['btn_primary'],
                'patch.edgecolor': colors['plot_grid'],
                'savefig.facecolor': colors['plot_bg'],
                'savefig.edgecolor': 'none',
                'savefig.dpi': 150,
                'figure.titlesize': 12,
                'axes.titlesize': 11,
                'axes.labelsize': 10,
            })
            
        except Exception as e:
            _LOGGER.warning(f"Error setting up matplotlib theme: {e}")
    
    def _update_all_plots(self):
        """Update all existing matplotlib figures with current theme"""
        if not self.matplotlib_available:
            return
            
        try:
            colors = self.get_current_colors()
            fig_nums = plt.get_fignums()
            
            for fig_num in fig_nums:
                try:
                    fig = plt.figure(fig_num)
                    
                    # Update figure background
                    fig.patch.set_facecolor(colors['plot_bg'])
                    
                    # Update all axes in the figure
                    for ax in fig.get_axes():
                        ax.set_facecolor(colors['plot_bg'])
                        ax.tick_params(colors=colors['plot_text'], labelcolor=colors['plot_text'])
                        ax.xaxis.label.set_color(colors['plot_text'])
                        ax.yaxis.label.set_color(colors['plot_text'])
                        ax.title.set_color(colors['plot_text'])
                        
                        # Update grid
                        ax.grid(True, color=colors['plot_grid'], alpha=0.3)
                        
                        # Update spines
                        for spine in ax.spines.values():
                            spine.set_color(colors['plot_grid'])
                        
                        # Update legend if present
                        legend = ax.get_legend()
                        if legend:
                            legend.get_frame().set_facecolor(colors['plot_bg'])
                            legend.get_frame().set_edgecolor(colors['plot_grid'])
                    
                    # Force redraw
                    fig.canvas.draw_idle()
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            pass
    
    def create_themed_figure(self, figsize: Tuple[float, float] = (10, 6), 
                           **kwargs) -> Tuple[plt.Figure, plt.Axes]:
        """Create a new matplotlib figure with proper theming"""
        if not self.matplotlib_available:
            raise ImportError("Matplotlib not available")
            
        colors = self.get_current_colors()
        
        fig, ax = plt.subplots(figsize=figsize, 
                              facecolor=colors['plot_bg'], 
                              **kwargs)
        
        # Apply theming
        ax.set_facecolor(colors['plot_bg'])
        ax.tick_params(colors=colors['plot_text'], labelcolor=colors['plot_text'])
        ax.grid(True, color=colors['plot_grid'], alpha=0.3)
        
        return fig, ax
    
    def register_dialog(self, dialog: tk.Toplevel):
        """Register a dialog for theme management"""
        if dialog not in self.active_dialogs:
            self.active_dialogs.append(dialog)
    
    def unregister_dialog(self, dialog: tk.Toplevel):
        """Unregister a dialog from theme management"""
        if dialog in self.active_dialogs:
            self.active_dialogs.remove(dialog)
    
    def add_theme_callback(self, callback: Callable[[str], None]):
        """Add callback for theme changes"""
        if callback not in self.theme_callbacks:
            self.theme_callbacks.append(callback)
    
    def add_theme_changed_callback(self, callback: Callable[[str], None]):
        """Add callback for theme changes - legacy compatibility"""
        self.add_theme_callback(callback)
    
    def disable_theme_application(self):
        """Temporarily disable theme application"""
        self._theme_application_enabled = False
    
    def enable_theme_application(self):
        """Re-enable theme application after dialog creation is complete"""
        self._theme_application_enabled = True
    
    def apply_theme(self, target_widget=None):
        """Apply theme to specific widget or main interface only (NOT globally)"""
        # Check if theme application is disabled during dialog creation
        if not self._theme_application_enabled:
            _LOGGER.debug("🛡️ THEME APPLICATION BLOCKED - disabled during dialog creation")
            return
        
        # CRITICAL DEBUG: Log every theme application call with stack trace
        stack_info = traceback.format_stack()
        caller_info = stack_info[-2].strip() if len(stack_info) >= 2 else "Unknown caller"
        
        if target_widget:
            widget_info = f"{target_widget.__class__.__name__}"
            _LOGGER.debug(f"🎨 THEME APPLY TO WIDGET: {widget_info}")
            _LOGGER.debug(f"   📍 Called from: {caller_info}")
            self._apply_theme_to_widget_tree(target_widget)
        else:
            _LOGGER.debug(f"🎨 THEME APPLY TO MAIN WINDOW")  
            _LOGGER.debug(f"   📍 Called from: {caller_info}")
            # Apply theme to main window only, not dialogs, and skip workflow buttons
            # This prevents interfering with workflow-managed button colors
            self._apply_theme_to_main_window_only()
            self._setup_matplotlib_theme()
            # DO NOT call _update_all_plots here as it can interfere with workflow buttons
    
    def _apply_theme_to_main_window_only(self):
        """Apply theme to main window only, avoiding interference with workflow buttons"""
        try:
            # Only apply to main window, skip buttons that might be workflow-managed
            colors = self.get_current_colors()
            
            # Apply to main window background and basic elements only
            if hasattr(self.master, 'configure'):
                try:
                    self.master.configure(bg=colors['bg_primary'])
                except tk.TclError:
                    pass
            
            # Apply to child widgets but be more selective about buttons
            self._apply_theme_selectively(self.master, colors)
            
        except Exception as e:
            pass
    
    def _apply_theme_selectively(self, widget: tk.Widget, colors: Dict[str, str]):
        """Apply theme selectively, being careful with buttons"""
        try:
            # Apply theme to current widget but be selective with buttons
            widget_class = widget.__class__.__name__
            
            if widget_class == 'Frame':
                self._theme_frame(widget, colors)
            elif widget_class == 'Label':
                self._theme_label(widget, colors)
            elif widget_class == 'Button':
    
                # Let the workflow system manage ALL button colors
                pass
            elif widget_class == 'Entry':
                self._theme_entry(widget, colors)
            elif widget_class == 'Text':
                self._theme_text(widget, colors)
            elif widget_class == 'Listbox':
                self._theme_listbox(widget, colors)
            elif widget_class == 'Canvas':
                self._theme_canvas(widget, colors)
            
            # Apply to children, but skip Toplevel windows (dialogs)
            try:
                for child in widget.winfo_children():
                    if child.__class__.__name__ != 'Toplevel':
                        self._apply_theme_selectively(child, colors)
            except tk.TclError:
                pass
                
        except Exception as e:
            pass
    
    def get_current_theme(self) -> Dict[str, Any]:
        """Get current theme information for compatibility"""
        colors = self.get_current_colors()
        return {
            'name': 'light',
            'colors': colors,
            'bg_color': colors['bg_primary'],
            'text_color': colors['text_primary'],
            'is_dark': False
        }
    
    def update_matplotlib_plot(self, fig, ax):
        """Update matplotlib plot with current theme"""
        try:
            colors = self.get_current_colors()
            
            # Update figure and axes backgrounds
            fig.patch.set_facecolor(colors['plot_bg'])
            ax.set_facecolor(colors['plot_bg'])
            
            # Update text colors
            ax.tick_params(colors=colors['plot_text'], labelcolor=colors['plot_text'])
            ax.xaxis.label.set_color(colors['plot_text'])
            ax.yaxis.label.set_color(colors['plot_text'])
            ax.title.set_color(colors['plot_text'])
            
            # Update grid and spines
            ax.grid(True, color=colors['plot_grid'], alpha=0.3)
            for spine in ax.spines.values():
                spine.set_color(colors['plot_grid'])
            
            # Update legend if present
            legend = ax.get_legend()
            if legend:
                legend.get_frame().set_facecolor(colors['plot_bg'])
                legend.get_frame().set_edgecolor(colors['plot_grid'])
                
        except Exception as e:
            pass
    
    def apply_theme_to_all_figures(self):
        """Apply theme to all matplotlib figures ONLY - no GUI button interference"""
        # CRITICAL: Only update matplotlib plots, never touch GUI buttons
        self._update_all_plots()
    
    def _notify_theme_changed(self):
        """Notify all registered callbacks about theme change"""
        for callback in self.theme_callbacks:
            try:
                callback('light')
            except Exception as e:
                pass
    
    def _apply_theme_to_dialog_only(self, dialog: tk.Toplevel):
        """Apply theme to a specific dialog window only"""
        try:
            colors = self.get_current_colors()
            
            # Apply theme to dialog and its children
            self._apply_theme_to_widget_tree(dialog)
            
            # Ensure dialog has proper background
            dialog.configure(bg=colors['bg_primary'])
            
            # Force update
            try:
                dialog.update_idletasks()
            except tk.TclError:
                # Widget may have been destroyed
                pass
                
        except Exception as e:
            pass

    def _is_workflow_managed(self, widget: tk.Widget) -> bool:
        """Return True if a button belongs to the workflow system (Python flag or Tcl var)."""
        try:
            if getattr(widget, '_workflow_managed', False):
                return True

            # Check Tcl variables: both path-based and id-based
            try:
                if widget.getvar(f"workflow_managed::{str(widget)}") == '1':
                    return True
            except tk.TclError:
                pass

            try:
                if widget.getvar(f"workflow_managed_{widget.winfo_id()}") == '1':
                    return True
            except tk.TclError:
                pass
            
            # DEBUG: log a miss for Button widgets we expected to be workflow managed
            try:
                widget_name = getattr(widget, '_workflow_button_name', 'unnamed')
                if isinstance(widget, tk.Button):
                    _LOGGER.debug(f"🧐 Workflow-managed check failed for button: {widget_name} (path {str(widget)})")
                    _LOGGER.debug(f"   📍 _workflow_managed: {getattr(widget, '_workflow_managed', 'NOT_SET')}")
                    _LOGGER.debug(f"   📍 _workflow_button_name: {getattr(widget, '_workflow_button_name', 'NOT_SET')}")
            except Exception:
                pass
            return False
        except Exception:
            return False


# Global theme manager instance
_global_theme_manager: Optional[UnifiedThemeManager] = None


def get_unified_theme_manager() -> Optional[UnifiedThemeManager]:
    """Get the global unified theme manager instance"""
    return _global_theme_manager


def initialize_unified_theme_manager(master_widget: tk.Widget) -> UnifiedThemeManager:
    """Initialize the global unified theme manager"""
    global _global_theme_manager
    _global_theme_manager = UnifiedThemeManager(master_widget)
    return _global_theme_manager


def create_themed_figure(figsize: Tuple[float, float] = (10, 6), 
                        **kwargs) -> Tuple[plt.Figure, plt.Axes]:
    """Create a themed matplotlib figure using the global theme manager"""
    theme_manager = get_unified_theme_manager()
    if theme_manager:
        return theme_manager.create_themed_figure(figsize, **kwargs)
    else:
        # Fallback to standard figure
        return plt.subplots(figsize=figsize, **kwargs) 
