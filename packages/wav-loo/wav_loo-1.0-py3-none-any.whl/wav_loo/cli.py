"""
Command line interface for WAV Finder.
"""

import argparse
import sys
import subprocess
from .finder import WavFinder


def cmd_find(args):
    finder = WavFinder()
    if args.verbose:
        print(f"Searching for WAV files in: {args.path}")
    wav_files = finder.find_wav_files(args.path)
    if args.verbose:
        print(f"Found {len(wav_files)} WAV file(s)")
    if wav_files:
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    for wav_file in wav_files:
                        f.write(f"{wav_file}\n")
                print(f"Results saved to: {args.output}")
            except IOError as e:
                print(f"Error writing to file {args.output}: {e}")
                sys.exit(1)
        else:
            for wav_file in wav_files:
                print(wav_file)
    else:
        print("No WAV files found.")
        sys.exit(1)

def cmd_kgn(args):
    subprocess.run(["kubectl", "get", "pods", "-o", "wide", "-n", "signal"])

def cmd_gp(args):
    subprocess.run(["gpustat", "-i"])

def cmd_uv(args):
    subprocess.run(["uv", "pip", "install", "-i", "http://mirrors.unisound.ai/repository/pypi/simple"] + args.packages)

def cmd_kd(args):
    subprocess.run(["kubectl", "delete", "pods"])
def cmd_kg(args):
    subprocess.run(["kubectl", "get", "pods", "-o", "wide"])
def cmd_kl(args):
    subprocess.run(["kubectl", "logs"])
def cmd_rs(args):
    subprocess.run(["kubectl", "describe", "ResourceQuota", "-n"] + args.extra)
def cmd_kdn(args):
    subprocess.run(["kubectl", "delete", "pods", "-n", "signal"])
def cmd_kln(args):
    subprocess.run(["kubectl", "logs", "-n", "signal"])
def cmd_at(args):
    subprocess.run(["atlasctl", "top", "node"])
def cmd_ad(args):
    subprocess.run(["atlasctl", "delete", "job"])
def cmd_atd(args):
    subprocess.run(["atlasctl", "delete"])
def cmd_adp(args):
    subprocess.run(["atlasctl", "delete", "job", "pytorchjob"])
def cmd_adn(args):
    subprocess.run(["atlasctl", "delete", "job", "-n", "signal"])
def cmd_tb(args):
    subprocess.run(["tensorboard", "--port=3027", "--logdir=."])
def cmd_ca(args):
    subprocess.run(["conda", "activate"] + args.env)
def cmd_kgg(args):
    subprocess.run(["kubectl", "get", "po", "--all-namespaces", "-o", "wide"] + ["|", "grep"] + args.extra)

def main():
    parser = argparse.ArgumentParser(description="wav-loo: multi-tool CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # find subcommand
    parser_find = subparsers.add_parser("find", help="Find WAV files from URLs or local paths")
    parser_find.add_argument('path', help='URL or local path to search for WAV files')
    parser_find.add_argument('--output', '-o', help='Output file to save results (optional)')
    parser_find.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser_find.set_defaults(func=cmd_find)

    # kd subcommand
    parser_kd = subparsers.add_parser("kd", help="kubectl delete pods")
    parser_kd.set_defaults(func=cmd_kd)

    # kg subcommand
    parser_kg = subparsers.add_parser("kg", help="kubectl get pods -o wide")
    parser_kg.set_defaults(func=cmd_kg)

    # kl subcommand
    parser_kl = subparsers.add_parser("kl", help="kubectl logs")
    parser_kl.set_defaults(func=cmd_kl)

    # rs subcommand
    parser_rs = subparsers.add_parser("rs", help="kubectl describe ResourceQuota -n ...")
    parser_rs.add_argument('extra', nargs=argparse.REMAINDER, help='Extra args')
    parser_rs.set_defaults(func=cmd_rs)

    # kdn subcommand
    parser_kdn = subparsers.add_parser("kdn", help="kubectl delete pods -n signal")
    parser_kdn.set_defaults(func=cmd_kdn)

    # kgn subcommand
    parser_kgn = subparsers.add_parser("kgn", help="kubectl get pods -o wide -n signal")
    parser_kgn.set_defaults(func=cmd_kgn)

    # kln subcommand
    parser_kln = subparsers.add_parser("kln", help="kubectl logs -n signal")
    parser_kln.set_defaults(func=cmd_kln)

    # at subcommand
    parser_at = subparsers.add_parser("at", help="atlasctl top node")
    parser_at.set_defaults(func=cmd_at)

    # ad subcommand
    parser_ad = subparsers.add_parser("ad", help="atlasctl delete job")
    parser_ad.set_defaults(func=cmd_ad)

    # atd subcommand
    parser_atd = subparsers.add_parser("atd", help="atlasctl delete")
    parser_atd.set_defaults(func=cmd_atd)

    # adp subcommand
    parser_adp = subparsers.add_parser("adp", help="atlasctl delete job pytorchjob")
    parser_adp.set_defaults(func=cmd_adp)

    # adn subcommand
    parser_adn = subparsers.add_parser("adn", help="atlasctl delete job -n signal")
    parser_adn.set_defaults(func=cmd_adn)

    # tb subcommand
    parser_tb = subparsers.add_parser("tb", help="tensorboard --port=3027 --logdir=.")
    parser_tb.set_defaults(func=cmd_tb)

    # ca subcommand
    parser_ca = subparsers.add_parser("ca", help="conda activate <env>")
    parser_ca.add_argument('env', nargs=argparse.REMAINDER, help='Conda environment name')
    parser_ca.set_defaults(func=cmd_ca)

    # kgg subcommand
    parser_kgg = subparsers.add_parser("kgg", help="kubectl get po --all-namespaces -o wide | grep ...")
    parser_kgg.add_argument('extra', nargs=argparse.REMAINDER, help='Extra args for grep')
    parser_kgg.set_defaults(func=cmd_kgg)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main() 