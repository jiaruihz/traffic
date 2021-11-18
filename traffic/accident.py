import pandas as pd
import numpy as np


# 看看accident和illegal_action能不能通过车牌号对应上
def get_driver_value(df_vehicle):
    df_calculate = df_vehicle[
        ['当事人_驾驶证号', 'age', 'is_local', 'trans_code', 'occur_prob', 'severity', '违法行为记分数', '违法行为罚款金额', '违法行为_事故等级']]
    df_res = df_calculate.groupby('当事人_驾驶证号').agg('mean')
    df_res.columns = ['age', 'is_local', 'trans_code', 'occur_prob', 'severity', 'score', 'fine', 'accident']
    df_res.index_name = '当事人_驾驶证号'
    df_res['counts'] = df_calculate['当事人_驾驶证号'].value_counts()

    b = df_res[df_res.index.isin(accident_uids)]
    print("在违法记录中能够查到的司机个数")
    print(len(b))



if __name__ == '__main__':
    df_accident_info = pd.read_csv("/Users/jiarui/Study/交通事故/data/海宁-事故人车信息记录表-晚于2015.1.1.csv")
    df_driver_info = pd.read_csv("/Users/jiarui/Study/交通事故/data/海宁驾驶证信息表.csv")
    list_driver_have_info_uids = list(df_driver_info["身份证明号码"])
    accident_uids = list(df_accident_info['当事人-身份证明号码'])

    #统计事故人信息 value_count
    # accident_driver =

    print("在驾驶人信息中能够查到的个数")

    print(len(df_accident_info['当事人-身份证明号码'].isin(list_driver_have_info_uids)))
    df_no_yingyun_input = pd.read_csv("/Users/jiarui/Study/交通事故/data/output/df_no_yingyun_value.csv")
    df_yingyun_input = pd.read_csv("/Users/jiarui/Study/交通事故/data/output/df_yingyun_value.csv")

    get_driver_value(df_no_yingyun_input)