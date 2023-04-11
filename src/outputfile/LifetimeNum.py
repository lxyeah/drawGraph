from itertools import groupby

from src.const.Const import base_dir, fileMap
from src.tools.FileTool import FileTool


class LifetimeNum():
    def __init__(self):
        self.ft = FileTool()

    def get_datas(self, projName):
        file_path = base_dir + "resource/datas/" + projName + "/"
        datas = self.ft.get_data_from_file('marked datas.csv', file_path)
        return datas

    def get_TPFP_average_lifetime(self, projName):
        datas = self.get_datas(projName)[1:]
        sorted_datas = sorted(datas, key=lambda x: (x[fileMap.get("resolution_line")]))
        group_datas = groupby(sorted_datas, key=lambda x: (x[fileMap.get("resolution_line")]))
        for key, group in group_datas:
            print(key, self.get_average_lifetime(list(group)))

    def get_average_lifetime(self, datas):
        sum = 0
        for i in datas:
            sum += int(i[fileMap.get("life_time_line")])
        return sum / len(datas)


if __name__ == '__main__':
    lt = LifetimeNum()
    lt.get_TPFP_average_lifetime("commons-digester")
