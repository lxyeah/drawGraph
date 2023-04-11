from src.const.Const import metrics_types


def metrics_order(a, b):
    orders = metrics_types
    return orders.index(a[0].split(' ')[-1]) - orders.index(b[0].split(' ')[-1])

def map2list(data:map):
    list = []
    for i in data:
        list.append([i]+data[i])
    return list