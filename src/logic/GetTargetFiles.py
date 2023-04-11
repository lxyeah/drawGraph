from src.const.Const import projList, fileMap, repo_base, init_file_headers
from src.logic.CollectDatas import CollectDatas
from src.logic.LifeTimeService import LifeTimeService
from src.logic.MetricsProcess import MetricsProcess


class GetTargetFiles:
    def __init__(self):
        self.l = LifeTimeService()
        return

    def get_all_join_res(self):
        for projname in projList:
            m = MetricsProcess(projname)
            nHeaders = init_file_headers + ['life_time']
            m.spotBugsDatas = self.add_lifeTime(m.spotBugsDatas, projname)
            headers, m.spotBugsDatas = self.getTPFPDatasByAllTpMedian(m.spotBugsDatas, nHeaders, projname)
            m.left_combine_metrics_spotBugs(headers)

    def add_lifeTime(self, init_datas, projName):
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
        return datas

    def getTPFPDatasByAllTpMedian(self, datas, headers, projName: str):
        median = self.l.fileConnector.getTPMedian(projName)
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
        return headers, res


if __name__ == '__main__':
    g = GetTargetFiles()
    g.get_all_join_res()
