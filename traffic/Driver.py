import pandas as pd
import numpy as np


# 整合每个司机的特征维度
def get_driver_value(df_vehicle):
    df_calculate = df_vehicle[
        ['当事人_驾驶证号', 'age', 'is_local', 'trans_code', 'occur_prob', 'severity', '违法行为记分数', '违法行为罚款金额', '违法行为_事故等级']]
    df_res = df_calculate.groupby('当事人_驾驶证号').agg('mean')
    df_res.columns = ['age', 'is_local', 'trans_code', 'occur_prob', 'severity', 'score', 'fine', 'accident']
    df_res.index_name = '当事人_驾驶证号'
    df_res['counts'] = df_calculate['当事人_驾驶证号'].value_counts()

    b = df_res[df_res.index.isin(list(df_driver_info['身份证明号码']))]
    print(len(b))
    for uid in list(b.index):
        if uid not in list(df_driver_info['身份证明号码']):
            print(uid + "not exist in info table")
            continue
        dfi = df_driver_info[df_driver_info["身份证明号码"] == uid]
        gender = dfi["性别"]
        first_year = dfi['初次领证日期'].str[0:4]
        drive_age = 2021 - pd.to_numeric(first_year, errors='coerce').fillna(0)
        driver_source = dfi["驾驶人来源说明"]
        driver_address = dfi["联系住所详细地址"]
        df_res.loc[uid, 'gender'] = gender[gender.index[0]]
        df_res.loc[uid, 'driver_age'] = drive_age[drive_age.index[0]]
        df_res.loc[uid, 'source'] = driver_source[driver_source.index[0]]
        df_res.loc[uid, 'address'] = driver_address[driver_address.index[0]]
    return df_res


# 划分等级
def get_driver_level(df_driver_value):
    # 如果只是df_level=df_res 是浅拷贝，和引用类似，会导致修改原来的值
    df_level = df_driver_value.copy(deep=True)
    df_level = df_level.round(0)
    list_col = df_driver_value.columns
    # list_col = ['counts']
    for col in list_col:
        if col == 'id' or col == 'trans_code' or col == 'is_local':
            continue
        dfi = df_level[col].copy(deep=True)
        Q1 = df_level[col].quantile(0.25)
        Q2 = df_level[col].quantile(0.5)
        Q3 = df_level[col].quantile(0.75)
        IQR = Q3 - Q1
        Max = Q3 + IQR * 1.5
        Min = Q1 - IQR * 1.5
        if col == 'counts':
            df_level.loc[dfi >= 5, col] = 5
        elif col == 'score':
            df_level.loc[dfi <= 0.5, col] = 1
            df_level.loc[(dfi < 1) & (dfi > 0.5), col] = 2
            df_level.loc[(dfi < 2) & (dfi >= 1), col] = 3
            df_level.loc[(dfi < 3) & (dfi >= 2), col] = 4
            df_level.loc[(dfi < 6) & (dfi >= 3), col] = 5
            df_level.loc[dfi >= 6, col] = 6
        elif col == 'fine':
            df_level.loc[dfi < 50, col] = 1
            df_level.loc[(dfi < 100) & (dfi >= 50), col] = 2
            df_level.loc[(dfi < 150) & (dfi >= 100), col] = 3
            df_level.loc[(dfi < 200) & (dfi >= 150), col] = 4
            df_level.loc[(dfi < 300) & (dfi >= 200), col] = 5
            df_level.loc[dfi >= 300, col] = 6
        elif col == 'age':
            df_level.loc[dfi <= 25, col] = 1
            df_level.loc[(dfi < 35) & (dfi >= 25), col] = 2
            df_level.loc[(dfi < 45) & (dfi >= 35), col] = 3
            df_level.loc[(dfi < 55) & (dfi >= 45), col] = 4
            df_level.loc[dfi >= 55, col] = 5
        elif col == 'accident':
            df_level.loc[dfi == 0, col] = 1
            df_level.loc[(dfi <= 2) & (dfi > 0), col] = 2
            df_level.loc[(dfi <= 4) & (dfi > 2), col] = 3
    df_level.index.name = 'id'
    return df_level


if __name__ == '__main__':
    df_driver_info = pd.read_csv("/Users/jiarui/Study/交通事故/data/海宁驾驶证信息表.csv")
    df_no_yingyun_input = pd.read_csv("/Users/jiarui/Study/交通事故/data/output/df_no_yingyun_value.csv")
    df_yingyun_input = pd.read_csv("/Users/jiarui/Study/交通事故/data/output/df_yingyun_value.csv")
    print("--------非营运车辆--------")
    # df_no_yingyun_value = get_driver_value(df_no_yingyun_input)
    print("--------营运车辆--------")
    df_yingyun_value = get_driver_value(df_yingyun_input)
