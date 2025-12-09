import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

class JSONDatabase:
    """Simple JSON-based database manager with configurable directory"""

    def __init__(self, db_dir: str = 'data'):
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(exist_ok=True)

    def _get_path(self, collection: str) -> Path:
        """Get the file path for a collection"""
        return self.db_dir / f"{collection}.json"

    def read(self, collection: str) -> Dict[str, Any]:
        """Read entire collection"""
        path = self._get_path(collection)
        if not path.exists():
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        except Exception as e:
            print(f"Error reading {collection}: {e}")
            return {}

    def write(self, collection: str, data: Dict[str, Any]) -> None:
        """Write entire collection"""
        try:
            path = self._get_path(collection)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing {collection}: {e}")

    def get(self, collection: str, key: str, default: Any = None) -> Any:
        """Get single value from collection"""
        data = self.read(collection)
        return data.get(str(key), default)

    def set(self, collection: str, key: str, value: Any) -> None:
        """Set single value in collection"""
        data = self.read(collection)
        data[str(key)] = value
        self.write(collection, data)

    def exists(self, collection: str, key: str) -> bool:
        """Check if key exists"""
        data = self.read(collection)
        return str(key) in data

    def delete(self, collection: str, key: str) -> bool:
        """Delete key from collection"""
        data = self.read(collection)
        if str(key) in data:
            del data[str(key)]
            self.write(collection, data)
            return True
        return False

    def push(self, collection: str, key: str, item: Any) -> None:
        """Push item to array in collection"""
        data = self.read(collection)
        if str(key) not in data:
            data[str(key)] = []
        if not isinstance(data[str(key)], list):
            data[str(key)] = []
        data[str(key)].append(item)
        self.write(collection, data)

    def pull(self, collection: str, key: str, item: Any) -> bool:
        """Remove item from array in collection"""
        data = self.read(collection)
        if str(key) in data and isinstance(data[str(key)], list):
            try:
                data[str(key)].remove(item)
                self.write(collection, data)
                return True
            except ValueError:
                return False
        return False

    def increment(self, collection: str, key: str, amount: int = 1) -> None:
        """Increment numeric value in collection"""
        data = self.read(collection)
        current = data.get(str(key), 0)
        data[str(key)] = current + amount
        self.write(collection, data)

    def all(self, collection: str) -> Dict[str, Any]:
        """Get all data from collection"""
        return self.read(collection)

    def clear(self, collection: str) -> None:
        """Clear entire collection"""
        self.write(collection, {})

    def size(self, collection: str) -> int:
        """Get number of keys in collection"""
        return len(self.read(collection))

    def keys(self, collection: str) -> List[str]:
        """Get all keys in collection"""
        return list(self.read(collection).keys())

    def values(self, collection: str) -> List[Any]:
        """Get all values in collection"""
        return list(self.read(collection).values())

    def items(self, collection: str) -> List[tuple]:
        """Get all items in collection"""
        return list(self.read(collection).items())


class GuildSettings:
    """Guild-specific settings manager"""

    def __init__(self, db: JSONDatabase):
        self.db = db
        self.collection = 'guild_settings'

    def get_settings(self, guild_id: int) -> Dict[str, Any]:
        """Get all settings for a guild"""
        return self.db.get(self.collection, str(guild_id), {})

    def set_setting(self, guild_id: int, key: str, value: Any) -> None:
        """Set a specific setting for a guild"""
        settings = self.get_settings(guild_id)
        settings[key] = value
        self.db.set(self.collection, str(guild_id), settings)

    def get_setting(self, guild_id: int, key: str, default: Any = None) -> Any:
        """Get a specific setting for a guild"""
        settings = self.get_settings(guild_id)
        return settings.get(key, default)

    def delete_setting(self, guild_id: int, key: str) -> None:
        """Delete a specific setting for a guild"""
        settings = self.get_settings(guild_id)
        if key in settings:
            del settings[key]
            self.db.set(self.collection, str(guild_id), settings)

    def initialize_guild(self, guild_id: int, config: Dict = None) -> None:
        """Initialize default settings for a guild"""
        if not self.db.exists(self.collection, str(guild_id)):
            default_settings = {
                'daily_animal_enabled': False,
                'daily_animal_channel': None,
                'daily_animal_time': config.get('default_daily_time', '08:00') if config else '08:00',
                'daily_animal_hour': 8,
                'daily_animal_minute': 0,
                'last_daily_animal': None,
                'animal_types': config.get('default_animals', []) if config else [],
                'prefix': config.get('prefix', '!') if config else '!',
                'created_at': datetime.now().isoformat()
            }
            self.db.set(self.collection, str(guild_id), default_settings)


class UserStats:
    """User statistics manager"""

    def __init__(self, db: JSONDatabase):
        self.db = db
        self.collection = 'user_stats'

    def get_stats(self, user_id: int) -> Dict[str, Any]:
        """Get all stats for a user"""
        return self.db.get(self.collection, str(user_id), {})

    def increment_command(self, user_id: int, command: str) -> None:
        """Increment command usage count"""
        stats = self.get_stats(user_id)
        if 'commands' not in stats:
            stats['commands'] = {}
        stats['commands'][command] = stats['commands'].get(command, 0) + 1
        self.db.set(self.collection, str(user_id), stats)

    def add_favorite_animal(self, user_id: int, animal: str) -> None:
        """Add favorite animal"""
        stats = self.get_stats(user_id)
        if 'favorite_animals' not in stats:
            stats['favorite_animals'] = {}
        stats['favorite_animals'][animal] = stats['favorite_animals'].get(animal, 0) + 1
        self.db.set(self.collection, str(user_id), stats)

    def get_favorite_animal(self, user_id: int) -> Optional[str]:
        """Get most viewed animal"""
        stats = self.get_stats(user_id)
        animals = stats.get('favorite_animals', {})
        if not animals:
            return None
        return max(animals, key=animals.get)

    def get_total_commands(self, user_id: int) -> int:
        """Get total commands used by user"""
        stats = self.get_stats(user_id)
        return sum(stats.get('commands', {}).values())
