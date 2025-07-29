import sys
from pprint import pprint
from datetime import datetime
from termcolor import cprint


def main():
    cprint(
        "\n✨ Welcome to pyql – Your Natural Language Interface for SQL & CQL ✨",
        "cyan",
        attrs=["bold"],
    )
    cprint("--------------------------------------------------------------", "green")

    cprint(
        "🔍 Ask me database questions in plain English, and I’ll translate them into SQL/Cypher.\n",
        "yellow",
    )

    cprint("🛠  Example usage:", "magenta")
    pprint("▶ pyql 'Show me all users who signed up last month'")

    cprint("📅 Current session: ", "blue", end="")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cprint("--------------------------------------------------------------", "green")
