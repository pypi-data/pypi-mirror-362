import time
from multiprocessing import Process

class ProcessWrapper:
    def __init__(self, target_func, name, *args):
        self.target_func = target_func
        self.args = args
        self.name = name

    def create_process(self):
        return Process(target=self.run, name=self.name)

    def run(self):
        self.target_func(*self.args)


def monitor_processes(LOG, process_wrapper_list, process_list, monitor_time_interval=10):
    """
    Monitor and restart processes if they are not alive.

    Parameters:
    - LOG: process monitor log
    - process_list: List of ProcessWrapper objects to monitor.
    - stop_event: Event object to signal when to stop monitoring.
    """
    while True:
        index = 0
        for p in process_list:
            if not p.is_alive():
                LOG.error('Process:{} with args:{} is not alive. Restarting...'.format(process_wrapper_list[index].name, process_wrapper_list[index].args))
                # Restart the process with the same target function and arguments
                new_process = process_wrapper_list[index].create_process()
                new_process.start()
                LOG.info('Started new process {} with PID {}'.format(process_wrapper_list[index].name, new_process.pid))
                # Replace the terminated process with the new process
                process_list[index] = new_process
            index = index + 1
        time.sleep(monitor_time_interval)
