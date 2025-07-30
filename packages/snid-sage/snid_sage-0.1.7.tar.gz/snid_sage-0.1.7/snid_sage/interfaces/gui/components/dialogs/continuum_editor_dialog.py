"""
Interactive Continuum Editor Dialog
===================================

A sophisticated dialog component for interactive continuum editing with dual-plot visualization.
Provides real-time editing of continuum fits with immediate visual feedback.

Features:
- Dual-plot layout (spectrum+continuum overlay, flattened spectrum preview)
- Interactive control points for continuum adjustment
- Real-time visual feedback
- Enhanced editing tools and view controls
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class InteractiveContinuumEditor:
    """
    Interactive continuum editor with dual-plot visualization
    
    This dialog provides a sophisticated interface for fine-tuning continuum fits
    with real-time visual feedback showing both the continuum overlay and the
    resulting flattened spectrum.
    """
    
    def __init__(self, wave, flux, initial_continuum, parent_dialog=None):
        """Initialize the interactive continuum editor"""
        self.wave = wave.copy()
        self.flux = flux.copy()  # This should be the spectrum BEFORE continuum fitting
        self.original_continuum = initial_continuum.copy()
        self.current_continuum = initial_continuum.copy()
        self.parent_dialog = parent_dialog
        
        # Control points for editing (start with a subset of wavelength points)
        self.n_control_points = min(20, len(wave) // 10)  # Reasonable number of control points
        self.control_indices = np.linspace(0, len(wave)-1, self.n_control_points, dtype=int)
        self.control_wave = wave[self.control_indices]
        self.control_continuum = initial_continuum[self.control_indices].copy()
        
        # Interaction state
        self.selected_point = None
        self.dragging = False
        
        # Create the editor window
        self.create_editor_window()
        
    def create_editor_window(self):
        """Create the interactive continuum editor window with dual plots"""
        self.window = tk.Toplevel()
        self.window.title("🎨 Interactive Continuum Editor - Dual View")
        self.window.geometry("1200x800")  # Larger for dual plots
        
        # Create matplotlib figure with dual plots layout
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(14, 10), 
                                                     gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.3})
        self.fig.suptitle("Interactive Continuum Editor - Dual View", fontsize=16, fontweight='bold')
        
        # Top plot: Original spectrum with editable continuum overlay
        self.ax1.plot(self.wave, self.flux, 'k-', alpha=0.8, linewidth=1, label='Spectrum')
        self.continuum_line, = self.ax1.plot(self.wave, self.current_continuum, 'r-', 
                                            linewidth=3, alpha=0.9, label='Fitted Continuum')
        self.control_points, = self.ax1.plot(self.control_wave, self.control_continuum, 'ro', 
                                           markersize=10, picker=True, markeredgecolor='darkred',
                                           markeredgewidth=2, label='Control Points (drag to edit)')
        
        self.ax1.set_xlabel('Wavelength (Å)', fontsize=12)
        self.ax1.set_ylabel('Flux', fontsize=12)
        self.ax1.set_title('📊 Spectrum with Continuum Overlay (drag red points to edit)', 
                          fontsize=14, fontweight='bold', pad=20)
        self.ax1.legend(loc='upper right', fontsize=10)
        self.ax1.grid(True, alpha=0.3)
        
        # Style the top plot
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.tick_params(axis='both', which='major', labelsize=10)
        
        # Bottom plot: Live flattened spectrum preview
        flattened = self.flux / self.current_continuum
        self.flattened_line, = self.ax2.plot(self.wave, flattened, 'b-', linewidth=2, 
                                           alpha=0.8, label='Flattened Spectrum')
        self.ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.7, linewidth=2, 
                        label='Unity Level')
        
        self.ax2.set_xlabel('Wavelength (Å)', fontsize=12)
        self.ax2.set_ylabel('Flattened Flux', fontsize=12)
        self.ax2.set_title('📈 Live Preview: Flattened Spectrum (updates as you edit)', 
                          fontsize=14, fontweight='bold', pad=20)
        self.ax2.legend(loc='upper right', fontsize=10)
        self.ax2.grid(True, alpha=0.3)
        
        # Style the bottom plot
        self.ax2.spines['top'].set_visible(False)
        self.ax2.spines['right'].set_visible(False)
        self.ax2.tick_params(axis='both', which='major', labelsize=10)
        
        # Set reasonable y-limits for flattened spectrum
        flat_mean = np.mean(flattened[np.isfinite(flattened)])
        flat_std = np.std(flattened[np.isfinite(flattened)])
        self.ax2.set_ylim(max(0, flat_mean - 3*flat_std), flat_mean + 3*flat_std)
        
        # Create canvas and toolbar in a frame structure
        canvas_frame = ttk.Frame(self.window)
        canvas_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.canvas = FigureCanvasTkAgg(self.fig, canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add navigation toolbar with enhanced styling
        toolbar_frame = ttk.Frame(canvas_frame)
        toolbar_frame.pack(fill='x', pady=(5, 0))
        
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Connect mouse events for interactivity
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        # Enhanced control buttons with better organization
        self.create_enhanced_control_panel()
        
        # Enhanced instructions with visual cues
        self.create_enhanced_instructions()
        
        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self.cancel_changes)
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the editor window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_enhanced_control_panel(self):
        """Create enhanced control panel with better organization"""
        # Main control frame with modern styling
        control_frame = ttk.Frame(self.window)
        control_frame.pack(fill='x', padx=15, pady=(10, 15))
        
        # Left side - editing tools
        left_frame = ttk.LabelFrame(control_frame, text="🔧 Editing Tools", padding=10)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        ttk.Button(left_frame, text="🔄 Reset to Original", 
                  command=self.reset_continuum, width=18).pack(pady=2)
        ttk.Button(left_frame, text="✨ Smooth Continuum", 
                  command=self.smooth_continuum, width=18).pack(pady=2)
        ttk.Button(left_frame, text="➕ Add Control Point", 
                  command=self.add_control_point, width=18).pack(pady=2)
        
        # Center frame - view tools
        center_frame = ttk.LabelFrame(control_frame, text="👁️ View Tools", padding=10)
        center_frame.pack(side='left', fill='y', padx=10)
        
        ttk.Button(center_frame, text="🔍 Auto Scale", 
                  command=self.auto_scale_plots, width=15).pack(pady=2)
        ttk.Button(center_frame, text="📊 Zoom to Data", 
                  command=self.zoom_to_data, width=15).pack(pady=2)
        
        # Right side - action buttons
        right_frame = ttk.LabelFrame(control_frame, text="💾 Actions", padding=10)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        
        ttk.Button(right_frame, text="✅ Apply Changes", 
                  command=self.apply_changes, width=15).pack(pady=2)
        ttk.Button(right_frame, text="❌ Cancel", 
                  command=self.cancel_changes, width=15).pack(pady=2)
                  
    def create_enhanced_instructions(self):
        """Create enhanced instructions with visual styling"""
        instruction_frame = ttk.LabelFrame(self.window, text="📖 Instructions", padding=10)
        instruction_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        instructions_text = (
            "🎯 Click and drag RED CONTROL POINTS on the top plot to modify the continuum fit\n"
            "👀 Watch the bottom plot update in real-time to see how changes affect the flattened spectrum\n"
            "🔧 Use editing tools to reset, smooth, or add new control points for fine-tuning\n"
            "💡 The goal is to achieve a flat baseline around 1.0 in the bottom plot"
        )
        
        instruction_label = ttk.Label(instruction_frame, text=instructions_text, 
                                    justify='left', wraplength=1000)
        instruction_label.pack(pady=5)
        
    def auto_scale_plots(self):
        """Auto-scale both plots to show data nicely"""
        # Auto-scale top plot
        self.ax1.relim()
        self.ax1.autoscale_view()
        
        # Auto-scale bottom plot with reasonable limits
        flattened = self.flux / self.current_continuum
        valid_flux = flattened[np.isfinite(flattened)]
        if len(valid_flux) > 0:
            flat_mean = np.mean(valid_flux)
            flat_std = np.std(valid_flux)
            self.ax2.set_ylim(max(0, flat_mean - 2*flat_std), flat_mean + 2*flat_std)
        
        self.canvas.draw_idle()
        
    def zoom_to_data(self):
        """Zoom to show the data range with some padding"""
        # Zoom top plot to data range
        wave_range = self.wave[-1] - self.wave[0]
        flux_range = np.max(self.flux) - np.min(self.flux)
        
        self.ax1.set_xlim(self.wave[0] - 0.02*wave_range, self.wave[-1] + 0.02*wave_range)
        self.ax1.set_ylim(np.min(self.flux) - 0.1*flux_range, np.max(self.flux) + 0.1*flux_range)
        
        # Zoom bottom plot to reasonable flattened range
        flattened = self.flux / self.current_continuum
        valid_flux = flattened[np.isfinite(flattened)]
        if len(valid_flux) > 0:
            self.ax2.set_xlim(self.wave[0] - 0.02*wave_range, self.wave[-1] + 0.02*wave_range)
            flat_min, flat_max = np.percentile(valid_flux, [5, 95])
            flat_range = flat_max - flat_min
            self.ax2.set_ylim(flat_min - 0.1*flat_range, flat_max + 0.1*flat_range)
        
        self.canvas.draw_idle()
        
    def interpolate_continuum(self):
        """Interpolate the full continuum from control points"""
        from scipy.interpolate import interp1d
        
        # Create interpolation function
        interp_func = interp1d(self.control_wave, self.control_continuum, 
                              kind='cubic', bounds_error=False, fill_value='extrapolate')
        
        # Interpolate to full wavelength grid
        self.current_continuum = interp_func(self.wave)
        
        # Ensure continuum is positive
        self.current_continuum = np.maximum(self.current_continuum, 0.01 * np.max(self.current_continuum))
        
    def update_plots(self):
        """Update both plots with current continuum and enhanced visual feedback"""
        # Update continuum line in top plot
        self.continuum_line.set_ydata(self.current_continuum)
        
        # Update control points with enhanced visual styling
        self.control_points.set_data(self.control_wave, self.control_continuum)
        
        # Update flattened spectrum in bottom plot with error handling
        try:
            # Avoid division by zero
            safe_continuum = np.where(self.current_continuum <= 0, 
                                    np.finfo(float).eps, self.current_continuum)
            flattened = self.flux / safe_continuum
            
            # Update the flattened spectrum line
            self.flattened_line.set_ydata(flattened)
            
            # Auto-adjust bottom plot y-limits for better visualization
            valid_flux = flattened[np.isfinite(flattened)]
            if len(valid_flux) > 10:  # Ensure we have enough data points
                flat_median = np.median(valid_flux)
                flat_mad = np.median(np.abs(valid_flux - flat_median))  # Median absolute deviation
                
                # Use robust statistics for better outlier handling
                y_min = max(0, flat_median - 4*flat_mad)
                y_max = flat_median + 4*flat_mad
                
                # Ensure reasonable range
                if y_max - y_min < 0.1:
                    y_min = flat_median - 0.5
                    y_max = flat_median + 0.5
                
                self.ax2.set_ylim(y_min, y_max)
            
        except Exception as e:
            print(f"Warning: Error updating flattened spectrum: {e}")
            # Fallback to simple update
            self.flattened_line.set_ydata(np.ones_like(self.wave))
        
        # Add visual feedback for editing
        if hasattr(self, 'selected_point') and self.selected_point is not None:
            # Highlight the selected control point
            selected_x = self.control_wave[self.selected_point]
            selected_y = self.control_continuum[self.selected_point]
            
            # Update selection indicator if it exists, otherwise create it
            if not hasattr(self, 'selection_indicator'):
                self.selection_indicator, = self.ax1.plot(selected_x, selected_y, 'yo', 
                                                        markersize=15, alpha=0.7,
                                                        markeredgecolor='orange', 
                                                        markeredgewidth=3)
            else:
                self.selection_indicator.set_data([selected_x], [selected_y])
                self.selection_indicator.set_visible(True)
        else:
            # Hide selection indicator if no point is selected
            if hasattr(self, 'selection_indicator'):
                self.selection_indicator.set_visible(False)
        
        # Redraw with optimized drawing
        self.canvas.draw_idle()
        
    def on_pick(self, event):
        """Handle picking of control points"""
        if event.artist == self.control_points:
            self.selected_point = event.ind[0]
            self.dragging = True
            
    def on_press(self, event):
        """Handle mouse press events"""
        if event.inaxes == self.ax1 and self.selected_point is not None:
            self.dragging = True
            
    def on_release(self, event):
        """Handle mouse release events"""
        self.dragging = False
        self.selected_point = None
        
    def on_motion(self, event):
        """Handle mouse motion events"""
        if self.dragging and self.selected_point is not None and event.inaxes == self.ax1:
            # Update the selected control point
            if event.ydata is not None:
                self.control_continuum[self.selected_point] = event.ydata
                
                # Interpolate and update
                self.interpolate_continuum()
                self.update_plots()
                
    def reset_continuum(self):
        """Reset continuum to original fit"""
        self.current_continuum = self.original_continuum.copy()
        self.control_continuum = self.original_continuum[self.control_indices].copy()
        self.update_plots()
        
    def smooth_continuum(self):
        """Apply smoothing to the control points"""
        from scipy.ndimage import gaussian_filter1d
        
        # Smooth the control points
        self.control_continuum = gaussian_filter1d(self.control_continuum, sigma=1.0)
        
        # Interpolate and update
        self.interpolate_continuum()
        self.update_plots()
        
    def add_control_point(self):
        """Add a new control point at the center of the current view"""
        xlim = self.ax1.get_xlim()
        center_wave = (xlim[0] + xlim[1]) / 2
        
        # Find the closest wavelength point
        idx = np.argmin(np.abs(self.wave - center_wave))
        
        # Add to control points if not already there
        if idx not in self.control_indices:
            # Insert in sorted order
            insert_pos = np.searchsorted(self.control_indices, idx)
            self.control_indices = np.insert(self.control_indices, insert_pos, idx)
            self.control_wave = self.wave[self.control_indices]
            self.control_continuum = np.insert(self.control_continuum, insert_pos, 
                                             self.current_continuum[idx])
            
            self.update_plots()
            messagebox.showinfo("Control Point Added", 
                              f"Added control point at {center_wave:.1f} Å")
        else:
            messagebox.showinfo("Control Point Exists", 
                              "A control point already exists near this wavelength")
            
    def apply_changes(self):
        """Apply the modified continuum"""
        if self.parent_dialog:
            # Return the modified continuum to the parent
            self.parent_dialog.apply_modified_continuum(self.current_continuum)
        self.window.destroy()
        
    def cancel_changes(self):
        """Cancel changes and close editor"""
        self.window.destroy() 
