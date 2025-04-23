from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class AssetSource(str, Enum):
    CROWDSTRIKE = "crowdstrike"
    QUALYS = "qualys"


class NetworkInterface(BaseModel):
    interface_name: Optional[str] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    gateway_address: Optional[str] = None


class Software(BaseModel):
    name: str
    version: str


class Policy(BaseModel):
    policy_type: str
    policy_id: str
    applied: bool
    settings_hash: Optional[str] = None
    assigned_date: Optional[str] = None
    applied_date: Optional[str] = None


class OpenPort(BaseModel):
    service_name: Optional[str] = None
    protocol: Optional[str] = None
    port: Optional[int] = None


class DiskVolume(BaseModel):
    name: str
    size: int
    free: int

class Vulnerability(BaseModel):
    vuln_id: int
    first_found: Optional[str] = None
    last_found: Optional[str] = None
    qid: Optional[int] = None


class CloudInfo(BaseModel):
    provider: Optional[str] = None
    account_id: Optional[str] = None
    instance_id: Optional[str] = None
    instance_type: Optional[str] = None
    region: Optional[str] = None
    zone: Optional[str] = None
    vpc_id: Optional[str] = None
    subnet_id: Optional[str] = None


class ProcessorInfo(BaseModel):
    name: Optional[str] = None
    speed: Optional[int] = None
    signature: Optional[str] = None


class SystemInfo(BaseModel):
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    bios_manufacturer: Optional[str] = None
    bios_version: Optional[str] = None
    bios_description: Optional[str] = None
    chassis_type: Optional[str] = None
    chassis_type_desc: Optional[str] = None
    total_memory: Optional[int] = None


class AgentInfo(BaseModel):
    agent_id: Optional[str] = None
    agent_version: Optional[str] = None
    status: Optional[str] = None
    last_checked_in: Optional[datetime] = None
    location: Optional[str] = None
    connected_from: Optional[str] = None
    platform: Optional[str] = None


class NormalizedAsset(BaseModel):
    asset_id: str
    source: AssetSource
    netbios_name: Optional[str] = None
    network_interfaces: List[NetworkInterface] = Field(default_factory=list)
    external_ip: Optional[str] = None
    os: Optional[str] = None
    os_build: Optional[str] = None
    platform_name: Optional[str] = None
    system_info: Optional[SystemInfo] = None
    processor_info: Optional[ProcessorInfo] = None
    software: List[Software] = Field(default_factory=list)
    open_ports: List[OpenPort] = Field(default_factory=list)
    disk_volumes: List[DiskVolume] = Field(default_factory=list)
    policies: List[Policy] = Field(default_factory=list)
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)
    last_vuln_scan: Optional[datetime] = None
    last_compliance_scan: Optional[str] = None
    cloud_info: Optional[CloudInfo] = None
    agent_info: Optional[AgentInfo] = None