import mapel.elections as mapel

from inner_functions import test_priceability, test_core


def print_values(experiment, list_of_rules, feature_id, column_id):

    features = {}
    for rule in list_of_rules:
        features[rule] = experiment.import_feature(feature_id, rule=rule, column_id=column_id)

    results = {}
    for rule in list_of_rules:
        feature = features[rule]
        total_value = 0
        ctr = 0
        for instance in feature:
            total_value += feature[instance]
            ctr += 1
        avg_value = 0
        if ctr != 0:
            avg_value = round(total_value / ctr, 2)
        results[rule] = avg_value

    for rule in list_of_rules:
        print(rule, end=" ")
        print(f'& {results[rule]}', end=" ")
        print("")


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

        experiment = mapel.prepare_offline_approval_experiment(
            experiment_id=f'{experiment_id}/rules_input',)

        experiment.add_feature('priceability', test_priceability)
        experiment.add_feature('core', test_core)

        experiment.import_committees(list_of_rules=list_of_rules)

        for election_id in experiment.elections:
            experiment.elections[election_id].winning_committee = {}

        for r in list_of_rules:
            for election_id in experiment.elections:
                experiment.elections[election_id].winning_committee[r] = \
                experiment.all_winning_committees[r][election_id][0]

            experiment.compute_feature(feature_id='ejr', feature_params={'rule': r})
            experiment.compute_feature(feature_id='core', feature_params={'rule': r})
            experiment.compute_feature(feature_id='priceability', feature_params={'rule': r})

        print("\nPriceability")
        print_values(experiment, list_of_rules, 'priceability', 'value')
        print("\nCore")
        print_values(experiment, list_of_rules, 'core', 'value')
        print("\nEJR")
        print_values(experiment, list_of_rules, 'ejr', 'ejr')
        print("\nPJR")
        print_values(experiment, list_of_rules, 'ejr', 'pjr')
        print("\nJR")
        print_values(experiment, list_of_rules, 'ejr', 'jr')