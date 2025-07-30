"""
Spectrum Loader Module for SNID SAGE
====================================

Unified spectrum loading functionality supporting multiple file formats:
- ASCII/text files (.txt, .dat, .ascii, .asci, .csv)
- FITS files (.fits, .fit)
- Various delimited formats

This module provides a consistent interface for loading spectrum data
regardless of the file format.
"""

import os
import numpy as np
from typing import Tuple, Optional, Dict, Any
import warnings
from pathlib import Path

from snid_sage.shared.types.spectrum_types import SpectrumData, SpectrumFormat
from snid_sage.shared.exceptions.core_exceptions import SpectrumLoadError

# Use centralized logging system
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('data_io.spectrum_loader')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('data_io.spectrum_loader')


def load_spectrum(filename: str, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load a spectrum from various file formats.
    
    Parameters:
        filename (str): Path to spectrum file
        **kwargs: Additional arguments passed to format-specific loaders
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Wavelength and flux arrays
        
    Raises:
        SpectrumLoadError: If the file cannot be loaded or parsed
    """
    if not os.path.exists(filename):
        raise SpectrumLoadError(f"File not found: {filename}")
    
    file_ext = Path(filename).suffix.lower()
    
    try:
        if file_ext in ['.fits', '.fit']:
            return load_fits_spectrum(filename, **kwargs)
        else:
            return load_text_spectrum(filename, **kwargs)
    except Exception as e:
        raise SpectrumLoadError(f"Failed to load spectrum from {filename}: {str(e)}")


def load_fits_spectrum(filename: str, band: int = 0, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load a spectrum from a FITS file.
    
    Parameters:
        filename (str): Path to FITS file
        band (int): Which band/extension to load (default: 0 for primary spectrum)
        **kwargs: Additional arguments (for compatibility)
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Wavelength and flux arrays
        
    Raises:
        SpectrumLoadError: If FITS file cannot be loaded or parsed
    """
    try:
        from astropy.io import fits
    except ImportError:
        raise SpectrumLoadError(
            "FITS file support requires astropy. Please install astropy: pip install astropy"
        )
    
    try:
        with fits.open(filename) as hdul:
            header = hdul[0].header
            data = hdul[0].data
            
            if data is None:
                raise SpectrumLoadError("FITS file contains no data")
            
            # Handle different data structures
            if data.ndim == 1:
                # Simple 1D spectrum
                flux = data
                wavelength = _construct_wavelength_axis(header, len(flux))
                
            elif data.ndim == 2:
                # 2D data - could be [wavelength, flux] or multiple spectra
                if data.shape[0] == 2:
                    # Assume [wavelength, flux] format
                    wavelength = data[0]
                    flux = data[1]
                elif data.shape[1] == 2:
                    # Assume columns are [wavelength, flux]
                    wavelength = data[:, 0]
                    flux = data[:, 1]
                else:
                    # Take first spectrum and construct wavelength
                    flux = data[0] if data.shape[0] < data.shape[1] else data[:, 0]
                    wavelength = _construct_wavelength_axis(header, len(flux))
                    
            elif data.ndim == 3:
                # 3D data - common for spectroscopic FITS files
                # Shape is typically (bands, spatial, wavelength)
                
                # Validate band selection
                if band >= data.shape[0]:
                    available_bands = data.shape[0]
                    warnings.warn(f"Band {band} requested but only {available_bands} bands available. Using band 0.")
                    band = 0
                
                # Extract spectrum from specified band, first spatial pixel
                flux = data[band, 0, :]
                wavelength = _construct_wavelength_axis(header, len(flux))
                
                # Print band information for user
                band_info = _get_band_info(header, band)
                if band_info:
                    _LOGGER.info(f"✅ Loaded FITS band {band}: {band_info}")
                
            else:
                raise SpectrumLoadError(f"Unsupported FITS data dimensions: {data.ndim}D")
            
            # Validate the extracted data
            wavelength, flux = _validate_and_clean_arrays(wavelength, flux)
            
            _LOGGER.info(f"✅ FITS spectrum loaded: {len(wavelength)} points, "
                  f"λ = {wavelength[0]:.1f}-{wavelength[-1]:.1f} Å")
            
            return wavelength, flux
            
    except SpectrumLoadError:
        raise
    except Exception as e:
        raise SpectrumLoadError(f"Error reading FITS file {filename}: {str(e)}")


def load_text_spectrum(filename: str, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load a spectrum from a text file.
    
    Parameters:
        filename (str): Path to text file
        **kwargs: Additional arguments for numpy.loadtxt
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Wavelength and flux arrays
        
    Raises:
        SpectrumLoadError: If text file cannot be loaded or parsed
    """
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
                    data = np.loadtxt(filename, comments='#', skiprows=1, **kwargs)
                    if data.ndim == 2 and data.shape[1] >= 2:
                        wavelength = data[:, 0]
                        flux = data[:, 1]
                        # Validate the data
                        wavelength, flux = _validate_and_clean_arrays(wavelength, flux)
                        _LOGGER.info(f"✅ Text spectrum loaded (header skipped): {len(wavelength)} points")
                        return wavelength, flux
                except Exception as e:
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
                        data = np.loadtxt(filename, comments='#', skiprows=1, **kwargs)
                        if data.ndim == 2 and data.shape[1] >= 2:
                            wavelength = data[:, 0]
                            flux = data[:, 1]
                            # Validate the data
                            wavelength, flux = _validate_and_clean_arrays(wavelength, flux)
                            _LOGGER.info(f"✅ Text spectrum loaded (non-numeric header skipped): {len(wavelength)} points")
                            return wavelength, flux
                    except Exception:
                        pass  # Fall through to other methods
    except:
        pass  # Fall through to standard loading
    
    try:
        # Try standard space/tab delimited loading
        data = np.loadtxt(filename, comments='#', **kwargs)
        
        if data.ndim == 1:
            # Single column - assume flux only
            flux = data
            wavelength = np.arange(len(flux), dtype=float)
            warnings.warn("Single column detected - generating sequential wavelength values")
            
        elif data.ndim == 2:
            if data.shape[1] >= 2:
                # Two or more columns - assume [wavelength, flux, ...]
                wavelength = data[:, 0]
                flux = data[:, 1]
            else:
                # Single column in 2D array
                flux = data[:, 0]
                wavelength = np.arange(len(flux), dtype=float)
                warnings.warn("Single column detected - generating sequential wavelength values")
        else:
            raise SpectrumLoadError(f"Unsupported data dimensions: {data.ndim}D")
        
        # Validate the data
        wavelength, flux = _validate_and_clean_arrays(wavelength, flux)
        
        _LOGGER.info(f"✅ Text spectrum loaded: {len(wavelength)} points")
        
        return wavelength, flux
        
    except (ValueError, TypeError) as e:
        # Check if the error might be due to headers or mixed data types
        if "could not convert string to float" in str(e) or "invalid literal" in str(e):
            # Try loading with skiprows to skip potential headers
            try:
                return _try_header_aware_loading(filename)
            except Exception:
                pass
        
        # Try alternative loading methods
        try:
            return _try_alternative_text_loading(filename)
        except Exception:
            raise SpectrumLoadError(f"Error reading text file {filename}: {str(e)}")
    except SpectrumLoadError:
        raise
    except Exception as e:
        # Try alternative loading methods
        try:
            return _try_alternative_text_loading(filename)
        except Exception:
            raise SpectrumLoadError(f"Error reading text file {filename}: {str(e)}")


def _construct_wavelength_axis(header: Dict[str, Any], n_pixels: int) -> np.ndarray:
    """
    Construct wavelength axis from FITS header WCS information.
    
    Parameters:
        header: FITS header dictionary
        n_pixels: Number of pixels in the spectrum
        
    Returns:
        np.ndarray: Wavelength array
    """
    # Try different WCS keywords
    if 'CRVAL1' in header:
        # Linear WCS
        start_wave = header['CRVAL1']
        ref_pixel = header.get('CRPIX1', 1.0)  # 1-based indexing
        
        # Try different step size keywords
        if 'CD1_1' in header:
            step = header['CD1_1']
        elif 'CDELT1' in header:
            step = header['CDELT1']
        else:
            step = 1.0
            warnings.warn("No wavelength step found in header, using step=1")
        
        # Calculate wavelengths
        # FITS uses 1-based indexing, convert to 0-based
        pixel_indices = np.arange(n_pixels, dtype=float)
        wavelength = start_wave + (pixel_indices - (ref_pixel - 1)) * step
        
    else:
        # Fallback to sequential values
        wavelength = np.arange(n_pixels, dtype=float)
        warnings.warn("No WCS information found in FITS header, using sequential values")
    
    return wavelength


def _get_band_info(header: Dict[str, Any], band: int) -> Optional[str]:
    """
    Extract band information from FITS header.
    
    Parameters:
        header: FITS header dictionary
        band: Band index
        
    Returns:
        Optional[str]: Band description if available
    """
    band_key = f'BANDID{band + 1}'  # FITS uses 1-based indexing
    return header.get(band_key, None)


def _validate_and_clean_arrays(wavelength: np.ndarray, flux: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Validate and clean wavelength and flux arrays.
    
    Parameters:
        wavelength: Wavelength array
        flux: Flux array
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Cleaned arrays
        
    Raises:
        SpectrumLoadError: If arrays are invalid
    """
    # Convert to numpy arrays and ensure they are numeric
    try:
        wavelength = np.asarray(wavelength, dtype=float)
        flux = np.asarray(flux, dtype=float)
    except (ValueError, TypeError) as e:
        raise SpectrumLoadError(f"Cannot convert data to numeric arrays: {str(e)}")
    
    # Check lengths match
    if len(wavelength) != len(flux):
        raise SpectrumLoadError(
            f"Wavelength and flux arrays have different lengths: "
            f"{len(wavelength)} vs {len(flux)}"
        )
    
    # Check for empty arrays
    if len(wavelength) == 0:
        raise SpectrumLoadError("Empty spectrum data")
    
    # Remove NaN and infinite values
    try:
        mask = np.isfinite(wavelength) & np.isfinite(flux)
        n_bad = np.sum(~mask)
        
        if n_bad > 0:
            warnings.warn(f"Removed {n_bad} non-finite data points")
            wavelength = wavelength[mask]
            flux = flux[mask]
    except TypeError as e:
        # Handle cases where isfinite fails on non-numeric data
        raise SpectrumLoadError(f"Data contains non-numeric values: {str(e)}")
    
    # Check if anything remains
    if len(wavelength) == 0:
        raise SpectrumLoadError("No valid data points after cleaning")
    
    # Automatic unit detection and conversion
    wavelength = _detect_and_convert_wavelength_units(wavelength)
    
    return wavelength, flux


def _detect_and_convert_wavelength_units(wavelength: np.ndarray) -> np.ndarray:
    """
    Detect wavelength units and convert to Angstroms if necessary.
    
    Parameters:
        wavelength: Wavelength array
        
    Returns:
        np.ndarray: Wavelength array in Angstroms
    """
    if len(wavelength) == 0:
        return wavelength
        
    min_wave = np.min(wavelength)
    max_wave = np.max(wavelength)
    
    # Detect likely units based on typical ranges
    if min_wave > 100 and max_wave < 1000:
        # Likely nanometers (nm) - convert to Angstroms
        wavelength_converted = wavelength * 10.0
        _LOGGER.info(f"🔄 Wavelength units detected as nanometers (nm)")
        _LOGGER.info(f"   Converting: {min_wave:.1f}-{max_wave:.1f} nm → "
              f"{wavelength_converted[0]:.1f}-{wavelength_converted[-1]:.1f} Å")
        return wavelength_converted
        
    elif min_wave > 0.1 and max_wave < 10:
        # Likely micrometers (μm) - convert to Angstroms
        wavelength_converted = wavelength * 10000.0
        _LOGGER.info(f"🔄 Wavelength units detected as micrometers (μm)")
        _LOGGER.info(f"   Converting: {min_wave:.2f}-{max_wave:.2f} μm → "
              f"{wavelength_converted[0]:.1f}-{wavelength_converted[-1]:.1f} Å")
        return wavelength_converted
        
    elif min_wave > 1000 and max_wave < 100000:
        # Likely already in Angstroms
        _LOGGER.info(f"✅ Wavelength units detected as Angstroms (Å): {min_wave:.1f}-{max_wave:.1f} Å")
        return wavelength
        
    else:
        # Unknown units - warn but don't convert
        warnings.warn(f"Unknown wavelength units detected (range: {min_wave:.2f}-{max_wave:.2f}). "
                     "Assuming Angstroms. Please verify units manually.")
        return wavelength


def _try_alternative_text_loading(filename: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Try alternative methods for loading text files.
    
    Parameters:
        filename: Path to text file
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Wavelength and flux arrays
    """
    # Try comma-separated
    try:
        data = np.loadtxt(filename, delimiter=',', comments='#')
        if data.ndim == 2 and data.shape[1] >= 2:
            return _validate_and_clean_arrays(data[:, 0], data[:, 1])
    except:
        pass
    
    # Try pandas if available
    try:
        import pandas as pd
        
        # Try whitespace-delimited
        df = pd.read_csv(filename, delim_whitespace=True, header=None, comment='#')
        if len(df.columns) >= 2:
            return _validate_and_clean_arrays(df.iloc[:, 0].values, df.iloc[:, 1].values)
            
        # Try comma-delimited
        df = pd.read_csv(filename, header=None, comment='#')
        if len(df.columns) >= 2:
            return _validate_and_clean_arrays(df.iloc[:, 0].values, df.iloc[:, 1].values)
            
    except ImportError:
        pass
    except:
        pass
    
    raise SpectrumLoadError("All text loading methods failed")


def create_spectrum_data(wavelength: np.ndarray, flux: np.ndarray, 
                        error: Optional[np.ndarray] = None,
                        header: Optional[Dict[str, Any]] = None,
                        filename: Optional[str] = None,
                        format: SpectrumFormat = SpectrumFormat.UNKNOWN) -> SpectrumData:
    """
    Create a SpectrumData object from arrays.
    
    Parameters:
        wavelength: Wavelength array
        flux: Flux array
        error: Optional error array
        header: Optional header information
        filename: Optional source filename
        format: Spectrum format
        
    Returns:
        SpectrumData: Structured spectrum data object
    """
    return SpectrumData(
        wavelength=wavelength,
        flux=flux,
        error=error,
        header=header,
        filename=filename,
        format=format
    ) 