#!/usr/bin/env python3
import os
import re
import struct
from pathlib import Path
from typing import Optional, List, Dict, Tuple


class SteamGameFinder:
    def __init__(self):
        self.steam_root = self._find_steam_root()
        self.library_folders = self._get_library_folders()

    def _find_steam_root(self) -> Optional[Path]:
        """Steamroot"""
        possible_paths = [
            Path.home() / ".steam" / "steam",
            Path.home() / ".steam" / "root",
            Path.home() / ".local" / "share" / "Steam",
            Path("/usr/share/steam"),
        ]

        for path in possible_paths:
            if path.exists() and (path / "steamapps").exists():
                return path
        return None

    def _parse_vdf_file(self, file_path: Path) -> Dict:
        """Parsing a VDF file"""
        if not file_path.exists():
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return {}

        result = {}
        lines = content.split('\n')
        stack = [result]

        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            if line == '{':
                continue
            elif line == '}':
                if len(stack) > 1:
                    stack.pop()
                continue

            if '"' in line:
                parts = line.split('"')
                if len(parts) >= 3:
                    key = parts[1]
                    if len(parts) >= 5:
                        value = parts[3]
                        stack[-1][key] = value
                    else:
                        stack[-1][key] = {}
                        stack.append(stack[-1][key])

        return result

    def _get_library_folders(self) -> List[Path]:
        """Getting all Steam libraries"""
        if not self.steam_root:
            return []

        folders = [self.steam_root / "steamapps"]

        # Additional paths?
        library_file = self.steam_root / "steamapps" / "libraryfolders.vdf"
        if library_file.exists():
            data = self._parse_vdf_file(library_file)

            # 2021 format
            if "libraryfolders" in data:
                for key, folder_data in data["libraryfolders"].items():
                    if isinstance(folder_data, dict) and "path" in folder_data:
                        path = Path(folder_data["path"]) / "steamapps"
                        if path.exists():
                            folders.append(path)
            else:
                # Legacy
                for key, value in data.items():
                    if key.isdigit() and isinstance(value, dict) and "path" in value:
                        path = Path(value["path"]) / "steamapps"
                        if path.exists():
                            folders.append(path)

        return list(set(folders))  # No duplicates

    def find_game_by_appid(self, app_id: str) -> Optional[Tuple[Path, Path]]:
        """
        Finding the game by ID
        Tuple (game_path, library_path)
        """
        for library_path in self.library_folders:
            # .acf files?
            acf_file = library_path / f"appmanifest_{app_id}.acf"
            if acf_file.exists():
                # parsing
                acf_data = self._parse_vdf_file(acf_file)

                if "AppState" in acf_data and "installdir" in acf_data["AppState"]:
                    install_dir = acf_data["AppState"]["installdir"]
                    game_path = library_path / "common" / install_dir

                    if game_path.exists():
                        return game_path, library_path

        return None

    def find_proton_prefix(self, app_id: str, library_path: Optional[Path] = None) -> Optional[Path]:
        """Find the proton prefix for the game"""
        if library_path:
            # Exact library
            compatdata_path = library_path / "compatdata" / app_id / "pfx"
            if compatdata_path.exists():
                return compatdata_path

        # All libraries
        for lib_path in self.library_folders:
            compatdata_path = lib_path / "compatdata" / app_id / "pfx"
            if compatdata_path.exists():
                return compatdata_path

        return None # Damn it

    def get_game_info(self, app_id: str) -> Dict[str, Optional[str]]:
        """Getting info about the game"""
        result = {
            "app_id": app_id,
            "game_path": None,
            "proton_prefix": None,
            "library_path": None,
            "found": False
        }

        game_info = self.find_game_by_appid(app_id)
        if game_info:
            game_path, library_path = game_info
            result["game_path"] = str(game_path)
            result["library_path"] = str(library_path)
            result["found"] = True

            # finding proton prefix
            proton_prefix = self.find_proton_prefix(app_id, library_path)
            if proton_prefix:
                result["proton_prefix"] = str(proton_prefix)

        return result