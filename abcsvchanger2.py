import csv, ast

#file = "Bitfinex_ETHUSD_d"
print("which file?")
#file = input()

def timenclosecsv(file):
    with open(file + ".csv", newline='') as csvfile:
        with open(file + "mod.csv",'w', newline='') as csvfilemod:
            reader = csv.reader(csvfile, delimiter=',')
            writer = csv.writer(csvfilemod, delimiter=',')
            for row in reader:
                if 'Created' not in row[0]:
                    row[1] = row[5]
                    row = [row[0], row[1]]
                    writer.writerow(row)
            #print(row[0][:-2])

def removeamnpm(file):
    with open(file, newline='') as csvfile:
        with open(file[:-4] + "mod.csv",'w', newline='') as csvfilemod:
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

def addtolines(file):
    with open(file, newline='') as csvfile:
        with open(file[:-4] + "mod2.csv",'w', newline='') as csvfilemod:
            reader = csv.reader(csvfile, delimiter=',')
            writer = csv.writer(csvfilemod, delimiter=',')
            sum = 0.0
            hmd = 2
            hmd2 = 2
            hmd3 = 25
            writer.writerow(["Date", "Close+Open/2", "Daily avg", "sums","how many hrs","Diff from avg"])
            for row in reader:
                if row[4] == "1":
                    row[3] =  "=SUM(B"+str(hmd2)+":B"+str(hmd) + ")"
                    row[6] =  "=SUM(F"+str(hmd2)+":F"+str(hmd) + ")"
                    row[4] = hmd + 1 - hmd2
                    hmd2 = hmd + 1
                    row[2] = "=D"+str(hmd)+"/E"+str(hmd)
                    row[5] = "=B" + str(hmd) + "-C" + str(hmd3)
                    hmd3 = hmd + 24
                else:
                    row[6] = ""
                    row[3] = ""
                    row[2] = ""
                    row[5] = "=B" + str(hmd) + "-C" + str(hmd3)
                hmd+=1
                writer.writerow(row)

def addtolines2(file):
    for i in range(24):
        with open(file, newline='') as csvfile:
            with open(file[:-4] + str(i) + ".csv",'w', newline='') as csvfilemod:
                reader = csv.reader(csvfile, delimiter=',')
                writer = csv.writer(csvfilemod, delimiter=',')
                currow = 1
                for row in reader:
                    currow +=1
                    if(row[i] != ""):
                        writer.writerow(row)
                print(currow)

def addtolines3(file):
    with open(file,'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(24):
            with open(file[:-4] + str(i) + ".csv",'r', newline='') as csvfilemod:
                reader = csv.reader(csvfilemod, delimiter=',')
                for row in reader:
                    writer.writerow(row)

def addtolines4(file):
    #with open(file, 'rw', newline='') as csvfile:
        #writer = csv.writer(csvfile, delimiter=',')
        for i in range(24):
            print('with open(file[:-4] + str(i) + ".csv","r", newline="") as csvfilemod' + str(i) + ":")
            print('reader' + str(i) +'=csv.reader(csvfilemod' + str(i)+ ', delimiter=",")')


#removeamnpm("test2.csv")
#addtolines("Gdax_BTCUSD_1hkmod.csv")
addtolines3("test2aaa.csv")
