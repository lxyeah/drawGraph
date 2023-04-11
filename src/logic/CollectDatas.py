import calendar

import pandas as pd
import py2neo.cypher

import src.tools.cmd_tool as ct
from datetime import datetime as dt

from src.const.Const import base_dir
from src.tools.GitTool import GitClass


class CollectDatas:

    def __init__(self):
        return

    def getLifeCycle(self, projPath: str, start_id: str, end_id: str):
        ct.change_path_to_target(projPath)

        oid_lines = ct.run_command('git log --pretty=format:“%cd” {} --date=default'.format(start_id))
        # print('git log --pretty=format:“%cd” {}'.format(start_id))
        oid_date = oid_lines[0].strip().split(' ')
        o_month = list(calendar.month_abbr).index(oid_date[1])
        o_day = oid_date[2]
        o_yeah = oid_date[4]

        fixer_lines = ct.run_command('git log --pretty=format:“%cd”  {} --date=default'.format(end_id))
        fixer_date = fixer_lines[0].strip().split(' ')
        try:
            f_month = list(calendar.month_abbr).index(fixer_date[1])
        except IndexError:
            return -1
        f_day = fixer_date[2]
        f_yeah = fixer_date[4]

        origin_date = dt(int(o_yeah), int(o_month), int(o_day))
        fixed_date = dt(int(f_yeah), int(f_month), int(f_day))
        day_count = (fixed_date - origin_date).days
        return day_count

    def getCsvData(self, projPath: str, cursor: py2neo.cypher.Cursor):
        res = []
        headers = ['vtype', 'commit', 'rank', 'project', 'id', 'oid', 'pid',
                   'fixer', 'priority', 'category', 'class']
        while (cursor.forward()):
            now = []
            for i in range(len(headers)):
                now.append(cursor.current['n.' + headers[i]])
            rootId = cursor.current['n.oid'].split(':')[1]
            leafId = cursor.current['n.fixer']
            lifeTime = self.getLifeCycle(projPath, rootId, leafId)
            now.append(lifeTime)
            res.append(now)
        headers.append("lifeTime")
        return headers, res

    def getDataFromCursor(self, cursor: py2neo.cypher.Cursor, headers: list):
        res = []
        while (cursor.forward()):
            now = []
            for i in range(len(headers)):
                now.append(cursor.current['n.' + headers[i]])
            res.append(now)
        return res

    def getGraphDatas(self, cursor: py2neo.cypher.Cursor, labels, needZero=True):
        x_data = []
        y_data = []
        if needZero:
            x_data.append(0), y_data.append(0)
        while cursor.forward():
            x_data.append(cursor.current[labels[0]])
            y_data.append(cursor.current[labels[1]])
        return x_data, y_data

    def getCommitChangeOrderByTime(self, datas, projName, only_now=False):
        x_data = []
        y_data = []
        projPath = base_dir + "resource/proj/" + projName + "/"
        gt = GitClass(projPath)
        commit_map = gt.get_log_time_order()
        commit_order = {}
        commit_fix_order = {}
        for i in datas:
            if i[2] != "":
                commit_fix_order[commit_map.get(i[2])] = commit_fix_order.get(commit_map.get(i[2]), 0) + 1
            commit_order[commit_map.get(i[1])] = commit_order.get(commit_map.get(i[1]), 0) + 1
        add_bugs_list = sorted(commit_order.keys(), reverse=False)
        fix_bugs_list = sorted(commit_fix_order.keys(), reverse=False)
        tmp = 0
        x_data.append(min(add_bugs_list[0], fix_bugs_list[0]) - 1)
        y_data.append(0)
        for i in range(min(add_bugs_list[0], fix_bugs_list[0]), max(add_bugs_list[-1], fix_bugs_list[-1]) + 1, 1):
            if only_now:
                if commit_order.get(i) is None:
                    continue
                tmp = commit_order.get(i)
            else:
                if commit_order.get(i) is None and commit_fix_order.get(i) is None:
                    continue
                if commit_order.get(i) is not None:
                    tmp += commit_order.get(i)
                if commit_fix_order.get(i) is not None:
                    tmp -= commit_fix_order.get(i)
            x_data.append(i)
            y_data.append(tmp)
        return x_data, y_data

    def get_list_from_groupBy_nums(self, series: pd.DataFrame, group_types: list):
        res = []
        fileList = []
        for i in list(series.index):
            if i[0] not in fileList:
                fileList.append(i[0])
        for i in fileList:
            now = [i]
            for j in group_types:
                try:
                    now.append(series.at[(i, j), 0])
                except KeyError:
                    now.append('')
            res.append(now)
        return res
