#!/usr/bin/env python3
"""
Minimal setup.py for custom build commands.
All package metadata is now handled by pyproject.toml.
"""

import os
import json
import urllib.request
from setuptools import setup, Command
from setuptools.command.build_py import build_py

# GitHub data source
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/pkmn/randbats/main/data"
GITHUB_API_BASE = "https://api.github.com/repos/pkmn/randbats/contents/data"

# Smogon data source
SMOGON_BASE_URL = "https://pkmn.github.io/smogon/data/sets"

# Available RandBats formats (defined here to avoid circular imports)
RANDBATS_FORMATS = [
    "gen1randombattle",
    "gen2randombattle", 
    "gen3randombattle",
    "gen4randombattle",
    "gen5randombattle",
    "gen6randombattle",
    "gen7letsgorandombattle",
    "gen7randombattle",
    "gen8bdsprandombattle",
    "gen8randombattle",
    "gen8randomdoublesbattle",
    "gen9babyrandombattle",
    "gen9randombattle",
    "gen9randomdoublesbattle"
]

# Available Smogon formats (common competitive formats)
SMOGON_FORMATS = [
    # Generation 9
    "gen9ou", "gen9uu", "gen9ru", "gen9nu", "gen9pu",
    "gen9ubers", "gen9doublesou", "gen9vgc2024",
    # Generation 8
    "gen8ou", "gen8uu", "gen8ru", "gen8nu", "gen8pu",
    "gen8ubers", "gen8doublesou", "gen8vgc2022", "gen8vgc2023",
    # Generation 7
    "gen7ou", "gen7uu", "gen7ru", "gen7nu", "gen7pu",
    "gen7ubers", "gen7doublesou", "gen7vgc2017", "gen7vgc2018", "gen7vgc2019",
    # Generation 6
    "gen6ou", "gen6uu", "gen6ru", "gen6nu", "gen6pu",
    "gen6ubers", "gen6doublesou", "gen6vgc2014", "gen6vgc2015", "gen6vgc2016",
    # Generation 5
    "gen5ou", "gen5uu", "gen5ru", "gen5nu", "gen5pu",
    "gen5ubers", "gen5doublesou", "gen5vgc2011", "gen5vgc2012", "gen5vgc2013",
    # Generation 4
    "gen4ou", "gen4uu", "gen4nu", "gen4pu",
    "gen4ubers", "gen4doublesou", "gen4vgc2009", "gen4vgc2010",
    # Generation 3
    "gen3ou", "gen3uu", "gen3nu", "gen3pu",
    "gen3ubers", "gen3doublesou",
    # Generation 2
    "gen2ou", "gen2uu", "gen2nu", "gen2pu",
    "gen2ubers", "gen2doublesou",
    # Generation 1
    "gen1ou", "gen1uu", "gen1nu", "gen1pu",
    "gen1ubers", "gen1doublesou"
]


class DownloadRandBatsDataCommand(Command):
    """Custom command to download RandBats data files during build."""
    
    description = "Download Pokemon random battle data files"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        """Download RandBats data files from GitHub."""
        print("Downloading Pokemon random battle data...")
        
        # Create data directory
        data_dir = os.path.join("localsets", "randbattle_data")
        metadata_dir = os.path.join("localsets", "metadata")
        
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(metadata_dir, exist_ok=True)
        
        # Download each format
        for format_name in RANDBATS_FORMATS:
            try:
                print(f"Downloading {format_name}.json...")
                
                # Download data file
                data_url = f"{GITHUB_RAW_BASE}/{format_name}.json"
                data_file = os.path.join(data_dir, f"{format_name}.json")
                
                with urllib.request.urlopen(data_url) as response:
                    with open(data_file, 'wb') as f:
                        f.write(response.read())
                
                # Get metadata from GitHub API
                metadata_url = f"{GITHUB_API_BASE}/{format_name}.json"
                with urllib.request.urlopen(metadata_url) as response:
                    metadata = json.loads(response.read().decode())
                
                # Save metadata
                metadata_file = os.path.join(metadata_dir, f"{format_name}_metadata.json")
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"[OK] Downloaded {format_name}.json")
                
            except Exception as e:
                print(f"[ERROR] Failed to download {format_name}.json: {e}")
                # Create empty file as fallback
                data_file = os.path.join(data_dir, f"{format_name}.json")
                with open(data_file, 'w') as f:
                    json.dump({}, f)
        
        print("RandBats data download complete!")


class DownloadSmogonDataCommand(Command):
    """Custom command to download Smogon data files during build."""
    
    description = "Download Smogon competitive sets data files"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        """Download Smogon data files from pkmn.github.io."""
        print("Downloading Smogon competitive sets data...")
        
        # Create Smogon data directory
        smogon_data_dir = os.path.join("localsets", "smogon_data")
        os.makedirs(smogon_data_dir, exist_ok=True)
        
        # Download each format
        for format_name in SMOGON_FORMATS:
            try:
                print(f"Downloading {format_name}.json...")
                
                # Download data file
                data_url = f"{SMOGON_BASE_URL}/{format_name}.json"
                data_file = os.path.join(smogon_data_dir, f"{format_name}.json")
                
                with urllib.request.urlopen(data_url) as response:
                    if response.status == 200:
                        with open(data_file, 'wb') as f:
                            f.write(response.read())
                        print(f"[OK] Downloaded {format_name}.json")
                    else:
                        print(f"[ERROR] {format_name}.json not available (404)")
                
            except Exception as e:
                print(f"[ERROR] Failed to download {format_name}.json: {e}")
                # Don't create empty file for Smogon - just skip if not available
        
        print("Smogon data download complete!")


class BuildPyCommand(build_py):
    """Custom build command that includes data download."""
    
    def run(self):
        # Download RandBats data first
        self.run_command('download_randbats_data')
        # Download Smogon data
        self.run_command('download_smogon_data')
        # Then run normal build
        super().run()


# Minimal setup call - all metadata handled by pyproject.toml
setup(
    cmdclass={
        'download_randbats_data': DownloadRandBatsDataCommand,
        'download_smogon_data': DownloadSmogonDataCommand,
        'build_py': BuildPyCommand,
    },
) 