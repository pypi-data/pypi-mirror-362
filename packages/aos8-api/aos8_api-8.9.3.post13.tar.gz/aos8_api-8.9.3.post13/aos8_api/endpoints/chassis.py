from helper import parse_system_output_json
from typing import Optional
from endpoints.base import BaseEndpoint
from models import ApiResult

class ChassisEndpoint(BaseEndpoint):
    """
    Endpoint to manage chassis on an Alcatel-Lucent OmniSwitch using MIB-based API commands.
    """
    def hardwareinfo(self, limit: int = 200) -> ApiResult:
        """
        Retrieve chassis component and environmental status.

        Args:
            limit (int): Maximum number of rows to retrieve.

        Returns:
            ApiResult: Parsed data including hardware, temperature, and status info.
        """
        params = {
            "domain": "mib",
            "urn": "chasChassisTable",
            "mibObject0": "entPhysicalIndex",
            "mibObject1": "entPhysicalModelName",
            "mibObject2": "chasEntPhysPartNumber",
            "mibObject3": "entPhysicalClass",
            "mibObject4": "entPhysicalDescr",
            "mibObject5": "entPhysicalHardwareRev",
            "mibObject6": "entPhysicalSerialNum",
            "mibObject7": "entPhysicalMfgName",
            "mibObject8": "chasEntPhysAdminStatus",
            "mibObject9": "chasEntPhysOperStatus",
            "mibObject10": "chasNumberOfResets",
            "mibObject11": "chasCPMAHardwareBoardTemp",
            "mibObject12": "chasTempThreshold",
            "mibObject13": "chasTempRange",
            "mibObject14": "chasDangerTempThreshold",
            "function": "chassisSlotArr_entPhysIndex",
            "object": "entPhysicalIndex",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)

    def temperature(self, limit: int = 200) -> ApiResult:
        """
        Retrieve current temperature, thresholds, and status for all temperature sensors.

        Args:
            limit (int): Max number of entries to retrieve. Defaults to 200.

        Returns:
            ApiResult: Parsed temperature data including thresholds and sensor status.
        """
        params = {
            "domain": "mib",
            "urn": "chasEntTemperatureTable",
            "mibObject0": "chasEntTempCurrent",
            "mibObject1": "chasEntTempThreshold",
            "mibObject2": "chasEntTempDangerThreshold",
            "mibObject3": "chasEntTempStatus",
            "function": "chassisSlotWithType_entPhysicalIndex",
            "object": "index",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)
    
    def software(self, limit: int = 200) -> ApiResult:
        """
        Fetch control module, loaded microcode, and virtual chassis hardware information.

        Args:
            limit (int): Maximum number of rows to retrieve.

        Returns:
            ApiResult: Parsed data including control status and versioning.
        """
        params = {
            "domain": "mib",
            "urn": "chasControlModuleTable|systemMicrocodeLoadedTable|systemVcHardwareTable",

            # chasControlModuleTable MIB objects
            "chasControlModuleTable-mibObject0": "entPhysicalIndex",
            "chasControlModuleTable-mibObject1": "chasPrimaryPhysicalIndex",
            "chasControlModuleTable-mibObject2": "chasControlCurrentRunningVersion",
            "chasControlModuleTable-mibObject3": "chasEntPhysAdminStatus",
            "chasControlModuleTable-mibObject4": "chasEntPhysOperStatus",
            "chasControlModuleTable-mibObject5": "chasControlDelayedRebootTimer",
            "chasControlModuleTable-mibObject6": "chasEntPhysPower",
            "chasControlModuleTable-mibObject7": "chasNumberOfResets",

            # systemMicrocodeLoadedTable MIB objects
            "systemMicrocodeLoadedTable-mibObject0": "systemMicrocodeLoadedDirectory",
            "systemMicrocodeLoadedTable-mibObject1": "systemMicrocodeLoadedVersion",

            # systemVcHardwareTable MIB objects
            "systemVcHardwareTable-mibObject0": "virtualChassisOperChasId",
            "systemVcHardwareTable-mibObject1": "systemVcHardwareFpga1Version",
            "systemVcHardwareTable-mibObject2": "systemVcHardwareUbootVersion",

            # Shared query controls
            "function": "entPhysIndexModuleType|chassis_entPhysIndex|entPhysicalIndex_chassisId|chassisSlotWithType_entPhysicalIndex",
            "object": "index|index|chassis_entPhysIndex_1|index",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)
    
    def cmmHardwareInfo(self, limit: int = 200) -> ApiResult:
        """
        Retrieve details about the active CMM module(s), including model, part number, and status.

        Args:
            limit (int): Maximum number of results to return.

        Returns:
            ApiResult: Parsed hardware and operational info of CMM modules.
        """
        params = {
            "domain": "mib",
            "urn": "entPhysicalTable",
            "mibObject0": "entPhysicalIndex",
            "mibObject1": "chasEntPhysOperStatus",
            "mibObject2": "entPhysicalModelName",
            "mibObject3": "chasEntPhysPartNumber",
            "mibObject4": "entPhysicalDescr",
            "mibObject5": "entPhysicalHardwareRev",
            "mibObject6": "entPhysicalSerialNum",
            "mibObject7": "entPhysicalMfgName",
            "function": "entPhysIndexModuleType|chassisSlotWithType_entPhysicalIndex",
            "object": "index|index",
            "filterObject": "entPhysIndexModuleType_0",
            "filterOperation": "==",
            "filterValue": "CMM",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)    
    
    def slot(self, limit: int = 200) -> ApiResult:
        """
        Retrieve hardware and PoE firmware details for NI modules.

        Args:
            limit (int): Maximum number of entries to return.

        Returns:
            ApiResult: Parsed inventory and versioning data for NI modules.
        """
        params = {
            "domain": "mib",
            "urn": "entPhysicalTable|alaPethMainPseTable",

            # entPhysicalTable MIB objects
            "entPhysicalTable-mibObject0": "entPhysicalIndex",
            "entPhysicalTable-mibObject1": "entPhysicalClass",
            "entPhysicalTable-mibObject2": "chasEntPhysModuleType",
            "entPhysicalTable-mibObject3": "entPhysicalModelName",
            "entPhysicalTable-mibObject4": "chasEntPhysPartNumber",
            "entPhysicalTable-mibObject5": "chasEntPhysAdminStatus",
            "entPhysicalTable-mibObject6": "chasEntPhysOperStatus",
            "entPhysicalTable-mibObject7": "chasControlReloadStatus",
            "entPhysicalTable-mibObject8": "chasEntPhysPower",
            "entPhysicalTable-mibObject9": "entPhysicalDescr",
            "entPhysicalTable-mibObject10": "chasEntPhysUbootRev",
            "entPhysicalTable-mibObject11": "chasEntPhysDaughterFpga1Rev",
            "entPhysicalTable-mibObject12": "entPhysicalHardwareRev",
            "entPhysicalTable-mibObject13": "entPhysicalFirmwareRev",
            "entPhysicalTable-mibObject14": "chasEntPhysDaughterFpga2Rev",
            "entPhysicalTable-mibObject15": "entPhysicalSerialNum",
            "entPhysicalTable-mibObject16": "entPhysicalMfgName",
            "entPhysicalTable-mibObject17": "chasEntPhysMacAddress",

            # alaPethMainPseTable MIB objects
            "alaPethMainPseTable-mibObject0": "alaPethMainPsePoESoftwareVersion",
            "alaPethMainPseTable-mibObject1": "alaPethMainPsePoEHardwareVersion",

            # Query function and filters
            "function": "entPhysIndexModuleType|chassisSlot_entPhysicalIndex|chassisEntSlotArr_entPhysIndex|wvGetVCMode",
            "object": "index|entPhysicalIndex|entPhysicalIndex",
            "filterObject": "entPhysIndexModuleType_0",
            "filterOperation": "==",
            "filterValue": "NI",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)   
    
    def powerSupplies(self, limit: int = 200) -> ApiResult:
        """
        Retrieve details of power supplies including power type and operational status.

        Args:
            limit (int): Maximum number of records to return.

        Returns:
            ApiResult: Parsed response with power supply information.
        """
        params = {
            "domain": "mib",
            "urn": "entPhysicalTable",
            "mibObject0": "entPhysicalIndex",
            "mibObject1": "chasEntPhysPower",
            "mibObject2": "chasEntPhysPowerType",
            "mibObject3": "chasEntPhysOperStatus",
            "mibObject4": "chasEntPhysAirflow",
            "function": "entPhysIndexModuleType|chassisSlot_entPhysicalIndex",
            "object": "index|entPhysicalIndex",
            "filterObject": "entPhysIndexModuleType_0",
            "filterOperation": "==",
            "filterValue": "PS",  # Filter for Power Supply modules
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)   

    def poePower(self, limit: int = 200) -> ApiResult:
        """
        Retrieve PoE controller configurations and firmware status.

        Args:
            limit (int): Maximum number of records to return.

        Returns:
            ApiResult: Parsed response containing PoE controller information.
        """
        params = {
            "domain": "mib",
            "urn": "alaPethMainPseTable",
            "mibObject0": "pethMainPseGroupIndex",
            "mibObject1": "alaPethMainPseAdminStatus",
            "mibObject2": "alaPethMainPseMaxPower",
            "mibObject3": "alaPethMainPsePriorityDisconnect",
            "mibObject4": "alaPethMainPseClassDetection",
            "mibObject5": "pethMainPseUsageThreshold",
            "mibObject6": "alaPethMainPseFastPoE",
            "mibObject7": "alaPethMainPsePerpetualPoE",
            "mibObject8": "alaPethMainPseHighResistanceDetection",
            "mibObject9": "alaPethMainPseFirmwareUpgradeSWVersion",
            "mibObject10": "alaPethMainPseFirmwareUpgradeStatus",
            "mibObject11": "alaPethMainPseDelayTime",
            "function": "chassisSlot_vcSlotNum",
            "object": "pethMainPseGroupIndex",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)    

    def transceiversInfo(self, limit: int = 200) -> ApiResult:
        """
        Retrieve GBIC/transceiver module information.

        Args:
            limit (int): Maximum number of entries to return.

        Returns:
            ApiResult: Parsed response with GBIC module data.
        """
        params = {
            "domain": "mib",
            "urn": "entPhysicalTable",
            "mibObject0": "chasEntPhysNiNum",
            "mibObject1": "chasEntPhysGbicNum",
            "mibObject2": "entPhysicalMfgName",
            "mibObject3": "chasEntPhysPartNumber",
            "mibObject4": "entPhysicalHardwareRev",
            "mibObject5": "entPhysicalSerialNum",
            "mibObject6": "entPhysicalMfgDate",
            "mibObject7": "chasEntPhysWaveLen",
            "mibObject8": "chasEntPhysAdminStatus",
            "mibObject9": "chasEntPhysOperStatus",
            "function": "entPhysIndexModuleType|chassis_entPhysIndex|addChassisIfVcMode",
            "object": "index|index|chassis_entPhysIndex_1,chasEntPhysNiNum",
            "filterObject": "entPhysIndexModuleType_0",
            "filterOperation": "==",
            "filterValue": "GBIC",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)  

    def dmmConfig(self) -> ApiResult:
        """
        Get global DDM configuration and trap settings.

        Returns:
            ApiResult: Parsed DDM configuration response.
        """
        params = {
            "domain": "mib",
            "urn": "ddmConfiguration",
            "mibObject0": "ddmConfig",
            "mibObject1": "ddmTrapConfig"
        }

        return self._client.get("/", params=params)       
    
    def fanStatus(self, limit: int = 200) -> ApiResult:
        """
        Retrieve fan information such as status, speed, and airflow.

        Args:
            limit (int): Maximum number of entries to retrieve.

        Returns:
            ApiResult: Fan hardware data from the switch.
        """
        params = {
            "domain": "mib",
            "urn": "alaChasEntPhysFanTable",
            "mibObject0": "entPhysicalIndex",
            "mibObject1": "alaChasEntPhysFanLocalIndex",
            "mibObject2": "alaChasEntPhysFanStatus",
            "mibObject3": "alaChasEntPhysFanSpeed",
            "mibObject4": "alaChasEntPhysFanAirflow",
            "function": "chassisSlot_entPhysicalIndex",
            "object": "entPhysicalIndex",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)    
    
    def runningDirectory(self, limit: int = 200) -> ApiResult:
        """
        Retrieve control module details including versions, status, and synchronization.

        Args:
            limit (int): Maximum number of entries to return.

        Returns:
            ApiResult: Control module information from the switch.
        """
        params = {
            "domain": "mib",
            "urn": "chasControlModuleTable",
            "mibObject0": "entPhysicalIndex",
            "mibObject1": "chasEntPhysOperStatus",
            "mibObject2": "chasControlCurrentRunningVersion",
            "mibObject3": "chasControlNextRunningVersion",
            "mibObject4": "chasControlCertifyStatus",
            "mibObject5": "chasControlWorkingVersion",
            "mibObject6": "chasControlRedundancyTime",
            "mibObject7": "chasControlSynchronizationStatus",
            "mibObject8": "configChangeStatus",
            "function": "chassis_entPhysIndex|getSwitchSecondaryCMMPhysicalIndex|getVCRole|csIsChassisModeVcOrErrStr|chassisSlotWithType_entPhysicalIndex",
            "object": "index|chassis_entPhysIndex_0|chassis_entPhysIndex_0||entPhysicalIndex",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)   

    def getHashControl(self) -> ApiResult:
        """
        Retrieve hash configuration parameters including hash mode and non-unicast behavior.

        Returns:
            ApiResult: Parsed hash control settings from the switch.
        """
        params = {
            "domain": "mib",
            "urn": "alaCapManHashControlCommands",
            "mibObject0": "alaCapManHashMode",
            "mibObject1": "alaCapManUdpTcpPortMode",
            "mibObject2": "alaCapManNonUCHashControl",
            "mibObject3": "alaCapManNonUCTunnelProtocol",
            "mibObject4": "alaCapManNonUCSourcePort"
        }

        return self._client.get("/", params=params)  
    
    def getLEDStatus(self, filter_value: str = "CMM", limit: int = 200) -> ApiResult:
        """
        Retrieve the list of LED and status information for CMM modules.

        Args:
            filter_value (str): Filter to apply on entPhysIndexModuleType (e.g., "CMM").
            limit (int): Maximum number of entries to return.

        Returns:
            ApiResult: Parsed status data from the switch.
        """
        params = {
            "domain": "mib",
            "urn": "chasEntPhysicalTable",
            "chasEntPhysicalTable-mibObject0": "chasEntPhysLedStatusOk1",
            "chasEntPhysicalTable-mibObject1": "chasEntPhysLedStatusOk2",
            "chasEntPhysicalTable-mibObject2": "chasEntPhysLedStatusPrimaryCMM",
            "chasEntPhysicalTable-mibObject3": "chasEntPhysLedStatusSecondaryCMM",
            "chasEntPhysicalTable-mibObject4": "chasEntPhysLedStatusTemperature",
            "chasEntPhysicalTable-mibObject5": "chasEntPhysLedStatusFan",
            "chasEntPhysicalTable-mibObject6": "chasEntPhysLedStatusBackupPS",
            "chasEntPhysicalTable-mibObject7": "chasEntPhysLedStatusInternalPS",
            "chasEntPhysicalTable-mibObject8": "chasEntPhysLedStatusControl",
            "chasEntPhysicalTable-mibObject9": "chasEntPhysLedStatusFabric",
            "chasEntPhysicalTable-mibObject10": "chasEntPhysLedStatusPS",
            "chasEntPhysicalTable-mibObject11": "chasEntPhysOperStatus",
            "chasEntPhysicalTable-mibObject12": "chasEntPhysAdminStatus",
            "chasEntPhysicalTable-mibObject13": "entPhysicalIndex",
            "function": "entPhysIndexModuleType|chassisEntSlotArr_entPhysIndex",
            "object": "entPhysicalIndex|entPhysicalIndex",
            "filterObject": "entPhysIndexModuleType_0",
            "filterOperation": "==",
            "filterValue": filter_value,
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)       


    
