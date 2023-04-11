from src.const.Const import tmp_base, fileMap, projList
from src.tools.FileTool import FileTool
from src.tools.MathTool import MathTool

filetool = FileTool()
mathTool = MathTool()


# 统计文件中每种类型的数量
def getTypeNum(path, file, typeList):
    datas = filetool.get_data_from_file(file, path)
    res = []
    for i in typeList:
        tmp = mathTool.get_groupSum_by_base(datas, [fileMap.get(i + "_line")])
        res.append(str(tmp))
    return res


# 获取所有的项目信息列表
def getAllTypeNum():
    filepath = tmp_base + "/before/"
    typelist = ['category', 'vtype', 'priority', 'rank', 'file', 'method']
    print(typelist)
    for projname in projList:
        filename = projname + " left join res.csv"
        res = getTypeNum(filepath, filename, typelist)
        # print(projname + " " + str(res))
        print(projname+"  "+"&".join(res))
        print()


if __name__ == '__main__':
    getAllTypeNum()
