from .generator import ProjectGenerator


def register(subparsers):
    parser = subparsers.add_parser("project", help="Create a new project directory")
    parser.add_argument("name", metavar="NAME", help="Name of the new project")
    parser.set_defaults(func=main)


def main(args, config):
    generator = ProjectGenerator(args.name, config=config)
    generator.run()
