import netemu.command as cmd


def main():
    while True:
        try:
            line = input("> ").split()
        except (EOFError, KeyboardInterrupt):
            print()
            cmd.ExitCommand().run()
            break

        if len(line) == 0:
            continue

        match line[0]:
            case "exit":
                cmd.ExitCommand().run()
                break
            case "new" | "n":
                cmd.NewCommand(line[1:]).run()
            case _:
                cmd.NodeCommand(line[0], line[1:]).run()
