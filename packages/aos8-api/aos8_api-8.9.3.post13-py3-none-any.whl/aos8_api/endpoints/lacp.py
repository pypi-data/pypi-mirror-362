from helper import parse_system_output_json
from typing import Optional
from endpoints.base import BaseEndpoint
from models import ApiResult

class LACPEndpoint(BaseEndpoint):
    """
    Endpoint to manage system-level configuration on an Alcatel-Lucent OmniSwitch using CLI-based API commands.
    """
    def getLACP(self, lacp_type: int = 0, limit: int = 200) -> ApiResult:
        """
        Retrieve link aggregation configurations filtered by LACP type.

        Args:
            lacp_type (int): 0 = Static, 1 = LACP. Default is 0 (static).
            limit (int): Max number of rows to retrieve. Default is 200.

        Returns:
            ApiResult: Contains LAG configurations.
        """
        params = {
            "domain": "mib",
            "urn": "alclnkaggAggTable",
            "mibObject0": "alclnkaggAggLacpType",
            "mibObject1": "alclnkaggAggIndex",
            "mibObject2": "alclnkaggAggMcLagType",
            "mibObject3": "alclnkaggAggSize",
            "mibObject4": "alclnkaggAggPortSelectionHash",
            "mibObject5": "alclnkaggAggAdminState",
            "mibObject6": "alclnkaggAggName",
            "mibObject7": "alclnkaggAggOperState",
            "mibObject8": "alclnkaggAggNbrSelectedPorts",
            "mibObject9": "alclnkaggAggNbrAttachedPorts",
            "mibObject10": "alclnkaggAggPrimaryPortIndex",
            "mibObject11": "alclnkaggAggDescr",
            "mibObject12": "alclnkaggAggWTRTimer",
            "function": "port_ifindex",
            "object": "alclnkaggAggIndex",
            "filterObject": "alclnkaggAggLacpType",
            "filterOperation": "==",
            "filterValue": str(lacp_type),
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)
    
    def lacpStats(self, limit: int = 200) -> ApiResult:
        """
        Retrieve per-port statistics for link aggregation.

        Args:
            limit (int): Maximum number of results to return.

        Returns:
            ApiResult: Contains statistics for LAG member ports.
        """
        params = {
            "domain": "mib",
            "urn": "alclnkaggAggPortTable",
            "mibObject0": "alclnkaggAggPortIndex",
            "mibObject1": "alclnkaggAggPortStatsLACPDUsRx",
            "mibObject2": "alclnkaggAggPortStatsMarkerPDUsRx",
            "mibObject3": "alclnkaggAggPortStatsMarkerResponsePDUsRx",
            "mibObject4": "alclnkaggAggPortStatsUnknownRx",
            "mibObject5": "alclnkaggAggPortStatsIllegalRx",
            "mibObject6": "alclnkaggAggPortStatsLACPDUsTx",
            "mibObject7": "alclnkaggAggPortStatsMarkerPDUsTx",
            "mibObject8": "alclnkaggAggPortStatsMarkerResponsePDUsTx",
            "function": "slotPort_ifindex",
            "object": "alclnkaggAggPortIndex",
            "limit": str(limit),
            "ignoreError": "true"
        }

        return self._client.get("/", params=params)    