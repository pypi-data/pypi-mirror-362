"""
SNID SAGE - Improved Button Workflow System
Unified system for managing button states and colors throughout the workflow.
"""

import tkinter as tk
from enum import Enum
from typing import Dict, List, Optional, Callable
import logging
import traceback

# Import centralized logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.button_workflow')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.button_workflow')

class WorkflowState(Enum):
    """Workflow states that trigger button activations"""
    INITIAL = "initial"
    FILE_LOADED = "file_loaded"
    PREPROCESSED = "preprocessed"
    REDSHIFT_SET = "redshift_set"
    ANALYSIS_COMPLETE = "analysis_complete"
    AI_READY = "ai_ready"

class ButtonColors:
    """Centralized button color definitions"""
    # User's specified color scheme
    LIGHT_GREY = "white"        # Initial disabled state (user prefers white)
    NEUTRAL_GREY = "#B0B0B0"    # Legacy grey (no longer used)
    LOAD_GREY = "#6E6E6E"       # Load button – medium grey matching palette
    AMBER = "#FFA600"           # Preprocessing
    CORAL = "#FF6361"           # Redshift
    MAGENTA = "#BC5090"         # SNID Analysis
    PURPLE = "#58508D"          # Advanced features
    DEEP_BLUE = "#003F5C"       # AI features
    
    # New colours for always-available utility buttons
    SETTINGS_GRAPHITE = "#7A8585"    # Settings button – Faint Graphite: subtle, calm, and system-feeling
    RESET_CRANBERRY = "#A65965"     # Reset button – Faint Cranberry: clearly distinct and appropriately serious
    
    # UI colors
    DARK_BORDER = "#555555"
    WHITE_TEXT = "white"
    BLACK_TEXT = "black"

class ButtonDefinition:
    """Definition of a button's workflow properties"""
    def __init__(self, name: str, enabled_color: str, activation_state: WorkflowState, 
                 always_enabled: bool = False, requires_ai: bool = False):
        self.name = name
        self.enabled_color = enabled_color
        self.activation_state = activation_state
        self.always_enabled = always_enabled
        self.requires_ai = requires_ai

