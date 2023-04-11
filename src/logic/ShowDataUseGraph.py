import numpy as np

from src.const.Const import fileMap, data_dir, projName
from src.dao.FileConnector import FileConnector
from src.logic.DataProcess import DataProcess
from src.logic.MetricsProcess import MetricsProcess
from src.tools.MathTool import MathTool
from src.tools.drawGraph import DrawGraph
from src.dao.Connector import Connector
from src.logic.CollectDatas import CollectDatas


class ShowDataUseGraph:
    def __init__(self, projname):
        # self.collector = Connector()
        self.fileCollector = FileConnector(projname, True)
        # 从before文件夹获取数据
        self.fileCollector.reload_datas_from_before(projname)
        # # 从after文件夹获取数据
        # self.fileCollector.reload_datas_from_after(projname)
        self.drawGraph = DrawGraph()
        self.collectdata = CollectDatas()
        self.mathTool = MathTool()
        self.dataProcess = DataProcess()
        return

    def fileAndSumBasedGraph(self, projName: str, based: str, save_path=""):
        # cursor = self.collector.findFieldGroupCounts(projName, based)
        # x_datas, y_data = self.collectdata.getGraphDatas(cursor, [based, 'cnt'])
        x_datas, y_data = self.fileCollector.findFieldGroupCounts(projName, based)
        x_int_datas = []
        sum = 0
        y_sum = np.sum(y_data, axis=0)
        for i in range(len(y_data)):
            sum += y_data[i];
            y_data[i] = sum / y_sum
            x_int_datas.append(i / len(x_datas))
        self.drawGraph.drawLineChart(x_int_datas, y_data, based + " nums", "fixed nums",
                                     "relations between " + based + " and fixedBugs", save_path)
        print(based + "line chart pic download finish (from file)")

    def fileAndBasedBarGraph(self, projName: str, based: str, save_path):
        # cursor = self.collector.findFieldGroupCounts(projName, based)
        # x_datas, y_datas = self.collectdata.getGraphDatas(cursor, [based, 'cnt'], False)
        x_datas, y_datas = self.fileCollector.findFieldGroupCounts(projName, based)
        self.drawGraph.drawBarChartWithoutPeicent(x_datas, y_datas, based + " nums", "fixed nums",
                                                  "relations between " + based + " nums and fixedBugs", save_path)
        print(based + "bar chart pic download finish (from file)")

    def fileAndBasedBarGraphFromFile(self, projName: str, based: str, save_path):
        cursor = self.filecollector.findBasedProjectCounts(projName, based)
        x_datas, y_datas = self.collectdata.getGraphDatas(cursor, [based, 'cnt'], False)
        self.drawGraph.drawBarChartWithoutPeicent(x_datas, y_datas, based + " nums", "fixed nums",
                                                  "relations between " + based + " nums and fixedBugs", save_path)
        print(based + " nums and findbugs relations bar chart pic download finished (From file)")

    def fileAndSumBasedGraphFromFile(self, projName: str, based: str, save_path=""):
        datas = self.fileCollector.findByFixedAndProject(projName)
        datas = self.mathTool.get_groupby_sort_data(datas, fileMap.get(based + "_line"))
        x_datas = datas.index.tolist()
        y_data = datas.values.tolist()
        x_int_datas = [0]
        y_int_datas = [0]
        sum = 0
        y_sum = np.sum(y_data, axis=0)[0]
        for i in range(len(y_data)):
            sum += y_data[i][0];
            y_int_datas.append(sum / y_sum)
            x_int_datas.append((i + 1) / len(x_datas))
        self.drawGraph.drawLineChart(x_int_datas, y_int_datas, based + " nums", "fixed nums",
                                     "relations between " + based + " and fixedBugs", save_path)
        print(based + "line chart pic download finish(from file)")

    # 从文件中读取并画出目标属性图
    def fileAndBasedGraphFromFile(self, projName: str, based: str, save_path):
        cursor = self.fileCollector.findFieldGroupCounts(projName, based)
        x_datas, y_datas = self.collectdata.getGraphDatas(cursor, [based, 'cnt'], False)
        self.drawGraph.drawBarChartWithoutPeicent(x_datas, y_datas, based + " nums", "fixed nums",
                                                  "relations between " + based + " nums and fixedBugs", save_path)
        print(based + " nums and findbugs relations bar chart pic download finished (From file)")

    #  显示一个属性随时间变化的图片
    def OneChangedInTimeOrder(self, projName: str, based: str, save_path, only_now=False):
        datas = self.fileCollector.findByFixedAndProject(projName)
        datas = self.mathTool.get_groupby_sort_data(datas, fileMap.get(based + "_line"), fileMap.get("rootId_line"))
        target_based = datas.index[0]
        datas = self.fileCollector.findBasedAndProjectAndFixed(based, target_based, projName)
        target_datas = []
        for i in datas:
            target_datas.append(
                [i[fileMap.get(based + "_line")], i[fileMap.get("rootId_line")], i[fileMap.get("leafId_line")]])
        x_data, y_data = self.collectdata.getCommitChangeOrderByTime(target_datas, projName, only_now)
        if only_now:
            file_name = "date and " + target_based + " nums without fixed data"
        else:
            file_name = "date and " + target_based + " nums"
        self.drawGraph.drawLineChartWithoutPeicent(x_data, y_data, "date", target_based + " nums",
                                                   file_name, save_path)
        print(file_name + "time change line chart pic download finish(from file)")

    def mutilDatasInOneGraph(self, projName: str, targets: list, based, save_path, m: MetricsProcess):
        # 获取根据fixed数量排序的file name list
        sorted_datas = self.fileCollector.findByFixedAndProject(projName)
        sorted_datas = self.mathTool.get_groupby_sort_data(sorted_datas, fileMap.get(based + "_line"))
        sorted_based_list = sorted_datas.index.tolist()

        datas = m.get_data_from_file()
        titles, x_datas_list, y_datas_list = self.dataProcess.get_mutil_percent_datas(datas, targets, based,
                                                                                      sorted_based_list)
        self.drawGraph.mutilDatasInOneGraph(x_datas_list, y_datas_list, titles, "% " + based, "% complexity",
                                            based + " and complexity", save_path)
        print(save_path + " " + based + " and complexity.png has finished")


if __name__ == "__main__":
    s = ShowDataUseGraph()
    s.OneChangedInTimeOrder(projName, "category", data_dir + "/category/")
