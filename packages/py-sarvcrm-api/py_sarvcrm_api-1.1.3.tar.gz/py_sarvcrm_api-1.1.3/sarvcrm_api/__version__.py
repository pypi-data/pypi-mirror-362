__version__ = '1.1.3'
__letter__ = 'v'

def get_version():
    return f"{__letter__}'{__version__}'"

__all__ = [
    'get_version',
]