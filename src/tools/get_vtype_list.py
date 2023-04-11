import lxml
from bs4 import BeautifulSoup

from src.const.Const import base_dir

if __name__ == '__main__':
    with open(base_dir + '/guideline/FindBugs Bug Descriptions.html', 'r') as f:
        data = f.read()
    # print(type(data))
    soup = BeautifulSoup(data, 'html.parser')
    h3list = soup.find_all('h3')
    s = "vtype_map = {\n"
    idx = 1
    for i in h3list:
        now = "'" + i.a.attrs['name'] + "':" + str(idx) + ",\n"
        idx += 1
        s += now
    s += '}'
    print(s)
