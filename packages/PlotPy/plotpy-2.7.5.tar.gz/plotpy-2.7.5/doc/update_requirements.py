# -*- coding: utf-8 -*-

"""Update requirements.rst file from pyproject.toml or setup.cfg file

Warning: this has to be done manually at release time.
It is not done automatically by the sphinx 'conf.py' file because it
requires an internet connection to fetch the dependencies metadata - this
is not always possible (e.g., when building the documentation on a machine
without internet connection like the Debian package management infrastructure).
"""

from guidata.utils.genreqs import gen_module_req_rst  # noqa: E402

import plotpy

if __name__ == "__main__":
    print("Updating requirements.rst file...", end=" ")
    gen_module_req_rst(plotpy, ["Python>=3.9", "PyQt5>=5.11"])
    print("done.")
