from aos8_api.helper import parse_system_output_json
from typing import Optional
from aos8_api.endpoints.base import BaseEndpoint
from aos8_api.models import ApiResult

class SystemEndpoint(BaseEndpoint):
    """
    Endpoint to manage system-level configuration on an Alcatel-Lucent OmniSwitch using CLI-based API commands.
    """


    def keepAlive(self) -> ApiResult:
        """
        Retrieve current trap count from the switch.

        Returns:
            ApiResult: Parsed trap count data.
        """
        params = {
            "domain": "sqliteQuery",
            "urn": "trapCount"
        }

        return self._client.get("/", params=params)

    def getSystemInformation(self) -> ApiResult:
        """
        Retrieve system and system service configuration data.

        Returns:
            ApiResult: Parsed response from the switch.
        """
        params = {
            "domain": "mib",
            "urn": "system|systemServices|systemBlueToothServices|systemServicesBluetoothTable|systemFips|alaAaaAuthConfig",
            "mibObject0": "sysDescr",
            "mibObject1": "sysObjectID",
            "mibObject2": "sysUpTime",
            "mibObject3": "sysContact",
            "mibObject4": "sysName",
            "mibObject5": "sysLocation",
            "mibObject6": "systemServicesTimezone",
            "mibObject7": "systemServicesEnableDST",
            "mibObject8": "systemServicesTime",
            "mibObject9": "systemServicesDate",
            "mibObject10": "systemServicesUsbEnable",
            "mibObject11": "systemServicesUsbAutoCopyEnable",
            "mibObject12": "systemServicesUsbCopyConfig",
            "mibObject13": "systemServicesUsbBackupAdminState",
            "mibObject14": "systemServicesUsbBackupKey",
            "mibObject15": "systemServicesUsbBackupHashkey",
            "mibObject16": "systemServicesAction",
            "mibObject17": "systemServicesArg1",
            "mibObject18": "systemServicesBluetoothStatus",
            "mibObject19": "systemServicesBluetoothEnable",
            "mibObject20": "systemServicesBluetoothTxPower",
            "mibObject21": "systemServicesBluetoothStatus",  # Duplicated in original, left as-is
            "mibObject22": "systemServicesBluetoothChassisId",
            "mibObject23": "systemFipsAdminState",
            "mibObject24": "systemFipsOperState",
            "mibObject25": "alaAaaUbootAuthenticationPassword",
            "mibObject26": "alaAaaUbootAccess",
        }

        return self._client.get("/", params=params)
    

    def setSystem(self, contact: Optional[str] = None, name: Optional[str] = None, location: Optional[str] = None) -> ApiResult:
        """
        Update the system contact, name, and location information.

        Args:
            contact (str): System contact email or name.
            name (str): System name (hostname).
            location (str): System location description.

        Returns:
            ApiResult: Response from the API.
        """
        url = "/?domain=mib&urn=system"
        form_data = {}

        if contact is not None:
            form_data["mibObject0-T1"] = f"sysContact:{contact}"

        if name is not None:
            form_data["mibObject1-T1"] = f"sysName:{name}"

        if location is not None:
            form_data["mibObject2-T1"] = f"sysLocation:{location}"            

        return self._client.post(url, data=form_data)    


    def setDateTime(self, date: Optional[str] = None, time: Optional[str] = None, timezone: Optional[str] = None) -> ApiResult:
        """
        Update the system date, time, and timezone information.

        Args:
            date (str): System date.
            time (str): System time.
            timezone (str): System timezone description.

        Returns:
            ApiResult: Response from the API.
        """
        url = "/?domain=mib&urn=systemServices"
        form_data = {}

        if date is not None:
            form_data["mibObject0-T1"] = f"systemServicesDate:{date}"

        if time is not None:
            form_data["mibObject1-T1"] = f"systemServicesTime:{time}"

        if timezone is not None:
            form_data["mibObject2-T1"] = f"systemServicesTimezone:{timezone}"            

        return self._client.post(url, data=form_data)    