class ImprovedButtonWorkflow:
    """Manages button states and colors according to workflow progression"""
    
    # Define the complete button workflow
    BUTTON_DEFINITIONS = {
        # Always available buttons
        'load_btn': ButtonDefinition('load_btn', ButtonColors.LOAD_GREY, WorkflowState.INITIAL, always_enabled=True),
        'reset_btn': ButtonDefinition('reset_btn', ButtonColors.RESET_CRANBERRY, WorkflowState.INITIAL, always_enabled=True),
        'settings_btn': ButtonDefinition('settings_btn', ButtonColors.SETTINGS_GRAPHITE, WorkflowState.INITIAL, always_enabled=True),
        
        # Workflow progression buttons
        'preprocess_btn': ButtonDefinition('preprocess_btn', ButtonColors.AMBER, WorkflowState.FILE_LOADED),
        'redshift_selection_btn': ButtonDefinition('redshift_selection_btn', ButtonColors.CORAL, WorkflowState.PREPROCESSED),
        'analysis_btn': ButtonDefinition('analysis_btn', ButtonColors.MAGENTA, WorkflowState.PREPROCESSED),  # Both activate after preprocessing
        
        # Advanced features (enabled after analysis)
        'emission_line_overlay_btn': ButtonDefinition('emission_line_overlay_btn', ButtonColors.PURPLE, WorkflowState.ANALYSIS_COMPLETE),
        'cluster_summary_btn': ButtonDefinition('cluster_summary_btn', ButtonColors.PURPLE, WorkflowState.ANALYSIS_COMPLETE),
        'gmm_btn': ButtonDefinition('gmm_btn', ButtonColors.PURPLE, WorkflowState.ANALYSIS_COMPLETE),
        'redshift_age_btn': ButtonDefinition('redshift_age_btn', ButtonColors.PURPLE, WorkflowState.ANALYSIS_COMPLETE),
        'subtype_proportions_btn': ButtonDefinition('subtype_proportions_btn', ButtonColors.PURPLE, WorkflowState.ANALYSIS_COMPLETE),
        
        # AI features (unified AI assistant – enabled after analysis complete)
        'ai_assistant_btn': ButtonDefinition('ai_assistant_btn', ButtonColors.DEEP_BLUE, WorkflowState.ANALYSIS_COMPLETE),
    }
    
    def __init__(self, gui_instance):
        self.gui = gui_instance
        self.current_state = WorkflowState.INITIAL
        self.button_widgets: Dict[str, tk.Button] = {}
        self.state_change_callbacks: list[Callable[[WorkflowState], None]] = []
        self.ai_configured = False
        
        _LOGGER.info("🔄 Improved Button Workflow System initialized")
    
    def register_button(self, button_name: str, button_widget: tk.Button):
        """Register a button widget with the workflow system"""
        if button_name in self.BUTTON_DEFINITIONS:
            self.button_widgets[button_name] = button_widget
            
            # Mark button as workflow-managed to prevent theme interference
            button_widget._workflow_managed = True
            button_widget._workflow_button_name = button_name
            
            # Set initial state forcefully
            definition = self.BUTTON_DEFINITIONS[button_name]
            if definition.always_enabled:
                self._set_button_state(button_widget, True, definition.enabled_color)
                _LOGGER.info(f"✅ Button {button_name} configured: {definition.enabled_color} (always enabled)")
            else:
                self._set_button_state(button_widget, False, ButtonColors.LIGHT_GREY)
                _LOGGER.info(f"✅ Button {button_name} configured: {ButtonColors.LIGHT_GREY} (disabled)")
            
            # Also register with workflow integrator if available
            if hasattr(self.gui, 'workflow_integrator') and self.gui.workflow_integrator:
                self.gui.workflow_integrator.register_button_if_needed(button_name, button_widget)
            
            _LOGGER.debug(f"✅ Button {button_name} registered with workflow system")
        else:
            _LOGGER.warning(f"⚠️ Unknown button name: {button_name}")
    
    def update_workflow_state(self, new_state: WorkflowState):
        """Update the workflow state and refresh all button states"""
        old_state = self.current_state
        self.current_state = new_state
        
        _LOGGER.info(f"🔄 Workflow state: {old_state.value} → {new_state.value}")
        
        # Update all button states
        self._refresh_all_buttons()
        
        # Notify callbacks
        for callback in self.state_change_callbacks:
            try:
                callback(new_state)
            except Exception as e:
                _LOGGER.error(f"❌ Error in state change callback: {e}")
    
    def set_ai_configured(self, configured: bool):
        """Set AI configuration status (legacy method, no longer affects button states)"""
        self.ai_configured = configured
        _LOGGER.info(f"🤖 AI configured: {configured} (no longer affects button states)")
    
    def _refresh_all_buttons(self):
        """Refresh the state of all registered buttons"""
        for button_name, definition in self.BUTTON_DEFINITIONS.items():
            if button_name in self.button_widgets:
                self._update_single_button(button_name, definition)
    
    def _update_single_button(self, button_name: str, definition: ButtonDefinition):
        """Update a single button's state based on current workflow"""
        button_widget = self.button_widgets[button_name]
        
        # Determine if button should be enabled
        should_enable = self._should_button_be_enabled(definition)
        
        # Set button state and color
        if should_enable:
            self._set_button_state(button_widget, True, definition.enabled_color)
            _LOGGER.info(f"🎨 Button {button_name}: ENABLED with color {definition.enabled_color}")
        else:
            self._set_button_state(button_widget, False, ButtonColors.LIGHT_GREY)
            _LOGGER.info(f"🎨 Button {button_name}: DISABLED with white background")
        
        _LOGGER.debug(f"🎨 Button {button_name}: {'enabled' if should_enable else 'disabled'}")
    
    def _should_button_be_enabled(self, definition: ButtonDefinition) -> bool:
        """Determine if a button should be enabled based on current state"""
        # Always enabled buttons
        if definition.always_enabled:
            return True
        
        # Check if we've reached the required state
        state_order = [
            WorkflowState.INITIAL,
            WorkflowState.FILE_LOADED,
            WorkflowState.PREPROCESSED,
            WorkflowState.REDSHIFT_SET,
            WorkflowState.ANALYSIS_COMPLETE,
            WorkflowState.AI_READY
        ]
        
        current_index = state_order.index(self.current_state)
        required_index = state_order.index(definition.activation_state)
        
        # Button enabled if we've reached or passed its activation state
        return current_index >= required_index
    
    def _set_button_state(self, button: tk.Button, enabled: bool, color: str):
        """Set button state and appearance with macOS compatibility"""
        try:
            # Get platform info to handle macOS differently
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            
            # Base configuration for all platforms
            base_config = {
                'state': ('normal' if enabled else 'disabled'),
                'fg': self._get_text_color(color),
                'disabledforeground': self._get_disabled_text_color(),
                'cursor': ('hand2' if enabled else 'arrow'),
                'relief': 'raised',
                'bd': 2
            }
            
            if platform_config and platform_config.is_macos:
                # Enhanced macOS-specific button styling to forcefully override system appearance
                macos_config = {
                    **base_config,
                    # Primary approach: Set background color
                    'bg': color,
                    'background': color,  # Alternative background property
                    
                    # Secondary approach: Use highlightbackground for macOS color control
                    'highlightbackground': color,
                    'highlightcolor': color,
                    'highlightthickness': 0,
                    
                    # Active and pressed state colors
                    'activebackground': self._darken_color(color),
                    'activeforeground': self._get_text_color(color),
                    
                    # Aggressive system appearance override
                    'borderwidth': 2,
                    'relief': 'raised',
                    'compound': 'none',
                    
                    # Additional macOS-specific properties to force custom appearance
                    'default': 'disabled',  # Disable default button styling
                    'takefocus': True,      # Allow focus for keyboard navigation
                    
                    # Try to override aqua styling
                    'selectbackground': self._darken_color(color),
                }
                
                # Apply configuration in stages to ensure it sticks
                try:
                    button.configure(**macos_config)
                    # Try to add selectforeground separately (may not be supported)
                    try:
                        button.configure(selectforeground=self._get_text_color(color))
                    except Exception:
                        pass  # Skip selectforeground if not supported
                except Exception as config_error:
                    _LOGGER.debug(f"Initial macOS button config failed: {config_error}")
                    # Try essential properties only
                    try:
                        button.configure(
                            bg=color, 
                            highlightbackground=color,
                            state=('normal' if enabled else 'disabled'),
                            fg=self._get_text_color(color)
                        )
                    except:
                        pass
                
                # Force background color using multiple techniques
                try:
                    # Technique 1: Direct background setting
                    button.configure(background=color)
                    
                    # Technique 2: Use itemconfigure if available
                    if hasattr(button, 'itemconfigure'):
                        try:
                            button.itemconfigure('background', background=color)
                        except:
                            pass
                    
                    # Technique 3: Set through option database
                    try:
                        button.option_add(f'*{button._name}.background', color)
                    except:
                        pass
                        
                    # Technique 4: Force update and re-apply color
                    button.update_idletasks()
                    button.configure(bg=color)
                    
                except Exception as force_error:
                    _LOGGER.debug(f"Force background color failed: {force_error}")
                
                # Schedule a delayed color re-application to overcome timing issues
                try:
                    def reapply_color():
                        try:
                            button.configure(bg=color, highlightbackground=color)
                        except:
                            pass
                    
                    button.after(50, reapply_color)  # Apply again after 50ms
                    
                except Exception as schedule_error:
                    _LOGGER.debug(f"Scheduled color reapplication failed: {schedule_error}")
                    
            else:
                # Windows/Linux configuration (original approach)
                windows_config = {
                    **base_config,
                    'bg': color,
                    'activebackground': self._darken_color(color),
                    'activeforeground': self._get_text_color(color),
                }
                button.configure(**windows_config)
            
            # Final verification and logging
            try:
                current_bg = button.cget('bg')
                if current_bg != color:
                    _LOGGER.debug(f"⚠️ Button color mismatch: expected {color}, got {current_bg}")
                else:
                    _LOGGER.debug(f"✅ Button color successfully set to {color}")
            except:
                pass
            
        except Exception as e:
            _LOGGER.error(f"Error setting button state: {e}")
            # Fallback: try basic configuration
            try:
                button.configure(
                    state=('normal' if enabled else 'disabled'),
                    bg=color,
                    fg=self._get_text_color(color),
                    cursor=('hand2' if enabled else 'arrow')
                )
            except:
                pass
    
    def _darken_color(self, hex_color: str) -> str:
        """Darken a hex color for hover effect"""
        try:
            # Remove the '#' if present
            hex_color = hex_color.lstrip('#')
            
            # Convert to RGB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Darken by 20%
            factor = 0.8
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color  # Return original if conversion fails
    
    def add_state_change_callback(self, callback: Callable[[WorkflowState], None]):
        """Add a callback to be called when workflow state changes"""
        self.state_change_callbacks.append(callback)
    
    def get_current_state(self) -> WorkflowState:
        """Get the current workflow state"""
        return self.current_state
    
    def reset_to_initial_state(self):
        """Reset workflow to initial state"""
        self.update_workflow_state(WorkflowState.INITIAL)
        self.ai_configured = False
        _LOGGER.info("🔄 Workflow reset to initial state")
    
    def _get_text_color(self, bg_color: str) -> str:
        """Get appropriate text color for background color"""
        # Light (white) backgrounds use black text for contrast; everything else gets white text.
        if bg_color == ButtonColors.LIGHT_GREY or bg_color.lower() in ["white", "#ffffff"]:
            return ButtonColors.BLACK_TEXT
        return ButtonColors.WHITE_TEXT
    
    def _get_disabled_text_color(self) -> str:
        """Get disabled text color"""
        return '#999999'  # Grey for disabled text



