import cli
from logger import initialize_logger

def main():
    initialize_logger("../../logs/info.log","../../logs/errors.log", 5_000_000)
    cli.run()
    
if __name__ == "__main__":
    main()