from typing import Iterable, TypeVar
from models import CrowdstrikeModel, QualysModel
from api import APIClient
from utils import ConfigManager, logger
from pipeline.AssetNormalizer import AssetNormalizer

T = TypeVar('T') 

class AssetFetcher:
    def __init__(self, skip: int = 0, limit: int = 2):
        self.skip = skip
        self.limit = limit
        self.config = ConfigManager()
        self.url = ""
        self.normalizer = AssetNormalizer()

    def iterate_normalized_hosts(self) -> Iterable[QualysModel]:
        while True:
            with APIClient(self.url, self.config.get_api_key()) as client:
                hosts = client.get_host_data("hosts", self.skip, self.limit)
            if not hosts:
                logger.info("No more hosts to fetch.")
                break
            else:
                logger.info(f"Fetched {len(hosts)} hosts from {self.url}")
            
            self.skip += self.limit
            for host in hosts:
                converted_host = self.convert_host(host)
                yield self.normalizer.normalize(converted_host)

    def convert_host(self, host_data: dict) -> T:
        raise NotImplementedError("Subclasses must implement this method")
    
class CrowdstrikeAsset(AssetFetcher):
    def __init__(self, skip: int = 0, limit: int = 2):
        super().__init__(skip, limit)
        self.url = self.config.get_crowdstrike_url()

    def convert_host(self, host_data: dict) -> CrowdstrikeModel:
        return CrowdstrikeModel(**host_data)

class QualysAsset(AssetFetcher):
    def __init__(self, skip: int = 0, limit: int = 2):
        super().__init__(skip, limit)
        self.url = self.config.get_qualys_url()

    def convert_host(self, host_data: dict) -> QualysModel:
        return QualysModel(**host_data)
