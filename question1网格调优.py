import pandas as pd

def is_zero(x):
    if x < 0:
        return x


matrix = pd.read_csv('data.csv', index_col=0)
classes = {}


# for _ in range(2):
def xxxx(weight):
    matrix = pd.read_csv('data.csv', index_col=0)
    classes = {}
    while len(matrix.index) > 1:
        # 转置
        matrix_new = matrix.T
        # 获取行标题
        cols = list(matrix_new.columns)
        index = cols[0]
        d = {}
        ans = []
        # 对列进行遍历并用第一列作差
        for i in range(1, matrix_new.shape[1]):
            matrix_new[cols[i]] = matrix_new[index] - matrix_new[cols[i]]
            # d[cols[i]] = [matrix_new2[cols[i]].tolist().count(-1),  matrix_new2[cols[i]] ]
            ans.append(matrix_new[cols[i]].tolist().count(-1))

        # print(len(ans))
        # 对第一列补充一个极大值
        ans = [200] + ans

        # 转置回来继续求解
        matrix_new = matrix_new.T
        # 将所有列与第一列差值作为新列
        matrix_new['cha'] = ans
        # 使用差值为主键排序
        matrix_new['sum'] = matrix['sum']

        matrix_new['cha'] = matrix_new['cha'] / matrix_new['sum'] - weight * matrix_new['sum'] / 150
        # matrix_new['sum'] = matrix_new['sum'].apply(lambda x:-x)
        matrix_new = matrix_new.sort_values(by=['cha'])

        # matrix_new = matrix_new.T
        matrix_new.drop(['cha'], axis=1, inplace=True)
        matrix_new = matrix_new.T

        cols = list(matrix_new.columns)
        rows = list(matrix_new.index)
        # 获取用过的列标
        used = []
        ls = [0] * len(matrix_new)
        for col in cols:
            value = matrix_new[col].tolist()
            # 取一个中间列表储存中间值，根据结果看是否要加入此列
            k = [ls[kkk] + value[kkk] for kkk in range(len(ls))]
            # 获取小于0值数量，即货物种类数量
            # print(col, len(list(filter(is_zero, k))))
            # print(matrix['sum'].loc[index])
            if len(list(filter(is_zero, k))) < 200 - matrix['sum'].loc[index]:
                ls = k
                used.append(col)
                classes[index] = classes.get(index, []) + [col]
            else:
                continue
        if index not in used:
            used += [index]
        print(len(classes.get(index,[])), end=' ')

        matrix.drop(used, axis=0, inplace=True)
    print('参数{}，批量总数{}：'.format(weight, len(classes)))


if __name__ == '__main__':
    ls = [0.05 * i for i in range(20)]
    for i in ls:
        xxxx(i)
