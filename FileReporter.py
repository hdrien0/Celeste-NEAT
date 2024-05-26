# adapted from neat-python stdout-reporter
# instead of printing to stdout, it writes the results to a file
# the file is named stats-{generation}.txt
# it also saves the best genome of each generation to a file named winner-{generation}.bin

import dill
import time
import os

from neat.reporting import BaseReporter
from neat.math_util import mean, stdev


class FileReporter(BaseReporter):

    def __init__(self, file_base_path, show_species_detail):
        self.show_species_detail = show_species_detail
        self.generation = None
        self.generation_start_time = None
        self.generation_times = []
        self.num_extinctions = 0
        self.file_base_path = file_base_path

        if not os.path.exists(file_base_path):
            os.makedirs(file_base_path)

    def log(self, msg):
        print(msg)
        with open(self.file_base_path + "stats-" + str(self.generation) + ".txt", "a") as f:
            f.write(msg + "\n")

    def start_generation(self, generation):
        self.generation = generation
        self.log('\n ****** Running generation {0} ****** \n'.format(generation))
        self.generation_start_time = time.time()

    def end_generation(self, config, population, species_set):
        ng = len(population)
        ns = len(species_set.species)
        if self.show_species_detail:
            self.log('Population of {0:d} members in {1:d} species:'.format(ng, ns))
            self.log("   ID   age  size   fitness   adj fit  stag")
            self.log("  ====  ===  ====  =========  =======  ====")
            for sid in sorted(species_set.species):
                s = species_set.species[sid]
                a = self.generation - s.created
                n = len(s.members)
                f = "--" if s.fitness is None else f"{s.fitness:.3f}"
                af = "--" if s.adjusted_fitness is None else f"{s.adjusted_fitness:.3f}"
                st = self.generation - s.last_improved
                self.log(f"  {sid:>4}  {a:>3}  {n:>4}  {f:>9}  {af:>7}  {st:>4}")

        else:
            self.log('Population of {0:d} members in {1:d} species'.format(ng, ns))

        elapsed = time.time() - self.generation_start_time
        self.generation_times.append(elapsed)
        self.generation_times = self.generation_times[-10:]
        average = sum(self.generation_times) / len(self.generation_times)
        self.log('Total extinctions: {0:d}'.format(self.num_extinctions))

        if len(self.generation_times) > 1:
            self.log("Generation time: {0:.3f} sec ({1:.3f} average)".format(elapsed, average))

        else:
            self.log("Generation time: {0:.3f} sec".format(elapsed))

    def post_evaluate(self, config, population, species, best_genome):
        # pylint: disable=no-self-use
        fitnesses = [c.fitness for c in population.values()]
        fit_mean = mean(fitnesses)
        fit_std = stdev(fitnesses)
        best_species_id = species.get_species_id(best_genome.key)
        self.log('Population\'s average fitness: {0:3.5f} stdev: {1:3.5f}'.format(fit_mean, fit_std))
        self.log(
            'Best fitness: {0:3.5f} - size: {1!r} - species {2} - id {3}'.format(best_genome.fitness,
                                                                                 best_genome.size(),
                                                                                 best_species_id,
                                                                                 best_genome.key))
        with open(self.file_base_path + f"winner-{self.generation}.bin", "wb") as f:
            dill.dump(best_genome, f)

    def complete_extinction(self):
        self.num_extinctions += 1
        self.log('All species extinct.')

    def found_solution(self, config, generation, best):
        self.log('\nBest individual in generation {0} meets fitness threshold - complexity: {1!r}'.format(
            self.generation, best.size()))

    def species_stagnant(self, sid, species):
        if self.show_species_detail:
            self.log("\nSpecies {0} with {1} members is stagnated: removing it".format(sid, len(species.members)))

    def info(self, msg):
        self.log(msg)