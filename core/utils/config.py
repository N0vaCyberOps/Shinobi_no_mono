import json
from pathlib import Path

def load_config():
    config_path = Path('config.json')
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        'bpf_filter': 'tcp port 80 or 443',
        'log_level': 'INFO',
        'log_dir': '/var/log/shinobi'
    }