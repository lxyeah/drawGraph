import csv
import os
import shutil

import pandas as pd

from src.const.Const import tmp_dir, data_base, projName, next_base


def rebuild_dir(dir_path: str, skip=False):
    if os.path.exists(dir_path):
        if skip:
            return False
        else:
            shutil.rmtree(dir_path)
    os.makedirs(dir_path)
    return True


class FileTool:
    def __init__(self):
        return

    def get_data_from_file(self, fileName, path=tmp_dir):
        file_dir = path + fileName
        file_datas = []
        with open(file_dir, "r") as f:
            reader = csv.reader(f)
            for i in reader:
                file_datas.append(i)
            f.close()
        return file_datas

    def save_datas2target_path(self, headers, datas, path):
        with open(path + ".csv", 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(datas)
        print("operator save file : " + path + ".csv |||| save finished")

    def save_to_file(self, fileName, headers: str, datas, projname=projName):
        with open(data_base + projname + "/" + fileName + ".csv", 'w', newline="") as f:
            # print("start writing")
            writer = csv.writer(f)
            # headers = 'categpry,vtype,priority,rank,project,origin commit,buggy commit, ' \
            #           'buggy path, buggy start, buggy end, fixer, fixer path,life time'.split(",")
            writer.writerow(headers)
            writer.writerows(datas)

    def save_to_target_file(self, fileName, headers: str, datas):
        with open(data_base + fileName + ".csv", 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(datas)

    def save_next_file(self, fileName, headers: str, datas, projname=projName):
        with open(next_base + projname + "/" + fileName + ".csv", 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(datas)
        print(next_base + projname + "/" + fileName + ".csv save finished")

    def dataFrame2ListMutilRow(self, datas: pd.DataFrame):
        headers = [""] + datas.columns.tolist()
        row_idx = datas.index.tolist()
        data = datas.values.tolist()
        rows = []
        for i in range(len(row_idx)):
            rows.append(list(row_idx[i]) + data[i])
        return headers, rows

    # def dataFrame2list(self, datas: pd.DataFrame):
    #     headers = [""] + datas.columns.tolist()
    #     row_idx = datas.index.tolist()
    #     data = datas.values.tolist()
    #     rows = []
    #     for i in range(len(row_idx)):
    #         rows.append([row_idx[i]] + data[i])
    #     return headers, rows

    def dataFrame2list(self, datas: pd.DataFrame, transform: map = {}):
        top = datas.columns.tolist()
        headers = [""]
        for i in top:
            headers.append(transform.get(i, i))
        row_idx = datas.index.tolist()
        data = datas.values.tolist()
        rows = []
        for i in range(len(row_idx)):
            rows.append([transform.get(row_idx[i], row_idx[i])] + data[i])
        return headers, rows

    def isfloat(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    os.makedirs("/Users/mayang/PycharmProjects/summary2Excel/resource/tmp/test/")
