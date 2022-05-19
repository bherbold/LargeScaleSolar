import CAPEX
import PowerPlant
import KPIs
import readData
import saveData
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

def simpleAnalysis (data,file):

    allSheets = []

    print('######### START simple analysis ########')
    for sheet in data:
        sheet_new = []
        for row in sheet:
            print(row)
            #plant = [row[0],row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], row[13],row[14],row[15],row[16],row[17],row[18]]
           # print(len(plant))
            total_gen = (row[13] + row[19])/1000000 #Ghw
            print(row[13])
            print(total_gen)
            plant = row

            powerplant = PowerPlant.PowerPlant(plant)

            capex = powerplant.capex_total
            opex = powerplant.opex_total_musd


            lcoe = KPIs.LCOE_simple(capex,opex,total_gen*1000)
            #powerplant.lcoe = lcoe

            cf = KPIs.cf((powerplant.csp_cap+powerplant.pv_cap),total_gen*1000000) #capacity factor
            #powerplant.capacityFactor = cf

            plant.append(lcoe)
            plant.append(cf)

            sheet_new.append(plant)
            #print(plant)

        allSheets.append(sheet_new)
    print(allSheets)

    saveData.saveToExcel(file,allSheets)

    return allSheets

def indepthAnalysis (data,file):

    #allSheets = simpleAnalysis(data,'data/results/SimpleofInDepth.xlsx')
    allSheets =[]
    for sheet in data:

        #total_gen = (sheet[13] + sheet[19]) / 1000000  # Ghw

        combined_generaton = combineGenerations(sheet[20],sheet[21],(sheet[3]*sheet[0])) # kWh
        sumComGen = sum(combined_generaton)



        #plant = [row[0],row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], row[13],row[14],row[15],row[16],row[17],row[18]]
       # print(len(plant))

        #print(row[13])
        #print(total_gen)

        powerplant = PowerPlant.PowerPlant(sheet)

        capex = powerplant.capex_total
        opex = powerplant.opex_total_musd


        lcoe = KPIs.LCOE_simple(capex,opex,sum(combined_generaton)/1000)
        #powerplant.lcoe = lcoe
        print('LCOE:  ',lcoe)



        cf = KPIs.cf((powerplant.csp_cap+powerplant.pv_cap/1000),sum(combined_generaton)) #capacity factor
        #powerplant.capacityFactor = cf

        peakProd = KPIs.peak_prod(combined_generaton) # ratio of generation in peak hours


        ppa = KPIs.PPA(capex,opex,combined_generaton,8760*peakProd)
        print('PPA: ', ppa)
        npv = KPIs.NPV(capex, opex, ppa, combined_generaton, 8760 * peakProd)  # imputs needed for PPA!!!
        print('NPV: ', npv)
        sheet.append(lcoe)
        sheet.append(cf)
        print('cf: ', cf)
        sheet.append(peakProd)
        print('PeakProd: ',peakProd)
        sheet.append(npv)
        sheet.append(ppa)
        sheet.append(combined_generaton)

        allSheets.append(sheet)
        #print(plant)

    print(allSheets)

    #saveData.saveToExcel(file,allSheets)


    return allSheets

def combineGenerations ( csp,pv,TES_cap):


    combined = noStrategy(csp,pv)

    #combined1 = simpleStrategy(csp,pv,150000,TES_cap)

    return combined

def noStrategy(csp,pv):
    combined = []

    for i in range(len(pv)):

        gen = 0
        if (pv[i] + csp[i] > 150000):
            combined.append(150000)
        else:

            combined.append(pv[i] + csp[i])

    return combined

def simpleStrategy(csp,pv,cut,TES_cap):

    TES_SOC = []
    #for i in range(len(csp)):
        #initially empty storage
     #   TES_SOC.append(0)

    cspProd = []
    pvProd = []
    combined = []

    goodDays = []
    hoursGood = []

    days = []
    day = []
    count = 0
    for hour in range(len(pv)):
        if count < 23 :
            day.append(pv[hour])
            count = count + 1
        else:
            days.append(day)
            count = 0
            day = []

    for i in range(len(days)):
        if max(days[i]) >= cut:
            goodDays.append(True)
        else:
            goodDays.append(False)

    for d in goodDays:

        daysToHours(hoursGood,d)

    for hours in range(len(csp)):

        if hoursGood[hours]:
            #print(csp)
            help = csp[hours]
            if len(TES_SOC) == 0:
                SimpleGoodDay(csp[hours], pv[hours], cut, combined, pvProd, cspProd, 0, TES_SOC,
                              TES_cap)
            else:
                SimpleGoodDay(csp[hours],pv[hours],cut,combined,pvProd,cspProd,TES_SOC[hours-1],TES_SOC,TES_cap)
        else:
            combined.append(pv[hours] + csp[hours])
            pvProd.append(pv[hours])
            cspProd.append(csp[hours])



    return combined

def SimpleGoodDay(csp,pv,cut,combined,pvProd,cspProd,TES_SOC,TES_array,TES_cap):

    if (pv + csp > cut):
        pvSurplus = pv - (pv-cut)
        pvProd.append(pvSurplus)
        #cspProd.append(csp)
        cspProd.append(chargeStorage(pvSurplus,csp,TES_SOC,TES_array,TES_cap))
        combined.append(cut)
        #chargeStorage(pvSurplus,csp,TES_SOC,TES_cap)

    else:
        pvProd.append(pv)
        cspProd.append(csp)
        combined.append(pv + csp)

def chargeStorage(pv,csp, TES_SOC,TES_array,TES_cap):

    cspOnly = 0
    eff = 0.99*0.42

    if len(TES_array) == 0:
        TES_array.append(0)
    else:

        if TES_SOC < TES_cap:
            if (TES_SOC + csp) <= TES_cap:

                TES_array.append(TES_SOC+csp)
            else:
                TES_array.append(TES_cap)
                cspOnly = csp - (TES_cap-TES_SOC)
        if TES_SOC < TES_cap:
            if pv > 0:
                if (TES_SOC + pv) <= TES_cap:

                    TES_array[len(TES_array-1)] = TES_array[len(TES_array-1)] + pv*eff


    return cspOnly


def daysToHours(hoursGood, d):
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)
    hoursGood.append(d)

"""
    for day in range(len(pv)):

        goodDay = False

        dayPeak = 0
        for hour in

        gen = 0
        if (pv[i] + csp[i] > 150000):
            combined.append(150000)
        else:

            combined.append(pv[i] + csp[i])
"""


