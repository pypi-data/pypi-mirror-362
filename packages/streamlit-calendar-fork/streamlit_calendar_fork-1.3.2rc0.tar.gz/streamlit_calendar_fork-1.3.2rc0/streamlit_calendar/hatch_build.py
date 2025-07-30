from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import subprocess
import os
import sys

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # Check if npm exists on the server
        try:
            npm_version = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
            print(f"npm is installed. Version: {npm_version.stdout.strip()}")
        except subprocess.CalledProcessError:
            print("npm is not installed or not found in PATH.")
            sys.exit(1)


        # Build frontend
        frontend_dir = os.path.join(self.root, "streamlit_calendar", "frontend")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
