import sys

from tournament import Tournament

def main():
    tournament = Tournament(200, 5)
    tournament.start(True)
    print(tournament.results())
    return 0

if __name__ == "__main__":
    sys.exit(main())