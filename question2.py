# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from multiprocessing import Pool

#获得距离矩阵的函数
def getdistmat(columns, matrix):
    matrix = matrix[columns]
    matrix = matrix.T
    ls = matrix.apply(lambda k: len(list(k)) - 1 - list(k)[::-1].index(1) - list(k).index(1))
    matrix = matrix.T
    dis = sum(ls)

    return dis, matrix


def initpara():
    alpha = 0.99
    t = (1, 100)
    markovlen = 1000
    return alpha, t, markovlen

def renwu(index):
    with open('result59.csv', 'r') as f:
        lines = f.readlines()

    data = []

    for line in lines:
        line = line.strip("'\n ").split(',')
        data.append(line)

    matrix = pd.read_csv('met.csv', index_col=0)
    col = data[index]
    matrix = matrix.loc[col]
    matrix = matrix.T
    matrix['sum'] = matrix.sum(axis=1)
    ls = []
    for i in matrix.index:
        if matrix.loc[i]['sum'] == 0:
            ls.append(i)
    matrix.drop(['sum'], axis=1, inplace=True)
    matrix.drop(ls, axis=0, inplace=True)
    matrix = matrix.T


    lens = list(matrix.columns)
    lens

    # 模拟退火算法
    ans = np.arange(matrix.shape[1])
    #=================初始化参数============
    num = matrix.shape[1]

    solutionnew = list(matrix.columns)
    solutioncurrent = solutionnew.copy()
    valuecurrent = 990000

    solutionbest = solutionnew.copy()
    valuebest = 990000  #np.max

    alpha, t2, markovlen = initpara()
    t = t2[1]

    result = []  #记录迭代过程当中的最优解
    while t > 1:
        for i in np.arange(markovlen):

            #下面的两交换和三角换是两种扰动方式，用于产生新解
            if np.random.rand() > 0.5:  # 交换路径中的这2个节点的顺序
                # np.random.rand()产生[0, 1)区间的均匀随机数
                while True:  #产生两个不一样的随机数
                    loc1 = np.int(np.ceil(np.random.rand() * (num - 1)))
                    loc2 = np.int(np.ceil(np.random.rand() * (num - 1)))
                    ## print(loc1,loc2)
                    if loc1 != loc2:
                        break
                solutionnew[loc1], solutionnew[loc2] = solutionnew[loc2], solutionnew[loc1]
            else:  #三交换
                while True:
                    loc1 = np.int(np.ceil(np.random.rand() * (num - 1)))
                    loc2 = np.int(np.ceil(np.random.rand() * (num - 1)))
                    loc3 = np.int(np.ceil(np.random.rand() * (num - 1)))

                    if ((loc1 != loc2) & (loc2 != loc3) & (loc1 != loc3)):
                        break

                # 下面的三个判断语句使得loc1<loc2<loc3
                if loc1 > loc2:
                    loc1, loc2 = loc2, loc1
                if loc2 > loc3:
                    loc2, loc3 = loc3, loc2
                if loc1 > loc2:
                    loc1, loc2 = loc2, loc1

                #下面的三行代码将[loc1,loc2)区间的数据插入到loc3以后
                tmplist = solutionnew[loc1:loc2].copy()
                solutionnew[loc1:loc3 - loc2 + 1 + loc1] = solutionnew[loc2:loc3 + 1].copy()
                solutionnew[loc3 - loc2 + 1 + loc1:loc3 + 1] = tmplist.copy()

            valuenew, matrix = getdistmat(solutionnew, matrix)

            # print (valuenew)
            if valuenew < valuecurrent:  #接受该解

                #更新solutioncurrent 和solutionbest
                valuecurrent = valuenew
                solutioncurrent = solutionnew.copy()

                if valuenew < valuebest:
                    valuebest = valuenew
                    solutionbest = solutionnew.copy()
            else:  #按必定的几率接受该解
                if np.random.rand() < np.exp(-(valuenew - valuecurrent) / t):
                    valuecurrent = valuenew
                    solutioncurrent = solutionnew.copy()
                else:
                    solutionnew = solutioncurrent.copy()
        t = alpha * t
        result.append(valuebest)
        print('\r' + str(t), end='')  #程序运行时间较长，打印t来监视程序进展速度

    print(getdistmat(solutionbest, matrix)[0])

    with open('result2.txt', 'a', encoding='GBK') as f:
        f.write(str(index) + ' ' + ','.join(solutionbest) + '\n')

from multiprocessing import Pool

if __name__ == '__main__':
    p = Pool(5)#创建一个进程池，最大进程数5
    for i in range(0, 40):
        p.apply_async(renwu, args=(i,))#apply_async(要调用的目标,args=(传递的参数,))
    p.close()#关闭进程池，关闭后进程池不再接受新的请求
    p.join()#等待所有子进程执行完毕，必须放在close语句后

