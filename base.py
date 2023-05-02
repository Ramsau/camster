from funcs import *
import argparse

parser = argparse.ArgumentParser(description='Simulate a mouse with a laser')
parser.add_argument('--background', help='debugging mode', action='store_true')

args = parser.parse_args()
vidLoop(args.background)