import logging
import time
import threading
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.high_level_commander import HighLevelCommander
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URIs of the Crazyflies
URIs = [
    uri_helper.uri_from_env(default='radio://0/100/2M/E7E7E7E7E7'),
    'radio://0/100/2M/E7E7E7E7E8',
    'radio://0/80/2M/E7E7E7E7E3',
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

def synchronized_takeoff_landing(sync_cfs):
    """
    Function to start the sequence for all drones simultaneously using threading.
    """
    threads = []

    # Create a thread for each drone
    for scf in sync_cfs:
        thread = threading.Thread(target=run_sequence, args=(scf.cf,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    try:
        # Initialize drivers for communication with the drones
        cflib.crtp.init_drivers()

        # Create a list to hold SyncCrazyfile objects for each drone
        sync_cfs = []

        for uri in URIs:
            try:
                cf = Crazyflie(rw_cache='./cache')
                scf = SyncCrazyfile(uri, cf=cf)
                scf.open_link()  # Open the communication link with the Crazyflie
                print(f'Connected to Crazyflie with URI: {uri}')
                sync_cfs.append(scf)
            except Exception as e:
                print(f"Failed to connect to {uri}: {str(e)}")

        # Ensure at least one drone is connected
        if not sync_cfs:
            raise RuntimeError("No Crazyflies connected. Exiting.")

        # Wait a moment to ensure everything is ready
        time.sleep(2)

        # Run the synchronized takeoff, hover, and landing sequence for all drones
        synchronized_takeoff_landing(sync_cfs)

        # Wait for a while before the program finishes to let the drones land properly
        time.sleep(5)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

    finally:
        # Disconnect all Crazyflies cleanly
        for scf in sync_cfs:
            scf.close_link()

