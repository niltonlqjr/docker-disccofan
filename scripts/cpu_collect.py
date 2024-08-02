import psutil
import argparse
import getpass
import sys

from time import sleep

class DataProcess:
    def __init__(self, psutil_process: psutil.Process):
        self.ps: psutil.Process = psutil_process
        self.mem_usage: list[int] = []
        self.cpu_usage: list[float] = []

    def update_ps(self):
        try:
            self.ps.name()
        except:
            print(f"error: process {self.ps.name} does not exists")

    def insert_cpu_usage(self, verbose=False):
        usage = self.ps.cpu_percent()
        if verbose:
            print(f'inserting {usage} into usage list of {self.ps.name()}')
        self.cpu_usage.append(usage)
            
    
    def insert_mem_usage(self, verbose=False):
        mem_info = self.ps.memory_full_info()
        if verbose:
            print(f"updating memory with value {mem_info} of {self.ps.name()}")
        mem = {}
        mem['uss'] = mem_info.uss
        mem['rss'] = mem_info.rss
        mem['vms'] = mem_info.vms
        mem['data'] = mem_info.data
        self.mem_usage.append(mem)


    def save_cpu_usage(self, filename: str, verbose=False) -> bool:
        try:
            if verbose:
                print(f'saving cpu usage for process {self.ps.pid}')
            with open(f'{filename}-{self.ps.pid}.txt','a') as f:
                for u in self.cpu_usage:
                    f.write(str(u)+'\n')
            self.cpu_usage = []
            return True
        except:
            print(f'error saving cpu usage for pid: {self.ps.pid}',file=sys.stderr)
            return False
        
    def save_mem_usage(self, filename: str, verbose=False, header=False) -> bool:
        try:
            if verbose:
                print(f'saving memory usage for process {self.ps.pid}')
            
            with open(f'{filename}-{self.ps.pid}.txt','a') as f:
                if header:
                    f.write('uss\trss\tvms\tdata\n')
                for m in self.mem_usage:
                    f.write("{uss}\t{rss}\t{vms}\t{data}\n".format(
                        uss=m['uss'],rss=m['rss'],vms=m['vms'],data=m['data'])
                    )
            self.mem_usage = []
            return True
        except:
            print(f'error saving memory consumption for pid: {self.ps.pid}',file=sys.stderr)
            return False
    
    def __repr__(self):
        return "(pid={0}; name={1}; mem={2}; usage={3}".format(
            self.ps.pid, self.ps.name(), self.mem_usage, self.cpu_usage
        )

    def __str__(self):
        return self.__repr__()

#############       Main begins here      ##############

parser = argparse.ArgumentParser()

parser.add_argument('monitored_name', type=str, default='a.out',
                    help='Process that the program will monitor cpu and memory consumption')
parser.add_argument('-c', '--cpu-output-prefix', dest='out_file_cpu', type=str, default='cpu-out',
                    help='output filename prefix to store cpu usage (each pid will have a file for it)')
parser.add_argument('-m', '--memory-output-prexix', dest='out_file_mem', type=str, default='memory-out',
                    help='output filename prefix to store memory consumption (each pid will have a file for it)')
parser.add_argument('-b', '--buffer-size', dest='buffer_size', type=int, default=20,
                    help='total of stored cpu/memory measures before wirte in output file (0 = unlimeted)')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                    help='enable prints in stdout')
parser.add_argument('-i','--interval-time', dest='interval_time', type=float, default=0.3,
                    help='time between measures')

args=parser.parse_args()

monitored_name = args.monitored_name
out_file_cpu = args.out_file_cpu
out_file_mem = args.out_file_mem
buffer_size = args.buffer_size
verbose = args.verbose
interval_time = args.interval_time


if buffer_size <= 0:
    buffer_size = float('inf')

me = getpass.getuser()

if verbose:
    print(f'user:{me}')
    print(f'args:{args}')

# procs is a dict with pids as keys and DataProcess class 
# (declared here) as values
procs: dict[int, DataProcess] =  {}

# dict to store pid of running process
monitored_pids: dict[int, bool] = {}



#wait until process start
if verbose:
    print(f'waiting for a process with name {monitored_name} starts...')

while monitored_pids == {}:
    sleep(interval_time)
    for p in psutil.process_iter():
        try:
            if p.name() == monitored_name:
                monitored_pids[p.pid] = True
                procs[p.pid] = DataProcess(p)
        except:
            print(f'error in process {p.pid}', file=sys.stderr)
if verbose:
    print(f"Process {monitored_name} START!")

write_header = True

while monitored_pids != {}:
    sleep(interval_time)
    for p in psutil.process_iter():
        try:
            if p.username() == me and p.name() == monitored_name:
                if not(p.pid in procs):
                    procs[p.pid] = DataProcess(p)
                    monitored_pids[p.pid] = True
                procs[p.pid].insert_cpu_usage(verbose=verbose)
                procs[p.pid].insert_mem_usage(verbose=verbose)
                if len(procs[p.pid].cpu_usage) > buffer_size:
                    saved_mem = procs[p.pid].save_mem_usage(out_file_mem,
                                                verbose=verbose,
                                                header=write_header)
                    write_header = write_header and False
                    saved_cpu = procs[p.pid].save_cpu_usage(out_file_cpu,
                                                verbose=verbose)
        except:
            print(f'error in process {p.pid}', file=sys.stderr)
    
    pop_vals = []
    for p in monitored_pids:
        if not psutil.pid_exists(p):
            pop_vals.append(p)
    for p in pop_vals:
        monitored_pids.pop(p)

for p in procs:
    procs[p].save_cpu_usage(out_file_cpu,
                            verbose=verbose)
    procs[p].save_mem_usage(out_file_mem,
                            verbose=verbose)

