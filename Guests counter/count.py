import os
import re

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
file_path = os.path.join(dir_path, 'list.txt')
with open(file_path, 'r') as f:
    data = f.read()
    pattern = re.compile(r'(ob|Ob|14[^.]*)')
    print(len(pattern.findall(data)))