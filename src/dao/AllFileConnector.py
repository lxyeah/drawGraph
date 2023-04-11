import operator
import os
import random

import numpy as np

from src.const import Const
from src.const.Const import categroyMap, fileMap, tmp_dir, projName, data_dir

from src.tools.FileTool import FileTool


class AllFileConnector:
    def __init__(self):
        root_dir = Const.base_dir + "resource/datas/"
        self.alldatas = {}
        self.datas = []
        self.f = FileTool()
        for proj in Const.projList:
            files = root_dir + proj + "/marked datas.csv"
            tmpdatas = []
            for file in [files]:
                data = self.f.get_data_from_file(file, "")[1:]
                now_data = []
                for i in data:
                    # if "Test.java" in i[fileMap.get('file_line')] or 'src/test' in i[fileMap.get('file_line')]:
                    #     continue
                    # if i[fileMap.get('resolution_line')] == '':
                    #     i[fileMap.get('resolution_line')] = 'unfixed'
                    # i[fileMap.get("category_line")] = categroyMap.get(i[fileMap.get('category_line')])
                    now_data.append(i[:fileMap.get("resolution_line")+1])
                tmpdatas = tmpdatas + now_data
            self.datas += tmpdatas
            self.alldatas[proj] = tmpdatas

    def findByFixedAndProject(self, projName: str):
        def get_fixed_target(x):
            return x[fileMap.get("project_line")] == projName and x[fileMap.get("resolution_line")] == 'fixed'

        return list(filter(get_fixed_target, self.datas))

    def findBasedAndProjectAndFixed(self, based: str, target_value: str, projName: str):
        def basedAndProject(x):
            return x[fileMap.get(based + "_line")] == target_value and x[fileMap.get("project_line")] == projName \
                   and x[fileMap.get("resolution_line")] == 'fixed'

        return list(filter(basedAndProject, self.datas))

    def findBasedAndProjectAndType(self, projName: str, resType: list):
        def basedAndProjectAndResType(x):
            return x[fileMap.get("project_line")] == projName and x[fileMap.get("resolution_line")] in resType

        return list(filter(basedAndProjectAndResType, self.datas))

    def findBasedAndFixed(self, datas: list, based: str, target_value: str):
        def get_fixed_target(x):
            return x[fileMap.get(based + "_line")] == target_value

        return list(filter(get_fixed_target, datas))


if __name__ == "__main__":
    fileConnector = AllFileConnector()
    # x_data, y_datas = fileConnector.findFieldGroupCounts(projName, 'vtype')
    # for i in range(len(x_data)):
    #     print(x_data[i] + " " + str(y_datas[i]))
    print(fileConnector.alldatas.keys())
