from rich.console import Console
from rich.syntax import Syntax
from rich.markup import escape

class CuriumParseError:
    def __init__(self,name="Builtin Exception"):
        self.name=name
    def raiseExec(self, message, line, lineno, start, end):
        # Start the rich console
        ec = Console()

        # Get the size of the error
        size = end - start

        # Update start
        linenoFormat = f"{lineno}-| "
        pos = start + len(linenoFormat)

        # Overline
        ec.print(f"|{'-'*max(50,end)}")

        # Print the line
        ec.print(f"| {linenoFormat}{escape(line)}")
        # Print the position
        ec.print(f"| {' '*pos}{'^'*size}")

        # Newline
        ec.print("|")

        # And the error
        ec.print(f"| [red][i]{self.name}[/i] on line [i]{lineno}[/i], col [i]{start}[/i]:[/red]", highlight=False)

        # And the message
        ec.print(f"| \t{message}")



