from aos8_api.helper import parse_ip_interface_output
from typing import Optional
from aos8_api.endpoints.base import BaseEndpoint
from aos8_api.models import ApiResult

class IPInterfaceEndpoint(BaseEndpoint):
    """
    Endpoint to manage IP interfaces on an Alcatel-Lucent OmniSwitch using CLI-based API calls.
    """

    def _get_ip_ifindex(self, name: str) -> str:
        """
        Retrieves IP interface configuration using a MIB-based POST request.

        Args:
            limit (int): Maximum number of records to return (default: 200)

        Returns:
            IP Interface  - ifindex, or None if not found
        """
        response = self.list()
        rows = response.data["rows"]
        for item in rows.values():
            slot_port = item.get("alaIpInterfaceName", "")
            if slot_port == name:
                return item.get("ifIndex")
        return None

    def list(self, limit: int = 200) -> ApiResult:
        """
        Retrieve all IP interfaces using MIB-based GET with full object mapping.

        Args:
            limit (int): Maximum number of entries to retrieve. Defaults to 200.

        Returns:
            dict: Dictionary of IP interface entries, keyed by ifIndex.
        """
        params = {
            "domain": "mib",
            "urn": "alaIpInterfaceTable",
            "limit": str(limit),
            "ignoreError": "true",
            "function": "slotPort_ifindex|ifindex_slotPort|chassisSlot_vcIfIndex",
            "object": "alaIpInterfacePortIfindex|alaIpInterfaceArpNiSlot,0,alaIpInterfaceArpNiChassis|ifindex_slotPort_1"
        }

        # Add all 33 MIB objects
        mib_objects = [
            "ifIndex",
            "alaIpInterfaceName",
            "alaIpInterfaceAddress",
            "alaIpInterfaceMask",
            "alaIpInterfaceBcastAddr",
            "alaIpInterfaceDeviceType",
            "alaIpInterfaceTag",
            "alaIpInterfacePortIfindex",
            "alaIpInterfaceEncap",
            "alaIpInterfaceVlanID",
            "alaIpInterfaceIpForward",
            "alaIpInterfaceAdminState",
            "alaIpInterfaceOperState",
            "alaIpInterfaceOperReason",
            "alaIpInterfaceRouterMac",
            "alaIpInterfaceDhcpStatus",
            "alaIpInterfaceLocalProxyArp",
            "alaIpInterfaceDhcpOption60String",
            "alaIpInterfaceMtu",
            "alaIpInterfaceArpNiSlot",
            "alaIpInterfaceArpNiChassis",
            "alaIpInterfaceArpCount",
            "alaIpInterfacePrimCfg",
            "alaIpInterfacePrimAct",
            "alaIpInterfaceVipAddress",
            "alaIpInterfaceTunnelSrcAddressType",
            "alaIpInterfaceTunnelSrc",
            "alaIpInterfaceTunnelDstAddressType",
            "alaIpInterfaceTunnelDst",
            "alaIpInterfaceDhcpVsiAcceptFilterString",
            "alaIpInterfaceDhcpIpRelease",
            "alaIpInterfaceDhcpIpRenew",
            "alaIpInterfaceDhcpServerPreference"
        ]

        for i, obj in enumerate(mib_objects):
            params[f"mibObject{i}"] = obj

        response = self._client.get("/", params=params)
        return response

    def create_name_interface(self, name: str) -> ApiResult:
        """
        Create a new IP interface with the given name.

        Args:
            name (str): The logical name of the interface (e.g., 'int-999').

        Returns:
            ApiResult: The API response.
        """
        url = "/?domain=mib&urn=alaIpItfConfigTable"

        form_data = {
            "mibObject0-T1": f"alaIpItfConfigName:{name}",
            "mibObject1-T1": "alaIpItfConfigRowStatus:4"
        }

        response = self._client.post(url, data=form_data)
        if response.success:
            response = self.list()
            return response
        return response

    def create_IP_Interface(
        self,
        name: str,
        address: Optional[str] = None,
        mask: Optional[str] = None,
        device: str = "Vlan",
        vlan_id: Optional[int] = None,
        encap: Optional[str] = "e2",
    ) -> ApiResult:
        """
        Create a new IP interface with specified parameters.

        Args:
            ifindex (str): ifindex of the interface.
            address (Optional[str]): IP address.
            mask (Optional[str]): Subnet mask.
            vlan (Optional[int]): VLAN ID.
            service (Optional[int]): Associated service ID.
            encapsulation (Optional[str]): Encapsulation type ('e2' or 'snap').

        Returns:
            ApiResult: Result of the creation operation or error response.            
        """
        ifindex = None
        response = self.create_name_interface(name)
        if response.success:

            ifindex = self._get_ip_ifindex(name)
            url = "/?domain=mib&urn=alaIpInterfaceTable"

            encapsulation_map = {
                'e2': '1',
                'snap': '2'
            }
            encapsulation = encapsulation_map.get(encap, '1')

            device_type_map = {
                'Vlan': '1',
                'GRE': '4',
                'IPIP': '5',           
            }        
            device_type = device_type_map.get(device, '1')                 

            form_data = {
                "mibObject0": f"ifIndex:{ifindex}",
                "mibObject1": f"alaIpInterfaceAddress:{address}",
                "mibObject2": f"alaIpInterfaceMask:{mask}",            
                "mibObject3": f"alaIpInterfaceDeviceType:{device_type}",  
                "mibObject4": f"alaIpInterfaceEncap:{encapsulation}",            
                "mibObject5": f"alaIpInterfaceIpForward:1",                        
            }

            if vlan_id is not None:
                form_data["mibObject9"] = f"alaIpInterfaceVlanID:{str(vlan_id)}"

            if ifindex is not None:
                response = self._client.post(url, data=form_data)
                if response.success:
                    response = self.list()
                    return response
                return response
        return response

    def edit_IP_Interface(
        self,
        ifindex: str,
        address: Optional[str] = None,
        mask: Optional[str] = None,
        device: Optional[str] = None,
        vlan_id: Optional[int] = None,
        forward: Optional[bool] = None,
        local_proxy_arp: Optional[bool] = None,
        encapsulation: Optional[str] = None,
        primary: Optional[bool] = None
    ) -> ApiResult:
        """
        Create a new IP interface with specified parameters.

        Args:
            ifindex (str): ifindex of the interface.
            address (Optional[str]): IP address.
            mask (Optional[str]): Subnet mask.
            vlan (Optional[int]): VLAN ID.
            service (Optional[int]): Associated service ID.
            encapsulation (Optional[str]): Encapsulation type ('e2' or 'snap').
            primary (Optional[bool]): Set as primary interface.

        Returns:
            ApiResult: Result of the creation operation or error response.            
        """
        if ifindex:
            url = "/?domain=mib&urn=alaIpInterfaceTable"
       
            form_data = {
                "mibObject0": f"ifIndex:{ifindex}",
                "mibObject1": f"alaIpInterfacePortIfindex:0",
            }

            if address is not None:
                form_data["mibObject2"] = f"alaIpInterfaceAddress:{address}"

            if mask is not None:
                form_data["mibObject3"] = f"alaIpInterfaceMask:{mask}"   

            if device is not None:
                device_type_map = {
                    'Vlan': '1',
                    'GRE': '4',
                    'IPIP': '5',            
                }        
                device_type_config = device_type_map.get(device, '1')                   
                form_data["mibObject4"] = f"alaIpInterfaceDeviceType:{device_type_config}"   

            if encapsulation is not None:
                encapsulation_map = {
                    'e2': '1',
                    'snap': '2'
                }
                encapsulation_config = encapsulation_map.get(encapsulation, '1')
                form_data["mibObject5"] = f"alaIpInterfaceEncap:{encapsulation_config}"   


            if primary is not None:
                primary_config_map = {
                    False : '0',
                    True : '1',
                }        
                primary_config = primary_config_map.get(primary, '0')                     
                form_data["mibObject6"] = f"alaIpInterfacePrimCfg:{str(primary_config)}"                           
                            
            if vlan_id is not None:
                form_data["mibObject7"] = f"alaIpInterfaceVlanID:{str(vlan_id)}"

            if forward is not None:
                forward_config_map = {
                    False: '2',
                    True: '1'
                }        
                forward_config = forward_config_map.get(forward, '1')                     
                form_data["mibObject8"] = f"alaIpInterfaceIpForward:{forward_config}"   

            if local_proxy_arp is not None:
                local_proxy_arp_map = {
                    False: '2',
                    True: '1'
                }        
                local_proxy_arp_config = local_proxy_arp_map.get(local_proxy_arp, '1')                     
                form_data["mibObject9"] = f"alaIpInterfaceLocalProxyArp:{local_proxy_arp_config}"                                  

            response = self._client.post(url, data=form_data)
            if response.success:
                response = self.list()
                return response
            return response
        return None

   

    def delete(self, name: str) -> ApiResult:
        """
        Delete an existing IP interface.

        Args:
            name (str): The logical name of the interface (e.g., 'int-999').

        Returns:
            ApiResult: Result of the deletion operation or error response.
        """
        url = "/?domain=mib&urn=alaIpItfConfigTable"

        form_data = {
            "mibObject0-T1": f"alaIpItfConfigName:{name}",
            "mibObject1-T1": "alaIpItfConfigRowStatus:6"
        }

        response = self._client.post(url, data=form_data)
        if response.success:
            response = self.list()
            return response
        return response

