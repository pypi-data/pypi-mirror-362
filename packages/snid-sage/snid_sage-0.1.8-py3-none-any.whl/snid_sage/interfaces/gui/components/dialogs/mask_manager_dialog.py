"""
Mask Manager Dialog Component

This module handles the wavelength mask management dialog functionality including:
- Viewing current mask regions
- Adding new mask ranges
- Removing existing masks
- Interactive masking integration
- Save and load mask configurations

Extracted from sage_gui.py to improve maintainability and modularity.
"""

import tkinter as tk
from tkinter import messagebox


class MaskManagerDialog:
    """
    Handles the wavelength mask management dialog.
    
    This class provides a comprehensive interface for managing wavelength masks
    that are used to exclude specific spectral regions from analysis.
    """
    
    def __init__(self, gui_instance):
        """
        Initialize the mask manager dialog.
        
        Args:
            gui_instance: Reference to the main GUI instance for accessing
                         theme manager, mask regions, and other components
        """
        self.gui = gui_instance
        self.window = None
        self.entry = None
        self.listbox = None
    
    @property
    def theme_manager(self):
        """Access to the theme manager from the GUI"""
        return self.gui.theme_manager
    
    def show(self):
        """Open the mask management dialog"""
        try:
            # Create the dialog window
            self.window = tk.Toplevel(self.gui.master)
            self.window.title("Wavelength Mask Management")
            self.window.geometry("500x500")
            self.window.configure(bg=self.theme_manager.get_color('bg_secondary'))
            
            # Main frame
            main_frame = tk.Frame(self.window, bg=self.theme_manager.get_color('bg_secondary'))
            main_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Title
            tk.Label(main_frame, text="Wavelength Mask Management",
                    font=('Segoe UI', 16, 'bold'),
                    bg=self.theme_manager.get_color('bg_secondary'),
                    fg=self.theme_manager.get_color('text_primary')).pack(pady=(0, 15))
            
            # Current masks display
            tk.Label(main_frame, text="Current Mask Regions:",
                    font=('Segoe UI', 14, 'normal'),
                    bg=self.theme_manager.get_color('bg_secondary'),
                    fg=self.theme_manager.get_color('text_primary')).pack(anchor='w', pady=(0, 5))
            
            # Listbox for masks
            listbox_frame = tk.Frame(main_frame, bg=self.theme_manager.get_color('bg_secondary'))
            listbox_frame.pack(fill='both', expand=True, pady=(0, 15))
            
            self.listbox = tk.Listbox(listbox_frame, font=('Consolas', 12),
                                     bg=self.theme_manager.get_color('bg_tertiary'),
                                     fg=self.theme_manager.get_color('text_primary'))
            self.listbox.pack(side='left', fill='both', expand=True)
            
            scrollbar = tk.Scrollbar(listbox_frame, orient='vertical')
            scrollbar.pack(side='right', fill='y')
            self.listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.listbox.yview)
            
            # Update listbox with current masks
            self._update_mask_listbox()
            
            # Entry for new masks
            tk.Label(main_frame, text="Add Mask Range (format: start:end):",
                    font=('Segoe UI', 12, 'normal'),
                    bg=self.theme_manager.get_color('bg_secondary'),
                    fg=self.theme_manager.get_color('text_primary')).pack(anchor='w', pady=(0, 5))
            
            self.entry = tk.Entry(main_frame, font=('Segoe UI', 12),
                                 bg=self.theme_manager.get_color('bg_tertiary'),
                                 fg=self.theme_manager.get_color('text_primary'))
            self.entry.pack(fill='x', pady=(0, 10))
            
            # Interactive masking info
            interactive_info = tk.Label(main_frame, 
                                      text="💡 Tip: Use 'Interactive Select' button or right-click on plot → 'Toggle Interactive Masking' to select ranges by dragging",
                                      font=('Segoe UI', 10, 'italic'),
                                      bg=self.theme_manager.get_color('bg_secondary'),
                                      fg=self.theme_manager.get_color('text_muted'),
                                      wraplength=450,
                                      justify='left')
            interactive_info.pack(anchor='w', pady=(0, 10))
            
            # Create buttons
            self._create_buttons(main_frame)
            
            # Center the window
            self.window.transient(self.gui.master)
            
        except Exception as e:
            messagebox.showerror("Mask Management Error", f"Failed to open mask management: {str(e)}")
            print(f"Mask management error: {e}")
    
    def _create_buttons(self, parent):
        """Create the button interface for the dialog"""
        # Buttons - reorganized into two rows for better spacing
        button_frame = tk.Frame(parent, bg=self.theme_manager.get_color('bg_secondary'))
        button_frame.pack(fill='x', pady=(15, 0))
        
        # First row: Main mask operations
        button_row1 = tk.Frame(button_frame, bg=self.theme_manager.get_color('bg_secondary'))
        button_row1.pack(fill='x', pady=(0, 8))
        
        add_btn = tk.Button(button_row1, text="➕ Add Mask",
                          bg=self.theme_manager.get_color('accent_primary'), fg='white',
                          font=('Segoe UI', 12, 'normal'),
                          relief='flat', bd=0, pady=10, cursor='hand2',
                          command=self._add_mask_from_entry)
        add_btn.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        remove_btn = tk.Button(button_row1, text="🗑️ Remove Selected",
                             bg=self.theme_manager.get_color('danger'), fg='white',
                             font=('Segoe UI', 12, 'normal'),
                             relief='flat', bd=0, pady=10, cursor='hand2',
                             command=self._remove_selected_mask)
        remove_btn.pack(side='left', fill='x', expand=True, padx=(4, 8))
        
        clear_btn = tk.Button(button_row1, text="🧹 Clear All",
                            bg=self.theme_manager.get_color('warning'), fg='white',
                            font=('Segoe UI', 12, 'normal'),
                            relief='flat', bd=0, pady=10, cursor='hand2',
                            command=self._clear_all_masks)
        clear_btn.pack(side='left', fill='x', expand=True, padx=(4, 0))
        
        # Second row: Interactive and save operations
        button_row2 = tk.Frame(button_frame, bg=self.theme_manager.get_color('bg_secondary'))
        button_row2.pack(fill='x', pady=(0, 0))
        
        # Interactive masking button
        interactive_btn = tk.Button(button_row2, text="📐 Interactive Select",
                                  bg=self.theme_manager.get_color('active'), fg='white',
                                  font=('Segoe UI', 12, 'normal'),
                                  relief='flat', bd=0, pady=10, cursor='hand2',
                                  command=self._start_interactive_masking)
        interactive_btn.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        # Save and close button
        save_btn = tk.Button(button_row2, text="💾 Save & Close",
                           bg=self.theme_manager.get_color('success'), fg='white',
                           font=('Segoe UI', 12, 'bold'),
                           relief='flat', bd=0, pady=10, cursor='hand2',
                           command=self._save_and_close)
        save_btn.pack(side='left', fill='x', expand=True, padx=(4, 0))
    
    def _add_mask_from_entry(self):
        """Add mask from entry field"""
        try:
            mask_text = self.entry.get().strip()
            if ':' in mask_text:
                start, end = map(float, mask_text.split(':'))
                if start < end:
                    self.gui.mask_regions.append((start, end))
                    self._update_mask_listbox()
                    self.entry.delete(0, tk.END)
                    print(f"Added mask region: {start:.2f} - {end:.2f}")
                else:
                    messagebox.showerror("Invalid Range", "Start wavelength must be less than end wavelength.")
            else:
                messagebox.showerror("Invalid Format", "Please use format: start:end (e.g., 5500:5600)")
        except ValueError:
            messagebox.showerror("Invalid Values", "Please enter valid numerical wavelengths.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add mask: {str(e)}")
    
    def _remove_selected_mask(self):
        """Remove selected mask from list"""
        try:
            selection = self.listbox.curselection()
            if selection:
                index = selection[0]
                if 0 <= index < len(self.gui.mask_regions):
                    removed_mask = self.gui.mask_regions.pop(index)
                    self._update_mask_listbox()
                    print(f"Removed mask region: {removed_mask[0]:.2f} - {removed_mask[1]:.2f}")
            else:
                messagebox.showwarning("No Selection", "Please select a mask region to remove.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove mask: {str(e)}")
    
    def _clear_all_masks(self):
        """Clear all mask regions"""
        try:
            if self.gui.mask_regions:
                result = messagebox.askyesno("Clear All Masks", 
                                           f"Are you sure you want to clear all {len(self.gui.mask_regions)} mask regions?")
                if result:
                    self.gui.mask_regions.clear()
                    self._update_mask_listbox()
                    print("All mask regions cleared")
            else:
                messagebox.showinfo("No Masks", "No mask regions to clear.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear masks: {str(e)}")
    
    def _update_mask_listbox(self):
        """Update the listbox with current mask regions"""
        try:
            if self.listbox:
                self.listbox.delete(0, tk.END)
                for i, (start, end) in enumerate(self.gui.mask_regions):
                    self.listbox.insert(tk.END, f"{i+1:2d}. {start:7.2f} - {end:7.2f} Å")
        except Exception as e:
            print(f"Error updating mask listbox: {e}")
    
    def _start_interactive_masking(self):
        """Start interactive masking mode"""
        try:
            # Delegate to the main GUI's interactive masking functionality
            if hasattr(self.gui, 'start_interactive_masking_dialog'):
                self.gui.start_interactive_masking_dialog(self.window)
            else:
                # Fallback to basic interactive masking
                self.gui.toggle_interactive_masking()
                messagebox.showinfo("Interactive Masking", 
                                   "Interactive masking enabled. Click and drag on the plot to select regions to mask.\n"
                                   "Right-click on the plot to disable interactive masking.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start interactive masking: {str(e)}")
    
    def _save_and_close(self):
        """Save mask configuration and close dialog"""
        try:
            # Update the GUI's mask parameters
            if self.gui.mask_regions:
                # Convert mask regions to string format for SNID parameters
                mask_str = ','.join([f"{start:.2f}:{end:.2f}" for start, end in self.gui.mask_regions])
                self.gui.params['wavelength_masks'] = mask_str
                print(f"Saved {len(self.gui.mask_regions)} mask regions")
                
                # Update the GUI display if needed
                if hasattr(self.gui, 'update_plot_with_masks'):
                    self.gui.update_plot_with_masks()
            else:
                self.gui.params['wavelength_masks'] = ''
                print("No mask regions to save")
            
            # Update header status
            if hasattr(self.gui, 'update_header_status'):
                mask_count = len(self.gui.mask_regions)
                if mask_count > 0:
                    self.gui.update_header_status(f"🎭 {mask_count} mask region(s) applied")
                else:
                    self.gui.update_header_status("🎭 No mask regions active")
            
            # Close the dialog
            if self.window:
                self.window.destroy()
                
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save mask configuration: {str(e)}")
            print(f"Error saving masks: {e}") 
