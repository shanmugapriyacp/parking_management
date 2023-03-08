import pytest

from fee_manager import FeeComputationManager
from parking_config import MALL, STADIUM, AIRPORT, CAR_SUV, MOTOR_CYCLE, BUS_TRUCK
from parking_manager import AirportParking, MallParking, StadiumParking
from slot_manager import SlotManager

vehicle_entry_test_data = [
    ('', AIRPORT, ['self.mock_assign_slot', ],
     "Value '' for field '<obj>' is not in the enumeration: ['motor_cycle', 'car_suv', 'bus_truck']"),
    (CAR_SUV, AIRPORT, ['self.mock_assign_slot', ], 1),
    (MOTOR_CYCLE, AIRPORT, ['self.mock_assign_slot_exc', ], "Parking slot is full or Vehicle Not allowed to park"),

    ('', STADIUM, ['self.mock_assign_slot', ],
     "Value '' for field '<obj>' is not in the enumeration: ['motor_cycle', 'car_suv', 'bus_truck']"),
    (BUS_TRUCK, STADIUM, ['self.mock_assign_slot', ], 1),
    (CAR_SUV, STADIUM, ['self.mock_assign_slot_exc', ], "Parking slot is full or Vehicle Not allowed to park"),

    ('', MALL, ['self.mock_assign_slot', ],
     "Value '' for field '<obj>' is not in the enumeration: ['motor_cycle', 'car_suv', 'bus_truck']"),
    (MOTOR_CYCLE, MALL, ['self.mock_assign_slot', ], 1),
    (CAR_SUV, MALL, ['self.mock_assign_slot_exc', ], "Parking slot is full or Vehicle Not allowed to park"),
]

vehicle_exit_test_data = [
    ('', AIRPORT, ['self.mock_release_slot', 'self.mock_calculate'],
     "Value '' for field '<obj>' is not of type integer"),
    (1, AIRPORT, ['self.mock_release_slot', 'self.mock_calculate'], 100),
    (1, AIRPORT, ['self.mock_release_slot_exc', 'self.mock_calculate'], "Validation Error"),
    (1, AIRPORT, ['self.mock_release_slot', 'self.mock_calculate_exc'],
     "No fee detail availabe for the given time slot"),

    ('', STADIUM, ['self.mock_release_slot', 'self.mock_calculate'],
     "Value '' for field '<obj>' is not of type integer"),
    (1, STADIUM, ['self.mock_release_slot', 'self.mock_calculate'], 100),
    (2, STADIUM, ['self.mock_release_slot_exc', 'self.mock_calculate'], "Validation Error"),
    (1, STADIUM, ['self.mock_release_slot', 'self.mock_calculate_exc'],
     "No fee detail availabe for the given time slot"),

    ('', MALL, ['self.mock_release_slot', 'self.mock_calculate'],
     "Value '' for field '<obj>' is not of type integer"),
    (1, MALL, ['self.mock_release_slot', 'self.mock_calculate'], 100),
    (1, MALL, ['self.mock_release_slot_exc', 'self.mock_calculate'], "Validation Error"),
    (1, MALL, ['self.mock_release_slot', 'self.mock_calculate_exc'],
     "No fee detail availabe for the given time slot"),
]


class TestParkingManagement(object):
    def mock_assign_slot(self, vehicle_type):
        return 1

    def mock_assign_slot_exc(self, vehicle_type):
        raise Exception("Parking slot is full or Vehicle Not allowed to park")

    def mock_release_slot(self, ticket_number):
        return CAR_SUV, 10

    def mock_release_slot_exc(self, ticket_number):
        raise Exception("Validation Error")

    def mock_calculate(self, computation_data):
        return 100

    def mock_calculate_exc(self, computation_data):
        raise Exception("No fee detail availabe for the given time slot")

    @pytest.mark.parametrize('vehicle_type, venue, mock_list, expected_result', vehicle_entry_test_data)
    def test_vehicle_entry(self, monkeypatch, vehicle_type, venue, mock_list, expected_result):
        try:
            venue_class_map = {AIRPORT: AirportParking,
                               MALL: MallParking,
                               STADIUM: StadiumParking}
            parking_obj = venue_class_map[venue]
            if mock_list:
                monkeypatch.setattr(SlotManager, 'assign_slot', eval(mock_list[0]))
            assert parking_obj().vehicle_entry(vehicle_type) == expected_result
        except Exception as e:
            print(e)
            assert str(e) == expected_result[1]

    @pytest.mark.parametrize('ticket_number, venue, mock_list, expected_result', vehicle_exit_test_data)
    def test_vehicle_exit(self, monkeypatch, ticket_number, venue, mock_list, expected_result):
        try:
            venue_class_map = {AIRPORT: AirportParking,
                               MALL: MallParking,
                               STADIUM: StadiumParking}
            parking_obj = venue_class_map[venue]
            if mock_list:
                monkeypatch.setattr(SlotManager, 'release_slot', eval(mock_list[0]))
                monkeypatch.setattr(FeeComputationManager, 'calculate', eval(mock_list[1]))
            assert parking_obj().vehicle_exit(ticket_number) == expected_result
        except Exception as e:
            print(e)
            assert str(e) == expected_result[1]
