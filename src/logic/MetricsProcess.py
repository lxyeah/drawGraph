import functools

from src.const.Const import projName, fileMap, metricsMap, metrics_headers, init_file_headers, data_dir
from src.dao.FileConnector import FileConnector
from src.dao.MetricsDao import MetricsDao
from src.tools.FileTool import FileTool
from src.tools.ListTool import metrics_order
from src.tools.MathTool import MathTool


class MetricsProcess:
    def __init__(self, projName: str, need_init=True):
        self.mathTool = MathTool()
        self.projName = projName
        self.filetool = FileTool()
        self.combineDatas = []
        if need_init:
            metricsDao = MetricsDao(projName)
            self.metricsDatas = metricsDao.datas
            spotBugsDao = FileConnector(projName)
            self.spotBugsDatas = spotBugsDao.datas

    def get_data_from_file(self, file_dir=data_dir):
        if len(self.combineDatas) > 0:
            return self.combineDatas
        tmp = self.filetool.get_data_from_file("/metrics/combine res.csv", file_dir)
        for i in tmp:
            now = []
            for j in i:
                if self.filetool.isfloat(j):
                    now.append(float(j))
                else:
                    now.append(j)
            self.combineDatas.append(now)
        return self.combineDatas

    def combine_metrics_spotBugs(self):
        print("start combine metrics and spotBugs res")
        datas = []
        for i in self.spotBugsDatas:
            fileName = i[fileMap.get("file_line")].split("/")[-1]
            metricsData = self.metricsDatas.get(i[fileMap.get("rootId_line")])
            if metricsData is None:
                continue
            metricsData = sorted(metricsData, key=functools.cmp_to_key(metrics_order))
            for j in metricsData:
                # print(j[metricsMap.get("fileName")] + " " + fileName)
                metricsKind = j[metricsMap.get("kind")]
                metricsFileName = j[metricsMap.get("fileName")]

                if "Method" in metricsKind and \
                        i[fileMap.get("method_line")].split("(")[0] in metricsFileName.split(".")[-1]:
                    now = i + j
                    datas.append(now)
                    break
                elif metricsKind.split(" ")[-1] == "Constructor" and \
                        metricsFileName.split(".")[-1] == fileName.split(".java")[0].split("/")[-1]:
                    now = i + j
                    datas.append(now)
                    break
                elif metricsKind.split(" ")[-1] == "Class" and \
                        metricsFileName.split(".")[-1] == fileName.split(".java")[0].split("/")[-1]:
                    now = i + j
                    datas.append(now)
                    break
                elif metricsKind == "File" and (fileName != '' and fileName in metricsFileName):
                    now = i + j
                    datas.append(now)
                    break
        self.filetool.save_to_file("/metrics/combine res", init_file_headers + metrics_headers, datas,self.projName)
        print('/metrics/combine res.csv write finished')
        return datas

    def left_combine_metrics_spotBugs(self, init_headers=init_file_headers):
        print("start combine metrics and spotBugs res")
        datas = []
        for i in self.spotBugsDatas:
            fileName = i[fileMap.get("file_line")].split("/")[-1]
            metricsData = self.metricsDatas.get(i[fileMap.get("rootId_line")])
            if metricsData is None:
                datas.append(i)
                continue
            metricsData = sorted(metricsData, key=functools.cmp_to_key(metrics_order))
            for j in metricsData:
                # print(j[metricsMap.get("fileName")] + " " + fileName)
                metricsKind = j[metricsMap.get("kind")]
                metricsFileName = j[metricsMap.get("fileName")]

                if "Method" in metricsKind and \
                        i[fileMap.get("method_line")].split("(")[0] in metricsFileName.split(".")[-1]:
                    now = i + j
                    break
                elif metricsKind.split(" ")[-1] == "Constructor" and \
                        metricsFileName.split(".")[-1] == fileName.split(".java")[0].split("/")[-1]:
                    now = i + j
                    break
                elif metricsKind.split(" ")[-1] == "Class" and \
                        metricsFileName.split(".")[-1] == fileName.split(".java")[0].split("/")[-1]:
                    now = i + j
                    break
                elif metricsKind == "File" and (fileName != '' and fileName in metricsFileName):
                    now = i + j
                    break
            datas.append(now)
        self.filetool.save_to_target_file(self.projName + "/metrics/" + self.projName + " left join res",
                                          init_headers + metrics_headers,
                                          datas)
        print('/metrics/' + self.projName + ' left join res.csv write finished')
        return datas

    # 获得metrics平均值
    def get_average_value(self, datas):
        res = []
        now_datas = []
        for line_num in range(metricsMap.get("startNums") + 1, len(metrics_headers)):
            now_datas = self.mathTool.get_groupby_average_data(datas, fileMap.get("resolution_line"),
                                                               fileMap.get("resolution_line") + 1 + line_num)
            tmp_datas = self.mathTool.my_fit_transform(now_datas.values.tolist())
            res.append([metrics_headers[line_num]] + tmp_datas)
        headers = [""] + now_datas.index.tolist()
        # headers[1] = "unfixed"
        print("/metrics/summary_datas.csv write finished")
        self.filetool.save_to_file("/metrics/summary_datas", headers, res)


if __name__ == "__main__":
    m = MetricsProcess(projName)
    datas = m.combine_metrics_spotBugs()
    m.get_average_value(datas)
