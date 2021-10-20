# %%
from tools import Strategy, Square, Collector
import copy

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
best_score_per_generation = []  # 每代的最好成绩

# 更新换代
for g in range(GENERATION_NUM):
    if pre_best_collector is None:  # 第一代
        for i in range(COLLECTOR_NUM):
            cur_collectors.append(Collector(strategy, gene=None))
    else:  # 第二代以及以后
        for i in range(COLLECTOR_NUM):
            cur_collectors.append(
                Collector(strategy, gene=pre_best_collector.gene()))

    best_collector_index = None
    best_score = None

    # 轮询每个Collector
    for j in range(COLLECTOR_NUM):
        total_score = 0.0

        # 某个Collector在不同的Square上工作，计算成绩
        for k in range(SQUARE_NUM):
            collector = copy.copy(cur_collectors[i])
            collector.bind_square(squares[k])

            for _ in range(ACTION_STEP_NUM):
                collector.action()

            total_score += collector.score()

        average_score = total_score / SQUARE_NUM

        if best_score is None or average_score > best_score:
            best_score = average_score
            best_collector_index = j

    # 本代清理
    pre_best_collector = cur_collectors[best_collector_index]
    cur_collectors = []
    best_score_per_generation.append(best_score)

    print(f'generation #{g}\'s best score: {best_score}')
# %%
