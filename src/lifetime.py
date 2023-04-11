import os
import csv
import tools.cmd_tool as ct
import  calendar
from datetime import datetime as dt

pro_repo = 'D:/data/repos/repos-a/'
pro_name = 'commons-lang'
sample_file_path = 'D:\\graduated_design\\data_preprocess\\commons-lang_master_sample.txt'
sample_res = 'D:\\sample_res\\{}\\final\\'.format(pro_name)
sample_repo = 'D:\\sample_repo\\{}\\'.format(pro_name)


def getDays(oid, fixer):
    ct.change_path_to_target(pro_repo + pro_name)

    oid_lines = ct.run_command('git log {}'.format(oid))

    oid_date = oid_lines[2].split('Date:')[1].strip().split(' ')
    o_month = list(calendar.month_abbr).index(oid_date[1])
    o_day = oid_date[2]
    o_yeah = oid_date[4]

    fixer_lines = ct.run_command('git log {}'.format(fixer))

    fixer_date = fixer_lines[2].split('Date:')[1].strip().split(' ')
    f_month = list(calendar.month_abbr).index(fixer_date[1])
    f_day = fixer_date[2]
    f_yeah = fixer_date[4]

    origin_date = dt(int(o_yeah), int(o_month), int(o_day))

    fixed_date = dt(int(f_yeah), int(f_month), int(f_day))

    day_count = (fixed_date - origin_date).days

    return day_count


if __name__ == '__main__':
    files = os.listdir(sample_res)
    for file in files:
        commit = file.split('.csv')[0]
        warnings = []
        with open(sample_res + file, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                warnings.append(i)
        f.close()
        warnings = warnings[1:]
        for warning in warnings:
            close_fixer = warning[9]
            mining_fixer = warning[11]
            mining_days = ''
            close_days = ''
            if close_fixer != '':
                close_days = getDays(commit, close_fixer)
            if mining_fixer != 'null':
                mining_days = getDays(commit, mining_fixer)
            warning.append(close_days)
            warning.append(mining_days)

        with open(sample_res + file, 'w', newline='') as f:
            print('writing......')
            writer = csv.writer(f)
            writer.writerow(['priority', 'category', 'vtype', 'path', 'method', 'field', 'start', 'end', 'close', 'close_fixer', 'mining', 'mining_fixer', 'close_lifecircle', 'mining_lifecircle'])
            writer.writerows(warnings)
        f.close()

