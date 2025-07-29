"""
Tests for core PokemonData functionality.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from localsets.core import PokemonData, RandBatsData
from localsets.formats import RANDBATS_FORMATS, SMOGON_FORMATS


class TestPokemonData:
    """Test PokemonData class functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_init_default(self):
        """Test PokemonData initialization with defaults."""
        with patch('localsets.core.user_cache_dir', return_value=self.temp_dir):
            data = PokemonData(auto_update=False)
            assert data.randbats_formats == RANDBATS_FORMATS
            assert data.smogon_formats == []
            assert data.cache_dir == Path(self.temp_dir)
            assert data.auto_update is False
    
    def test_init_custom_formats(self):
        """Test PokemonData initialization with custom formats."""
        custom_randbats = ['gen9randombattle', 'gen8randombattle']
        custom_smogon = ['gen9ou', 'gen8ou']
        
        with patch('localsets.core.user_cache_dir', return_value=self.temp_dir):
            data = PokemonData(
                randbats_formats=custom_randbats,
                smogon_formats=custom_smogon,
                auto_update=False
            )
            assert data.randbats_formats == custom_randbats
            assert data.smogon_formats == custom_smogon
    
    def test_init_custom_cache_dir(self):
        """Test PokemonData initialization with custom cache directory."""
        custom_cache = Path(self.temp_dir) / "custom_cache"
        data = PokemonData(cache_dir=str(custom_cache), auto_update=False)
        assert data.cache_dir == custom_cache
        assert custom_cache.exists()
    
    def test_normalize_name(self):
        """Test Pokemon name normalization."""
        data = PokemonData(auto_update=False)
        
        # Test various name formats
        assert data._normalize_name("Pikachu") == "pikachu"
        assert data._normalize_name("Pikachu-EX") == "pikachuex"
        assert data._normalize_name("Mr. Mime") == "mrmime"
        assert data._normalize_name("Ho-Oh") == "hooh"
    
    def test_get_randbats_formats(self):
        """Test getting available RandBats formats."""
        data = PokemonData(auto_update=False)
        formats = data.get_randbats_formats()
        assert isinstance(formats, list)
        assert len(formats) >= 0  # May be empty if no data loaded
    
    def test_get_smogon_formats(self):
        """Test getting available Smogon formats."""
        data = PokemonData(auto_update=False)
        formats = data.get_smogon_formats()
        assert isinstance(formats, list)
        assert len(formats) >= 0  # May be empty if no data loaded
    
    def test_get_all_formats(self):
        """Test getting all available formats."""
        data = PokemonData(auto_update=False)
        all_formats = data.get_all_formats()
        
        assert 'randbats' in all_formats
        assert 'smogon' in all_formats
        assert isinstance(all_formats['randbats'], list)
        assert isinstance(all_formats['smogon'], list)
    
    def test_get_cache_info(self):
        """Test getting cache information."""
        data = PokemonData(auto_update=False)
        info = data.get_cache_info()
        
        assert 'cache_dir' in info
        assert 'randbats_formats' in info
        assert 'smogon_formats' in info
        assert 'total_randbats_pokemon' in info
        assert 'randbats_format_counts' in info
        assert isinstance(info['cache_dir'], str)
        assert isinstance(info['randbats_formats'], list)
        assert isinstance(info['smogon_formats'], list)
        assert isinstance(info['total_randbats_pokemon'], int)
        assert isinstance(info['randbats_format_counts'], dict)


class TestRandBatsDataLoading:
    """Test RandBats data loading functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_randbats_format_from_cache(self):
        """Test loading RandBats format data from cache."""
        # Create mock cache data
        cache_file = self.cache_dir / "gen9randombattle.json"
        mock_data = {"pikachu": {"level": 50, "moves": ["thunderbolt"]}}
        
        with open(cache_file, 'w') as f:
            json.dump(mock_data, f)
        
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        assert "gen9randombattle" in data._randbats_data
        assert data._randbats_data["gen9randombattle"] == mock_data
    
    def test_load_randbats_format_from_bundled(self):
        """Test loading RandBats format data from bundled files."""
        # This test would require actual bundled data files
        # For now, just test that it doesn't crash
        data = PokemonData(auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        # Should create empty data if no bundled file exists
        assert "gen9randombattle" in data._randbats_data
    
    def test_load_randbats_format_error_handling(self):
        """Test error handling during RandBats format loading."""
        # Create corrupted cache file
        cache_file = self.cache_dir / "gen9randombattle.json"
        with open(cache_file, 'w') as f:
            f.write("invalid json")
        
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        # Should create empty data on error
        assert "gen9randombattle" in data._randbats_data
        assert data._randbats_data["gen9randombattle"] == {}


class TestSmogonDataLoading:
    """Test Smogon data loading functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_smogon_sets_initialization(self):
        """Test SmogonSets initialization."""
        data = PokemonData(auto_update=False)
        assert hasattr(data, '_smogon_data')
        assert data._smogon_data is not None
    
    def test_smogon_discover_formats(self):
        """Test Smogon format discovery."""
        data = PokemonData(auto_update=False)
        # Test that discovery doesn't crash
        data._smogon_data._discover_formats()
        assert isinstance(data._smogon_data.formats, list)


