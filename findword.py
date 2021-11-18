import pandas as pd

# 读取文件，并去除重复值

df = pd.read_csv("/Users/jiarui/projects/assets_20211019.csv")
list_input = list(df['网站标题'])
set_word = list(set(list_input))
print(set_word)


# 寻找满足阈值的最长子串函数
def findString(list_input, threshold):
    biggest_score = 0
    longest_string = ''
    # 遍历去重后的list，并求出其中每两两字符串之间的最长子串，如果其长度比目前计算结果长并且大于阈值，则更新结果
    for i in range(len(set_word) - 1):

        for j in range(len(set_word) - i - 1):
            # 求最长子串
            longest_temp = find_lcsubstr(set_word[i], set_word[i + j + 1])
            if longest_temp != '':
                score = calculate_score(longest_temp, list_input)
            else:
                score = 0
            if len(longest_temp) >= len(longest_string) and score >= threshold:
                longest_string = longest_temp
                biggest_score = score
    print("longest string is " + longest_string)
    print("score is " + str(biggest_score))
    return longest_string


# 求最长公共子串函数
def find_lcsubstr(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return s1[p - mmax:p]  # 返回最长子串及其长度

# 计算分数函数，并与阈值做判断
def calculate_score(string_input, list_input):
    if_in = 0
    for title in list_input:
        if string_input in title:
            if_in += 1
    score = if_in / len(list_input)
    # print("the input string is {}, score is {}".format(string_input, score))
    return score


# 结果展示
print("result is {}".format(findString(list_input, 0.8)))
