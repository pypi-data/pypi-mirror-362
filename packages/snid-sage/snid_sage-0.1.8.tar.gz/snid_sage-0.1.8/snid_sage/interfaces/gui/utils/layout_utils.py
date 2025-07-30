"""
Layout utilities for SNID SAGE GUI components.
Provides modular layout creation functions for consistent GUI design.
"""

import tkinter as tk
from tkinter import ttk
import os
import sys

# Import centralized logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.layout')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.layout')

# Color constants - now managed by the improved workflow system
BUTTON_COLORS = {
    'disabled': "white",
    # Lightened border colour for raised buttons to soften edges
    'border': "#555555"
}

def create_cross_platform_button(parent, text, command=None, **kwargs):
    """
    Create a button that works properly on all platforms, especially macOS.
    
    This function handles the macOS Tkinter button color issue by using
    highlightbackground and other workarounds.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Button command callback
        **kwargs: Additional button configuration options
        
    Returns:
        Configured tk.Button widget
    """
    # Get platform info for platform-specific handling
    try:
        from snid_sage.shared.utils.config.platform_config import get_platform_config
        platform_config = get_platform_config()
        is_macos = platform_config and platform_config.is_macos
        is_linux = platform_config and platform_config.is_linux
    except:
        is_macos = False
        is_linux = False
    
    # Extract color-related kwargs
    bg_color = kwargs.pop('bg', 'white')
    fg_color = kwargs.pop('fg', 'black')
    
    # Linux-specific adjustments to prevent text cutting
    if is_linux:
        # Reduce font size for Linux to prevent text overflow
        if 'font' in kwargs:
            font_tuple = kwargs['font']
            if isinstance(font_tuple, tuple) and len(font_tuple) >= 2:
                # Reduce font size by 1-2 points for Linux
                font_size = max(10, font_tuple[1] - 1)  # Minimum 10px
                kwargs['font'] = (font_tuple[0], font_size, font_tuple[2] if len(font_tuple) > 2 else 'normal')
        
        # Increase padding for Linux buttons
        if 'padx' not in kwargs:
            kwargs['padx'] = 15  # Default 15px horizontal padding for Linux
        else:
            kwargs['padx'] = max(kwargs['padx'], 15)  # Ensure minimum 15px
            
        if 'pady' not in kwargs:
            kwargs['pady'] = 10  # Default 10px vertical padding for Linux
        else:
            kwargs['pady'] = max(kwargs['pady'], 10)  # Ensure minimum 10px
    
    # Base configuration
    base_config = {
        'text': text,
        'command': command,
        'relief': kwargs.pop('relief', 'raised'),
        'bd': kwargs.pop('bd', 2),
        'cursor': kwargs.pop('cursor', 'hand2'),
        **kwargs  # Include any other kwargs
    }
    
    if is_macos:
        # Enhanced macOS-specific button configuration with aggressive styling override
        macos_config = {
            **base_config,
            
            # Multiple background color approaches for macOS
            'bg': bg_color,
            'background': bg_color,
            'fg': fg_color,
            'foreground': fg_color,
            
            # macOS color control techniques
            'highlightbackground': bg_color,
            'highlightcolor': bg_color,
            'highlightthickness': 0,
            
            # System appearance override
            'borderwidth': base_config['bd'],
            'compound': 'none',
            'default': 'disabled',  # Disable default button styling
            'takefocus': True,
            
            # Additional properties to force custom appearance
            'selectbackground': bg_color,
            'disabledforeground': '#999999',
            
            # Active state colors
            'activebackground': bg_color,
            'activeforeground': fg_color,
        }
        button = tk.Button(parent, **macos_config)
        
        # Post-creation macOS enhancements
        try:
            # Force background color using multiple techniques
            button.configure(background=bg_color)
            # Try to add selectforeground separately (may not be supported)
            try:
                button.configure(selectforeground=fg_color)
            except Exception:
                pass  # Skip selectforeground if not supported
            
            # Try to disable system button styling if available (macOS-specific)
            try:
                button.tk.call('::tk::unsupported::MacWindowStyle', 'style', button, 'plain')
            except:
                pass  # Not available on all Tk versions
            
            # Set option database entries to override system defaults
            try:
                if hasattr(button, '_name') and button._name:
                    button.option_add(f'*{button._name}.background', bg_color)
                    button.option_add(f'*{button._name}.highlightBackground', bg_color)
            except:
                pass
            
            # Force immediate update
            button.update_idletasks()
            
            # Schedule delayed color application to overcome macOS timing issues
            def apply_delayed_macOS_styling():
                try:
                    button.configure(bg=bg_color, highlightbackground=bg_color)
                    _LOGGER.debug(f"✅ Delayed macOS button color applied: {bg_color}")
                except Exception as delayed_error:
                    _LOGGER.debug(f"Delayed macOS styling failed: {delayed_error}")
            
            button.after(25, apply_delayed_macOS_styling)
            
        except Exception as enhancement_error:
            _LOGGER.debug(f"macOS button post-creation enhancements failed: {enhancement_error}")
            
    else:
        # Windows/Linux configuration
        windows_config = {
            **base_config,
            'bg': bg_color,
            'fg': fg_color,
        }
        button = tk.Button(parent, **windows_config)
    
    return button

def _create_workflow_button(parent, text, font, command, button_name, gui_instance):
    """Create a button that's managed by the workflow system"""
    
    # Create button using cross-platform function
    button = create_cross_platform_button(
        parent,
        text=text,
        font=font,
        command=command,
        bg=BUTTON_COLORS['disabled'],
        fg='black',
        relief='raised',
        bd=2,
        pady=10,
        cursor='hand2',
        state='disabled'
    )
    
    # Mark button as workflow-managed to prevent theme interference
    button._workflow_managed = True
    button._workflow_button_name = button_name
    
    # Register with workflow system if available
    if hasattr(gui_instance, 'workflow_integrator') and gui_instance.workflow_integrator:
        gui_instance.workflow_integrator.workflow.register_button(button_name, button)
        _LOGGER.debug(f"✅ Button {button_name} registered with workflow system")
    else:
        _LOGGER.debug(f"⏳ Button {button_name} created - workflow system will register it later")
    
    return button