class TestRandBatsPokemonLookup:
    """Test RandBats Pokemon lookup functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
        
        # Create mock data
        self.mock_data = {
            "gen9randombattle": {
                "pikachu": {"level": 50, "moves": ["thunderbolt", "quick attack"]},
                "charizard": {"level": 55, "moves": ["flamethrower", "dragon claw"]}
            }
        }
        
        # Write mock data to cache
        for format_name, data in self.mock_data.items():
            cache_file = self.cache_dir / f"{format_name}.json"
            with open(cache_file, 'w') as f:
                json.dump(data, f)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_randbats_exact_match(self):
        """Test getting RandBats Pokemon with exact name match."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        pokemon = data.get_randbats("pikachu", "gen9randombattle")
        assert pokemon is not None
        assert pokemon["level"] == 50
        assert "thunderbolt" in pokemon["moves"]
    
    def test_get_randbats_case_insensitive(self):
        """Test getting RandBats Pokemon with case-insensitive matching."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        pokemon = data.get_randbats("Pikachu", "gen9randombattle")
        assert pokemon is not None
        assert pokemon["level"] == 50
    
    def test_get_randbats_not_found(self):
        """Test getting RandBats Pokemon that doesn't exist."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        pokemon = data.get_randbats("nonexistent", "gen9randombattle")
        assert pokemon is None
    
    def test_get_randbats_format_not_available(self):
        """Test getting RandBats Pokemon from unavailable format."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        
        pokemon = data.get_randbats("pikachu", "nonexistent_format")
        assert pokemon is None
    
    def test_list_randbats_pokemon(self):
        """Test listing RandBats Pokemon in a format."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        pokemon_list = data.list_randbats_pokemon("gen9randombattle")
        assert isinstance(pokemon_list, list)
        assert "pikachu" in pokemon_list
        assert "charizard" in pokemon_list
        assert len(pokemon_list) == 2
    
    def test_list_randbats_pokemon_format_not_available(self):
        """Test listing RandBats Pokemon from unavailable format."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        
        pokemon_list = data.list_randbats_pokemon("nonexistent_format")
        assert pokemon_list == []
    
    def test_backward_compatibility_get_pokemon(self):
        """Test backward compatibility for get_pokemon method."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        pokemon = data.get_pokemon("pikachu", "gen9randombattle")
        assert pokemon is not None
        assert pokemon["level"] == 50
    
    def test_backward_compatibility_list_pokemon(self):
        """Test backward compatibility for list_pokemon method."""
        data = PokemonData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_randbats_format("gen9randombattle")
        
        pokemon_list = data.list_pokemon("gen9randombattle")
        assert isinstance(pokemon_list, list)
        assert "pikachu" in pokemon_list


