"""
Command line interface for localsets (standard library only).
"""

import sys
import argparse
import json
import logging
from typing import List, Optional

from .core import PokemonData
from .formats import (
    RANDBATS_FORMATS, SMOGON_FORMATS, RANDBATS_FORMAT_MAPPINGS, 
    SMOGON_FORMAT_MAPPINGS, resolve_randbats_formats, resolve_smogon_formats,
    get_randbats_format_info, get_smogon_format_info
)

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    parser = argparse.ArgumentParser(description="Pokemon Data CLI - RandBats and Smogon sets.")
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    subparsers = parser.add_subparsers(dest='command')

    # RandBats commands
    randbats_parser = subparsers.add_parser('randbats', help='RandBats random battle data commands')
    randbats_subparsers = randbats_parser.add_subparsers(dest='randbats_command')

    rb_update = randbats_subparsers.add_parser('update', help='Update RandBats data')
    rb_update.add_argument('--format', '-f', dest='format_name', help='Specific format to update')
    rb_update.add_argument('--all', action='store_true', help='Update all formats')
    rb_update.add_argument('--force', action='store_true', help='Force update')

    rb_get = randbats_subparsers.add_parser('get', help='Get RandBats Pokemon data')
    rb_get.add_argument('pokemon_name')
    rb_get.add_argument('--format', '-f', dest='format_name', help='Format to search in')
    rb_get.add_argument('--json', action='store_true', help='Output as JSON')

    rb_list = randbats_subparsers.add_parser('list', help='List Pokemon in RandBats format(s)')
    rb_list.add_argument('--format', '-f', dest='format_name', help='Format to list')
    rb_list.add_argument('--count', action='store_true', help='Show only count')

    # Smogon commands
    smogon_parser = subparsers.add_parser('smogon', help='Smogon competitive sets commands')
    smogon_subparsers = smogon_parser.add_subparsers(dest='smogon_command')

    sm_get = smogon_subparsers.add_parser('get', help='Get Smogon sets for a Pokemon')
    sm_get.add_argument('pokemon_name')
    sm_get.add_argument('format_name')
    sm_get.add_argument('--set', dest='set_name', help='Specific set name')
    sm_get.add_argument('--json', action='store_true', help='Output as JSON')

    sm_list = smogon_subparsers.add_parser('list', help='List Pokemon in Smogon format(s)')
    sm_list.add_argument('--format', '-f', dest='format_name', help='Format to list')
    sm_list.add_argument('--count', action='store_true', help='Show only count')

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command == 'randbats':
        data = PokemonData()
        if args.randbats_command == 'update':
            if args.all:
                formats_to_update = RANDBATS_FORMATS
            elif args.format_name:
                formats_to_update = resolve_randbats_formats([args.format_name])
            else:
                formats_to_update = data.get_randbats_formats()
            if not formats_to_update:
                print("No RandBats formats to update")
                return
            if args.force:
                updated = data.updater.force_update(formats_to_update)
            else:
                updated = data.updater.update_formats(formats_to_update)
            if updated:
                print(f"Updated {len(updated)} RandBats formats: {', '.join(updated)}")
            else:
                print("No RandBats updates needed")
        elif args.randbats_command == 'get':
            pokemon_data = data.get_randbats(args.pokemon_name, args.format_name)
            if pokemon_data is None:
                print(f"Pokemon '{args.pokemon_name}' not found in RandBats data")
                return
            if args.json:
                print(json.dumps(pokemon_data, indent=2))
            else:
                print(f"RandBats data for {args.pokemon_name} ({args.format_name or 'all formats'}):")
                print(pokemon_data)
        elif args.randbats_command == 'list':
            if args.format_name:
                formats_to_list = resolve_randbats_formats([args.format_name])
            else:
                formats_to_list = data.get_randbats_formats()
            if not formats_to_list:
                print("No RandBats formats available")
                return
            for fmt in formats_to_list:
                pokemon_list = data.list_randbats_pokemon(fmt)
                if args.count:
                    print(f"{fmt}: {len(pokemon_list)} Pokemon")
                else:
                    print(f"{fmt}: {', '.join(pokemon_list)}")
    elif args.command == 'smogon':
        data = PokemonData()
        if args.smogon_command == 'get':
            if args.set_name:
                set_data = data.get_smogon_set(args.pokemon_name, args.format_name, args.set_name)
                if set_data is None:
                    print(f"Set '{args.set_name}' not found for '{args.pokemon_name}' in {args.format_name}")
                    return
                if args.json:
                    print(json.dumps(set_data, indent=2))
                else:
                    print(f"Smogon set for {args.pokemon_name} ({args.format_name}) [{args.set_name}]:")
                    print(set_data)
            else:
                sets_data = data.get_smogon_sets(args.pokemon_name, args.format_name)
                if sets_data is None:
                    print(f"Pokemon '{args.pokemon_name}' not found in {args.format_name}")
                    return
                if args.json:
                    print(json.dumps(sets_data, indent=2))
                else:
                    print(f"Smogon sets for {args.pokemon_name} ({args.format_name}):")
                    print(sets_data)
        elif args.smogon_command == 'list':
            if args.format_name:
                formats_to_list = resolve_smogon_formats([args.format_name])
            else:
                formats_to_list = data.get_smogon_formats()
            if not formats_to_list:
                print("No Smogon formats available")
                return
            for fmt in formats_to_list:
                pokemon_list = data.list_smogon_pokemon(fmt)
                if args.count:
                    print(f"{fmt}: {len(pokemon_list)} Pokemon")
                else:
                    print(f"{fmt}: {', '.join(pokemon_list)}")
    else:
        parser.print_help()

def main_cli():
    """Entry point for the CLI command."""
    main()

if __name__ == "__main__":
    main() 
