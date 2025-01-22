from netemu.state import State

state = State()


class ExitCommand:
    def __init__(self):
        pass

    def run(self):
        state.close_nodes()


class NewCommand:
    def __init__(self, line):
        if not line:
            self.switch = False
        else:
            match line[0]:
                case "switch" | "sw":
                    self.switch = True
                case "node" | "n":
                    self.switch = False
                case _:
                    print("Unknown command")

    def run(self):
        if self.switch:
            state.new_switch()
        else:
            state.new_node()


class NodeCommand:
    class Execute:
        def __init__(self, nid, line):
            self.nid = nid
            self.exec = line

        def run(self):
            disown = self.exec[-1] == "&"
            if disown:
                self.exec = self.exec[:-1]
            state.execute(self.nid, self.exec, disown)

    class Connect:
        def __init__(self, nid1, nid2):
            self.nid1 = nid1
            self.nid2 = nid2

        def run(self):
            state.connect(self.nid1, self.nid2)

    def __init__(self, nid, line):
        if not line:
            self.cmd = NodeCommand.Execute(nid, ["sh"])
        else:
            match line[0]:
                case "connect" | "conn" | "c":
                    self.cmd = NodeCommand.Connect(nid, line[1])
                case "execute" | "exec" | "x":
                    self.cmd = NodeCommand.Execute(nid, line[1:])
                case _:
                    self.cmd = NodeCommand.Execute(nid, line)

    def run(self):
        self.cmd.run()
