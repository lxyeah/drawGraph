import numpy as np

from src.const.Const import fileMap, projList, summary_dir, base_dir
from src.dao.AllFileConnector import AllFileConnector
from src.logic.CollectDatas import CollectDatas
from src.logic.DataProcess import DataProcess
from src.tools.FileTool import FileTool
from src.tools.MathTool import MathTool
from src.tools.drawGraph import DrawGraph
from src.logic.MetricsProcess import MetricsProcess
import warnings

warnings.filterwarnings('ignore')


# 汇总的各种操作
class SummaryProcess:
    def __init__(self):
        self.fileConnector = AllFileConnector()
        self.drawGraph = DrawGraph()
        self.collectdata = CollectDatas()
        self.mathTool = MathTool()
        self.dataProcess = DataProcess(True)
        self.ft = FileTool()

    def main_process(self):
        self.fileAndSumBasedGraphFromFile('category', summary_dir, projList, '% of category containing actionable warnings', '% of actionable warnings')
        # self.fileAndSumBasedGraphFromFile('vtype', summary_dir, projList, '% of type containing actionable warnings', '% of actionable warnings')
        # self.fileAndSumBasedGraphFromFile('file', summary_dir, projList, '% of file containing actionable warnings', '% of actionable warnings')
        # self.fileAndSumBasedGraphFromFile('method', summary_dir, projList, '% of method containing actionable warnings', '% of actionable warnings')
        # self.fileAndBasedBarGraphFromFile('priority', summary_dir, projList, 'Priority level', '# of actionable warnings')
        # self.fileAndSumBasedGraphFromFile('rank', summary_dir, projList, '% of rank containing actionable warnings', '% of actionable warnings')
        # self.get_top1_category_graph('category', summary_dir)
        # self.get_top3_tyoes("category", summary_dir)
        # self.get_top1_vtype_graph('vtype', summary_dir)
        # self.get_top3_tyoes("vtype", summary_dir)

        # targets = ['Cyclomatic', 'CountLine']
        # self.mutilDatasInOneGraph(targets, 'file', summary_dir)
        # self.mutilDatasInOneGraph(targets, 'method', summary_dir)

        # self.mutilResTypeNums('file', summary_dir)
        # self.mutilResTypeNums('method', summary_dir)

        # self.getFixedNumsGroupByBased("rank", summary_dir)
        # self.getFixedNumsGroupByBased("priority", summary_dir)

    def fileAndBasedBarGraphFromFile(self, based: str, save_path, projList, x_label, y_label):
        y_datas_list = {}
        x_int_datas = ['1', '2', '3']
        for projname in projList:
            datas = self.fileConnector.findByFixedAndProject(projname)
            datas = self.mathTool.get_groupby_sort_data(datas, fileMap.get(based + "_line"))
            x_datas = datas.index.tolist()
            y_data = datas.values.tolist()
            y_int_datas = []

            for i in x_int_datas:
                y_int_datas.append(y_data[x_datas.index(i)][0])


            y_datas_list[projname] = y_int_datas
        x_int_datas = ['Priority 1', 'Priority 2', 'Priority 3']
        self.drawGraph.drawMutiBarChart(x_int_datas, y_datas_list, x_label, y_label,
                                          '', save_path + based + " percent nums")
        print(save_path + based + " mutil line chart pic download finish(from file)")

    # 所有项目根据base进行切割并且归一后的图
    def fileAndSumBasedGraphFromFile(self, based: str, save_path, projList, x_label, y_label):
        x_datas_list = {}
        y_datas_list = {}
        for projname in projList:
            datas = self.fileConnector.findByFixedAndProject(projname)
            datas = self.mathTool.get_groupby_sort_data(datas, fileMap.get(based + "_line"))
            x_datas = datas.index.tolist()
            y_data = datas.values.tolist()
            x_int_datas = []
            y_int_datas = []
            sum = 0
            y_sum = np.sum(y_data, axis=0)[0]
            for i in range(len(y_data)):
                sum += y_data[i][0]
                y_int_datas.append(sum / y_sum)
                x_int_datas.append((i + 1) / len(x_datas))
            x_datas_list[projname] = x_int_datas
            y_datas_list[projname] = y_int_datas
        self.drawGraph.drawMutilLineChart(x_datas_list, y_datas_list, x_label, y_label,
                                          '', save_path + based + " percent nums")
        print(save_path + based + " mutil line chart pic download finish(from file)")

    def fileAndSumBarGraphFromFile(self, based: str, save_path, projList, x_label, y_label):
        x_datas_list = {}
        y_datas_list = {}
        for projname in projList:
            datas = self.fileConnector.findByFixedAndProject(projname)
            datas = self.mathTool.get_groupby_sort_data(datas, fileMap.get(based + "_line"))
            x_datas = datas.index.tolist()
            y_data = datas.values.tolist()
            x_int_datas = []
            y_int_datas = []
            sum = 0
            y_sum = np.sum(y_data, axis=0)[0]
            for i in range(len(y_data)):
                sum += y_data[i][0]
                y_int_datas.append(sum / y_sum)
                x_int_datas.append((i + 1) / len(x_datas))
            x_datas_list[projname] = x_int_datas
            y_datas_list[projname] = y_int_datas
        self.drawGraph.drawMutilLineChart(x_datas_list, y_datas_list, x_label, y_label,
                                          '', save_path + based + " percent nums")
        print(save_path + based + " mutil line chart pic download finish(from file)")

    def get_top3_tyoes(self, based: str, save_path, projList=projList):
        alldatas = []
        for projName in projList:
            datas = self.fileConnector.findByFixedAndProject(projName)
            datas = self.mathTool.get_groupby_sort_data(datas, fileMap.get(based + "_line"), fileMap.get("rootId_line"))
            alldatas.append([projName, datas.index[0:3].tolist()])
        self.ft.save_datas2target_path(['projName', based], alldatas, save_path + "/" + based + " top3 datas")

    # 获取不同项目的top1随时间变化的图像，并画在一张图上
    def get_top1_graph(self, based: str, save_path, projList=projList):
        x_times_list = {}
        y_datas_list = {}
        save_datas = []
        for projname in projList:
            datas = self.fileConnector.findByFixedAndProject(projname)
            datas = self.mathTool.get_groupby_sort_data(datas, fileMap.get(based + "_line"), fileMap.get("rootId_line"))
            target_based = datas.index[0]
            datas = self.fileConnector.findBasedAndProjectAndFixed(based, target_based, projname)
            target_datas = []
            for i in datas:
                target_datas.append(
                    [i[fileMap.get(based + "_line")], i[fileMap.get("rootId_line")], i[fileMap.get("leafId_line")]])
            x_data, y_data = self.collectdata.getCommitChangeOrderByTime(target_datas, projname, True)
            x_times_list[projname] = x_data
            y_datas_list[projname] = y_data
            save_datas.append([projname, x_data, y_data])
            print([projname, x_data, y_data])
        self.drawGraph.drawMutiLineChartWithoutPeicent(x_times_list, y_datas_list, "date", "num of vulnerabilities",
                                                       based + ' top1 changed on time', save_path)
        self.ft.save_datas2target_path(['projName', 'types', 'datas'], save_datas,
                                       save_path + "/" + based + " top1 datas")
        print(based + "time change line chart pic download finish(from file)")

    def get_top1_category_graph(self, based: str, save_path):
        x_times_list = {}
        y_datas_list = {}
        save_datas = self.ft.get_data_from_file('category top1 datas.csv', save_path)[1:]
        for i in save_datas:
            x_times_list[i[0]] = eval(i[1])
            y_datas_list[i[0]] = eval(i[2])
        self.drawGraph.drawMutiLineChartWithoutPeicent(x_times_list, y_datas_list, "Date", "Num of actionable warnings",
                                                       '', save_path + '/' + based + ' top1 changed on time')

    def get_top1_vtype_graph(self, based: str, save_path):
        x_times_list = {}
        y_datas_list = {}
        save_datas = self.ft.get_data_from_file('vtype top1 datas.csv', save_path)[1:]
        for i in save_datas:
            x_times_list[i[0]] = eval(i[1])
            y_datas_list[i[0]] = eval(i[2])
        self.drawGraph.drawMutiLineChartWithoutPeicent(x_times_list, y_datas_list, "Date", "Num of actionable warnings",
                                                       '', save_path + '/' + based + ' top1 changed on time')

    # 绘制所有项目的metrics百分比图，每个metrics一个图片
    def mutilDatasInOneGraph(self, targets: list, based, save_path, projList=projList):
        # 获取根据fixed数量排序的file name list
        x_datas_dict = {}
        y_datas_dict = {}
        titles = []
        for projName in projList:
            sorted_datas = self.fileConnector.findByFixedAndProject(projName)
            sorted_datas = self.mathTool.get_groupby_sort_data(sorted_datas, fileMap.get(based + "_line"))
            sorted_based_list = sorted_datas.index.tolist()
            m = MetricsProcess(base_dir + "resource/proj/" + projName + "/", False)
            datas = m.get_data_from_file(base_dir + "resource/datas/" + projName + "/")
            tmptitles, x_datas_list, y_datas_list = self.dataProcess.get_mutil_percent_datas(datas, targets, based,
                                                                                             sorted_based_list)
            x_datas_dict[projName] = x_datas_list
            y_datas_dict[projName] = y_datas_list
            titles = tmptitles
        for i in range(len(titles)):
            x_datas_list = []
            y_datas_list = []
            for projName in projList:
                x_datas_list.append(x_datas_dict[projName][i])
                y_datas_list.append(y_datas_dict[projName][i])
            self.drawGraph.mutilDatasInOneGraph(x_datas_list, y_datas_list, projList, "% of " + based + ' containing actionable warnings',
                                                "% of " + titles[i],
                                                '', save_path + based + " with " + targets[i])
        print(based + " and complexity.png has finished")

    # 统计统一项目下，各个类型的数量
    def mutilResTypeNums(self, based, save_path, projList=projList):
        res_datas = []
        for projName in projList:
            fixed_list = self.fileConnector.findBasedAndProjectAndType(projName, ['fixed'])
            fixed_nums = self.mathTool.get_groupby_sort_data(fixed_list, fileMap.get(based + "_line"))
            unfixed_list = self.fileConnector.findBasedAndProjectAndType(projName, ['unfixed'])
            unfixed_nums = self.mathTool.get_groupby_sort_data(unfixed_list, fileMap.get(based + "_line"))
            unknown_list = self.fileConnector.findBasedAndProjectAndType(projName, ['unknown', 'disappeared'])
            unknown_nums = self.mathTool.get_groupby_sort_data(unknown_list, fileMap.get(based + "_line"))
            all_list = self.fileConnector.findBasedAndProjectAndType(projName,
                                                                     ['fixed', 'unfixed', 'unknown', 'disappeared'])
            all_nums = self.mathTool.get_groupby_sort_data(all_list, fileMap.get(based + "_line"))
            for i in all_nums.index:
                fixed_num = fixed_nums.at[i, 0] if i in fixed_nums.index.values else 0
                unfixed_num = unfixed_nums.at[i, 0] if i in unfixed_nums.index.values else 0
                if unknown_nums != 0:
                    unknown_num = unknown_nums.at[i, 0] if i in unknown_nums.index.values else 0
                else:
                    unknown_num = 0
                res_num = (fixed_num + unfixed_num) / (fixed_num + unknown_num + unfixed_num)
                res_datas.append([projName, i, fixed_num, unfixed_num, unknown_num, res_num])
        self.ft.save_datas2target_path(
            ['project', 'file', 'fixed num', 'unfixed num', 'unknown num', '(fixed+unfixed)/all'], res_datas,
            save_path + "/" + based + " warning type nums")

    # 获取根据base分组的fixed数量以及fixed的lifetime
    def getFixedNumsGroupByBased(self, based, save_path, projList=projList):
        res_datas = []
        for projName in projList:
            datas = self.ft.get_data_from_file("marked datas.csv", base_dir + "resource/datas/" + projName + "/")
            datas = self.fileConnector.findBasedAndFixed(datas, "resolution", 'fixed')
            groupRes = self.mathTool.get_list_groupby_based(datas, based, "life_time")
            for i in groupRes.keys():
                res_datas.append([projName, i, len(groupRes.get(i)), groupRes.get(i)])
        self.ft.save_datas2target_path(
            ['project', based + ' type', 'fixed num', 'fixed lifetime list'], res_datas,
            save_path + "/" + based + " with actionable datas")


if __name__ == '__main__':
    sp = SummaryProcess()
    sp.main_process()
