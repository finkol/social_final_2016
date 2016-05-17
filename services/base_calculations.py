from __future__ import division

from services.soda_api import get_data

count_of_every_felony_response = get_data(select="count(offense)")
list_of_offenses_response = get_data(select="offense", group="offense")
list_of_offenses = [x['offense'] for x in list_of_offenses_response]
count_of_every_felony = int(count_of_every_felony_response[0]['count_offense'])
offense_count = get_data(select="offense, count(offense)", group="offense")

offense_count_by_borough = get_data(select="borough, count(offense)", group="borough")
offense_count_by_borough = [x for x in offense_count_by_borough if 'borough' in x]
offense_count_by_borough = [x for x in offense_count_by_borough if x['borough'] not in ('NA', '(null)', None)]

offense_count_by_borough_and_offense = get_data(select="offense, borough, count(offense)", group="borough, offense")
offense_count_by_borough_and_offense = [x for x in offense_count_by_borough_and_offense if 'borough' in x]
offense_count_by_borough_and_offense = [x for x in offense_count_by_borough_and_offense if
                                        x['borough'] not in ('NA', '(null)', None)]

boroughs = get_data(select="borough", group="borough")
boroughs = [x['borough'] for x in boroughs[1:]]
boroughs = [x for x in boroughs if x not in ('NA', '(null)', None)]


def probability_of_felony(offense_type):
    number_of_crimes = int([x['count_offense'] for x in offense_count if x['offense'] == offense_type][0])
    return number_of_crimes / count_of_every_felony


def offense_ratio_overall():
    offense_ratio = {}
    for offense in list_of_offenses:
        offense_ratio[offense] = probability_of_felony(offense)

    return offense_ratio


def probability_of_offense_by_borough(offense, borough):
    all_offenses_in_borough = sum(
        [int(x['count_offense']) for x in offense_count_by_borough_and_offense if x['borough'] == borough])
    number_of_specific_offense = sum([int(x['count_offense']) for x in offense_count_by_borough_and_offense
                                      if (x['borough'] == borough
                                          and x['offense'] == offense)])
    return number_of_specific_offense / all_offenses_in_borough


def offense_ratio_by_borough():
    temp_offense_ratio_by_borough = {}
    for borough in boroughs:
        temp_offense_ratio_by_borough[borough] = []
        temp_dict = {}
        for offense in list_of_offenses:
            temp_dict[offense] = probability_of_offense_by_borough(offense, borough)
        temp_offense_ratio_by_borough[borough].append(temp_dict)
    return temp_offense_ratio_by_borough


def probability_of_offense_by_borough_compared_to_other_boroughs(offense, borough):
    probability = offense_ratio_by_borough()[borough][0][offense]
    return probability / offense_ratio_overall()[offense]


def offense_by_borough_compared_to_other_boroughs():
    temp_offense_by_borough_compared_to_other_boroughs = {}
    for borough in boroughs:
        temp_offense_by_borough_compared_to_other_boroughs[borough] = []
        temp_dict = {}
        for offense in list_of_offenses:
            temp_dict[offense] = probability_of_offense_by_borough_compared_to_other_boroughs(offense, borough)
        temp_offense_by_borough_compared_to_other_boroughs[borough].append(temp_dict)
    return temp_offense_by_borough_compared_to_other_boroughs
