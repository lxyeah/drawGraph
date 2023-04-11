from src.const.Const import metrics_headers, fileMap, start_loc, projName, resolution_type, marked_baesd_datas_headers
from src.dao.FileConnector import FileConnector
from src.logic.CollectDatas import CollectDatas
from src.tools.ListTool import map2list
from src.tools.MapTool import add_value_to_map, add_percent_value_to_map
from src.tools.MathTool import MathTool


class DataProcess:
    def __init__(self, skip=False):
        self.mathTool = MathTool()
        self.dao = FileConnector(skip=skip)
        self.collectDatas = CollectDatas()

    def get_spearMan_datas(self, datas: list):
        spearMan_data = self.mathTool.get_spearMan_data(datas)
        # print(spearMan_data)
        print("spear man calculate finish !")
        return spearMan_data

    def get_mutil_percent_datas(self, datas: list, targets: list, based: str, sort_based_list=None) -> list:
        y_datas_list = []
        x_datas_list = []
        titles = []
        for i in targets:
            if i in metrics_headers:
                # tmp = [j[metrics_headers.index(i) + start_loc] for j in datas]
                # 获取根据base分类的分类数据
                tmp = self.mathTool.get_nums_groupBy_based(datas, fileMap.get(based + "_line"),
                                                           metrics_headers.index(i) + start_loc)
                y_datas = tmp.values.tolist()
                x_datas = tmp.index.tolist()

                # 根据fixed数量排序
                if sort_based_list is not None:
                    tmp_y_datas = y_datas
                    y_datas = []
                    for s in sort_based_list:
                        for tmp in x_datas:
                            if tmp == s:
                                y_datas.append(tmp_y_datas[x_datas.index(tmp)])

                titles.append(i)
                # 获取归一化的百分比数据
                x_datas, y_datas = self.mathTool.get_add_percent_value(y_datas)
                x_datas_list.append(x_datas)
                y_datas_list.append(y_datas)
        return titles, x_datas_list, y_datas_list

    # 统计同一base下正误报数量
    def get_TPFP_nums_groupBy_file(self, datas: list, based: str) -> list:
        datas = self.dao.datas
        tmp_df = self.mathTool.get_groupNums_by_base(datas,
                                                     [fileMap.get(based + "_line"), fileMap.get("resolution_line")])
        headers = [based] + resolution_type
        res = self.collectDatas.get_list_from_groupBy_nums(tmp_df, resolution_type)
        return headers, res

    # 统计base下tp和fp的lifetime的平均值以及的数据
    def get_average_lifeTime_groupBy_based(self, based: str, isfixed="fixed") -> list:
        datas = self.dao.getDatasWithLifeTime(projName, isfixed)
        headers = [based, "average", 'above_average', 'below_average']
        tmp_df = self.mathTool.get_groupby_average_data(datas, fileMap.get(based + "_line"),
                                                        fileMap.get("life_time_line"))
        res = []
        # 获取全部数据
        all_averages = self.mathTool.get_all_average_data(datas, fileMap.get(based + "_line"),
                                                          fileMap.get("life_time_line"))
        res.append(['all', all_averages.values[0],
                    self.mathTool.get_all_above_value(datas, fileMap.get(based + "_line"),
                                                      fileMap.get("life_time_line"), all_averages.values[0]).values[0],
                    self.mathTool.get_all_below_value(datas, fileMap.get(based + "_line"),
                                                      fileMap.get("life_time_line"), all_averages.values[0]).values[0]])
        # 获取分类的数据
        for i in range(len(tmp_df.index)):
            now = [tmp_df.index[i], tmp_df.values[i],
                   self.mathTool.get_certainValue_above_datas(datas, fileMap.get(based + "_line"), tmp_df.index[i],
                                                              fileMap.get("life_time_line"), tmp_df.values[i])
                       .values[0],
                   self.mathTool.get_certainValue_below_datas(datas, fileMap.get(based + "_line"), tmp_df.index[i],
                                                              fileMap.get("life_time_line"), tmp_df.values[i])
                       .values[0]]
            res.append(now)
        return headers, res

    # 获取根据base分类的lifeTime的平均值、中值以及密度
    def average_medium_density_lifeTime(self, based: int) -> list:
        datas = self.dao.getDatasWithLifeTime(projName)
        # print(datas[0])
        headers = [based] + marked_baesd_datas_headers
        map = {}
        averages = self.mathTool.get_average_groupBy_based(datas, fileMap.get(based + "_line"),
                                                           fileMap.get("life_time_line"), 'fixed')
        medium = self.mathTool.get_medium_groupBy_based(datas, fileMap.get(based + "_line"),
                                                        fileMap.get("life_time_line"), 'fixed')
        fix_count, unfix_count = self.mathTool.get_density_groupby_based(datas, fileMap.get(based + "_line"),
                                                                         fileMap.get("resolution_line"))

        add_value_to_map(map, averages)
        add_value_to_map(map, medium)
        add_percent_value_to_map(map, fix_count, unfix_count)
        # print(map)
        # print(averages)
        list = map2list(map)
        return headers, list, map


if __name__ == '__main__':
    d = DataProcess()
    res = d.average_medium_density_lifeTime('vtype')
