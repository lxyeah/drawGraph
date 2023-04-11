import numpy as np
import pandas as pd

from src.const.Const import fileMap


class MathTool:
    def __init__(self):
        return

    def getAverage(self, datas: list, idx: int):
        res = 0
        for i in datas:
            try:
                res += i[idx]
            except Exception:
                continue
        return res / len(datas)

    def getMax(self, datas: list, idx: int):
        res = datas[0][idx];
        for i in datas:
            try:
                res = max(res, i[idx])
            except Exception:
                continue
        return res;

    def getMin(self, datas: list, idx: int):
        res = datas[0][idx];
        for i in datas:
            try:
                res = min(res, i[idx])
            except Exception:
                continue
        return res;

    def get_sum_datas(self, init_datas: list, idx: int) -> pd.DataFrame:
        df = pd.DataFrame(init_datas)
        df = df.iloc[:, [idx, 9]]
        datas = df.groupby(idx).count()
        return datas

    def get_mutisum_datas(self, init_datas: list, idx1: int, idx2) -> pd.DataFrame:
        df = pd.DataFrame(init_datas)
        df = df.iloc[:, [idx1, idx2, fileMap.get("file_line")]]
        datas = df.groupby([idx1, idx2]).count()
        return datas

    def get_summary_datas(self, init_datas: list, idx: int) -> pd.DataFrame:
        df = pd.DataFrame(init_datas)
        tmp = df.iloc[:, [idx, fileMap.get("life_time_line")]]
        datas = tmp.groupby(idx).agg([np.max, np.min, np.mean, np.median, np.count_nonzero])
        return datas

    def get_mutisummary_datas(self, init_datas, idx1, idx2) -> pd.DataFrame:
        df = pd.DataFrame(init_datas)
        tmp = df.iloc[:, [idx1, idx2, fileMap.get("life_time_line")]]
        datas = tmp.groupby([idx1, idx2]).agg([np.max, np.min, np.mean, np.median, np.count_nonzero])
        return datas

    def get_all_mutisummary_datas(self, init_datas) -> pd.DataFrame:
        lifeTime = [i[fileMap.get("life_time_line")] for i in init_datas]
        return [np.max(lifeTime), np.min(lifeTime), np.mean(lifeTime), np.median(lifeTime), np.count_nonzero(lifeTime)]

    def get_groupby_sort_data(self, init_datas, idx1, idx2=0) -> pd.DataFrame:
        if len(init_datas) == 0:
            return 0
        if idx1 == idx2:
            idx2 = 1
        df = pd.DataFrame(init_datas)
        tmp = df.iloc[:, [idx1, idx2]]
        datas = tmp.groupby(idx1).agg(np.count_nonzero).apply(lambda x: x.sort_values(0, ascending=False))
        return datas

    def get_groupby_average_data(self, init_datas, idx1, idx2=0) -> pd.DataFrame:
        df = pd.DataFrame(init_datas)
        tmp = df.iloc[:, [idx1, idx2]]
        datas = tmp.loc[tmp[idx2] >= 0].groupby(idx1)[idx2].mean()
        return datas

    def get_all_average_data(self, datas, idx1, idx2=0) -> pd.DataFrame:
        df = pd.DataFrame(datas)
        tmp = df.iloc[:, [idx1, idx2]]
        data = tmp.mean()
        return data

    def get_spearMan_data(self, datas):
        spear_man_data = pd.DataFrame(datas).corr(method="spearman")
        # print(spear_man_data)
        return spear_man_data

    # metrics分组获得平均值
    def get_nums_groupBy_based(self, datas: list, based: int, target: int) -> pd.DataFrame:
        df = pd.DataFrame(datas[1:])
        x_datas = df.loc[df[target] >= 0].groupby(based)[target].mean()
        return x_datas

    # lifeTime分组获得平均值
    def get_average_groupBy_based(self, datas: list, based: int, target: int, type="") -> pd.DataFrame:
        df = pd.DataFrame(datas)
        x_datas = df.loc[(type == df[fileMap.get("resolution_line")])].groupby(based)[target].mean()
        return x_datas

    # lifeTime分组获取中值
    def get_medium_groupBy_based(self, datas: list, base: int, target: int, type="") -> int:
        df = pd.DataFrame(datas)
        data = df.loc[(type == df[fileMap.get("resolution_line")])].groupby(base)[target].median()
        return data

    # 获取组内占比
    def get_density_groupby_based(self, datas: list, base1: int, base2: int) -> pd.DataFrame:
        df = pd.DataFrame(datas)
        fix_data = df.loc[df[fileMap.get("resolution_line")] == 'fixed'].groupby(base1)[base2].count()
        unfix_data = df.loc[df[fileMap.get("resolution_line")] == 'unfixed'].groupby(base1)[base2].count()
        return fix_data, unfix_data

    def get_add_percent_value(self, datas: list):
        y_datas = []
        x_datas = []
        sums = sum(datas)
        tmp = 0
        idx = 1
        for i in datas:
            tmp += i
            x_datas.append(idx / len(datas))
            idx += 1
            y_datas.append(tmp / sums)
        return x_datas, y_datas

    # 归一化处理
    def my_fit_transform(self, datas: list) -> list:
        sums = sum(datas)
        if sums == 0:
            return datas
        res = []
        for i in datas:
            res.append(i / sums)
        return res

    # 分组获取各类型数量
    def get_groupNums_by_base(self, datas: list, based: list, cnt_line=0) -> pd.DataFrame:
        df = pd.DataFrame(datas)
        tmp = df.iloc[:, based + [cnt_line]]
        res = tmp.groupby(based).count()
        # print(res)
        return res

    # 获取有多少种
    def get_groupSum_by_base(self, datas: list, based: list) -> pd.DataFrame:
        df = pd.DataFrame(datas)
        tmp = df[based]
        res = len(tmp.value_counts().index)
        # print(res)
        return res

    def get_certainValue_above_datas(self, datas: list, based_line: str, based_value: str, target_line,
                                     target_value: int) -> int:
        df = pd.DataFrame(datas)
        tmp = df.iloc[:, [based_line, target_line]]
        data = tmp.loc[(tmp[based_line] == based_value) & (tmp[target_line] >= target_value)].count()
        return data

    def get_certainValue_below_datas(self, datas: list, based_line: str, based_value: str, target_line,
                                     target_value: int) -> int:
        df = pd.DataFrame(datas)
        tmp = df.iloc[:, [based_line, target_line]]
        data = tmp.loc[(tmp[based_line] == based_value) & (tmp[target_line] < target_value)].count()
        return data

    def get_all_above_value(self, datas: list, based_line, target_line,
                            target_value: int) -> int:
        df = pd.DataFrame(datas)
        tmp = df.iloc[:, [based_line, target_line]]
        data = tmp.loc[tmp[target_line] >= target_value].count()
        return data

    def get_all_below_value(self, datas: list, based_line, target_line,
                            target_value: int) -> int:
        df = pd.DataFrame(datas)
        tmp = df.iloc[:, [based_line, target_line]]
        data = tmp.loc[tmp[target_line] < target_value].count()
        return data

    # 根据based分组并获取对应的target列表
    def get_list_groupby_based(self, datas: list, based_line, target_line):
        res = {}
        for i in datas:
            if i[fileMap.get(based_line + "_line")] in res.keys():
                list = res.get(i[fileMap.get(based_line + "_line")])
                list.append(int(i[fileMap.get(target_line + "_line")]))
                res[i[fileMap.get(based_line + "_line")]] = list
            else:
                res[i[fileMap.get(based_line + "_line")]] = [int(i[fileMap.get(target_line + "_line")])]
        return res
