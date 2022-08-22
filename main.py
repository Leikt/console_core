from argparse import ArgumentParser

import terminal

parser = ArgumentParser()
commands = terminal.load_plugins_from_file('plugins.txt')
ter: terminal.PTerminal = terminal.Terminal(parser)
ter.initialize(commands)
ter.mainloop()
