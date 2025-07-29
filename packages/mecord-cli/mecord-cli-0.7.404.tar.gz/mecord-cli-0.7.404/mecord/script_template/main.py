##################################################
# do not change this file, real File is [run.py] #
##################################################
import argparse, json, os
from run import *

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--run", type=str, default=None, help=("input param file path"))
parser.add_argument("--out", type=str, default=None, help=("output file path"))
cmd_opts = parser.parse_args()

def main(cmd_opts):
    if cmd_opts.run == None or cmd_opts.out == None:
        print("args fail!")
        return
    
    if os.path.exists(cmd_opts.run):
        with open(cmd_opts.run, 'r', encoding='UTF-8') as f:
            data = json.load(f)
    result = runTask(data)
    with open(cmd_opts.out, 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    main(cmd_opts)
