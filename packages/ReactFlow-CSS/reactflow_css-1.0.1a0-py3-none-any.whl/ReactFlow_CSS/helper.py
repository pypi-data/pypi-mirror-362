"""
This helper module provides a simplified interface for using the styling capabilities
of the style_for_reactpy package.
"""
import os
from .tailwindcss import (
    configure as configure_tailwind,
    default_css as default_tailwind
)

from .bootstrap import (
    configure as configure_boots,
    Convert_style as convert_imports_to_link,
    default_css as default_boots
)

class StyleHelper:
    """
    A helper class to easily manage CSS styles for ReactPy projects using either
    Tailwind CSS or Bootstrap.
    """
    def __init__(self, main_file_path: str):
        """
        Initializes the helper with the path of the main script.
        This helps in resolving relative paths for configuration and output files.

        Args:
            main_file_path (str): Pass `__file__` from your main script here.
        """
        if not main_file_path:
            raise ValueError("main_file_path cannot be empty. Please provide the path to your main script, e.g., __file__.")
        self.main_dir = os.path.dirname(os.path.abspath(main_file_path))
        self._tailwind_configurator = None
        self._bootstrap_configurator = None

    @property
    def tailwind(self) -> configure_tailwind:
        """
        Provides access to the Tailwind CSS configuration and compilation functionalities.

        Returns:
            An instance of the Tailwind `configure` class.
        """
        if not self._tailwind_configurator:
            # The configure class for tailwind takes the project's root directory
            self._tailwind_configurator = configure_tailwind(self.main_dir)
        return self._tailwind_configurator

    @property
    def bootstrap(self) -> configure_boots:
        """
        Provides access to the Bootstrap CSS configuration functionalities.

        Returns:
            An instance of the Bootstrap `configure` class.
        """
        if not self._bootstrap_configurator:
            # The bootstrap `configure` class takes a path to a file within the project directory
            # to determine the project's root. We can provide a dummy path.
            bootstrap_main_path = os.path.join(self.main_dir, "__init__.py")
            self._bootstrap_configurator = configure_boots(bootstrap_main_path)
        return self._bootstrap_configurator

    def get_default_css(self, framework: str, output_path: str = None) -> str:
        """
        Gets the default pre-compiled CSS for the specified framework.

        Args:
            framework (str): The CSS framework to use. Can be 'tailwind' or 'bootstrap'.
            output_path (str, optional): If provided, writes the CSS content to this file path.
                                         The path is relative to your main script. Defaults to None.

        Returns:
            str: The default CSS content as a string.
        """
        if framework.lower() == 'tailwind':
            return default_tailwind(output_path)
        elif framework.lower() == 'bootstrap':
            return default_boots(output_path)
        else:
            raise ValueError("Unsupported framework. Please choose 'tailwind' or 'bootstrap'.")

    def to_reactpy_links(self, css_string: str):
        """
        Converts a CSS string containing @import rules into reactpy-compatible html.link components.
        This is particularly useful for Bootstrap styles that are composed of multiple imports.

        Args:
            css_string (str): The CSS content string.

        Returns:
            A reactpy VDOM object containing the <link> tags.
        """
        return convert_imports_to_link(css_string)

__all__ = ["StyleHelper"]
