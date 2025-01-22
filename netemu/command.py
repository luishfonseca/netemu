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
