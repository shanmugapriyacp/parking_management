import pytest
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

from slot_manager import SlotManager
from parking_config import MALL, STADIUM, AIRPORT, CAR_SUV, MOTOR_CYCLE, BUS_TRUCK

slot_assign_test_data = [
    ('', '', ['self.mock_read_csv_empty', 'self.mock_to_csv'], (Exception, "Value '' for field '<obj>' is not in the enumeration: ['airport', 'stadium', 'mall']")),
    ('', STADIUM, ['self.mock_read_csv_empty', 'self.mock_to_csv'], (Exception, "Value '' for field '<obj>' is not in the enumeration: ['motor_cycle', 'car_suv', 'bus_truck']")),

    (CAR_SUV, AIRPORT, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (MOTOR_CYCLE, AIRPORT, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (BUS_TRUCK, AIRPORT, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (MOTOR_CYCLE, MALL, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (BUS_TRUCK, MALL, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (CAR_SUV, MALL, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (CAR_SUV, STADIUM, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (MOTOR_CYCLE, STADIUM, ['self.mock_read_csv_empty', 'self.mock_to_csv'], 1),
    (BUS_TRUCK, STADIUM, ['self.mock_read_csv_empty', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),

    (CAR_SUV, AIRPORT, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (MOTOR_CYCLE, AIRPORT, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (BUS_TRUCK, AIRPORT, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (MOTOR_CYCLE, MALL, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (BUS_TRUCK, MALL, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (CAR_SUV, MALL, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (CAR_SUV, STADIUM, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (MOTOR_CYCLE, STADIUM, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),
    (BUS_TRUCK, STADIUM, ['self.mock_read_csv_full', 'self.mock_to_csv'], (Exception, "Parking slot is full or Vehicle Not allowed to park")),

    (CAR_SUV, AIRPORT, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (MOTOR_CYCLE, AIRPORT, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (BUS_TRUCK, AIRPORT, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (MOTOR_CYCLE, MALL, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (BUS_TRUCK, MALL, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (CAR_SUV, MALL, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (CAR_SUV, STADIUM, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (MOTOR_CYCLE, STADIUM, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],1),
    (BUS_TRUCK, STADIUM, ['self.mock_read_csv_partial', 'self.mock_to_csv_assert'],
     (Exception, "Parking slot is full or Vehicle Not allowed to park")),
]

slot_release_test_data = [
    ('', '', ['self.mock_read_csv_empty', 'self.mock_to_csv'],
     (Exception, "Value '' for field '<obj>' is not in the enumeration: ['airport', 'stadium', 'mall']")),
    ('', STADIUM, ['self.mock_read_csv_empty', 'self.mock_to_csv'],
     (Exception, "Value '' for field '<obj>' is not of type integer")),
    (.1, AIRPORT, ['self.mock_read_csv_empty', 'self.mock_to_csv'], (Exception, "Value 0.1 for field '<obj>' is not of type integer")),
    ('abc', AIRPORT, ['self.mock_read_csv_empty', 'self.mock_to_csv'], (Exception, "Value 'abc' for field '<obj>' is not of type integer")),
    (1, AIRPORT, ['self.mock_read_csv_full', 'self.mock_to_csv'], (CAR_SUV, 10)),
]

class TestSlotManager(object):
    def mock_read_csv_empty(self, file_name):
        data = {}
        if AIRPORT in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv', 2: 'bus_truck'}, 'slots': {0: 200, 1: 500, 2: 100}, 'occupied_slots': {0: 0, 1: 0, 2: 0}}
        elif STADIUM in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv'}, 'slots': {0: 1000, 1: 1500}, 'occupied_slots': {0: 0, 1: 0}}
        elif MALL in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv', 2: 'bus_truck'}, 'slots': {0: 100, 1: 80, 2: 10}, 'occupied_slots': {0: 0, 1: 0, 2: 0}}
        elif 'ticket' in file_name:
            data = {'ticket_number': {}, 'vehicle_type': {}, 'entry': {}, 'exit': {}}
        return pd.DataFrame.from_dict(data)

    def mock_read_csv_full(self, file_name):
        data = {}
        if AIRPORT in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv', 2: 'bus_truck'}, 'slots': {0: 200, 1: 500, 2: 100}, 'occupied_slots': {0: 200, 1: 500, 2: 100}}
        elif STADIUM in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv'}, 'slots': {0: 1000, 1: 1500}, 'occupied_slots': {0: 1000, 1: 1500}}
        elif MALL in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv', 2: 'bus_truck'}, 'slots': {0: 1000, 1: 1500, 2:10}, 'occupied_slots': {0: 1000, 1: 1500, 2:10}}
        elif 'ticket' in file_name:
            data = {'ticket_number': {0:1}, 'vehicle_type': {0:CAR_SUV}, 'entry': {0:(datetime.now()-timedelta(hours=10)).strftime("%d/%m/%Y, %H:%M:%S")}, 'exit': {0: np.nan}}
        return pd.DataFrame.from_dict(data)

    def mock_read_csv_partial(self, file_name):
        data = {}
        if AIRPORT in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv', 2: 'bus_truck'}, 'slots': {0: 200, 1: 500, 2: 100}, 'occupied_slots': {0: 199, 1: 499, 2: 99}}
        elif STADIUM in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv'}, 'slots': {0: 1000, 1: 1500}, 'occupied_slots': {0: 999, 1: 1499}}
        elif MALL in file_name and 'parking_slot' in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv', 2: 'bus_truck'}, 'slots': {0: 1000, 1: 1500, 2:10}, 'occupied_slots': {0: 999, 1: 1499, 2:9}}
        elif 'ticket' in file_name:
            data = {'ticket_number': {}, 'vehicle_type': {}, 'entry': {}, 'exit': {}}
        return pd.DataFrame.from_dict(data)

    def mock_to_csv(self, slot_file, index=False):
        return True


    def mock_to_csv_assert(self, slot_file, index=False):
        if 'ticket' in slot_file:
            assert datetime.strptime(slot_file['entry'], "%d/%m/%Y, %H:%M:%S").date() == date.today()
            assert slot_file['entry'].isNan()
        return True

    def mock_read_csv_err(self, file_name):
        raise Exception("File Not Found")

    @pytest.mark.parametrize('vehicle_type, venue, mock_list, expected_result', slot_assign_test_data)
    def test_assign_slot(self, monkeypatch, vehicle_type, venue, mock_list, expected_result):
        try:
            slot_mgr = SlotManager(venue)
            if mock_list:
                monkeypatch.setattr(pd, 'read_csv', eval(mock_list[0]))
                monkeypatch.setattr(slot_mgr.ticket_details, 'to_csv', eval(mock_list[1]))
                monkeypatch.setattr(slot_mgr.slot_details, 'to_csv', eval(mock_list[1]))
            slot_mgr = SlotManager(venue)
            assert slot_mgr.assign_slot(vehicle_type) == expected_result
        except Exception as e:
            print(e)
            assert str(e) == expected_result[1]

    @pytest.mark.parametrize('ticket_number, venue, mock_list, expected_result', slot_release_test_data)
    @pytest.mark.rel
    def test_release_slot(self, monkeypatch, ticket_number, venue, mock_list, expected_result):
        try:
            slot_mgr = SlotManager(venue)
            if mock_list:
                monkeypatch.setattr(pd, 'read_csv', eval(mock_list[0]))
                monkeypatch.setattr(slot_mgr.ticket_details, 'to_csv', eval(mock_list[1]))
                monkeypatch.setattr(slot_mgr.slot_details, 'to_csv', eval(mock_list[1]))
            slot_mgr = SlotManager(venue)
            assert slot_mgr.release_slot(ticket_number) == expected_result
        except Exception as e:
            print(e)
            assert str(e) == expected_result[1]
