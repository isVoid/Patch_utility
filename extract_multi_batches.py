import os
import subprocess

try: input = raw_input
except: pass

root = input("Input the root folder for all patches: ")
batches = input("Input the 'batches:patch_per_image' that you want to extract, separate by ,(comma): ")
target = input("Extract pathces to: ")

cop = os.path.join(target, "Clean")
nop = os.path.join(target, "Noisy")

batches = batches.split(",")
for b in batches:
    ppi = b.split(":")[-1]
    b = b.split(":")[0]
    p = os.path.join(root, b)
    cp = os.path.join(p, "Clean")
    np = os.path.join(p, "Noisy")

    # print (ppi, b, p, cp, np)
    print (subprocess.call(['python', 'extract_patches.py', np, cp, '-no', nop, '-co', cop, '-ppi', ppi]))
