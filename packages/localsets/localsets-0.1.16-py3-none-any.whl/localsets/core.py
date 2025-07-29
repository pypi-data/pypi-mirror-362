"""
Core PokemonData class for managing Pokemon random battle data.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import requests
from appdirs import user_cache_dir

from .updater import DataUpdater
from .formats import FORMATS, FORMAT_MAPPINGS
from .smogon import SmogonSets

logger = logging.getLogger(__name__)


class PokemonData:
    """
    Main class for managing Pokemon data from both RandBats and Smogon sources.
    
    Provides methods to load, cache, and update Pokemon data from various
    battle formats and generations.
    """
    
    def __init__(self, randbats_formats: Optional[List[str]] = None, 
                 smogon_formats: Optional[List[str]] = None,
                 cache_dir: Optional[str] = None,
                 auto_update: bool = True):
        """
        Initialize PokemonData instance.
        
        Args:
            randbats_formats: List of RandBats format names to load. If None, loads all available.
            smogon_formats: List of Smogon format names to load. If None, loads all available.
            cache_dir: Directory to store cached data. If None, uses default.
            auto_update: Whether to automatically check for RandBats updates.
        """
        self.randbats_formats = randbats_formats or FORMATS
        self.smogon_formats = smogon_formats or []
        self.cache_dir = Path(cache_dir or user_cache_dir('localsets'))
        self.auto_update = auto_update
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # RandBats data storage
        self._randbats_data: Dict[str, Dict] = {}
        self._randbats_stats: Dict[str, Dict] = {}
        self._randbats_metadata: Dict[str, Dict] = {}
        self._loaded_randbats_formats: set = set()
        
        # Smogon data storage
        self._smogon_data = SmogonSets(smogon_formats)
        
        # Initialize RandBats updater
        self.updater = DataUpdater(self.cache_dir)
        
        # Load RandBats data
        self._load_randbats_data()
        
        # Auto-update if enabled
        if self.auto_update:
            self._check_randbats_updates()
    
    def _load_randbats_data(self):
        """Load RandBats data for all specified formats."""
        for format_name in self.randbats_formats:
            if format_name not in self._loaded_randbats_formats:
                self._load_randbats_format(format_name)
    
    def _load_randbats_format(self, format_name: str):
        """Load RandBats data and stats for a specific format."""
        try:
            # Try cache first
            cache_file = self.cache_dir / f"{format_name}.json"
            stats_file = self.cache_dir / f"{format_name}_stats.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self._randbats_data[format_name] = json.load(f)
                # Try to load stats if available
                if stats_file.exists():
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        self._randbats_stats[format_name] = json.load(f)
                self._loaded_randbats_formats.add(format_name)
                logger.debug(f"Loaded {format_name} from cache (sets and stats)")
                return
            # Fall back to bundled data - try multiple possible paths
            possible_paths = [
                Path(__file__).parent / "randbattle_data" / f"{format_name}.json",
                Path(__file__).parent.parent / "localsets" / "randbattle_data" / f"{format_name}.json",
            ]
            stats_paths = [
                Path(__file__).parent / "randbattle_data" / f"{format_name}_stats.json",
                Path(__file__).parent.parent / "localsets" / "randbattle_data" / f"{format_name}_stats.json",
            ]
            for bundled_file, stats_bundled_file in zip(possible_paths, stats_paths):
                if bundled_file.exists():
                    with open(bundled_file, 'r', encoding='utf-8') as f:
                        self._randbats_data[format_name] = json.load(f)
                    if stats_bundled_file.exists():
                        with open(stats_bundled_file, 'r', encoding='utf-8') as f:
                            self._randbats_stats[format_name] = json.load(f)
                    self._loaded_randbats_formats.add(format_name)
                    logger.debug(f"Loaded {format_name} from bundled data: {bundled_file} (sets and stats)")
                    return
            # Try importlib.resources as last resort (for installed packages)
            try:
                import importlib.resources as pkg_resources
                with pkg_resources.open_text('localsets.randbattle_data', f"{format_name}.json") as f:
                    self._randbats_data[format_name] = json.load(f)
                try:
                    with pkg_resources.open_text('localsets.randbattle_data', f"{format_name}_stats.json") as f:
                        self._randbats_stats[format_name] = json.load(f)
                except (FileNotFoundError, ModuleNotFoundError):
                    pass
                self._loaded_randbats_formats.add(format_name)
                logger.debug(f"Loaded {format_name} from package resources (sets and stats)")
                return
            except (ImportError, FileNotFoundError, ModuleNotFoundError):
                pass
            # Create empty data if nothing available
            self._randbats_data[format_name] = {}
            self._randbats_stats[format_name] = {}
            self._loaded_randbats_formats.add(format_name)
            logger.warning(f"No data available for {format_name} - file not found in cache or bundled data")
        except Exception as e:
            logger.error(f"Failed to load {format_name}: {e}")
            self._randbats_data[format_name] = {}
            self._randbats_stats[format_name] = {}
            self._loaded_randbats_formats.add(format_name)
    
    def _check_randbats_updates(self):
        """Check for RandBats updates if needed."""
        try:
            # Check if update is needed (24 hour interval)
            last_update_file = self.cache_dir / "last_update"
            if last_update_file.exists():
                with open(last_update_file, 'r') as f:
                    last_update = datetime.fromisoformat(f.read().strip())
                if datetime.now() - last_update < timedelta(hours=24):
                    return  # No update needed
            
            # Perform update
            self.update_randbats_all()
            
        except Exception as e:
            logger.warning(f"Auto-update check failed: {e}")
    
    # RandBats methods (existing API)
    def get_randbats(self, pokemon_name: str, format_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get RandBats Pokemon data for a specific Pokemon and format.
        
        Args:
            pokemon_name: Name of the Pokemon (case-insensitive)
            format_name: Battle format. If None, tries to auto-detect.
            
        Returns:
            Pokemon data dictionary or None if not found
        """
        if format_name is None:
            format_name = self._detect_randbats_format(pokemon_name)
        
        if format_name not in self._randbats_data:
            logger.warning(f"Format {format_name} not available")
            return None
        
        # Normalize Pokemon name
        pokemon_name = self._normalize_name(pokemon_name)
        
        # Search in format data
        format_data = self._randbats_data[format_name]
        if pokemon_name in format_data:
            return format_data[pokemon_name]
        
        # Try fuzzy matching
        for key in format_data.keys():
            if self._normalize_name(key) == pokemon_name:
                return format_data[key]
        
        return None
    
    def list_randbats_pokemon(self, format_name: str) -> List[str]:
        """
        List all Pokemon available in a specific RandBats format.
        
        Args:
            format_name: Battle format name
            
        Returns:
            List of Pokemon names
        """
        if format_name not in self._randbats_data:
            logger.warning(f"Format {format_name} not available")
            return []
        
        return list(self._randbats_data[format_name].keys())
    
    def get_randbats_stats(self, pokemon_name: str, format_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get RandBats stats data for a specific Pokemon and format.
        Args:
            pokemon_name: Name of the Pokemon (case-insensitive)
            format_name: Battle format. If None, tries to auto-detect.
        Returns:
            Stats data dictionary or None if not found
        """
        if format_name is None:
            format_name = self._detect_randbats_format(pokemon_name)
        if format_name not in self._randbats_stats:
            logger.warning(f"Stats for format {format_name} not available")
            return None
        pokemon_name = self._normalize_name(pokemon_name)
        stats_data = self._randbats_stats[format_name]
        # Try exact match
        if pokemon_name in stats_data:
            return stats_data[pokemon_name]
        # Try fuzzy match
        for key in stats_data.keys():
            if self._normalize_name(key) == pokemon_name:
                return stats_data[key]
        return None

    def get_randbats_with_stats(self, pokemon_name: str, format_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get both RandBats set and stats data for a specific Pokemon and format.
        Args:
            pokemon_name: Name of the Pokemon (case-insensitive)
            format_name: Battle format. If None, tries to auto-detect.
        Returns:
            Dictionary with 'set' and 'stats' keys, or None if not found
        """
        set_data = self.get_randbats(pokemon_name, format_name)
        stats_data = self.get_randbats_stats(pokemon_name, format_name)
        if set_data is None and stats_data is None:
            return None
        return {'set': set_data, 'stats': stats_data}
    
    def get_randbats_formats(self) -> List[str]:
        """Get list of available RandBats formats."""
        return list(self._loaded_randbats_formats)
    
    def update_randbats(self, formats: Optional[List[str]] = None):
        """
        Update RandBats data for specific formats.
        
        Args:
            formats: List of formats to update. If None, updates all loaded formats.
        """
        formats_to_update = formats or list(self._loaded_randbats_formats)
        
        try:
            updated_formats = self.updater.update_formats(formats_to_update)
            
            # Reload updated formats
            for format_name in updated_formats:
                if format_name in self._loaded_randbats_formats:
                    self._load_randbats_format(format_name)
            
            # Update last update timestamp
            last_update_file = self.cache_dir / "last_update"
            with open(last_update_file, 'w') as f:
                f.write(datetime.now().isoformat())
            
            logger.info(f"Updated {len(updated_formats)} formats")
            
        except Exception as e:
            logger.error(f"Update failed: {e}")
    
    def update_randbats_all(self):
        """Update RandBats data for all available formats."""
        self.update_randbats(FORMATS)
    
    # Smogon methods (new API)
    def get_smogon_sets(self, pokemon_name: str, format_name: str) -> Optional[Dict[str, Any]]:
        """
        Get all Smogon sets for a Pokemon in a specific format.
        
        Args:
            pokemon_name: Name of the Pokemon (case-insensitive)
            format_name: Battle format
            
        Returns:
            Dictionary of sets or None if not found
        """
        return self._smogon_data.get_sets(pokemon_name, format_name)
    
    def get_smogon_set(self, pokemon_name: str, format_name: str, set_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific Smogon set for a Pokemon.
        
        Args:
            pokemon_name: Name of the Pokemon
            format_name: Battle format
            set_name: Name of the specific set
            
        Returns:
            Set data dictionary or None if not found
        """
        return self._smogon_data.get_set(pokemon_name, format_name, set_name)
    
    def list_smogon_sets(self, pokemon_name: str, format_name: str) -> List[str]:
        """
        List all set names for a Pokemon in a Smogon format.
        
        Args:
            pokemon_name: Name of the Pokemon
            format_name: Battle format
            
        Returns:
            List of set names
        """
        return self._smogon_data.list_sets(pokemon_name, format_name)
    
    def list_smogon_pokemon(self, format_name: str) -> List[str]:
        """
        List all Pokemon available in a specific Smogon format.
        
        Args:
            format_name: Battle format name
            
        Returns:
            List of Pokemon names
        """
        return self._smogon_data.list_pokemon(format_name)
    
    def get_smogon_formats(self) -> List[str]:
        """Get list of available Smogon formats."""
        return self._smogon_data.get_formats()
    
    def search_smogon(self, pokemon_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Search for a Pokemon across all loaded Smogon formats.
        
        Args:
            pokemon_name: Name of the Pokemon
            
        Returns:
            Dictionary mapping format names to Pokemon sets
        """
        return self._smogon_data.search(pokemon_name)
    
    # Unified methods
    def get_pokemon(self, pokemon_name: str, format_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get Pokemon data (RandBats) - maintained for backward compatibility.
        
        Args:
            pokemon_name: Name of the Pokemon (case-insensitive)
            format_name: Battle format. If None, tries to auto-detect.
            
        Returns:
            Pokemon data dictionary or None if not found
        """
        return self.get_randbats(pokemon_name, format_name)
    
    def list_pokemon(self, format_name: str) -> List[str]:
        """
        List all Pokemon in a format (RandBats) - maintained for backward compatibility.
        
        Args:
            format_name: Battle format name
            
        Returns:
            List of Pokemon names
        """
        return self.list_randbats_pokemon(format_name)
    
    def get_formats(self) -> List[str]:
        """Get list of available RandBats formats - maintained for backward compatibility."""
        return self.get_randbats_formats()
    
    def update(self, formats: Optional[List[str]] = None):
        """Update RandBats data - maintained for backward compatibility."""
        self.update_randbats(formats)
    
    def update_all(self):
        """Update all RandBats data - maintained for backward compatibility."""
        self.update_randbats_all()
    
    def get_all_formats(self) -> Dict[str, List[str]]:
        """
        Get all available formats from both sources.
        
        Returns:
            Dictionary with 'randbats' and 'smogon' keys containing format lists
        """
        return {
            'randbats': self.get_randbats_formats(),
            'smogon': self.get_smogon_formats()
        }
    
    def search_all(self, pokemon_name: str) -> Dict[str, Any]:
        """
        Search for a Pokemon across both RandBats and Smogon data.
        
        Args:
            pokemon_name: Name of the Pokemon
            
        Returns:
            Dictionary with 'randbats' and 'smogon' results
        """
        results = {
            'randbats': {},
            'smogon': {}
        }
        
        # Search RandBats
        for format_name in self._loaded_randbats_formats:
            data = self.get_randbats(pokemon_name, format_name)
            if data:
                results['randbats'][format_name] = data
        
        # Search Smogon
        results['smogon'] = self.search_smogon(pokemon_name)
        
        return results
    
    def _detect_randbats_format(self, pokemon_name: str) -> str:
        """
        Auto-detect the best RandBats format for a Pokemon.
        
        Args:
            pokemon_name: Name of the Pokemon
            
        Returns:
            Best matching format name
        """
        # Simple heuristic: try most recent formats first
        recent_formats = ['gen9randombattle', 'gen8randombattle', 'gen7randombattle']
        
        for format_name in recent_formats:
            if format_name in self._randbats_data:
                pokemon_data = self.get_randbats(pokemon_name, format_name)
                if pokemon_data:
                    return format_name
        
        # Fall back to first available format
        return next(iter(self._loaded_randbats_formats), 'gen9randombattle')
    
    def _normalize_name(self, name: str) -> str:
        """
        Normalize Pokemon name for comparison.
        
        Args:
            name: Pokemon name
            
        Returns:
            Normalized name
        """
        # Remove all non-alphanumeric characters
        return ''.join(c for c in name.lower() if c.isalnum())
    
    def get_randbats_metadata(self, format_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific RandBats format.
        
        Args:
            format_name: Battle format name
            
        Returns:
            Metadata dictionary or None
        """
        try:
            metadata_file = self.cache_dir / f"{format_name}_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    return json.load(f)
            
            # Try bundled metadata
            bundled_metadata = Path(__file__).parent / "metadata" / f"{format_name}_metadata.json"
            if bundled_metadata.exists():
                with open(bundled_metadata, 'r') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to load metadata for {format_name}: {e}")
            return None
    
    def get_smogon_format_info(self, format_name: str) -> Dict[str, Any]:
        """
        Get information about a specific Smogon format.
        
        Args:
            format_name: Battle format name
            
        Returns:
            Dictionary with format information
        """
        return self._smogon_data.get_format_info(format_name)
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about cached data.
        
        Returns:
            Dictionary with cache information
        """
        info = {
            'cache_dir': str(self.cache_dir),
            'randbats_formats': list(self._loaded_randbats_formats),
            'smogon_formats': self.get_smogon_formats(),
            'total_randbats_pokemon': sum(len(data) for data in self._randbats_data.values()),
            'randbats_format_counts': {fmt: len(data) for fmt, data in self._randbats_data.items()}
        }
        
        # Add last update info
        last_update_file = self.cache_dir / "last_update"
        if last_update_file.exists():
            with open(last_update_file, 'r') as f:
                info['last_update'] = f.read().strip()
        
        return info


# Backward compatibility alias
RandBatsData = PokemonData 

__all__ = [
    'PokemonData',
    'RandBatsData',
] 