import operator
import os
import random

import numpy as np

from src.const.Const import categroyMap, fileMap, projName, tmp_base, data_base
from src.tools.FileTool import FileTool


class FileConnector:
    def __init__(self, proj=projName, skip=False):
        tmp_dir = tmp_base + proj + "/"
        files = os.listdir(tmp_dir)
        self.f = FileTool()
        self.datas = []
        if skip:
            return
        for file in files:
            data = self.f.get_data_from_file(file, tmp_dir)
            now_data = []
            for i in data:
                if "Test.java" in i[fileMap.get('file_line')] or 'src/test' in i[fileMap.get('file_line')]:
                    continue
                if i[fileMap.get('resolution_line')] == '':
                    i[fileMap.get('resolution_line')] = 'unfixed'
                i[fileMap.get("category_line")] = categroyMap.get(i[fileMap.get('category_line')])
                now_data.append(i)
            self.datas = self.datas + now_data

    def reload_datas_from_before(self, proj=projName):
        dir = tmp_base + "/before/"
        name = proj + " left join res.csv"
        self.datas = self.f.get_data_from_file(name, dir)

    def reload_datas_from_after(self, proj=projName):
        dir = tmp_base + "/after/"
        name = proj + " left join res.csv"
        self.datas = self.f.get_data_from_file(name, dir)

    def download_project(self, projName):
        cmd = "git clone https://github.com/apache/" + projName
        print("first step is : " + cmd)
        os.system(cmd)

    def delete_project(self, projName):
        cmd = "rm -rf " + projName
        print("third step is : " + cmd)
        # os.system(cmd)

    def findByProject(self, projName: str):
        def get_target(x):
            return x[fileMap.get("project_line")] == projName

        return list(filter(get_target, self.datas))

    def findByUnfixedAndProject(self, projName: str):
        def get_fixed_target(x):
            return x[fileMap.get("project_line")] == projName and x[fileMap.get("resolution_line")] != 'fixed';

        return list(filter(get_fixed_target, self.datas))

    def findByFixedAndProject(self, projName: str):
        def get_fixed_target(x):
            return x[fileMap.get("project_line")] == projName and x[fileMap.get("resolution_line")] == 'fixed';

        return list(filter(get_fixed_target, self.datas))

    def findByVtypeAndProject(self, vtype: str, projName: str):
        def vtypeAndPrjoectfilter(x):
            return x[fileMap.get("vtype_line")] == vtype and x[fileMap.get("project_line")] == projName

        return list(filter(vtypeAndPrjoectfilter, self.datas))

    def findBasedProjectCounts(self, projName: str, based: str):
        # def

        return list(filter())

    def findBasedAndProject(self, based: str, target_value: str, projName: str):
        def basedAndProject(x):
            return x[fileMap.get(based + "_line")] == target_value and x[fileMap.get("project_line")] == projName

        return list(filter(basedAndProject, self.datas))

    def findBasedAndProjectAndFixed(self, based: str, target_value: str, projName: str):
        def basedAndProject(x):
            return x[fileMap.get(based + "_line")] == target_value and x[fileMap.get("project_line")] == projName \
                   and x[fileMap.get("resolution_line")] == 'fixed';

        return list(filter(basedAndProject, self.datas))

    def getDatasWithLifeTime(self, projName, fixed_or_unfixed='all'):
        data = []
        fixed_name = 'fixed-' + projName + '.csv'
        unfixed_name = 'unfixed-' + projName + '.csv'
        data_dir = data_base + projName + "/"
        if os.path.exists(data_dir + fixed_name) and (fixed_or_unfixed == 'fixed' or fixed_or_unfixed == 'all'):
            data = self.f.get_data_from_file(fixed_name, data_dir)[1:]
        if os.path.exists(data_dir + unfixed_name) and (fixed_or_unfixed == 'unfixed' or fixed_or_unfixed == 'all'):
            data += self.f.get_data_from_file(unfixed_name, data_dir)[1:]
        for i in range(len(data)):
            data[i][fileMap.get('life_time_line')] = int(data[i][fileMap.get('life_time_line')])
        return data

    def findFieldGroupCounts(self, projName: str, base: str):
        data = {}
        for i in self.datas:
            if i[fileMap.get("resolution_line")] == 'fixed':
                data[i[fileMap.get(base + "_line")]] = data.get(i[fileMap.get(base + "_line")], 0) + 1
        res = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
        x_datas = []
        y_datas = []
        for i in res:
            x_datas.append(i[0])
            y_datas.append(i[1])
        return x_datas, y_datas

    def getTPMedian(self, projName: str):
        datas = self.getDatasWithLifeTime(projName, 'fixed')
        TPdatas = [i[fileMap.get("life_time_line")] for i in datas]
        return np.median(TPdatas, axis=0)

    def getRandomDatas(self, isFixed='', nums: int = 20):
        datas = self.getDatasWithLifeTime(projName, isFixed)
        return random.sample(datas, nums)


if __name__ == "__main__":
    fileConnector = FileConnector()
    # x_data, y_datas = fileConnector.findFieldGroupCounts(projName, 'vtype')
    # for i in range(len(x_data)):
    #     print(x_data[i] + " " + str(y_datas[i]))
    print(fileConnector.getTPMedian(projName))
