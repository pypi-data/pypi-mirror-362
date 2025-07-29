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

    def get_most_likely_role(self, pokemon_name: str, format_name: Optional[str] = None) -> Optional[str]:
        """
        Get the most likely role for a Pokémon in a given format based on role weights.
        Returns the role name with the highest weight, or None if not found.
        """
        data = self.get_randbats(pokemon_name, format_name)
        if not data or 'stats' not in data or 'roles' not in data['stats']:
            return None
        roles = data['stats']['roles']
        if not roles:
            return None
        # Find role with highest weight
        return max(roles.items(), key=lambda x: x[1].get('weight', 0))[0]

    def get_most_likely_item(self, pokemon_name: str, format_name: Optional[str] = None, role: Optional[str] = None) -> Optional[str]:
        """
        Get the most likely item for a Pokémon in a given format (optionally for a specific role).
        Returns the item with the highest weight, or None if not found.
        """
        data = self.get_randbats(pokemon_name, format_name)
        if not data or 'stats' not in data:
            return None
        if role:
            roles = data['stats'].get('roles', {})
            if role in roles and 'items' in roles[role]:
                items = roles[role]['items']
                if items:
                    return max(items.items(), key=lambda x: x[1])[0]
        # Fallback to top-level items
        items = data['stats'].get('items', {})
        if items:
            return max(items.items(), key=lambda x: x[1])[0]
        return None

    def get_most_likely_ability(self, pokemon_name: str, format_name: Optional[str] = None, role: Optional[str] = None) -> Optional[str]:
        """
        Get the most likely ability for a Pokémon in a given format (optionally for a specific role).
        Returns the ability with the highest weight, or None if not found.
        """
        data = self.get_randbats(pokemon_name, format_name)
        if not data or 'stats' not in data:
            return None
        if role:
            roles = data['stats'].get('roles', {})
            if role in roles and 'abilities' in roles[role]:
                abilities = roles[role]['abilities']
                if abilities:
                    return max(abilities.items(), key=lambda x: x[1])[0]
        # Fallback to top-level abilities
        abilities = data['stats'].get('abilities', {})
        if abilities:
            return max(abilities.items(), key=lambda x: x[1])[0]
        return None

    def get_most_likely_tera_type(self, pokemon_name: str, format_name: Optional[str] = None, role: Optional[str] = None) -> Optional[str]:
        """
        Get the most likely Tera Type for a Pokémon in a given format (optionally for a specific role).
        Returns the Tera Type with the highest weight, or None if not found.
        """
        data = self.get_randbats(pokemon_name, format_name)
        if not data or 'stats' not in data:
            return None
        if role:
            roles = data['stats'].get('roles', {})
            if role in roles and 'teraTypes' in roles[role]:
                teras = roles[role]['teraTypes']
                if teras:
                    return max(teras.items(), key=lambda x: x[1])[0]
        # Fallback to top-level (rare, but for completeness)
        teras = data['stats'].get('teraTypes', {})
        if teras:
            return max(teras.items(), key=lambda x: x[1])[0]
        return None

    def get_most_likely_moves(self, pokemon_name: str, format_name: Optional[str] = None, role: Optional[str] = None, top_n: int = 4) -> Optional[List[str]]:
        """
        Get the most likely moves for a Pokémon in a given format (optionally for a specific role).
        Returns a list of up to top_n moves with the highest weights, or None if not found.
        """
        data = self.get_randbats(pokemon_name, format_name)
        if not data or 'stats' not in data:
            return None
        moves = None
        if role:
            roles = data['stats'].get('roles', {})
            if role in roles and 'moves' in roles[role]:
                moves = roles[role]['moves']
        if moves is None:
            moves = data['stats'].get('moves', {})
        if not moves:
            return None
        # Sort moves by weight, descending, and return top_n
        sorted_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)
        return [move for move, _ in sorted_moves[:top_n]]

RandBatsData = PokemonData

__all__ = [
    'PokemonData',
    'RandBatsData',
] 