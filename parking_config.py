import pandas as pd

# Vehicle Types
MOTOR_CYCLE = 'motor_cycle'
CAR_SUV = 'car_suv'
BUS_TRUCK = 'bus_truck'

# FEE TYPES
PER_UNIT = 'per_unit'
INTERVAL = 'interval'

# TIME UNIT
HOUR = 'hour'
DAY = 'day'

# FEE SUM TYPE
SUM_UP = 'sum_up'
FLAT = 'flat'

# PARKING VENUE
MALL = 'mall'
STADIUM = 'stadium'
AIRPORT = 'airport'

# CLOSE VALUE
LEFT = 'left'
RIGHT = 'right'
BOTH = 'both'

#FEE FILE MAPPING
FEE_FILE_MAP = {
    MALL: 'input/fee_model/mall_fee_model.csv',
    STADIUM: 'input/fee_model/stadium_fee_model.csv',
    AIRPORT: 'input/fee_model/airport_fee_model.csv',
}

SLOT_FILE_MAP = {
    MALL: 'input/slot_assignment/mall_parking_slots.csv',
    STADIUM: 'input/slot_assignment/stadium_parking_slots.csv',
    AIRPORT: 'input/slot_assignment/airport_parking_slots.csv',
}

TICKET_FILE_MAP = {
    MALL: 'input/ticket_assignment/mall_tickets.csv',
    STADIUM: 'input/ticket_assignment/stadium_tickets.csv',
    AIRPORT: 'input/ticket_assignment/airport_tickets.csv',
}

# PARKING DATA VALIDATIONS
PARKING_VENUE_VALIDATION = {"enum": [AIRPORT,STADIUM,MALL], "required": True}
VEHICLE_TYPE_VALIDATION = {"enum": [MOTOR_CYCLE, CAR_SUV, BUS_TRUCK], "required": True}
TICKET_NUMBER_VALIDATION = {"type": "integer", "required": True, "minimum": 1}
PARKING_DATA_SCHEMA = {"type": "object",
                       "properties": {
                            'parked_time': {"type": "number", "required": True, "minimum": 0.01},
                            'time_unit': {"enum": [HOUR, DAY], "required": True},
                            'vehicle_type': VEHICLE_TYPE_VALIDATION
                       }
}

# FEE_VAL = {
#     VEHICLE_TYPE:{
#         FEE_MODEL:[{
#             VALUE_TYPE : HOUR,
#             VALUES:pd.interval(0,4,closed='left'),
#             FEE:10
#             },
#             {
#                 VALUE_TYPE: HOUR,
#                 VALUES: pd.interval(4,12,closed='left'),
#                 FEE: 10
#             },
#             {
#                 VALUE_TYPE: HOUR,
#                 VALUES: pd.interval(12,),
#                 FEE: 10
#             }
#         ]
#     }
# }
#
# # MALL FEE
#
# MALL_FEE_VAL = {MOTOR_CYCLE: 10,
#                 CAR_SUV: 20,
#                 BUS_TRUCK: 50
#                 }
# MALL_FEE_TYPE = FLAT
#
# STADIUM_FEE = {
#
# }
