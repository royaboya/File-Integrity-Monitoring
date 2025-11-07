import argparse
import monitor

# Creates a subcommand
def add_cust_cmd(subparser, name:str, desc:str, handler):
    custom_cmd = subparser.add_parser(name, help=desc)
    custom_cmd.set_defaults(func=handler)
    return custom_cmd

def add_cust_cmd_flag(subparser, name, alias, action, desc):
    subparser.add_argument(name, alias, action=action, help=desc)

def add_flag(parser, flag_name, desc=""):
    parser.add_argument(f"-{flag_name}", action="store_true", help=desc)

def scan(args):
    print("Scanning Directories from config")
    # need to display directories scanned
    if args.deep:
        monitor.scan(True)
    
    monitor.scan()
    
def generate_baseline(args):
    print("Generating a new baseline")
    monitor.generate_new_baseline()

def build_parser():
    
    parser = argparse.ArgumentParser(prog="fim", description="FIM system")
    subparser = parser.add_subparsers(dest="command", required=True)
    
    add_flag(parser, "r", "Generate a Report Summary after the scan")

    scan_cmd = add_cust_cmd(subparser, "scan", "Scans the directories in config and compares the values stored in the baseline", scan)
    generate_cmd = add_cust_cmd(subparser, "generate-baseline", "Creates a new baseline configuration for the files", generate_baseline)
    
    add_cust_cmd_flag(scan_cmd, "-d", "--deep", action="store_true", desc="Enable deep reursive scanning")
    
    return parser
    

def run(logger=None):
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)    
    
    if args.r:
        report = monitor.generate_report()
        print(report)

if __name__ == "__main__":
    run()
