import pandas as pd


def read():
    data_path = "/Users/jiarui/Study/交通事故/data/data.csv"
    df = pd.read_csv(data_path)
    list_drivers = df["当事人姓名"].unique()
    print(df['驾驶证号'].value_counts())

    df_d1 = df[df['当事人姓名'] == '刘伟']
    print(df_d1)
    print()


if __name__ == '__main__':
    read()