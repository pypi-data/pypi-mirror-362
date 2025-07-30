"""
SNID SAGE - GUI Helper Utilities
===============================

Collection of helper functions for GUI operations, data validation,
and common UI tasks.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from typing import Optional, List, Tuple, Dict, Any

# Import the centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.helpers')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.helpers')


class GUIHelpers:
    """Collection of helper methods for GUI operations"""
    
    @staticmethod
    def safe_float(value, default=0.0):
        """Safely convert value to float, return default if conversion fails
        
        Parameters:
        -----------
        value : any
            Value to convert to float
        default : float
            Default value to return if conversion fails
            
        Returns:
        --------
        float : Converted value or default
        """
        if value is None or value == '':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_int(value, default=0):
        """Safely convert value to int, return default if conversion fails
        
        Parameters:
        -----------
        value : any
            Value to convert to int
        default : int
            Default value to return if conversion fails
            
        Returns:
        --------
        int : Converted value or default
        """
        if value is None or value == '':
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_bool(value, default=False):
        """Safely convert value to bool, return default if conversion fails
        
        Parameters:
        -----------
        value : any
            Value to convert to bool
        default : bool
            Default value to return if conversion fails
            
        Returns:
        --------
        bool : Converted value or default
        """
        if value is None or value == '':
            return default
        try:
            if isinstance(value, str):
                return value.lower() in ('1', 'true', 'yes', 'on')
            return bool(int(value))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def filter_nonzero_spectrum(wave, flux, processed_spectrum=None):
        """Filter out zero-padded regions from spectrum data
        
        Uses the nonzero region boundaries calculated during preprocessing.
        
        Parameters:
        -----------
        wave : array
            Wavelength array
        flux : array  
            Flux array
        processed_spectrum : dict, optional
            Processed spectrum dictionary containing edge information
            
        Returns:
        --------
        tuple : (filtered_wave, filtered_flux)
            Arrays with zero-padded regions removed
        """
        try:
            # If we have processed spectrum with edge information, use it
            if processed_spectrum and 'left_edge' in processed_spectrum and 'right_edge' in processed_spectrum:
                left_edge = processed_spectrum['left_edge']
                right_edge = processed_spectrum['right_edge']
                return wave[left_edge:right_edge+1], flux[left_edge:right_edge+1]
            
            # Fallback: find nonzero regions manually
            nonzero_mask = flux > 0
            if np.any(nonzero_mask):
                left_edge = np.argmax(nonzero_mask)
                right_edge = len(flux) - 1 - np.argmax(nonzero_mask[::-1])
                return wave[left_edge:right_edge+1], flux[left_edge:right_edge+1]
            
            # If no nonzero data found, return original arrays
            return wave, flux
            
        except Exception as e:
            _LOGGER.warning(f"Warning: Error filtering nonzero spectrum: {e}")
            return wave, flux
    
    @staticmethod
    def center_window(window, width=None, height=None):
        """Center a window on the screen
        
        Parameters:
        -----------
        window : tk.Toplevel or tk.Tk
            Window to center
        width : int, optional
            Window width (uses current width if not specified)
        height : int, optional
            Window height (uses current height if not specified)
        """
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
            
            # Ensure window is not off-screen
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))
            
            window.geometry(f"{width}x{height}+{x}+{y}")
            
        except Exception as e:
            _LOGGER.warning(f"Warning: Could not center window: {e}")
    
    @staticmethod
    def create_tooltip(widget, text):
        """Create a simple tooltip for a widget
        
        Parameters:
        -----------
        widget : tk.Widget
            Widget to attach tooltip to
        text : str
            Tooltip text
        """
        def on_enter(event):
            try:
                tooltip = tk.Toplevel()
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                
                label = tk.Label(tooltip, text=text, 
                               background="lightyellow", 
                               relief="solid", borderwidth=1,
                               font=("Arial", 9))
                label.pack()
                
                widget.tooltip = tooltip
            except:
                pass
        
        def on_leave(event):
            try:
                if hasattr(widget, 'tooltip'):
                    widget.tooltip.destroy()
                    del widget.tooltip
            except:
                pass
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    @staticmethod
    def validate_numeric_input(value, min_val=None, max_val=None):
        """Validate numeric input and show error if invalid
        
        Parameters:
        -----------
        value : str
            Input value to validate
        min_val : float, optional
            Minimum allowed value
        max_val : float, optional
            Maximum allowed value
            
        Returns:
        --------
        tuple : (is_valid, converted_value)
            Whether input is valid and the converted numeric value
        """
        try:
            num_val = float(value)
            
            if min_val is not None and num_val < min_val:
                messagebox.showerror("Invalid Input", f"Value must be >= {min_val}")
                return False, None
            
            if max_val is not None and num_val > max_val:
                messagebox.showerror("Invalid Input", f"Value must be <= {max_val}")
                return False, None
            
            return True, num_val
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
            return False, None
    
    @staticmethod
    def show_info_dialog(title, message, details=None):
        """Show an information dialog with optional details
        
        Parameters:
        -----------
        title : str
            Dialog title
        message : str
            Main message
        details : str, optional
            Additional details to show in expandable section
        """
        if details:
            # Create custom dialog with details
            dialog = tk.Toplevel()
            dialog.title(title)
            dialog.geometry("400x300")
            GUIHelpers.center_window(dialog, 400, 300)
            dialog.transient()
            dialog.grab_set()
            
            # Main message
            msg_label = tk.Label(dialog, text=message, wraplength=350, justify='left')
            msg_label.pack(pady=10, padx=10)
            
            # Details section
            details_frame = tk.Frame(dialog)
            details_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
            
            details_text = tk.Text(details_frame, wrap='word', height=10)
            scrollbar = tk.Scrollbar(details_frame, orient='vertical', command=details_text.yview)
            details_text.configure(yscrollcommand=scrollbar.set)
            
            details_text.insert('1.0', details)
            details_text.configure(state='disabled')
            
            details_text.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # OK button
            ok_btn = tk.Button(dialog, text="OK", command=dialog.destroy)
            ok_btn.pack(pady=10)
            
        else:
            messagebox.showinfo(title, message)
    
    @staticmethod
    def create_progress_dialog(parent, title, message="Processing..."):
        """Create a simple progress dialog
        
        Parameters:
        -----------
        parent : tk.Widget
            Parent window
        title : str
            Dialog title
        message : str
            Initial message
            
        Returns:
        --------
        tuple : (dialog, progress_var, status_label)
            Dialog window, progress variable, and status label
        """
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("400x150")
        GUIHelpers.center_window(dialog, 400, 150)
        dialog.transient(parent)
        dialog.grab_set()
        
        # Message
        status_label = tk.Label(dialog, text=message, font=('Arial', 11))
        status_label.pack(pady=20)
        
        # Progress bar
        from tkinter import ttk
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(dialog, variable=progress_var, maximum=100)
        progress_bar.pack(pady=10, padx=20, fill='x')
        
        return dialog, progress_var, status_label
    
    @staticmethod
    def parse_wavelength_masks(mask_str):
        """Parse wavelength mask string into list of tuples
        
        Parameters:
        -----------
        mask_str : str
            String containing wavelength masks in various formats
            
        Returns:
        --------
        list : List of (start, end) tuples for wavelength ranges
        """
        try:
            if not mask_str or mask_str.strip() == '':
                return []
            
            masks = []
            # Split by commas or semicolons
            parts = mask_str.replace(';', ',').split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range format: "4000-5000"
                    range_parts = part.split('-')
                    if len(range_parts) == 2:
                        try:
                            start = float(range_parts[0].strip())
                            end = float(range_parts[1].strip())
                            if start < end:
                                masks.append((start, end))
                        except ValueError:
                            continue
                elif ':' in part:
                    # Alternative range format: "4000:5000"
                    range_parts = part.split(':')
                    if len(range_parts) == 2:
                        try:
                            start = float(range_parts[0].strip())
                            end = float(range_parts[1].strip())
                            if start < end:
                                masks.append((start, end))
                        except ValueError:
                            continue
            
            return masks
            
        except Exception as e:
            _LOGGER.warning(f"Warning: Error parsing wavelength masks: {e}")
            return []
    
    @staticmethod
    def format_wavelength_masks(masks):
        """Format wavelength masks list back to string
        
        Parameters:
        -----------
        masks : list
            List of (start, end) tuples
            
        Returns:
        --------
        str : Formatted mask string
        """
        try:
            if not masks:
                return ""
            
            mask_strings = []
            for start, end in masks:
                mask_strings.append(f"{start:.1f}-{end:.1f}")
            
            return ", ".join(mask_strings)
            
        except Exception as e:
            _LOGGER.warning(f"Warning: Error formatting wavelength masks: {e}")
            return ""
    
    @staticmethod
    def create_loading_indicator(parent):
        """Create a simple loading indicator
        
        Parameters:
        -----------
        parent : tk.Widget
            Parent widget
            
        Returns:
        --------
        tk.Label : Loading label widget
        """
        loading_label = tk.Label(parent, text="⏳ Loading...", 
                               font=('Arial', 12), fg='blue')
        return loading_label
    
    @staticmethod
    def animate_loading_text(label, base_text="Loading"):
        """Animate loading text with dots
        
        Parameters:
        -----------
        label : tk.Label
            Label to animate
        base_text : str
            Base text without dots
        """
        def update_dots():
            current_text = label.cget('text')
            if current_text.endswith('...'):
                label.configure(text=f"⏳ {base_text}")
            elif current_text.endswith('..'):
                label.configure(text=f"⏳ {base_text}...")
            elif current_text.endswith('.'):
                label.configure(text=f"⏳ {base_text}..")
            else:
                label.configure(text=f"⏳ {base_text}.")
            
            # Schedule next update
            label.after(500, update_dots)
        
        update_dots()
    
    @staticmethod
    def handle_exception(exception, context=""):
        """Handle exceptions with user-friendly error display
        
        Parameters:
        -----------
        exception : Exception
            Exception that occurred
        context : str
            Context where exception occurred
        """
        error_msg = str(exception)
        if context:
            full_msg = f"Error in {context}:\n\n{error_msg}"
        else:
            full_msg = f"An error occurred:\n\n{error_msg}"
        
        _LOGGER.error(f"❌ Exception: {full_msg}")
        messagebox.showerror("Error", full_msg) 
