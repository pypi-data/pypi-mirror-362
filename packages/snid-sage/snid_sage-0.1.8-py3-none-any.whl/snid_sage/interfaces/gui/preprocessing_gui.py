"""
SNID GUI Preprocessing Module - Integration Layer
================================================

Thin integration layer for preprocessing functionality, importing modular
components from their proper locations according to the SNID SAGE architecture.

This module now serves as the main interface while delegating actual
implementation to specialized components:
- SpectrumPreprocessor: Core preprocessing logic (features/preprocessing/)
- PreprocessingDialog: Step-by-step wizard (components/dialogs/)
- InteractiveContinuumEditor: Interactive editing (components/dialogs/)
"""

# Import the modular components from their proper locations
from snid_sage.interfaces.gui.features.preprocessing.spectrum_preprocessor import SpectrumPreprocessor
from snid_sage.interfaces.gui.components.dialogs.preprocessing_dialog import PreprocessingDialog
from snid_sage.interfaces.gui.components.dialogs.continuum_editor_dialog import InteractiveContinuumEditor

# Re-export for backward compatibility
__all__ = [
    'SpectrumPreprocessor',
    'PreprocessingDialog', 
    'InteractiveContinuumEditor'
]

# Convenience function for showing preprocessing dialog
def show_preprocessing_dialog(parent, spectrum_data=None):
    """
    Convenience function to show the preprocessing dialog.
    
    Args:
        parent: Parent window
        spectrum_data: Optional spectrum data for the preprocessor
        
    Returns:
        PreprocessingDialog instance
    """
    # Import here to avoid circular imports if needed
    from snid_sage.interfaces.gui.features.preprocessing.spectrum_preprocessor import SpectrumPreprocessor
    from snid_sage.interfaces.gui.components.dialogs.preprocessing_dialog import PreprocessingDialog
    
    # Create preprocessor if spectrum data provided
    if spectrum_data:
        preprocessor = SpectrumPreprocessor(parent)
        # Load spectrum data if it's a file path
        if isinstance(spectrum_data, str):
            preprocessor.load_spectrum(spectrum_data)
    else:
        preprocessor = SpectrumPreprocessor(parent)
    
    # Create and show dialog
    dialog = PreprocessingDialog(parent, preprocessor)
    dialog.show()
    
    return dialog
