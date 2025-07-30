#!/usr/bin/env python3
"""CLI entry point for dcs-jupyter."""

import json
import os
import subprocess
import sys
from tempfile import TemporaryDirectory

from jupyter_client.kernelspec import KernelSpecManager


def install_kernel():
    """Install the DCS Jupyter kernel if not already installed."""
    ksm = KernelSpecManager()

    # Check if kernel is already installed
    if 'dcs-lua' in ksm.get_all_specs():
        print('DCS kernel already installed')
        return True

    # Define kernel spec
    kernel_json = {
        'argv': [sys.executable, '-m', 'dcs_jupyter.kernel', '-f', '{connection_file}'],
        'display_name': 'dcs-lua',
        'language': 'lua',
    }

    try:
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755)

            # Write kernel.json
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)

            # Install the kernel in the current environment
            ksm.install_kernel_spec(td, 'dcs-lua', user=False, prefix=sys.prefix)
            print('DCS kernel installed successfully')
            return True
    except Exception as e:
        print(f'Error installing kernel: {e}')
        return False


def main():
    """Main CLI entry point."""
    print('Setting up DCS Jupyter kernel...')

    if not install_kernel():
        sys.exit(1)

    print('Starting Jupyter console with DCS kernel...')
    print('Type Lua code to execute in DCS. Press Ctrl+D to exit.')

    try:
        subprocess.run([sys.executable, '-m', 'jupyter', 'console', '--kernel=dcs-lua'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error starting Jupyter console: {e}')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit(0)


def main_lab():
    """Main CLI entry point for JupyterLab."""
    print('Setting up DCS Jupyter kernel...')

    if not install_kernel():
        sys.exit(1)

    # Check if JupyterLab is available
    try:
        subprocess.run([sys.executable, '-m', 'jupyter', 'lab', '--version'], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print('Error: JupyterLab is not installed.')
        print('Please install with: pipx install "dcs-jupyter[lab]"')
        sys.exit(1)
    except FileNotFoundError:
        print('Error: JupyterLab is not installed.')
        print('Please install with: pipx install "dcs-jupyter[lab]"')
        sys.exit(1)

    print('Starting JupyterLab with DCS kernel...')
    print('Create a new notebook and select the DCS Lua kernel.')

    try:
        subprocess.run([sys.executable, '-m', 'jupyter', 'lab'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error starting JupyterLab: {e}')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit(0)


if __name__ == '__main__':
    main()
