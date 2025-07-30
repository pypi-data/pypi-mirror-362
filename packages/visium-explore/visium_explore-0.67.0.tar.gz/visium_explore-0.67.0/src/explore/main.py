"""Main module for the explore package."""

import sys

from streamlit.web.cli import main

from explore import app


def run_explore() -> None:
    """Run the explore app using streamlit's CLI."""
    sys.argv = ["streamlit", "run", app.__file__]
    sys.exit(main())


if __name__ == "__main__":
    print("Hello World")
    run_explore()
