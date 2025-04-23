from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field


class HostAssetAccount(BaseModel):
    username: str


class Account(BaseModel):
    list: List[Dict[str, HostAssetAccount]]


class HostAssetProcessor(BaseModel):
    name: str
    speed: int

class HostAssetProcessorWrapper(BaseModel):
    HostAssetProcessor: HostAssetProcessor

class Processor(BaseModel):
    list: List[HostAssetProcessorWrapper]


class HostAssetInterface(BaseModel):
    interfaceName: Optional[str] = None
    macAddress: Optional[str] = None
    gatewayAddress: Optional[str] = None
    address: str
    hostname: str


class HostAssetInterfaceWrapper(BaseModel):
    HostAssetInterface: HostAssetInterface

class NetworkInterface(BaseModel):
    list: List[HostAssetInterfaceWrapper]


class HostAssetOpenPort(BaseModel):
    serviceName: Optional[str] = None
    protocol: str
    port: int

class HostAssetOpenPortWrapper(BaseModel):
    HostAssetOpenPort: HostAssetOpenPort

class OpenPort(BaseModel):
    list: List[HostAssetOpenPortWrapper]


class HostAssetSoftware(BaseModel):
    name: str
    version: str

class HostAssetSoftwareWrapper(BaseModel):
    HostAssetSoftware: HostAssetSoftware

class Software(BaseModel):
    list: List[HostAssetSoftwareWrapper]

class NumberLong(BaseModel):
    numberLong: int = Field(..., alias="$numberLong")

class HostAssetVolume(BaseModel):
    free: Union[int, NumberLong]
    name: str
    size: Union[int, NumberLong]

class VolumeWrapper(BaseModel):
    HostAssetVolume: HostAssetVolume

class Volume(BaseModel):
    list: List[VolumeWrapper]

class HostInstanceVulnId(BaseModel):
    numberLong: int = Field(..., alias="$numberLong")

class HostAssetVuln(BaseModel):
    hostInstanceVulnId: HostInstanceVulnId
    lastFound: str
    firstFound: str
    qid: int

class HostAssetVulnWrapper(BaseModel):
    HostAssetVuln: HostAssetVuln

class Vuln(BaseModel):
    list: List[HostAssetVulnWrapper]


class LastCheckedIn(BaseModel):
    date: datetime = Field(..., alias="$date")


class ManifestVersion(BaseModel):
    sca: str
    vm: str


class ActivationKey(BaseModel):
    title: str
    activationId: str


class AgentConfiguration(BaseModel):
    id: int
    name: str


class AgentInfo(BaseModel):
    location: str
    locationGeoLatitude: str
    lastCheckedIn: LastCheckedIn
    locationGeoLongtitude: str
    agentVersion: str
    manifestVersion: ManifestVersion
    activatedModule: str
    activationKey: ActivationKey
    agentConfiguration: AgentConfiguration
    status: str
    chirpStatus: str
    connectedFrom: str
    agentId: str
    platform: str


class LastVulnScan(BaseModel):
    date: datetime = Field(..., alias="$date")


class TagSimple(BaseModel):
    id: int
    name: str


class TagSimpleWrapper(BaseModel):
    TagSimple: TagSimple

class Tags(BaseModel):
    list: List[TagSimpleWrapper]


class Ec2AssetSourceSimple(BaseModel):
    instanceType: str
    subnetId: str
    imageId: str
    groupName: str
    accountId: str
    macAddress: str
    createdDate: Optional[str] = None
    reservationId: str
    instanceId: str
    monitoringEnabled: str
    spotInstance: str
    zone: str
    instanceState: str
    privateDnsName: str
    vpcId: str
    type: str
    availabilityZone: str
    privateIpAddress: str
    firstDiscovered: str
    ec2InstanceTags: Dict[str, Any]
    publicIpAddress: str
    lastUpdated: str
    region: str
    assetId: int
    groupId: str
    localHostname: str
    publicDnsName: str


class Ec2AssetSourceSimpleWrapper(BaseModel):
    Ec2AssetSourceSimple: Ec2AssetSourceSimple

class AssetSource(BaseModel):
    pass

class SourceInfo(BaseModel):
    list: List[Union[Ec2AssetSourceSimpleWrapper, Dict[str, AssetSource]]]

class QualysModel(BaseModel):
    account: Account
    address: str
    agentInfo: AgentInfo
    biosDescription: str
    cloudProvider: str
    created: str
    dnsHostName: str
    fqdn: str
    id: int
    isDockerHost: str
    lastComplianceScan: str
    lastLoggedOnUser: Optional[str] = None
    lastSystemBoot: str
    lastVulnScan: LastVulnScan
    manufacturer: str
    model: str
    modified: str
    name: str
    networkGuid: str
    networkInterface: NetworkInterface
    openPort: OpenPort
    os: str
    processor: Processor
    qwebHostId: int
    software: Software
    sourceInfo: SourceInfo
    tags: Tags
    timezone: str
    totalMemory: int
    trackingMethod: str
    type: str
    volume: Volume
    vuln: Vuln
    domain: Optional[str] = None
    netbiosName: Optional[str] = None