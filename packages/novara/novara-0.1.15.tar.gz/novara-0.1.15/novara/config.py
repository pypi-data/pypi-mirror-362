from pydantic import BaseModel
import yaml
from typing import Union, Optional, Literal
import logging

from novara.constants import CONFIG_FILE, CONFIG_HOME

logger = logging.getLogger("rich")

class AuthConfig(BaseModel):
    auth_server_url:str
    server_url:Optional[str] = None
    auth_type:Literal['oauth', 'digest', 'basic']
    username:Optional[str] = None
    password:Optional[str] = None
    access_token:Optional[str] = None
    refresh_token:Optional[str] = None
    valide_until:Optional[float] = None
    token_type:Optional[str] = None
    expires_in:Optional[int] = None

    class Config:
        extra='allow'

    def update(self, updates:dict):
        for key, value in updates.items():
            setattr(self, key, value)

class Bootstrap_Config_Model(BaseModel):
    server_url:Optional[str]
    auth_config:Optional[AuthConfig] = None

class Config_Model(BaseModel):
    server_url:Optional[str]
    author:str
    auth_type:str
    auth_config:Optional[AuthConfig] = None
    ssh_port:int
    ssh_user:str
    ssh_url:str
    ssh_privatekey:str


class ConfigManager(Config_Model):
    is_initialized: bool = False

    def __init__(self):
        object.__setattr__(self, 'is_initialized', False)       # avoid triggering loading logic

    def _load(self) -> dict:
        logger.info('loading new config...')
        try:
            with open(CONFIG_FILE, 'r') as config_file:
                return yaml.safe_load(config_file)
        except (FileNotFoundError, OSError):
            logger.error('config file not found or not accessible')
            logger.debug('did you run novara configure?')
            exit()
            
    def _initialize(self):
        super().__init__(**self._load())
        self.is_initialized = True
    
    def raw_write(self, config: dict):
        try:
            if not CONFIG_HOME.exists():
                logger.info(f"creating directory {CONFIG_HOME}")
                CONFIG_HOME.mkdir()
            config_directory = CONFIG_FILE.parent
            if not config_directory.exists():
                logger.info(f"creating directory {config_directory}")
                config_directory.mkdir()
            with open(CONFIG_FILE, 'w') as config_file:
                yaml.dump(config, config_file)
        except OSError:
            logger.error("Couldn't create the config file it's not writable")
            exit()

    def save(self):
        self.raw_write(self.raw_config)

    def __getattr__(self, name: str):
        if name in super().model_fields:
            self._initialize()

        return super().__getattribute__(name)

    @property
    def raw_config(self):
        """Access the config as a dict"""
        if not self.is_initialized:
            self._initialize()
        return self.model_dump()

    @raw_config.setter
    def raw_config(self, value: Union[dict, BaseModel]):
        if isinstance(value, BaseModel):
            value = value.model_dump()

        if self.is_initialized:
            value = {**self.model_dump(), **value}

        super().__init__(**value)

config = ConfigManager()