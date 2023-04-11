import warnings

from src.const.Const import projList
from src.logic.LifeTimeService import LifeTimeService
from src.logic.MetricsProcess import MetricsProcess
from src.logic.PictureService import PictureService
from src.logic.SummaryProcess import SummaryProcess
from src.tools.InitTool import InitTool

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    # # # TODO action占所有文件的比例，时间变化只要增加不要减少
    for projname in projList:
        InitTool(projname)
        # # # # 获取文件
        # # f = LifeTimeService(projname)
        # # f.get_analysis_data(projname)
        # # f.getAndSaveSpearManDatas(projname)
        #
        # # 获取图片
        # p = PictureService(projname)
        # p.get_pic(projname)
        #
        # 结合metrics数据和fixed数据
        # m = MetricsProcess(projname, False)
        # datas = m.combine_metrics_spotBugs()
        # m.get_average_value(datas)
        # p.get_metrics_pic(projname, m)
        # print('all finish')
        # #
        # # # 选择标记数据
        # f.getRandonFPDatas()
        # #
        # 导出文件
        # f.getLearningData(projname)
        #
    # 汇总文件
    sp = SummaryProcess()
    sp.main_process()
