import os
import time

import spacecan


class TestBasic:

    def setup_method(self):
        self.controller = spacecan.Controller.from_file(
            os.path.join(os.path.dirname(__file__), "config/controller.json")
        )
        self.controller.connect()
        self.controller.start()

        self.responder1 = spacecan.Responder.from_file(
            os.path.join(os.path.dirname(__file__), "config/responder1.json")
        )
        self.responder1.connect()
        self.responder1.start()

    def teardown_method(self):
        self.controller.stop()
        self.controller.disconnect()

    def test_switch_bus(self):
        assert self.controller.network.selected_bus == self.controller.network.bus_a
        assert self.responder1.network.selected_bus == self.responder1.network.bus_a
        self.controller.switch_bus()

        assert self.controller.network.selected_bus == self.controller.network.bus_b
        time.sleep(4)
        assert self.responder1.network.selected_bus == self.responder1.network.bus_b

    def test_send_scet(self):
        coarse_time = 0x11223344
        fine_time = 0xAABBCC
        has_received = False

        def callback(coarse_time_, fine_time_):
            nonlocal has_received
            has_received = True
            assert coarse_time_ == coarse_time
            assert fine_time_ == fine_time

        self.responder1.received_scet = callback
        self.controller.send_scet(coarse_time, fine_time)

        time.sleep(1)
        assert has_received

    def test_send_utc(self):
        day = 0x1122
        ms_of_day = 0xAABBCCDD
        sub_ms_of_day = 0xEEFF
        has_received = False

        def callback(day_, ms_of_day_, sub_ms_of_day_):
            nonlocal has_received
            has_received = True
            assert day_ == day
            assert ms_of_day_ == ms_of_day
            assert sub_ms_of_day_ == sub_ms_of_day

        self.responder1.received_utc = callback
        self.controller.send_utc(day, ms_of_day, sub_ms_of_day)

        time.sleep(1)
        assert has_received

    def test_send_telecommand(self):
        data = bytearray([1, 2, 3, 4, 5, 6, 7, 8])
        node_id = 1
        has_received = False

        def callback(data_):
            nonlocal has_received
            has_received = True
            assert data_ == data

        self.responder1.received_telecommand = callback
        self.controller.send_telecommand(data, node_id)

        time.sleep(1)
        assert has_received
