from src.const.Const import base_dir, metrics_base, data_base
import src.tools.cmd_tool as ct
from src.logic.LifeTimeService import LifeTimeService
from src.logic.MetricsProcess import MetricsProcess
from src.logic.PictureService import PictureService
from src.logic.SummaryProcess import SummaryProcess
from src.tools import FileTool
from src.tools.InitTool import InitTool


class ProjectService():

    def __init__(self):
        return

    @staticmethod
    def downLoadProject(projUrl):
        repoDir = base_dir + "resource/proj/"
        ct.change_path_to_target(repoDir)
        status = ct.get_run_result("git clone %s" % projUrl)
        if status != 0:
            return False
        return True

    @staticmethod
    def analyseProject(projName):
        InitTool()
        # # # 获取文件
        f = LifeTimeService()
        f.get_analysis_data(projName)
        f.getAndSaveSpearManDatas(projName)

        # # 获取图片
        # p = PictureService()
        # p.get_pic(projName)
        return True

    @staticmethod
    def summaryProject():
        sp = SummaryProcess()
        sp.main_process()

    @staticmethod
    def metricsProcess(projName, metricsFile):
        folder_path = metrics_base + projName + "/"
        metricsFile.save(metrics_base + projName + ".zip")
        unzipCommond = "unzip -o -q -d {0} {1}".format(metrics_base,
                                                       metrics_base + projName + ".zip")
        ct.run_command(unzipCommond)
        mvCommond = "mv {0} {1}".format(metrics_base + metricsFile.filename.split(".")[0], metrics_base + projName)
        ct.run_command(mvCommond)
        p = PictureService()
        m = MetricsProcess(projName)
        datas = m.combine_metrics_spotBugs()
        m.get_average_value(datas)
        p.get_metrics_pic(projName, m)

    @staticmethod
    def picProcess(projName):
        # 获取单个图片
        # p = PictureService()
        # p.get_pic(projName)
        # p.get_metrics_pic(projName, m)
        # 获取汇总图片
        sp = SummaryProcess()
        sp.main_process()

    @staticmethod
    def getProjDatas(projName):
        ft = FileTool.FileTool()
        filePath = data_base + projName + "/" + "marked datas.csv"
        datas = ft.get_data_from_file("", filePath)
        return datas[0], datas[1:]
