import sys
import argparse

__version__ = '0.1.0'
__all__ = ['', 'main']


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    commandLine = argparse.ArgumentParser(description='Check for Python package')
    commandLine.add_argument('--version', action='version', version="%(prog)s "+__version__)
    commandLine.add_argument('--package', type=str, help='package to look for', required=True)
    environment = commandLine.parse_args(argv)

    try:
        __import__(environment.package)
    except ImportError:
        return 1
        
    return 0

if __name__ == '__main__':
    if sys.argv[0] is None:
        # fix for weird behaviour when run with python -m
        # from a zipped egg.
        sys.argv[0] = 'find_package.py'
    sys.exit(main())

