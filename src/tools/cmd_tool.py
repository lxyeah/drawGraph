import os


def change_path_to_target(path):
    commendline = path
    os.chdir(commendline)
    # print(res)


def run_command(command):
    com_res = os.popen(command)
    com_res = com_res.buffer.read().decode(encoding='utf-8', errors='ignore')
    return com_res.split('\n')


def get_run_result(commond):
    com_res = os.system(commond)
    print(commond)
    return com_res


if __name__ == "__main__":
    # change_path_to_target('E:\\projects\\git\\mooctest\\tika-vtype\\')
    # run_command('git log')
    x = '-        private float duration;'
    print(
        'd4a39b4873 tika-parser-modules/tika-parser-integration-tests/src/test/java/org/apache/tika/parser/pdf/PDFParserTest.java                  vtype) /*'.split(
            ')', maxsplit=1)[1].strip())
