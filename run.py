# %%
from tools import Strategy, Square, Collector
import copy
from multiprocessing import Pool, Manager, managers

PROCESSOR_NUM = 8
SQUARE_WIDTH = 10
SQUARE_HEIGHT = 10
SQUARE_NUM = 100
COLLECTOR_NUM = 100
ACTION_STEP_NUM = 200
GENERATION_NUM = 1000

strategy = Strategy()
squares = []

for i in range(SQUARE_NUM):
    squares.append(Square(SQUARE_WIDTH, SQUARE_HEIGHT))

pre_best_collector = None  # 上一代分数最高的Collector
cur_collectors = []


def collector_work(collector, squares, scores):
    '''某个Collector在不同的Square上工作，计算平均成绩'''

    total_score = 0.0

    for i in range(SQUARE_NUM):
        collector.reset_score()
        collector.bind_square(squares[i])

        for _ in range(ACTION_STEP_NUM):
            collector.action()

        total_score += collector.score()

    average_score = total_score / SQUARE_NUM
    scores.append(average_score)

    print(f'finished with score: {average_score}')


# 更新换代
for g in range(GENERATION_NUM):
    if pre_best_collector is None:  # 第一代
        for i in range(COLLECTOR_NUM):
            cur_collectors.append(
                Collector(strategy, mother=None, father=None))
    else:  # 第二代以及以后
        for i in range(COLLECTOR_NUM):
            cur_collectors.append(
                Collector(
                    strategy,
                    mother=pre_best_collector.gene(),
                    father=None
                )
            )

    best_collector_index = None
    best_score = None

    manager = Manager()
    scores = manager.list()
    pool = Pool(processes=PROCESSOR_NUM)

    # 轮询每个Collector
    for j in range(COLLECTOR_NUM):
        pool.apply_async(collector_work, (cur_collectors[j], squares, scores))

    pool.close()
    pool.join()

    # 本代清理
    best_score = max(scores)
    best_score_index = scores.index(best_score)
    pre_best_collector = cur_collectors[best_score_index]
    cur_collectors = []

    print(f'generation #{g}\'s best score: {best_score}')
# %%
