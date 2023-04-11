import matplotlib.font_manager as fm

# projList = ['commons-collections', 'commons-codec', 'commons-fileupload', 'commons-net',
#             'maven-dependency-plugin', 'commons-configuration']
projList = [
    'commons-codec',
    'commons-fileupload',
    'commons-net',
    'maven-dependency-plugin',
    'commons-collections',
    'commons-digester',
    'commons-pool',
    'commons-dbcp',
    'commons-bcel',
    'commons-configuration'
]

month_abbr_list = ['Jan',
                   'Feb',
                   'Mar',
                   'Apr',
                   'May',
                   'Jun',
                   'Jul',
                   'Aug',
                   'Sep',
                   'Oct',
                   'Nov',
                   'Dec'
                   ]

picProjList = [
    'codec',
    'fileupload',
    'net',
    'mavendp',
    'collections',
    'digester',
    'pool',
    'dbcp',
    'bcel',
    'configuration'
]
# projName = projList[-1]
projName = 'commons-bcel'

base_dir = "C:/Users/lxyeah/Desktop/task1/"
summary_dir = base_dir + "resource/datas/summary/"
data_base = base_dir + "resource/datas/"
data_dir = base_dir + "resource/datas/" + projName + "/"
repo_base = base_dir + "resource/proj/"
repo_dir = base_dir + "resource/proj/" + projName + "/"
tmp_base = base_dir + "resource/tmp/"
tmp_dir = base_dir + "resource/tmp/" + projName + "/"
metrics_base = base_dir + "resource/metrics/"
metrics_dir = base_dir + "resource/metrics/" + projName + "/"
next_base = base_dir + 'resource/initdatas/'
next_dir = base_dir + 'resource/initdatas/' + projName + '/'

default_year = 2022
git_short_commit_lens = 8
pic_font_size = 10
pic_legend_size = 10
pic_label_font_size = 13
pic_label_font = {'style': 'normal', 'weight': 'bold', 'size': 12}
pic_tick_font = fm.FontProperties(style='normal', weight='bold', size=10)
pic_legend_font = {'style': 'normal', 'weight': 'bold', 'size': 9}

fileMap = {"category_line": 0,
           "vtype_line": 1,
           "priority_line": 2,
           "rank_line": 3,
           "project_line": 4,
           "rootId_line": 5,
           'buggy_line': 6,
           "file_line": 7,
           "leafId_line": 10,
           "file_path_line": 11,
           "method_line": 12,
           "field_line": 13,
           "resolution_line": 14,
           "life_time_line": 15}

categroyMap = {'B': "BAD_PRACTICE",
               'C': "CORRECTNESS",
               "E": "Malicious code vulnerability",
               'I': "I18N",
               'D': "DODGY_CODE",
               'S': "SECURITY",
               'P': "PERFORMANCE",
               'V': "MALICIOUS_CODE",
               'X': "EXPERIMENTAL",
               'M': "Multithreaded correctness"
               }

init_file_headers = [
    "categpry", "vtype", "priority", "rank", "project", 'origin commit', 'buggy commit', 'buggy path', 'buggy start',
    "buggy end", "fixer", "fixer path", 'method', 'field', 'resolution']

metrics_headers = "Kind,Name,File,AvgCyclomatic,AvgCyclomaticModified,AvgCyclomaticStrict,AvgEssential," \
                  "AvgLine,AvgLineBlank,AvgLineCode,AvgLineComment,CountClassBase,CountClassCoupled," \
                  "CountClassCoupledModified,CountClassDerived,CountDeclClass,CountDeclClassMethod," \
                  "CountDeclClassVariable,CountDeclExecutableUnit,CountDeclFile,CountDeclFunction," \
                  "CountDeclInstanceMethod,CountDeclInstanceVariable,CountDeclMethod,CountDeclMethodAll," \
                  "CountDeclMethodDefault,CountDeclMethodPrivate,CountDeclMethodProtected,CountDeclMethodPublic," \
                  "CountInput,CountLine,CountLineBlank,CountLineCode,CountLineCodeDecl,CountLineCodeExe," \
                  "CountLineComment,CountOutput,CountPath,CountPathLog,CountSemicolon,CountStmt,CountStmtDecl," \
                  "CountStmtExe,Cyclomatic,CyclomaticModified,CyclomaticStrict,Essential,Knots,MaxCyclomatic," \
                  "MaxCyclomaticModified,MaxCyclomaticStrict,MaxEssential,MaxEssentialKnots,MaxInheritanceTree," \
                  "MaxNesting,MinEssentialKnots,PercentLackOfCohesion,PercentLackOfCohesionModified," \
                  "RatioCommentToCode,SumCyclomatic,SumCyclomaticModified,SumCyclomaticStrict,SumEssential".split(",")
metricsMap = {
    "kind": 0,
    "fileName": 1,
    "startNums": 2
}
# metrics_headers = "Kind,Name,AvgCyclomatic,AvgCyclomaticModified,AvgCyclomaticStrict,AvgEssential," \
#                   "AvgLine,AvgLineBlank,AvgLineCode,AvgLineComment,CountClassBase,CountClassCoupled," \
#                   "CountClassCoupledModified,CountClassDerived,CountDeclClass,CountDeclClassMethod," \
#                   "CountDeclClassVariable,CountDeclExecutableUnit,CountDeclFile,CountDeclFunction," \
#                   "CountDeclInstanceMethod,CountDeclInstanceVariable,CountDeclMethod,CountDeclMethodAll," \
#                   "CountDeclMethodDefault,CountDeclMethodPrivate,CountDeclMethodProtected,CountDeclMethodPublic," \
#                   "CountInput,CountLine,CountLineBlank,CountLineCode,CountLineCodeDecl,CountLineCodeExe," \
#                   "CountLineComment,CountOutput,CountPath,CountPathLog,CountSemicolon,CountStmt,CountStmtDecl," \
#                   "CountStmtExe,Cyclomatic,CyclomaticModified,CyclomaticStrict,Essential,Knots,MaxCyclomatic," \
#                   "MaxCyclomaticModified,MaxCyclomaticStrict,MaxEssential,MaxEssentialKnots,MaxInheritanceTree," \
#                   "MaxNesting,MinEssentialKnots,PercentLackOfCohesion,PercentLackOfCohesionModified," \
#                   "RatioCommentToCode,SumCyclomatic,SumCyclomaticModified,SumCyclomaticStrict,SumEssential".split(",")

metrics_types = ['Annotation', 'Type', 'TypeVariable', 'Constructor', 'Method', 'Class', 'Interface', 'File', 'Package']
start_loc = fileMap.get("resolution_line") + 1

default_metrics_value = -1

resolution_type = ['unknown', 'fixed', 'disappear', 'unfixed']

marked_baesd_datas_headers = ['average', 'median', 'density']
marked_based = 'median'


