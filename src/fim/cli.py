import argparse
import monitor


def add_cust_cmd(subparser, name:str, desc:str, handler):
    custom_cmd = subparser.add_parser(name, help=desc)
    custom_cmd.set_defaults(func=handler)

def add_flag(parser, flag_name):
    parser.add_argument(f"-{flag_name}", action="store_true")


# r flag (generate a report)
def scan_for_flags(parser):
    pass

def scan(args):
    print("Scanning Directories from config")
    monitor.scan()
    # add display
    
def generate_baseline(args):
    print("Generating a new baseline")
    monitor.generate_new_baseline()
    # add display

def build_parser():
    
    parser = argparse.ArgumentParser(prog="fim", description="FIM system")
    subparser = parser.add_subparsers(dest="command", required=True)
    
    add_flag(parser, "r")

    
    add_cust_cmd(subparser, "scan", "Scans the directories in config and compares the values stored in the baseline", scan)
    add_cust_cmd(subparser, "generate-baseline", "Creates a new baseline configuration for the files", generate_baseline)
    
    #add -r optin
    
    return parser
    

def run(logger=None):
    parser = build_parser()
    args = parser.parse_args()
    
    args.func(args)    


if __name__ == "__main__":
    run()
