from netemu import core

class State:
    class Node:
        def __init__(self, nid):
            self.proc = core.start_node()
            self.nid = nid

    def __init__(self):
        self.nodes = {}
        self.last_node = 0
        core.init()

    def new_node(self):
        self.last_node += 1

        n = self.Node(f"n{self.last_node}")
        self.nodes[n.nid] = n

        print(f"[{n.proc.pid}] Created node {n.nid}")

        return n.nid

    def close_nodes(self):
        for n in self.nodes.values():
            core.stop_node(n.proc)
