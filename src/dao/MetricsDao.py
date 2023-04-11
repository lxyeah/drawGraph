import os

from src.const import Const
from src.const.Const import metricsMap, default_metrics_value, base_dir
from src.tools.FileTool import FileTool
from src.tools.GitTool import GitClass


class MetricsDao:
    def __init__(self, projName: str):
        tmp = Const.metrics_base + projName + "/"
        projPath = base_dir + "resource/proj/" + projName + "/"
        gitTool = GitClass(projPath)
        short_long_map = gitTool.get_commitId_short_long_map()
        files = os.listdir(tmp)
        f = FileTool()
        self.datas = {}
        print("start read metrics")
        for file in files:
            short_id = file.split("_")[1].split(".")[0]
            long_id = short_long_map.get(short_id)
            data = f.get_data_from_file(file, tmp)[1:]
            new_datas = []
            for i in data:
                for j in range(metricsMap.get("startNums") + 1, len(i)):
                    if i[j] == "":
                        i[j] = default_metrics_value
                    else:
                        i[j] = float(i[j])
                new_datas.append(i)
            self.datas[long_id] = new_datas
            print(projName + " now read metrics files idx is : " + str(files.index(file)) + "/" + str(len(files)))
            # if files.index(file) > 500:
            #     break
        print("finish reading")


if __name__ == "__main__":
    m = MetricsDao(Const.projName)
