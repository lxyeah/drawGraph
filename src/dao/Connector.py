import csv

from py2neo import *
import pandas as pd

from src.const.Const import projName
from src.logic.CollectDatas import CollectDatas

neoj4_username = "neo4j"
neoj4_url = 'http://172.29.4.23:7474'
neoj4_passwd = "ise@1901"
# neoj4_url = 'http://172.29.4.55:7474'
# neoj4_passwd = "112358"
prjName = projName
basePath = "/Users/mayang/PycharmProjects/summary2Excel/"


class Connector:
    def __init__(self):
        self.graph = Graph(neoj4_url, auth=(neoj4_username, neoj4_passwd))
        self.matcher = NodeMatcher(self.graph)

    def getDataByClassAndProj(self, classType: str, projName: str):
        matchStr = """
            match (n) 
            where n.class = "{}" and n.project = "{}" and not n.oid contains 'Test:'
            return n.vtype,n.commit,n.rank,n.project,n.id,n.oid,n.pid,n.priority,n.category,n.class
        """.format(classType, projName)
        return self.graph.run(matchStr)

    def getDataByResolution(self, resolution: str, projName: str) -> pd.DataFrame:
        matchStr = """
                    match (n) 
                    where n.resolution = "{}" and n.project = "{}" and not n.oid contains 'Test:'
                    return n.vtype,n.commit,n.rank,n.project,n.id,n.oid,n.pid,n.fixer,n.priority,n.category,n.class
                    limit 5
                """.format(resolution, projName)
        return self.graph.run(matchStr)

    def findByField(self, field: str):
        matchStr = """
            match (n)
            where n.field = "{}" and not n.oid contains 'Test:'
            return n
        """.format(field)
        return self.graph.run(matchStr)

    def findFieldGroupCounts(self, projName: str, base: str):
        matchStr = """
                match (n)
                where n.resolution = "fixed" and n.project = "{}" and not n.oid contains 'Test:'
                return n.{} as {},count(*) as cnt
                order by cnt desc
        """.format(projName, base, base)
        return self.graph.run(matchStr)


if __name__ == "__main__":
    c = Connector()
    # # cursor = c.getDataByClassAndProj("origin", "maven-dependency-plugin")
    # cursor = c.getDataByResolution("fixed", prjName)
    # print(cursor)
    # projPath = basePath + prjName
    # dataPath = basePath + prjName + ".csv"
    # with open(dataPath, 'w', newline='') as f:
    #     collectdata = CollectDatas()
    #     headers, datas = collectdata.getCsvData(projPath, cursor)
    #     writer = csv.writer(f)
    #     writer.writerow(headers)
    #     writer.writerows(datas)
    #     print(prjName + " has finished")
    print(c.findFieldGroupCounts(projName,'vtype'))
