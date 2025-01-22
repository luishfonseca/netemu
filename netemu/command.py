from netemu.state import State

state = State()

class ExitCommand:
    def __init__(self):
        pass
    def run(self):
        state.close_nodes()

class NewCommand:
    def __init__(self):
        pass
    def run(self):
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

    def __init__(self, nid, line):
        if not line:
            self.cmd = NodeCommand.Execute(nid, ["sh"])
        else:
            match line[0]:
                case "execute" | "exec" | "x":
                    self.cmd = NodeCommand.Execute(nid, line[1:])
                case _:
                    self.cmd = NodeCommand.Execute(nid, line)
    def run(self):
        self.cmd.run()
