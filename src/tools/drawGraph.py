import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

from src.const.Const import projName, pic_font_size, picProjList, pic_legend_size, pic_label_font, pic_tick_font, \
    pic_legend_font
from src.dao.Connector import Connector
from src.logic.CollectDatas import CollectDatas


class DrawGraph:
    def __init__(self):
        self.point_style = ['o', '>', '+', 's', '*', 'H', 'x', 'd', '^', 'v']
        return

    # def drawLineChart(self, x_data: list, y_data: list, x_label: str, y_label: str, title: str, save_path: str):
    #     plt.plot(x_data, y_data)
    #     plt.grid()
    #     plt.xlabel(x_label, fontsize=pic_font_size)
    #     plt.ylabel(y_label, fontsize=pic_font_size)
    #     plt.title(title, fontsize=pic_font_size)
    #     plt.xlim(0, 1)
    #     plt.ylim(0, 1)
    #     plt.xticks(size=pic_font_size)
    #     plt.yticks(size=pic_font_size)
    #     plt.savefig(save_path + title)
    #     # plt.show()
    #     plt.cla()
    #     plt.clf()
    #     plt.close()

    # def drawMutilLineChart(self, x_data: dict, y_data: dict, x_label: str, y_label: str, title: str, save_path: str):
    #     i = 0
    #     for projname in x_data.keys():
    #         plt.plot(x_data.get(projname), y_data.get(projname), linestyle=':', marker=self.point_style[i])
    #         i += 1
    #     plt.grid()
    #     plt.xlabel(x_label, fontsize=pic_font_size)
    #     plt.ylabel(y_label, fontsize=pic_font_size)
    #     plt.title(title, fontsize=pic_font_size)
    #     plt.xlim(0, 1)
    #     plt.ylim(0, 1)
    #     plt.xticks(size=pic_font_size)
    #     plt.yticks(size=pic_font_size)
    #     plt.legend(x_data.keys(), loc='best', fontsize=pic_legend_size)
    #     # plt.legend(picProjList, loc='best', fontsize=pic_legend_size)
    #     plt.savefig(save_path + title)
    #     # plt.show()
    #     plt.cla()
    #     plt.clf()
    #     plt.close()
    #     print(save_path + title + " saved finish")

    def drawLineChart(self, x_data: list, y_data: list, x_label: str, y_label: str, title: str, save_path: str):
        self.init_plt(x_label, y_label, title)

        plt.scatter(x_data, y_data, marker=self.point_style[0], edgecolor='black', linewidths=0.5, s=100)

        plt.savefig(save_path + title)
        # plt.show()
        plt.cla()
        plt.clf()
        plt.close()

    def drawMutilLineChart(self, x_data: dict, y_data: dict, x_label: str, y_label: str, title: str, save_path: str):
        self.init_plt(x_label, y_label, title)

        i = 0
        for projname in x_data.keys():
            plt.scatter(x_data.get(projname), y_data.get(projname), marker=self.point_style[i], edgecolor='black',
                        linewidths=0.5, s=100)
            i += 1
        # loc = 'lower right',
        picProjList.sort()
        leg = plt.legend(picProjList, loc=8, frameon=True, prop=pic_legend_font, fancybox=False,
                         edgecolor='black', bbox_to_anchor=(0.5, -0.25), ncol=5, labelspacing=0.4, columnspacing=0.4, handletextpad=0.1)
        leg.get_frame().set_linewidth(2)
        # plt.legend(picProjList, loc='best', fontsize=pic_legend_size)
        plt.savefig(save_path + title, bbox_inches='tight')
        # plt.show()
        plt.cla()
        plt.clf()
        plt.close()
        print(save_path + title + " saved finish")

    def drawMutiBarChart(self, x_data: list, y_data: dict, x_label: str, y_label: str, title: str, save_path: str):
        self.init_bar_plt(x_data, x_label, y_label, title)

        i = 0
        x_width = range(0, len(x_data))
        total_width = 0.8
        n = len(y_data.keys())
        width = total_width / n
        x_width = [j - (total_width - width) / 2 for j in x_width]
        for projname in y_data.keys():
            plt.bar([j + i * width for j in x_width], y_data.get(projname), width=width, edgecolor='black')
            i += 1

        picProjList.sort()
        leg = plt.legend(picProjList, loc=8, frameon=True, prop=pic_legend_font, fancybox=False,
                         edgecolor='black', bbox_to_anchor=(0.5, -0.25), ncol=5, labelspacing=0.4, columnspacing=0.4, handletextpad=0.1)
        leg.get_frame().set_linewidth(2)
        # plt.legend(picProjList, loc='best', fontsize=pic_legend_size)
        plt.savefig(save_path + title, bbox_inches='tight')
        # plt.show()
        plt.cla()
        plt.clf()
        plt.close()
        print(save_path + title + " saved finish")

    # def drawMutiLineChartWithoutPeicent(self, x_data: dict, y_data: dict, x_label: str, y_label: str, title: str,
    #                                     save_path):
    #     i = 0
    #     for projname in x_data.keys():
    #         plt.plot(x_data.get(projname), y_data.get(projname), linestyle=':', marker=self.point_style[i])
    #         i += 1
    #     plt.grid()
    #     plt.xlabel(x_label, fontsize=pic_font_size)
    #     plt.ylabel(y_label, fontsize=pic_font_size)
    #     plt.title(title, fontsize=pic_font_size)
    #     plt.legend(picProjList, loc='best', fontsize=pic_legend_size)
    #     plt.xticks(size=pic_font_size)
    #     plt.yticks(size=pic_font_size)
    #     plt.savefig(save_path + title)
    #     # plt.show()
    #     plt.cla()
    #     plt.clf()
    #     plt.close()

    def drawMutiLineChartWithoutPeicent(self, x_data: dict, y_data: dict, x_label: str, y_label: str, title: str,
                                        save_path):
        x_tick_data = [str(i) for i in range(2005, 2022)]
        self.init_plt_years(x_tick_data, x_label, y_label, title)
        i = 0
        for projname in x_data.keys():
            plt.plot(x_data.get(projname), y_data.get(projname), linestyle=':', marker=self.point_style[i])
            i += 1

        picProjList.sort()
        leg = plt.legend(picProjList, loc=8, frameon=True, prop=pic_legend_font, fancybox=False,
                         edgecolor='black', bbox_to_anchor=(0.5, -0.3), ncol=5, labelspacing=0.4, columnspacing=0.4,
                         handletextpad=0.1)
        leg.get_frame().set_linewidth(2)
        # plt.legend(picProjList, loc='best', fontsize=pic_legend_size)
        plt.savefig(save_path + title, bbox_inches='tight')
        # plt.xticks(size=pic_font_size)
        # plt.yticks(size=pic_font_size)
        # plt.show()
        plt.cla()
        plt.clf()
        plt.close()

    def drawBarChartWithoutPeicent(self, x_data: list, y_data: list, x_label: str, y_label: str, title: str,
                                   save_path):
        plt.bar(x_data, y_data)
        plt.grid()
        plt.xlabel(x_label, fontsize=pic_font_size)
        plt.ylabel(y_label, fontsize=pic_font_size)
        plt.title(title, fontsize=pic_font_size)
        plt.savefig(save_path + title)
        plt.xticks(size=pic_font_size)
        plt.yticks(size=pic_font_size)
        # plt.show()
        plt.cla()
        plt.clf()
        plt.close()

    def drawLineChartWithoutPeicent(self, x_data: list, y_data: list, x_label: str, y_label: str, title: str,
                                    save_path):
        plt.plot(x_data, y_data)
        plt.grid()
        plt.xlabel(x_label, fontsize=pic_font_size)
        plt.ylabel(y_label, fontsize=pic_font_size)
        plt.title(title, fontsize=pic_font_size)
        plt.savefig(save_path + title)
        plt.xticks(size=pic_font_size)
        plt.yticks(size=pic_font_size)
        # plt.show()
        plt.cla()
        plt.clf()
        plt.close()

    def mutilDatasInOneGraph(self, x_datas: list, y_datas: list, line_labels: list, x_label: str, y_label: str,
                             title: str, save_path):
        picProjList.sort()

        for i in range(len(x_datas)):
            plt.scatter(x_datas[i], y_datas[i], label=line_labels[i], marker=self.point_style[i])
            leg = plt.legend(picProjList, loc=8, frameon=True, prop=pic_legend_font, fancybox=False,
                             edgecolor='black', bbox_to_anchor=(0.5, -0.25), ncol=5, labelspacing=0.4, columnspacing=0.4,
                             handletextpad=0.1)
            leg.get_frame().set_linewidth(2)
        self.init_plt(x_label, y_label, title)
        plt.savefig(save_path + title, bbox_inches='tight')
        plt.cla()
        plt.clf()
        plt.close()

    def init_bar_plt(self, x_data, x_label, y_label, title):
        plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
        plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
        # plt.axis('square')

        plt.grid(ls=(0, (2, 5)), c='black', linewidth=1)

        plt.xlabel(x_label, fontdict=pic_label_font)
        plt.ylabel(y_label, fontdict=pic_label_font)
        plt.title(title, fontsize=pic_font_size)

        # x_major_locator = MultipleLocator(0.1)
        # # 把x轴的刻度间隔设置为1，并存在变量里
        # y_major_locator = MultipleLocator(0.1)
        # 把y轴的刻度间隔设置为10，并存在变量里
        ax = plt.gca()
        # ax为两条坐标轴的实例
        # ax.xaxis.set_major_locator(x_major_locator)
        # # 把x轴的主刻度设置为1的倍数
        # ax.yaxis.set_major_locator(y_major_locator)

        for xtl in ax.get_xticklines():
            xtl.set_markersize(5)  # length
            xtl.set_markeredgewidth(1)  # width

        for ytl in ax.get_yticklines():
            ytl.set_markersize(5)
            ytl.set_markeredgewidth(1)

        for xtlabel in ax.get_xticklabels():
            xtlabel.set_fontproperties(pic_tick_font)

        for ytlabel in ax.get_yticklabels():
            ytlabel.set_fontproperties(pic_tick_font)

        bwith = 2
        ax.spines['left'].set_color((0, 0, 0, 1))
        ax.spines['left'].set_linewidth(bwith)
        ax.spines['right'].set_color((0, 0, 0, 1))
        ax.spines['right'].set_linewidth(bwith)
        ax.spines['top'].set_color((0, 0, 0, 1))
        ax.spines['top'].set_linewidth(bwith)
        ax.spines['bottom'].set_color((0, 0, 0, 1))
        ax.spines['bottom'].set_linewidth(bwith)

        # plt.xlim(0, 1)
        # plt.ylim(0, 1)
        plt.xticks(range(0, len(x_data)), x_data, size=pic_font_size)
        # plt.yticks(np.asarray([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]), size=pic_font_size)

    def init_plt(self, x_label, y_label, title):
        plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
        plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
        plt.axis('square')

        plt.grid(ls=(0, (2, 5)), c='black', linewidth=1)

        plt.xlabel(x_label, fontdict=pic_label_font)
        plt.ylabel(y_label, fontdict=pic_label_font)
        plt.title(title, fontsize=pic_font_size)

        x_major_locator = MultipleLocator(0.1)
        # 把x轴的刻度间隔设置为1，并存在变量里
        y_major_locator = MultipleLocator(0.1)
        # 把y轴的刻度间隔设置为10，并存在变量里
        ax = plt.gca()
        # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        # 把x轴的主刻度设置为1的倍数
        ax.yaxis.set_major_locator(y_major_locator)

        for xtl in ax.get_xticklines():
            xtl.set_markersize(5)  # length
            xtl.set_markeredgewidth(1)  # width

        for ytl in ax.get_yticklines():
            ytl.set_markersize(5)
            ytl.set_markeredgewidth(1)

        for xtlabel in ax.get_xticklabels():
            xtlabel.set_fontproperties(pic_tick_font)

        for ytlabel in ax.get_yticklabels():
            ytlabel.set_fontproperties(pic_tick_font)

        bwith = 2
        ax.spines['left'].set_color((0, 0, 0, 1))
        ax.spines['left'].set_linewidth(bwith)
        ax.spines['right'].set_color((0, 0, 0, 1))
        ax.spines['right'].set_linewidth(bwith)
        ax.spines['top'].set_color((0, 0, 0, 1))
        ax.spines['top'].set_linewidth(bwith)
        ax.spines['bottom'].set_color((0, 0, 0, 1))
        ax.spines['bottom'].set_linewidth(bwith)

        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xticks(np.asarray([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]), size=pic_font_size)
        plt.yticks(np.asarray([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]), size=pic_font_size)

    def init_plt_years(self, x_data, x_label, y_label, title):
        plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
        plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
        # plt.axis('square')

        plt.grid(ls=(0, (2, 4)), c='black', linewidth=1)

        plt.xlabel(x_label, fontdict=pic_label_font)
        plt.ylabel(y_label, fontdict=pic_label_font)
        plt.title(title, fontsize=pic_font_size)

        x_major_locator = MultipleLocator(1)
        # 把x轴的刻度间隔设置为1，并存在变量里
        y_major_locator = MultipleLocator(5)
        # 把y轴的刻度间隔设置为10，并存在变量里
        ax = plt.gca()
        # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        # 把x轴的主刻度设置为1的倍数
        ax.yaxis.set_major_locator(y_major_locator)

        for xtl in ax.get_xticklines():
            xtl.set_markersize(5)  # length
            xtl.set_markeredgewidth(1)  # width

        for ytl in ax.get_yticklines():
            ytl.set_markersize(5)
            ytl.set_markeredgewidth(1)

        for xtlabel in ax.get_xticklabels():
            xtlabel.set_fontproperties(pic_tick_font)

        for ytlabel in ax.get_yticklabels():
            ytlabel.set_fontproperties(pic_tick_font)

        bwith = 2
        ax.spines['left'].set_color((0, 0, 0, 1))
        ax.spines['left'].set_linewidth(bwith)
        ax.spines['right'].set_color((0, 0, 0, 1))
        ax.spines['right'].set_linewidth(bwith)
        ax.spines['top'].set_color((0, 0, 0, 1))
        ax.spines['top'].set_linewidth(bwith)
        ax.spines['bottom'].set_color((0, 0, 0, 1))
        ax.spines['bottom'].set_linewidth(bwith)
        # plt.xlim(2005, 2021)
        # plt.ylim(0, 24)
        plt.xticks(rotation=30)
        # plt.yticks(np.asarray([0, 6, 12, 18, 24]), size=pic_font_size)


if __name__ == "__main__":
    # c = Connector()
    # collectdata = CollectDatas()
    # cursor = c.findFieldGroupCounts(projName, "field")
    # x_datas, y_data = collectdata.getGraphDatas(cursor, ['field', 'cnt'])
    # x_int_datas = []
    # sum = 0
    # y_sum = np.sum(y_data, axis=0)
    # for i in range(len(y_data)):
    #     sum += y_data[i]
    #     y_data[i] = sum / y_sum
    #     x_int_datas.append(i / len(x_datas))
    # d = DrawGraph()
    # d.drawLineChart(x_int_datas, y_data, "file nums", "fixed nums", "relations between files and fixedBugs")
    picProjList.sort()
    print(picProjList)
