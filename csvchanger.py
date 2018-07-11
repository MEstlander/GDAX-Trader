import csv


def removeamnpm(file)
    with open(file, newline='') as csvfile:
        with open(file - "-.csv" + "mod.csv",'w', newline='') as csvfilemod:
            reader = csv.reader(csvfile, delimiter=',')
            writer = csv.writer(csvfilemod, delimiter=',')
            for row in reader:
                #print(row[0][:2])
                #print(row[0][2:])
                if 'AM' in row[0][-2:]:
                    if '12' in row[0][-5:]:
                        row[0] = row[0][:-5] + "00:00:00"
                    else:
                        row[0] = row[0][:-3] + ":00:00"
                if 'PM' in row[0][-2:]:
                    if '12' in row[0][-5:]:
                        row[0] = row[0][:-3] + ":00:00"
                    else:
                        row[0] = row[0][:-5] + str(int(row[0][11:][:-3]) + 12) + ":00:00"
                print(row[0])
                writer.writerow(row)
            #print(row[0][:-2])


'''
2017-10-09 10-AM
2018-06-16 07-PM
2018-06-16 06-PM
2018-06-16 05-PM
2018-06-16 04-PM
2018-06-16 03-PM
2018-06-16 02-PM
2018-06-16 01-PM
2018-06-16 12-PM
2018-06-16 11-AM
2018-06-16 10-AM
2018-06-16 09-AM
2018-06-16 08-AM
2018-06-16 07-AM
2018-06-16 06-AM
2018-06-16 05-AM
2018-06-16 04-AM
2018-06-16 03-AM
2018-06-16 02-AM
2018-06-16 01-AM
2018-06-16 12-AM
2018-06-15 11-PM
2018-06-15 10-PM
2018-06-15 09-PM
'''