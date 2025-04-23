from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class PolicyDetails(BaseModel):
    policy_type: str
    policy_id: str
    applied: bool
    settings_hash: Optional[str] = None
    assigned_date: str
    applied_date: str
    rule_groups: Optional[List[Any]] = Field(default_factory=list) 
    uninstall_protection: Optional[str] = None
    rule_set_id: Optional[str] = None

class ModifiedTimestamp(BaseModel):
    date: datetime = Field(..., alias="$date")
        
class Meta(BaseModel):
    version: str
    version_string: str
    
class CrowdstrikeModel(BaseModel):
    id: str = Field(..., alias="_id")
    device_id: str
    cid: str
    agent_load_flags: str
    agent_local_time: str
    agent_version: str
    bios_manufacturer: Optional[str] = None
    bios_version: Optional[str] = None
    config_id_base: str
    config_id_build: str
    config_id_platform: str
    cpu_signature: Optional[str] = None
    external_ip: str
    mac_address: str
    instance_id: Optional[str] = None
    service_provider: Optional[str] = None
    service_provider_account_id: Optional[str] = None
    hostname: str
    first_seen: str
    last_seen: str
    local_ip: str
    major_version: str
    minor_version: str
    os_version: str
    os_build: Optional[str] = None
    platform_id: str
    platform_name: str
    policies: List[PolicyDetails]
    reduced_functionality_mode: str
    device_policies: Dict[str, PolicyDetails]
    groups: List[str]
    group_hash: str
    product_type_desc: str
    provision_status: str
    serial_number: str
    status: str
    system_manufacturer: Optional[str] = None
    system_product_name: Optional[str] = None
    tags: List[Any] = Field(default_factory=list)
    modified_timestamp: ModifiedTimestamp
    meta: Meta
    zone_group: Optional[str] = None
    kernel_version: str
    chassis_type: Optional[str] = None
    chassis_type_desc: Optional[str] = None
    connection_ip: Optional[str] = None
    default_gateway_ip: Optional[str] = None
    connection_mac_address: Optional[str] = None