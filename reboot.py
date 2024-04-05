#!/usr/bin/python3
import argparse
import configparser
import os


parser = argparse.ArgumentParser()
parser.add_argument('target')
parser.add_argument('-y',action='store_true')
parser.add_argument('-g','--grub',action='store_true')
parser.add_argument('-i','--initrd',action='store_true')
args = parser.parse_args()

config = configparser.ConfigParser()
config.read("/etc/reboot.py/config.ini")
targets=config.get('General','targets').split(",")
files=config.get('General','files').split(",")

if args.target not in targets:
    c=0
    _t=""
    for t in targets:
        if t.startswith(args.target):
            _t=t
            c+=1
    if c == 0: raise Exception(f"{target} target doesn't exist")
    elif c>1: raise Exception(f"multiple targets match {target}")
    else: target=_t
else: target=args.target
print(f"booting to {target}")


for file in files:
    with open(file, "r+") as f:
        lines = f.readlines()
        for l in range(len(lines)):
            if lines[l].endswith(f"#reboot-{target}\n") and lines[l].startswith("#"): lines[l]=lines[l][1:] 
            for _target in [t for t in targets if t!=target]:
                if lines[l].endswith(f"#reboot-{_target}\n") and not lines[l].startswith("#"): lines[l]="#"+lines[l] 
        lines="".join(lines)
        f.seek(0)
        f.write(lines)

if args.initrd:os.system("dracut --regenerate-all -f")
if args.grub: os.system("grub2-mkconfig -o /boot/grub2/grub.cfg")
os.system("sync")

if not args.y:
    input("waiting for enter to reboot")

os.system("reboot")
