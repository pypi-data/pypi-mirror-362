"""Loss tracking and management system for wf2wf.

This module provides comprehensive loss tracking during workflow format conversions,
including detection, recording, validation, and restoration of lost information.

For detailed implementation, see the wf2wf.loss submodules:
- wf2wf.loss.core: Core loss tracking functionality
- wf2wf.loss.context_detection: Format-specific loss detection
- wf2wf.loss.export: Export loss detection for different formats
- wf2wf.loss.import_: Import loss detection and validation
"""

# Import all public functions and classes from submodules
from .loss.core import (
    LossEntry,
    reset,
    record,
    as_list,
    write,
    apply,
    prepare,
    compute_checksum,
    record_environment_adaptation,
    record_spec_class_loss,
    record_environment_specific_loss,
    generate_summary,
    create_loss_document,
    write_loss_document,
    detect_and_apply_loss_sidecar,
    create_loss_sidecar_summary,
)

from .loss.context_detection import (
    detect_format_specific_losses,
    record_environment_specific_value_loss,
    validate_environment_specific_value,
    restore_environment_specific_value,
    FormatLossDetector,
    EnvironmentLossRecorder,
)

from .loss.export import (
    detect_and_record_export_losses,
    record_cwl_losses,
    record_dagman_losses,
    record_snakemake_losses,
    record_nextflow_losses,
    record_wdl_losses,
    record_galaxy_losses,
)

from .loss.import_ import (
    detect_and_record_import_losses,
    validate_loss_sidecar,
    validate_loss_entry,
)

__all__ = [
    # Core loss functions
    "LossEntry",
    "reset",
    "record",
    "as_list",
    "write",
    "apply",
    "prepare",
    "compute_checksum",
    "record_environment_adaptation",
    "record_spec_class_loss",
    "record_environment_specific_loss",
    "generate_summary",
    "create_loss_document",
    "write_loss_document",
    "detect_and_apply_loss_sidecar",
    "create_loss_sidecar_summary",
    
    # Context detection
    "detect_format_specific_losses",
    "record_environment_specific_value_loss",
    "validate_environment_specific_value",
    "restore_environment_specific_value",
    "FormatLossDetector",
    "EnvironmentLossRecorder",
    
    # Export loss detection
    "detect_and_record_export_losses",
    "record_cwl_losses",
    "record_dagman_losses",
    "record_snakemake_losses",
    "record_nextflow_losses",
    "record_wdl_losses",
    "record_galaxy_losses",
    
    # Import loss detection
    "detect_and_record_import_losses",
    "validate_loss_sidecar",
    "validate_loss_entry",
]
