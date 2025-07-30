"""
SNID SAGE - Dialog Controller
==============================

Handles dialog creation, management, and interactions for the SNID SAGE GUI.
Moved from sage_gui.py to reduce main file complexity.

Part of the SNID SAGE GUI restructuring - Controllers Module
"""

import tkinter as tk
from tkinter import messagebox
from snid_sage.interfaces.gui.components.dialogs import MaskManagerDialog
from snid_sage.interfaces.gui.components.dialogs import AISummaryDialog
from typing import Dict, Any

# Import centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.dialog_controller')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.dialog_controller')


class DialogController:
    """Manages dialogs and modal windows"""
    
    def __init__(self, gui_instance):
        """Initialize dialog controller with reference to main GUI"""
        self.gui = gui_instance
        self.open_dialogs = {}  # Track open dialogs
    
    def _get_version(self):
        """Get the current version of SNID SAGE"""
        try:
            from snid_sage import __version__
            return __version__
        except ImportError:
            return "unknown"
    
    def open_preprocessing_dialog(self):
        """Open preprocessing dialog - create and show the step-by-step wizard"""
        try:
            # Check if a spectrum is loaded
            if not hasattr(self.gui, 'file_path') or not self.gui.file_path:
                messagebox.showwarning("No Spectrum", "Please load a spectrum file first.")
                return
            
            # Import the modular preprocessing components from their new locations
            from snid_sage.interfaces.gui.features.preprocessing.spectrum_preprocessor import SpectrumPreprocessor
            from snid_sage.interfaces.gui.components.dialogs.preprocessing_dialog import PreprocessingDialog
            
            # Create a spectrum preprocessor instance
            preprocessor = SpectrumPreprocessor(self.gui)
            
            # Load the current spectrum into the preprocessor
            if preprocessor.load_spectrum(self.gui.file_path):
                # Create and show the step-by-step preprocessing dialog
                dialog = PreprocessingDialog(self.gui.master, preprocessor)
                
                # Register the dialog
                self.register_dialog('preprocessing', dialog)
                
                # Show the dialog - this is a non-blocking call that just displays the window
                # The dialog handles its own workflow and applies results in its on_close method
                dialog.show()
                
                _LOGGER.info("🔧 Advanced preprocessing dialog opened successfully")
                    
            else:
                messagebox.showerror("Error", "Failed to load spectrum for preprocessing.")
                
        except Exception as e:
            _LOGGER.error(f"❌ Error opening preprocessing dialog: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Could not open preprocessing dialog: {e}")
    
    def _apply_preprocessing_results(self, preprocessor, result):
        """Apply preprocessing results to the main GUI"""
        try:
            # Get the preprocessed spectrum from the preprocessor
            wave, flux = preprocessor.get_preprocessed_spectrum()
            
            # Store the preprocessed spectrum in the main GUI
            self.gui.processed_spectrum = {
                'log_wave': wave,
                'log_flux': flux,
                'display_flux': flux,
                'display_flat': flux,  # For now, use same data
                'preprocessing_trace': preprocessor.get_preprocessing_summary()
            }
            
            # Update the plot with the preprocessed spectrum
            self.gui.plot_preprocessed_spectrum(wave, flux)
            
            _LOGGER.info("✅ Applied preprocessing results to main GUI")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error applying preprocessing results: {e}")
            messagebox.showerror("Error", f"Failed to apply preprocessing results: {e}")
    
    def open_preprocessing_selection(self):
        """Open preprocessing selection dialog to choose between quick and advanced preprocessing"""
        try:
            # Check if a spectrum is loaded
            if not hasattr(self.gui, 'file_path') or not self.gui.file_path:
                messagebox.showwarning("No Spectrum", "Please load a spectrum file first.")
                return
            
            # Import the preprocessing selection dialog
            from snid_sage.interfaces.gui.components.dialogs.preprocessing_selection_dialog import PreprocessingSelectionDialog
            
            # Create and show the preprocessing selection dialog
            dialog = PreprocessingSelectionDialog(self.gui)
            dialog.show()
            
            _LOGGER.info("🔧 Preprocessing selection dialog opened successfully")
                
        except Exception as e:
            _LOGGER.error(f"❌ Error opening preprocessing selection dialog: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Could not open preprocessing selection dialog: {e}")

    def manage_masks(self):
        """Open mask manager dialog"""
        try:
            if not hasattr(self.gui, 'mask_manager_dialog') or self.gui.mask_manager_dialog is None:
                self.gui.mask_manager_dialog = MaskManagerDialog(self.gui)
            
            self.gui.mask_manager_dialog.show()
        except Exception as e:
            _LOGGER.error(f"❌ Error opening mask manager: {e}")
            messagebox.showerror("Error", f"Could not open mask manager: {e}")
    
    def configure_options(self):
        """Configure options - open simple SNID options dialog
        
        Returns:
            bool: True if options were configured and applied, False if cancelled
        """
        try:
            from snid_sage.interfaces.gui.components.dialogs.configuration_dialog import show_snid_options_dialog
            
            # Get current parameters from GUI
            current_params = {}
            if hasattr(self.gui, 'params'):
                # Extract the SNID parameters we need
                param_mapping = {
                    'zmin': self.gui.params.get('zmin', '-0.01'),
                    'zmax': self.gui.params.get('zmax', '1.0'),
                    'rlapmin': self.gui.params.get('rlapmin', '5.0'),
                    'lapmin': self.gui.params.get('lapmin', '0.3'),
                    'max_output_templates': self.gui.params.get('max_output_templates', '10'),
                    'age_min': self.gui.params.get('age_min', ''),
                    'age_max': self.gui.params.get('age_max', ''), 
                    'type_filter': self.gui.params.get('type_filter', ''),
                    'template_filter': self.gui.params.get('template_filter', []),
                    'save_plots': self.gui.params.get('save_plots', '0') == '1',
                    'save_summary': self.gui.params.get('save_summary', '0') == '1'
                }
                
                # Convert string values to appropriate types
                for key, value in param_mapping.items():
                    if key == 'template_filter':
                        # Keep template_filter as list
                        if isinstance(value, list):
                            current_params[key] = value
                        elif isinstance(value, str) and value:
                            # Parse comma-separated string to list
                            current_params[key] = [t.strip() for t in value.split(',') if t.strip()]
                        else:
                            current_params[key] = []
                    elif isinstance(value, str) and value:
                        if key in ['zmin', 'zmax', 'rlapmin', 'lapmin']:
                            try:
                                current_params[key] = float(value)
                            except ValueError:
                                pass  # Use defaults
                        elif key in ['max_output_templates']:
                            try:
                                current_params[key] = int(value)
                            except ValueError:
                                pass  # Use defaults
                        elif key in ['age_min', 'age_max'] and value:
                            try:
                                current_params[key] = float(value)
                            except ValueError:
                                pass  # Use defaults
                        else:
                            current_params[key] = value
                    elif isinstance(value, bool):
                        current_params[key] = value
            
            # Show the simple SNID options dialog
            result = show_snid_options_dialog(self.gui.master, current_params)
            
            if result:
                # Update GUI parameters with the results
                self._apply_snid_options(result)
                
                # Update header status
                if hasattr(self.gui, 'update_header_status'):
                    self.gui.update_header_status("⚙️ SNID options updated successfully")
                
                _LOGGER.info("✅ SNID options updated successfully")
                return True
            else:
                _LOGGER.info("⚪ SNID options dialog cancelled")
                return False
                
        except Exception as e:
            _LOGGER.error(f"❌ Error opening SNID options dialog: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Configuration Error", 
                               f"Failed to open SNID options dialog: {str(e)}")
            return False
    
    def _apply_snid_options(self, options: Dict[str, Any]):
        """Apply SNID options to GUI parameters"""
        try:
            if not hasattr(self.gui, 'params'):
                self.gui.params = {}
            
            # Update GUI params with new values
            for key, value in options.items():
                if key in ['save_plots', 'save_summary']:
                    # Convert boolean to string for GUI params
                    self.gui.params[key] = '1' if value else '0'
                elif key == 'template_filter':
                    # Keep template_filter as list for proper parsing
                    self.gui.params[key] = value
                else:
                    # Keep as string for GUI params
                    self.gui.params[key] = str(value)
            
            # Update any toggle variables if they exist
            if hasattr(self.gui, 'save_plots_toggle'):
                self.gui.save_plots_toggle.set(options.get('save_plots', False))
            if hasattr(self.gui, 'save_summary_toggle'):
                self.gui.save_summary_toggle.set(options.get('save_summary', False))
            
            # Update status display
            self._update_snid_options_status(options)
            
            print("✅ SNID options applied to GUI parameters")
            
        except Exception as e:
            print(f"❌ Error applying SNID options: {e}")
    
    def _update_snid_options_status(self, options: Dict[str, Any]):
        """Update the SNID options status display"""
        try:
            # Update main status label
            if hasattr(self.gui, 'config_status_label'):
                self.gui.config_status_label.config(text="⚙️ Custom SNID options active")
            
            # Update quick config summary
            if hasattr(self.gui, 'quick_config_label'):
                zmin = options.get('zmin', -0.01)
                zmax = options.get('zmax', 1.0)
                max_templates = options.get('max_output_templates', 10)
                
                # Add indicators for special settings
                indicators = []
                
                if options.get('save_plots', False):
                    indicators.append("P")  # Save plots
                if options.get('save_summary', False):
                    indicators.append("S")  # Save summary
                if options.get('type_filter'):
                    indicators.append("T")  # Type filter
                if options.get('age_min') or options.get('age_max'):
                    indicators.append("A")  # Age filter
                
                indicators_text = f" [{'.'.join(indicators)}]" if indicators else ""
                
                quick_text = f"z: {zmin:.2f} to {zmax:.1f} | Templates: {max_templates}{indicators_text}"
                self.gui.quick_config_label.config(text=quick_text)
            
            _LOGGER.info("📊 SNID options status display updated")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error updating SNID options status display: {e}")
    
    def show_results_summary(self, result):
        """Show comprehensive results summary dialog"""
        try:
            from snid_sage.interfaces.gui.components.dialogs.enhanced_ai_assistant_dialog import EnhancedAIAssistantDialog as AISummaryDialog
            
            # Create dialog with only gui_instance argument
            dialog = AISummaryDialog(self.gui)
            
            # Dialog themes itself independently, no need to register with main window theme manager
            
            # Show dialog with the result data
            dialog.show(snid_results=result)
            
            if self.gui.logger:
                self.gui.logger.info("📊 Opened AI-enhanced results summary dialog")
            
        except Exception as e:
            if self.gui.logger:
                self.gui.logger.error(f"Error showing results summary: {e}")
            messagebox.showerror("Results Summary Error", f"Failed to show results summary: {str(e)}")
    
    def show_ai_summary_dialog(self, analysis_result=None):
        """Show AI summary dialog"""
        try:
            from snid_sage.interfaces.gui.components.dialogs.enhanced_ai_assistant_dialog import EnhancedAIAssistantDialog as AISummaryDialog
            
            if 'ai_summary' not in self.open_dialogs or self.open_dialogs['ai_summary'] is None:
                self.open_dialogs['ai_summary'] = AISummaryDialog(self.gui)
            
            # Show dialog with analysis result data
            self.open_dialogs['ai_summary'].show(snid_results=analysis_result)
        except Exception as e:
            _LOGGER.error(f"❌ Error opening AI summary dialog: {e}")
            messagebox.showerror("Error", f"Could not open AI summary dialog: {e}")
    
    def show_line_detection_dialog(self):
        """Show line detection configuration dialog"""
        try:
            if hasattr(self.gui, 'line_detection_controller'):
                self.gui.line_detection_controller.configure_line_detection()
            else:
                messagebox.showerror("Error", "Line detection controller not initialized.")
        except Exception as e:
            _LOGGER.error(f"❌ Error opening line detection dialog: {e}")
            messagebox.showerror("Error", f"Could not open line detection dialog: {e}")
    
    def show_template_manager_dialog(self):
        """Show template manager dialog"""
        try:
            if hasattr(self.gui, 'template_manager'):
                # Create and show template manager dialog
                from tkinter import simpledialog
                messagebox.showinfo("Template Manager", 
                                  "Template manager functionality will be implemented here.")
            else:
                messagebox.showerror("Error", "Template manager not initialized.")
        except Exception as e:
            _LOGGER.error(f"❌ Error opening template manager dialog: {e}")
            messagebox.showerror("Error", f"Could not open template manager: {e}")
    
    def show_about_dialog(self):
        """Show about dialog"""
        try:
            about_text = (
                f"SNID SAGE v{self._get_version()}\n"
                "Modern GUI Interface\n\n"
                "SuperNova IDentification Spectral Analysis GUI Environment\n\n"
                "Developed by Fiorenzo Stoppa\n"
                "Based on the original Fortran SNID by Stéphane Blondin & John L. Tonry\n\n"
                "Features:\n"
                "• Modern toggle-based interface\n"
                "• Intelligent preprocessing\n"
                "• LLM integration for analysis\n"
                "• Advanced line detection\n"
                "• Interactive masking\n"
                "• Games during analysis\n\n"
                "© 2024 SNID SAGE Project"
            )
            messagebox.showinfo("About SNID SAGE", about_text)
        except Exception as e:
            _LOGGER.error(f"❌ Error showing about dialog: {e}")
    
    def show_help_dialog(self):
        """Show help dialog"""
        try:
            help_text = (
                "SNID SAGE Help\n\n"
                "Getting Started:\n"
                "1. Load a spectrum file using 'Browse & Load Spectrum File'\n"
                "2. Configure analysis options as needed\n"
                "3. Run SNID analysis\n\n"
                "Keyboard Shortcuts:\n"
                "• Ctrl+O: Open file\n"
                "• Ctrl+R: Run analysis\n"
                "• Ctrl+D: Toggle dark mode\n"
                "• Ctrl+P: Open preprocessing\n"
                "• Ctrl+M: Manage masks\n"
                "• Ctrl+G: Start games\n"
                "• F1: Show this help\n\n"
                "Features:\n"
                "• Toggle switches for easy configuration\n"
                "• Right-click plots for context menu\n"
                "• Drag to select wavelength ranges\n"
                "• LLM integration for intelligent analysis\n\n"
                "For more help, consult the documentation."
            )
            messagebox.showinfo("SNID SAGE Help", help_text)
        except Exception as e:
            _LOGGER.error(f"❌ Error showing help dialog: {e}")
    
    def close_dialog(self, dialog_name):
        """Close a specific dialog"""
        try:
            if dialog_name in self.open_dialogs:
                dialog = self.open_dialogs[dialog_name]
                if dialog and hasattr(dialog, 'destroy'):
                    dialog.destroy()
                self.open_dialogs[dialog_name] = None
        except Exception as e:
            _LOGGER.error(f"❌ Error closing dialog {dialog_name}: {e}")
    
    def close_all_dialogs(self):
        """Close all open dialogs"""
        try:
            for dialog_name in list(self.open_dialogs.keys()):
                self.close_dialog(dialog_name)
        except Exception as e:
            _LOGGER.error(f"❌ Error closing all dialogs: {e}")
    
    def is_dialog_open(self, dialog_name):
        """Check if a specific dialog is open"""
        return (dialog_name in self.open_dialogs and 
                self.open_dialogs[dialog_name] is not None)
    
    def register_dialog(self, dialog_name, dialog_instance):
        """Register a dialog instance"""
        self.open_dialogs[dialog_name] = dialog_instance
    
    def get_dialog(self, dialog_name):
        """Get a dialog instance"""
        return self.open_dialogs.get(dialog_name, None)

    # New method to create dialog window with proper theming support
    def create_dialog_with_theme(self, dialog_name, dialog_instance):
        """Create a dialog window with proper theming support"""
        try:
            # Create dialog window with proper theming support
            dialog = tk.Toplevel(self.gui.master)
            dialog.title("SNID-SAGE Analysis Results")
            dialog.geometry("900x700")
            dialog.resizable(True, True)
            
            # Register dialog with theme integration for proper theme updates
            if hasattr(self.gui, 'theme_integration'):
                self.gui.theme_integration.register_dialog(dialog)
            
            # Dialog themes itself independently, no need to apply main window theme
            
            # Register the dialog
            self.register_dialog(dialog_name, dialog_instance)
            
            _LOGGER.info(f"✅ {dialog_name} dialog created with theme support")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error creating {dialog_name} dialog: {e}")
            messagebox.showerror("Error", f"Could not create {dialog_name} dialog: {e}") 
