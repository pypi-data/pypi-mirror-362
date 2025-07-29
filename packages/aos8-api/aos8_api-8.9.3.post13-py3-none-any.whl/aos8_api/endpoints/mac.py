from aos8_api.helper import parse_output_json
from aos8_api.endpoints.base import BaseEndpoint
from aos8_api.models import ApiResult

class MacLearningEndpoint(BaseEndpoint):
    """Endpoint for managing MVRP configuration."""

    def globalMacLearning(self) -> ApiResult:
        """
        Retrieves the system MAC address aging value.

        Returns:
            ApiResult: Contains the `slMacAgingValue` if successful.
        """
        params = {
            "domain": "mib",
            "urn": "slMacAddressAgingTable",
            "mibObject0": "slMacAgingValue"
        }

        response = self._client.get("/", params=params)
        return response
    
    def macPortConfiguration(self, limit: int = 200) -> ApiResult:
        """
        Retrieve MAC learning control status per interface.

        Args:
            limit (int): Maximum number of results to return.

        Returns:
            ApiResult: Parsed response containing interface MAC learning control statuses.
        """
        params = {
            "domain": "mib",
            "urn": "slMacLearningControlTable",
            "mibObject0": "ifIndex",
            "mibObject1": "slMacLearningControlStatus",
            "function": "slotPort_ifindex",
            "object": "ifIndex",
            "limit": str(limit),
            "ignoreError": "true"
        }
        return self._client.get("/", params=params)    
    
    def showMacAddress(self, limit: int = 200) -> ApiResult:
        """
        Retrieve global MAC address records.

        Args:
            limit (int): Maximum number of results to return.

        Returns:
            ApiResult: Contains parsed global MAC address entries.
        """
        params = {
            "domain": "mib",
            "urn": "alaSlMacAddressGlobalTable",
            "mibObject0": "slMacDomain",
            "mibObject1": "slLocaleType",
            "mibObject2": "slOriginId",
            "mibObject3": "slServiceId",
            "mibObject4": "slSubId",
            "mibObject5": "slMacAddressGbl",
            "mibObject6": "slMacAddressGblManagement",
            "mibObject7": "slMacAddressGblDisposition",
            "mibObject8": "slMacAddressGblProtocol",
            "mibObject9": "slMacAddressGblGroupField",
            "mibObject10": "slSvcISID",
            "mibObject11": "slVxLanVnID",
            "mibObject12": "slL2GreVpnID",
            "function": "slotPort_ifindex",
            "object": "slOriginId",
            "limit": str(limit),
        }

        return self._client.get("/", params=params)