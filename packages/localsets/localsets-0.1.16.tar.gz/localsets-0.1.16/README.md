# localsets

Offline Pokemon battle data with auto-updates from official sources.

## What it does

- **Random Battle Data**: Access Pokemon Showdown's RandBats data offline, including option likelihood stats
- **Competitive Sets**: Get Smogon competitive Pokemon sets
- **Auto-Updates**: Automatically syncs with official repositories every 24 hours
- **Multiple Formats**: Supports all generations (Gen 1-9) and battle formats

## Quick Start

```python
from localsets import PokemonData

# Initialize with specific formats
data = PokemonData(
    randbats_formats=['gen9randombattle'],
    smogon_formats=['gen9ou']
)

# Get random battle data
pikachu = data.get_randbats('pikachu', 'gen9randombattle')

# Get competitive sets
sets = data.get_smogon_sets('pikachu', 'gen9ou')

# Get both set and stats data for a Pokemon
pikachu_both = data.get_randbats_with_stats('pikachu', 'gen9randombattle')
if pikachu_both:
    print('Set:', pikachu_both['set'])
    print('Stats:', pikachu_both['stats'])
```

## Installation

```bash
pip install localsets
```

## CLI Usage

```bash
# Get random battle Pokemon
localsets randbats get pikachu --format gen9randombattle

# Get competitive sets
localsets smogon get pikachu gen9ou

# Update data
localsets randbats update
```

## Data Sources

- **RandBats**: [pkmn/randbats](https://github.com/pkmn/randbats) - Pokemon Showdown random battle data and stats
- **Smogon**: [smogon/pokemon-showdown](https://github.com/smogon/pokemon-showdown) - Competitive Pokemon sets

## Features

- Offline-first with bundled data
- Automatic updates every 24 hours
- Support for all Pokemon generations
- Both random battle and competitive formats
- Includes option likelihood stats for random battle sets
- Simple Python API and CLI interface
- Graceful fallbacks and error handling 
