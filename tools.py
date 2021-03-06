import random
import copy
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

    def get_gene_index(self, left, top, right, bottom, center):
        route = f'{left}:{top}:{right}:{bottom}:{center}'
        return self.__route_table[route]


class Square(object):
    def __init__(self, width, height):
        self.__max_pos_x = width - 1
        self.__max_pos_y = height - 1
        self.__square = np.random.randint(2, size=(width, height))

    def __get_result(self, pos_x, pos_y):
        if pos_x < 0 or pos_x > self.__max_pos_x:
            return 2

        if pos_y < 0 or pos_y > self.__max_pos_y:
            return 2

        return self.__square[pos_x, pos_y]

    def max_pos_x(self):
        return self.__max_pos_x

    def max_pos_y(self):
        return self.__max_pos_y

    def get_route(self, pos_x, pos_y):
        left = self.__get_result(pos_x - 1, pos_y)
        top = self.__get_result(pos_x, pos_y - 1)
        right = self.__get_result(pos_x + 1, pos_y)
        bottom = self.__get_result(pos_x, pos_y + 1)
        center = self.__get_result(pos_x, pos_y)

        return left, top, right, bottom, center

    def clear(self, pos_x, pos_y):
        self.__square[pos_x, pos_y] = 0


class BreedingWay(object):
    def __init__(self, strategy: Strategy,  mutation_rate):
        self._strategy = strategy
        self._mutation_rate = mutation_rate

    def mutation_rate(self):
        return self._mutation_rate

    def bind_genes_with_scores(self, genes_with_scores):
        self._genes_with_scores = genes_with_scores
        self._genes_with_scores.sort(reverse=True)

    def breed(self):
        return None

    def _generate_mutation_gene(self, gene):
        mutation_num = int(self._strategy.gene_num() * self._mutation_rate)

        for _ in range(mutation_num):
            mutation_index = random.randint(0, self._strategy.gene_num() - 1)
            gene[mutation_index] = random.randint(
                0,
                self._strategy.action_num() - 1
            )

        return gene


class SingleBreeding(BreedingWay):
    def __init__(self, strategy: Strategy, mutation_rate):
        BreedingWay.__init__(self, strategy, mutation_rate)

    def breed(self):
        return self._generate_mutation_gene(self._genes_with_scores[0][1])


class CoupleBreeding(BreedingWay):
    def __init__(self, strategy: Strategy, mutation_rate):
        BreedingWay.__init__(self, strategy, mutation_rate)

    def bind_genes_with_scores(self, genes_with_scores):
        BreedingWay.bind_genes_with_scores(self, genes_with_scores)
        self.__generate_gene_rate_index()

    def breed(self):
        gene_1 = self.__find_gene_randomly()
        gene_2 = self.__find_gene_randomly()
        gene = self.__merge_two_gene_randomly(gene_1, gene_2)

        return self._generate_mutation_gene(gene)

    def __generate_gene_rate_index(self):
        self.__gene_rate_index = []
        collector_num = len(self._genes_with_scores)

        for i in range(collector_num):
            tmp = [i for _ in range(collector_num - i)]
            self.__gene_rate_index.extend(tmp)

        random.shuffle(self.__gene_rate_index)

    def __find_gene_randomly(self):
        random_index = random.randint(0, len(self.__gene_rate_index) - 1)
        random_index = self.__gene_rate_index[random_index]

        return self._genes_with_scores[random_index][1]

    def __merge_two_gene_randomly(self, gene_1, gene_2):
        gene = []
        split_pos = random.randint(1, self._strategy.gene_num() - 2)

        gene.extend(gene_1[:split_pos])
        gene.extend(gene_2[split_pos:])

        return gene


class Collector(object):
    def __init__(self, strategy: Strategy, breeding_way: BreedingWay = None):
        self.__strategy = strategy

        self.__score = 0
        self.__cur_pos_x = 0
        self.__cur_pos_y = 0

        if breeding_way is None:
            self.__generate_random_gene()
        else:
            self.__gene = breeding_way.breed()

    def __generate_random_gene(self):
        self.__gene = []

        for _ in range(self.__strategy.gene_num()):
            self.__gene.append(
                random.randint(0, self.__strategy.action_num() - 1)
            )

    def __move(self, action):
        if action == 0:  # move left
            if self.__cur_pos_x <= 0:
                self.__score -= 5
                self.__cur_pos_x = 0
            else:
                self.__cur_pos_x -= 1
        elif action == 1:  # move top
            if self.__cur_pos_y <= 0:
                self.__score -= 5
                self.__cur_pos_y = 0
            else:
                self.__cur_pos_y -= 1
        elif action == 2:  # move right
            if self.__cur_pos_x >= self.__square.max_pos_x():
                self.__score -= 5
                self.__cur_pos_x = self.__square.max_pos_x()
            else:
                self.__cur_pos_x += 1
        elif action == 3:  # move bottom
            if self.__cur_pos_y >= self.__square.max_pos_y():
                self.__score -= 5
                self.__cur_pos_y = self.__square.max_pos_y()
            else:
                self.__cur_pos_y += 1

    def gene(self):
        return self.__gene

    def score(self):
        return self.__score

    def reset_score(self):
        self.__score = 0

    def bind_square(self, square):
        self.__square = copy.copy(square)

    def action(self):
        left, top, right, bottom, center = self.__square.get_route(
            self.__cur_pos_x, self.__cur_pos_y)
        gene_index = self.__strategy.get_gene_index(
            left, top, right, bottom, center)
        action = self.__gene[gene_index]

        if action < 4:  # move accordingly
            self.__move(action)
        elif action == 4:  # move randomly
            self.__move(random.randint(0, 3))
            pass
        elif action == 5:  # do nothing
            pass
        elif action == 6:  # pick garbage
            if center == 0:
                self.__score -= 1
            else:
                self.__square.clear(self.__cur_pos_x, self.__cur_pos_y)
                self.__score += 10
