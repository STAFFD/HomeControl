from Server import HomeServer
import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-IP', type=str, default='192.168.2.240')
parser.add_argument('-p', type=int, default=8000)
args = parser.parse_args()


homeServer = HomeServer(args.IP, args.p)
homeServer.run()
