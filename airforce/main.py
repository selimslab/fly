from airforce.monitor import monitor
from airforce.repl import repl

def start_tracking():
    repl(monitor)

if __name__ == "__main__":
    start_tracking()
