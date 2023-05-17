import itertools

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import stats

import mapel.elections as mapel

import os
import csv

from mapel.core.matchings import solve_matching_vectors



if __name__ == "__main__":

    committee_size = 10
    distance_id = 'norm_jaccard'
    embedding_id = 'kamada'

    names = ['disjoint', 'resampling', '1d', '2d', 'partylist', 'pabulib']

    list_of_rules = ["av", "cc", "sav", "pav", "slav", "seqpav", "seqslav",
                     "seqcc", "seqphragmen", "greedy-monroe", "rule-x",
                     "geom2", "geom3", "geom4", "geom5", "minimaxav"]

    for name in names:
        experiment_id = f'{name}'

        experiment = mapel.prepare_experiment(experiment_id=f'{experiment_id}/rules_output',
                                              instance_type='rule', distance_id=distance_id,
                                              embedding_id=embedding_id)

        experiment.embed(algorithm=embedding_id, zero_distance=0.001)

        experiment.print_map(
            textual=list_of_rules,
            legend=False,
        )
