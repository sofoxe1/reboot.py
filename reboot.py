#!/usr/bin/python3
import argparse
import configparser
import subprocess


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
initrd_command=config.get('General','initrd_command')
grub_command=config.get('General','grub_command')
values=list(config.items("General"))

preexec=None
postexec=None
default_args=None
strip_spaces=False

for v in values:
    if v[0] == "args":
        default_args=v[1]
    elif v[0] == "strip_spaces":
        strip_spaces=bool(v[1])
    elif v[0] == "preexec":
        preexec=v[1]
    elif v[0] == "postexec":
        postexec=v[1]

_args=None
targets=targets+config.sections()
targets.remove("General")
if args.target not in targets:
    c=0
    _t=""
    for t in targets:
        if t.startswith(args.target):
            _t=t
            c+=1
    if c == 0: raise Exception(f"{target} doesn't exist")
    elif c>1: raise Exception(f"multiple targets match {target}")
    else: args.target=_t
switch=False
s_targets=[]
current=""
_args=default_args
if args.target in config.sections():
    values=list(config.items(args.target))
    for v in values:
        if v[0] == "args":
            if v[0].startswith("+"):
                _args=default_args+v[1][1:]
            else:
                _args=v[1]
        elif v[0] == "strip_spaces":
            strip_spaces=bool(v[1])
        elif v[0] == "preexec":
            preexec=v[1]
        elif v[0] == "postexec":
            postexec=v[1]
        elif v[0] == "targets":
            switch=True
            s_targets=v[1].split(",")
            current=config.get(args.target,"current")
            print(s_targets)
            print(current)
            s_targets.remove(current)
            config[args.target]["current"]=s_targets[0]
            args.target=s_targets[0]
            


with open("/etc/reboot.py/config.ini","w") as f:
    config.write(f)


for c in _args:
    if c=="g": args.grub=True
    elif c == "i": args.initrd=True
    elif c == "y": args.y=True
    

if preexec is not None: subprocess.run(preexec.split(" "),check=True)
for file in files:
    with open(file, "r+") as f:
        lines = f.readlines()
        for l in range(len(lines)):
            if strip_spaces:
                lines[l]=lines[l].strip()
            if lines[l].endswith(f"#reboot-{args.target}\n") and lines[l].startswith("#"): lines[l]=lines[l][1:] 
            for target in [t for t in targets if t!=args.target]:
                if lines[l].endswith(f"#reboot-{target}\n") and not lines[l].startswith("#"): lines[l]="#"+lines[l] 
        lines="".join(lines)
        f.seek(0)
        f.write(lines)

if args.initrd:subprocess.run(initrd_command.split(" "),check=True)
if args.grub: subprocess.run(grub_command.split(" "),check=True)
subprocess.run("sync")

if not args.y:
    input("waiting for enter to reboot")
if postexec is not None: subprocess.run(postexec.split(" "),check=True)
subprocess.run("reboot",check=True)
