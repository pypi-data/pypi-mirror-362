"""
SNID SAGE GUI Dialogs
====================

Collection of dialog windows for the SNID SAGE GUI interface.

Available dialogs:
- PreprocessingDialog: Spectrum preprocessing configuration
- PreprocessingSelectionDialog: Preprocessing mode selection
- ConfigurationDialog: SNID analysis parameters configuration  
- MaskManagerDialog: Spectrum masking management
- AISummaryDialog: LLM-generated analysis summaries
- ResultsDialog: Analysis results viewing
- SettingsDialog: GUI settings and preferences
- ShortcutsDialog: Keyboard shortcuts and hotkeys reference
- ManualRedshiftDialog: Manual galaxy redshift determination
- MultiStepEmissionAnalysisDialog: Multi-step supernova emission line analysis tool
"""

from .preprocessing_dialog import PreprocessingDialog
from .preprocessing_selection_dialog import PreprocessingSelectionDialog
from .configuration_dialog import ModernSNIDOptionsDialog, show_snid_options_dialog
from .mask_manager_dialog import MaskManagerDialog
from .enhanced_ai_assistant_dialog import EnhancedAIAssistantDialog, AISummaryDialog
from .results_dialog import ResultsDialog
from .settings_dialog import GUISettingsDialog, show_gui_settings_dialog
from .shortcuts_dialog import ShortcutsDialog
from .manual_redshift_dialog import ManualRedshiftDialog, show_manual_redshift_dialog
from .multi_step_emission_dialog import MultiStepEmissionAnalysisDialog, show_multi_step_emission_dialog
from .snid_analysis_dialog import SNIDAnalysisDialog, show_snid_analysis_dialog

__all__ = [
    'PreprocessingDialog',
    'PreprocessingSelectionDialog',
    'ModernSNIDOptionsDialog',
    'show_snid_options_dialog',
    'MaskManagerDialog', 
    'AISummaryDialog',
    'EnhancedAIAssistantDialog',
    'ResultsDialog',
    'GUISettingsDialog',
    'show_gui_settings_dialog',
    'ShortcutsDialog',
    'ManualRedshiftDialog',
    'show_manual_redshift_dialog',
    'MultiStepEmissionAnalysisDialog',
    'show_multi_step_emission_dialog',
    'SNIDAnalysisDialog',
    'show_snid_analysis_dialog'
] 
