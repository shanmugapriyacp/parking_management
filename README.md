# parking_management
parking_management

## Execution steps
The Project was built and executed in Pycharm IDE, For data storing I have used csv files which can be replaced by database for large infrastructure.
Please install the required Packages in requirements.txt in pycharm or any other platform of your choice.
The Main File is parking_manager.py which can be executed to park a vehicle or unpark a vehicle
## Few execution samples
C:\Users\shanmugapriya.palani\PycharmProjects\pythonProject\parking_management>python parking_manager.py
Select the venue
1.airport
2. mall
3.stadium
3
Press
1. Park
2. Unpark
1
Select Vehicle
1.motor_cycle
2.car_suv
3.bus_truck
3
Assigning slot for vehicle:  bus_truck
Parking slot is full or Vehicle Not allowed to park

C:\Users\shanmugapriya.palani\PycharmProjects\pythonProject\parking_management>python parking_manager.py
Select the venue
1.airport
2. mall
3.stadium
1
Press
1. Park
2. Unpark
1
Select Vehicle
1.motor_cycle
2.car_suv
3.bus_truck
2
Assigning slot for vehicle:  car_suv
Your Ticket is 5

C:\Users\shanmugapriya.palani\PycharmProjects\pythonProject\parking_management>python parking_manager.py
Select the venue
1.airport
2. mall
3.stadium
1
Press
1. Park
2. Unpark
2
Please Enter Your Ticket Number: 3

Releasing slot for ticket:  3

Your Fee amount is 0

C:\Users\shanmugapriya.palani\PycharmProjects\pythonProject\parking_management>python parking_manager.py
Select the venue
1.airport
2. mall
3.stadium
3
Press
1. Park
2. Unpark
2
Please Enter Your Ticket Number: 1

Releasing slot for ticket:  1

Your Fee amount is 30

C:\Users\shanmugapriya.palani\PycharmProjects\pythonProject\parking_management>python parking_manager.py
Select the venue
1.airport
2. mall
3.stadium
3
Press
1. Park
2. Unpark
2
Please Enter Your Ticket Number: 1

Releasing slot for ticket:  1

Ticket Closed


## Executing Test suite
Execute the test files in location parrking_management/tests to verify the unit tests
python -m pytest tests/
