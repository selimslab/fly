import threading

from .api import api_client
from .monitor import SpireApiMonitor

import time 
try:
    import readline    
except:
    pass #readline not available


def start_api_monitor(monitor:SpireApiMonitor):
    # start the api monitor in a separate thread 
    t1 = threading.Thread(target=monitor.process_target_updates)
    t1.start()
    

def repl(monitor:SpireApiMonitor):
    start_api_monitor(monitor)
    commands = {"plot": lambda: monitor.plot(), "stats": lambda: monitor.print_stats()}
    while True:
        try:
            command = input('airforce > ')
            if command in commands:
                commands[command]()
        except KeyboardInterrupt:
            print("bye!")
            return      

