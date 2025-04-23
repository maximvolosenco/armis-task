from typing import List, Union
from models import (
    CrowdstrikeModel,
    QualysModel,
    NetworkInterface,
    AssetSource,
    Software,
    Policy,
    OpenPort,
    DiskVolume,
    Vulnerability,
    CloudInfo,
    ProcessorInfo,
    SystemInfo,
    AgentInfo,
    NormalizedAsset,
    Ec2AssetSourceSimpleWrapper
)

class AssetNormalizer:
    def normalize(self, item: Union[CrowdstrikeModel, QualysModel]) -> NormalizedAsset:
        if isinstance(item, CrowdstrikeModel):
            return self.__normalize_crowdstrike(item)
        elif isinstance(item, QualysModel):
            return self.__normalize_qualys(item)
        else:
            raise TypeError(f"Unsupported type: {type(item)}")
        
    @staticmethod
    def __normalize_crowdstrike(
        crowdstrike_item: CrowdstrikeModel,
    ) -> NormalizedAsset:
        normalized_policies: List[Policy] = []

        for policy in crowdstrike_item.policies:
            normalized_policies = [
                Policy(
                    policy_type=policy.policy_type,
                    policy_id=policy.policy_id,
                    applied=policy.applied,
                    settings_hash=policy.settings_hash,
                    assigned_date=policy.assigned_date,
                    applied_date=policy.applied_date,
                )
            ]

        network_interfaces = [
            NetworkInterface(
                mac_address=crowdstrike_item.mac_address,
                ip_address=crowdstrike_item.local_ip,
                gateway_address=crowdstrike_item.default_gateway_ip,
                hostname=crowdstrike_item.hostname
            )
        ]

        system_info = SystemInfo(
            manufacturer=crowdstrike_item.system_manufacturer,
            model=crowdstrike_item.system_product_name,
            serial_number=crowdstrike_item.serial_number,
            bios_manufacturer=crowdstrike_item.bios_manufacturer,
            bios_version=crowdstrike_item.bios_version,
            chassis_type=crowdstrike_item.chassis_type,
            chassis_type_desc=crowdstrike_item.chassis_type_desc,
        )

        processor_info = ProcessorInfo(signature=crowdstrike_item.cpu_signature)

        cloud_info = None
        if crowdstrike_item.service_provider:
            cloud_info = CloudInfo(
                provider=crowdstrike_item.service_provider,
                account_id=crowdstrike_item.service_provider_account_id,
                instance_id=crowdstrike_item.instance_id,
            )

        agent_info = AgentInfo(
            agent_version=crowdstrike_item.agent_version, status=crowdstrike_item.status
        )

        software: List[Software] = []
        if crowdstrike_item.kernel_version:
            software.append(Software(
                name="Kernel",
                version=crowdstrike_item.kernel_version
            ))

        return NormalizedAsset(
                asset_id=crowdstrike_item.device_id,
                source=AssetSource.CROWDSTRIKE,
                network_interfaces=network_interfaces,
                external_ip=crowdstrike_item.external_ip,
                software=software,
                os=crowdstrike_item.os_version,
                os_build=crowdstrike_item.os_build,
                platform_name=crowdstrike_item.platform_name,
                kernel_version=crowdstrike_item.kernel_version,
                system_info=system_info,
                processor_info=processor_info,
                policies=normalized_policies,
                cloud_info=cloud_info,
                agent_info=agent_info
            )
        
    @staticmethod
    def __normalize_qualys(qualys_item: QualysModel) -> NormalizedAsset:
        network_interfaces = []
        
        for interface in qualys_item.networkInterface.list:
            network_interfaces.append(
                NetworkInterface(
                    interface_name=interface.HostAssetInterface.interfaceName,
                    mac_address=interface.HostAssetInterface.macAddress,
                    ip_address=interface.HostAssetInterface.address,
                    hostname=interface.HostAssetInterface.hostname,
                    gateway_address=interface.HostAssetInterface.gatewayAddress
                )
            )
            
        software_list = []
        for software in qualys_item.software.list:
            software_list.append(
                Software(
                    name=software.HostAssetSoftware.name,
                    version=software.HostAssetSoftware.version
                )
            )
        
        open_ports = []
        for port in qualys_item.openPort.list:
            open_ports.append(
                OpenPort(
                    service_name=port.HostAssetOpenPort.serviceName,
                    protocol=port.HostAssetOpenPort.protocol,
                    port=port.HostAssetOpenPort.port
                )
            )
        
        volumes = []
        for volume_wrapper in qualys_item.volume.list:
            volume = volume_wrapper.HostAssetVolume
            
            if isinstance(volume.size, int):
                size = volume.size
                free = volume.free
            else:
                size = volume.size.numberLong
                free = volume.size.numberLong
            
            volumes.append(
                DiskVolume(
                    name=volume.name,
                    size=size,
                    free=free
                )
                )
        
        vulns = []
        for vuln_wrapper in qualys_item.vuln.list:
            vuln = vuln_wrapper.HostAssetVuln
            vulns.append(
                Vulnerability(
                    vuln_id=vuln.hostInstanceVulnId.numberLong,
                    first_found=vuln.firstFound,
                    last_found=vuln.lastFound,
                    qid=vuln.qid
                )
            )

        
        processor_info = None
        for processor in qualys_item.processor.list:
            processor_info = ProcessorInfo(
                name=processor.HostAssetProcessor.name,
                speed=processor.HostAssetProcessor.speed
            )
        
        system_info = SystemInfo(
            manufacturer=qualys_item.manufacturer,
            model=qualys_item.model,
            bios_description=qualys_item.biosDescription,
            total_memory=qualys_item.totalMemory
        )
        
        agent_info = AgentInfo(
            agent_id=qualys_item.agentInfo.agentId,
            agent_version=qualys_item.agentInfo.agentVersion,
            status=qualys_item.agentInfo.status,
            last_checked_in=qualys_item.agentInfo.lastCheckedIn.date,
            location=qualys_item.agentInfo.location,
            connected_from=qualys_item.agentInfo.connectedFrom,
            platform=qualys_item.agentInfo.platform
        )
        
        cloud_info = None
        for source in qualys_item.sourceInfo.list:
            if isinstance(source, Ec2AssetSourceSimpleWrapper):
                cloud_info = CloudInfo(
                    account_id=source.Ec2AssetSourceSimple.accountId,
                    instance_id=source.Ec2AssetSourceSimple.instanceId,
                    instance_type=source.Ec2AssetSourceSimple.instanceType,
                    region=source.Ec2AssetSourceSimple.region,
                    zone=source.Ec2AssetSourceSimple.zone,
                    vpc_id=source.Ec2AssetSourceSimple.vpcId,
                    subnet_id=source.Ec2AssetSourceSimple.subnetId
                )
        
        return NormalizedAsset(
        asset_id=str(qualys_item.id),
        source=AssetSource.QUALYS,
        netbios_name=qualys_item.netbiosName,
        external_ip=qualys_item.address,
        network_interfaces=network_interfaces,      
        os=qualys_item.os,        
        system_info=system_info,
        processor_info=processor_info,        
        software=software_list,
        open_ports=open_ports,
        disk_volumes=volumes,
        vulnerabilities=vulns,
        last_vuln_scan=qualys_item.lastVulnScan.date,
        last_compliance_scan=qualys_item.lastComplianceScan,
        cloud_info=cloud_info,
        agent_info=agent_info,
    )

