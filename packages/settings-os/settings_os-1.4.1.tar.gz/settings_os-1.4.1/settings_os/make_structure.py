"""
Project Structure Generator Module

This module provides a flexible way to generate project directory structures 
dynamically. The project structure is defined using a nested dictionary where:

- Keys represent directory names
- Values can be:
  1. Empty list `[]`: Creates an empty directory
  2. List with `.py` files: Creates those specific Python module files
  3. List with directory names: Creates those subdirectories
  4. Nested dictionary: Allows creating complex, nested directory structures

Example Default Structure:
structure = {
    'docs': [],                 # Empty documentation directory
    'data': [],                 # Empty data directory
    'src': {
        'config': ['environments.py'],  # Creates environments.py module
        'controller': [],        # Empty controller directory
        'main': ['handler.py'],  # Creates handler.py module
        'models': [              # Creates nested directories
            'entities', 
            'repository'
        ]
    }
}

ProjectStructureGenerator(custom_structure=structure)
"""
import os
from pathlib import Path
from typing import Literal


structures = {
    'simple_mvc': {
            'docs': [],
            'data': [],
            'src': {
                'config': ['environments.py'],
                'controller': [],
                'services': [],
                'main': ['handler.py'],
                'models': ['entities', 'repository'],
                'utils': []
            }
        },
    'ml': {
        'data': [
            'raw',           # Original, unprocessed data
            'processed',     # Cleaned and transformed data
            'external'       # Additional external data sources
        ],
        'notebooks': [],
        'tests': [],
        'config': [],
        'reports': [         # Model and analysis reports
            'figures',       # Visualization outputs
        ],
        'models': [],
        'docs': [],          # Project documentation
        'utils': []
    }
}


class ProjectStructureGenerator:
    def __init__(self, project_type: Literal['simple_mvc', 'ml', None], base_dir=None, custom_structure=None):
        self.base_dir = Path(base_dir or os.getcwd())
        if project_type == 'simple_mvc':
            self.structures = structures['simple_mvc']

            self.config_path = self.base_dir / 'src' / 'config' / 'environments.py'
            self.env_path = self.base_dir / '.env'

            self.create_project_structure()
            self.generate_config()
            self.generate_env()
        elif project_type == 'ml':
            self.structures = structures['ml']
            self.create_project_structure()
        else:
            if custom_structure:
                self.structures = custom_structure
            else:
                raise RuntimeError("Precisa ser selecionada uma estrutura ou passada uma personalizada.")

    def create_project_structure(self):
        """
        Create project directory structure recursively
        """
        def create_dirs(base_path, structure):
            for key, value in structure.items():
                current_path = base_path / key
                current_path.mkdir(parents=True, exist_ok=True)

                if isinstance(value, list):
                    for subitem in value:
                        subpath = current_path / subitem
                        if '.' in subitem:
                            subpath.touch(exist_ok=True)
                        else:
                            subpath.mkdir(exist_ok=True)
                elif isinstance(value, dict):
                    create_dirs(current_path, value)

        create_dirs(self.base_dir, self.structures)
        print(f"Project structure created in {self.base_dir}")

    def generate_config(self):
        """
        Create or update environments.py file with dotenv loading
        """
        config_content = ''.join([
            'import os\n',
            'from pathlib import Path\n'
            'from dotenv import load_dotenv\n\n', 
            'load_dotenv()\n\n', 
            'class Config:\n\tBASEDIR: Path = Path(os.getenv("BASEDIR"))\n\n'
        ])

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w') as f:
            f.write(config_content)
        
        print(f"Config file created at: {self.config_path}")

    def generate_env(self):
        """
        Create .env file with initial configurations
        """
        env_content = f'BASEDIR="{self.base_dir}"\n'
        with open(self.env_path, 'w') as f:
            f.write(env_content)

        print(f".env file created at: {self.env_path}")


if __name__ == "__main__":
    ProjectStructureGenerator(project_type='simple_mvc', base_dir=r'F:\settings_os\teste')
