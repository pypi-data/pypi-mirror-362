import tomllib
import json

CONFIG_FILE = 'pyproject.toml'

def load_config(file_path: str) -> dict:
    """Loads and parses a TOML configuration file."""
    with open(file_path, 'rb') as file:
        return tomllib.load(file)

if __name__ == '__main__':
    config = load_config(CONFIG_FILE)
    # bug_tracker_url = config['project']['urls']['Bug Tracker']
    print(json.dumps(config, indent=2))