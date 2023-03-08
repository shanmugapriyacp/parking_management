import pandas as pd
import pytest

from fee_manager import FeeComputationManager
from parking_config import MALL, STADIUM, AIRPORT

parking_test_data = [
    ({}, '', [], ('Exception', "Value '' for field '<obj>' is not in the enumeration: ['airport', 'stadium', 'mall']")),
    ({}, AIRPORT, ['self.mock_read_csv_err', ], ('Exception', "File Not Found")),
    ({}, AIRPORT, ['self.mock_read_csv', ], ('Exception', "Required field '<obj>.parked_time' is missing")),
    ({'parked_time': 2, 'time_unit': 'day'}, AIRPORT, ['self.mock_read_csv', ],
     ('Exception', "Required field '<obj>.vehicle_type' is missing")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv'}, AIRPORT, ['self.mock_read_csv', ],
     ('Exception', "Required field '<obj>.time_unit' is missing")),
    ({'parked_time': 2, 'vehicle_type': 'taxi', 'time_unit': 'day'}, AIRPORT, ['self.mock_read_csv', ],
     ('Exception', "Value 'taxi' for field '<obj>.vehicle_type' is not in the enumeration: ['motor_cycle', 'car_suv', "
                   "'bus_truck']")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv', 'time_unit': 'sec'}, AIRPORT, ['self.mock_read_csv', ],
     ('Exception', "Value 'sec' for field '<obj>.time_unit' is not in the enumeration: ['hour', 'day']")),
    ({'parked_time': 2, 'vehicle_type': 'bus_truck', 'time_unit': 'day'}, AIRPORT, ['self.mock_read_csv', ],
     ('Exception', "No fee detail available for the given Given Vehicle and time unit")),
    ({'parked_time': 0.2, 'vehicle_type': 'car_suv', 'time_unit': 'day'}, AIRPORT, ['self.mock_read_csv', ],
     ('Exception', "No fee detail availabe for the given time slot")),
    ({'parked_time': -2, 'vehicle_type': 'car_suv', 'time_unit': 'day'}, AIRPORT, ['self.mock_read_csv', ],
     ('Exception', "Value -2 for field '<obj>.parked_time' is less than minimum value: 0.01")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv', 'time_unit': 'day'}, AIRPORT, ['self.mock_read_csv', ], 200),
    ({'parked_time': 2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, AIRPORT, ['self.mock_read_csv', ], 60),
    ({'parked_time': 2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, AIRPORT, ['self.mock_read_csv', ], 40),
    ({'parked_time': 8, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, AIRPORT, ['self.mock_read_csv', ], 60),
    ({'parked_time': 2, 'vehicle_type': 'motor_cycle', 'time_unit': 'day'}, AIRPORT, ['self.mock_read_csv', ], 160),
    ({'parked_time': 12, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, AIRPORT, ['self.mock_read_csv', ], 80),
    ({'parked_time': 14, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, AIRPORT, ['self.mock_read_csv', ], 80),
    ({'parked_time': 0.2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, AIRPORT, ['self.mock_read_csv', ], 0),
    ({'parked_time': 1.2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, AIRPORT, ['self.mock_read_csv', ], 40),

    ({}, AIRPORT, ['self.mock_read_csv_err', ], ('Exception', "File Not Found")),
    ({}, AIRPORT, ['self.mock_read_csv', ], ('Exception', "Required field '<obj>.parked_time' is missing")),
    ({'parked_time': 2, 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ],
     ('Exception', "Required field '<obj>.vehicle_type' is missing")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv'}, MALL, ['self.mock_read_csv', ],
     ('Exception', "Required field '<obj>.time_unit' is missing")),
    ({'parked_time': 2, 'vehicle_type': 'taxi', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ],
     ('Exception', "Value 'taxi' for field '<obj>.vehicle_type' is not in the enumeration: ['motor_cycle', 'car_suv', "
                   "'bus_truck']")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv', 'time_unit': 'sec'}, MALL, ['self.mock_read_csv', ],
     ('Exception', "Value 'sec' for field '<obj>.time_unit' is not in the enumeration: ['hour', 'day']")),
    ({'parked_time': 2, 'vehicle_type': 'bus_truck', 'time_unit': 'day'}, MALL, ['self.mock_read_csv', ],
     ('Exception', "No fee detail available for the given Given Vehicle and time unit")),
    ({'parked_time': -2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ],
     ('Exception', "Value -2 for field '<obj>.parked_time' is less than minimum value: 0.01")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 40),
    ({'parked_time': 2, 'vehicle_type': 'bus_truck', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 100),
    ({'parked_time': 2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 20),
    ({'parked_time': 0.2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 20),
    ({'parked_time': 0.2, 'vehicle_type': 'bus_truck', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 50),
    ({'parked_time': 0.2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 10),
    ({'parked_time': 3.2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 80),
    ({'parked_time': 3.2, 'vehicle_type': 'bus_truck', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 200),
    ({'parked_time': 3.2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, MALL, ['self.mock_read_csv', ], 40),

    ({}, STADIUM, ['self.mock_read_csv_err', ], ('Exception', "File Not Found")),
    ({}, STADIUM, ['self.mock_read_csv', ], ('Exception', "Required field '<obj>.parked_time' is missing")),
    ({'parked_time': 2, 'time_unit': 'day'}, STADIUM, ['self.mock_read_csv', ],
     ('Exception', "Required field '<obj>.vehicle_type' is missing")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv'}, STADIUM, ['self.mock_read_csv', ],
     ('Exception', "Required field '<obj>.time_unit' is missing")),
    ({'parked_time': 2, 'vehicle_type': 'taxi', 'time_unit': 'day'}, STADIUM, ['self.mock_read_csv', ],
     ('Exception', "Value 'taxi' for field '<obj>.vehicle_type' is not in the enumeration: ['motor_cycle', 'car_suv', "
                   "'bus_truck']")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv', 'time_unit': 'sec'}, STADIUM, ['self.mock_read_csv', ],
     ('Exception', "Value 'sec' for field '<obj>.time_unit' is not in the enumeration: ['hour', 'day']")),
    ({'parked_time': 2, 'vehicle_type': 'bus_truck', 'time_unit': 'day'}, STADIUM, ['self.mock_read_csv', ],
     ('Exception', "No fee detail available for the given Given Vehicle and time unit")),
    ({'parked_time': -2, 'vehicle_type': 'car_suv', 'time_unit': 'day'}, STADIUM, ['self.mock_read_csv', ],
     ('Exception', "Value -2 for field '<obj>.parked_time' is less than minimum value: 0.01")),
    ({'parked_time': 2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 60),
    ({'parked_time': 0.2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 60),
    ({'parked_time': 1.2, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 60),
    ({'parked_time': 4, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 180),
    ({'parked_time': 12, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 380),
    ({'parked_time': 12.6, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 380),
    ({'parked_time': 30, 'vehicle_type': 'car_suv', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 3980),
    ({'parked_time': 0.2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 30),
    ({'parked_time': 2, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 30),
    ({'parked_time': 8, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 90),
    ({'parked_time': 30, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 1990),
    ({'parked_time': 14.7, 'vehicle_type': 'motor_cycle', 'time_unit': 'hour'}, STADIUM, ['self.mock_read_csv', ], 390)

]


class TestFeeComputationManager(object):
    def mock_read_csv(self, file_name):
        data = {}
        if AIRPORT in file_name:
            data = {
                'vehicle_type': {0: 'motor_cycle', 1: 'motor_cycle', 2: 'motor_cycle', 3: 'motor_cycle', 4: 'car_suv',
                                 5: 'car_suv', 6: 'car_suv'},
                'time_unit': {0: 'hour', 1: 'hour', 2: 'hour', 3: 'day', 4: 'hour', 5: 'hour', 6: 'day'},
                'start_value': {0: 0, 1: 1, 2: 8, 3: 1, 4: 0, 5: 12, 6: 1},
                'end_value': {0: 1, 1: 8, 2: 24, 3: 999999, 4: 12, 5: 24, 6: 999999},
                'close_value': {0: 'left', 1: 'left', 2: 'left', 3: 'left', 4: 'left', 5: 'left', 6: 'left'},
                'fee_type': {0: 'interval', 1: 'interval', 2: 'per_unit', 3: 'per_unit', 4: 'interval', 5: 'interval',
                             6: 'per_unit'}, 'fee': {0: 0, 1: 40, 2: 60, 3: 80, 4: 60, 5: 80, 6: 100},
                'fee_sum_type': {0: 'flat', 1: 'flat', 2: 'flat', 3: 'flat', 4: 'flat', 5: 'flat', 6: 'flat'}}
        elif STADIUM in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'motor_cycle', 2: 'motor_cycle', 3: 'car_suv', 4: 'car_suv',
                                     5: 'car_suv'},
                    'time_unit': {0: 'hour', 1: 'hour', 2: 'hour', 3: 'hour', 4: 'hour', 5: 'hour'},
                    'start_value': {0: 0, 1: 4, 2: 12, 3: 0, 4: 4, 5: 12},
                    'end_value': {0: 4, 1: 12, 2: 999999, 3: 4, 4: 12, 5: 999999},
                    'close_value': {0: 'left', 1: 'left', 2: 'left', 3: 'left', 4: 'left', 5: 'left'},
                    'fee_type': {0: 'interval', 1: 'interval', 2: 'per_unit', 3: 'interval', 4: 'interval',
                                 5: 'per_unit'}, 'fee': {0: 30, 1: 60, 2: 100, 3: 60, 4: 120, 5: 200},
                    'fee_sum_type': {0: 'sum_up', 1: 'sum_up', 2: 'sum_up', 3: 'sum_up', 4: 'sum_up', 5: 'sum_up'}}
        elif MALL in file_name:
            data = {'vehicle_type': {0: 'motor_cycle', 1: 'car_suv', 2: 'bus_truck'},
                    'time_unit': {0: 'hour', 1: 'hour', 2: 'hour'}, 'start_value': {0: 0, 1: 0, 2: 0},
                    'end_value': {0: 999999, 1: 999999, 2: 999999}, 'close_value': {0: 'left', 1: 'left', 2: 'left'},
                    'fee_type': {0: 'per_unit', 1: 'per_unit', 2: 'per_unit'}, 'fee': {0: 10, 1: 20, 2: 50},
                    'fee_sum_type': {0: 'sum_up', 1: 'sum_up', 2: 'sum_up'}}
        return pd.DataFrame.from_dict(data)

    def mock_read_csv_err(self, file_name):
        raise Exception("File Not Found")

    @pytest.mark.parametrize('parking_data, venue, mock_list, expected_result', parking_test_data)
    def test_calculate(self, monkeypatch, parking_data, venue, mock_list, expected_result):
        try:
            if mock_list:
                monkeypatch.setattr(pd, 'read_csv', eval(mock_list[0]))
            assert FeeComputationManager(venue).calculate(parking_data) == expected_result
        except Exception as e:
            print(e)
            assert str(e) == expected_result[1]
