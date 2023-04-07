from argparse import ArgumentParser
import hashlib
import os
import shutil
import pathlib
from uuid import uuid4

SUPPORT_FILE_TYPES = ["png", "jpeg", "heic", "jpg", "mp4", "avi", "mov"]
IGNORE_FILES = ["DS_Store"]

parser = ArgumentParser()
parser.add_argument("--target_folder_path", help="target folder")
parser.add_argument("--invalid_folder_path", help="invalid folder")
parser.add_argument("--valid_folder_path", help="valid folder")

args = parser.parse_args()
print("target folder path", args.target_folder_path)
print("invalid folder path", args.invalid_folder_path)
print("valid folder path", args.valid_folder_path)

checker = set()

def cal_hash(filename):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        buf = f.read()
        m.update(buf)

    hash_key = m.hexdigest()
    return hash_key

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

def is_valid_file_type(filename):
    lowers = filename.lower()
    for t in SUPPORT_FILE_TYPES:
        if t in lowers:
            return True
    return False

def is_ignore_file(filename):
    for t in IGNORE_FILES:
        if t in filename:
            return True
    return False

def move_file(src, dest_folder):
    filename = pathlib.Path(src).name
    dest = os.path.join(dest_folder, filename)
    print(dest)
    if os.path.exists(dest):
        parent = "/".join(dest.split("/")[:-1])
        name, suffix = os.path.join(parent, filename.split(".")[0]), filename.split(".")[1]
        dest = "{name}-{uuid}.{suffix}".format(name=name, uuid=str(uuid4()).split("-")[1], suffix=suffix)
    shutil.move(src, dest)

for current_filepath in list_files(args.target_folder_path):
    if is_ignore_file(current_filepath):
        continue
    if not is_valid_file_type(current_filepath):
        # move to invalid folder
        move_file(current_filepath, args.invalid_folder_path)
        continue
    hash_key = cal_hash(current_filepath)

    # check hash key is in set or not
    if hash_key not in checker:
        checker.add(hash_key)
        move_file(current_filepath, args.valid_folder_path)
    else:
        move_file(current_filepath, args.invalid_folder_path)
