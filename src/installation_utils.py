import os
import time
import zipfile
from pathlib import Path
from PySide6 import QtCore
import requests
import json

def get_latest_geode_tag() -> str:
    url = 'https://api.geode-sdk.org/v1/loader/versions/latest'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Error code: {}".format(response.status_code))

    json_result = response.json()
    if json_result['error'] != '':
        raise Exception("Reason: {}".format(json_result['error']))

    if json_result.get('payload') is None:
        raise Exception("Payload is None")

    return json_result.get('payload').get('tag')

def get_download_url() -> str:
    tag = get_latest_geode_tag()
    return 'https://github.com/geode-sdk/geode/releases/download/{}/geode-{}-win.zip'.format(tag, tag)

def unzip_to_destination(zip_url: str, destination_dir: str) -> None:
    zip_response = requests.get(zip_url, stream=True)
    zip_file_path = os.path.join(destination_dir, "geode_win.zip")
    with open(zip_file_path, 'wb') as f:
        for chunk in zip_response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)
    os.remove(zip_file_path)

def install_to_dir(destination_dir: str) -> None:
    win_zip_release_link = get_download_url()
    unzip_to_destination(win_zip_release_link, destination_dir)

def get_steam_gd_path() -> Path:
    gd_path = f'{os.getenv('HOME')}/.steam/steam/steamapps/common/Geometry Dash'
    return Path(gd_path)

def get_steam_gd_prefix() -> Path:
    pfx_path = f'{os.getenv('HOME')}/.steam/steam/steamapps/compatdata/322170/pfx'
    return Path(pfx_path)


def patch_prefix_registry(reg_file_path: str) -> None:
    # We need to patch Wine registry adding a simple dll override
    with open(reg_file_path, 'r') as f:
        content = f.read()

    # Find the DllOverrides section
    dll_overrides_section = "[Software\\\\Wine\\\\DllOverrides]"

    if dll_overrides_section not in content:
        # If section doesn't exist, add it
        content += f"\n\n{dll_overrides_section} {int(time.time())}\n#time={hex(int(time.time()))[2:]}\n"
        content += '"xinput1_4"="native,builtin"\n'
    else:
        # Section exists, check if xinput1_4 key is present
        lines = content.split('\n')
        dll_section_found = False
        xinput_found = False
        insert_index = -1

        for i, line in enumerate(lines):
            if line.startswith(dll_overrides_section):
                dll_section_found = True
                continue

            if dll_section_found:
                # We're in the DllOverrides section
                if line.startswith('[') and not line.startswith(dll_overrides_section):
                    # We've reached the next section, insert xinput here if not found
                    insert_index = i
                    break
                elif '"xinput1_4"=' in line:
                    xinput_found = True
                    break
                elif line.strip() == '':
                    # Empty line, potential insertion point
                    insert_index = i

        # If xinput1_4 not found, add it
        if not xinput_found:
            if insert_index == -1:
                # Add at the end of file
                content += '\n"xinput1_4"="native,builtin"\n'
            else:
                # Insert at the found position
                lines.insert(insert_index, '"xinput1_4"="native,builtin"')
                content = '\n'.join(lines)

    # Write the modified content back
    with open(reg_file_path, 'w') as f:
        f.write(content)

def install_geode_to_wine(prefix: Path, gd_path: Path) -> None:
    if not prefix.exists():
        raise Exception("Can't find prefix: {}".format(prefix))

    if not gd_path.exists():
        raise Exception("Can't find Geometry Dash: {}".format(gd_path))

    install_to_dir(gd_path.as_posix())
    patch_prefix_registry((prefix / 'user.reg').as_posix())

def install_geode_to_steam():
    steam_gd_path = get_steam_gd_path()
    steam_gd_prefix = get_steam_gd_prefix()

    if not steam_gd_path.exists():
        raise Exception("Can't find Steam GD at {}".format(steam_gd_path))

    install_geode_to_wine(steam_gd_prefix, steam_gd_path)

class WineInstallationThread(QtCore.QThread):
    finished_signal = QtCore.Signal(bool, str)

    def __init__(self, wine_prefix: Path, gd_path: Path, parent=None):
        super().__init__(parent)
        self.wine_prefix = wine_prefix
        self.gd_path = gd_path

    def run(self):
        try:
            install_geode_to_wine(self.wine_prefix, self.gd_path)
            self.finished_signal.emit(True, "Success!")
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class SteamInstallationThread(QtCore.QThread):
    finished_signal = QtCore.Signal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            install_geode_to_steam()
            self.finished_signal.emit(True, "Success!")
        except Exception as e:
            self.finished_signal.emit(False, str(e))