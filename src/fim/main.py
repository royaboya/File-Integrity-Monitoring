import cli
from logger import initialize_logger


def main():
    log = initialize_logger("../../logs/fim.log", "UTF-8", level="DEBUG")
    cli.run(log)
    
if __name__ == "__main__":
    main()