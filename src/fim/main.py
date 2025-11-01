import cli
from logger import initialize_logger

def main():
    initialize_logger("../../logs/fim.log", "UTF-8", level="DEBUG", format="%(asctime)s - %(levelname)s -%(message)s")
    cli.run()
    
if __name__ == "__main__":
    main()