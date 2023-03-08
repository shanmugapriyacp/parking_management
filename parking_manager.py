import math
import traceback
import validictory

from fee_manager import FeeComputationManager
from parking_config import MALL, STADIUM, AIRPORT, VEHICLE_TYPE_VALIDATION, TICKET_NUMBER_VALIDATION
from slot_manager import SlotManager


class ParkingManagement:
    def __init__(self):
        self._fee_model = FeeComputationManager(self.avenue)
        self._slot_manager = SlotManager(self.avenue)

    def _fetch_time_unit(self, parked_time):
        return 'hour'

    def _fetch_parked_time(self, parked_time):
        return parked_time

    def vehicle_entry(self, vehicle_type):
        try:
            validictory.validate(vehicle_type, VEHICLE_TYPE_VALIDATION)
            return self._slot_manager.assign_slot(vehicle_type)
        except Exception as e:
            print(traceback.format_exc())
            return str(e)

    def vehicle_exit(self, ticket_number):
        try:
            validictory.validate(ticket_number, TICKET_NUMBER_VALIDATION)
            vehicle_type, parked_time = self._slot_manager.release_slot(ticket_number)
            computation_data = {
                'time_unit': self._fetch_time_unit(parked_time),
                'parked_time': parked_time,
                'vehicle_type': vehicle_type,
            }
            return self._fee_model.calculate(computation_data)
        except Exception as e:
            print(traceback.format_exc())
            return str(e)


class AirportParking(ParkingManagement):
    def __init__(self):
        self.avenue = AIRPORT
        self.time_unit = 'hour'
        super(AirportParking, self).__init__()

    def _fetch_time_unit(self, parked_time):
        if parked_time > 24:
            return 'day'
        else:
            return 'hour'

    def _fetch_parked_time(self, parked_time):
        if parked_time > 24:
            return math.ceil(parked_time / 24)
        else:
            return parked_time


class StadiumParking(ParkingManagement):
    def __init__(self):
        self.avenue = STADIUM
        self.time_unit = 'hour'
        super(StadiumParking, self).__init__()


class MallParking(ParkingManagement):
    def __init__(self):
        self.avenue = MALL
        self.time_unit = 'hour'
        super(MallParking, self).__init__()


if __name__ == '__main__':
    ap = AirportParking()
    t1 = ap.vehicle_entry('car_suv')
    t2 = ap.vehicle_entry('bus_truck')
    t3 = ap.vehicle_entry('motor_cycle')
    t4 = ap.vehicle_entry('car_suv')

    print(t1, t2, t3, t4)
    import time

    time.sleep(65)
    print("fee for t4", ap.vehicle_exit(t1))
    print("fee for t2", ap.vehicle_exit(t2))
    print("fee for t3", ap.vehicle_exit(t3))
    print("fee for t1", ap.vehicle_exit(t4))
