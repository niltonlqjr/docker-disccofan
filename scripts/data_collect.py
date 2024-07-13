import ctypes
import signal
import datetime
import threading
import psutil

# This is a Python 3 demo of how to interact with the Nethogs library via Python. The Nethogs
# library operates via a callback. The callback implemented here just formats the data it receives
# and prints it to stdout. This must be run as root (`sudo python3 python-wrapper.py`).
# By Philip Semanchuk (psemanchuk@caktusgroup.com) November 2016
# Copyright waived; released into public domain as is.

# The code is multi-threaded to allow it to respond to SIGTERM and SIGINT (Ctrl+C).  In single-
# threaded mode, while waiting in the Nethogs monitor loop, this Python code won't receive Ctrl+C
# until network activity occurs and the callback is executed. By using 2 threads, we can have the
# main thread listen for SIGINT while the secondary thread is blocked in the monitor loop.

#######################
# BEGIN CONFIGURATION #
#######################

# You can use this to monitor only certain devices, like:
# device_names = ['enp4s0', 'docker0']
device_names = []

# LIBRARY_NAME has to be exact, although it doesn't need to include the full path.
# The version tagged as 0.8.7-44-g0fe341e that is installed in this container.

LIBRARY_NAME = 'libnethogs.so.0.8.7-44-g0fe341e'

# EXPERIMENTAL: Optionally, specify a capture filter in pcap format (same as
# used by tcpdump(1)) or None. See `man pcap-filter` for full information.
# Note that this feature is EXPERIMENTAL (in libnethogs) and may be removed or
# changed in an incompatible way in a future release.
# example:
# FILTER = 'port 80 or port 8080 or port 443'
FILTER = None

#####################
# END CONFIGURATION #
#####################

# Here are some definitions from libnethogs.h
# https://github.com/raboof/nethogs/blob/master/src/libnethogs.h
# Possible actions are NETHOGS_APP_ACTION_SET & NETHOGS_APP_ACTION_REMOVE
# Action REMOVE is sent when nethogs decides a connection or a process has died. There are two
# timeouts defined, PROCESSTIMEOUT (150 seconds) and CONNTIMEOUT (50 seconds). AFAICT, the latter
# trumps the former so we see a REMOVE action after ~45-50 seconds of inactivity.
class Action():
    SET = 1
    REMOVE = 2

    MAP = {SET: 'SET', REMOVE: 'REMOVE'}

class LoopStatus():
    """Return codes from nethogsmonitor_loop()"""
    OK = 0
    FAILURE = 1
    NO_DEVICE = 2

    MAP = {OK: 'OK', FAILURE: 'FAILURE', NO_DEVICE: 'NO_DEVICE'}

# The sent/received KB/sec values are averaged over 5 seconds; see PERIOD in nethogs.h.
# https://github.com/raboof/nethogs/blob/master/src/nethogs.h#L43
# sent_bytes and recv_bytes are a running total
class NethogsMonitorRecord(ctypes.Structure):
    """ctypes version of the struct of the same name from libnethogs.h"""
    _fields_ = (('record_id', ctypes.c_int),
                ('name', ctypes.c_char_p),
                ('pid', ctypes.c_int),
                ('uid', ctypes.c_uint32),
                ('device_name', ctypes.c_char_p),
                ('sent_bytes', ctypes.c_uint64),
                ('recv_bytes', ctypes.c_uint64),
                ('sent_kbs', ctypes.c_float),
                ('recv_kbs', ctypes.c_float),
                )


def signal_handler(signal, frame):
    print('SIGINT received; requesting exit from monitor loop.')
    lib.nethogsmonitor_breakloop()


def dev_args(devnames):
    """
    Return the appropriate ctypes arguments for a device name list, to pass
    to libnethogs ``nethogsmonitor_loop_devices``. The return value is a
    2-tuple of devc (``ctypes.c_int``) and devicenames (``ctypes.POINTER``)
    to an array of ``ctypes.c_char``).

    :param devnames: list of device names to monitor
    :type devnames: list
    :return: 2-tuple of devc, devicenames ctypes arguments
    :rtype: tuple
    """
    devc = len(devnames)
    devnames_type = ctypes.c_char_p * devc
    devnames_arg = devnames_type()
    for idx, val in enumerate(devnames):
        devnames_arg[idx] = (val + chr(0)).encode('ascii')
    return ctypes.c_int(devc), ctypes.cast(
        devnames_arg, ctypes.POINTER(ctypes.c_char_p)
    )


