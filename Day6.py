from ast import Num


#day_6_time_test = [7, 15, 30]
#day_6_distance_test = [9, 40, 200]

#day_6_time_test = [46,     85,     75,     82]
#day_6_distance_test = [208,   1412,   1257,   1410]

#day_6_time_test = [71530]
#day_6_distance_test = [940200]

day_6_time_test = [46857582]
day_6_distance_test = [208141212571410]

num_possible_combos = []
race_tracker = 0

for t in day_6_time_test:
    race_combo_tracker = 0
    i = 1
    while i < day_6_time_test[race_tracker]:
        if i*(t - i) > day_6_distance_test[race_tracker]:
            race_combo_tracker = race_combo_tracker + 1
            print("Time held = " + str(i) + " - distance traveled = " + str(i*(t-i)) + " which is greater than " + str(day_6_distance_test[race_tracker]))
        i = i + 1
    print("Total options for race - " + str(race_combo_tracker))
    num_possible_combos.append(race_combo_tracker)
    race_tracker = race_tracker + 1

product = 1
for c in num_possible_combos:
    product = product * c

print("Produt of number of combos overall - " + str(product))


