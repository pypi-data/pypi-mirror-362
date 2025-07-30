from .client import Client

__name__ = "zerogpt"
__version__ = "1.2.1"
__author__ = "RedPiar"
__license__ = "MIT"
__copyright__ = "Copyright 2025 RedPiar"


def _check_pypi_version():
    import sys
    import json
    import urllib.request

    try:
        url = f"https://pypi.org/pypi/{__name__}/json"
        with urllib.request.urlopen(url, timeout=3) as response:
            data = json.load(response)
            latest_version = data["info"]["version"]
            from packaging import version
            if version.parse(latest_version) > version.parse(__version__):
                print(
                    f"\n[WARNING] A new version of the '{__name__}' package is available: {latest_version} (you have {__version__})\n"
                    f"Please update the package with the command:\n"
                    f"    pip install -U {__name__}\n"
                )
    except Exception:
        pass

_check_pypi_version()
