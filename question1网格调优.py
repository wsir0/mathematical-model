from multiprocessing import Pool
import pandas as pd


def is_zero(x):
    if x < 0:
        return x


matrix = pd.read_csv('data.csv', index_col=0)
classes = {}


def xxxx(weight):
    matrix = pd.read_csv('data.csv', index_col=0)
    classes = {}
    while len(matrix.index) > 1:
        # 转置
        matrix_new = matrix.T
        # 获取行标题
        cols = list(matrix_new.columns)
        index = cols[0]

        # 对列进行遍历并用第一列作差
        for i in range(1, matrix_new.shape[1]):
            matrix_new[cols[i]] = matrix_new[index] - matrix_new[cols[i]]
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
        # 获取用过的列标
        used = []
        ls = [0] * len(matrix_new)
        for col in cols:
            value = matrix_new[col].tolist()
            # 取一个中间列表储存中间值，根据结果看是否要加入此列
            k = [ls[kkk] + value[kkk] for kkk in range(len(ls))]
            # 获取小于0值数量，即货物种类数量
            if len(list(filter(is_zero, k))) < 200 - matrix['sum'].loc[index]:
                ls = k
                used.append(col)
                classes[index] = classes.get(index, []) + [col]
            else:
                continue
        if index not in used:
            used += [index]
        print(len(classes.get(index, [])), end=' ')

        matrix.drop(used, axis=0, inplace=True)
    return weight, len(classes), classes
    print('参数{}，批量总数{}：'.format(weight, len(classes)))


def add(classes, d):
    # 加上之前预处理掉的部分订单
    for i in d:
        for key in classes:
            if i in classes[key]:
                classes[key] = classes[key] + d[i]
                break
    return classes


def result1_save():
    # 读取之前保存结果并按照赛题要求格式转存
    with open('result59.csv', 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        line = line.strip("'\n ").split(',')
        data.append(line)

    with open('result1.csv', 'w') as f:
        for i in range(len(data)):
            for j in range(len(data[i])):
                f.write(str(data[i][j]) + ',' + str(i + 1) + '\n')


def main():
    ls = [0.05 * i for i in range(20)]
    '''
    # 多进程操作
    p = Pool(5)  # 创建一个进程池，最大进程数5
    for i in range(0, 40):
        p.apply_async(xxxx, args=(i,))  # apply_async(要调用的目标,args=(传递的参数,))
    p.close()  # 关闭进程池，关闭后进程池不再接受新的请求
    p.join()  # 等待所有子进程执行完毕，必须放在close语句后'''

    # 最优解初始值
    best_result = [-1, 10000, []]

    for i in ls:
        result = xxxx(i)
        if result[1] < best_result[1]:
            best_result = result

    d = dict([('D0148', ['D0614', 'D0126', 'D0026', 'D0212', 'D0243']), ('D0190', ['D0318', 'D0110', 'D0092', 'D0091']),
              ('D0031', ['D0188', 'D0003']), ('D0175', ['D0002']), ('D0145', ['D0800']), ('D0029', ['D0245', 'D0205']),
              ('D0006', ['D0260']), ('D0194', ['D0019', 'D0043']), ('D0133', ['D0042']), ('D0280', ['D0146']),
              ('D0085', ['D0119']), ('D0224', ['D0158']), ('D0244', ['D0514']), ('D0281', ['D0221']),
              ('D0261', ['D0414']), ('D0066', ['D0600']), ('D0178', ['D0140', 'D0078']), ('D0228', ['D0530']),
              ('D0226', ['D0162', 'D0169']), ('D0153', ['D0101']), ('D0027', ['D0215']),
              ('D0441', ['D0112', 'D0105', 'D0045', 'D0044']), ('D0176', ['D0106']), ('D0806', ['D0009']),
              ('D0711', ['D0152']), ('D0466', ['D0840']), ('D0675', ['D0442']), ('D0350', ['D0005']),
              ('D0147', ['D0142', 'D0166']), ('D0248', ['D0168']), ('D0672', ['D0122'])])
    # 获取分类结果
    classes = best_result[2]

    # 加上之前预处理掉的部分订单
    classes = add(classes, d)

    # 将结果保存
    with open('./result59.csv', 'w') as f:
        for i in classes.values():
            f.write(','.join(i) + '\n')
    result1_save()


if __name__ == '__main__':
    main()