def run_monitor_loop(lib, devnames):
    # Create a type for my callback func. The callback func returns void (None), and accepts as
    # params an int and a pointer to a NethogsMonitorRecord instance.
    # The params and return type of the callback function are mandated by nethogsmonitor_loop().
    # See libnethogs.h.
    CALLBACK_FUNC_TYPE = ctypes.CFUNCTYPE(
        ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(NethogsMonitorRecord)
    )

    filter_arg = FILTER
    if filter_arg is not None:
        filter_arg = ctypes.c_char_p(filter_arg.encode('ascii'))

    if len(devnames) < 1:
        # monitor all devices
        rc = lib.nethogsmonitor_loop(
            CALLBACK_FUNC_TYPE(network_activity_callback),
            filter_arg
        )
    else:
        devc, devicenames = dev_args(devnames)
        rc = lib.nethogsmonitor_loop_devices(
            CALLBACK_FUNC_TYPE(network_activity_callback),
            filter_arg,
            devc,
            devicenames,
            ctypes.c_bool(False)
        )

    if rc != LoopStatus.OK:
        print('nethogsmonitor_loop returned {}'.format(LoopStatus.MAP[rc]))
    else:
        print('exiting monitor loop')


def network_activity_callback(action, data):
    global procs
    #print(datetime.datetime.now().strftime('@%H:%M:%S.%f'))

    # Action type is either SET or REMOVE. I have never seen nethogs send an unknown action
    # type, and I don't expect it to do so.
    action_type = Action.MAP.get(action, 'Unknown')
    pid = data.contents.pid
    if pid in procs:
        procs[pid].data_sent = data.contents.sent_bytes
        procs[pid].data_recv = data.contents.recv_bytes
    
    '''print('Action: {}'.format(action_type))
    print('Record id: {}'.format(data.contents.record_id))
    print('Name: {}'.format(data.contents.name))
    print('PID: {}'.format(data.contents.pid))
    print('UID: {}'.format(data.contents.uid))
    print('Device name: {}'.format(data.contents.device_name.decode('ascii')))
    print('Sent/Recv bytes: {} / {}'.format(data.contents.sent_bytes, data.contents.recv_bytes))
    print('Sent/Recv kbs: {} / {}'.format(data.contents.sent_kbs, data.contents.recv_kbs))
    print('-' * 30)'''



class DataProcess:
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.mem = 0
        self.usage = []
        self.data_sent = 0
        self.data_recv = 0

    def __repr__(self):
        return "(pid={}; name={}; mem={}; usage={}; data_sent={}; data_recv={}".format(
            self.pid, self.name, self.mem, str(self.usage), self.data_sent, self.data_recv
        )
        

    def __str__(self):
        return self.__repr__()

    def save_usage(self, filename):
        try:
            with open(filename,'a') as f:
                for u in self.usage:
                    f.write(str(u)+'\n')
                self.usage = []
            return True
        except:
            return False
    
    def save_mem(self, filename):
        try:
            with open(filename,'a') as f:
                f.write(str(self.mem)+'\n')
            return True
        except:
            return False
    
    def save_network(self, filename, header=False):
        try:
            with open(filename,'a') as f:
                if header:
                    f.write('Sent \t Recv\n')
                f.write('{sent}\t{recv}\n'.format(sent=self.data_sent,
                                                  recv=self.data_recvr))
            return True
        except:
            return False
    
    def insert_usage(self, u):
        self.usage.append(u)
    
    def update_mem(self, mem):
        self.mem_usage = max(self.mem_usage, mem)

#############       Main begins here      ##############

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

lib = ctypes.CDLL(LIBRARY_NAME)

monitor_thread = threading.Thread(
    target=run_monitor_loop, args=(lib, device_names,)
)


procs = {}





interval_time = 0.3
monitored_process = 'ssh'


monitor_thread.start()
done = False

key=''

print('type q and enter to close.')
x = 1
while x <= 10:

    monitor_thread.join(interval_time)
    #print(i)
    psprocs = psutil.pids()
    print(psprocs)
    for pid in psprocs:
        p = psutil.Process(pid)
        try:
            if not (pid in procs):
                procs[pid] = DataProcess(pid, p.name())
            procs[pid].update_mem(p.memory_full_info().uss)
            procs[pid].insert_usage(p.cpu_percent())
        except:
            pass
            #print("impossible to get information about process:", pid)
    x+=1
            
lib.nethogsmonitor_breakloop()

for p in procs:
    print(procs[p])