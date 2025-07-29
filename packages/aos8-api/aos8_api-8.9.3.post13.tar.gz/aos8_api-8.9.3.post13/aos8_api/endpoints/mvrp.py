from aos8_api.helper import parse_output_json
from aos8_api.endpoints.base import BaseEndpoint
from aos8_api.models import ApiResult

class MvrpEndpoint(BaseEndpoint):
    """Endpoint for managing MVRP configuration."""

    def globalMVRP(self) -> ApiResult:
        """
        Retrieve global MVRP configuration settings.

        Returns:
            ApiResult: MVRP global status and VLAN limit configuration.
        """
        params = {
            "domain": "mib",
            "urn": "alcatelIND1MVRPMIBObjects",
            "mibObject0": "alaMvrpGlobalStatus",
            "mibObject1": "alaMvrpMaxVlanLimit"
        }

        response = self._client.get("/", params=params)
        return response
    
    def mvrpPortConfig(self, limit: int = 200) -> ApiResult:
        """
        Retrieve MVRP port configuration table.

        Args:
            limit (int): Maximum number of rows to return (default is 200).

        Returns:
            ApiResult: The MVRP port configuration per interface.
        """
        params = {
            "domain": "mib",
            "urn": "alaMvrpPortConfigTable",
            "mibObject0": "alaMvrpPortConfigIfIndex",
            "mibObject1": "alaMvrpPortStatus",
            "mibObject2": "alaMvrpPortConfigRegistrarMode",
            "mibObject3": "alaMvrpPortConfigApplicantMode",
            "mibObject4": "alaMvrpPortConfigJoinTimer",
            "mibObject5": "alaMvrpPortConfigLeaveTimer",
            "mibObject6": "alaMvrpPortConfigLeaveAllTimer",
            "mibObject7": "alaMvrpPortConfigPeriodicTimer",
            "mibObject8": "alaMvrpPortConfigPeriodicTransmissionStatus",
            "function": "slotPort_ifindex",
            "object": "alaMvrpPortConfigIfIndex",
            "limit": str(limit),
            "ignoreError": "true"
        }

        response = self._client.get("/", params=params)
        return response   

    def mvrp_stats(self, port_status: int = 1, limit: int = 200) -> ApiResult:
        """
        Retrieve MVRP port statistics with an optional port status filter.

        Args:
            port_status (int): Filter for `alaMvrpPortStatus` (default is 1).
            limit (int): Max number of rows to retrieve (default is 200).

        Returns:
            ApiResult: Parsed MVRP port statistics.
        """
        params = {
            "domain": "mib",
            "urn": "alaMvrpPortStatsTable",
            "mibObject0": "alaMvrpPortStatsIfIndex",
            "mibObject1": "alaMvrpPortStatsNewReceived",
            "mibObject2": "alaMvrpPortStatsJoinInReceived",
            "mibObject3": "alaMvrpPortStatsJoinEmptyReceived",
            "mibObject4": "alaMvrpPortStatsLeaveReceived",
            "mibObject5": "alaMvrpPortStatsInReceived",
            "mibObject6": "alaMvrpPortStatsEmptyReceived",
            "mibObject7": "alaMvrpPortStatsLeaveAllReceived",
            "mibObject8": "alaMvrpPortStatsTotalPDUReceived",
            "mibObject9": "alaMvrpPortStatsTotalMsgsReceived",
            "mibObject10": "alaMvrpPortStatsInvalidMsgsReceived",
            "mibObject11": "alaMvrpPortFailedRegistrations",
            "mibObject12": "alaMvrpPortLastPduOrigin",
            "function": "slotPort_ifindex",
            "object": "alaMvrpPortStatsIfIndex",
            "filterObject": "alaMvrpPortStatus",
            "filterOperation": "==",
            "filterValue": str(port_status),
            "limit": str(limit),
            "ignoreError": "true"
        }

        response = self._client.get("/", params=params)
        return response     
    

    def mvrp_Vlan_Restriction(self, limit: int = 200) -> ApiResult:
        """
        Retrieve MVRP VLAN restriction configuration entries where restrictions are set.

        Args:
            limit (int): Maximum number of rows to retrieve (default 200).

        Returns:
            ApiResult: Parsed data with restricted VLANs.
        """
        params = {
            "domain": "mib",
            "urn": "alaMvrpPortRestrictVlanConfigTable",
            "mibObject0": "alaMvrpPortRestrictVlanIfIndex",
            "mibObject1": "alaMvrpPortRestrictVlanID",
            "mibObject2": "alaMvrpPortVlanRestrictions",
            "function": "slotPort_ifindex",
            "object": "alaMvrpPortRestrictVlanIfIndex",
            "filterObject": "alaMvrpPortVlanRestrictions",
            "filterOperation": "!=",
            "filterValue": "00",
            "limit": str(limit),
            "ignoreError": "true"
        }

        response = self._client.get("/", params=params)
        return response    