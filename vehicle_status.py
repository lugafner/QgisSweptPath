

from .qgis_swept_path_enum import VehicleStatusType, VehicleStatusAction

class VehicleStatus:
    def __init__(self,
                 vehicle_name: str,
                 status_action: VehicleStatusAction,
                 status_type: VehicleStatusType,
                 status_message_title: str,
                 status_message: str):

        self._vehicle_name = vehicle_name
        self._status_action = status_action
        self._status_type = status_type
        self._status_message_title = status_message_title
        self._status_message = status_message


    def __str__(self):
        return "Vehicle {} hast status: {}, {}".format(
            self._vehicle_name,
            self._status_message_title,
            self._status_message)


    @property
    def vehicle_name(self) -> str:
        """Name of the vehicle sendet the status"""
        return self._vehicle_name


    @property
    def status_action(self) -> VehicleStatusAction:
        """The status action enum"""
        return self._status_action


    @property
    def status_type(self) -> VehicleStatusType:
        """The status type enum"""
        return self._status_type


    @property
    def status_message_title(self) -> str:
        """The title of the status message"""
        return self._status_message_title


    @property
    def status_message(self) -> str:
        """The status message body"""
        return self._status_message
