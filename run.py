# %%
from tools import Strategy, Square, Collector
import numpy as np
import copy

SQUARE_WIDTH = 10
SQUARE_HEIGHT = 10
SQUARE_NUM = 100
COLLECTOR_NUM = 100
ACTION_STEP_NUM = 200

strategy = Strategy()
squares = []
collectors = []

for i in range(SQUARE_NUM):
    squares.append(Square(SQUARE_WIDTH, SQUARE_HEIGHT))

for i in range(COLLECTOR_NUM):
    collectors.append(Collector(strategy))

for i in range(COLLECTOR_NUM):
    total_score = 0.0

    for j in range(SQUARE_NUM):
        collector = copy.copy(collectors[i])
        collector.bind_square(squares[j])

        for k in range(ACTION_STEP_NUM):
            collector.action()

        total_score += collector.score()

    average_score = total_score / SQUARE_NUM
    print(f'Collector #{i + 1} got score: {average_score}')

# %%
