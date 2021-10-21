from tools import Strategy, Square, Collector
from tools import BreedingWay, SingleBreeding, CoupleBreeding
from multiprocessing import Pool, Manager
import matplotlib.pyplot as plt
import sys

PROCESSOR_NUM = 8  # 进程数量
SQUARE_WIDTH = 10  # 广场宽度
SQUARE_HEIGHT = 10  # 广场高度
SQUARE_NUM = 100  # 广场数量
COLLECTOR_NUM = 100  # 垃圾回收机器人个数
ACTION_STEP_NUM = 200  # 垃圾回收机器人一次清扫行动步数
GENERATION_NUM = 1000  # 遗传代数
MUTATION_RATE = 0.01  # 变异率


def collector_work(collector: Collector, squares: list, scores_with_genes: list):
    '''某个Collector在不同的Square上工作，计算平均成绩'''

    total_score = 0.0

    for i in range(SQUARE_NUM):
        collector.reset_score()
        collector.bind_square(squares[i])

        for _ in range(ACTION_STEP_NUM):
            collector.action()

        total_score += collector.score()

    average_score = total_score / SQUARE_NUM
    scores_with_genes.append([average_score, collector.gene()])


def generation_work(generation, pre_genes_with_scores: list, breeding_way: BreedingWay):
    '''每一代开始工作'''

    cur_collectors = []

    if len(pre_genes_with_scores) == 0:  # 第一代
        for _ in range(COLLECTOR_NUM):
            cur_collectors.append(Collector(strategy))
    else:  # 第二代及以后
        breeding_way.bind_genes_with_scores(pre_genes_with_scores)
        for _ in range(COLLECTOR_NUM):
            collector = Collector(strategy, breeding_way=breeding_way)
            cur_collectors.append(collector)

    manager = Manager()
    pool = Pool(processes=PROCESSOR_NUM)
    scores_with_genes = manager.list()

    # 轮询每个Collector
    for j in range(COLLECTOR_NUM):
        pool.apply_async(
            collector_work,
            (cur_collectors[j], squares, scores_with_genes)
        )

    pool.close()
    pool.join()

    # 本代清理
    best_score = max(scores_with_genes)[0]
    print(f'generation #{generation + 1}\'s best score: {best_score}')

    return scores_with_genes, best_score


if __name__ == '__main__':
    cmd = 'python ./run.py [breeding way: 1-single breeding; 2-couple breeding]'

    if len(sys.argv) != 2:
        print(f'Usage: {cmd}')
        exit(1)

    strategy = Strategy()
    squares = []

    for i in range(SQUARE_NUM):
        squares.append(Square(SQUARE_WIDTH, SQUARE_HEIGHT))

    breeding_way = None
    algorithm_name = ''

    if sys.argv[1] == '1':
        breeding_way = SingleBreeding(strategy, mutation_rate=MUTATION_RATE)
        algorithm_name = 'Single Breeding'
    elif sys.argv[1] == '2':
        breeding_way = CoupleBreeding(strategy, mutation_rate=MUTATION_RATE)
        algorithm_name = 'Couple Breeding'

    if breeding_way is None:
        print(f'Usage: {cmd}')
        exit(1)

    best_scores = []
    pre_genes_with_scores = []

    # 更新换代
    for g in range(GENERATION_NUM):
        pre_genes_with_scores, best_score = generation_work(
            g, pre_genes_with_scores, breeding_way)
        best_scores.append(best_score)

    # 画进化分数图
    x = []
    y = []

    for key, value in enumerate(best_scores):
        x.append(key + 1)
        y.append(value)

    plt.title(f'GA({algorithm_name}) Demo: Garbage Collector\'s Evolution')
    plt.xlabel('generations')
    plt.ylabel('scores')
    plt.plot(x, y, label='evolutionary score curve')
    plt.legend()
    plt.show()
