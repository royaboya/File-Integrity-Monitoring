import argparse
import monitor

# Creates a subcommand
def add_cust_cmd(subparser, name:str, desc:str, handler):
    custom_cmd = subparser.add_parser(name, help=desc)
    custom_cmd.set_defaults(func=handler)

def add_flag(parser, flag_name, desc=""):
    parser.add_argument(f"-{flag_name}", action="store_true", help=desc)


def scan(args):
    print("Scanning Directories from config")
    # display directories scanned
    monitor.scan()
    
def generate_baseline(args):
    print("Generating a new baseline")
    monitor.generate_new_baseline()

def build_parser():
    
    parser = argparse.ArgumentParser(prog="fim", description="FIM system")
    subparser = parser.add_subparsers(dest="command", required=True)
    
    add_flag(parser, "r", "Generate a Report Summary after the scan")

    add_cust_cmd(subparser, "scan", "Scans the directories in config and compares the values stored in the baseline", scan)
    add_cust_cmd(subparser, "generate-baseline", "Creates a new baseline configuration for the files", generate_baseline)
        
    return parser
    

def run(logger=None):
    parser = build_parser()
    args = parser.parse_args()
    
    if args.r:
        monitor.generate_report()
    
    args.func(args)    


if __name__ == "__main__":
    run()
