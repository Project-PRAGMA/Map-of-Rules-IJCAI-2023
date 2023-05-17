import mapel.elections as mapel

import os
import csv

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

        exp_output = mapel.prepare_experiment(experiment_id=f'{experiment_id}/rules_output',
                                              instance_type='rule', distance_id=distance_id,
                                              embedding_id=embedding_id)
        exp_output.print_matrix(
            saveas=f'matrix/{experiment_id}', dpi=200, rounding=2)
