import os
import stat
import requests
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION_FILE = "krakenparser/version.py"


class CustomInstallCommand(install):
    """Custom installation to download scripts and set execution permissions."""

    def run(self):
        # Run standard installation
        install.run(self)

        # Define where to download the scripts
        install_dir = os.path.join(self.install_lib, "krakenparser")
        os.makedirs(install_dir, exist_ok=True)

        # List of external scripts to download
        scripts = {
            "combine_mpa.py": "https://raw.githubusercontent.com/jenniferlu717/KrakenTools/refs/heads/master/combine_mpa.py",
            "kreport2mpa.py": "https://raw.githubusercontent.com/jenniferlu717/KrakenTools/refs/heads/master/kreport2mpa.py",
        }

        for script_name, script_url in scripts.items():
            script_path = os.path.join(install_dir, script_name)
            print(f"Downloading {script_url} to {script_path}...")

            try:
                response = requests.get(script_url, timeout=10)
                response.raise_for_status()
                with open(script_path, "wb") as f:
                    f.write(response.content)
                print(f"Successfully downloaded {script_path}")

                # Set executable permissions
                os.chmod(
                    script_path,
                    stat.S_IRUSR
                    | stat.S_IWUSR
                    | stat.S_IXUSR
                    | stat.S_IRGRP
                    | stat.S_IXGRP
                    | stat.S_IROTH
                    | stat.S_IXOTH,
                )
                print(f"Set executable permissions on {script_path}")

            except requests.RequestException as e:
                print(f"Failed to download {script_url}: {e}")

        # Ensure all local scripts in krakenparser/ are executable
        self.set_executable_permissions(install_dir)

    def set_executable_permissions(self, directory):
        """Ensure all scripts in krakenparser/ have execution permissions."""
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith((".py", ".sh")):  # Adjust if needed
                    script_path = os.path.join(root, filename)
                    os.chmod(
                        script_path,
                        stat.S_IRUSR
                        | stat.S_IWUSR
                        | stat.S_IXUSR
                        | stat.S_IRGRP
                        | stat.S_IXGRP
                        | stat.S_IROTH
                        | stat.S_IXOTH,
                    )
                    print(f"Set executable permissions for {script_path}")


version = {}
with open(VERSION_FILE) as f:
    exec(f.read(), version)

setup(
    name="krakenparser",
    version=version["__version__"],
    description="A collection of scripts designed to process Kraken2 reports and convert them into CSV format.",
    long_description=open("README_PyPI.md").read(),
    long_description_content_type="text/markdown",
    author="Ilia Popov",
    author_email="iljapopov17@gmail.com",
    url="https://github.com/PopovIILab/KrakenParser",
    packages=find_packages(),
    include_package_data=True,  # Ensure non-Python files are included
    package_data={
        "krakenparser": ["*.sh"],  # Include all .sh scripts inside krakenparser/
    },
    cmdclass={"install": CustomInstallCommand},
    entry_points={
        "console_scripts": [
            "KrakenParser=krakenparser:krakenparser.main",  # Maps the command to the main function
        ],
    },
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.6",
)
