import sys

from importlib.metadata import entry_points, version


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: camera-segment <command> [options]")
        print()
        print("Available commands:")
        for ep in entry_points(group="camera_segment.commands"):
            print(f"  {ep.name}")
        sys.exit(1)

    cmd_name, *cmd_args = argv

    plugins = {ep.name: ep for ep in entry_points(group="camera_segment.commands")}

    if cmd_name not in plugins:
        print(f"Unknown command: {cmd_name}")
        sys.exit(1)

    cmd = plugins[cmd_name].load()
    cmd(cmd_args)


def show_version(*args):
    print(f"camera-segment: v{version('camera-segment')}")
    sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    main()
