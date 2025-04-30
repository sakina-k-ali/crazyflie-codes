import logging
import time
import threading
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.high_level_commander import HighLevelCommander
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URIs of the Crazyflies
URIs = [
    uri_helper.uri_from_env(default='radio://0/100/2M/E7E7E7E7E6'),
    'radio://0/100/2M/E7E7E7E7E8',
]

# Setup logging level
logging.basicConfig(level=logging.ERROR)

def run_sequence(cf):
    """
    Function to take off, hover, and land for a single drone.
    """
    commander = cf.high_level_commander  # High-level commander for sending commands
    commander.takeoff(1.0, 5.0)  # Takeoff to 1m height in 5 seconds
    time.sleep(5)  # Hover for 5 seconds
    commander.land(0.0, 5.0)  # Land in 5 seconds

def synchronized_takeoff_landing(cf1, cf2):
    """
    Function to start the sequence for all drones simultaneously using threading.
    """
    thread_1 = threading.Thread(target=run_sequence, args=(cf1,))
    thread_2 = threading.Thread(target=run_sequence, args=(cf2,))

    # Start both threads at the same time
    thread_1.start()
    thread_2.start()

    # Wait for both threads to finish
    thread_1.join()
    thread_2.join()

if __name__ == '__main__':
    try:
        # Initialize drivers for communication with the drones
        cflib.crtp.init_drivers()

        # Create a list to hold SyncCrazyfile objects for each drone
        scfs = []

        for uri in URIs:
            cf = Crazyflie(rw_cache='./cache')
            scf = SyncCrazyflie(uri, cf=cf)
            scf.open_link()  # Open the communication link with the Crazyflie
            print(f'Connected to Crazyflie with URI: {uri}')
            scfs.append(scf)

        # Wait a moment to ensure everything is ready
        time.sleep(2)

        # Run the synchronized takeoff, hover, and landing sequence for all drones
        synchronized_takeoff_landing(scfs[0].cf, scfs[1].cf)

        # Wait for a while before the program finishes to let the drones land properly
        time.sleep(5)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

    finally:
        # Disconnect all Crazyflies cleanly
        for scf in scfs:
            scf.close_link()
