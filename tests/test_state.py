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
