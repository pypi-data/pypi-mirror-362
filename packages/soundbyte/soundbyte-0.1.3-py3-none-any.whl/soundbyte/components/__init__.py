"""
SoundByte Components

This module imports all component implementations to ensure they are
registered with the plugin system.
"""

import os
import importlib

base_dir = os.path.dirname(__file__)
package_name = __name__

for root, dirs, files in os.walk(base_dir):
    rel_path = os.path.relpath(root, base_dir).replace(os.sep, '.')
    if rel_path == '.':
        rel_path = ''
    else:
        rel_path = f".{rel_path}"

    for file in files:
        if file.endswith('.py') and not file.startswith('_') and file != '__init__.py':
            module_name = file[:-3]
            importlib.import_module(f"{package_name}{rel_path}.{module_name}")
