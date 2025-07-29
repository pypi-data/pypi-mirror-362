import subprocess
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Union, Optional

from .exceptions import BootsTrapError, ModuleNotFound, ProcessError

class configure:
    def __init__(self, __path__):
        # __path__ is typically __name__ or the path to the main script
        self.main_dir = os.path.dirname(os.path.abspath(__path__))
        self.file_dir = Path(__file__).parent
        self.file_dir = self.file_dir / '..' / 'modules' / 'bootstrap' / 'css' / 'bootstrap.min.css'
        # Initial import logic for CSS
        self.import_ = f"@import '{self.file_dir}/bootstrap/css/bootstrap.min.css';"
        # Initial style content
        self.style = ""
        # Initial output path for the Bootstrap file
        self.output = ""
    
    def render_templates(self, path_input: str) -> str:
        """
        Renders templates from a given input path.
        """
        input_path = os.path.normpath(f"{self.main_dir / path_input}")
        with open(input_path, "r") as inputs:
            self.style = inputs.read()
            if not inputs.read():
                raise ModuleNotFound(f"Where is the content, for: {input_path}")
    
    def config(self, style: str = "", output: str = None, *args) -> str:
        """
        Configures the Bootstrap style.
        """
        # Basic logic for input validation
        self.style = style
        self.output = output
        
        # Validate imported content
        validated_imports = validated_modules(__main__=self.file_dir, import_=self.import_, *args)
        
        # Update style with validated imports
        final_style = update_style(style=self.style, imports=validated_imports)
        
        if output:
            path_output = os.path.normpath(f"{self.main_dir}/{output}")
            with open(path_output, "w") as f:
                f.write(final_style)
        
        return final_style
        
def validated_modules(__main__, import_, *args):
    """
    Validates modules and imports in CSS.
    """
    result = []
    result.append(import_)
    
    for line in args:
        if line.startswith("@import '--/"):
            # Correct the replace logic
            corrected_line = line.replace('--/', str(__main__) + "/")
            result.append(corrected_line)
        else:
            raise ModuleNotFound(f"Error: Root imports not found for: {line}")
    
    return result

def update_style(style, imports):
    """
    Updates the style with imports.
    """
    result = []
    
    # Add all imports first
    for import_line in imports:
        result.append(import_line + "\n")
    
    # Add the main style
    if style:
        result.append("\n" + style)
    
    # Combine all into a single string
    return "".join(result)

def default_css(path_output: str = None) -> str:
    """
    Returns the default Bootstrap CSS content.
    """
    main_dir = Path(__file__).parent
    imports = main_dir / '..' / 'modules' / 'bootstrap' / 'css' / 'bootstrap.min.css'
    final_imports = f"@import '{str(imports)}';"
    if path_output:
        open(path_output, "w").write(final_imports)
    
    return final_imports
