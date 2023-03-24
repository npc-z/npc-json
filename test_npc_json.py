from internal import test_parser, test_scanner
from internal.utils import log


def main():
    log("hello npc-json")
    test_parser.test_parser_with_list_with_additional_comma()


if __name__ == "__main__":
    main()
