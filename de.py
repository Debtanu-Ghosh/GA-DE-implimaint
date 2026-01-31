import random
import numpy as np
import os

class de:
    def __init__(self, cr, f, np, mu_stra, gen, N):
        self.cr = cr
        self.f = f
        self.np = np
        self.mu = mu_stra
        self.g = gen
        self.ep = N
        self.hp = {}

    def generate_candidate(self):
        candidate = {}
        for param in self.hp.keys():
            if self.hp[param]["type"] == "float":
                candidate[param] = random.uniform(self.hp[param]["low"], self.hp[param]["high"])
            elif self.hp[param]["type"] == "int" or self.hp[param]["type"] == "choice":
                candidate[param] = random.randint(self.hp[param]["low"], self.hp[param]["high"])
        return candidate
    
    def inpop(self):
        return [{"candidate": self.generate_candidate(), "score": float("inf"), "Acc": 0} for _ in range(self.np)]
    
    def fitness(self, trial_vector, ep):
        pass
    
    def clamp(self):
        pass
    
    def print_population(self, population):
        for p in population:
            print(f"{p['score']:.4f}", end=" -> ")
            print(f"{p['Acc']:.4f}", end = " -> ")
            self.print_candidate(p['candidate'])
    
    def print_candidate(self, candidate):
        readable_candidate = {}
        for param in candidate.keys():
            if self.hp[param]["type"] == "choice":
                choice = candidate[param]
                readable_candidate[param] = self.hp[param]["choices"][choice]
            else:
                readable_candidate[param] = candidate[param]
        print(readable_candidate)
        

    def mutation(self, population, i, strategy="rand/1"):

        target_vector = population[i]["candidate"]

        choices = list(range(0, i)) + list(range(i + 1, self.np))
        best_vector = population[0]["candidate"]

        # -------------------------------
        # SELECT INDICES
        # -------------------------------
        if strategy == "rand/1":
            a, b, c = np.random.choice(choices, 3, replace=False)
            x1 = population[a]["candidate"]
            x2 = population[b]["candidate"]
            x3 = population[c]["candidate"]

        elif strategy == "best/1":
            a, b = np.random.choice(choices, 2, replace=False)
            x1 = best_vector
            x2 = population[a]["candidate"]
            x3 = population[b]["candidate"]

        elif strategy == "current-to-best/1":
            a, b = np.random.choice(choices, 2, replace=False)
            x1 = target_vector
            x2 = best_vector
            x3 = population[a]["candidate"]
            x4 = population[b]["candidate"]

        elif strategy == "rand/2":
            a, b, c, d, e = np.random.choice(choices, 5, replace=False)
            x1 = population[a]["candidate"]
            x2 = population[b]["candidate"]
            x3 = population[c]["candidate"]
            x4 = population[d]["candidate"]
            x5 = population[e]["candidate"]

        else:
            raise ValueError(f"Unknown mutation strategy: {strategy}")

        # -------------------------------
        # MUTATION
        # -------------------------------
        donor_vector = {}

        for param in target_vector.keys():

            if strategy == "rand/1":
                value = x1[param] + self.f * (x2[param] - x3[param])

            elif strategy == "best/1":
                value = x1[param] + self.f * (x2[param] - x3[param])

            elif strategy == "current-to-best/1":
                value = (
                    x1[param]
                    + self.f * (x2[param] - x1[param])
                    + self.f * (x3[param] - x4[param])
                )

            elif strategy == "rand/2":
                value = (
                    x1[param]
                    + self.f * (x2[param] - x3[param])
                    + self.f * (x4[param] - x5[param])
                )

            # -------------------------------
            # TYPE HANDLING
            # -------------------------------
            if self.hp[param]["type"] in ("int", "choice"):
                value = round(value)

            # -------------------------------
            # BOUNDARY CONTROL
            # -------------------------------
            value = self.clamp(value,
                            self.hp[param]["low"],
                            self.hp[param]["high"])

            donor_vector[param] = value

        print(f"Mutation strategy: {strategy}")
        print("donor_vector:", end=" ")
        self.print_candidate(donor_vector)

        return donor_vector

    def crossover(self, donor_vector, target_vector):
        keep_param = random.choice(list(target_vector.keys()))      # R: random param to always keep
        trial_vector = {}
        for param in target_vector.keys():
            r = random.random()
            if r < self.cr or param == keep_param:
                trial_vector[param] = donor_vector[param]
            else:
                trial_vector[param] = target_vector[param]

    def run_de(self):
        population = self.inpop()
        best_candidate, best_score, best_Acc = self.fitness(population, self.ep)
        for G in range(self.g):
            print(f"=========================[ GENERATION {G+1:2d} ]=========================")
            for i in range(len(population)):
                print(f"-------------------------[ CANDIDATE  {i+1:2d} ]-------------------------")
                target_vector = population[i]["candidate"]
                print("target_vector:", end=" ")
                self.print_candidate(target_vector)

                donor_vector = self.mutation(population=population,
                                             i=i,
                                             strategy=self.mu)

                # # GENERATE
                # choices = list(range(0, i)) + list(range(i+1, self.np))  # make chance of picking ith candidate 0
                # a, b, c = np.random.choice(choices, 3, replace=False)

                # x1 = population[a]["candidate"]
                # x2 = population[b]["candidate"]
                # x3 = population[c]["candidate"]

                # # MUTATION
                # donor_vector = {}
                # for param in target_vector.keys():
                #     donor_vector[param] = x1[param] + self.f * (x2[param] - x3[param])
                #     if self.hp[param]["type"] in ("int", "choice"):
                #         donor_vector[param] = round(donor_vector[param])
                #     donor_vector[param] = self.clamp(donor_vector[param], self.hp[param]["low"], self.hp[param]["high"])

                # print("donor_vector:", end=" ")
                # self.print_candidate(donor_vector)

                # CROSSOVER
                trial_vector = self.crossover(donor_vector=donor_vector, target_vector=target_vector)
                # keep_param = random.choice(list(target_vector.keys()))      # R: random param to always keep
                # trial_vector = {}
                # for param in target_vector.keys():
                #     r = random.random()
                #     if r < self.cr or param == keep_param:
                #         trial_vector[param] = donor_vector[param]
                #     else:
                #         trial_vector[param] = target_vector[param]

                # print("trial_vector:", end=" ")
                # self.print_candidate(trial_vector)

                # EVALUATE
                trial_score, trial_acc = self.fitness(trial_vector, self.ep)
                if trial_score < population[i]["score"]:
                    print(f"{trial_score:0.5f} < {population[i]['score']:0.5f}, picking trial_vector")
                    population[i]["candidate"] = trial_vector
                    population[i]["score"] = trial_score
                    population[i]["Acc"] = trial_acc
                else:
                    print(f"{trial_score:0.5f} >= {population[i]['score']:0.5f}, keeping target_vector")

                    # FIND BEST TILL NOW
            best_index = np.argmin([c["score"] for c in population])
            new_best_score = population[best_index]["score"]
            new_best_acc = population[best_index]["Acc"]
            if new_best_score < best_score:
                print(f"Best score improved from {best_score:0.4f} to {new_best_score:0.4f}")
                best_score = new_best_score
                best_Acc = new_best_acc
                best_candidate = population[best_index]["candidate"]
                print("Best candidate: ", end="")
                self.print_candidate(best_candidate)
        return best_Acc, best_candidate
