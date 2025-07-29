from .generator import ProjectGenerator


def register(subparsers):
    parser = subparsers.add_parser("create", help="Create a new project directory")
    parser.add_argument("name", metavar="NAME", help="Name of the new project")
    parser.set_defaults(func=main)


def main(args):
    generator = ProjectGenerator(args.name, config=None)
    generator.run()
