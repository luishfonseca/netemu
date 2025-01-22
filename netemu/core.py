import os
import signal
import subprocess
from multiprocessing import Process, Pipe


def _node(ready):
    os.unshare(os.CLONE_NEWNET)
    ready.send(True)
    while True:
        try:
            signal.pause()
        except KeyboardInterrupt:
            pass


def _runner(pid, cmds, disown):
    fd = os.open(f"/proc/{pid}/ns/net", os.O_RDONLY)
    os.setns(fd, os.CLONE_NEWNET)
    os.close(fd)
    run(cmds, disown)


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


def run(cmds, disown=False):
    for cmd in cmds:
        if disown:
            subprocess.Popen(cmd)
        else:
            subprocess.run(cmd)


def start_node():
    ready_rcv, ready_snd = Pipe(False)
    proc = Process(target=_node, args=(ready_snd,))
    proc.start()
    assert ready_rcv.recv()
    return proc


def stop_node(proc):
    proc.terminate()
    while True:
        try:
            proc.join()
            break
        except KeyboardInterrupt:
            pass


def run_in_node(proc, cmds, disown=False):
    proc = Process(target=_runner, args=(proc.pid, cmds, disown))
    proc.start()
    while True:
        try:
            proc.join()
            break
        except KeyboardInterrupt:
            proc.terminate()
            print()
