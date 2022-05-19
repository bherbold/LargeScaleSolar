
def toGAMS (data,filename):
    with open(filename, 'w') as f:
        for sheet in data:
            i = 1;
            for pv in sheet[21]:

                s = 'I.hour'+str(i) +' '+ str(pv) + ','
                f.write(s)
                i = i +1
                if(i == 500):
                    f.write('\n')
                if (i == 1000):
                    f.write('\n')
                if (i == 1500):
                    f.write('\n')
                if (i == 2000):
                    f.write('\n')
                if (i == 2500):
                    f.write('\n')
                if (i == 3000):
                    f.write('\n')
                if (i == 3500):
                    f.write('\n')
                if (i == 4000):
                    f.write('\n')
                if (i == 4500):
                    f.write('\n')
                if (i == 5000):
                    f.write('\n')
                if (i == 5500):
                    f.write('\n')

                if (i == 6000):
                    f.write('\n')
                if (i == 6500):
                    f.write('\n')
                if (i == 7000):
                    f.write('\n')
                if (i == 7500):
                    f.write('\n')
                if (i == 8000):
                    f.write('\n')

            i=1
            for csp in sheet[20]:
                s = 'II.hour'+str(i)  +' '+ str(csp) + ','
                f.write(s)
                i = i + 1
                if (i == 500):
                    f.write('\n')
                if (i == 1000):
                    f.write('\n')
                if (i == 1500):
                    f.write('\n')
                if (i == 2000):
                    f.write('\n')
                if (i == 2500):
                    f.write('\n')
                if (i == 3000):
                    f.write('\n')
                if (i == 3500):
                    f.write('\n')
                if (i == 4000):
                    f.write('\n')
                if (i == 4500):
                    f.write('\n')
                if (i == 5000):
                    f.write('\n')
                if (i == 5500):
                    f.write('\n')

                if (i == 6000):
                    f.write('\n')
                if (i == 6500):
                    f.write('\n')
                if (i == 7000):
                    f.write('\n')
                if (i == 7500):
                    f.write('\n')
                if (i == 8000):
                    f.write('\n')
            #20= CSP, 21=PV

def OneWeek (data,filename):

    with open(filename, 'w') as f:
        for sheet in data:
            i = 0
            j = 1
            for pv in sheet[21]:

                if (i >= 4200) and (i < 4368):

                    s = 'I.hour' + str(j) + ' ' + str(pv) + ','
                    f.write(s)
                    i = i + 1
                    j = j + 1

                else:
                    i = i + 1



            i=0
            j = 1
            for csp in sheet[20]:

                if (i >= 4200) and (i < 4368):

                    s = 'II.hour' + str(j) + ' ' + str(csp) + ','
                    f.write(s)
                    i = i + 1
                    j = j + 1

                else:
                    i = i + 1


            #20= CSP, 21=PV
def genPrice(days,ppa):

    with open('data/results/genPricesGams.txt', 'w') as f:

        day = 1

        for i in range(1,days*24+1):

            if day <=5 and day >0:
                s= 'hour'+str(i) + ' ' + str(0.5*ppa) + ','
                f.write(s)
                day = day +1
            elif day >5 and day <=16:
                s= 'hour'+str(i) + ' ' + str(1*ppa) + ','
                f.write(s)
                day = day +1
            elif day > 16 and day <= 24:
                s = 'hour' + str(i) + ' ' + str(2*ppa) + ','
                f.write(s)
                day = day +1
            if day > 24:
                day = 1
