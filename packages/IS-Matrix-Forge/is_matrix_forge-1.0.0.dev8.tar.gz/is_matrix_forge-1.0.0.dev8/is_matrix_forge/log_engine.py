from inspy_logger import InspyLogger, Loggable
from inspy_logger.constants import LEVEL_MAP


LOG_LEVELS = [level for level in LEVEL_MAP.keys()]

del LEVEL_MAP

PROGNAME = 'LEDMatrixBattery'
AUTHOR = 'Inspyre-Softworks'

INSPY_LOG_LEVEL = 'INFO'

ROOT_LOGGER = InspyLogger(PROGNAME, console_level='info', no_file_logging=True)


__all__ = [
    'AUTHOR',
    'INSPY_LOG_LEVEL',
    'Loggable',
    'LOG_LEVELS',
    'PROGNAME',
    'ROOT_LOGGER',
]

