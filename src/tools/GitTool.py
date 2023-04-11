import time

import src.tools.cmd_tool as ct
from src.const import Const
from src.const.Const import repo_dir, default_year, projName


class GitClass:
    def __init__(self, projPath=repo_dir):
        ct.change_path_to_target(projPath)
        self.projPath = projPath
        print("projPath is : " + projPath)
        return

    def get_log_time_order(self):
        res = ct.run_command("""git log --all --pretty=format:\"%H\"""")
        map = {}
        for i in range(len(res)):
            map[res[i]] = self.get_commit_time(res[i])
        return map

    def get_commit_time(self, commit_id):
        time = ct.run_command('git log --pretty=format:“%cd” {}  --date=default'.format(commit_id))[0].strip().split(
            ' ')
        if (len(time) < 4):
            return default_year
        return int(time[4])

    def get_commitId_short_long_map(self):
        res = ct.run_command("""git log --all --pretty=format:\"%H\"""")
        map = {}
        for i in res:
            map[i[0:Const.git_short_commit_lens]] = i
        return map

    # 使用 git config --global log.date format:'%Y-%m-%d %H:%M:%S' 格式化git log输出
    def get_commit_orderBy_time(self, commit_list=[]):
        if commit_list == []:
            commit_list = ct.run_command("""git log --all --pretty=format:\"%H\"""")
        map = {}
        for i in commit_list:
            print(self.projPath + ' git log get time index is ' + str(commit_list.index(i)) + "/" + str(len(commit_list)))
            gitTime = ct.run_command('git log --pretty=format:“%cd” {}'.format(i))[0][1:-1]
            timeStamp = int(time.mktime(time.strptime(gitTime, "%Y-%m-%d %H:%M:%S")))
            map[i] = timeStamp
        print('time map get finished')
        return map


if __name__ == "__main__":
    gc = GitClass(projName)
    print(gc.get_commit_orderBy_time())
