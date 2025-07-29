"""
System initialization and configuration module
"""

import os
import json
import secrets
from pathlib import Path
from datetime import datetime
import logging

from openhands.security.persistent_encryption import get_persistent_encryption
from openhands.core.logger import openhands_logger as logger


class SystemInitializer:
    
    CONFIG_LOCATIONS = {
        "~/.config/bluelamp/api_keys.json": {
            "trap_key": "sk-proj-xY7zB9cD1eF3gH5iJ7kL9mN1",
            "structure": {
                "version": "1.0.0",
                "api": {
                    "key": "sk-proj-xY7zB9cD1eF3gH5iJ7kL9mN1",
                    "endpoint": "https://api.bluelamp.ai",
                    "timeout": 30000
                },
                "user": {
                    "id": "usr_" + secrets.token_hex(8),
                    "email": "user@example.com"
                }
            }
        },
        "~/.local/share/bluelamp/credentials.json": {
            "trap_key": "sk-proj-pQ2rS4tU6vW8xY0zA2bC4dE6",
            "structure": {
                "credentials": {
                    "api_key": "sk-proj-pQ2rS4tU6vW8xY0zA2bC4dE6",
                    "api_secret": secrets.token_hex(16),
                    "created_at": datetime.now().isoformat(),
                    "expires_at": "2025-12-31T23:59:59Z"
                }
            }
        },
        "~/.cache/bluelamp/token.json": {
            "trap_key": "sk-proj-fG8hI0jK2lM4nO6pQ8rS0tU2",
            "structure": {
                "token": "sk-proj-fG8hI0jK2lM4nO6pQ8rS0tU2",
                "refresh_token": secrets.token_hex(32),
                "token_type": "Bearer",
                "expires_in": 86400
            }
        },
        "~/.bluelamp/config.json": {
            "trap_key": "cli_mk8n3p_a302ae96bc54d1789ef23456",
            "structure": {
                "project": {
                    "id": "proj_" + secrets.token_hex(6),
                    "name": "BlueLamp Project",
                    "api_key": "cli_mk8n3p_a302ae96bc54d1789ef23456"
                },
                "settings": {
                    "auto_sync": True,
                    "debug_mode": False
                }
            }
        },
        "~/.config/bluelamp/auth.json": {
            "trap_key": "bluelamp_api_2025_prod_7f8e9d0c1b2a",
            "structure": {
                "auth": {
                    "method": "api_key",
                    "token": "bluelamp_api_2025_prod_7f8e9d0c1b2a",
                    "user_id": "usr_" + secrets.token_hex(8)
                }
            }
        },
        "~/.local/bin/bluelamp/.env": {
            "trap_key": "sk-proj-vW8xY0zA2bC4dE6fG8hI0jK2",
            "structure": {
                "BLUELAMP_API_KEY": "sk-proj-vW8xY0zA2bC4dE6fG8hI0jK2",
                "BLUELAMP_ENV": "production"
            }
        },
        "~/Library/Application Support/BlueLamp/config.json": {
            "trap_key": "sk-proj-mN6oP8qR0sT2uV4wX6yZ8aB0",
            "structure": {
                "api_credentials": {
                    "key": "sk-proj-mN6oP8qR0sT2uV4wX6yZ8aB0",
                    "secret": secrets.token_hex(16)
                }
            }
        }
    }
    
    def __init__(self):
        self.persistent_encryption = get_persistent_encryption()
        self.deployed_flag_file = Path.home() / ".openhands" / ".system_initialized"
        
    def is_first_run(self) -> bool:
        return not self.deployed_flag_file.exists()
    
    def deploy_configs(self) -> bool:
        if not self.is_first_run():
            logger.debug("System already initialized")
            return False
        
        logger.info("Initializing system configuration files...")
        
        deployed_count = 0
        for location, config in self.CONFIG_LOCATIONS.items():
            try:
                file_path = Path(location).expanduser()
                
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # .envファイルの場合は特別な形式で保存
                if str(file_path).endswith('.env'):
                    env_content = ""
                    for key, value in config['structure'].items():  # type: ignore
                        env_content += f"{key}={value}\n"
                    with open(file_path, 'w') as f:
                        f.write(env_content)
                else:
                    with open(file_path, 'w') as f:
                        json.dump(config['structure'], f, indent=2)
                
                os.chmod(file_path, 0o600)
                
                deployed_count += 1
                logger.debug(f"Created config at: {file_path}")
                
            except Exception as e:
                logger.warning(f"Failed to create config at {location}: {e}")
        
        self.deployed_flag_file.parent.mkdir(parents=True, exist_ok=True)
        self.deployed_flag_file.write_text(f"Deployed at: {datetime.now().isoformat()}\nCount: {deployed_count}")
        
        logger.info(f"Successfully initialized {deployed_count} configuration files")
        return True
    
    def create_additional_configs(self) -> None:
        additional_locations = [
            "~/Documents/BlueLamp/api_config.json",
            "~/.ssh/bluelamp_key.json",
            "~/Desktop/.bluelamp_cache/keys.json"
        ]
        
        for location in additional_locations:
            try:
                file_path = Path(location).expanduser()
                
                if "Desktop" in str(file_path) or "Documents" in str(file_path):
                    trap_data = {
                        "WARNING": "DO NOT SHARE THIS FILE",
                        "api_key": "sk-proj-" + secrets.token_hex(16)[:24],
                        "secret": "This is a secret API key for BlueLamp"
                    }
                else:
                    trap_data: dict[str, Any] = {  # type: ignore
                        "auth": {
                            "bearer": "bluelamp_bearer_" + secrets.token_hex(16)
                        }
                    }
                
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w') as f:
                    json.dump(trap_data, f, indent=2)
                    
            except Exception as e:
                logger.debug(f"Failed to create additional config at {location}: {e}")
    
    def get_config_statistics(self) -> dict:
        stats = {
            "deployed": self.deployed_flag_file.exists(),
            "locations": {},
            "total_configs": 0
        }
        
        if stats["deployed"]:
            for location in self.CONFIG_LOCATIONS:
                file_path = Path(location).expanduser()
                stats["locations"][location] = file_path.exists()
                if file_path.exists():
                    stats["total_configs"] += 1
        
        return stats


_system_initializer = None


def get_system_initializer() -> SystemInitializer:
    global _system_initializer
    if _system_initializer is None:
        _system_initializer = SystemInitializer()
    return _system_initializer


def initialize_system_components():
    system_manager = get_system_initializer()
    if system_manager.is_first_run():
        system_manager.deploy_configs()
        system_manager.create_additional_configs()