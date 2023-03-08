import pandas as pd
import numpy as np
from datetime import datetime
import math
import validictory

from parking_config import SLOT_FILE_MAP, TICKET_FILE_MAP, VEHICLE_TYPE_VALIDATION, PARKING_VENUE_VALIDATION, \
    TICKET_NUMBER_VALIDATION


class SlotManager:
    def __init__(self, parked_venue):
        validictory.validate(parked_venue, PARKING_VENUE_VALIDATION)
        self.slot_file = SLOT_FILE_MAP[parked_venue]
        self.ticket_file = TICKET_FILE_MAP[parked_venue]
        self.slot_details = pd.read_csv(self.slot_file)
        self.ticket_details = pd.read_csv(self.ticket_file)
        print(self.slot_details.to_dict())
        print(self.ticket_details.to_dict())

    def __is_slot_available(self, vehicle_type):
        try:
            slot = self.slot_details[(self.slot_details['vehicle_type'] == vehicle_type) & (
                        self.slot_details['slots'] != self.slot_details['occupied_slots'])]
            if slot.empty:
                raise Exception('Parking slot is full or Vehicle Not allowed to park')
            self.slot_details.loc[
                (self.slot_details['vehicle_type'] == vehicle_type) & (self.slot_details['slots'] != self.slot_details[
                    'occupied_slots']), 'occupied_slots'] = self.slot_details['occupied_slots'] + 1
            self.slot_details.to_csv(self.slot_file, index=False)
            return True
        except Exception:
            raise

    def __get_ticket(self, vehicle_type):
        max_ticket = self.ticket_details['ticket_number'].max(skipna=True)
        max_ticket = 0 if math.isnan(max_ticket) else max_ticket
        self.ticket_details.loc[len(self.ticket_details.index)] = [max_ticket + 1, vehicle_type,
                                                                   datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                                                                   np.nan]
        self.ticket_details.to_csv(self.ticket_file, index=False)
        return max_ticket + 1

    def assign_slot(self, vehicle_type):
        try:
            validictory.validate(vehicle_type, VEHICLE_TYPE_VALIDATION)
            if self.__is_slot_available(vehicle_type):
                return self.__get_ticket(vehicle_type)
        except Exception as e:
            raise

    def __validate_ticket(self, ticket):
        if ticket.empty:
            raise Exception("Invalid Ticket Number")
        if not ticket['exit'].isnull().values.any():
            raise Exception("Ticket Closed")

    def __update_slot_occupy(self, vehicle_type):
        # oc = self.slot_details.loc[self.slot_details['vehicle_type'] == vehicle_type]["occupied_slots"]
        self.slot_details.loc[self.slot_details['vehicle_type'] == vehicle_type, "occupied_slots"] -= 1
        self.slot_details.to_csv(self.slot_file, index=False)

    def release_slot(self, ticket_number):
        try:
            print("Releasing slot for ", ticket_number)
            validictory.validate(ticket_number, TICKET_NUMBER_VALIDATION)
            ticket = self.ticket_details[self.ticket_details['ticket_number'] == ticket_number]
            self.__validate_ticket(ticket)

            entry_time = datetime.strptime(ticket['entry'].values[0], "%d/%m/%Y, %H:%M:%S")
            exit_time = datetime.now()
            vehicle_type = ticket['vehicle_type'].values[0]
            parked_time = round((exit_time - entry_time).total_seconds() / 3600, 2)

            self.ticket_details.loc[self.ticket_details['ticket_number'] == ticket_number, 'exit'] = exit_time.strftime(
                "%d/%m/%Y, %H:%M:%S")
            self.ticket_details.to_csv(self.ticket_file, index=False)

            self.__update_slot_occupy(vehicle_type)
            return vehicle_type, parked_time
        except Exception as e:
            raise


if __name__ == '__main__':
    sm = SlotManager('stadium')
    # sm.assign_slot('motor_cycle')
    sm.release_slot(2)
    # sm.release_slot(3)