class TestSmogonPokemonLookup:
    """Test Smogon Pokemon lookup functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
        
        # Create mock Smogon data with all expected fields and sets
        self.mock_smogon_data = {
            "gen9ou": {
                "Pikachu": {
                    "Life Orb": {
                        "item": "Life Orb",
                        "ability": "Static",
                        "nature": "Naive",
                        "evs": {"atk": 252, "spa": 4, "spe": 252},
                        "moves": ["Volt Tackle", "Extreme Speed", "Iron Tail", "Knock Off"]
                    },
                    "Choice Band": {
                        "item": "Choice Band",
                        "ability": "Static",
                        "nature": "Adamant",
                        "evs": {"hp": 4, "atk": 252, "spe": 252},
                        "moves": ["Volt Tackle", "Extreme Speed", "Iron Tail", "U-turn"]
                    }
                },
                "Charizard": {
                    "Special Attacker": {
                        "item": "Choice Specs",
                        "ability": "Blaze",
                        "nature": "Timid",
                        "evs": {"spa": 252, "spe": 252, "spd": 4},
                        "moves": ["Fire Blast", "Air Slash", "Focus Blast", "Dragon Pulse"]
                    }
                }
            }
        }
        
        # Create Smogon data directory and write mock data
        smogon_data_dir = self.cache_dir / "smogon" / "data"
        smogon_data_dir.mkdir(parents=True, exist_ok=True)
        
        for format_name, data in self.mock_smogon_data.items():
            data_file = smogon_data_dir / f"{format_name}.json"
            with open(data_file, 'w') as f:
                json.dump(data, f)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_smogon_sets_exact_match(self):
        """Test getting Smogon sets with exact name match."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            sets = data.get_smogon_sets("Pikachu", "gen9ou")
            
            assert sets is not None
            assert "Life Orb" in sets
            assert sets["Life Orb"]["item"] == "Life Orb"
    
    def test_get_smogon_sets_case_insensitive(self):
        """Test getting Smogon sets with case-insensitive matching."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            sets = data.get_smogon_sets("pikachu", "gen9ou")
            
            assert sets is not None
            assert "Life Orb" in sets
    
    def test_get_smogon_sets_not_found(self):
        """Test getting Smogon sets for Pokemon that doesn't exist."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            sets = data.get_smogon_sets("nonexistent", "gen9ou")
            
            assert sets is None
    
    def test_get_smogon_sets_format_not_available(self):
        """Test getting Smogon sets from unavailable format."""
        data = PokemonData(auto_update=False)
        sets = data.get_smogon_sets("Pikachu", "nonexistent_format")
        assert sets is None
    
    def test_get_smogon_set_specific(self):
        """Test getting a specific Smogon set."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            set_data = data.get_smogon_set("Pikachu", "gen9ou", "Life Orb")
            
            assert set_data is not None
            assert set_data["item"] == "Life Orb"
            assert set_data["ability"] == "Static"
            assert set_data["nature"] == "Naive"
            assert set_data["evs"]["atk"] == 252
            assert "Volt Tackle" in set_data["moves"]
    
    def test_get_smogon_set_not_found(self):
        """Test getting a Smogon set that doesn't exist."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            set_data = data.get_smogon_set("Pikachu", "gen9ou", "Nonexistent Set")
            
            assert set_data is None
    
    def test_list_smogon_sets(self):
        """Test listing Smogon set names for a Pokemon."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            set_names = data.list_smogon_sets("Pikachu", "gen9ou")
            
            assert isinstance(set_names, list)
            assert "Life Orb" in set_names
            assert "Choice Band" in set_names
            assert len(set_names) == 2
    
    def test_list_smogon_pokemon(self):
        """Test listing Smogon Pokemon in a format."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            pokemon_list = data.list_smogon_pokemon("gen9ou")
            
            assert isinstance(pokemon_list, list)
            assert "Pikachu" in pokemon_list
            assert "Charizard" in pokemon_list
            assert len(pokemon_list) == 2
    
    def test_search_smogon(self):
        """Test searching for a Pokemon across all Smogon formats."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            results = data.search_smogon("Pikachu")
            
            assert isinstance(results, dict)
            # Should find Pikachu in gen9ou
            assert "gen9ou" in results
            # The search method returns the sets, not the Pokemon name
            assert "Life Orb" in results["gen9ou"]


class TestUnifiedFunctionality:
    """Test unified functionality across both data sources."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
        
        # Create mock RandBats data
        randbats_data = {
            "gen9randombattle": {
                "pikachu": {"level": 50, "moves": ["thunderbolt"]}
            }
        }
        
        # Create mock Smogon data
        self.mock_smogon_data = {
            "gen9ou": {
                "Pikachu": {
                    "Life Orb": {
                        "item": "Life Orb",
                        "moves": ["Volt Tackle", "Extreme Speed"]
                    }
                }
            }
        }
        
        # Write RandBats data to cache
        for format_name, data in randbats_data.items():
            cache_file = self.cache_dir / f"{format_name}.json"
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        
        # Write Smogon data
        smogon_data_dir = self.cache_dir / "smogon" / "data"
        smogon_data_dir.mkdir(parents=True, exist_ok=True)
        
        for format_name, data in self.mock_smogon_data.items():
            data_file = smogon_data_dir / f"{format_name}.json"
            with open(data_file, 'w') as f:
                json.dump(data, f)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_search_all(self):
        """Test searching across both RandBats and Smogon data."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            data._load_randbats_format("gen9randombattle")
            # Mock the Smogon data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            
            results = data.search_all("pikachu")
            
            assert isinstance(results, dict)
            assert 'randbats' in results
            assert 'smogon' in results
            
            # Should find in RandBats
            assert "gen9randombattle" in results['randbats']
            
            # Should find in Smogon
            assert "gen9ou" in results['smogon']
    
    def test_search_all_not_found(self):
        """Test searching for Pokemon that doesn't exist in either source."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(auto_update=False)
            data._load_randbats_format("gen9randombattle")
            
            results = data.search_all("nonexistent")
            
            assert isinstance(results, dict)
            assert 'randbats' in results
            assert 'smogon' in results
            assert len(results['randbats']) == 0
            assert len(results['smogon']) == 0


class TestBackwardCompatibility:
    """Test backward compatibility with old RandBatsData class."""
    
    def test_randbats_data_alias(self):
        """Test that RandBatsData is still available as an alias."""
        from localsets.core import RandBatsData
        assert RandBatsData is PokemonData
    
    def test_old_api_still_works(self):
        """Test that old API methods still work."""
        data = RandBatsData(auto_update=False)
        
        # Old method names should still work
        assert hasattr(data, 'get_pokemon')
        assert hasattr(data, 'list_pokemon')
        assert hasattr(data, 'get_formats')
        assert hasattr(data, 'update')
        assert hasattr(data, 'update_all')
        
        # New method names should also work
        assert hasattr(data, 'get_randbats')
        assert hasattr(data, 'list_randbats_pokemon')
        assert hasattr(data, 'get_randbats_formats')
        assert hasattr(data, 'update_randbats')
        assert hasattr(data, 'update_randbats_all') 