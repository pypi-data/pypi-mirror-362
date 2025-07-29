from aos8_api.helper import parse_output_json
from aos8_api.endpoints.base import BaseEndpoint
from aos8_api.models import ApiResult

class VlanPortAssociation(BaseEndpoint):
    """Endpoint for managing VLAN-port associations via the AOS CLI API."""

    def _get_port_index(self, port_id: str) -> str:
        """
        Retrieves MVRP port configuration using a MIB-based POST request.

        Args:
            limit (int): Maximum number of records to return (default: 200)

        Returns:
            ApiResult: Parsed MVRP port configuration data from the switch.
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
            "limit": str(200),
            "ignoreError": "true"
        }

        response = self._client.get("/", params=params)

        rows = response.data["rows"]
        for item in rows.values():
            # Decode escaped port ID (e.g., '1\/1\/22' becomes '1/1/22')
            slot_port = item.get("slotPort_ifindex_0", "").replace("\\/", "/")
            if slot_port == port_id:
                return item.get("alaMvrpPortConfigIfIndex")
        return None

    
    def list_by_vlan(self,vlan_id:str):
        """
        Retrieve all port associations for a given VLAN using a GET request.

        Args:
            vlan_id (int): VLAN ID to filter the VPA table.

        Returns:
            ApiResult: Parsed data from the VPA table for the specified VLAN.
        """
        params = {
            "domain": "mib",
            "urn": "vpaTable",
            "mibObject0": "vpaVlanNumber",
            "mibObject1": "vpaIfIndex",
            "mibObject2": "vpaState",
            "mibObject3": "vpaType",
            "function": "slotPort_ifindex",
            "object": "vpaIfIndex",
            "filterObject": "vpaVlanNumber",
            "filterOperation": "==",
            "filterValue": str(vlan_id),
            "ignoreError": "true"
        }

        response = self._client.get("/", params=params)
        return response        

    def create(self, port_id: str, vlan_id: str, mode: str = "untagged") -> ApiResult:
        """
        Add a port to a VLAN with the specified tagging mode via MIB POST API.

        Args:
            port_id (str): Port identifier (e.g., "1/1/22").
            vlan_id (str): VLAN ID to associate with the port.
            mode (str, optional): "untagged" or "tagged". Defaults to "untagged".

        Returns:
            ApiResult: Retrieve all port associations for a given VLAN using a GET request.
        """
        url = "/?domain=mib&urn=vpaTable"

        ifindex = self._get_port_index(port_id)
        if ifindex is None:
            return None  # Optionally raise an exception here

        # Determine vpaType: 1 = untagged, 2 = tagged
        vpa_type = 1 if mode.lower() == "untagged" else 2

        form_data = {
            "mibObject0": f"vpaVlanNumber:|{str(vlan_id)}",
            "mibObject1": f"vpaIfIndex:|{ifindex}",
            "mibObject2": f"vpaType:{str(vpa_type)}",
            "mibObject3": "vpaStatus:4"  # Create/activate entry
        }

        response = self._client.post(url, data=form_data)
        if response.success:
            response = self.list_by_vlan(vlan_id)
        return response

    def edit(self, port_id: str, vlan_id: str, mode: str = "untagged") -> ApiResult:
        """Modify a port's tagging mode in a VLAN.

        Args:
            port_id (str): Port identifier.
            vlan_id (str): VLAN ID.
            mode (str, optional): New tagging mode ("untagged" or "tagged"). Defaults to "untagged".

        Returns:
            ApiResult: Retrieve all port associations for a given VLAN using a GET request.
        """
        url = "/?domain=mib&urn=vpaTable"

        ifindex = self._get_port_index(port_id)
        if ifindex is None:
            return None  # Optionally raise an exception here

        # Determine vpaType: 1 = untagged, 2 = tagged
        vpa_type = 1 if mode.lower() == "untagged" else 2

        form_data = {
            "mibObject0": f"vpaVlanNumber:|{str(vlan_id)}",
            "mibObject1": f"vpaIfIndex:|{ifindex}",
            "mibObject2": f"vpaType:{str(vpa_type)}",
            "mibObject3": "vpaStatus:4"  # Create/activate entry
        }

        response = self._client.post(url, data=form_data)
        if response.success:
            response = self.list_by_vlan(vlan_id)
        return response

    def delete(self, port_id: str, vlan_id: int) -> ApiResult:
        """Remove a port from a VLAN.

        Args:
            port_id (str): Port identifier.
            vlan_id (str): VLAN ID to disassociate from the port.

        Returns:
            ApiResult: Retrieve all port associations for a given VLAN using a GET request.
        """
        url = "/?domain=mib&urn=vpaTable"

        ifindex = self._get_port_index(port_id)

        if ifindex:
            form_data = {
                "mibObject0": f"vpaVlanNumber:|{str(vlan_id)}",
                "mibObject1": f"vpaIfIndex:|{ifindex}",
                "mibObject2": "vpaStatus:6"
            }

            response = self._client.post(url, data=form_data)
            if response.success:
                response = self.list_by_vlan(vlan_id)
                return response
            return response
        return None
