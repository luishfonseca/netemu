import os
import signal
from multiprocessing import Process

def _node():
    os.unshare(os.CLONE_NEWNET)
    while True:
        signal.pause()

def init():
    uid = os.getuid()
    gid = os.getgid()

    os.unshare(os.CLONE_NEWUSER | os.CLONE_NEWNET)

    with open("/proc/self/uid_map", "w") as f:
        f.write(f"0 {uid} 1")

    with open("/proc/self/setgroups", "w") as f:
        f.write("deny")

    with open("/proc/self/gid_map", "w") as f:
        f.write(f"0 {gid} 1")

def start_node():
    proc = Process(target=_node, args=())
    proc.start()
    return proc

def stop_node(proc):
    proc.terminate()
    proc.join()
