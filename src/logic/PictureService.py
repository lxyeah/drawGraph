from src.const.Const import data_dir, metrics_headers, start_loc, projName, fileMap, base_dir
from src.logic.DataProcess import DataProcess
from src.logic.MetricsProcess import MetricsProcess
from src.logic.ShowDataUseGraph import ShowDataUseGraph
from src.tools.MathTool import MathTool


class PictureService:
    def __init__(self, projname):
        self.basePath = base_dir + "resource/datas/" + projname + "/"
        self.sdug = ShowDataUseGraph(projname)
        self.mathTool = MathTool()
        self.dataProcess = DataProcess()
        return

    def get_pic(self, projName):
        print("process : picture draw started")
        self.sdug.OneChangedInTimeOrder(projName, "category", self.basePath + "/category/")
        self.sdug.OneChangedInTimeOrder(projName, "vtype", self.basePath + "/vtype/")
        self.sdug.OneChangedInTimeOrder(projName, "category", self.basePath + "/category/", True)
        self.sdug.OneChangedInTimeOrder(projName, "vtype", self.basePath + "/vtype/", True)
        self.sdug.fileAndSumBasedGraphFromFile(projName, "vtype", self.basePath + "/vtype/")
        self.sdug.fileAndSumBasedGraphFromFile(projName, "file", self.basePath + "/file/")
        self.sdug.fileAndSumBasedGraph(projName, "category", self.basePath + "/category/")
        self.sdug.fileAndSumBasedGraph(projName, "field", self.basePath + "/field/")
        self.sdug.fileAndSumBasedGraph(projName, "method", self.basePath + "/method/")
        self.sdug.fileAndSumBasedGraph(projName, "rank", self.basePath + "/rank/")
        self.sdug.fileAndSumBasedGraph(projName, "priority", self.basePath + "/priority/")
        self.sdug.fileAndBasedBarGraph(projName, "rank", self.basePath + "/rank/")
        self.sdug.fileAndBasedBarGraph(projName, "priority", self.basePath + "/priority/")

    def get_metrics_pic(self, projName: str, metricsprocess):
        targets = ['Cyclomatic', 'CountLine']
        self.sdug.mutilDatasInOneGraph(projName, targets, "file", self.basePath + "/metrics/", metricsprocess)
        self.sdug.mutilDatasInOneGraph(projName, targets, "method", self.basePath + "/metrics/", metricsprocess)


if __name__ == "__main__":
    p = PictureService()
    p.get_metrics_pic(projName)
