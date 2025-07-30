from argparse import ArgumentParser

from ftts.commands.serve import ServerCommand
from ftts.commands.infer import InferCommand


def main():
    parser = ArgumentParser(
        "FTTS CLI tool",
        usage="fhtts <command> [<args>]",
        epilog="For more information about a command, run: `fhtts <command> --help`",
    )
    commands_parser = parser.add_subparsers(help="fhtts command helpers")

    # Register commands
    ServerCommand.register_subcommand(commands_parser)
    InferCommand.register_subcommand(commands_parser)

    # Let's go
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    # Run
    service = args.func(args)
    service.run()


if __name__ == "__main__":
    main()
