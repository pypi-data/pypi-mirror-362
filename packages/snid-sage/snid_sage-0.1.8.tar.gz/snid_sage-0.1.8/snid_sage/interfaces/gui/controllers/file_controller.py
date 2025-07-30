"""
File Controller for SNID SAGE GUI

Handles file operations including:
- File browsing and selection
- File loading and validation
- File format support
- File path management
- Recent files tracking

Extracted from sage_gui.py to improve maintainability and modularity.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np
from pathlib import Path
import logging

# Import unified systems for consistent plot styling
try:
    from snid_sage.interfaces.gui.utils.no_title_plot_manager import apply_no_title_styling
    UNIFIED_SYSTEMS_AVAILABLE = True
except ImportError:
    UNIFIED_SYSTEMS_AVAILABLE = False

_LOGGER = logging.getLogger(__name__)

class FileController:
    """Handles file operations and file-related functionality"""
    
    def __init__(self, gui_instance):
        """Initialize file controller with reference to main GUI"""
        self.gui = gui_instance
        
        # Supported file extensions
        self.supported_extensions = [
            '.txt', '.dat', '.spec', '.fits', '.fit', '.ascii', '.asci', '.csv',
            '.lnw', '.flm', '.sn', '.dat2', '.spectrum'
        ]
        
        # Recent files tracking
        self.recent_files = []
        self.max_recent_files = 10
    
    def _get_version(self):
        """Get the current version of SNID SAGE"""
        try:
            from snid_sage import __version__
            return __version__
        except ImportError:
            return "unknown"
    
    def browse_file(self):
        """Browse for a spectrum file"""
        try:
            # Define file types for the dialog
            filetypes = [
                ("All Spectrum Files", "*.txt *.dat *.spec *.fits *.fit *.ascii *.asci *.csv *.lnw *.flm *.sn *.dat2 *.spectrum"),
                ("Text Files", "*.txt *.dat *.ascii *.asci"),
                ("FITS Files", "*.fits *.fit"),
                ("SNID Templates", "*.lnw *.flm"),
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
            
            # Get initial directory
            initial_dir = self._get_initial_directory()
            
            # Show file dialog
            filename = filedialog.askopenfilename(
                title="Select Spectrum File",
                initialdir=initial_dir,
                filetypes=filetypes
            )
            
            if filename:
                # Validate and load the file
                success = self.load_spectrum_file(filename)
                if success:
                    self._add_to_recent_files(filename)
                    self._update_file_status(filename)
                    
                    # Update button states after successful file load
                    if hasattr(self.gui, 'app_controller'):
                        self.gui.app_controller.update_button_states()
                    
                    # Update header status
                    self.gui.update_header_status(f"📁 Loaded: {os.path.basename(filename)}")
                    
                    _LOGGER.info(f"✅ File loaded successfully: {filename}")
                else:
                    self.gui.update_header_status("❌ Failed to load spectrum file")
                    
        except Exception as e:
            print(f"❌ Error browsing for file: {e}")
            messagebox.showerror("File Browse Error", f"Failed to browse for file: {str(e)}")
    
    def load_spectrum_file(self, filename):
        """Load and validate a spectrum file"""
        try:
            # Check if file exists
            if not os.path.exists(filename):
                messagebox.showerror("File Not Found", f"File not found: {filename}")
                return False
            
            # Check file extension
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in self.supported_extensions:
                result = messagebox.askyesno(
                    "Unsupported File Type",
                    f"File extension '{file_ext}' is not in the supported list.\n\n"
                    f"Supported extensions: {', '.join(self.supported_extensions)}\n\n"
                    "Do you want to try loading it anyway?"
                )
                if not result:
                    return False
            
            # Try to load the file
            wave, flux = self._load_spectrum_data(filename)
            
            if wave is None or flux is None:
                messagebox.showerror("Load Error", 
                                   f"Failed to load spectrum data from {filename}")
                return False
            
            # Validate the data
            if not self._validate_spectrum_data(wave, flux):
                return False
            
            # COMPREHENSIVE RESET: Clear all previous spectrum state before loading new one
            # This ensures the application starts completely fresh with the new spectrum
            if hasattr(self.gui, 'spectrum_reset_manager') and self.gui.spectrum_reset_manager:
                self.gui.spectrum_reset_manager.reset_for_new_spectrum(preserve_file_path=True)
            else:
                # Fallback to manual reset if reset manager is not available
                self._manual_reset_spectrum_state()
            
            # Store the loaded data
            self.gui.file_path = filename
            self.gui.original_wave = wave
            self.gui.original_flux = flux
            
            # Enable view navigation (up/down) buttons as soon as a spectrum is loaded
            # This lets users switch between Flux and Flat without waiting for analysis
            if hasattr(self.gui, 'up_btn') and self.gui.up_btn:
                try:
                    self.gui.up_btn.configure(state='normal', relief='raised', bd=2)
                except Exception:
                    pass

            if hasattr(self.gui, 'down_btn') and self.gui.down_btn:
                try:
                    self.gui.down_btn.configure(state='normal', relief='raised', bd=2)
                except Exception:
                    pass
            
            # Plot the spectrum if matplotlib is available
            self._plot_loaded_spectrum(wave, flux)
            
            # CRITICAL: Set view to Flux mode when loading original spectrum
            if hasattr(self.gui, 'view_style') and self.gui.view_style:
                self.gui.view_style.set("Flux")
                _LOGGER.info("🔄 View mode set to Flux after loading spectrum")
                
                # Update segmented control buttons
                if hasattr(self.gui, '_update_segmented_control_buttons'):
                    self.gui._update_segmented_control_buttons()
                    _LOGGER.debug("✅ Segmented control buttons updated for Flux view")
            
            # CRITICAL: Trigger state transition to FILE_LOADED
            # This will enable preprocessing button with amber color
            if hasattr(self.gui, 'workflow_integrator') and self.gui.workflow_integrator:
                # Use the workflow integrator to trigger FILE_LOADED state
                self.gui.workflow_integrator.set_file_loaded()
                _LOGGER.info("🔄 File loaded: Workflow state set to FILE_LOADED (preprocess button should turn amber)")
            else:
                _LOGGER.error("❌ No workflow integrator available - buttons will not update correctly!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading spectrum file: {e}")
            messagebox.showerror("Load Error", f"Failed to load spectrum: {str(e)}")
            return False
    
    def _load_spectrum_data(self, filename):
        """Load spectrum data from file"""
        try:
            # Try different loading methods based on file extension
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext in ['.fits', '.fit']:
                return self._load_fits_spectrum(filename)
            else:
                return self._load_text_spectrum(filename)
                
        except Exception as e:
            print(f"❌ Error loading spectrum data: {e}")
            return None, None
    
    def _load_fits_spectrum(self, filename):
        """Load spectrum from FITS file"""
        try:
            from astropy.io import fits
            
            with fits.open(filename) as hdul:
                # Try to extract wavelength and flux
                data = hdul[0].data
                header = hdul[0].header
                
                if data is None:
                    raise ValueError("FITS file contains no data")
                
                if data.ndim == 1:
                    # Simple 1D spectrum
                    flux = data
                    # Try to construct wavelength from header
                    if 'CRVAL1' in header:
                        start = header['CRVAL1']
                        step = header.get('CD1_1', header.get('CDELT1', 1.0))
                        wave = np.arange(len(flux)) * step + start
                    else:
                        # Default wavelength grid
                        wave = np.arange(len(flux))
                        
                elif data.ndim == 2:
                    # 2D data - could be [wavelength, flux] or multiple spectra
                    if data.shape[0] == 2:
                        # Assume [wavelength, flux] format
                        wave = data[0]
                        flux = data[1]
                    elif data.shape[1] == 2:
                        # Assume columns are [wavelength, flux]
                        wave = data[:, 0]
                        flux = data[:, 1]
                    else:
                        # Take first spectrum and construct wavelength
                        flux = data[0] if data.shape[0] < data.shape[1] else data[:, 0]
                        if 'CRVAL1' in header:
                            start = header['CRVAL1']
                            step = header.get('CD1_1', header.get('CDELT1', 1.0))
                            wave = np.arange(len(flux)) * step + start
                        else:
                            wave = np.arange(len(flux))
                            
                elif data.ndim == 3:
                    # 3D data - common for spectroscopic FITS files
                    # Shape is typically (bands, spatial, wavelength)
                    # Take first band (usually the cleaned spectrum), first spatial pixel
                    flux = data[0, 0, :]
                    
                    # Construct wavelength from header
                    if 'CRVAL1' in header:
                        start = header['CRVAL1']
                        step = header.get('CD1_1', header.get('CDELT1', 1.0))
                        wave = np.arange(len(flux)) * step + start
                    else:
                        wave = np.arange(len(flux))
                    
                    # Print band information if available
                    band_key = 'BANDID1'  # First band
                    if band_key in header:
                        _LOGGER.info(f"✅ Loaded FITS band 0: {header[band_key]}")
                        
                else:
                    raise ValueError(f"Unsupported FITS data dimensions: {data.ndim}D")
                
                # Convert to float arrays
                wave = np.asarray(wave, dtype=float)
                flux = np.asarray(flux, dtype=float)
                
                _LOGGER.info(f"✅ GUI FITS spectrum loaded: {len(wave)} points, "
                              f"λ = {wave[0]:.1f}-{wave[-1]:.1f} Å")
                
                return wave, flux
                
        except ImportError:
            messagebox.showerror("FITS Support Error", 
                               "FITS file support requires astropy.\n"
                               "Please install astropy to load FITS files.")
            return None, None
        except Exception as e:
            print(f"❌ Error loading FITS file: {e}")
            return None, None
    
    def _load_text_spectrum(self, filename):
        """Load spectrum from text file"""
        # First, check if file has headers by examining the first line
        try:
            with open(filename, 'r') as f:
                first_line = f.readline().strip()
                # Check if first line contains obvious header keywords
                header_keywords = ['WAVE', 'FLUX', 'WAVELENGTH', 'SPECTRUM', 'LAMBDA', 'COUNTS']
                has_header = any(keyword.upper() in first_line.upper() for keyword in header_keywords)
                
                # If first line has text that looks like a header, try skipping it
                if has_header:
                    try:
                        data = np.loadtxt(filename, skiprows=1)
                        if data.ndim == 2 and data.shape[1] >= 2:
                            wave = data[:, 0]
                            flux = data[:, 1]
                            # Add automatic unit conversion
                            wave = self._detect_and_convert_wavelength_units(wave)
                            _LOGGER.info(f"✅ GUI: Text spectrum loaded (header skipped): {len(wave)} points")
                            return wave, flux
                    except Exception:
                        pass  # Fall through to other methods
                
                # Also check if the first line doesn't look like numbers
                parts = first_line.split()
                if len(parts) >= 2:
                    try:
                        float(parts[0])
                        float(parts[1])
                        # First line looks like numbers, don't skip
                    except ValueError:
                        # First line doesn't look like numbers, try skipping
                        try:
                            data = np.loadtxt(filename, skiprows=1)
                            if data.ndim == 2 and data.shape[1] >= 2:
                                wave = data[:, 0]
                                flux = data[:, 1]
                                # Add automatic unit conversion
                                wave = self._detect_and_convert_wavelength_units(wave)
                                _LOGGER.info(f"✅ GUI: Text spectrum loaded (non-numeric header skipped): {len(wave)} points")
                                return wave, flux
                        except Exception:
                            pass  # Fall through to other methods
        except:
            pass  # Fall through to standard loading
        
        try:
            # Try to load as space/tab delimited text
            data = np.loadtxt(filename)
            
            if data.ndim == 1:
                # Single column - assume it's flux, create wavelength grid
                flux = data
                wave = np.arange(len(flux))
            elif data.ndim == 2:
                if data.shape[1] >= 2:
                    # Two or more columns - assume [wavelength, flux, ...]
                    wave = data[:, 0]
                    flux = data[:, 1]
                else:
                    # Single column in 2D array
                    flux = data[:, 0]
                    wave = np.arange(len(flux))
            else:
                raise ValueError("Unsupported data format")
            
            # Add automatic unit conversion
            wave = self._detect_and_convert_wavelength_units(wave)
            return wave, flux
            
        except (ValueError, TypeError) as e:
            # Check if error might be due to headers
            if "could not convert string to float" in str(e) or "invalid literal" in str(e):
                # Try skipping potential headers
                for skip_rows in [1, 2, 3]:
                    try:
                        data = np.loadtxt(filename, skiprows=skip_rows)
                        if data.ndim == 2 and data.shape[1] >= 2:
                            wave = data[:, 0]
                            flux = data[:, 1]
                            # Add automatic unit conversion
                            wave = self._detect_and_convert_wavelength_units(wave)
                            return wave, flux
                    except (ValueError, TypeError):
                        continue
            
            # Try alternative loading methods
            try:
                # Try with comma delimiter
                data = np.loadtxt(filename, delimiter=',')
                if data.ndim == 2 and data.shape[1] >= 2:
                    wave = data[:, 0]
                    flux = data[:, 1]
                    # Add automatic unit conversion
                    wave = self._detect_and_convert_wavelength_units(wave)
                    return wave, flux
            except:
                pass
            
            # Try pandas if available
            try:
                import pandas as pd
                df = pd.read_csv(filename, sep=r'\s+', header=None)
                if len(df.columns) >= 2:
                    wave = df.iloc[:, 0].values
                    flux = df.iloc[:, 1].values
                    # Add automatic unit conversion
                    wave = self._detect_and_convert_wavelength_units(wave)
                    return wave, flux
            except ImportError:
                pass
            except:
                pass
            
            print(f"❌ Could not parse text file: {e}")
            return None, None
    
    def _detect_and_convert_wavelength_units(self, wavelength):
        """
        Detect wavelength units and convert to Angstroms if necessary.
        
        Parameters:
            wavelength: Wavelength array
            
        Returns:
            np.ndarray: Wavelength array in Angstroms
        """
        wavelength = np.asarray(wavelength, dtype=float)
        
        if len(wavelength) == 0:
            return wavelength
            
        min_wave = np.min(wavelength)
        max_wave = np.max(wavelength)
        
        # Detect likely units based on typical ranges
        if min_wave > 100 and max_wave < 1000:
            # Likely nanometers (nm) - convert to Angstroms
            wavelength_converted = wavelength * 10.0
            _LOGGER.info(f"🔄 GUI: Wavelength units detected as nanometers (nm)")
            _LOGGER.debug(f"   Converting: {min_wave:.1f}-{max_wave:.1f} nm → "
                  f"{wavelength_converted[0]:.1f}-{wavelength_converted[-1]:.1f} Å")
            return wavelength_converted
            
        elif min_wave > 0.1 and max_wave < 10:
            # Likely micrometers (μm) - convert to Angstroms
            wavelength_converted = wavelength * 10000.0
            _LOGGER.info(f"🔄 GUI: Wavelength units detected as micrometers (μm)")
            _LOGGER.debug(f"   Converting: {min_wave:.2f}-{max_wave:.2f} μm → "
                  f"{wavelength_converted[0]:.1f}-{wavelength_converted[-1]:.1f} Å")
            return wavelength_converted
            
        elif min_wave > 1000 and max_wave < 100000:
            # Likely already in Angstroms
            _LOGGER.info(f"✅ GUI: Wavelength units detected as Angstroms (Å): {min_wave:.1f}-{max_wave:.1f} Å")
            return wavelength
            
        else:
            # Unknown units - warn but don't convert
            _LOGGER.warning(f"⚠️ GUI: Unknown wavelength units detected (range: {min_wave:.2f}-{max_wave:.2f}). "
                  "Assuming Angstroms. Please verify units manually.")
            return wavelength
    
    def _validate_spectrum_data(self, wave, flux):
        """Validate loaded spectrum data"""
        try:
            # Check if arrays are not empty
            if len(wave) == 0 or len(flux) == 0:
                messagebox.showerror("Invalid Data", "Spectrum data is empty")
                return False
            
            # Check if arrays have same length
            if len(wave) != len(flux):
                messagebox.showerror("Invalid Data", 
                                   f"Wavelength and flux arrays have different lengths:\n"
                                   f"Wavelength: {len(wave)} points\n"
                                   f"Flux: {len(flux)} points")
                return False
            
            # Check for valid numeric data
            if not np.all(np.isfinite(wave)) or not np.all(np.isfinite(flux)):
                # Count and report non-finite values
                bad_wave = np.sum(~np.isfinite(wave))
                bad_flux = np.sum(~np.isfinite(flux))
                
                if bad_wave > 0 or bad_flux > 0:
                    result = messagebox.askyesno(
                        "Data Quality Warning",
                        f"Spectrum contains non-finite values:\n"
                        f"Bad wavelength points: {bad_wave}\n"
                        f"Bad flux points: {bad_flux}\n\n"
                        "Do you want to continue loading? "
                        "(Non-finite values will be filtered out)"
                    )
                    if not result:
                        return False
            
            # Check for reasonable data ranges
            wave_range = np.ptp(wave[np.isfinite(wave)])
            if wave_range <= 0:
                messagebox.showerror("Invalid Data", "Wavelength data has no range")
                return False
            
            # Warn about unusual wavelength ranges
            min_wave = np.min(wave[np.isfinite(wave)])
            max_wave = np.max(wave[np.isfinite(wave)])
            
            if min_wave < 1000 or max_wave > 50000:
                result = messagebox.askyesno(
                    "Wavelength Range Warning",
                    f"Unusual wavelength range detected:\n"
                    f"Range: {min_wave:.1f} - {max_wave:.1f}\n\n"
                    "Typical optical spectra range from ~3000-10000 Å.\n"
                    "Do you want to continue?"
                )
                if not result:
                    return False
            
            _LOGGER.info(f"✅ Spectrum validation passed: {len(wave)} points, "
                  f"wavelength range {float(min_wave):.1f}-{float(max_wave):.1f} Å")
            
            return True
            
        except Exception as e:
            print(f"❌ Error validating spectrum data: {e}")
            messagebox.showerror("Validation Error", f"Error validating spectrum: {str(e)}")
            return False
    
    def _plot_loaded_spectrum(self, wave, flux):
        """Plot the loaded spectrum"""
        try:
            # Store data in GUI and use plot controller
            # This ensures proper matplotlib initialization after reset
            self.gui.original_wave = wave
            self.gui.original_flux = flux
            
            # Use plot controller if available (proper method)
            if hasattr(self.gui, 'plot_controller') and self.gui.plot_controller:
                # Initialize matplotlib if needed (especially after reset)
                if not hasattr(self.gui, 'ax') or self.gui.ax is None:
                    _LOGGER.info("🔧 Initializing matplotlib plot for loaded spectrum")
                    self.gui.plot_controller.init_matplotlib_plot()
                
                # Verify matplotlib components are valid
                if not self.gui.plot_controller._matplotlib_components_valid():
                    _LOGGER.info("🔧 Reinitializing matplotlib components after reset")
                    self.gui.plot_controller.init_matplotlib_plot()
                
                # Use plot controller to plot original spectrum
                self.gui.plot_controller.plot_original_spectrum()
                _LOGGER.info("✅ Spectrum plotted via plot controller")
                return
            
            # FALLBACK: Direct plotting if plot controller not available
            _LOGGER.warning("⚠️ Plot controller not available, using fallback plotting")
            
            # Check if matplotlib plot is available
            if not hasattr(self.gui, 'ax') or not self.gui.ax:
                # Try to initialize matplotlib if not done yet
                if hasattr(self.gui, 'init_matplotlib_plot'):
                    self.gui.init_matplotlib_plot()
                else:
                    print("⚠️ Matplotlib plot not available yet")
                    return
            
            # Clear previous plot
            self.gui.ax.clear()
            
            # Filter out non-finite values for plotting
            mask = np.isfinite(wave) & np.isfinite(flux)
            wave_clean = wave[mask]
            flux_clean = flux[mask]
            
            if len(wave_clean) == 0:
                self.gui.ax.text(0.5, 0.5, 'No valid data to plot', 
                               transform=self.gui.ax.transAxes, 
                               ha='center', va='center')
            else:
                # FIXED: Use the same nice blue color as preprocessing plots
                spectrum_color = '#0078d4'  # Nice blue matching preprocessing dialog
                
                # Plot the spectrum
                self.gui.ax.plot(wave_clean, flux_clean, color=spectrum_color, linewidth=2, alpha=0.8)
                self.gui.ax.set_xlabel('Wavelength (Å)')
                self.gui.ax.set_ylabel('Flux')
                # Apply no-title styling per user requirement
                if UNIFIED_SYSTEMS_AVAILABLE:
                    apply_no_title_styling(self.gui.fig, self.gui.ax, "Wavelength (Å)", "Flux", 
                                         getattr(self.gui, 'theme_manager', None))
                self.gui.ax.grid(True, alpha=0.3)
            
            # Update the plot
            if hasattr(self.gui, 'canvas'):
                self.gui.canvas.draw()
            
            _LOGGER.info("✅ Spectrum plotted successfully (fallback method)")
            
        except Exception as e:
            print(f"❌ Error plotting spectrum: {e}")
            # Try one more time to reinitialize everything
            try:
                _LOGGER.info("🔧 Attempting to reinitialize plot area after error")
                if hasattr(self.gui, 'plot_controller') and self.gui.plot_controller:
                    self.gui.plot_controller.init_matplotlib_plot()
                    self.gui.plot_controller.plot_original_spectrum()
                    _LOGGER.info("✅ Spectrum plotted successfully on retry")
            except Exception as retry_error:
                _LOGGER.error(f"❌ Failed to plot spectrum even after retry: {retry_error}")
                # Don't fail the loading process just because plotting failed
    
    def _get_initial_directory(self):
        """Get initial directory for file dialog"""
        try:
            # Try recent files first
            if self.recent_files:
                return os.path.dirname(self.recent_files[0])
            
            # Try current file directory
            if hasattr(self.gui, 'file_path') and self.gui.file_path:
                return os.path.dirname(self.gui.file_path)
            
            # Try common data directories
            common_dirs = [
                './data',
                './spectra',
                './examples',
                os.path.expanduser('~/Documents'),
                os.path.expanduser('~/Desktop'),
                '.'
            ]
            
            for dir_path in common_dirs:
                if os.path.exists(dir_path):
                    return dir_path
            
            return '.'
            
        except Exception:
            return '.'
    
    def _add_to_recent_files(self, filename):
        """Add file to recent files list"""
        try:
            filename = os.path.abspath(filename)
            
            # Remove if already in list
            if filename in self.recent_files:
                self.recent_files.remove(filename)
            
            # Add to beginning
            self.recent_files.insert(0, filename)
            
            # Limit list size
            if len(self.recent_files) > self.max_recent_files:
                self.recent_files = self.recent_files[:self.max_recent_files]
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error updating recent files: {e}")
    
    def _update_file_status(self, filename):
        """Update file status display"""
        try:
            if hasattr(self.gui, 'file_status_label'):
                # Show just the filename, not the full path
                display_name = os.path.basename(filename)
                if len(display_name) > 40:
                    display_name = display_name[:37] + "..."
                
                self.gui.file_status_label.configure(
                    text=f"✅ {display_name}",
                    fg=self.gui.theme_manager.get_color('success') if hasattr(self.gui, 'theme_manager') else 'green'
                )
            
            # Clear any previous redshift determination when loading new file
            if hasattr(self.gui, 'clear_redshift_status'):
                self.gui.clear_redshift_status()
            
            # Update window title
            self.gui.master.title(f"SNID SAGE v{self._get_version()} - {os.path.basename(filename)}")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error updating file status: {e}")
    
    def get_recent_files(self):
        """Get list of recent files"""
        # Filter out files that no longer exist
        self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
        return self.recent_files.copy()
    
    def clear_recent_files(self):
        """Clear recent files list"""
        self.recent_files.clear()
        _LOGGER.info("🗑️ Recent files list cleared")
    
    def _manual_reset_spectrum_state(self):
        """
        Manual fallback reset for when spectrum_reset_manager is not available
        This is a simplified version of the comprehensive reset
        """
        _LOGGER.debug("🔄 Performing manual spectrum state reset (fallback)...")
        
        # Reset processing state
        self.gui.processed_spectrum = None
        self.gui.preprocessed_wave = None
        self.gui.preprocessed_flux = None
        self.gui.snid_results = None
        self.gui.snid_trace = None
        
        # Reset template navigation
        if hasattr(self.gui, 'current_template'):
            self.gui.current_template = 0
        
        # Clear any existing plots
        if hasattr(self.gui, 'ax') and self.gui.ax:
            self.gui.ax.clear()
            if hasattr(self.gui, 'canvas'):
                self.gui.canvas.draw()
        
        _LOGGER.debug("✅ Manual spectrum state reset completed") 
