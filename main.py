import sys

from src.overview import OverviewCommand
from src.settings import create_config_file, read_config_file


def main() -> None:
    try:
        config = read_config_file()
    except FileNotFoundError:
        create_config_file()
        config = read_config_file()
    overview = OverviewCommand(config)
    try:
        overview.run()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()
