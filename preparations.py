
import mapel.elections as mapel

import os
import csv

import numpy as np
from mapel.core.matchings import solve_matching_vectors


def compute_normalized_distances(experiment, list_of_rules, distance_id):

    experiment.import_committees(list_of_rules=list_of_rules)

    path = os.path.join(os.getcwd(), "experiments", f'{experiment_id}/rules_output',
                        'distances', f'{distance_id}.csv')

    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["election_id_1", "election_id_2", "distance", "time"])

        all_results = {r1: {r2: [] for r2 in list_of_rules} for r1 in list_of_rules}

        for election_id in experiment.elections:
            print(election_id)

            tmp_results = {r1: {} for r1 in list_of_rules}
            tmp_list = []

            for i, r1 in enumerate(list_of_rules):
                for j, r2 in enumerate(list_of_rules):
                    if i < j:

                        com1 = experiment.all_winning_committees[r1][
                            election_id][0]
                        com2 = experiment.all_winning_committees[r2][
                            election_id][0]

                        if distance_id in ['norm_jaccard']:
                            cand_dist = np.zeros([committee_size,
                                                  committee_size])

                            experiment.elections[election_id].compute_reverse_approvals()
                            for k1, c1 in enumerate(com1):
                                for k2, c2 in enumerate(com2):

                                    ac1 = experiment.elections[election_id].reverse_approvals[c1]
                                    ac2 = experiment.elections[election_id].reverse_approvals[c2]
                                    if distance_id == 'norm_jaccard':
                                        if len(ac1.union(ac2)) != 0:
                                            cand_dist[k1][k2] = 1 - len(ac1.intersection(ac2))/len(ac1.union(ac2))
                            distance, _ = solve_matching_vectors(cand_dist)
                            distance /= committee_size

                        tmp_results[r1][r2] = distance
                        tmp_list.append(distance)

            max_dist = max(tmp_list)
            if max_dist == 0:
                max_dist = 1

            for i, r1 in enumerate(list_of_rules):
                for j, r2 in enumerate(list_of_rules):
                    if i < j:
                        norm_result = tmp_results[r1][r2] / max_dist
                        all_results[r1][r2].append(norm_result)

        for i, r1 in enumerate(list_of_rules):
            for j, r2 in enumerate(list_of_rules):
                if i < j:
                    mean = sum(all_results[r1][r2]) / experiment.num_elections
                    writer.writerow([r1, r2, mean, 0.])


if __name__ == "__main__":

    committee_size = 10
    distance_id = 'norm_jaccard'

    names = ['disjoint', 'resampling', '1d', '2d', 'partylist', 'pabulib']

    list_of_rules = ["av", "cc", "sav", "pav", "slav", "seqpav", "seqslav",
                     "seqcc", "seqphragmen", "greedy-monroe", "rule-x",
                     "geom2", "geom3", "geom4", "geom5", "minimaxav"]

    for name in names:
        experiment_id = f'{name}'

        experiment = mapel.prepare_offline_approval_experiment(
            experiment_id=f'{experiment_id}/rules_input',
            distance_id=distance_id)
        experiment.prepare_elections()
        experiment.compute_rules(list_of_rules=list_of_rules, committee_size=committee_size,
                                 printing=False, resolute=True)

        compute_normalized_distances(experiment, list_of_rules, distance_id)


