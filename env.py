#!/usr/bin/env python

import re
import sys
import subprocess 

def _get_platform():
    if sys.platform == "win32":
        return "win"
    elif sys.platform == "darwin":
        return "mac"
    elif sys.platform == "linux2":
        return "linux"
    raise Exception("Unsupported platform")

def _get_nth(located_after, word_number, a_string):
    """
    Returns the nth alpha-numeric word following a string. 
    """
    regex = r"" + located_after + r"(?:\W+(\w+)){" + str(word_number) + "}"
    result = re.compile(regex).findall(a_string)
    return "".join(result)

def _normalize(s):
    if(s[-1] == "M"):
        return int(s[:-1]) * 1000
    if(s[-1] == "k"):
        return int(s[:-1])
    return (int(s) / 1000)

def get():
    env = {}
    
    if _get_platform() == "mac":
        top_cmd = subprocess.Popen(['top', '-l', '1'], shell=False, stdout=subprocess.PIPE)
        top_out, top_err= top_cmd.communicate()

        env["proc_load"] = _get_nth("Load Avg:", 4, top_out)
        env["mem_load"] = _normalize(_get_nth("PhysMem", 7, top_out))
        env["nb_process"] =  _get_nth("Processes", 1, top_out)
        env["nb_process_running"] =  _get_nth("Processes", 3, top_out)
    
    elif _get_platform() == "linux":
        top_cmd = subprocess.Popen(['top', '-b', '-n', '1'], shell=False, stdout=subprocess.PIPE)
        top_out, top_err= top_cmd.communicate()

        env["proc_load"] = _get_nth("Cpu\(s\):", 1, top_out)
        env["mem_load"] = _normalize(_get_nth("Mem:", 3, top_out))
        env["nb_process"] =  _get_nth("Tasks:",1, top_out)
        env["nb_process_running"] =  _get_nth("Tasks:",3, top_out)
        
    net_cmd = subprocess.Popen("host -r -W 1 google.com", shell=True, stdout=subprocess.PIPE)
    net_cmd.wait()
    env["net_available"] = True if net_cmd.returncode == 0 else False

    return env

if __name__ == '__main__':
    print get()
