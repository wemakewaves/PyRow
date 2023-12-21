import pyrow
import time
from enum import Enum

class State(Enum):
    ERROR = 0
    READY = 1
    IDLE = 2
    HAVE_ID = 3
    NA = 4
    IN_USE = 5
    PAUSE = 6
    FINISHED = 7
    MANUAL = 8
    OFFLINE = 9

class Stroke(Enum):
    WAIT_MIN_SPEED = 0
    WAIT_ACCELERATION = 1
    DRIVE = 2
    DWELLING = 3
    RECOVERY = 4

class Workout(Enum):
    WAIT_BEGIN = 0
    WORKOUT_ROW = 1
    COUNTDOWN_PAUSE = 2
    INTERVAL_REST = 3
    WORK_TIME_INTERVAL = 4
    WORK_DISTANCE_INTERVAL = 5
    REST_END_TIME = 6
    REST_END_DISTANCE = 7
    TIME_END_REST = 8
    DISTANCE_END_REST = 9
    WORKOUT_END = 10
    WORKOUT_TERMINATE = 11
    WORKOUT_LOGGED = 12
    WORKOUT_REARM = 13

COMMAND = ['CSAFE_GETSTATUS_CMD', 'CSAFE_PM_GET_STROKESTATE', 'CSAFE_PM_GET_WORKOUTSTATE']

def main():
    # Connecting to erg
    ergs = list(pyrow.find())
    if not ergs:
        exit("No ergs found.")
    
    erg = pyrow.pyrow(ergs[0])
    print("Connected to erg.")

    # Prime status number
    c_state = -1
    c_stroke = -1
    c_workout = -1

    erg.set_workout(distance=2000, split=100, pace=120)

    # Inf loop
    while True:
        results = erg.send(COMMAND)

        if c_state != (results['CSAFE_GETSTATUS_CMD'][0] & 0xF):
            c_state = results['CSAFE_GETSTATUS_CMD'][0] & 0xF
            print(f"State {c_state}: {State(c_state).name}")

        if c_stroke != results['CSAFE_PM_GET_STROKESTATE'][0]:
            c_stroke = results['CSAFE_PM_GET_STROKESTATE'][0]
            print(f"Stroke {c_stroke}: {Stroke(c_stroke).name}")

        if c_workout != results['CSAFE_PM_GET_WORKOUTSTATE'][0]:
            c_workout = results['CSAFE_PM_GET_WORKOUTSTATE'][0]
            print(f"Workout {c_workout}: {Workout(c_workout).name}")

        time.sleep(1)

if __name__ == '__main__':
    main()
