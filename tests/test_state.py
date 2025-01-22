from netemu.state import State
import os

def test_new_node():
    state = State()
    nid = state.new_node()

    assert nid == "n1"
    assert nid in state.nodes

    assert os.path.exists(f"/proc/{state.nodes[nid].proc.pid}")

    parent_userns = os.readlink(f"/proc/{os.getpid()}/ns/user")
    parent_netns = os.readlink(f"/proc/{os.getpid()}/ns/net")
    userns = os.readlink(f"/proc/{state.nodes[nid].proc.pid}/ns/user")
    netns = os.readlink(f"/proc/{state.nodes[nid].proc.pid}/ns/net")

    assert userns == parent_userns
    assert netns != parent_netns

    state.close_nodes()

    assert not os.path.exists(f"/proc/{state.nodes[nid].proc.pid}")

def test_execute_no_node(capfd):
    state = State()

    state.execute("n1", ["sh"])

    assert capfd.readouterr().out == "Node n1 does not exist\n"

def test_execute(capfd):
    state = State()
    nid = state.new_node()

    netns = os.readlink(f"/proc/{state.nodes[nid].proc.pid}/ns/net")

    capfd.readouterr()

    state.execute(nid, ["readlink", "/proc/self/ns/net"])

    assert capfd.readouterr().out == f"{netns}\n"

    state.close_nodes()
    