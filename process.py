#!/usr/bin/env python

import os
import time
import subprocess 

UPDATE_TIMER = 10

class Process():
    
    def __init__(self, pid, ppid, elapsed, started, user, command):
        self.pid = pid
        self.ppid = ppid
        self.started = started
        self.user = user
        self.command = command
        self.elapsed = elapsed

    def __repr__(self):
        return str(self.pid) + " " + str(self.command) + " started at " + str(self.started) + " by " + str(self.user) + " from " + str(self.ppid) 
    
    @staticmethod
    def all():
        tpid = os.getpid()
        ps = subprocess.Popen(['ps', 'wwax', '-o', 'pid,ppid,user,start,etime,command'], shell=False, stdout=subprocess.PIPE)
        ps_list = []
        lines = [ l for l in ps.stdout ]
        headers = lines[0].split()
        (user_ind, pid_ind, ppid_ind, started_ind, cmd_ind, elapsed_ind) = (headers.index("USER"), headers.index("PID"), 
                    headers.index("PPID"), headers.index("STARTED"), headers.index("COMMAND"), headers.index("ELAPSED"))
        for l in lines[1:]:
            fields = l.split()
            p = Process(int(fields[pid_ind]), int(fields[ppid_ind]), fields[elapsed_ind], fields[started_ind], fields[user_ind], " ".join([f for f in fields[cmd_ind:] if not f.startswith("-psn_")]))
            if p.pid != tpid and p.pid != ps.pid:
                ps_list.append(p)
        return ps_list
    
    @staticmethod
    def latest():
        ps_all = Process.all()
        latests = []
        for p in ps_all:
            try:
                if time.strptime(p.elapsed, "%M:%S").tm_min < UPDATE_TIMER:
                    latests.append(p)
            except ValueError:
                pass
        return latests


if __name__ == "__main__" :
    print "All:"
    ps_list = Process.all()
    for p in ps_list:
        print p
    print "Running:"
    ps_latest_list = Process.latest()
    for p in ps_latest_list:
        print p