class LayoutUtils:
    """Utility class for creating GUI layouts"""
    
    @staticmethod
    def create_main_layout(gui_instance, master):
        """Create the main application layout structure"""
        try:
            # Main container
            main_container = tk.Frame(master, bg=gui_instance.theme_manager.get_color('bg_primary'))
            main_container.pack(fill='both', expand=True)
            
            # Create header
            header_frame = LayoutUtils.create_header(gui_instance, main_container)
            
            # Create content area below header
            content_frame = tk.Frame(main_container, bg=gui_instance.theme_manager.get_color('bg_primary'))
            content_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
            
            return main_container, header_frame, content_frame
            
        except Exception as e:
            _LOGGER.error(f"Error creating main layout: {e}")
            return None, None, None
    
    @staticmethod
    def create_header(gui_instance, parent):
        """Create application header with logo and status"""
        try:
            # Construct a header frame that sizes itself naturally to its content (logo & status)
            # and uses minimal external padding so the header does not dominate vertical space.
            header_frame = tk.Frame(
                parent,
                bg=gui_instance.theme_manager.get_color('bg_secondary')
            )
            # Modest outer padding (10 px instead of 20) – reduces white-space top/bottom.
            header_frame.pack(fill='x', padx=10, pady=10)
            # Allow the frame to shrink/expand based on its children.
            header_frame.pack_propagate(True)
            
            # Internal content padding trimmed (horizontal 10, vertical 5).
            content = tk.Frame(header_frame, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            content.pack(fill='both', expand=True, padx=10, pady=5)
            
            # Logo removed – no left section. Ensure downstream attributes exist.
            gui_instance.logo_label = None
            
            # Center - Status section with info button
            center_section = tk.Frame(content, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            center_section.pack(fill='x', expand=True)
            
            # Container for info button and status bar
            status_container = tk.Frame(center_section, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            status_container.pack(fill='x', expand=True)
            
            # Info button (left side) - fixed square size with larger icon
            # Create a wrapper frame with fixed pixel dimensions for precise control
            info_frame = tk.Frame(status_container, width=36, height=36, 
                                bg=gui_instance.theme_manager.get_color('bg_secondary'))
            info_frame.pack(side='left', padx=(0, 10))
            info_frame.pack_propagate(False)  # Prevent frame from resizing to fit contents
            
            info_btn = create_cross_platform_button(
                info_frame,
                text="ℹ",
                font=('Segoe UI', 24, 'bold'),  # Large font for the icon
                bg=gui_instance.theme_manager.get_color('accent_primary'),
                fg='white',
                relief='raised',
                bd=1,
                padx=0,  # No internal padding - frame controls size
                pady=0,  # No internal padding - frame controls size
                cursor='hand2',
                command=lambda: gui_instance._show_shortcuts_dialog() if hasattr(gui_instance, '_show_shortcuts_dialog') else None
            )
            # Position the button precisely within the frame to control icon placement
            # x=0, y=0 would be top-left, y=5 pushes the icon down 5 pixels
            info_btn.place(x=-2, y=-5, width=40, height=40)
            
            # Store reference to info button
            gui_instance.info_btn = info_btn
            
            # Add tooltip for info button
            LayoutUtils._add_tooltip(gui_instance, info_btn, "Show keyboard shortcuts and hotkeys")
            
            # Status box with border (takes remaining space)
            status_box = tk.Frame(status_container, bg=gui_instance.theme_manager.get_color('bg_tertiary'), 
                                 highlightbackground=gui_instance.theme_manager.get_color('border'),
                                 highlightthickness=1, relief='solid', bd=1)
            status_box.pack(side='left', expand=True, fill='both')
            
            # Status content
            status_content = tk.Frame(status_box, bg=gui_instance.theme_manager.get_color('bg_tertiary'))
            status_content.pack(fill='both', expand=True, padx=10, pady=1)
            
            # Status label
            gui_instance.header_status_label = tk.Label(status_content, text="🚀 Ready - Load a spectrum to begin analysis",
                                                       font=('Segoe UI', 11, 'normal'),
                                                       bg=gui_instance.theme_manager.get_color('bg_tertiary'),
                                                       fg=gui_instance.theme_manager.get_color('text_primary'),
                                                       anchor='center')
            gui_instance.header_status_label.pack(expand=True, fill='x')
            
            return header_frame
            
        except Exception as e:
            _LOGGER.error(f"Error creating header: {e}")
            return None

    @staticmethod
    def create_left_panel(gui_instance, parent):
        """Create left panel with workflow sections"""
        try:
            left_panel = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'), width=240,
                                 highlightbackground=gui_instance.theme_manager.get_color('border'),
                                 highlightthickness=1, relief='flat')
            left_panel.pack(side='left', fill='y', padx=(0, 5))
            left_panel.pack_propagate(False)
            
            # Main content frame
            content = tk.Frame(left_panel, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            content.pack(fill='both', expand=True, padx=10, pady=(20, 10))
            
            # Load spectrum section
            LayoutUtils._create_load_section(gui_instance, content)
            
            # Preprocessing section (moved up before redshift)
            LayoutUtils._create_preprocessing_section(gui_instance, content)
            
            # Galaxy Analysis section (redshift selection)
            LayoutUtils._create_galaxy_analysis_section(gui_instance, content)
            
            # Configuration section (now includes Analysis button)
            LayoutUtils._create_configuration_section(gui_instance, content)
            
            # SN Emission Line Overlay section (moved from analysis section)
            LayoutUtils._create_emission_line_section(gui_instance, content)
            
            # Chat with AI section
            LayoutUtils._create_chat_section(gui_instance, content)
            
            # Settings section at the bottom
            settings_frame = tk.Frame(left_panel, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            settings_frame.pack(fill='x', side='bottom', padx=10, pady=(0, 10))
            
            # Settings button
            gui_instance.settings_btn = create_cross_platform_button(
                settings_frame, 
                text="⚙️ Settings",
                font=('Segoe UI', 10, 'bold'),
                command=lambda: gui_instance._open_settings_dialog() if hasattr(gui_instance, '_open_settings_dialog') else None,
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                cursor='hand2'
            )
            gui_instance.settings_btn.pack(side='left', fill='both', expand=True, padx=(0, 2))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.settings_btn, 
                                   "Open GUI settings dialog\nConfigure fonts, themes, display options")
            
            # Reset button
            gui_instance.reset_btn = create_cross_platform_button(
                settings_frame, 
                text="🔄 Reset",
                font=('Segoe UI', 10, 'bold'),
                command=lambda: gui_instance.reset_gui_to_initial_state() if hasattr(gui_instance, 'reset_gui_to_initial_state') else None,
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                cursor='hand2'
            )
            gui_instance.reset_btn.pack(side='left', fill='both', expand=True, padx=(2, 0))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.reset_btn, 
                                    "Reset GUI to initial state\nClears all data, plots, and analysis results\nKeeps theme and settings unchanged")
            
            _LOGGER.info("✅ Left panel created successfully")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error creating left panel: {e}")
            import traceback
            traceback.print_exc()
    
    @staticmethod
    def create_center_panel(gui_instance, parent):
        """Create center panel with plot area"""
        try:
            center_panel = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'),
                                  highlightbackground=gui_instance.theme_manager.get_color('border'),
                                  highlightthickness=1, relief='flat')
            center_panel.pack(side='left', fill='both', expand=True, padx=(0, 0))
            
            # Plot area header - reduced height and padding
            plot_header = tk.Frame(center_panel, bg=gui_instance.theme_manager.get_color('bg_secondary'), height=60)
            plot_header.pack(fill='x', padx=10, pady=(10, 0))
            plot_header.pack_propagate(False)
            
            # Plot controls
            controls_frame = tk.Frame(plot_header, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            controls_frame.pack(fill='both', expand=True)
            
            # First row: Navigation and view controls
            nav_row = tk.Frame(controls_frame, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            nav_row.pack(fill='x', pady=(0, 5))
            
            # Template navigation with 4-arrow layout
            nav_frame = tk.Frame(nav_row, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            nav_frame.pack(side='left')
            
            # Left arrow
            gui_instance.prev_btn = create_cross_platform_button(
                nav_frame,
                text='◀',
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('bg_tertiary'), 
                fg=gui_instance.theme_manager.get_color('text_secondary'),
                relief='raised',
                bd=2,
                padx=8,
                pady=4,
                cursor='hand2',
                command=gui_instance.prev_template,
                state='disabled',
                width=3,
                height=1
            )
            gui_instance.prev_btn.pack(side='left', padx=(0, 2))
            
            # Up/Down buttons in center
            center_nav = tk.Frame(nav_frame, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            center_nav.pack(side='left', padx=2)
            
            gui_instance.up_btn = create_cross_platform_button(
                center_nav,
                text='▲',
                font=('Segoe UI', 10, 'bold'),
                bg=gui_instance.theme_manager.get_color('bg_tertiary'),
                fg=gui_instance.theme_manager.get_color('text_secondary'),
                relief='raised',
                bd=2,
                padx=6,
                pady=2,
                cursor='hand2',
                # Cycle view upwards (Flux/Flat) via the central event handler
                command=lambda: gui_instance.event_handlers._handle_view_cycling(None, 'up'),
                state='disabled',
                width=3,
                height=1,
            )
            gui_instance.up_btn.pack()
            
            gui_instance.down_btn = create_cross_platform_button(
                center_nav,
                text='▼',
                font=('Segoe UI', 10, 'bold'),
                bg=gui_instance.theme_manager.get_color('bg_tertiary'),
                fg=gui_instance.theme_manager.get_color('text_secondary'),
                relief='raised',
                bd=2,
                padx=6,
                pady=2,
                cursor='hand2',
                # Cycle view downwards (Flux/Flat) via the central event handler
                command=lambda: gui_instance.event_handlers._handle_view_cycling(None, 'down'),
                state='disabled',
                width=3,
                height=1,
            )
            gui_instance.down_btn.pack()
            
            # Right arrow
            gui_instance.next_btn = create_cross_platform_button(
                nav_frame,
                text='▶',
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('bg_tertiary'), 
                fg=gui_instance.theme_manager.get_color('text_secondary'),
                relief='raised',
                bd=2,
                padx=8,
                pady=4,
                cursor='hand2',
                command=gui_instance.next_template,
                state='disabled',
                width=3,
                height=1
            )
            gui_instance.next_btn.pack(side='left', padx=(2, 0))
            
            # View style segmented control (center) - now includes Correlation
            view_frame = tk.Frame(nav_row, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            view_frame.pack(side='left', padx=(20, 0))
            
            view_label = tk.Label(view_frame, text="View:",
                                font=('Segoe UI', 12, 'bold'),
                                bg=gui_instance.theme_manager.get_color('bg_secondary'),
                                fg=gui_instance.theme_manager.get_color('text_primary'))
            view_label.pack(side='left', padx=(0, 10))
            
            # Updated view options to include Flux and Flat (template-specific)
            view_options = ["Flux", "Flat"]
            ToggleUtils.create_segmented_control(gui_instance, view_frame, view_options, gui_instance.view_style)
            
            # Reposition navigation arrows to appear immediately to the right of the segmented view buttons
            # This ensures the "‹" and "›" buttons come after the Flux/Flat toggle in visual order
            try:
                nav_frame.pack_forget()
                nav_frame.pack(side='left', padx=(20, 0))
            except Exception as e:
                _LOGGER.warning(f"❗ Could not reposition navigation buttons: {e}")
            
            # Overall Analysis buttons on the right side
            analysis_buttons_frame = tk.Frame(nav_row, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            analysis_buttons_frame.pack(side='right', padx=(0, 10))
            
            # Analysis Results button with same size as Flux/Flat
            gui_instance.cluster_summary_btn = create_cross_platform_button(
                analysis_buttons_frame,
                text="📋 Results",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.show_cluster_summary() if hasattr(gui_instance, 'show_cluster_summary') else None,
                state='disabled'
            )
            gui_instance.cluster_summary_btn.pack(side='left', padx=(0, 4))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.cluster_summary_btn, "Comprehensive analysis results summary\nShows classification, redshift, age estimates, and template details")
            
            # GMM clustering button with same size as Flux/Flat
            gui_instance.gmm_btn = create_cross_platform_button(
                analysis_buttons_frame,
                text="🔮 GMM",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.plot_gmm_clustering() if hasattr(gui_instance, 'plot_gmm_clustering') else None,
                state='disabled'
            )
            gui_instance.gmm_btn.pack(side='left', padx=(0, 4))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.gmm_btn, "Type-specific GMM clustering with 3D visualization\nRedshift vs Type vs RLAP")
            
            # Redshift vs age button with same size as Flux/Flat
            gui_instance.redshift_age_btn = create_cross_platform_button(
                analysis_buttons_frame,
                text="📈 z vs Age",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.plot_redshift_age() if hasattr(gui_instance, 'plot_redshift_age') else None,
                state='disabled'
            )
            gui_instance.redshift_age_btn.pack(side='left', padx=(0, 4))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.redshift_age_btn, "Redshift vs Age distribution analysis")
            
            # Subtype proportions button with same size as Flux/Flat
            gui_instance.subtype_proportions_btn = create_cross_platform_button(
                analysis_buttons_frame,
                text="🥧 Subtypes",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.plot_subtype_proportions() if hasattr(gui_instance, 'plot_subtype_proportions') else None,
                state='disabled'
            )
            gui_instance.subtype_proportions_btn.pack(side='left')
            LayoutUtils._add_tooltip(gui_instance, gui_instance.subtype_proportions_btn, "Subtype proportions within selected cluster\nShows distribution of subtypes in the winning cluster")
            
            # Store overall analysis plot buttons for enabling/disabling
            gui_instance.analysis_plot_buttons = [
                gui_instance.cluster_summary_btn, gui_instance.gmm_btn, 
                gui_instance.redshift_age_btn, gui_instance.subtype_proportions_btn
            ]
            
            # Store template-specific navigation buttons (now includes up/down buttons)
            gui_instance.nav_buttons = [gui_instance.prev_btn, gui_instance.next_btn, gui_instance.up_btn, gui_instance.down_btn]
            gui_instance.template_buttons = []  # No template-specific buttons needed
            
            # Connect view style changes to plot updates
            gui_instance.view_style.trace('w', gui_instance._on_view_style_change)
            
            # Plot area - reduced padding to maximize plot space
            plot_frame = tk.Frame(center_panel, bg=gui_instance.theme_manager.get_color('bg_primary'))
            plot_frame.pack(fill='both', expand=True, padx=5, pady=5)
            
            # Initialize matplotlib plot
            gui_instance.init_matplotlib_plot_area = plot_frame  # Store reference for later initialization
            
            _LOGGER.info("✅ Center panel created successfully with plot control buttons")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error creating center panel: {e}")
            import traceback
            traceback.print_exc()
    
    @staticmethod
    def create_right_panel(gui_instance, parent):
        """Create right panel with overall analysis plots"""
        try:
            # Right panel for overall analysis tools
            right_panel = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'), width=140,
                                  highlightbackground=gui_instance.theme_manager.get_color('border'),
                                  highlightthickness=1, relief='flat')
            right_panel.pack(side='right', fill='y', padx=(5, 5))
            right_panel.pack_propagate(False)
            
            # Header for analysis plots
            analysis_header = tk.Label(right_panel, text="📊 Overall Analysis",
                                     font=('Segoe UI', 14, 'bold'),
                                     bg=gui_instance.theme_manager.get_color('bg_secondary'),
                                     fg=gui_instance.theme_manager.get_color('text_primary'))
            analysis_header.pack(pady=(10, 15))
            
            # Analysis plots section
            analysis_frame = tk.Frame(right_panel, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            analysis_frame.pack(fill='x', padx=8)
            
            # Analysis results button
            gui_instance.cluster_summary_btn = create_cross_platform_button(
                analysis_frame, 
                text="📋 Analysis Results",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.show_cluster_summary() if hasattr(gui_instance, 'show_cluster_summary') else None,
                state='disabled'
            )
            # Override pady for right panel buttons (keep raised relief)
            gui_instance.cluster_summary_btn.config(pady=8, relief='raised', bd=2)
            gui_instance.cluster_summary_btn.pack(fill='x', pady=(5, 5))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.cluster_summary_btn, "Comprehensive analysis results summary\nShows classification, redshift, age estimates, and template details")
            
            # GMM clustering button
            gui_instance.gmm_btn = create_cross_platform_button(
                analysis_frame, 
                text="🔮 GMM Clustering",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.plot_gmm_clustering() if hasattr(gui_instance, 'plot_gmm_clustering') else None,
                state='disabled'
            )
            # Override pady for right panel buttons (keep raised relief)
            gui_instance.gmm_btn.config(pady=8, relief='raised', bd=2)
            gui_instance.gmm_btn.pack(fill='x', pady=(5, 5))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.gmm_btn, "Type-specific GMM clustering with 3D visualization\nRedshift vs Type vs RLAP")
            
            # Redshift vs age button
            gui_instance.redshift_age_btn = create_cross_platform_button(
                analysis_frame, 
                text="📈 Redshift vs Age",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.plot_redshift_age() if hasattr(gui_instance, 'plot_redshift_age') else None,
                state='disabled'
            )
            # Override pady for right panel buttons (keep raised relief)
            gui_instance.redshift_age_btn.config(pady=8, relief='raised', bd=2)
            gui_instance.redshift_age_btn.pack(fill='x', pady=(5, 5))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.redshift_age_btn, "Redshift vs Age distribution analysis")
            
            # Subtype proportions button
            gui_instance.subtype_proportions_btn = create_cross_platform_button(
                analysis_frame, 
                text="🥧 Subtype Proportions",
                font=('Segoe UI', 12, 'bold'),
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                command=lambda: gui_instance.plot_subtype_proportions() if hasattr(gui_instance, 'plot_subtype_proportions') else None,
                state='disabled'
            )
            # Override pady for right panel buttons (keep raised relief)
            gui_instance.subtype_proportions_btn.config(pady=8, relief='raised', bd=2)
            gui_instance.subtype_proportions_btn.pack(fill='x', pady=(5, 0))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.subtype_proportions_btn, "Subtype proportions within selected cluster\nShows distribution of subtypes in the winning cluster")
            

            
            # Store overall analysis plot buttons for enabling/disabling
            gui_instance.analysis_plot_buttons = [
                gui_instance.cluster_summary_btn, gui_instance.gmm_btn, 
                gui_instance.redshift_age_btn, gui_instance.subtype_proportions_btn
            ]
            
            # Add flexible spacer to push settings button to bottom
            spacer_frame = tk.Frame(right_panel, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            spacer_frame.pack(fill='both', expand=True)
            
            # Settings section at the bottom
            settings_frame = tk.Frame(right_panel, bg=gui_instance.theme_manager.get_color('bg_secondary'))
            settings_frame.pack(fill='x', side='bottom', padx=8, pady=(0, 10))
            
            # Settings button
            gui_instance.settings_btn = create_cross_platform_button(
                settings_frame, 
                text="⚙️ Settings",
                font=('Segoe UI', 10, 'bold'),
                command=lambda: gui_instance._open_settings_dialog() if hasattr(gui_instance, '_open_settings_dialog') else None,
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                cursor='hand2'
            )
            # Override pady for settings buttons (keep raised relief)
            gui_instance.settings_btn.config(pady=6, relief='raised', bd=2)
            gui_instance.settings_btn.pack(side='left', fill='both', expand=True, padx=(0, 2))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.settings_btn, 
                                   "Open GUI settings dialog\nConfigure fonts, themes, display options")
            
            # Reset button
            gui_instance.reset_btn = create_cross_platform_button(
                settings_frame, 
                text="🔄 Reset",
                font=('Segoe UI', 10, 'bold'),
                command=lambda: gui_instance.reset_gui_to_initial_state() if hasattr(gui_instance, 'reset_gui_to_initial_state') else None,
                bg=gui_instance.theme_manager.get_color('button_bg'),
                fg='white',
                relief='raised',
                bd=2,
                padx=12,
                pady=6,
                cursor='hand2'
            )
            # Override pady for settings buttons (keep raised relief)
            gui_instance.reset_btn.config(pady=6, relief='raised', bd=2)
            gui_instance.reset_btn.pack(side='left', fill='both', expand=True, padx=(2, 0))
            LayoutUtils._add_tooltip(gui_instance, gui_instance.reset_btn, 
                                    "Reset GUI to initial state\nClears all data, plots, and analysis results\nKeeps theme and settings unchanged")
            
            _LOGGER.info("✅ Right panel created successfully with overall analysis plots and settings button")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error creating right panel: {e}")
            import traceback
            traceback.print_exc()
    
    # Private helper methods for creating sections
    
    @staticmethod
    def _create_load_section(gui_instance, parent):
        """Create load spectrum section"""
        load_frame = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        load_frame.pack(fill='x', pady=(0, 6))
        
        # Get platform-specific font size for Linux
        try:
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            is_linux = platform_config and platform_config.is_linux
            button_font_size = 13 if is_linux else 14  # Smaller font for Linux
        except:
            button_font_size = 14
        
        # File selection button - Always enabled, always grey
        gui_instance.load_btn = create_cross_platform_button(
            load_frame, 
            text="📁 Load Spectrum File",
            font=('Segoe UI', button_font_size, 'bold'),
            command=lambda: gui_instance.file_controller.browse_file() if hasattr(gui_instance, 'file_controller') else None,
            bg=gui_instance.theme_manager.get_color('button_bg'),
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        gui_instance.load_btn.config(pady=14)
        gui_instance.load_btn.pack(fill='x', pady=(0, 6))
        

        
        # File status display
        gui_instance.file_status_label = tk.Label(
            load_frame,
            text="No spectrum loaded",
            font=('Segoe UI', 12, 'italic'),
            bg=gui_instance.theme_manager.get_color('bg_secondary'),
            fg=gui_instance.theme_manager.get_color('text_secondary')
        )
        gui_instance.file_status_label.pack(anchor='w', pady=(2, 0))
    
    @staticmethod
    def _create_galaxy_analysis_section(gui_instance, parent):
        """Create galaxy analysis section with unified redshift selection"""
        galaxy_frame = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        galaxy_frame.pack(fill='x', pady=(6, 6))
        
        # Get platform-specific font size for Linux
        try:
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            is_linux = platform_config and platform_config.is_linux
            button_font_size = 13 if is_linux else 14  # Smaller font for Linux
        except:
            button_font_size = 14
        
        # Galaxy analysis buttons row
        galaxy_row = tk.Frame(galaxy_frame, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        galaxy_row.pack(fill='x', pady=(0, 0))  # Keep container flush; button controls spacing
        
        # Combined Redshift Selection button
        gui_instance.redshift_selection_btn = create_cross_platform_button(
            galaxy_row, 
            text="🌌 Redshift Selection",
            font=('Segoe UI', button_font_size, 'bold'),
            command=gui_instance.open_redshift_selection,
            bg=gui_instance.theme_manager.get_color('button_bg'),
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        gui_instance.redshift_selection_btn.config(pady=14)
        gui_instance.redshift_selection_btn.pack(fill='x', pady=(0, 6), expand=True)
        

        
        # Redshift status display - similar to file status label
        gui_instance.redshift_status_label = tk.Label(
            galaxy_frame,
            text="Optional: no redshift selected",
            font=('Segoe UI', 12, 'italic'),
            bg=gui_instance.theme_manager.get_color('bg_secondary'),
            fg=gui_instance.theme_manager.get_color('text_secondary')
        )
        gui_instance.redshift_status_label.pack(anchor='w', pady=(2, 0))
        
        # Add tooltip to redshift button
        LayoutUtils._add_tooltip(gui_instance, gui_instance.redshift_selection_btn, 
                                "Redshift determination - automatic detection or manual identification\n"
                                "Will constrain SNID search range around determined redshift")
        LayoutUtils._add_tooltip(gui_instance, gui_instance.redshift_status_label,
                                "Shows current galaxy redshift status\n"
                                "When set, SNID analysis will search in tight range around this redshift")
        
        
    
    @staticmethod
    def _create_preprocessing_section(gui_instance, parent):
        """Create preprocessing section"""
        preprocess_frame = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        preprocess_frame.pack(fill='x', pady=(6, 6))
        
        # Get platform-specific font size for Linux
        try:
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            is_linux = platform_config and platform_config.is_linux
            button_font_size = 13 if is_linux else 14  # Smaller font for Linux
        except:
            button_font_size = 14
        
        # Single Preprocessing button
        gui_instance.preprocess_btn = create_cross_platform_button(
            preprocess_frame, 
            text="🔧 Preprocess Spectrum",
            font=('Segoe UI', button_font_size, 'bold'),
            command=gui_instance.open_preprocessing_selection,
            bg=gui_instance.theme_manager.get_color('button_bg'),
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        gui_instance.preprocess_btn.config(pady=14)
        gui_instance.preprocess_btn.pack(fill='x', pady=(0, 6))
        
        # Right-click shortcut: run quick preprocessing immediately if the button is active
        gui_instance.preprocess_btn.bind(
            '<Button-3>',
            lambda event: gui_instance.preprocessing_controller.run_quick_snid_preprocessing_silent()
            if gui_instance.preprocess_btn.cget('state') == 'normal' and hasattr(gui_instance, 'preprocessing_controller') else None
        )
        
        # Tooltip describing action and shortcut
        LayoutUtils._add_tooltip(
            gui_instance,
            gui_instance.preprocess_btn,
            "Run preprocessing on the loaded spectrum.\nRight-click to launch quick preprocessing with default settings."
        )
        
        # Status label below preprocessing button – shows ✔ when preprocessing done
        gui_instance.preprocess_status_label = tk.Label(
            preprocess_frame,
            text="Not preprocessed",
            font=('Segoe UI', 12, 'italic'),
            bg=gui_instance.theme_manager.get_color('bg_secondary'),
            fg=gui_instance.theme_manager.get_color('text_secondary'),
        )
        gui_instance.preprocess_status_label.pack(anchor='w', pady=(2, 0))
    
    @staticmethod
    def _create_configuration_section(gui_instance, parent):
        """Create configuration section - now combined with analysis"""
        # Get platform-specific font size for Linux
        try:
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            is_linux = platform_config and platform_config.is_linux
            button_font_size = 13 if is_linux else 14  # Smaller font for Linux
        except:
            button_font_size = 14
        
        # Single Analysis button - no header, pushed higher
        gui_instance.analysis_btn = create_cross_platform_button(
            parent, 
            text="🚀 Run Analysis",
            font=('Segoe UI', button_font_size, 'bold'),
            command=gui_instance.open_snid_analysis_dialog,
            bg=gui_instance.theme_manager.get_color('button_bg'),
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        gui_instance.analysis_btn.config(pady=14)
        gui_instance.analysis_btn.pack(fill='x', pady=(0, 6))
        
        # Right-click shortcut: run SNID analysis immediately if the button is active
        gui_instance.analysis_btn.bind(
            '<Button-3>',
            lambda event: gui_instance.analysis_controller.run_snid_analysis_only()
            if gui_instance.analysis_btn.cget('state') == 'normal' and hasattr(gui_instance, 'analysis_controller') else None
        )
        
        # Add tooltip for analysis button with right-click info
        LayoutUtils._add_tooltip(
            gui_instance,
            gui_instance.analysis_btn,
            "Run full SNID-SAGE analysis on the preprocessed spectrum.\nRight-click to start analysis immediately using current parameters."
        )
        
        # Configuration status indicator (stacked vertically under the button)
        status_frame = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        status_frame.pack(fill='x', pady=(0, 6))

        # Primary configuration status (shows check-mark when analysis dialog opened)
        gui_instance.config_status_label = tk.Label(
            status_frame,
            text="",  # Initially blank until preprocessing is done
            font=('Segoe UI', 12, 'italic'),
            bg=gui_instance.theme_manager.get_color('bg_secondary'),
            fg=gui_instance.theme_manager.get_color('text_secondary')
        )
        gui_instance.config_status_label.pack(anchor='w')

    

    

    
    @staticmethod
    def _create_emission_line_section(gui_instance, parent):
        """Create emission line overlay section"""
        # Get platform-specific font size for Linux
        try:
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            is_linux = platform_config and platform_config.is_linux
            button_font_size = 13 if is_linux else 14  # Smaller font for Linux
        except:
            button_font_size = 14
        
        # Emission line overlay button – uniform spacing like other workflow buttons
        gui_instance.emission_line_overlay_btn = create_cross_platform_button(
            parent, 
            text="🔬 SN Emission Line Analysis",
            font=('Segoe UI', button_font_size, 'bold'),
            command=gui_instance.open_emission_line_overlay,
            bg=gui_instance.theme_manager.get_color('button_bg'),
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        gui_instance.emission_line_overlay_btn.config(pady=14)
        gui_instance.emission_line_overlay_btn.pack(fill='x', pady=(0, 6))
        
        # Status label for emission-line analysis (initially idle)
        gui_instance.emission_status_label = tk.Label(
            parent,
            text="Not analyzed",
            font=('Segoe UI', 12, 'italic'),
            bg=gui_instance.theme_manager.get_color('bg_secondary'),
            fg=gui_instance.theme_manager.get_color('text_secondary')
        )
        gui_instance.emission_status_label.pack(anchor='w', pady=(2, 0))
    
    @staticmethod
    def _create_chat_section(gui_instance, parent):
        """Create chat with AI section"""
        # Get platform-specific font size for Linux
        try:
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            is_linux = platform_config and platform_config.is_linux
            button_font_size = 13 if is_linux else 14  # Smaller font for Linux
        except:
            button_font_size = 14
        
        # Uniform spacing for chat section
        chat_frame = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        chat_frame.pack(fill='x', pady=(6, 6))
        
        # Enhanced AI assistant button (enabled after analysis completes)
        gui_instance.ai_assistant_btn = create_cross_platform_button(
            chat_frame,
            text="🤖 AI Assistant",
            font=('Segoe UI', button_font_size, 'bold'),
            command=lambda: gui_instance._show_enhanced_ai_assistant() if hasattr(gui_instance, '_show_enhanced_ai_assistant') else None,
            bg=gui_instance.theme_manager.get_color('button_bg'),
            fg='white',
            relief='raised',
            bd=2,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        gui_instance.ai_assistant_btn.config(pady=14)
        gui_instance.ai_assistant_btn.pack(fill='x', pady=(0, 6))
        
        # Backwards compatibility: provide old attribute name if referenced elsewhere
        gui_instance.chat_with_ai_btn = gui_instance.ai_assistant_btn

        # Status / description label under AI assistant button
        gui_instance.ai_status_label = tk.Label(
            chat_frame,
            text="Summary • Chat • TNS Reports",
            font=('Segoe UI', 9),
            bg=gui_instance.theme_manager.get_color('bg_secondary'),
            fg=gui_instance.theme_manager.get_color('text_secondary')
        )
        gui_instance.ai_status_label.pack(anchor='w', pady=(2, 10))
        
        # Backwards-compatibility alias so existing helper functions can update it
        description_label = gui_instance.ai_status_label  # legacy reference

    
    @staticmethod
    def _create_separator(gui_instance, parent):
        """Create a visual separator"""
        separator = tk.Frame(parent, height=2, bg=gui_instance.theme_manager.get_color('border'))
        separator.pack(fill='x', pady=(3, 3))

    @staticmethod
    def _add_tooltip(gui_instance, widget, text):
        """Add tooltip to a widget"""
        try:
            def on_enter(event):
                # Create tooltip window
                tooltip = tk.Toplevel()
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{event.x_root+20}+{event.y_root+10}")
                
                # Increased font size for better readability
                label = tk.Label(tooltip, text=text, 
                               font=('Segoe UI', 11, 'normal'),
                               bg='#f0f0f0', fg='black',
                               relief='solid', bd=1, padx=5, pady=2)
                label.pack()
                
                widget.tooltip = tooltip
            
            def on_leave(event):
                # Destroy tooltip when mouse leaves
                if hasattr(widget, 'tooltip') and widget.tooltip:
                    try:
                        widget.tooltip.destroy()
                        widget.tooltip = None
                    except:
                        pass
            
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            
        except Exception as e:
            _LOGGER.warning(f"Warning: Could not add tooltip: {e}")

    @staticmethod
    def update_config_display(gui_instance):
        """Update the configuration display with current effective parameters"""
        try:
            # quick_config_label removed – nothing to update
            return
            
            # Get effective redshift range
            zmin_eff, zmax_eff, is_manual = gui_instance.get_effective_redshift_range()
            max_templates = gui_instance._safe_int(gui_instance.params.get('max_output_templates', ''), 10)
            
            # Create display text
            if is_manual:
                config_text = f"z: {zmin_eff:.3f} to {zmax_eff:.3f} (manual) | Templates: {max_templates}"
                text_color = gui_instance.theme_manager.get_color('success')
            else:
                config_text = f"z: {zmin_eff:.2f} to {zmax_eff:.1f} | Templates: {max_templates}"
                text_color = gui_instance.theme_manager.get_color('text_muted')
            
            gui_instance.quick_config_label.configure(text=config_text, fg=text_color)
            
        except Exception as e:
            if hasattr(gui_instance, 'logger'):
                gui_instance.logger.debug(f"Error updating config display: {e}")


class ToggleUtils:
    """Utilities for creating toggle switches and controls"""
    
    @staticmethod
    def create_toggle_switch(gui_instance, parent, text, variable, callback=None):
        """Create a modern toggle switch"""
        container = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=4)
        
        # Label
        tk.Label(container, text=text,
                font=('Segoe UI', 12, 'normal'),
                bg=gui_instance.theme_manager.get_color('bg_secondary'),
                fg=gui_instance.theme_manager.get_color('text_primary')).pack(side='left')
        
        # Toggle switch frame
        toggle_frame = tk.Frame(container, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        toggle_frame.pack(side='right')
        
        # Store the variable
        gui_instance.toggle_states[text] = variable
        
        # Toggle background
        bg_color = gui_instance.theme_manager.get_color('accent_primary') if variable.get() else gui_instance.theme_manager.get_color('disabled')
        toggle_bg = tk.Frame(toggle_frame, bg=bg_color, width=50, height=24)
        toggle_bg.pack()
        toggle_bg.pack_propagate(False)
        
        # Toggle handle
        handle_x = 26 if variable.get() else 2
        toggle_handle = tk.Frame(toggle_bg, bg='white', width=20, height=20)
        toggle_handle.place(x=handle_x, y=2)
        
        def toggle_click(event):
            current = variable.get()
            new_state = not current
            variable.set(new_state)
            
            # Animate toggle
            new_bg = gui_instance.theme_manager.get_color('accent_primary') if new_state else gui_instance.theme_manager.get_color('disabled')
            new_x = 26 if new_state else 2
            
            toggle_bg.configure(bg=new_bg)
            toggle_handle.place(x=new_x, y=2)
            
            if callback:
                callback(new_state)
        
        toggle_bg.bind('<Button-1>', toggle_click)
        toggle_handle.bind('<Button-1>', toggle_click)
        
        return container, variable
    
    @staticmethod
    def create_segmented_control(gui_instance, parent, options, variable):
        """Create a segmented control button group"""
        container = tk.Frame(parent, bg=gui_instance.theme_manager.get_color('bg_secondary'))
        container.pack(side='left', padx=(10, 0))
        
        # Get platform info for macOS-specific handling
        try:
            from snid_sage.shared.utils.config.platform_config import get_platform_config
            platform_config = get_platform_config()
            is_macos = platform_config and platform_config.is_macos
        except:
            is_macos = False
        
        buttons = []
        
        for i, option in enumerate(options):
            is_selected = variable.get() == option
            if is_selected:
                bg_color = gui_instance.theme_manager.get_color('accent_primary')  # Blue active state
                fg_color = 'white'
            else:
                # Inactive buttons appear white like default buttons
                bg_color = gui_instance.theme_manager.get_color('bg_secondary')  # White/neutral
                fg_color = gui_instance.theme_manager.get_color('text_secondary')
            
            if is_macos:
                # macOS-specific button creation for segmented control
                btn = tk.Button(container, text=option,
                               bg=bg_color, fg=fg_color,
                               font=('Segoe UI', 12, 'normal'),
                               relief='raised', bd=2, padx=20, pady=8,
                               # Use highlightbackground for macOS color control
                               highlightbackground=bg_color,
                               highlightcolor=bg_color,
                               highlightthickness=0,
                               # Override system appearance
                               borderwidth=2,
                               compound='none',
                               cursor='hand2')
            else:
                # Windows/Linux button creation (original)
                btn = tk.Button(container, text=option,
                               bg=bg_color, fg=fg_color,
                               font=('Segoe UI', 12, 'normal'),
                               relief='raised', bd=2, padx=20, pady=8,
                               highlightbackground=BUTTON_COLORS['border'],
                               highlightcolor=BUTTON_COLORS['border'],
                               highlightthickness=1,
                               cursor='hand2')
            
            # Mark as workflow-managed so global theme re-application skips them
            btn._workflow_managed = True
            btn._workflow_button_name = f"view_style_{option.lower()}"
            
            def make_click_handler(option_text):
                def click_handler():
                    _LOGGER.info(f"🔄 Segmented control clicked: {option_text}")
                    _LOGGER.info(f"📊 Before setting: view_style = {variable.get()}")
                    variable.set(option_text)
                    _LOGGER.info(f"📊 After setting: view_style = {variable.get()}")
                    
                    # Update all buttons with platform-specific handling
                    for j, button in enumerate(buttons):
                        if options[j] == option_text:
                            if is_macos:
                                button.configure(
                                    bg=gui_instance.theme_manager.get_color('accent_primary'), 
                                    fg='white', 
                                    relief='raised', 
                                    bd=2,
                                    highlightbackground=gui_instance.theme_manager.get_color('accent_primary')
                                )
                            else:
                                button.configure(
                                    bg=gui_instance.theme_manager.get_color('accent_primary'), 
                                    fg='white', 
                                    relief='raised', 
                                    bd=2
                                )
                        else:
                            if is_macos:
                                button.configure(
                                    bg=gui_instance.theme_manager.get_color('bg_secondary'),
                                    fg=gui_instance.theme_manager.get_color('text_secondary'), 
                                    relief='raised', 
                                    bd=2,
                                    highlightbackground=gui_instance.theme_manager.get_color('bg_secondary')
                                )
                            else:
                                button.configure(
                                    bg=gui_instance.theme_manager.get_color('bg_secondary'),
                                    fg=gui_instance.theme_manager.get_color('text_secondary'), 
                                    relief='raised', 
                                    bd=2
                                )
                    
                    # Call the view style change handler
                    if hasattr(gui_instance, '_on_view_style_change'):
                        _LOGGER.info(f"🔄 Calling _on_view_style_change()")
                        gui_instance._on_view_style_change()
                    else:
                        _LOGGER.warning(f"❌ No _on_view_style_change method found!")
                
                return click_handler
            
            btn.configure(command=make_click_handler(option))
            btn.pack(side='left')
            buttons.append(btn)
        
        # Store buttons for external updates
        gui_instance.view_style_buttons = buttons
        gui_instance.view_style_options = options
        
        # Add method to update button states programmatically
        def update_segmented_control_buttons():
            """Update segmented control button appearances to match variable"""
            try:
                current_value = variable.get()
                _LOGGER.debug(f"🔄 Updating segmented control buttons for value: {current_value}")
                
                for j, button in enumerate(buttons):
                    if options[j] == current_value:
                        if is_macos:
                            button.configure(
                                bg=gui_instance.theme_manager.get_color('accent_primary'), 
                                fg='white', 
                                relief='raised', 
                                bd=2,
                                highlightbackground=gui_instance.theme_manager.get_color('accent_primary')
                            )
                        else:
                            button.configure(
                                bg=gui_instance.theme_manager.get_color('accent_primary'), 
                                fg='white', 
                                relief='raised', 
                                bd=2
                            )
                    else:
                        if is_macos:
                            button.configure(
                                bg=gui_instance.theme_manager.get_color('bg_secondary'),
                                fg=gui_instance.theme_manager.get_color('text_secondary'), 
                                relief='raised', 
                                bd=2,
                                highlightbackground=gui_instance.theme_manager.get_color('bg_secondary')
                            )
                        else:
                            button.configure(
                                bg=gui_instance.theme_manager.get_color('bg_secondary'),
                                fg=gui_instance.theme_manager.get_color('text_secondary'), 
                                relief='raised', 
                                bd=2
                            )
                
                _LOGGER.debug(f"✅ Segmented control buttons updated for: {current_value}")
                
            except Exception as e:
                _LOGGER.error(f"❌ Error updating segmented control buttons: {e}")
        
        # Store the update function in the GUI instance
        gui_instance._update_segmented_control_buttons = update_segmented_control_buttons
        
        return container


# Legacy workflow functions - now handled by improved_button_workflow.py 
