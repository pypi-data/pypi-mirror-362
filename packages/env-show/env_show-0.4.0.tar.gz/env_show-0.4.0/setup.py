# from setuptools import setup, find_packages

# setup(
#     name="env_show",  # Your package name
#     version="0.3.0",
#     packages=find_packages(),
#     install_requires=[
#         "fastapi",
#         "python-dotenv"
#     ],
#     author="test",
#     description="FastAPI plugin to expose .env values via an endpoint",
#     long_description=open("./README.md ").read(),
#     long_description_content_type="text/markdown",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "Framework :: FastAPI",
#         "License :: OSI Approved :: MIT License"
#     ],
# )
# setup.py
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

# Define the name of the patch file that will be installed as .pth
PATCH_FILE_NAME = '_env_show_patch.py'
PTH_FILE_NAME = 'env_show_fastapi_patch.pth'

class install(_install):
    """
    Custom install command to copy the patch file to site-packages as a .pth file.
    """
    def run(self):
        _install.run(self)
        # Determine the site-package# setup(
#     name="env_show",  # Your package name
#     version="0.3.0",
#     packages=find_packages(),
#     install_requires=[
#         "fastapi",
#         "python-dotenv"
#     ],
#     author="test",# setup(
#     name="env_show",  # Your package name
#     version="0.3.0",
#     packages=find_packages(),
#     install_requires=[
#         "fastapi",
#         "python-dotenv"
#     ],
#     author="test",
#     description="FastAPI plugin to expose .env values via an endpoint",
#     long_description=open("./README.md ").read(),
#     long_description_content_type="text/markdown",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "Framework :: FastAPI",
#         "License :: OSI Approved :: MIT License"
#     ],
# )
#     description="FastAPI plugin to expose .env values via an endpoint",
#     long_description=open("./README.md ").read(),
#     long_description_content_type="text/markdown",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "Framework :: FastAPI",
#         "License :: OSI Approved :: MIT License"
#     ],
# )s directory
        # This is a bit tricky as site-packages can vary.
        # For simplicity, we'll try to find the standard ones.
        # In a virtual environment, it's usually sys.prefix/lib/pythonX.Y/site-packages
        # For global installs, it's usually /usr/lib/pythonX.Y/site-packages etc.
        try:
            from distutils.sysconfig import get_python_lib
            site_packages_path = get_python_lib()
        except ImportError:
            # Fallback for some environments
            site_packages_path = next(
                p for p in sys.path if 'site-packages' in p and p.endswith('site-packages')
            )

        if not site_packages_path:
            print("Warning: Could not determine site-packages path to install .pth file.", file=sys.stderr)
            return

        patch_source_path = self.install_lib + f'/env_show/{PATCH_FILE_NAME}'
        patch_destination_path = f'{site_packages_path}/{PTH_FILE_NAME}'

        try:
            import shutil
            shutil.copy(patch_source_path, patch_destination_path)
            print(f"Successfully installed FastAPI patch to: {patch_destination_path}")
        except Exception as e:
            print(f"Error installing FastAPI patch .pth file: {e}", file=sys.stderr)

setup(
    name="env_show",  # Your package name
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "python-dotenv"
    ],
    author="test",
    description="FastAPI plugin to expose .env values via an endpoint",
    long_description=open("./README.md ").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License"
    ],
)