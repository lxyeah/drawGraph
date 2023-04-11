from src.const.Const import data_dir, fileMap, projName
from src.tools.FileTool import FileTool


class BugFile():
    def __init__(self):
        self.ft = FileTool()
        return

    def getTPpercent(self, based, line=-1):
        datas = self.ft.get_data_from_file('marked datas.csv', data_dir)
        tpmap = {}
        fpmap = {}
        for i in datas:
            if i[line] == 'TP':
                tpmap[i[fileMap.get(based + '_line')]] = tpmap.get(i[fileMap.get(based + '_line')], 0) + 1
            elif i[line] == 'FP':
                fpmap[i[fileMap.get(based + '_line')]] = fpmap.get(i[fileMap.get(based + '_line')], 0) + 1
        res = []
        for key in list(set(list(tpmap.keys()) + list(fpmap.keys()))):
            res.append([key, tpmap.get(key, 0), fpmap.get(key, 0),
                        tpmap.get(key, 0) / (fpmap.get(key, 0) + tpmap.get(key, 0))])
        self.ft.save_to_file(based+'/tp percent in ' + based, [based, 'tp num', 'fp num', 'percent'], res)
        print(projName+" has finish")



if __name__ == '__main__':
    b = BugFile()
    b.getTPpercent('vtype')
