"""
Core PokemonData class for managing Pokemon random battle data.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from .updater import DataReader
from .formats import FORMATS, FORMAT_MAPPINGS
from .smogon import SmogonSets

logger = logging.getLogger(__name__)

class PokemonData:
    """
    Main class for managing Pokemon data from both RandBats and Smogon sources.
    Provides methods to load Pokemon data from various battle formats and generations.
    """
    def __init__(self, randbats_formats: Optional[List[str]] = None, 
                 smogon_formats: Optional[List[str]] = None,
                 cache_dir: Optional[str] = None):
        """
        Initialize PokemonData instance.
        Args:
            randbats_formats: List of RandBats format names to load. If None, loads all available.
            smogon_formats: List of Smogon format names to load. If None, loads all available.
            cache_dir: Directory to store cached data. If None, uses default.
        """
        self.randbats_formats = randbats_formats or FORMATS
        self.smogon_formats = smogon_formats or []
        self.cache_dir = Path(cache_dir) if cache_dir else None
        # RandBats data storage
        self._randbats_data: Dict[str, Dict] = {}
        self._loaded_randbats_formats: set = set()
        # Smogon data storage
        self._smogon_data = SmogonSets(self.smogon_formats)
        # Data reader for offline data
        self.data_reader = DataReader(Path(__file__).parent / "randbattle_data")
        self.metadata_reader = DataReader(Path(__file__).parent / "metadata")
        # Load RandBats data
        self._load_randbats_data()

    def _load_randbats_data(self):
        """Load RandBats data for all specified formats."""
        for format_name in self.randbats_formats:
            if format_name not in self._loaded_randbats_formats:
                self._load_randbats_format(format_name)

    def _load_randbats_format(self, format_name: str):
        """Load RandBats data for a specific format from bundled data only."""
        try:
            data = self.data_reader.get_format_data(format_name)
            if data is not None:
                self._randbats_data[format_name] = data
                self._loaded_randbats_formats.add(format_name)
                logger.debug(f"Loaded {format_name} from bundled data")
                return
            # Create empty data if nothing available
            self._randbats_data[format_name] = {}
            self._loaded_randbats_formats.add(format_name)
            logger.warning(f"No data available for {format_name} - file not found in bundled data")
        except Exception as e:
            logger.error(f"Failed to load {format_name}: {e}")
            self._randbats_data[format_name] = {}
            self._loaded_randbats_formats.add(format_name)

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

    def get_randbats_formats(self) -> List[str]:
        """Get list of available RandBats formats."""
        return list(self._loaded_randbats_formats)

    # Smogon methods (new API)
    def get_smogon_sets(self, pokemon_name: str, format_name: str) -> Optional[Dict[str, Any]]:
        return self._smogon_data.get_sets(pokemon_name, format_name)

    def get_smogon_set(self, pokemon_name: str, format_name: str, set_name: str) -> Optional[Dict[str, Any]]:
        return self._smogon_data.get_set(pokemon_name, format_name, set_name)

    def list_smogon_sets(self, pokemon_name: str, format_name: str) -> List[str]:
        return self._smogon_data.list_sets(pokemon_name, format_name)

    def list_smogon_pokemon(self, format_name: str) -> List[str]:
        return self._smogon_data.list_pokemon(format_name)

    def get_smogon_formats(self) -> List[str]:
        return self._smogon_data.get_formats()

    def search_smogon(self, pokemon_name: str) -> Dict[str, Dict[str, Any]]:
        return self._smogon_data.search(pokemon_name)

    # Unified methods
    def get_pokemon(self, pokemon_name: str, format_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        return self.get_randbats(pokemon_name, format_name)

    def list_pokemon(self, format_name: str) -> List[str]:
        return self.list_randbats_pokemon(format_name)

    def get_formats(self) -> List[str]:
        return self.get_randbats_formats()

    def get_all_formats(self) -> Dict[str, List[str]]:
        return {
            'randbats': self.get_randbats_formats(),
            'smogon': self.get_smogon_formats()
        }

    def search_all(self, pokemon_name: str) -> Dict[str, Any]:
        results = {
            'randbats': {},
            'smogon': {}
        }
        for format_name in self._loaded_randbats_formats:
            data = self.get_randbats(pokemon_name, format_name)
            if data:
                results['randbats'][format_name] = data
        results['smogon'] = self.search_smogon(pokemon_name)
        return results

    def _detect_randbats_format(self, pokemon_name: str) -> str:
        recent_formats = ['gen9randombattle', 'gen8randombattle', 'gen7randombattle']
        for format_name in recent_formats:
            if format_name in self._randbats_data:
                pokemon_data = self.get_randbats(pokemon_name, format_name)
                if pokemon_data:
                    return format_name
        return next(iter(self._loaded_randbats_formats), 'gen9randombattle')

    def _normalize_name(self, name: str) -> str:
        return ''.join(c for c in name.lower() if c.isalnum())

    def get_randbats_metadata(self, format_name: str) -> Optional[Dict[str, Any]]:
        try:
            metadata = self.metadata_reader.get_format_data(f"{format_name}_metadata")
            return metadata
        except Exception as e:
            logger.error(f"Failed to load metadata for {format_name}: {e}")
            return None

    def get_smogon_format_info(self, format_name: str) -> Dict[str, Any]:
        return self._smogon_data.get_format_info(format_name)

    def get_cache_info(self) -> Dict[str, Any]:
        info = {
            'randbats_formats': list(self._loaded_randbats_formats),
            'smogon_formats': self.get_smogon_formats(),
            'total_randbats_pokemon': sum(len(data) for data in self._randbats_data.values()),
            'randbats_format_counts': {fmt: len(data) for fmt, data in self._randbats_data.items()}
        }
        return info

RandBatsData = PokemonData

__all__ = [
    'PokemonData',
    'RandBatsData',
] 