# coding=utf-8

import sys
import os

try:
    current_file = os.path.dirname(__file__)
except:
    current_file = os.path.dirname(sys.argv[0])
sys.path.insert(0, current_file)

try:
    import HoudiniAnalyze
except:
    HoudiniAnalyze = __import__("HoudiniAnalyze_py%d%d" % (sys.version_info[0], sys.version_info[1]))

args = sys.argv

cmd_input = '-input'
cmd_output = '-output'


if cmd_input in args:
    cg_file_flag = args.index(cmd_input)
    hip_file = args[cg_file_flag + 1]

if cmd_output in args:
    path_json_flag = args.index(cmd_output)
    json_file = args[path_json_flag + 1]


param_dict = {
    "hip_path": hip_file,
    "output_path": json_file,
}

HoudiniAnalyze.HoudiniAnalyze(param_dict)
