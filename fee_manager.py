import math

import pandas as pd
import validictory

from parking_config import FEE_FILE_MAP, LEFT, RIGHT, BOTH, SUM_UP, FLAT, PER_UNIT, \
    PARKING_DATA_SCHEMA, PARKING_VENUE_VALIDATION, INTERVAL


class FeeComputationManager:
    def __init__(self, parked_venue):
        validictory.validate(parked_venue, PARKING_VENUE_VALIDATION)
        file = FEE_FILE_MAP[parked_venue]
        self.__fee_data = pd.read_csv(file)

    def __validate_input(self, parking_data):
        validictory.validate(parking_data, PARKING_DATA_SCHEMA)

    def calculate(self, parking_data):
        try:
            self.__validate_input(parking_data)
            vehicle_type = parking_data['vehicle_type']
            time_unit = parking_data['time_unit']
            parked_time = parking_data['parked_time']
            close_value = self.__fee_data.loc[0]['close_value']
            res = self.__fee_data[
                (self.__fee_data['vehicle_type'] == vehicle_type) & (self.__fee_data['time_unit'] == time_unit)]
            if res.empty:
                raise Exception("No fee detail available for the given Given Vehicle and time unit")
            result = None
            if close_value == LEFT:
                result = res[(res['start_value'] <= parked_time) & (res['end_value'] > parked_time)]
            elif close_value == RIGHT:
                result = res[(res['start_value'] < parked_time) & (res['end_value'] >= parked_time)]
            elif close_value == BOTH:
                result = res[(res['start_value'] <= parked_time) & (res['end_value'] >= parked_time)]
            if result.empty:
                raise Exception("No fee detail availabe for the given time slot")

            sumup_result = 0
            flat_result = 0

            if result['fee_sum_type'].values[0] == SUM_UP:
                records = res[(res['end_value'] <= parked_time) |
                              ((res['start_value'] <= parked_time) & (res['end_value'] >= parked_time))]
                for indx, rec in records.iterrows():
                    if rec['fee_type'] == PER_UNIT:
                        slot_val = min(parked_time, rec['end_value'])
                        mul_val = slot_val - rec['start_value']
                        if result['close_value'].values[0] == LEFT and result['start_value'].values[0] > 0:
                            mul_val = math.floor(mul_val)
                            mul_val += 1
                        else:
                            mul_val = math.ceil(mul_val)

                        sumup_result += rec['fee'] * mul_val
                    elif rec['fee_type'] == INTERVAL:
                        sumup_result += rec['fee']
            elif result['fee_sum_type'].values[0] == FLAT:
                if result['fee_type'].values[0] == PER_UNIT:
                    mul_val = math.floor(parked_time - result['start_value'])
                    if result['close_value'].values[0] == LEFT and result['start_value'].values[0] > 0:
                        mul_val += 1
                    flat_result += result['fee'].values[0] * mul_val
                elif result['fee_type'].values[0] == INTERVAL:
                    flat_result += result['fee'].values[0]
            final_result = sumup_result + flat_result
            return final_result and final_result or result['fee'].values[0]
        except Exception as e:
            print("Exception in FeeComputationManager.calculate ", e)
            raise


if __name__ == '__main__':
    parking_data = {
        'parked_time': 14.5,
        'vehicle_type': 'motor_cycle',
        'time_unit': 'hour'
    }
    print("The total fee is ", FeeComputationManager('stadium').calculate(parking_data))
