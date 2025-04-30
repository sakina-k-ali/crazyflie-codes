import time
import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Slow takeoff function
def take_off(scf):
    commander = scf.cf.high_level_commander

    # Take off to 1.0 meter with 6 seconds duration (slow)
    commander.takeoff(1.0, 6.0)
    time.sleep(6)  # Wait for the duration of takeoff

# Slow landing function
def land(scf):
    commander = scf.cf.high_level_commander

    # Land with 6 seconds duration (slow descent)
    commander.land(0.0, 6.0)
    time.sleep(6)  # Wait for the duration of landing

    commander.stop()

# Function to perform a square flight sequence
def run_square_sequence(scf):
    box_size = 1.0  # Side length of the square (meters)
    flight_time = 6.0  # Time to travel each side (seconds) - slower speed

    commander = scf.cf.high_level_commander

    # Move in a square pattern slowly
    print("Starting square flight sequence...")
    commander.go_to(box_size, 0, 0, 0, flight_time, relative=True)
    time.sleep(flight_time)

    commander.go_to(0, box_size, 0, 0, flight_time, relative=True)
    time.sleep(flight_time)

    commander.go_to(-box_size, 0, 0, 0, flight_time, relative=True)
    time.sleep(flight_time)

    commander.go_to(0, -box_size, 0, 0, flight_time, relative=True)
    time.sleep(flight_time)

    print("Square flight sequence complete.")
    commander.stop()

# Main section
if __name__ == '__main__':
    # Initialize Crazyflie drivers
    cflib.crtp.init_drivers()

    # URI of the drone to control
    uri = 'radio://0/100/2M/E7E7E7E7E8'

    # Connect to Crazyflie and execute the sequence
    with SyncCrazyflie(uri) as scf:
        print('Connected to Crazyflie')

        # Perform slow takeoff
        take_off(scf)

        # Run the square flight sequence
        run_square_sequence(scf)

        # Perform slow landing
        land(scf)

        print("Mission complete.")
