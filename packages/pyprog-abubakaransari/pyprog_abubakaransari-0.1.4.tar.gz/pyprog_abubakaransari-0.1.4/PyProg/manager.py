# Copyright 2025 Muhammad Abubakar Siddique Ansari
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json

class AssetNotFoundError(FileNotFoundError):
    pass

class PyProgAssetsManager:
    def __init__(self, base_folder='PyProg/assets', record_file='assets.files'):
        self.base_path = os.path.abspath(base_folder)
        self.record_file = os.path.join(self.base_path, record_file)
        os.makedirs(self.base_path, exist_ok=True)

        self.assets = {}
        self.files = {}
        self.all_styles = []
        self.all_themes = []
        self.show_msg = False

        self._load_all()

    def _read_record_file(self):
        if not os.path.exists(self.record_file):
            return []
        with open(self.record_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def _write_record_file(self, paths):
        with open(self.record_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(paths) + '\n')

    def _add_to_record_file(self, path):
        abs_path = os.path.abspath(path)
        paths = self._read_record_file()
        if abs_path not in paths:
            paths.append(abs_path)
            self._write_record_file(paths)

    def _load_file_list(self):
        return [p for p in self._read_record_file() if os.path.isfile(p)]

    def save(self, content: dict, category: str, file_key: str, name: str):
        folder = os.path.join(self.base_path, category)
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"{file_key}.json")

        # Load or create file
        file_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)

        file_data[name] = content

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(file_data, f, indent=4)

        self._add_to_record_file(file_path)

        # Internal dictionaries
        self.assets.setdefault(category, {})[file_key] = file_data
        self.files.setdefault(category, {})[file_key] = file_path

        # Dynamic object structure
        cat_obj = getattr(self, category, type('CategoryObj', (), {})())
        setattr(self, category, cat_obj)
        key_obj = getattr(cat_obj, file_key, type('FileKeyObj', (), {})())
        setattr(cat_obj, file_key, key_obj)
        setattr(key_obj, name, content)

        # Update names list
        if category == 'spinner':
            if file_key == 'style':
                self.all_styles = list(file_data.keys())
                setattr(cat_obj, 'all_styles', self.all_styles)
            elif file_key == 'theme':
                self.all_themes = list(file_data.keys())
                setattr(cat_obj, 'all_themes', self.all_themes)

        if self.show_msg:
            print(f"✅ Saved '{name}' → '{category}/{file_key}.json'")

    def load(self, category: str, file_key: str, name: str):
        folder = os.path.join(self.base_path, category)
        file_path = os.path.join(folder, f"{file_key}.json")
        if not os.path.isfile(file_path):
            raise AssetNotFoundError(f"File '{file_key}.json' not found in '{category}'")

        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)

        if name not in file_data:
            raise AssetNotFoundError(f"Asset '{name}' not found in '{file_key}.json'")

        asset_data = file_data[name]

        cat_obj = getattr(self, category, type('CategoryObj', (), {})())
        setattr(self, category, cat_obj)
        key_obj = getattr(cat_obj, file_key, type('FileKeyObj', (), {})())
        setattr(cat_obj, file_key, key_obj)
        setattr(key_obj, name, asset_data)

        return asset_data

    def _load_all(self):
        self.all_styles.clear()
        self.all_themes.clear()

        for path in self._load_file_list():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                category = os.path.basename(os.path.dirname(path))
                file_key = os.path.splitext(os.path.basename(path))[0]

                self.assets.setdefault(category, {})[file_key] = data
                self.files.setdefault(category, {})[file_key] = path

                cat_obj = getattr(self, category, type('CategoryObj', (), {})())
                setattr(self, category, cat_obj)
                key_obj = getattr(cat_obj, file_key, type('FileKeyObj', (), {})())
                setattr(cat_obj, file_key, key_obj)

                for name, content in data.items():
                    setattr(key_obj, name, content)

                # Add to global lists for 'spinner'
                if category == 'spinner':
                    if file_key == 'style':
                        self.all_styles += list(data.keys())
                        setattr(cat_obj, 'all_styles', list(data.keys()))
                    elif file_key == 'theme':
                        self.all_themes += list(data.keys())
                        setattr(cat_obj, 'all_themes', list(data.keys()))

            except Exception as e:
                print(f"⚠️ Failed to load asset from {path}: {e}")

    def delete(self, category: str, file_key: str, name: str):
        file_path = os.path.join(self.base_path, category, f"{file_key}.json")
        if not os.path.exists(file_path):
            raise AssetNotFoundError(f"File '{file_key}.json' not found")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if name not in data:
            raise AssetNotFoundError(f"Asset '{name}' not found in '{file_key}.json'")

        del data[name]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.assets[category][file_key].pop(name, None)
        if category == 'spinner':
            if file_key == 'style':
                self.all_styles = list(data.keys())
            elif file_key == 'theme':
                self.all_themes = list(data.keys())

        if self.show_msg:
            print(f"🗑️ Deleted '{name}' from '{category}/{file_key}.json'")

    def rename(self, category: str, file_key: str, old_name: str, new_name: str):
        file_path = os.path.join(self.base_path, category, f"{file_key}.json")
        if not os.path.exists(file_path):
            raise AssetNotFoundError(f"File '{file_key}.json' not found")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if old_name not in data:
            raise AssetNotFoundError(f"Asset '{old_name}' not found")
        if new_name in data:
            raise ValueError(f"Asset '{new_name}' already exists")

        data[new_name] = data.pop(old_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        self.assets[category][file_key] = data

        if self.show_msg:
            print(f"✏️ Renamed '{old_name}' → '{new_name}'")

    def get_path(self, category: str, file_key: str):
        path = os.path.join(self.base_path, category, f"{file_key}.json")
        if not os.path.exists(path):
            raise AssetNotFoundError(f"Path '{path}' not found")
        return os.path.abspath(path)

    def list_all(self):
        return self.files
