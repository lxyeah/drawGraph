import pandas as pd


# 将df的值插入到map中
def add_value_to_map(data_map: map, df: pd.DataFrame):
    indexs = df.index.tolist()
    datas = df.values.tolist()
    for i in range(len(indexs)):
        data_map[indexs[i]] = data_map.setdefault(indexs[i], []) + [datas[i]]


# 将df的值用占比的形式插入map中
def add_percent_value_to_map(data_map: map, son_df: pd.DataFrame, ma_df: pd.DataFrame):
    types = list(set((son_df.index.tolist() + ma_df.index.tolist())))
    for i in types:
        son = 0
        ma = 0
        try:
            son += son_df.get(i)
            ma += son_df.get(i)
        except TypeError:
            son += 0
        try:
            ma += ma_df.get(i)
        except TypeError:
            ma += 0
        data_map[i] = data_map.setdefault(i, []) + [son / (son + ma)]
