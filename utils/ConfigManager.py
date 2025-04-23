import json
import logging
from typing import Dict, Any, Optional
from utils.Logger import logger


class ConfigManager:    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return {}
        
    def get_api_key(self) -> Optional[str]:
        return self.config.get("api-key")
    
    def get_crowdstrike_url(self) -> Optional[str]:
        return self.config.get("crowdstrike-url")
    
    def get_qualys_url(self) -> Optional[str]:
        return self.config.get("qualys-url")
    
    def get_connection_string(self) -> Optional[str]:
        return self.config.get("mongo-connection-string")
    
    def get_database_name(self) -> Optional[str]:
        return self.config.get("database-name")
    
    def get_collection_name(self) -> Optional[str]:
        return self.config.get("collection-name")