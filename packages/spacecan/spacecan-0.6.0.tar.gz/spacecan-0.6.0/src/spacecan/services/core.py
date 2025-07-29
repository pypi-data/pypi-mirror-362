import threading
import json

from ..controller import Controller
from .service_packet import ServicePacket

from .request import (
    RequestVerificationServiceController,
    RequestVerificationServiceResponder,
)
from .housekeeping import (
    HousekeepingServiceController,
    HousekeepingServiceResponder,
)
from .function import (
    FunctionManagementServiceController,
    FunctionManagementServiceResponder,
)
from .test import TestServiceController, TestServiceResponder
from .parameter import (
    ParameterManagementServiceController,
    ParameterManagementServiceResponder,
)


class Services:
    def __new__(cls, parent):
        if isinstance(parent, Controller):
            return ServiceController(parent)
        else:
            return ServiceResponder(parent)


class ServiceProtocol:
    def __init__(self):
        self.packet_monitor = None
        self.request = None
        self.housekeeping = None
        self.function = None
        self.test = None
        self.function = None
        self.parameter = None

    def received_packet(self, packet, node_id=None):
        service_packet = ServicePacket.from_packet(packet)
        service = service_packet.service
        subtype = service_packet.subtype
        data = service_packet.data

        if self.packet_monitor is not None:
            self.packet_monitor(service_packet, node_id)

        # dispatch packet to the individual service handlers
        # run them in threads to not block the main loop

        # request verification service
        if service == 1:
            t = threading.Thread(
                target=self.request.process,
                args=(service, subtype, data, node_id),
            )
            t.start()

        # # housekeeping service
        elif service == 3:
            t = threading.Thread(
                target=self.housekeeping.process,
                args=(service, subtype, data, node_id),
            )
            t.start()

        # function management service
        elif service == 8:
            t = threading.Thread(
                target=self.function.process, args=(service, subtype, data, node_id)
            )
            t.start()

        # test service
        elif service == 17:
            t = threading.Thread(
                target=self.test.process, args=(service, subtype, data, node_id)
            )
            t.start()

        # parameter management service
        elif service == 20:
            t = threading.Thread(
                target=self.parameter.process,
                args=(service, subtype, data, node_id),
            )
            t.start()


class ServiceController(ServiceProtocol):
    def __init__(self, parent):
        self.parent = parent
        self.parent.received_packet = self.received_packet

        self.request = RequestVerificationServiceController(self)
        self.housekeeping = HousekeepingServiceController(self)
        self.function = FunctionManagementServiceController(self)
        self.test = TestServiceController(self)
        self.parameter = ParameterManagementServiceController(self)

        self.packet_monitor = None

    def send(self, service_packet, node_id):
        # convert to regular packet (prepend data field with type and subtype)
        packet = service_packet.to_packet()
        self.parent.send_packet(packet, node_id)

    def from_file(self, filepath, node_id=None):
        if node_id is None:
            with open(filepath, "r", encoding="utf-8") as f:
                x = json.load(f)
            node_id = x.get("node_id")
            if node_id is None:
                raise ValueError("node_id must be defined")

        self.parameter.add_parameters_from_file(filepath, node_id)
        self.housekeeping.add_housekeeping_reports_from_file(filepath, node_id)
        self.function.add_functions_from_file(filepath, node_id)
        return self


class ServiceResponder(ServiceProtocol):
    def __init__(self, parent):
        self.parent = parent
        self.parent.received_packet = self.received_packet

        self.request = RequestVerificationServiceResponder(self)
        self.housekeeping = HousekeepingServiceResponder(self)
        self.function = FunctionManagementServiceResponder(self)
        self.test = TestServiceResponder(self)
        self.parameter = ParameterManagementServiceResponder(self)

        self.packet_monitor = None

    def send(self, service_packet):
        # convert to regular packet (prepend data field with type and subtype)
        packet = service_packet.to_packet()
        self.parent.send_packet(packet)

    def from_file(self, file):
        self.parameter.add_parameters_from_file(file)
        self.housekeeping.add_housekeeping_reports_from_file(file)
        self.function.add_functions_from_file(file)
        return self
