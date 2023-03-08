import sys
import math
import traceback
import validictory

from fee_manager import FeeComputationManager
from parking_config import MALL, STADIUM, AIRPORT, VEHICLE_TYPE_VALIDATION, MOTOR_CYCLE, CAR_SUV, BUS_TRUCK, TICKET_NUMBER_VALIDATION
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
            return "Your Ticket is " + str(self._slot_manager.assign_slot(vehicle_type))
        except Exception as e:
            # print(traceback.format_exc())
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
            return "Your Fee amount is " + str(self._fee_model.calculate(computation_data))
        except Exception as e:
            # print(traceback.format_exc())
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
    venue_class_map = {'1': AirportParking,
                       '2': MallParking,
                       '3': StadiumParking}
    parking_type_map = {'1': 'vehicle_entry',
                        '2': 'vehicle_exit'}
    vehicle_type_map = {'1': MOTOR_CYCLE,
                        '2': CAR_SUV,
                        '3': BUS_TRUCK
                        }
    venue = input("Select the venue \n1.%s \n2. %s \n3.%s \n" % (AIRPORT, MALL, STADIUM))
    parking_type = input("Press \n1. Park \n2. Unpark \n")
    if parking_type == '1':
        vehicle_type = input("Select Vehicle \n1.%s \n2.%s \n3.%s \n" % (MOTOR_CYCLE, CAR_SUV, BUS_TRUCK))
        argu = vehicle_type_map[vehicle_type]
    elif parking_type == '2':
        argu = input("Please Enter Your Ticket Number: ")
        argu = int(argu)

    print(getattr(venue_class_map[venue](), parking_type_map[parking_type])(argu))
