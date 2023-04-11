import os

from src.const.Const import next_dir, base_dir, projName, data_base


class InitTool:
    def __init__(self, projname=projName):
        root_path = data_base + projname + "/"
        os.makedirs(next_dir, exist_ok=True)
        os.makedirs(root_path, exist_ok=True)
        os.makedirs(root_path + "category/", exist_ok=True)
        os.makedirs(root_path + "field/", exist_ok=True)
        os.makedirs(root_path + "metrics/", exist_ok=True)
        os.makedirs(root_path + "file/", exist_ok=True)
        os.makedirs(root_path + "method/", exist_ok=True)
        os.makedirs(root_path + "priority/", exist_ok=True)
        os.makedirs(root_path + "rank/", exist_ok=True)
        os.makedirs(root_path + "spearman/", exist_ok=True)
        os.makedirs(root_path + "vtype/", exist_ok=True)
        os.makedirs(base_dir + "resource/datas/summary/", exist_ok=True)
        return
