# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from multiprocessing import Pool
import random

import warnings


def initpara():
    alpha = 0.99
    t = (1, 100)
    markovlen = 1000
    return alpha, t, markovlen


def result3(indexs):

    warnings.filterwarnings('ignore')
    with open('result59.csv', 'r') as f:
        lines = f.readlines()

    data = []

    for line in lines:
        line = line.strip("'\n ").split(',')
        data.append(line)
    with open('result.txt', 'r') as f:
        lines = f.readlines()
    d = {}
    for line in lines:
        line = line.strip()
        d[line.split()[0]] = line.split()[1].split(',')

    matrix = pd.read_csv('met.csv', index_col=0)

    matrix = matrix.loc[data[indexs]]
    matrix = matrix[d.get(str(indexs))]

    matrix = matrix.T

    right = matrix.apply(lambda k: len(list(k)) - list(k)[::-1].index(1)).tolist()
    left = matrix.apply(lambda k: list(k).index(1) + 1).tolist()
    pos = [[left[j], right[j], data[0][j]] for j in range(len(left))]

    # 模拟退火算法
    # =================初始化参数============
    num = len(pos)

    solutionnew = []
    solutioncurrent = solutionnew.copy()
    valuecurrent = 990000

    solutionbest = solutionnew.copy()
    valuebest = 990000  # np.max

    alpha, t2, markovlen = initpara()
    t = t2[1]

    result = []  # 记录迭代过程当中的最优解
    while t > 1:
        for i in range(markovlen):
            # 订单起止区间信息
            ls = pos
            # 记录员工位置信息
            order = [[], [], [], [], []]

            # np.random.rand()产生[0, 1)区间的均匀随机数
            while True:  # 产生两个不一样的随机数

                loc1 = random.randint(0, num - 1)
                loc2 = random.randint(0, num - 1)
                loc3 = random.randint(0, num - 1)
                loc4 = random.randint(0, num - 1)
                loc5 = random.randint(0, num - 1)

                if len(set([loc1, loc2, loc3, loc4, loc5])) == 5:
                    used = [loc1, loc2, loc3, loc4, loc5]
                    # print(used)
                    break

            loc = [loc1, loc2, loc3, loc4, loc5]
            dis = [0, 0, 0, 0, 0]
            # 完成第一个订单需要移动距离
            for i in range(5):
                dis[i] += ls[loc[i]][1]

            # 订单选取信息
            for i in range(5):
                order[i].append(ls[loc[i]][2])

            # 完成第一个订单员工位置
            new = [loc1, loc2, loc3, loc4, loc5]

            while len(used) < len(ls):
                mins = min(dis)
                index = dis.index(mins)

                up_min = [1000, 0, 0]

                for i in range(len(ls)):
                    if i not in used:
                        if abs(ls[i][0] - new[index]) < up_min[0]:
                            up_min[0] = abs(ls[i][0] - new[index])
                            up_min[1] = i
                            up_min[2] = 0
                        if abs(ls[i][1] - new[index]) < up_min[0]:
                            up_min[0] = abs(ls[i][0] - new[index])
                            up_min[1] = i
                            up_min[2] = 1
                # 更新总距离
                dis[index] += up_min[0] + abs(ls[up_min[1]][1] - ls[up_min[1]][0])
                # 更新那单顺序
                order[index].append(ls[up_min[1]][2])
                # 更新完成订单后位置信息
                new[index] = ls[up_min[1]][1 - up_min[2]]

                used.append(up_min[1])
            for i in range(5):
                dis[i] += new[i]
            valuenew = max(dis)

            # print (valuenew)
            if valuenew < valuecurrent:  # 接受该解

                # 更新solutioncurrent 和solutionbest
                valuecurrent = valuenew
                solutioncurrent = order.copy()

                if valuenew < valuebest:
                    valuebest = valuenew
                    solutionbest = order.copy()
            else:  # 按必定的几率接受该解
                if np.random.rand() < np.exp(-(valuenew - valuecurrent) / t):
                    valuecurrent = valuenew
                    solutioncurrent = order.copy()
                else:
                    order = solutioncurrent.copy()

        t = alpha * t
        result.append(valuebest)
        print('\r' + str(t), end='')  # 程序运行时间较长，打印t来监视程序进展速度

    with open('result4.txt', 'a', encoding='GBK') as f:
        for i in range(5):
            f.write(str(indexs + 1) + ' ' + str(i + 1) + ' ' + ','.join(solutionbest[i]) + '\n')


from multiprocessing import Pool

if __name__ == '__main__':
    p = Pool(48)  # 创建一个进程池，最大进程数5
    for i in range(0, 59):
        p.apply_async(result3, args=(i,))  # apply_async(要调用的目标,args=(传递的参数,))
    p.close()  # 关闭进程池，关闭后进程池不再接受新的请求
    p.join()  # 等待所有子进程执行完毕，必须放在close语句后
