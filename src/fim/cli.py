import argparse

import monitor

def add_cust_cmd(subparser, name:str, desc:str, handler):
    custom_cmd = subparser.add_parser(name, help=desc)
    custom_cmd.set_defaults(func=handler)

def scan(args):
    #print("scan command called")
    monitor.scan()

def generate_baseline(args):
    print("generate baseline called")
    # monitor.generate_new_baseline()


def build_parser():
    
    parser = argparse.ArgumentParser(prog="fim", description="FIM system")
    subparser = parser.add_subparsers(dest="command", required=True)
    
    add_cust_cmd(subparser, "scan", "description", scan)
    add_cust_cmd(subparser, "generate-baseline", "description", generate_baseline)
    
    return parser
    

def main():
    parser = build_parser()
    args = parser.parse_args()
    
    args.func(args)    


if __name__ == "__main__":
    main()


# Example cmds
# python main.py scan -> runs through config and scan list of dirs and file paths
# python main.py generate-baseline -> creates a new baseline and stores it
# python main.py -h