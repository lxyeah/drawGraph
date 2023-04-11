from src.const.Const import fileMap, init_file_headers, repo_dir, projName, marked_based, repo_base, data_base
from src.dao.FileConnector import FileConnector
from src.logic.CollectDatas import CollectDatas
from src.logic.DataProcess import DataProcess
from src.tools.FileTool import FileTool
from src.tools.GitTool import GitClass
from src.tools.MathTool import MathTool


class LifeTimeService:
    def __init__(self, projname=projName):
        self.fileConnector = FileConnector(projname)
        self.mathTool = MathTool()
        self.ft = FileTool()
        self.gt = GitClass(repo_base + projname + "/")
        self.dataProcess = DataProcess()
        self.headers = ['', 'fixed max', 'fixed min', 'fixed average', 'fixed median', 'fixed-cnt',
                        "unfixed max", 'unfixed min', 'unfixed average', 'unfixed median', "unfixed-cnt"]
        return

    def add_lifeTime(self, init_datas, projName, isFixed=True, needSave=True):
        datas = []
        c = CollectDatas()
        for i in init_datas:
            root_id = i[fileMap.get("rootId_line")]
            leaf_id = i[fileMap.get('buggy_line')]
            print(projName + " analyse lifetime process: " + str(init_datas.index(i)) + " / " + str(len(init_datas)))
            if i[fileMap.get("resolution_line")] == 'fixed':
                leaf_id = i[fileMap.get("leafId_line")]
            life_time = c.getLifeCycle(repo_base + projName + "/", root_id, leaf_id)
            if life_time == -1:
                continue
            i.append(life_time)
            datas.append(i)
        if not needSave:
            return datas
        elif isFixed:
            self.ft.save_to_file("fixed-" + projName, init_file_headers + ["life time"], datas)
        else:
            self.ft.save_to_file("unfixed-" + projName, init_file_headers + ["life time"], datas)
        return datas

    # 获取分析数据主流程
    def get_analysis_data(self, projName: str):
        datas = self.fileConnector.findByFixedAndProject(projName)
        datas = self.add_lifeTime(datas, projName)
        unfixed_datas = self.fileConnector.findByUnfixedAndProject(projName)
        unfixed_datas = self.add_lifeTime(unfixed_datas, projName, False)
        self.saveAllFile(projName, datas, unfixed_datas)

    def saveFile(self, proj_name, datas, unfixed_datas, type, idx):
        fixed_datas = self.mathTool.get_summary_datas(datas, idx)
        unfixed_sumdatas = self.mathTool.get_sum_datas(unfixed_datas, idx)
        ndatas = fixed_datas.merge(unfixed_sumdatas, "outer", left_index=True, right_index=True)
        headers, ndatas = self.ft.dataFrame2list(ndatas)
        self.ft.save_to_file("/" + type + "/" + proj_name, self.headers, ndatas)

    # 不同base分组下的tp和fp的最大值最小值中值平均值
    def saveMutiDataFile(self, proj_name, datas, unfixed_datas, type, idx1, idx2):
        fixed_datas = self.mathTool.get_mutisummary_datas(datas, idx1, idx2)
        unfixed_sumdatas = self.mathTool.get_mutisummary_datas(unfixed_datas, idx1, idx2)
        alldatas = [['all category', 'all vtype'] + self.mathTool.get_all_mutisummary_datas(
            datas) + self.mathTool.get_all_mutisummary_datas(unfixed_datas)]
        init_datas = fixed_datas.merge(unfixed_sumdatas, "outer", left_index=True, right_index=True)
        headers, ndatas = self.ft.dataFrame2ListMutilRow(init_datas)
        ndatas = alldatas + ndatas
        self.ft.save_to_file("/" + type + "/" + proj_name + " tp-fp max min average median",
                             [""] + self.headers, ndatas)

    def saveAllFile(self, proj_name, datas, unfix_datas):
        # self.saveFile(proj_name, datas, unfix_datas, "category", fileMap.get("category_line"))
        # self.saveMutiDataFile(proj_name, datas, unfix_datas, "vtype", fileMap.get("category_line"),
        #                       fileMap.get("vtype_line"))
        # self.saveFile(proj_name, datas, unfix_datas, "priority", fileMap.get("priority_line"))
        # self.saveFile(proj_name, datas, unfix_datas, "rank", fileMap.get("rank_line"))
        # self.saveFile(proj_name, datas, unfix_datas, "file", fileMap.get("file_line"))
        # self.saveFile(proj_name, datas, unfix_datas, "field", fileMap.get("field_line"))
        # self.saveFile(proj_name, datas, unfix_datas, "method", fileMap.get("method_line"))
        # self.saveFileTPFPNums(proj_name, 'file')
        # self.saveFileTPFPNums(proj_name, 'method')
        # self.saveGroupByNums(proj_name, 'vtype')
        self.getLifeTimeDatas(projName, ['vtype', 'category'])

    def getAndSaveSpearManDatas(self, proj_name):
        datas = self.fileConnector.findByFixedAndProject(proj_name)
        datas = self.add_lifeTime(datas, proj_name, True, False)
        tmp_datas = [[int(i[fileMap.get("priority_line")]), int(i[fileMap.get("rank_line")]),
                      i[fileMap.get("life_time_line")]] for i in datas]
        ndatas = self.dataProcess.get_spearMan_datas(tmp_datas)
        map = {0: "priority", 1: "rank", 2: "life time"}
        headers, ndatas = self.ft.dataFrame2list(ndatas, map)
        self.ft.save_to_file("/spearman/" + proj_name + "-spearMan", headers, ndatas)

    # 保存不同based TP——FP数量
    def saveFileTPFPNums(self, projName: str, based: str):
        datas = self.fileConnector.findByProject(projName)
        headers, res = self.dataProcess.get_TPFP_nums_groupBy_file(datas, based)
        self.ft.save_to_file(based + '/' + projName + "-TPFP_nums", headers, res)

    # 获取某base下分类数据并统计above和below数据
    def saveGroupByNums(self, projName: str, based: str):
        # 分析fixed数据
        headers, res = self.dataProcess.get_average_lifeTime_groupBy_based(based)
        self.ft.save_to_file(based + "/" + projName + '-fixed-average-nums', headers, res)
        # 分析unfixed数据
        headers, res = self.dataProcess.get_average_lifeTime_groupBy_based(based, 'unfixed')
        self.ft.save_to_file(based + "/" + projName + '-unfixed-average-nums', headers, res)

    # 获取base下lifetime的平均值、中值以及tp的比例
    def getLifeTimeDatas(self, projName, based_list):
        print('process: average-median-density.csv write finished')

        datas = self.fileConnector.getDatasWithLifeTime(projName)
        res_headers = init_file_headers + ['life_time']
        for based in based_list:
            headers, res, data_map = self.dataProcess.average_medium_density_lifeTime(based)
            self.ft.save_to_file(based + "/average-median-density", headers, res)
            res_headers, datas = self.getTPFPDatasByMedian(datas, res_headers, projName, data_map, based,
                                                           (headers.index(marked_based) - 1))
        self.getTPFPDatasByAllTpMedian(datas, res_headers, projName)

    def getTPFPDatasByMedian(self, datas, headers, projName: str, data_map: map, based: str, compare_based):
        headers.append("mark-" + based)
        for i in datas:
            try:
                if i[fileMap.get("resolution_line")] == 'fixed':
                    i.append('TP')
                elif i[fileMap.get("life_time_line")] >= data_map[i[fileMap.get(based + "_line")]][compare_based]:
                    i.append("FP")
                else:
                    i.append("UNKNOWN")
            except (IndexError, KeyError):
                i.append('UNKNOWN')
        self.ft.save_to_file(based + "/marked datas", headers, datas)
        print('process: FP marked finished by ' + based)
        return headers, datas

    def getTPFPDatasByAllTpMedian(self, datas, headers, projName: str):
        median = self.fileConnector.getTPMedian(projName)
        headers.append('mark-all')
        res = []
        for i in datas:
            try:
                if i[fileMap.get("resolution_line")] == 'fixed':
                    res.append(i + ['TP'])
                elif i[fileMap.get("life_time_line")] >= median:
                    res.append(i + ["FP"])
                else:
                    res.append(i + ["UNKNOWN"])
            except (IndexError, KeyError):
                res.append(i + ['UNKNOWN'])
        self.ft.save_to_file("/marked datas", headers, res)
        print('process: FP marked by all fixed median finished. median = ' + str(median))
        return headers, res

    # 随机选择n个数据导出成表格
    def getRandonFPDatas(self):
        datas = self.fileConnector.getRandomDatas('unfixed')
        self.ft.save_to_file('unfixed needed marked datas', init_file_headers + ['life time'], datas)
        print('process: FP needed marked data random get finished')

    # 获取训练数据
    def getLearningData(self, projname=projName):
        metrics_datas = self.ft.get_data_from_file('combine res.csv', data_base + projname + "/metrics/")
        marked_datas = self.ft.get_data_from_file('marked datas.csv', data_base + projname + "/")
        res = []
        commit_list = []
        for i in range(1, len(metrics_datas)):
            j = 0
            while j < len(marked_datas) and metrics_datas[i][:len(init_file_headers)-1] != \
                    marked_datas[j][:len(init_file_headers)-1]:
                j += 1
            if j < len(marked_datas) and metrics_datas[i][:len(init_file_headers)-1] == marked_datas[j][
                                                                                      :len(init_file_headers)-1]:
                res.append(marked_datas[j] + metrics_datas[i][len(init_file_headers):])
                commit_list.append(marked_datas[j][5])
        commit_list = list(set(commit_list))
        time_order = self.gt.get_commit_orderBy_time(commit_list)
        res = sorted(res, key=lambda x: time_order[x[5]])
        train_res = res[:int(len(res) / 2)]
        test_res = res[int(len(res) / 2):]
        self.ft.save_next_file('train_res', marked_datas[0] + metrics_datas[0][len(init_file_headers):], train_res,
                               projname)
        self.ft.save_next_file('test_res', marked_datas[0] + metrics_datas[0][len(init_file_headers):], test_res,
                               projname)


if __name__ == "__main__":
    f = LifeTimeService()
    proj_name = projName
    f.getLearningData()
    # f.getRandonFPDatas()
    # f.get_analysis_data(proj_name)
    # f.getLifeTimeDatas(proj_name, 'vtype')
    # f.saveFileTPFPNums(proj_name, 'file')
    # f.saveFileTPFPNums(proj_name, 'method')
    # f.getLifeTimeDatas(proj_name, ['vtype', 'category'])
    # f.getAndSaveSpearManDatas(proj_name)
