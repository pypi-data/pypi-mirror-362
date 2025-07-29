"""
Tests for Smogon functionality.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from localsets.smogon import SmogonSets
from localsets.core import PokemonData


class TestSmogonSets:
    """Test SmogonSets class functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = Path(self.temp_dir) / "smogon" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_init_default(self):
        """Test SmogonSets initialization with defaults."""
        with patch('localsets.smogon.Path') as mock_path:
            # Mock the data directory to not exist so no formats are discovered
            mock_path.return_value.parent.exists.return_value = False
            
            smogon = SmogonSets()
            assert smogon.formats == []
            assert isinstance(smogon._data, dict)
            assert isinstance(smogon._loaded_formats, set)
    
    def test_init_custom_formats(self):
        """Test SmogonSets initialization with custom formats."""
        custom_formats = ['gen9ou', 'gen8ou']
        smogon = SmogonSets(formats=custom_formats)
        assert smogon.formats == custom_formats
    
    def test_discover_formats(self):
        """Test format discovery from bundled data."""
        # Create mock data files
        (self.data_dir / "gen9ou.json").touch()
        (self.data_dir / "gen8ou.json").touch()
        (self.data_dir / "gen7ou.json").touch()
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._discover_formats()
            
            assert "gen9ou" in smogon.formats
            assert "gen8ou" in smogon.formats
            assert "gen7ou" in smogon.formats
    
    def test_load_format_success(self):
        """Test successful format loading."""
        # Create mock data file
        mock_data = {
            "Pikachu": {
                "Life Orb": {
                    "item": "Life Orb",
                    "ability": "Static",
                    "nature": "Naive",
                    "evs": {"atk": 252, "spa": 4, "spe": 252},
                    "moves": ["Volt Tackle", "Extreme Speed", "Iron Tail", "Knock Off"]
                }
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            assert "gen9ou" in smogon._data
            assert "gen9ou" in smogon._loaded_formats
            assert smogon._data["gen9ou"] == mock_data
    
    def test_load_format_file_not_found(self):
        """Test format loading when file doesn't exist."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("nonexistent")
            
            assert "nonexistent" in smogon._data
            assert "nonexistent" in smogon._loaded_formats
            assert smogon._data["nonexistent"] == {}
    
    def test_load_format_corrupted_json(self):
        """Test format loading with corrupted JSON."""
        # Create corrupted JSON file
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            f.write("invalid json content")
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            assert "gen9ou" in smogon._data
            assert "gen9ou" in smogon._loaded_formats
            assert smogon._data["gen9ou"] == {}
    
    def test_normalize_name(self):
        """Test Pokemon name normalization."""
        smogon = SmogonSets()
        
        assert smogon._normalize_name("Pikachu") == "pikachu"
        assert smogon._normalize_name("Pikachu-EX") == "pikachuex"
        assert smogon._normalize_name("Mr. Mime") == "mrmime"
        assert smogon._normalize_name("Ho-Oh") == "hooh"
        assert smogon._normalize_name("Nidoran♀") == "nidoran"
        assert smogon._normalize_name("Nidoran♂") == "nidoran"
    
    def test_get_sets_exact_match(self):
        """Test getting sets with exact name match."""
        mock_data = {
            "Pikachu": {
                "Life Orb": {"item": "Life Orb", "moves": ["Volt Tackle"]},
                "Choice Band": {"item": "Choice Band", "moves": ["Volt Tackle"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            sets = smogon.get_sets("Pikachu", "gen9ou")
            assert sets is not None
            assert "Life Orb" in sets
            assert "Choice Band" in sets
            assert sets["Life Orb"]["item"] == "Life Orb"
    
    def test_get_sets_case_insensitive(self):
        """Test getting sets with case-insensitive matching."""
        mock_data = {
            "Pikachu": {
                "Life Orb": {"item": "Life Orb", "moves": ["Volt Tackle"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            sets = smogon.get_sets("pikachu", "gen9ou")
            assert sets is not None
            assert "Life Orb" in sets
    
    def test_get_sets_not_found(self):
        """Test getting sets for Pokemon that doesn't exist."""
        mock_data = {
            "Charizard": {
                "Special Attacker": {"item": "Choice Specs", "moves": ["Fire Blast"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            sets = smogon.get_sets("Pikachu", "gen9ou")
            assert sets is None
    
    def test_get_sets_format_not_available(self):
        """Test getting sets from unavailable format."""
        smogon = SmogonSets()
        sets = smogon.get_sets("Pikachu", "nonexistent_format")
        assert sets is None
    
    def test_get_set_specific(self):
        """Test getting a specific set."""
        mock_data = {
            "Pikachu": {
                "Life Orb": {
                    "item": "Life Orb",
                    "ability": "Static",
                    "nature": "Naive",
                    "evs": {"atk": 252, "spa": 4, "spe": 252},
                    "moves": ["Volt Tackle", "Extreme Speed", "Iron Tail", "Knock Off"]
                }
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            set_data = smogon.get_set("Pikachu", "gen9ou", "Life Orb")
            assert set_data is not None
            assert set_data["item"] == "Life Orb"
            assert set_data["ability"] == "Static"
            assert set_data["nature"] == "Naive"
            assert set_data["evs"]["atk"] == 252
            assert "Volt Tackle" in set_data["moves"]
    
    def test_get_set_not_found(self):
        """Test getting a set that doesn't exist."""
        mock_data = {
            "Pikachu": {
                "Life Orb": {"item": "Life Orb", "moves": ["Volt Tackle"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            set_data = smogon.get_set("Pikachu", "gen9ou", "Nonexistent Set")
            assert set_data is None
    
    def test_list_sets(self):
        """Test listing set names for a Pokemon."""
        mock_data = {
            "Pikachu": {
                "Life Orb": {"item": "Life Orb", "moves": ["Volt Tackle"]},
                "Choice Band": {"item": "Choice Band", "moves": ["Volt Tackle"]},
                "Special Attacker": {"item": "Choice Specs", "moves": ["Thunderbolt"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            set_names = smogon.list_sets("Pikachu", "gen9ou")
            assert isinstance(set_names, list)
            assert "Life Orb" in set_names
            assert "Choice Band" in set_names
            assert "Special Attacker" in set_names
            assert len(set_names) == 3
    
    def test_list_sets_pokemon_not_found(self):
        """Test listing sets for Pokemon that doesn't exist."""
        mock_data = {
            "Charizard": {
                "Special Attacker": {"item": "Choice Specs", "moves": ["Fire Blast"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            set_names = smogon.list_sets("Pikachu", "gen9ou")
            assert set_names == []
    
    def test_list_pokemon(self):
        """Test listing Pokemon in a format."""
        mock_data = {
            "Pikachu": {
                "Life Orb": {"item": "Life Orb", "moves": ["Volt Tackle"]}
            },
            "Charizard": {
                "Special Attacker": {"item": "Choice Specs", "moves": ["Fire Blast"]}
            },
            "Blastoise": {
                "Bulky": {"item": "Leftovers", "moves": ["Scald"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            pokemon_list = smogon.list_pokemon("gen9ou")
            assert isinstance(pokemon_list, list)
            assert "Pikachu" in pokemon_list
            assert "Charizard" in pokemon_list
            assert "Blastoise" in pokemon_list
            assert len(pokemon_list) == 3
    
    def test_list_pokemon_format_not_available(self):
        """Test listing Pokemon from unavailable format."""
        smogon = SmogonSets()
        pokemon_list = smogon.list_pokemon("nonexistent_format")
        assert pokemon_list == []
    
    def test_get_formats(self):
        """Test getting available formats."""
        smogon = SmogonSets()
        formats = smogon.get_formats()
        assert isinstance(formats, list)
        assert len(formats) >= 0
    
    def test_search(self):
        """Test searching for a Pokemon across all formats."""
        # Create mock data for multiple formats
        gen9ou_data = {
            "Pikachu": {
                "Life Orb": {"item": "Life Orb", "moves": ["Volt Tackle"]}
            }
        }
        
        gen8ou_data = {
            "Pikachu": {
                "Choice Band": {"item": "Choice Band", "moves": ["Volt Tackle"]}
            }
        }
        
        # Write data files
        (self.data_dir / "gen9ou.json").write_text(json.dumps(gen9ou_data))
        (self.data_dir / "gen8ou.json").write_text(json.dumps(gen8ou_data))
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            smogon._load_format("gen8ou")
            
            results = smogon.search("Pikachu")
            assert isinstance(results, dict)
            assert "gen9ou" in results
            assert "gen8ou" in results
            # The search method returns the sets, not the Pokemon name
            assert "Life Orb" in results["gen9ou"]
            assert "Choice Band" in results["gen8ou"]
    
    def test_search_not_found(self):
        """Test searching for Pokemon that doesn't exist."""
        mock_data = {
            "Charizard": {
                "Special Attacker": {"item": "Choice Specs", "moves": ["Fire Blast"]}
            }
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            results = smogon.search("Pikachu")
            assert isinstance(results, dict)
            assert len(results) == 0
    
    def test_get_format_info(self):
        """Test getting format information."""
        mock_data = {
            "Pikachu": {"Life Orb": {"item": "Life Orb", "moves": ["Volt Tackle"]}},
            "Charizard": {"Special Attacker": {"item": "Choice Specs", "moves": ["Fire Blast"]}}
        }
        
        data_file = self.data_dir / "gen9ou.json"
        with open(data_file, 'w') as f:
            json.dump(mock_data, f)
        
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent = self.data_dir.parent
            
            smogon = SmogonSets()
            smogon._load_format("gen9ou")
            
            info = smogon.get_format_info("gen9ou")
            assert info["name"] == "gen9ou"
            assert info["generation"] == "9"
            assert info["type"] == "ou"
            assert info["pokemon_count"] == 2
            assert info["available"] is True
    
    def test_get_format_info_not_available(self):
        """Test getting format info for unavailable format."""
        smogon = SmogonSets()
        info = smogon.get_format_info("nonexistent_format")
        assert info == {}
    
    def test_extract_generation(self):
        """Test generation extraction from format names."""
        smogon = SmogonSets()
        
        assert smogon._extract_generation("gen9ou") == "9"
        assert smogon._extract_generation("gen8ou") == "8"
        assert smogon._extract_generation("gen1ou") == "1"
        assert smogon._extract_generation("invalid") == "unknown"
    
    def test_extract_type(self):
        """Test battle type extraction from format names."""
        smogon = SmogonSets()
        
        assert smogon._extract_type("gen9ou") == "ou"
        assert smogon._extract_type("gen9uu") == "uu"
        assert smogon._extract_type("gen9ru") == "ru"
        assert smogon._extract_type("gen9nu") == "nu"
        assert smogon._extract_type("gen9pu") == "pu"
        assert smogon._extract_type("gen9ubers") == "ubers"
        assert smogon._extract_type("gen9doublesou") == "doubles"
        assert smogon._extract_type("gen9vgc2024") == "vgc"
        assert smogon._extract_type("gen9other") == "other"


class TestSmogonIntegration:
    """Test Smogon integration with PokemonData class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
        
        # Create mock Smogon data
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
            },
            "gen8ou": {
                "Pikachu": {
                    "Light Ball": {
                        "item": "Light Ball",
                        "ability": "Static",
                        "nature": "Timid",
                        "evs": {"spa": 252, "spe": 252, "spd": 4},
                        "moves": ["Thunderbolt", "Volt Switch", "Surf", "Grass Knot"]
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
    
    def test_pokemon_data_smogon_initialization(self):
        """Test PokemonData initialization with Smogon formats."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou', 'gen8ou'],
                auto_update=False
            )
            
            assert data.smogon_formats == ['gen9ou', 'gen8ou']
            assert hasattr(data, '_smogon_data')
            assert data._smogon_data is not None
    
    def test_get_smogon_sets_integration(self):
        """Test getting Smogon sets through PokemonData."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou'],
                auto_update=False
            )
            
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            
            sets = data.get_smogon_sets("Pikachu", "gen9ou")
            assert sets is not None
            assert "Life Orb" in sets
            assert "Choice Band" in sets
            assert sets["Life Orb"]["item"] == "Life Orb"
            assert sets["Choice Band"]["item"] == "Choice Band"
    
    def test_get_smogon_set_integration(self):
        """Test getting specific Smogon set through PokemonData."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou'],
                auto_update=False
            )
            
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            
            set_data = data.get_smogon_set("Pikachu", "gen9ou", "Life Orb")
            assert set_data is not None
            assert set_data["item"] == "Life Orb"
            assert set_data["ability"] == "Static"
            assert set_data["nature"] == "Naive"
            assert set_data["evs"]["atk"] == 252
    
    def test_list_smogon_sets_integration(self):
        """Test listing Smogon set names through PokemonData."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou'],
                auto_update=False
            )
            
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            
            set_names = data.list_smogon_sets("Pikachu", "gen9ou")
            assert isinstance(set_names, list)
            assert "Life Orb" in set_names
            assert "Choice Band" in set_names
            assert len(set_names) == 2
    
    def test_list_smogon_pokemon_integration(self):
        """Test listing Smogon Pokemon through PokemonData."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou'],
                auto_update=False
            )
            
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            
            pokemon_list = data.list_smogon_pokemon("gen9ou")
            assert isinstance(pokemon_list, list)
            assert "Pikachu" in pokemon_list
            assert "Charizard" in pokemon_list
            assert len(pokemon_list) == 2
    
    def test_search_smogon_integration(self):
        """Test Smogon search through PokemonData."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou', 'gen8ou'],
                auto_update=False
            )
            
            # Mock the data loading to return our test data
            data._smogon_data._data["gen9ou"] = self.mock_smogon_data["gen9ou"]
            data._smogon_data._data["gen8ou"] = self.mock_smogon_data["gen8ou"]
            data._smogon_data._loaded_formats.add("gen9ou")
            data._smogon_data._loaded_formats.add("gen8ou")
            
            results = data.search_smogon("Pikachu")
            assert isinstance(results, dict)
            assert "gen9ou" in results
            assert "gen8ou" in results
            # The search method returns the sets, not the Pokemon name
            assert "Life Orb" in results["gen9ou"]
            assert "Light Ball" in results["gen8ou"]
    
    def test_get_smogon_formats_integration(self):
        """Test getting Smogon formats through PokemonData."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou', 'gen8ou'],
                auto_update=False
            )
            
            formats = data.get_smogon_formats()
            assert isinstance(formats, list)
            assert "gen9ou" in formats
            assert "gen8ou" in formats
    
    def test_get_smogon_format_info_integration(self):
        """Test getting Smogon format info through PokemonData."""
        with patch('localsets.smogon.Path') as mock_path:
            mock_path.return_value.parent.parent = self.cache_dir
            
            data = PokemonData(
                smogon_formats=['gen9ou'],
                auto_update=False
            )
            
            info = data.get_smogon_format_info("gen9ou")
            assert info["name"] == "gen9ou"
            assert info["generation"] == "9"
            assert info["type"] == "ou"
            assert info["available"] is True 