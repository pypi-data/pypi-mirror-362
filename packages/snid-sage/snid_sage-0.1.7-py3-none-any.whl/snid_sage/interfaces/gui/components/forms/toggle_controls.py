"""
Toggle Controls Component for SNID GUI

This module handles all toggle switches, checkboxes, and boolean controls.
Extracted from the main GUI to improve modularity and maintainability.
"""

import tkinter as tk


class ToggleControlsComponent:
    """Handles all toggle switches and boolean controls"""
    
    def __init__(self, parent_gui):
        """Initialize the toggle controls component
        
        Args:
            parent_gui: Reference to the main GUI instance
        """
        self.parent_gui = parent_gui
        self.theme_manager = parent_gui.theme_manager
        
    def create_toggle_switch(self, parent, text, variable, callback=None):
        """Create a modern toggle switch
        
        Args:
            parent: Parent widget
            text (str): Label text for the toggle
            variable: Tkinter BooleanVar to bind to
            callback: Optional callback function when toggled
            
        Returns:
            tk.Frame: Container frame for the toggle
        """
        container = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=2)
        
        # Label
        label = tk.Label(container, text=text,
                        font=('Segoe UI', 11, 'normal'),
                        bg=self.theme_manager.get_color('bg_secondary'),
                        fg=self.theme_manager.get_color('text_primary'))
        label.pack(side='left')
        
        # Toggle switch frame
        toggle_frame = tk.Frame(container, bg=self.theme_manager.get_color('bg_secondary'))
        toggle_frame.pack(side='right')
        
        # Create the toggle switch
        toggle_switch = self._create_modern_toggle(toggle_frame, variable, callback)
        
        return container
    
    def _create_modern_toggle(self, parent, variable, callback=None):
        """Create a modern-looking toggle switch
        
        Args:
            parent: Parent widget
            variable: Tkinter BooleanVar
            callback: Optional callback function
            
        Returns:
            tk.Canvas: The toggle switch canvas
        """
        # Toggle dimensions
        width = 50
        height = 24
        
        # Create canvas for the toggle
        canvas = tk.Canvas(parent, width=width, height=height,
                          bg=self.theme_manager.get_color('bg_secondary'),
                          highlightthickness=0, relief='flat')
        canvas.pack()
        
        # Colors for toggle states
        off_color = self.theme_manager.get_color('bg_tertiary')
        on_color = self.theme_manager.get_color('accent_primary')
        handle_color = 'white'
        
        def update_toggle():
            """Update the visual state of the toggle"""
            canvas.delete("all")
            
            is_on = variable.get()
            bg_color = on_color if is_on else off_color
            handle_x = width - 12 if is_on else 12
            
            # Draw background rounded rectangle
            canvas.create_oval(2, 2, height-2, height-2, fill=bg_color, outline="")
            canvas.create_rectangle(height//2, 2, width-height//2, height-2, fill=bg_color, outline="")
            canvas.create_oval(width-height+2, 2, width-2, height-2, fill=bg_color, outline="")
            
            # Draw handle
            canvas.create_oval(handle_x-8, 4, handle_x+8, height-4, 
                             fill=handle_color, outline="", width=0)
        
        def toggle_state(event=None):
            """Toggle the state and update visuals"""
            variable.set(not variable.get())
            update_toggle()
            if callback:
                callback(variable.get())
        
        # Bind click event with Mac-specific improvements
        from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
        CrossPlatformWindowManager.setup_mac_event_bindings(
            canvas, 
            click_callback=toggle_state
        )
        canvas.bind("<Button-1>", toggle_state)  # Fallback for all platforms
        
        # Initial state
        update_toggle()
        
        # Trace variable changes
        variable.trace('w', lambda *args: update_toggle())
        
        return canvas
    
    def create_segmented_control(self, parent, options, variable):
        """Create a segmented control with multiple options
        
        Args:
            parent: Parent widget
            options (list): List of option strings
            variable: Tkinter StringVar
            
        Returns:
            tk.Frame: Container frame for the segmented control
        """
        from snid_sage.interfaces.gui.utils.layout_utils import create_cross_platform_button
        
        container = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=5)
        
        # Create buttons for each option
        buttons = []
        for i, option in enumerate(options):
            # Use cross-platform button creation for better macOS support
            btn = create_cross_platform_button(
                container, 
                text=option,
                font=('Segoe UI', 10, 'normal'),
                relief='flat', 
                bd=0, 
                padx=15, 
                pady=5,
                cursor='hand2',
                command=lambda opt=option: self._select_option(variable, opt, buttons)
            )
            btn.pack(side='left', padx=(0, 1) if i < len(options)-1 else 0)
            buttons.append(btn)
        
        # Update button styles based on selection
        def update_buttons():
            selected = variable.get()
            for i, btn in enumerate(buttons):
                if options[i] == selected:
                    bg_color = self.theme_manager.get_color('accent_primary')
                    fg_color = 'white'
                else:
                    bg_color = self.theme_manager.get_color('bg_tertiary')
                    fg_color = self.theme_manager.get_color('text_primary')
                
                # Apply colors with macOS compatibility
                btn.config(bg=bg_color, fg=fg_color)
                # For macOS, also set highlightbackground
                try:
                    btn.config(highlightbackground=bg_color)
                except:
                    pass
        
        # Initial update
        update_buttons()
        
        # Trace variable changes
        variable.trace('w', lambda *args: update_buttons())
        
        return container
    
    def _select_option(self, variable, option, buttons):
        """Select an option in a segmented control
        
        Args:
            variable: Tkinter StringVar
            option (str): Selected option
            buttons (list): List of button widgets
        """
        variable.set(option)
    
    def create_chip_buttons(self, parent, chip_vars):
        """Create chip-style toggle buttons
        
        Args:
            parent: Parent widget
            chip_vars (dict): Dictionary of {label: BooleanVar}
            
        Returns:
            tk.Frame: Container frame for the chips
        """
        container = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=5)
        
        chips = {}
        for label, var in chip_vars.items():
            chip = self._create_chip_button(container, label, var)
            chips[label] = chip
        
        return container
    
    def _create_chip_button(self, parent, label, variable):
        """Create a single chip button
        
        Args:
            parent: Parent widget
            label (str): Chip label
            variable: Tkinter BooleanVar
            
        Returns:
            tk.Button: The chip button
        """
        from snid_sage.interfaces.gui.utils.layout_utils import create_cross_platform_button
        
        def toggle_chip():
            variable.set(not variable.get())
            update_chip_style()
        
        def update_chip_style():
            is_selected = variable.get()
            if is_selected:
                bg_color = self.theme_manager.get_color('accent_primary')
                fg_color = 'white'
            else:
                bg_color = self.theme_manager.get_color('bg_tertiary')
                fg_color = self.theme_manager.get_color('text_primary')
            
            # Apply colors with macOS compatibility
            chip.config(bg=bg_color, fg=fg_color)
            # For macOS, also set highlightbackground
            try:
                chip.config(highlightbackground=bg_color)
            except:
                pass
        
        # Use cross-platform button creation for better macOS support
        chip = create_cross_platform_button(
            parent, 
            text=label,
            font=('Segoe UI', 9, 'normal'),
            relief='flat', 
            bd=0, 
            padx=10, 
            pady=3,
            cursor='hand2', 
            command=toggle_chip
        )
        chip.pack(side='left', padx=(0, 5))
        
        # Initial style
        update_chip_style()
        
        # Trace variable changes
        variable.trace('w', lambda *args: update_chip_style())
        
        return chip
    
    def create_checkbox_group(self, parent, title, options, variables):
        """Create a group of checkboxes with a title
        
        Args:
            parent: Parent widget
            title (str): Group title
            options (list): List of option strings
            variables (list): List of BooleanVar objects
            
        Returns:
            tk.Frame: Container frame for the checkbox group
        """
        container = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=5)
        
        # Title
        if title:
            title_label = tk.Label(container, text=title,
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=self.theme_manager.get_color('bg_secondary'),
                                  fg=self.theme_manager.get_color('text_primary'))
            title_label.pack(anchor='w', pady=(0, 5))
        
        # Checkboxes
        for option, var in zip(options, variables):
            self._create_styled_checkbox(container, option, var)
        
        return container
    
    def _create_styled_checkbox(self, parent, text, variable):
        """Create a styled checkbox
        
        Args:
            parent: Parent widget
            text (str): Checkbox label
            variable: Tkinter BooleanVar
            
        Returns:
            tk.Frame: Container frame for the checkbox
        """
        container = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=1)
        
        # Custom checkbox using canvas
        checkbox_canvas = tk.Canvas(container, width=16, height=16,
                                   bg=self.theme_manager.get_color('bg_secondary'),
                                   highlightthickness=0, relief='flat')
        checkbox_canvas.pack(side='left', padx=(0, 8))
        
        # Label
        label = tk.Label(container, text=text,
                        font=('Segoe UI', 11, 'normal'),
                        bg=self.theme_manager.get_color('bg_secondary'),
                        fg=self.theme_manager.get_color('text_primary'))
        label.pack(side='left')
        
        def update_checkbox():
            """Update checkbox visual state"""
            checkbox_canvas.delete("all")
            
            # Draw checkbox background
            bg_color = (self.theme_manager.get_color('accent_primary') 
                       if variable.get() 
                       else self.theme_manager.get_color('bg_tertiary'))
            
            checkbox_canvas.create_rectangle(2, 2, 14, 14, 
                                           fill=bg_color, 
                                           outline=self.theme_manager.get_color('border'))
            
            # Draw checkmark if checked
            if variable.get():
                checkbox_canvas.create_line(4, 8, 7, 11, fill='white', width=2)
                checkbox_canvas.create_line(7, 11, 12, 5, fill='white', width=2)
        
        def toggle_checkbox(event=None):
            """Toggle checkbox state"""
            variable.set(not variable.get())
            update_checkbox()
        
        # Bind click events
        # Improved click handling for Mac
        CrossPlatformWindowManager.setup_mac_event_bindings(
            checkbox_canvas, 
            click_callback=toggle_checkbox
        )
        CrossPlatformWindowManager.setup_mac_event_bindings(
            label, 
            click_callback=toggle_checkbox
        )
        checkbox_canvas.bind("<Button-1>", toggle_checkbox)  # Fallback
        label.bind("<Button-1>", toggle_checkbox)  # Fallback
        
        # Initial state
        update_checkbox()
        
        # Trace variable changes
        variable.trace('w', lambda *args: update_checkbox())
        
        return container
    
    def create_radio_group(self, parent, title, options, variable):
        """Create a group of radio buttons
        
        Args:
            parent: Parent widget
            title (str): Group title
            options (list): List of option strings
            variable: Tkinter StringVar for selected option
            
        Returns:
            tk.Frame: Container frame for the radio group
        """
        container = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=5)
        
        # Title
        if title:
            title_label = tk.Label(container, text=title,
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=self.theme_manager.get_color('bg_secondary'),
                                  fg=self.theme_manager.get_color('text_primary'))
            title_label.pack(anchor='w', pady=(0, 5))
        
        # Radio buttons
        for option in options:
            self._create_styled_radio(container, option, variable)
        
        return container
    
    def _create_styled_radio(self, parent, text, variable):
        """Create a styled radio button
        
        Args:
            parent: Parent widget
            text (str): Radio button label
            variable: Tkinter StringVar
            
        Returns:
            tk.Frame: Container frame for the radio button
        """
        container = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        container.pack(fill='x', pady=1)
        
        # Custom radio button using canvas
        radio_canvas = tk.Canvas(container, width=16, height=16,
                                bg=self.theme_manager.get_color('bg_secondary'),
                                highlightthickness=0, relief='flat')
        radio_canvas.pack(side='left', padx=(0, 8))
        
        # Label
        label = tk.Label(container, text=text,
                        font=('Segoe UI', 11, 'normal'),
                        bg=self.theme_manager.get_color('bg_secondary'),
                        fg=self.theme_manager.get_color('text_primary'))
        label.pack(side='left')
        
        def update_radio():
            """Update radio button visual state"""
            radio_canvas.delete("all")
            
            # Draw radio button circle
            border_color = (self.theme_manager.get_color('accent_primary') 
                           if variable.get() == text 
                           else self.theme_manager.get_color('border'))
            
            radio_canvas.create_oval(2, 2, 14, 14, 
                                   outline=border_color, width=2,
                                   fill=self.theme_manager.get_color('bg_secondary'))
            
            # Draw inner circle if selected
            if variable.get() == text:
                radio_canvas.create_oval(5, 5, 11, 11, 
                                       fill=self.theme_manager.get_color('accent_primary'),
                                       outline="")
        
        def select_radio(event=None):
            """Select this radio button"""
            variable.set(text)
        
        # Bind click events
        # Improved click handling for Mac
        CrossPlatformWindowManager.setup_mac_event_bindings(
            radio_canvas, 
            click_callback=select_radio
        )
        CrossPlatformWindowManager.setup_mac_event_bindings(
            label, 
            click_callback=select_radio
        )
        radio_canvas.bind("<Button-1>", select_radio)  # Fallback
        label.bind("<Button-1>", select_radio)  # Fallback
        
        # Initial state
        update_radio()
        
        # Trace variable changes
        variable.trace('w', lambda *args: update_radio())
        
        return container 
