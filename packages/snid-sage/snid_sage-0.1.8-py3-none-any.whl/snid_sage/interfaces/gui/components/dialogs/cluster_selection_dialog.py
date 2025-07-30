"""
Interactive GMM Cluster Selection Dialog with Enhanced Professional Design

This dialog presents all viable GMM clusters in a 3D interactive plot where users
can click directly on clusters to select them. Features real-time selection feedback,
visual cluster highlighting with black edges, and automatic fallback to best cluster.

NEW: Enhanced integrated top-3 matches panel that shows spectrum overlays alongside 
the main clustering view for better visibility and user experience.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from typing import List

try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.cluster_selection')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.cluster_selection')


class ClusterSelectionDialog:
    """Professional 3D cluster selection dialog with enhanced visual design.

    ENHANCED (January 2025): Now features an integrated top-3 matches panel on the right 
    side that shows detailed spectrum overlays. The panel updates dynamically when users 
    select different clusters, providing immediate visual feedback of template quality.
    """
    
    def __init__(self, parent, clustering_results, theme_manager, snid_result=None, callback=None):
        self.parent = parent
        self.clustering_results = clustering_results
        self.theme_manager = theme_manager
        self.callback = callback
        # Store full SNID result so we can access the processed input spectrum
        self.snid_result = snid_result
        
        self.all_candidates = clustering_results.get('all_candidates', [])
        self.automatic_best = clustering_results.get('best_cluster')
        
        self.selected_cluster = None
        self.selected_index = -1
        
        # UI components
        self.dialog = None
        self.canvas = None
        self.fig = None
        self.ax = None
        self.scatter_plots = []

        
        # Enhanced: Integrated matches panel components
        self.matches_panel = None
        self.matches_canvas = None
        self.matches_fig = None
        self.matches_axes = []
        
        # Preview pop-up window handle and Shift state
        self.preview_window = None
        self._shift_held = False  # Track if Shift is currently held
        
        # Visual state - track persistent highlights for hover behavior
        self.current_selected_scatters = []  # Track currently selected cluster visuals
        self.persistent_highlight_scatters = []  # Track persistent highlights that stay when hovering away
        
        # View state - always use 3D
        self.is_3d_view = True
        self.force_2d = False  # Keep for compatibility but always use 3D
        
        # Use consistent colors
        self.colors = self._get_colors()
        self.type_colors = self._get_type_colors()
        
        # Cluster selector menu components
        self.cluster_selector_open = False
        self.cluster_selector_menu = None
        
        # -----------------------------------------------------------------
        # Ensure candidate list is sorted by the same score used in automatic
        # selection so that the drop-down order matches the ranking logic.
        # We sort in-place once here to keep indices consistent everywhere.
        # -----------------------------------------------------------------
        def _get_candidate_score(c):
            # Preferred metric hierarchy: penalised_score → composite_score → mean_rlap
            return (
                c.get('penalized_score') or
                c.get('penalised_score') or  # British spelling safeguard
                c.get('composite_score') or
                c.get('mean_rlap') or 0.0
            )

        try:
            self.all_candidates.sort(key=_get_candidate_score, reverse=True)
        except Exception as sort_err:
            _LOGGER.debug(f"Could not sort clusters by score: {sort_err}")

        # After sorting we must recalculate the selected index for automatic_best
        # because its position may have changed.
        def _recompute_best_index():
            if not self.automatic_best:
                return -1
            # direct object identity or equality first
            try:
                return self.all_candidates.index(self.automatic_best)
            except ValueError:
                pass
            # fallback by (type, cluster_id)
            t_type = self.automatic_best.get('type')
            t_id = self.automatic_best.get('cluster_id')
            for idx, cand in enumerate(self.all_candidates):
                if cand.get('type') == t_type and cand.get('cluster_id') == t_id:
                    return idx
            return -1

        # recompute index later used for highlighting
        self.selected_index = _recompute_best_index()
        # Ensure automatic_best remains consistent reference in list
        if self.selected_index >= 0:
            self.selected_cluster = self.all_candidates[self.selected_index]
        # -----------------------------------------------------------------
        
        try:
            self._create_dialog()
            # Don't call _setup_plot() or _plot_clusters() here - they're now called in _create_left_panel()
            
            _LOGGER.info(f"🎯 Enhanced cluster selection dialog opened with {len(self.all_candidates)} candidates")
        except Exception as e:
            _LOGGER.error(f"Error initializing cluster selection dialog: {e}")
            # Try to create a minimal dialog even if plotting fails
            try:
                if not hasattr(self, 'dialog') or self.dialog is None:
                    self._create_dialog()
                # Show error message in the dialog
                if hasattr(self, 'dialog') and self.dialog:
                    messagebox.showerror("Plot Error", f"Error creating cluster plot: {e}\nDialog may not function properly.")
            except Exception as critical_error:
                _LOGGER.error(f"Critical error in dialog initialization: {critical_error}")
                raise
    
    def _get_colors(self):
        """Get color scheme with white backgrounds as requested"""
        try:
            theme = self.theme_manager.get_current_theme()
            return {
                'bg_main': 'white',        # White background as requested
                'bg_panel': 'white',       # White background as requested
                'bg_step': '#f0f0f0',      # Light gray for variety
                'bg_current': '#0078d4',
                'button_bg': '#e0e0e0',    # Light gray buttons
                'text_primary': '#000000', # Black text on white
                'text_secondary': '#666666',
                'accent': '#0078d4',
                'success': '#107c10',
                'warning': '#ff8c00',
                'hover': '#e6f3ff'        # Light blue hover effect
            }
        except:
            return {
                'bg_main': 'white',        # White background as requested
                'bg_panel': 'white',       # White background as requested
                'bg_step': '#f0f0f0',
                'bg_current': '#0078d4',
                'button_bg': '#e0e0e0',
                'text_primary': '#000000',
                'text_secondary': '#666666',
                'accent': '#0078d4',
                'success': '#107c10',
                'warning': '#ff8c00',
                'hover': '#e6f3ff'        # Light blue hover effect
            }
    
    def _get_type_colors(self):
        # Use 10 DISTINCT PASTEL colors for the specified supernova types
        return {
            'Ia': '#FFB3B3',      # Pastel Red
            'Ib': '#FFCC99',      # Pastel Orange  
            'Ic': '#99CCFF',      # Pastel Blue
            'II': '#9370DB',     # Medium slate blue
            'Galaxy': '#8A2BE2',  # Blue-violet for galaxies
            'Star': '#FFD700',    # Gold for stars
            'AGN': '#FF6347',     # Tomato red for AGN/QSO
            'SLSN': '#20B2AA',    # Light sea green
            'LFBOT': '#FFFF99',   # Pastel Yellow
            'TDE': '#D8BFD8',     # Pastel Purple/Thistle
            'KN': '#B3FFFF',      # Pastel Cyan
            'GAP': '#FFCC80',     # Pastel Orange
            'Unknown': '#D3D3D3', # Light Gray
            'Other': '#C0C0C0'    # Silver
        }
    
    def _create_dialog(self):
        """Create professional dialog window matching other dialogs"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("🎯 Enhanced GMM Cluster Selection")
        self.dialog.geometry("1700x1000")  # Optimized size for 65/35 split
        self.dialog.resizable(True, True)
        self.dialog.minsize(1500, 900)  # Adjusted minimum size
        
        # Apply background color
        self.dialog.configure(bg=self.colors['bg_main'])
        
        # Handle window close - automatically use best cluster
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close_auto_select)
        
        # Center on parent
        self._center_dialog()
        
        # Create layout
        self._create_layout()
    
    def _center_dialog(self):
        """Center dialog on parent window, positioned higher on screen"""
        self.dialog.update_idletasks()
        
        try:
            # Center on parent window, but position higher
            parent_widget = self.parent
            x = parent_widget.winfo_x() + (parent_widget.winfo_width() // 2) - (1800 // 2)
            # Position higher by reducing y offset - move up by 75 pixels (changed from 100 to 75)
            y = parent_widget.winfo_y() + (parent_widget.winfo_height() // 2) - (1000 // 2) - 75
            self.dialog.geometry(f"1800x1000+{x}+{y}")
        except (AttributeError, tk.TclError):
            # Fallback: center on screen, but position higher
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width // 2) - (1800 // 2)
            # Position higher by reducing y offset - move up by 75 pixels (changed from 100 to 75)
            y = (screen_height // 2) - (1000 // 2) - 75
            self.dialog.geometry(f"1800x1000+{x}+{y}")
    
    def _create_layout(self):
        """Create professional layout matching other dialogs"""
        # Header
        self._create_header()
        
        # Main content with split panel layout
        self._create_split_panel_layout()
        
        # Footer with buttons
        self._create_footer()
    
    def _create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.dialog, bg=self.colors['accent'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        content_frame = tk.Frame(header_frame, bg=self.colors['accent'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        title_label = tk.Label(content_frame, text="🎯 GMM Cluster Selection",
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.colors['accent'], fg='white')
        title_label.pack()
        
        subtitle_text = f"Select the best cluster from {len(self.all_candidates)} candidates • Hover to highlight • Click to select"
        subtitle_label = tk.Label(content_frame, text=subtitle_text,
                                 font=('Segoe UI', 12),
                                 bg=self.colors['accent'], fg='#e0f2fe')
        subtitle_label.pack(pady=(5, 0))
    
    def _create_split_panel_layout(self):
        """Create enhanced two-panel layout: 70% GMM + dropdown | 30% matches panel"""
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg_main'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Calculate total width for proportional sizing
        total_width = 1680  # Slightly less than 1700 for padding
        
        # Create two-panel layout: 70% cluster selector + 30% top 2 matches (changed from 60/40)
        self.left_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], width=int(total_width * 0.70))  # Changed from 0.60 to 0.70
        self.left_panel.pack(side='left', fill='both', expand=False)
        self.left_panel.pack_propagate(False)
        
        self.right_panel = tk.Frame(main_frame, bg=self.colors['bg_panel'], width=int(total_width * 0.30))  # Changed from 0.40 to 0.30
        self.right_panel.pack(side='left', fill='both', expand=True)
        self.right_panel.pack_propagate(False)

        # Create main layout
        self._create_left_panel()   # Fancy dropdown cluster selector only
        self._create_right_panel()  # Top 3 matches
        
        # NOW setup the integrated matches panel after both panels exist
        self._setup_integrated_matches_panel()
        
        # THEN: Schedule automatic selection after dialog is fully initialized
        if self.all_candidates:
            # Automatically highlight the pre-computed best cluster (fall back to first if unavailable)
            best_index = self.selected_index if self.selected_index is not None and self.selected_index >= 0 else 0
            self.dialog.after(100, lambda: self._select_cluster(best_index))  # 100 ms delay ensures UI is ready

    def _create_left_panel(self):
        """Create the cluster selector panel with GMM plot"""
        # GMM Plot Section (full left panel)
        plot_frame = tk.Frame(self.left_panel, bg=self.colors['bg_panel'])
        plot_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Setup the matplotlib plot
        self._setup_plot_in_frame(plot_frame)
        
        # Initialize the GMM plot
        self._plot_clusters()
    
    def _create_right_panel(self):
        """Create the enhanced integrated matches panel"""
        # Title with icon - more compact
        matches_title = tk.Label(self.right_panel, text="🔍 Top 2 Template Matches For Selected Cluster",
                             font=('Segoe UI', 14, 'bold'),
                             bg=self.colors['bg_panel'], fg=self.colors['text_primary'])
        matches_title.pack(fill='x', pady=(10, 5))        # let it span full panel width
        matches_title.config(anchor='center', justify='center')    

        # Container for the matplotlib figure - maximize space
        self.matches_panel = tk.Frame(self.right_panel, bg=self.colors['bg_panel'])
        self.matches_panel.pack(fill='both', expand=True, padx=5, pady=(5, 5))
        
        # Don't create info label - we'll show content directly

    def _create_footer(self):
        """Create footer with action buttons"""
        footer_frame = tk.Frame(self.dialog, bg=self.colors['bg_step'], height=80)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        button_frame = tk.Frame(footer_frame, bg=self.colors['bg_step'])
        button_frame.pack(expand=True, pady=20)
        
        # Confirm button (primary) - centered
        confirm_button = tk.Button(button_frame, text="✅ Confirm Selection",
                                 command=self._confirm_selection,
                                 bg=self.colors['success'], fg='white',
                                 font=('Segoe UI', 14, 'bold'),
                                 relief='raised', bd=3,
                                 width=20, height=2)
        confirm_button.pack(pady=5)

        # Bind Shift shortcut
        self._bind_preview_shortcut()

    def _setup_integrated_matches_panel(self):
        """Setup the matplotlib figure for the integrated matches panel"""
        _LOGGER.debug("Setting up integrated matches panel")
        
        if not self.matches_panel:
            _LOGGER.debug("No matches panel available")
            return
            
        # Close any existing figure to prevent overlaps
        if hasattr(self, 'matches_fig') and self.matches_fig:
            plt.close(self.matches_fig)
        
        # Destroy any existing canvas to prevent conflicts
        if hasattr(self, 'matches_canvas') and self.matches_canvas:
            self.matches_canvas.get_tk_widget().destroy()
        
        # Create matplotlib figure for matches - optimized size for the 30% panel width
        # Adjusted figure size for the smaller panel and optimized plot spacing
        self.matches_fig = plt.Figure(figsize=(8, 12), dpi=100, facecolor='white')  # Reduced width from 8.5 to 6.5, height from 12 to 10
        
        # Clear any existing content
        self.matches_fig.clear()
        
        # Create exactly 2 subplots vertically stacked with optimized spacing for maximum size
        self.matches_axes = []
        for i in range(2):  # Changed from 3 to 2 for better space usage
            # Use maximized subplot spacing
            ax = self.matches_fig.add_subplot(2, 1, i+1)  # Changed from 3,1 to 2,1
            ax.set_facecolor('white')
            ax.tick_params(colors=self.colors['text_secondary'], labelsize=10)
            for spine in ax.spines.values():
                spine.set_color(self.colors['text_secondary'])
            ax.grid(True, alpha=0.3, linewidth=0.5)
            self.matches_axes.append(ax)
        
        # Optimize subplot parameters: shorter individual plots with less spacing between them
        self.matches_fig.subplots_adjust(left=0.12, right=0.98, top=0.94, bottom=0.06, hspace=0.15)  # Reduced top from 0.97 to 0.94, increased bottom from 0.03 to 0.06, reduced hspace from 0.25 to 0.15
        
        # Embed in tkinter with full expansion
        self.matches_canvas = FigureCanvasTkAgg(self.matches_fig, master=self.matches_panel)
        self.matches_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        _LOGGER.debug(f"Matches panel setup complete: {len(self.matches_axes)} axes created with maximized size (2 plots)")
    
    def _show_placeholder_content(self):
        """Show placeholder content when no cluster is selected"""
        try:
            for i, ax in enumerate(self.matches_axes):
                if ax is not None:  # Add null check
                    ax.clear()
                    ax.set_facecolor('white')
                    ax.text(0.5, 0.5, f'Select a cluster\nto view match #{i+1}', 
                           transform=ax.transAxes, ha='center', va='center',
                           fontsize=12, color=self.colors['text_secondary'], style='italic')
                    ax.set_title(f"Match #{i+1}: Awaiting Selection", fontsize=11, 
                               color=self.colors['text_secondary'])
                    
                    # Configure appearance
                    ax.tick_params(colors=self.colors['text_secondary'], labelsize=9)
                    for spine in ax.spines.values():
                        spine.set_color(self.colors['text_secondary'])
                    ax.grid(True, alpha=0.3, linewidth=0.5)
            
            # Don't use tight_layout - we manually set subplot parameters
            self.matches_canvas.draw()
        except Exception as e:
            _LOGGER.error(f"Error showing placeholder content: {e}")

    def _update_integrated_matches_panel(self):
        """Update the integrated matches panel with current cluster's top 3 matches"""
        _LOGGER.debug(f"Updating integrated matches panel for cluster: {self.selected_cluster.get('type', 'Unknown') if self.selected_cluster else 'None'}")
        
        # First ensure the panel is setup
        if not hasattr(self, 'matches_axes') or not self.matches_axes:
            _LOGGER.debug("Matches axes not initialized - setting up panel first")
            self._setup_integrated_matches_panel()
        
        if not self.selected_cluster or not hasattr(self, 'matches_axes') or not self.matches_axes:
            _LOGGER.debug("Cannot update matches panel - missing requirements")
            return
            
        # Get top 2 matches from selected cluster (changed from 3 to 2)
        matches = sorted(self.selected_cluster.get('matches', []), 
                        key=lambda m: m.get('rlap', 0), reverse=True)[:2]  # Changed from [:3] to [:2]
        
        # Get input spectrum data
        input_wave = input_flux = None
        if (self.snid_result is not None and hasattr(self.snid_result, 'processed_spectrum') and
                self.snid_result.processed_spectrum):
            # Try different keys for processed spectrum
            if 'log_wave' in self.snid_result.processed_spectrum:
                input_wave = self.snid_result.processed_spectrum['log_wave']
                input_flux = self.snid_result.processed_spectrum['log_flux']
            elif 'wave' in self.snid_result.processed_spectrum:
                input_wave = self.snid_result.processed_spectrum['wave']
                input_flux = self.snid_result.processed_spectrum['flux']
        elif (self.snid_result is not None and hasattr(self.snid_result, 'input_spectrum') and
              isinstance(self.snid_result.input_spectrum, dict)):
            input_wave = self.snid_result.input_spectrum.get('wave')
            input_flux = self.snid_result.input_spectrum.get('flux')
        
        _LOGGER.debug(f"Input spectrum available: {input_wave is not None}, Matches count: {len(matches)}")
        
        # Clear all axes first to prevent overlaps - with null checks
        for i, ax in enumerate(self.matches_axes):
            if ax is not None:  # Add null check to prevent the error
                ax.clear()
                ax.set_facecolor('white')
                # Reset axis properties
                ax.spines['top'].set_visible(True)
                ax.spines['right'].set_visible(True)
                ax.spines['bottom'].set_visible(True)
                ax.spines['left'].set_visible(True)
        
        # Update exactly 2 subplots
        for idx in range(2):
            if idx >= len(self.matches_axes):
                break
                
            ax = self.matches_axes[idx]
            if ax is None:  # Skip if axis is None
                continue
                
            ax.set_facecolor('white')
            ax.tick_params(colors=self.colors['text_secondary'], labelsize=9)
            for spine in ax.spines.values():
                spine.set_color(self.colors['text_secondary'])
            ax.grid(True, alpha=0.3, linewidth=0.5)
            
            if idx < len(matches) and matches[idx]:
                match = matches[idx]
                
                # Plot input spectrum
                if input_wave is not None and input_flux is not None:
                    ax.plot(input_wave, input_flux, color='#0078d4', linewidth=1.5, alpha=0.8, 
                           label='Input Spectrum', zorder=2)
                
                # Plot template match
                try:
                    # Try different ways to access template spectrum
                    t_wave = t_flux = None
                    
                    if 'spectra' in match and isinstance(match['spectra'], dict):
                        if 'flux' in match['spectra']:
                            t_wave = match['spectra']['flux'].get('wave')
                            t_flux = match['spectra']['flux'].get('flux')
                        elif 'wave' in match['spectra']:
                            t_wave = match['spectra']['wave']
                            t_flux = match['spectra']['flux']
                    elif 'wave' in match:
                        t_wave = match['wave']
                        t_flux = match['flux']
                    elif 'template_wave' in match:
                        t_wave = match['template_wave']
                        t_flux = match['template_flux']
                    
                    if t_wave is not None and t_flux is not None:
                        ax.plot(t_wave, t_flux, color='#E74C3C', linewidth=1.5, alpha=0.9,
                               label=f"Template: {match.get('name', 'Unknown')}", zorder=3)
                    else:
                        _LOGGER.debug(f"No template data found for match {idx+1}: keys={list(match.keys())}")
                        
                except Exception as e:
                    _LOGGER.debug(f"Error plotting template match {idx+1}: {e}")
                    import traceback
                    _LOGGER.debug(f"Traceback: {traceback.format_exc()}")
                
                # Simplified title 
                title_text = f"#{idx+1}: {match.get('name', 'Unknown')} (RLAP: {match.get('rlap', 0):.1f})"
                ax.set_title(title_text, fontsize=10, color=self.colors['text_primary'], 
                           fontweight='bold', pad=5)
                
                # Add legend for first plot only to save space
                if idx == 0:
                    ax.legend(loc='upper right', fontsize=7, framealpha=0.9)
                    
            else:
                # No match available
                ax.text(0.5, 0.5, f'No Match #{idx+1}', transform=ax.transAxes,
                       ha='center', va='center', fontsize=12, 
                       color=self.colors['text_secondary'], style='italic')
                ax.set_title(f"#{idx+1}: No Template Available", fontsize=11, 
                           color=self.colors['text_secondary'])
            
            # Set labels (only for bottom plot to save space)
            if idx == 1:  # Always the last (2nd) plot
                ax.set_xlabel('Wavelength (Å)', fontsize=10, color=self.colors['text_secondary'])
            ax.set_ylabel('Flux', fontsize=9, color=self.colors['text_secondary'])
        
        # Update cluster info display
        cluster_type = self.selected_cluster.get('type', 'Unknown')
        cluster_redshift = self.selected_cluster.get('enhanced_redshift', 
                                                   self.selected_cluster.get('weighted_mean_redshift', 0))
        
        # Update cluster info label
        if hasattr(self, 'cluster_info_label'):
            # Use dynamic metric name (RLAP or RLAP-Cos)
            try:
                from snid_sage.shared.utils.math_utils import get_metric_name_for_match
                if self.selected_cluster.get('matches'):
                    metric_name_local = get_metric_name_for_match(self.selected_cluster['matches'][0])
                else:
                    metric_name_local = 'RLAP'
            except ImportError:
                metric_name_local = 'RLAP'
            mean_metric_val = self.selected_cluster.get('mean_metric', self.selected_cluster.get('mean_rlap', 0))
            info_text = f"Selected: {cluster_type} cluster at redshift z = {cluster_redshift:.4f}  |  {metric_name_local} = {mean_metric_val:.1f}"
            self.cluster_info_label.config(text=info_text)
        
        # Refresh the canvas - don't use tight_layout as we manually set subplot params
        try:
            if hasattr(self, 'matches_canvas') and self.matches_canvas:
                # Ensure figure is the right size
                self.matches_fig.set_size_inches(6.5, 10)
                # Draw the canvas
                self.matches_canvas.draw()
                # Force update of the widget
                self.matches_canvas.get_tk_widget().update_idletasks()
            _LOGGER.debug("Matches panel canvas refreshed")
        except Exception as e:
            _LOGGER.error(f"Error refreshing matches canvas: {e}")
            import traceback
            _LOGGER.error(f"Traceback: {traceback.format_exc()}")
    
    def _setup_plot_in_frame(self, plot_frame):
        """Setup the matplotlib plot with navigation toolbar - maximized size"""
        # Create much larger figure
        self.fig = plt.figure(figsize=(16, 10))  # Much larger figure
        self.fig.patch.set_facecolor('white')  # White background as requested
        
        # MAXIMIZE the plot area - use almost the entire window space
        self.fig.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.08)
        
        # Setup plot based on current view state
        self._setup_current_view()
        
        # Create canvas 
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add navigation toolbar with white background
        toolbar_frame = tk.Frame(plot_frame, bg='white')
        toolbar_frame.pack(fill='x', pady=(3, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        self.toolbar.config(bg='white')
    
    def _setup_plot(self):
        """Setup plot after creation"""
        # This method is no longer needed as plotting is done in _setup_plot_in_frame
        pass
    
    def _setup_current_view(self):
        """Setup the 3D view (2D functionality removed)"""
        try:
            # Clear existing plot if it exists
            if hasattr(self, 'ax') and self.ax is not None:
                self.ax.clear()
            
            # Always use 3D plot
            try:
                from mpl_toolkits.mplot3d import Axes3D
                # Remove existing axis only if it exists and is not None
                if hasattr(self, 'ax') and self.ax is not None:
                    self.ax.remove()
                self.ax = self.fig.add_subplot(111, projection='3d')
                # Explicitly set 3D plot background to white
                self.ax.set_facecolor('white')
                self.is_3d = True
            except (ImportError, Exception) as e:
                # 3D not available - show error message
                _LOGGER.error(f"3D plotting unavailable: {e}")
                # Create a simple 2D plot for error display only
                if hasattr(self, 'ax') and self.ax is not None:
                    self.ax.remove()
                self.ax = self.fig.add_subplot(111)
                self.ax.set_facecolor('white')
                self.ax.text(0.5, 0.5, '3D plotting not available\nPlease install mplot3d', 
                           ha='center', va='center', transform=self.ax.transAxes,
                           fontsize=14, color='red')
                self.is_3d = False
                self.force_2d = True
                self.is_3d_view = False
                
        except Exception as e:
            _LOGGER.error(f"Error setting up view: {e}")
            # Emergency fallback - create a simple error display
            try:
                self.ax = self.fig.add_subplot(111)
                self.ax.set_facecolor('white')
                self.ax.text(0.5, 0.5, 'Error setting up plot', 
                           ha='center', va='center', transform=self.ax.transAxes,
                           fontsize=14, color='red')
                self.is_3d = False
                self.force_2d = True
                self.is_3d_view = False
            except Exception as fallback_error:
                _LOGGER.error(f"Critical error in plot setup: {fallback_error}")
                raise
    
    def _toggle_view(self):
        """Toggle functionality removed - always use 3D view"""
        # This method is kept for compatibility but does nothing
        # 2D functionality has been completely removed
        pass
    
    def _on_plot_button_click(self, event):
        """Handle click events for plot buttons"""
        try:
            # Get the clicked object
            clicked_object = event.artist
            
            # Check if the clicked object is a text object
            if hasattr(clicked_object, 'get_text'):
                button_text = clicked_object.get_text()
                
                # Check which button was clicked
                if "Cluster" in button_text or button_text == "Select Cluster":
                    # Open cluster selector menu
                    self._show_cluster_selector_menu()
                    
        except Exception as e:
            _LOGGER.error(f"Error handling plot button click: {e}")
    
    def _show_cluster_selector_menu(self):
        """Show cluster selector menu near the button"""
        if self.cluster_selector_open:
            self._close_cluster_selector_menu()
            return
            
        # Create menu window
        self.cluster_selector_menu = tk.Toplevel(self.dialog)
        self.cluster_selector_menu.overrideredirect(True)  # Remove window decorations
        self.cluster_selector_menu.configure(bg='white')
        
        # Apply Mac-specific improvements to the menu window
        try:
            from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            if CrossPlatformWindowManager.is_macos():
                # Ensure the menu window gets proper focus and event handling
                self.cluster_selector_menu.focus_set()
                self.cluster_selector_menu.lift()
                self.cluster_selector_menu.attributes('-topmost', True)
        except Exception as e:
            _LOGGER.debug(f"Mac menu window setup failed: {e}")
        
        # Create frame with border
        menu_frame = tk.Frame(self.cluster_selector_menu, bg='white', relief='solid', bd=1)
        menu_frame.pack(fill='both', expand=True)
        
        # Add title with larger font
        title_label = tk.Label(menu_frame, text="🎯 Select Cluster", 
                             font=('Segoe UI', 14, 'bold'),
                             bg='#0078d4', fg='white', padx=15, pady=8)
        title_label.pack(fill='x')
        
        # Add cluster options with much larger font
        for i, candidate in enumerate(self.all_candidates):
            cluster_type = candidate.get('type', 'Unknown')
            cluster_redshift = (candidate.get('enhanced_redshift') or 
                               candidate.get('weighted_mean_redshift') or 
                               candidate.get('mean_redshift') or 
                               candidate.get('redshift', 0.0))
            
            is_best = i == 0
            is_selected = i == self.selected_index
            
            # Format text with cluster number, type, and redshift on one line
            text = f"Cluster {i+1}: {cluster_type} (z = {cluster_redshift:.4f})"
            if is_best:
                text += " ⭐ BEST"
            
            # Create frame for each cluster option
            option_frame = tk.Frame(menu_frame, bg='white')
            option_frame.pack(fill='x', padx=2, pady=2)
            
            # Enhanced button creation with Mac compatibility
            btn = self._create_mac_compatible_button(
                option_frame, 
                text=text,
                font=('Segoe UI', 13, 'bold'),
                bg='#e3f2fd' if is_selected else 'white',
                fg='#0078d4' if is_best else 'black',
                relief='flat',
                anchor='w',
                padx=15,
                pady=10,
                cluster_index=i
            )
            btn.pack(fill='x')
            
            # Enhanced hover effects with Mac event bindings
            self._setup_enhanced_hover_effects(option_frame, btn, is_selected, i)
        
        # Position menu near button (top left of plot)
        self.cluster_selector_menu.update_idletasks()
        
        # Get dialog position
        dialog_x = self.dialog.winfo_x()
        dialog_y = self.dialog.winfo_y()
        
        # Position menu in top left area of dialog
        menu_x = dialog_x + 50
        menu_y = dialog_y + 150
        
        self.cluster_selector_menu.geometry(f"+{menu_x}+{menu_y}")
        
        self.cluster_selector_open = True
        
        # Enhanced click outside detection with Mac compatibility
        self._setup_enhanced_outside_click_detection()
        
    def _close_cluster_selector_menu(self):
        """Close the cluster selector menu"""
        if self.cluster_selector_menu and self.cluster_selector_menu.winfo_exists():
            self.cluster_selector_menu.destroy()
        self.cluster_selector_menu = None
        self.cluster_selector_open = False
        self.dialog.unbind('<Button-1>')
        
    def _on_click_outside_menu(self, event):
        """Handle clicks outside the cluster menu"""
        if self.cluster_selector_menu and self.cluster_selector_menu.winfo_exists():
            # Check if click is outside the menu
            x, y = event.x_root, event.y_root
            menu_x = self.cluster_selector_menu.winfo_x()
            menu_y = self.cluster_selector_menu.winfo_y()
            menu_width = self.cluster_selector_menu.winfo_width()
            menu_height = self.cluster_selector_menu.winfo_height()
            
            if not (menu_x <= x <= menu_x + menu_width and menu_y <= y <= menu_y + menu_height):
                self._close_cluster_selector_menu()
                
    def _select_cluster_from_menu(self, cluster_index):
        """Select a cluster from the menu"""
        self._close_cluster_selector_menu()
        self._select_cluster(cluster_index)
        
        # Update the button text
        self._update_cluster_button_text()
    
    def _create_mac_compatible_button(self, parent, text, font, bg, fg, relief, anchor, padx, pady, cluster_index):
        """Create a button that works properly on macOS with enhanced click detection"""
        try:
            from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            # Create button with enhanced Mac compatibility
            btn = tk.Button(parent, text=text,
                          font=font,
                          bg=bg, fg=fg,
                          relief=relief,
                          anchor=anchor,
                          padx=padx,
                          pady=pady,
                          cursor='hand2')
            
            # Enhanced command binding that works better on macOS
            def enhanced_click_handler():
                try:
                    _LOGGER.debug(f"Button click detected for cluster {cluster_index}")
                    self._select_cluster_from_menu(cluster_index)
                except Exception as e:
                    _LOGGER.error(f"Button click handler error: {e}")
            
            btn.configure(command=enhanced_click_handler)
            
            # Apply Mac-specific event bindings for better click detection
            if CrossPlatformWindowManager.is_macos():
                CrossPlatformWindowManager.setup_mac_event_bindings(
                    btn, 
                    click_callback=lambda e: enhanced_click_handler()
                )
                
                # Additional Mac-specific bindings for better responsiveness
                btn.bind("<Button-1>", lambda e: enhanced_click_handler(), add="+")
                btn.bind("<Return>", lambda e: enhanced_click_handler(), add="+")
                btn.bind("<space>", lambda e: enhanced_click_handler(), add="+")
                
                # Ensure button can receive focus on Mac
                btn.configure(takefocus=True)
                
                # Mac-specific styling to override system appearance
                btn.configure(
                    highlightbackground=bg,
                    highlightcolor=bg,
                    highlightthickness=0,
                    borderwidth=1,
                    compound='none'
                )
            
            return btn
            
        except Exception as e:
            _LOGGER.error(f"Enhanced button creation failed: {e}")
            # Fallback to simple button
            return tk.Button(parent, text=text, font=font, bg=bg, fg=fg, 
                           relief=relief, anchor=anchor, padx=padx, pady=pady,
                           command=lambda: self._select_cluster_from_menu(cluster_index))
    
    def _setup_enhanced_hover_effects(self, option_frame, button, is_selected, cluster_index):
        """Setup enhanced hover effects with Mac compatibility"""
        try:
            from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            # Enhanced hover effects for the whole frame
            def on_enter(e, frame=option_frame, btn=button, selected=is_selected):
                if not selected:
                    try:
                        btn.config(bg='#f0f8ff')
                        frame.config(bg='#f0f8ff')
                        for child in frame.winfo_children():
                            if isinstance(child, tk.Label):
                                child.config(bg='#f0f8ff')
                        
                        # Mac-specific: Ensure button gets focus on hover
                        if CrossPlatformWindowManager.is_macos():
                            btn.focus_set()
                            
                    except Exception as e:
                        _LOGGER.debug(f"Hover enter effect failed: {e}")
            
            def on_leave(e, frame=option_frame, btn=button, selected=is_selected):
                if not selected:
                    try:
                        btn.config(bg='white')
                        frame.config(bg='white')
                        for child in frame.winfo_children():
                            if isinstance(child, tk.Label):
                                child.config(bg='white')
                    except Exception as e:
                        _LOGGER.debug(f"Hover leave effect failed: {e}")
            
            # Bind hover events to both frame and button
            option_frame.bind('<Enter>', on_enter)
            option_frame.bind('<Leave>', on_leave)
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)
            
            # Mac-specific: Additional event bindings for better interaction
            if CrossPlatformWindowManager.is_macos():
                # Handle trackpad and mouse wheel events
                def handle_mac_events(event):
                    # Ensure button receives focus when interacted with
                    button.focus_set()
                    return "continue"
                
                button.bind("<Motion>", handle_mac_events, add="+")
                option_frame.bind("<Motion>", handle_mac_events, add="+")
            
        except Exception as e:
            _LOGGER.debug(f"Enhanced hover effects setup failed: {e}")
    
    def _setup_enhanced_outside_click_detection(self):
        """Setup enhanced outside click detection with Mac compatibility"""
        try:
            from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            def enhanced_outside_click_handler(event):
                try:
                    if self.cluster_selector_menu and self.cluster_selector_menu.winfo_exists():
                        # Check if click is outside the menu
                        x, y = event.x_root, event.y_root
                        menu_x = self.cluster_selector_menu.winfo_x()
                        menu_y = self.cluster_selector_menu.winfo_y()
                        menu_width = self.cluster_selector_menu.winfo_width()
                        menu_height = self.cluster_selector_menu.winfo_height()
                        
                        if not (menu_x <= x <= menu_x + menu_width and menu_y <= y <= menu_y + menu_height):
                            self._close_cluster_selector_menu()
                except Exception as e:
                    _LOGGER.debug(f"Outside click detection error: {e}")
                    # If detection fails, just close the menu
                    self._close_cluster_selector_menu()
            
            # Bind click outside detection with Mac compatibility
            if CrossPlatformWindowManager.is_macos():
                # Mac-specific bindings for all click types
                self.dialog.bind('<Button-1>', enhanced_outside_click_handler, add='+')
                self.dialog.bind('<Button-2>', enhanced_outside_click_handler, add='+')
                self.dialog.bind('<Button-3>', enhanced_outside_click_handler, add='+')
                self.dialog.bind('<Control-Button-1>', enhanced_outside_click_handler, add='+')
            else:
                # Standard binding for other platforms
                self.dialog.bind('<Button-1>', enhanced_outside_click_handler, add='+')
                
        except Exception as e:
            _LOGGER.debug(f"Enhanced outside click detection setup failed: {e}")
            # Fallback to simple binding
            self.dialog.bind('<Button-1>', self._on_click_outside_menu, add='+')

    def _plot_clusters(self):
        """Plot clusters with enhanced visual design and black edge selection"""
        if not self.all_candidates:
            self.ax.text(0.5, 0.5, 'No clusters available', 
                        ha='center', va='center', transform=self.ax.transAxes,
                        fontsize=14, color=self.colors['text_primary'])
            return
        
        self.ax.clear()
        self.scatter_plots.clear()
        
        # Prepare type mapping with consistent ordering
        unique_types = sorted(list(set(c.get('type', 'Unknown') for c in self.all_candidates)))
        type_to_index = {sn_type: i for i, sn_type in enumerate(unique_types)}
        
        # Determine which metric name we are using (RLAP or RLAP-Cos)
        try:
            from snid_sage.shared.utils.math_utils import get_best_metric_value, get_metric_name_for_match
        except ImportError:
            # Fallback lambdas if utilities not available
            get_best_metric_value = lambda m: m.get('rlap', 0)
            get_metric_name_for_match = lambda m: 'RLAP'
        
        metric_name_global = 'RLAP'
        # Try to detect from first match if possible
        for cand in self.all_candidates:
            if cand.get('matches'):
                metric_name_global = get_metric_name_for_match(cand['matches'][0])
                break
        
        # Plot all clusters with enhanced styling
        if self.is_3d:
            # 3D Plot: X=redshift, Y=type, Z=Metric (RLAP or RLAP-Cos)
            for i, candidate in enumerate(self.all_candidates):
                matches = candidate.get('matches', [])
                if not matches:
                    candidate_redshifts = [candidate.get('mean_redshift', 0)]
                    candidate_metrics = [candidate.get('mean_metric', candidate.get('mean_rlap', 0))]
                else:
                    candidate_redshifts = [m['redshift'] for m in matches]
                    candidate_metrics = [get_best_metric_value(m) for m in matches]
                
                candidate_type_indices = [type_to_index[candidate['type']]] * len(candidate_redshifts)
                
                # Visual style: consistent size, no transparency
                size = 80  # Larger points for better visibility  
                alpha = 1.0  # No transparency as requested
                
                # Gray edges for all by default (black edges added later for selected)
                edgecolor = 'gray'
                linewidth = 0.5
                
                # Use consistent type colors
                color = self.type_colors.get(candidate['type'], self.type_colors['Unknown'])
                
                # Plot all points
                scatter = self.ax.scatter(candidate_redshifts, candidate_type_indices, candidate_metrics,
                                        c=color, s=size, alpha=alpha,
                                        edgecolors=edgecolor, linewidths=linewidth)
                
                self.scatter_plots.append((scatter, i, candidate))
                
                # NO cluster number labels - removed as requested
            
            # Enhanced 3D setup
            self.ax.set_xlabel('Redshift (z)', color=self.colors['text_primary'], fontsize=16, labelpad=15)
            self.ax.set_ylabel('SN Type', color=self.colors['text_primary'], fontsize=16, labelpad=15)
            self.ax.set_zlabel(metric_name_global, color=self.colors['text_primary'], fontsize=16, labelpad=15)
            self.ax.set_yticks(range(len(unique_types)))
            self.ax.set_yticklabels(unique_types, fontsize=12)
            
            # Set view and enable ONLY horizontal rotation
            self.ax.view_init(elev=25, azim=45)
            self.ax.set_box_aspect([2.5, 1.0, 1.5])  # Even wider for the larger plot
            
            # Connect rotation constraint to ONLY allow horizontal (azimuth) rotation
            def on_rotate(event):
                if event.inaxes == self.ax and self.is_3d and hasattr(self.ax, 'view_init'):
                    # LOCK elevation to 25 degrees, only allow azimuth changes (3D only)
                    self.ax.view_init(elev=25, azim=self.ax.azim)
                    self.canvas.draw_idle()
            
            self.canvas.mpl_connect('motion_notify_event', on_rotate)
            
            # Enhanced 3D styling with completely white background
            try:
                # Ensure all panes are white and remove any blue artifacts
                self.ax.xaxis.pane.fill = True
                self.ax.yaxis.pane.fill = True
                self.ax.zaxis.pane.fill = True
                self.ax.xaxis.pane.set_facecolor('white')
                self.ax.yaxis.pane.set_facecolor('white')
                self.ax.zaxis.pane.set_facecolor('white')
                self.ax.xaxis.pane.set_edgecolor('lightgray')
                self.ax.yaxis.pane.set_edgecolor('lightgray')
                self.ax.zaxis.pane.set_edgecolor('lightgray')
                self.ax.xaxis.pane.set_alpha(1.0)
                self.ax.yaxis.pane.set_alpha(1.0)
                self.ax.zaxis.pane.set_alpha(1.0)
                
                # Additional background fixes to eliminate blue artifacts (if attributes exist)
                try:
                    # These attributes may not exist in all matplotlib versions
                    if hasattr(self.ax, 'w_xaxis'):
                        self.ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))  # White
                    if hasattr(self.ax, 'w_yaxis'):
                        self.ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))  # White
                    if hasattr(self.ax, 'w_zaxis'):
                        self.ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))  # White
                except AttributeError:
                    # Skip if these attributes don't exist in this matplotlib version
                    pass
                
                # Force complete redraw to ensure white background
                self.fig.patch.set_facecolor('white')
                self.ax.set_facecolor('white')
                
            except Exception as e:
                # If any 3D styling fails, log it but don't crash
                _LOGGER.warning(f"Some 3D styling options not available: {e}")
                # Still try to set basic white background
                try:
                    self.fig.patch.set_facecolor('white')
                    self.ax.set_facecolor('white')
                except:
                    pass
            
        # 2D plotting functionality has been completely removed
        # Only 3D plotting is supported
        
        # Remove title as requested
        
        # Enhanced plot styling
        self.ax.xaxis.label.set_color(self.colors['text_primary'])
        self.ax.yaxis.label.set_color(self.colors['text_primary'])
        if self.is_3d:
            self.ax.zaxis.label.set_color(self.colors['text_primary'])
        self.ax.tick_params(colors=self.colors['text_secondary'], labelsize=12)
        self.ax.grid(True, alpha=0.4, color='gray', linestyle='-', linewidth=0.5)
        
        # Toggle button removed - always use 3D view
        
        # Add cluster selector button
        self._add_cluster_selector_button()
        
        # Connect click events for cluster selector button only
        self.canvas.mpl_connect('pick_event', self._on_plot_button_click)
        
        # Show persistent highlight for the auto-selected best cluster
        if self.selected_cluster is not None and self.selected_index >= 0:
            self._add_persistent_highlight(self.selected_index)
        
        self.canvas.draw()
    
    def _add_toggle_button(self):
        """Toggle button functionality removed - always use 3D view"""
        # This method is kept for compatibility but does nothing
        # 2D functionality has been completely removed
        pass
    
    def _add_cluster_selector_button(self):
        """Add cluster selector button in top left of plot"""
        # Get selected cluster info
        if self.selected_cluster:
            cluster_type = self.selected_cluster.get('type', 'Unknown')
            cluster_idx = self.selected_index + 1
            button_text = f"▼ Cluster {cluster_idx}: {cluster_type}"
        else:
            button_text = "▼ Select Cluster"
        
        # Add button in top left with clearer styling
        if self.is_3d and hasattr(self.ax, 'text2D'):  # 3D axis
            self.cluster_button_text = self.ax.text2D(0.02, 0.98, button_text, 
                          transform=self.ax.transAxes,
                          va='top', ha='left', fontsize=11, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.6', facecolor='#e3f2fd', 
                                  alpha=0.95, edgecolor='#0078d4', linewidth=2),
                          picker=True)
        else:  # 2D axis
            self.cluster_button_text = self.ax.text(0.02, 0.98, button_text, 
                        transform=self.ax.transAxes,
                        va='top', ha='left', fontsize=11, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.6', facecolor='#e3f2fd', 
                                alpha=0.95, edgecolor='#0078d4', linewidth=2),
                        picker=True)
    
    def _add_persistent_highlight(self, cluster_index):
        """Add persistent highlight for selected cluster"""
        try:
            # Dynamically determine best metric value extractor (RLAP or RLAP-Cos)
            try:
                from snid_sage.shared.utils.math_utils import get_best_metric_value
            except ImportError:
                # Fallback in case the utility cannot be imported (e.g., during unit tests)
                get_best_metric_value = lambda m: m.get('rlap', 0)

            if 0 <= cluster_index < len(self.scatter_plots):
                scatter, idx, candidate = self.scatter_plots[cluster_index]
                
                # Add BLACK edge highlights to this cluster
                matches = candidate.get('matches', [])
                if not matches:
                    candidate_redshifts = [candidate.get('mean_redshift', 0)]
                    candidate_metrics = [candidate.get('mean_metric', candidate.get('mean_rlap', 0))]
                else:
                    candidate_redshifts = [m['redshift'] for m in matches]
                    candidate_metrics = [get_best_metric_value(m) for m in matches]
                
                if self.is_3d:
                    unique_types = sorted(list(set(c.get('type', 'Unknown') for c in self.all_candidates)))
                    type_to_index = {sn_type: i for i, sn_type in enumerate(unique_types)}
                    candidate_type_indices = [type_to_index[candidate['type']]] * len(candidate_redshifts)
                    
                    # Add highlighted scatter with BLACK edges
                    highlight_scatter = self.ax.scatter(candidate_redshifts, candidate_type_indices, candidate_metrics,
                                                      c=self.type_colors.get(candidate['type'], self.type_colors['Unknown']), 
                                                      s=80, alpha=1.0,
                                                      edgecolors='black', linewidths=1.2, zorder=3)
                # 2D highlighting functionality removed - only 3D is supported
                
                # Store the persistent highlight
                self.persistent_highlight_scatters.append(highlight_scatter)
                
        except Exception as e:
            _LOGGER.debug(f"Error adding persistent highlight: {e}")
    
    def _clear_all_highlights(self):
        """Clear all visual highlights"""
        try:
            # Clear current highlights (used for temporary hover highlights before)
            for scatter in self.current_selected_scatters:
                if scatter in self.ax.collections:
                    scatter.remove()
            self.current_selected_scatters.clear()
            
            # Clear persistent highlights
            for scatter in self.persistent_highlight_scatters:
                if scatter in self.ax.collections:
                    scatter.remove()
            self.persistent_highlight_scatters.clear()
            
            # Force canvas redraw
            self.canvas.draw_idle()
        except Exception as e:
            _LOGGER.debug(f"Error clearing highlights: {e}")

    def _select_cluster(self, cluster_index):
        """Select a cluster and update UI"""
        if 0 <= cluster_index < len(self.all_candidates):
            self.selected_cluster = self.all_candidates[cluster_index]
            self.selected_index = cluster_index
            
            # Clear all highlights first
            self._clear_all_highlights()
            
            # Add persistent highlight for the selected cluster
            self._add_persistent_highlight(cluster_index)
            
            # Update cluster button text
            self._update_cluster_button_text()
            
            _LOGGER.info(f"🎯 Selected cluster {cluster_index + 1}: {self.selected_cluster.get('type', 'Unknown')}")
            
            # Update integrated matches panel
            self._update_integrated_matches_panel()
            
            # Also refresh legacy preview window if it is open
            self._update_preview_window()
    
    def _update_cluster_button_text(self):
        """Update the cluster selector button text"""
        if hasattr(self, 'cluster_button_text') and self.selected_cluster:
            cluster_type = self.selected_cluster.get('type', 'Unknown')
            cluster_idx = self.selected_index + 1
            new_text = f"▼ Cluster {cluster_idx}: {cluster_type}"
            self.cluster_button_text.set_text(new_text)
            self.canvas.draw_idle()
    

    
    def _get_all_children(self, widget):
        """Get all child widgets recursively"""
        children = []
        for child in widget.winfo_children():
            children.append(child)
            children.extend(self._get_all_children(child))
        return children
    
    def _confirm_selection(self):
        """Confirm the current selection"""
        if self.selected_cluster is None:
            messagebox.showwarning("No Selection", "Please select a cluster first.")
            return
        
        # Unbind shortcuts before closing
        self._unbind_preview_shortcut()
        
        # Call callback with the user-selected cluster
        if self.callback:
            self.callback(self.selected_cluster, self.selected_index)
        
        self.dialog.destroy()
    
    def _on_close_auto_select(self):
        """Handle window close by automatically using the best cluster"""
        _LOGGER.info("🤖 Dialog closed - automatically using best cluster")
        
        # Unbind shortcuts before closing
        self._unbind_preview_shortcut()
        
        if self.automatic_best and self.callback:
            # Robustly locate the automatic best index
            try:
                auto_index = self.all_candidates.index(self.automatic_best)
            except ValueError:
                auto_index = None
            if auto_index is None:
                # Fallback using (type, cluster_id)
                auto_index = next((idx for idx, cand in enumerate(self.all_candidates)
                                   if cand.get('type') == self.automatic_best.get('type') and
                                      cand.get('cluster_id') == self.automatic_best.get('cluster_id')), 0)
            # Safety fallback
            if auto_index is None:
                auto_index = 0
            # FIX: only 2 parameters as expected by the callback
            self.callback(self.automatic_best, auto_index)
        
        self.dialog.destroy()

    # ---------------------------------------------------------------------
    # Preview pop-up window helpers
    # ---------------------------------------------------------------------

    def _open_preview_window(self):
        """Show preview window with top-3 template overlays for current cluster"""
        if self.selected_cluster is None:
            messagebox.showwarning("No Selection", "Please select a cluster first.")
            return

        # If window already exists, just raise and update
        if self.preview_window and self.preview_window.winfo_exists():
            try:
                self.preview_window.lift()
                self._update_preview_window()
                return
            except tk.TclError:
                # Window exists but is invalid, clear the reference
                self.preview_window = None

        # Check if parent dialog still exists
        if not self.dialog or not self.dialog.winfo_exists():
            _LOGGER.warning("Parent dialog no longer exists, cannot create preview window")
            return

        # Create new window with error handling
        try:
            self.preview_window = tk.Toplevel(self.dialog)
            self.preview_window.title("🔍 Top-3 Templates Preview")
            self.preview_window.geometry("1100x800")
            self.preview_window.configure(bg=self.colors['bg_main'])

            # Close action
            self.preview_window.protocol("WM_DELETE_WINDOW", self._close_preview_window)

            # Build plots
            self._update_preview_window()
            
        except tk.TclError as e:
            _LOGGER.error(f"Failed to create preview window: {e}")
            self.preview_window = None
            messagebox.showerror("Preview Error", f"Could not create preview window: {e}")
        except Exception as e:
            _LOGGER.error(f"Unexpected error creating preview window: {e}")
            self.preview_window = None

    def _update_preview_window(self):
        """(Re)draw preview plots if the window is open"""
        if not (self.preview_window and self.preview_window.winfo_exists()):
            return  # Nothing to do
            
        try:
            # Test if window is still valid
            self.preview_window.winfo_exists()
        except tk.TclError:
            # Window is invalid, clear reference
            self.preview_window = None
            return

        try:
            # Clear existing widgets
            for child in self.preview_window.winfo_children():
                child.destroy()

            # Fetch top-3 matches
            candidate = self.selected_cluster
            from snid_sage.shared.utils.math_utils import get_best_metric_value
            matches = sorted(candidate.get('matches', []), key=get_best_metric_value, reverse=True)[:3]

            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            # Prepare observed spectrum
            input_wave = input_flux = None
            if (self.snid_result is not None and hasattr(self.snid_result, 'processed_spectrum') and
                    self.snid_result.processed_spectrum):
                input_wave = self.snid_result.processed_spectrum['log_wave']
                input_flux = self.snid_result.processed_spectrum['log_flux']
            elif (self.snid_result is not None and hasattr(self.snid_result, 'input_spectrum') and
                  isinstance(self.snid_result.input_spectrum, dict)):
                input_wave = self.snid_result.input_spectrum.get('wave')
                input_flux = self.snid_result.input_spectrum.get('flux')

            # Create figure with three subplots
            fig = plt.Figure(figsize=(12, 4), dpi=100)
            fig.patch.set_facecolor(self.colors['bg_main'])

            # Horizontal layout: 1 row, 3 columns
            axes = [fig.add_subplot(1, 3, i+1) for i in range(3)]
            for idx, ax in enumerate(axes):
                ax.set_facecolor('white')
                ax.tick_params(colors=self.colors['text_secondary'], labelsize=7)
                for spine in ax.spines.values():
                    spine.set_color(self.colors['text_secondary'])
                ax.grid(True, alpha=0.15)

                # Plot input spectrum
                if input_wave is not None and input_flux is not None:
                    ax.plot(input_wave, input_flux, color='#0078d4', linewidth=0.8, alpha=0.7, label='Input')

                # Plot template if exists
                if idx < len(matches):
                    match = matches[idx]
                    try:
                        t_wave = match['spectra']['flux']['wave']
                        t_flux = match['spectra']['flux']['flux']
                        ax.plot(t_wave, t_flux, color='#E74C3C', linewidth=0.9, alpha=0.8,
                                label=f"{match['name']}")
                    except Exception as e:
                        _LOGGER.debug(f"Preview plotting issue: {e}")

                    ax.set_title(f"#{idx+1} {match.get('name', '')} – RLAP {match.get('rlap', 0):.1f}  z {match.get('redshift', 0):.4f}",
                                 fontsize=10, color=self.colors['text_primary'])
                else:
                    ax.text(0.5, 0.5, 'No Match', transform=ax.transAxes,
                            ha='center', va='center', fontsize=9)

                ax.set_xlabel('λ (Å)', fontsize=7, color=self.colors['text_secondary'])
                ax.set_ylabel('Flux', fontsize=7, color=self.colors['text_secondary'])

            # Embed canvas
            canvas = FigureCanvasTkAgg(fig, master=self.preview_window)
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=8, pady=8)
            canvas.draw_idle()

            # Reduce whitespace between subplots
            fig.tight_layout(pad=2.0)
            
        except tk.TclError as e:
            _LOGGER.error(f"TclError in preview window update: {e}")
            # Window might have been destroyed, clear reference
            self.preview_window = None
        except Exception as e:
            _LOGGER.error(f"Error updating preview window: {e}")
            # Try to show error message in the window if it still exists
            try:
                if self.preview_window and self.preview_window.winfo_exists():
                    for child in self.preview_window.winfo_children():
                        child.destroy()
                    error_label = tk.Label(self.preview_window, 
                                         text=f"Error creating preview: {str(e)}",
                                         bg=self.colors['bg_main'], fg='red',
                                         font=('Segoe UI', 12))
                    error_label.pack(expand=True)
            except:
                self.preview_window = None

    # ---------------------------------------------------------------------
    # Shift-key bindings and footer button
    # ---------------------------------------------------------------------

    def _bind_preview_shortcut(self):
        """Bind Shift press/release to preview window display/dismiss with debouncing."""
        # Bind only to this specific dialog, not globally
        self.dialog.bind('<KeyPress-Shift_L>', self._on_shift_press)
        self.dialog.bind('<KeyPress-Shift_R>', self._on_shift_press)
        self.dialog.bind('<KeyRelease-Shift_L>', self._on_shift_release)
        self.dialog.bind('<KeyRelease-Shift_R>', self._on_shift_release)

    def _on_shift_press(self, event=None):
        if not self._shift_held:
            self._shift_held = True
            self._open_preview_window()

    def _on_shift_release(self, event=None):
        if self._shift_held:
            self._shift_held = False
            self._close_preview_window()

    def _close_preview_window(self):
        if self.preview_window and self.preview_window.winfo_exists():
            try:
                self.preview_window.destroy()
            except tk.TclError:
                # Window might already be destroyed
                pass
        self.preview_window = None
    
    def _unbind_preview_shortcut(self):
        """Unbind Shift key shortcuts when dialog is closed"""
        try:
            if self.dialog and self.dialog.winfo_exists():
                self.dialog.unbind('<KeyPress-Shift_L>')
                self.dialog.unbind('<KeyPress-Shift_R>')
                self.dialog.unbind('<KeyRelease-Shift_L>')
                self.dialog.unbind('<KeyRelease-Shift_R>')
        except tk.TclError:
            # Dialog might already be destroyed
            pass


    
    def _highlight_selected_cluster(self, cluster_index):
        """Highlight the selected cluster in the plot"""
        try:
            # Clear previous highlights
            self._clear_all_highlights()
            
            # Add highlight to selected cluster
            self._add_persistent_highlight(cluster_index)
            
            # Refresh the plot
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.draw()
                
        except Exception as e:
            _LOGGER.error(f"Error highlighting cluster: {e}")


def show_cluster_selection_dialog(parent, clustering_results, theme_manager, snid_result=None, callback=None):
    """Utility function to create and show the cluster selection dialog"""
    dialog = ClusterSelectionDialog(parent, clustering_results, theme_manager, snid_result=snid_result, callback=callback)
    dialog.dialog.grab_set()
    dialog.dialog.wait_window()
    return dialog.selected_cluster, dialog.selected_index