# Convenience functions for integration
def create_workflow_button(parent, text, font, command, button_name, workflow_system):
    """Create a button that's automatically registered with the workflow system"""
    # Get platform info for platform-specific handling
    try:
        from snid_sage.shared.utils.config.platform_config import get_platform_config
        platform_config = get_platform_config()
        is_macos = platform_config and platform_config.is_macos
        is_linux = platform_config and platform_config.is_linux
    except:
        is_macos = False
        is_linux = False
    
    # Linux-specific font size adjustment
    if is_linux and isinstance(font, tuple) and len(font) >= 2:
        # Reduce font size by 1 point for Linux to prevent text cutting
        font_size = max(10, font[1] - 1)  # Minimum 10px
        font = (font[0], font_size, font[2] if len(font) > 2 else 'normal')
    
    if is_macos:
        # Enhanced macOS-specific button creation with aggressive styling override
        button = tk.Button(
            parent,
            text=text,
            font=font,
            command=command,
            relief='raised',
            bd=2,
            pady=10,
            
            # Primary color setting approaches
            bg=ButtonColors.LIGHT_GREY,
            background=ButtonColors.LIGHT_GREY,
            
            # macOS-specific color control
            highlightbackground=ButtonColors.LIGHT_GREY,
            highlightcolor=ButtonColors.LIGHT_GREY,
            highlightthickness=0,
            
            # System appearance override
            compound='none',
            default='disabled',  # Disable default styling
            takefocus=True,      # Allow focus
            
            # Additional properties to force custom appearance
            selectbackground=ButtonColors.LIGHT_GREY,
            disabledforeground='#999999',
        )
        
        # Post-creation macOS enhancements
        try:
            # Force the button to use our styling instead of system styling
            button.configure(background=ButtonColors.LIGHT_GREY)
            # Try to add selectforeground separately (may not be supported)
            try:
                button.configure(selectforeground='black')
            except Exception:
                pass  # Skip selectforeground if not supported
            
            # Try to disable system button styling if available
            try:
                button.tk.call('::tk::unsupported::MacWindowStyle', 'style', button, 'plain')
            except:
                pass  # Not available on all Tk versions
            
            # Set option database entries to override defaults
            try:
                button.option_add(f'*{button._name}.background', ButtonColors.LIGHT_GREY)
                button.option_add(f'*{button._name}.highlightBackground', ButtonColors.LIGHT_GREY)
            except:
                pass
            
            # Schedule delayed styling to overcome macOS timing issues
            def apply_delayed_styling():
                try:
                    button.configure(
                        bg=ButtonColors.LIGHT_GREY,
                        highlightbackground=ButtonColors.LIGHT_GREY
                    )
                except:
                    pass
            
            button.after(10, apply_delayed_styling)
            
        except Exception as e:
            _LOGGER.debug(f"macOS button post-creation enhancements failed: {e}")
            
    else:
        # Windows/Linux button creation (original)
        button = tk.Button(
            parent,
            text=text,
            font=font,
            command=command,
            relief='raised',
            bd=2,
            pady=10,
            highlightbackground=ButtonColors.DARK_BORDER,
            highlightcolor=ButtonColors.DARK_BORDER
        )
    
    # Register with workflow system
    workflow_system.register_button(button_name, button)
    
    return button

def integrate_with_existing_gui(gui_instance):
    """Integrate the improved workflow system with an existing GUI"""
    workflow = ImprovedButtonWorkflow(gui_instance)
    
    # Register existing buttons if they exist
    button_mappings = {
        'load_btn': 'load_btn',
        'preprocess_btn': 'preprocess_btn',
        'redshift_selection_btn': 'redshift_selection_btn',
        'analysis_btn': 'analysis_btn',
        'emission_line_overlay_btn': 'emission_line_overlay_btn',
        'configure_llm_btn': 'configure_llm_btn',
        'summarize_llm_btn': 'summarize_llm_btn',
        'chat_llm_btn': 'chat_llm_btn',
        'reset_btn': 'reset_btn',
        'settings_btn': 'settings_btn'
    }
    
    for gui_attr, workflow_name in button_mappings.items():
        if hasattr(gui_instance, gui_attr):
            button = getattr(gui_instance, gui_attr)
            if button:
                workflow.register_button(workflow_name, button)
    
    return workflow 
