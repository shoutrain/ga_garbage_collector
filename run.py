import random
import numpy as np


class Strategy(object):
    def __init__(self):
        # 0: move left
        # 1: move top
        # 2: move right
        # 3: move bottom
        # 4: move randomly
        # 5: do nothing
        # 6: pick garbage
        self.__action_num = 7

        self.__generate_route_table()

    def __generate_route_table(self):
        # 0: empty; 1: garbage; 2: wall
        # i: left; j: top; k: right; l: bottom; m: center
        self.__route_table = {}
        self.__gene_num = 0

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        for m in range(2):
                            route = f'{i}:{j}:{k}:{l}:{m}'
                            self.__route_table[route] = self.__gene_num
                            self.__gene_num += 1

    def action_num(self):
        return self.__action_num

    def gene_num(self):
        return self.__gene_num


class Square(object):
    def __init__(self, width, height):
        self.__square = np.random.randint(2, (width, height))

    def get_route(self, pos_x, pos_y):
        pass


class Collector(object):
    def __init__(self, strategy: Strategy, square: Square):
        self.__strategy = strategy
        self.__square = square
        self.__score = 0
        self.__cur_pos_x = 0
        self.__cur_pos_y = 0
        self.__generate_random_gene()

    def __generate_random_gene(self):
        self.__gene = []

        for _ in range(self.__strategy.gene_num()):
            self.__gene.append(
                random.randint(0, self.__strategy.action_num() - 1)
            )

    def gene(self):
        return self.__gene

    def score(self):
        return self.__score

    def action(self, square):
        route = square.get_route(self.__cur_pos_x, self.__cur_pos_y)
