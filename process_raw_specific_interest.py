import csv

interest = []
category_id = []
with open("data/raw_file/raw_nasa_scope_input_subjects_of_specific_interest.txt", "r") as f:
    for line in f:
        interest.append(line.split(' .')[0])
        category_id.append(int(line.split('.')[-1].strip()))

    header = ['interest','category_id']
    with open("data/nasa_scope_subject_category_to_interest.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(interest, category_id))