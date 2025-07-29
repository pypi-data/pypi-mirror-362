from aos8_api.helper import parse_vlan_output_json
from typing import Optional
from aos8_api.endpoints.base import BaseEndpoint
from aos8_api.models import ApiResult

class VlanEndpoint(BaseEndpoint):
    """Endpoint for managing VLAN configuration via the AOS RESTFUL API."""


    def list(self, vlan_type: int = 5, limit: int = 200):
        """
        Retrieve the list of VLANs using the MIB-based REST API.

        Args:
            vlan_type (int): VLAN type filter (default 5 for Ethernet VLAN).
            limit (int): Maximum number of results to return.

        Returns:
            ApiResult: Parsed VLAN data from the switch.
        """
        params = {
            "domain": "mib",
            "urn": "vlanTable",
            "mibObject0": "vlanNumber",
            "mibObject1": "vlanDescription",
            "mibObject2": "vlanAdmStatus",
            "mibObject3": "vlanType",
            "mibObject4": "vlanOperStatus",
            "mibObject5": "vlanMtu",
            "mibObject6": "vlanRouterStatus",
            "mibObject7": "vlanSrcLearningStatus",
            "filterObject": "vlanType",
            "filterOperation": "==",
            "filterValue": str(vlan_type),
            "limit": str(limit),
            "ignoreError": "true"
        }

        response = self._client.get("/", params=params)
        return response

    def create(self, vlan_id: int, description: Optional[str] = None, mtu: int = 1500, AdmStatus = 1, vlanSrcLearningStatus = 1) -> ApiResult:
        """
        Create VLAN info using a POST request with specific MIB object filters.

        Returns:
            ApiResult: VLAN data from the switch.
        """
        url = "/?domain=mib&urn=vlanTable"
        form_data = {
            "mibObject0": f"vlanNumber:|{str(vlan_id)}",
            "mibObject1": f"vlanDescription:{description}",
            "mibObject2": f"vlanAdmStatus:{str(AdmStatus)}",
            "mibObject3": f"vlanMtu:{str(mtu)}",
            "mibObject4": f"vlanSrcLearningStatus:{str(vlanSrcLearningStatus)}",
            "mibObject5": "vlanStatus:4"
        }

        response = self._client.post(url, data=form_data)
        if response.success:
            return self.list()
        return response

    def edit(self, vlan_id: int, description: Optional[str] = None, mtu: int = 1500, AdmStatus = 1, vlanSrcLearningStatus = 1) -> ApiResult:
        """
        Edit VLAN info using a POST request with specific MIB object filters.

        Returns:
            ApiResult: VLAN data from the switch.
        """
        url = "/?domain=mib&urn=vlanTable"
        form_data = {
            "mibObject0": f"vlanNumber:|{str(vlan_id)}",
            "mibObject1": f"vlanDescription:{description}",
            "mibObject2": f"vlanAdmStatus:{str(AdmStatus)}",
            "mibObject3": f"vlanMtu:{str(mtu)}",
            "mibObject4": f"vlanSrcLearningStatus:{str(vlanSrcLearningStatus)}",
        }

        response = self._client.post(url, data=form_data)
        if response.success:
            return self.list()
        return response

    def delete(self, vlan_id: int) -> ApiResult:
        """
        Delete VLAN using a POST request with specific MIB object filters.

        Returns:
            ApiResult: VLAN data from the switch.
        """
        url = "/?domain=mib&urn=vlanTable"
        form_data = {
            "mibObject0": f"vlanNumber:|{str(vlan_id)}",
            "mibObject1": "vlanStatus:6"
        }

        response = self._client.post(url, data=form_data)
        if response.success:
            return self.list()
        return response
