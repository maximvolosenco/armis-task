from typing import Any, Dict, Optional, Set
from models import NormalizedAsset


class DeduplicationStrategy:
    def get_comparison_value(self, asset: NormalizedAsset) -> Any:
        raise NotImplementedError("Deduplication strategies must implement get_comparison_value")
    
    def are_duplicates(self, asset1: NormalizedAsset, asset2: NormalizedAsset) -> bool:
        set1 = self.get_comparison_value(asset1)
        set2 = self.get_comparison_value(asset2)
        if set1 and set2:
            return set1 == set2
        return False

    def get_query(self, asset: NormalizedAsset) -> Optional[dict]:
        return None

class OsStrategy(DeduplicationStrategy):
    def get_comparison_value(self, asset: NormalizedAsset) -> Set[str]:
        return set(asset.os)
    
    def get_query(self, asset: NormalizedAsset) -> Optional[dict]:
        if asset.os:
            return {"os": asset.os}
        return {"os": "nan"}

class IPAddressStrategy(DeduplicationStrategy):
    def get_comparison_value(self, asset: NormalizedAsset) -> Set[str]:
        return set(asset.external_ip)
    
    def get_query(self, asset: NormalizedAsset) -> Optional[dict]:
        if asset.external_ip:
            return {"external_ip": asset.external_ip}
        return {"external_ip": "nan"}

class IdStrategy(DeduplicationStrategy):
    def get_comparison_value(self, asset: NormalizedAsset) -> Set[str]:
        return set(asset.asset_id)
    
    def get_query(self, asset: NormalizedAsset) -> Optional[dict]:
        if asset.external_ip:
            return {"asset_id": asset.asset_id}
        return {"asset_id": "nan"}

# need refactor
class SystemInfoStrategy(DeduplicationStrategy):
    def get_comparison_value(self, asset: NormalizedAsset) -> Dict[str, str]:
        if not asset.system_info:
            return set()
        
        return set(vars(asset.system_info).values())
    
class CloudInfoStrategy(DeduplicationStrategy):
    def get_comparison_value(self, asset: NormalizedAsset) -> Dict[str, str]:
        if not asset.cloud_info:
            return set()
        
        return set(vars(asset.cloud_info).values())

class NetworkInterfaceStrategy(DeduplicationStrategy):
    def get_comparison_value(self, asset: NormalizedAsset) -> Set[str]:
        network_interfaces = set()
        for interface in asset.network_interfaces:
            network_interfaces.add(vars(interface).values())
        return network_interfaces
    