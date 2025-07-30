"""
Shortcuts Dialog for SNID SAGE GUI
==================================

This module provides a dialog to display keyboard shortcuts and hotkeys
available in the SNID SAGE GUI interface.
"""

import tkinter as tk
from tkinter import ttk
import platform

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.shortcuts_dialog')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.shortcuts_dialog')


class ShortcutsDialog:
    """Dialog to display keyboard shortcuts"""
    
    def __init__(self, parent, theme_manager):
        """Initialize shortcuts dialog"""
        self.parent = parent
        self.theme_manager = theme_manager
        self.dialog = None
        self.is_mac = platform.system() == "Darwin"
        
        # Get platform-specific shortcuts
        try:
            from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            self.shortcuts = CrossPlatformWindowManager.get_keyboard_shortcuts()
        except ImportError:
            self.shortcuts = self._get_default_shortcuts()
    
    def _get_default_shortcuts(self):
        """Get default shortcuts if cross-platform manager unavailable"""
        if self.is_mac:
            return {
                'quick_workflow': 'Cmd+Enter',
                'quit': 'Cmd+Q',
                'copy': 'Cmd+C',
                'paste': 'Cmd+V'
            }
        else:  # Windows/Linux
            return {
                'quick_workflow': 'Ctrl+Enter',
                'quit': 'Ctrl+Q',
                'copy': 'Ctrl+C',
                'paste': 'Ctrl+V'
            }
    
    def _get_platform_modifier(self):
        """Get the platform-specific modifier key text"""
        return "Cmd" if self.is_mac else "Ctrl"
    
    def _get_platform_alt(self):
        """Get the platform-specific alt key text"""
        return "Option" if self.is_mac else "Alt"
    
    def show(self):
        """Show the shortcuts dialog"""
        try:
            # Create dialog window as a proper OS window
            self.dialog = tk.Toplevel(self.parent)
            self.dialog.title("SNID SAGE - Keyboard Shortcuts")
            self.dialog.geometry("750x550")  # Reduced size to better fit content
            self.dialog.resizable(True, True)
            
            # Set minimum size to prevent squashing
            self.dialog.minsize(650, 400)
            
            # Set icon and make it a proper window (not modal)
            try:
                self.dialog.iconbitmap(default=None)  # Use default icon
            except:
                pass
            
            # Don't make it modal - let it be a proper independent window
            self.dialog.transient(self.parent)
            
            # Configure dialog styling
            self.dialog.configure(bg=self.theme_manager.get_color('bg_primary'))
            
            # Create main frame with reduced padding
            main_frame = tk.Frame(self.dialog, bg=self.theme_manager.get_color('bg_primary'), padx=20, pady=15)
            main_frame.pack(fill='both', expand=True)

            
            # Create table-style shortcuts display
            self._create_shortcuts_table(main_frame)
            
            # Center dialog on parent
            self._center_dialog()
            
            # Bind escape key to close
            self.dialog.bind('<Escape>', lambda e: self.close())
            
            # Focus dialog
            self.dialog.focus_set()
            
            _LOGGER.info("✅ Shortcuts dialog opened")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error creating shortcuts dialog: {e}")
            if self.dialog:
                self.dialog.destroy()
    


    def _create_shortcuts_table(self, main_frame):
        """Create table-style shortcuts display with improved formatting"""
        
        mod_key = self._get_platform_modifier()
        alt_key = self._get_platform_alt()
        
        # Define shortcuts data organized by category with OS-aware shortcuts
        shortcuts_data = [
            {
                "category": "🚀 QUICK WORKFLOW",
                "shortcuts": [
                    {"action": "Open Spectrum", "shortcut": f"{mod_key}+O", "description": "Load spectrum file"},
                    {"action": "Quick Analysis", "shortcut": f"{mod_key}+Enter", "description": "Auto-preprocess + analyze spectrum"},
                    {"action": "Reset", "shortcut": f"{mod_key}+R", "description": "Reset all analysis and plots"}
                ]
            },
            {
                "category": "🧭 TEMPLATE NAVIGATION",
                "shortcuts": [
                    {"action": "Previous Template", "shortcut": "← (Left Arrow)", "description": "Go to previous template"},
                    {"action": "Next Template", "shortcut": "→ (Right Arrow)", "description": "Go to next template"},
                    {"action": "Cycle View Up", "shortcut": "↑ (Up Arrow)", "description": "Switch display up"},
                    {"action": "Cycle View Down", "shortcut": "↓ (Down Arrow)", "description": "Switch display down"},
                    {"action": "Switch Mode", "shortcut": "Spacebar", "description": "Toggle view mode"}
                ]
            }
        ]
        
        # Create scrollable frame for all tables
        canvas = tk.Canvas(main_frame, bg=self.theme_manager.get_color('bg_primary'), 
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme_manager.get_color('bg_primary'))
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create tables for each category
        for category_data in shortcuts_data:
            self._create_category_table(scrollable_frame, category_data)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Tips section at the bottom
        tips_frame = tk.Frame(scrollable_frame, bg=self.theme_manager.get_color('bg_primary'))
        tips_frame.pack(fill='x', pady=(25, 10))
        
        mod_display = "Cmd" if self.is_mac else "Ctrl"
        tips_text = f"💡 TIPS: Start with {mod_display}+O to open a spectrum, then {mod_display}+Enter for quick analysis. Press Escape to close this dialog."
        
        tips_label = tk.Label(tips_frame, 
                             text=tips_text,
                             font=('Segoe UI', 14, 'italic'),
                             bg=self.theme_manager.get_color('bg_primary'),
                             fg=self.theme_manager.get_color('text_secondary'),
                             wraplength=700)  # Reduced wraplength for smaller window
        tips_label.pack(anchor='w')

    def _create_category_table(self, parent, category_data):
        """Create a well-formatted table for a specific category of shortcuts"""
        
        # Category header
        category_frame = tk.Frame(parent, bg=self.theme_manager.get_color('bg_primary'))
        category_frame.pack(fill='x', pady=(25, 15))
        
        category_label = tk.Label(category_frame, 
                                text=category_data["category"],
                                font=('Segoe UI', 18, 'bold'),
                                bg=self.theme_manager.get_color('bg_primary'),
                                fg=self.theme_manager.get_color('text_primary'))
        category_label.pack(anchor='w')
        
        # Main table frame with border
        table_frame = tk.Frame(parent, bg='#d1d5db', relief='solid', bd=1)
        table_frame.pack(fill='x', pady=(0, 15))
        
        # Configure grid for proper column alignment - adjusted for smaller window
        table_frame.columnconfigure(0, weight=2, minsize=180)  # Action column - reduced
        table_frame.columnconfigure(1, weight=1, minsize=130)  # Shortcut column - reduced
        table_frame.columnconfigure(2, weight=3, minsize=280)  # Description column - reduced
        
        # Header row with improved styling
        header_bg = '#374151'
        header_fg = 'white'
        headers = ["Action", "Shortcut", "Description"]
        
        for col, header in enumerate(headers):
            header_label = tk.Label(table_frame, 
                                  text=header,
                                  font=('Segoe UI', 16, 'bold'),
                                  bg=header_bg,
                                  fg=header_fg,
                                  anchor='w',
                                  padx=15,
                                  pady=12,
                                  relief='flat')
            header_label.grid(row=0, column=col, sticky='ew')
        
        # Data rows with alternating colors and improved spacing
        row_bg_colors = [self.theme_manager.get_color('bg_secondary'), '#f8fafc']
        
        for row_idx, shortcut in enumerate(category_data["shortcuts"]):
            bg_color = row_bg_colors[row_idx % 2]
            
            # Action column
            action_label = tk.Label(table_frame,
                                  text=shortcut["action"],
                                  font=('Segoe UI', 15),
                                  bg=bg_color,
                                  fg=self.theme_manager.get_color('text_primary'),
                                  anchor='w',
                                  padx=15,
                                  pady=10)
            action_label.grid(row=row_idx + 1, column=0, sticky='ew')
            
            # Shortcut column with highlighting
            shortcut_label = tk.Label(table_frame,
                                    text=shortcut["shortcut"],
                                    font=('Consolas', 14, 'bold'),
                                    bg='#fef3c7' if not self.is_mac else '#dbeafe',
                                    fg='#92400e' if not self.is_mac else '#1e40af',
                                    anchor='center',
                                    padx=10,
                                    pady=10,
                                    relief='solid',
                                    bd=1)
            shortcut_label.grid(row=row_idx + 1, column=1, sticky='ew', padx=5, pady=2)
            
            # Description column
            desc_label = tk.Label(table_frame,
                                text=shortcut["description"],
                                font=('Segoe UI', 15),
                                bg=bg_color,
                                fg=self.theme_manager.get_color('text_secondary'),
                                anchor='w',
                                padx=15,
                                pady=10,
                                wraplength=260)  # Reduced wraplength for smaller window
            desc_label.grid(row=row_idx + 1, column=2, sticky='ew')

    def _center_dialog(self):
        """Center dialog on parent window"""
        try:
            self.dialog.update_idletasks()
            
            # Get screen dimensions
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            
            # Get parent window position and size
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            # Use smaller dialog size
            dialog_width = 750
            dialog_height = 550
            
            # Calculate center position relative to parent
            x = parent_x + (parent_width - dialog_width) // 2
            y = parent_y + (parent_height - dialog_height) // 2
            
            # Ensure dialog stays on screen with margins
            x = max(50, min(x, screen_width - dialog_width - 50))
            y = max(50, min(y, screen_height - dialog_height - 50))
            
            self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Could not center shortcuts dialog: {e}")
    
    def close(self):
        """Close the dialog"""
        try:
            if self.dialog:
                self.dialog.destroy()
                self.dialog = None
                _LOGGER.info("✅ Shortcuts dialog closed")
        except Exception as e:
            _LOGGER.error(f"❌ Error closing shortcuts dialog: {e}") 