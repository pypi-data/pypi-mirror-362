__version__ = "0.1.0.dev9"

# Core functionality is always available
from sw_ut_report.parse_txt_file import format_txt_file
from sw_ut_report.parse_xml_file import format_xml_to_dict
from sw_ut_report.template_manager import get_local_template

# Jama integration is optional (only import if dependencies are available)
try:
    from sw_ut_report.jama_ut_manager import (
        create_unit_tests_in_jama,
        extract_test_names_and_covers,
        validate_jama_environment_for_ut_creation
    )
    from sw_ut_report.jama_common import JamaUTManager, JamaConnectionError
    JAMA_AVAILABLE = True
except ImportError:
    JAMA_AVAILABLE = False

__all__ = [
    "__version__",
    "format_txt_file",
    "format_xml_to_dict",
    "get_local_template",
    "JAMA_AVAILABLE"
]

# Add Jama exports if available
if JAMA_AVAILABLE:
    __all__.extend([
        "create_unit_tests_in_jama",
        "extract_test_names_and_covers",
        "validate_jama_environment_for_ut_creation",
        "JamaUTManager",
        "JamaConnectionError"
    ])
