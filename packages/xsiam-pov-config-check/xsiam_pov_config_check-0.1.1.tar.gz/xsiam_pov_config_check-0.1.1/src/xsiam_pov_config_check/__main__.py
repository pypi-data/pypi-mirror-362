"""
Entry‑point wrapper so that the package can be executed with

    python -m xsiam_pov_config_check
    xsiam-pov-config-check        (console script)

It simply delegates to the main() function defined in
xsiam_pov_config_check.py.
"""
from .xsiam_pov_config_check import main

if __name__ == "__main__":  # pragma: no cover
    main()
