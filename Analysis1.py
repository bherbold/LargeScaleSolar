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

        combined_generaton = combineGenerations(sheet[0],sheet[20],sheet[21],sheet[26],sheet[27],(sheet[3]*sheet[0]),sheet[28],sheet[29])




        #plant = [row[0],row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], row[13],row[14],row[15],row[16],row[17],row[18]]
       # print(len(plant))

        #print(row[13])
        #print(total_gen)
        sheet[13] = sum(combined_generaton[2])
        sheet[19] = sum(combined_generaton[1])
        powerplant = PowerPlant.PowerPlant(sheet)

        capex = powerplant.capex_total
        opex = powerplant.opex_total_musd


        lcoe = KPIs.LCOE_simple(capex,opex,sum(combined_generaton[0])/1000)
        #powerplant.lcoe = lcoe


        cf = KPIs.cf((powerplant.csp_cap+powerplant.pv_cap/1000),sum(combined_generaton[0])) #capacity factor
        #powerplant.capacityFactor = cf

        peakProd = KPIs.peak_prod(combined_generaton[0]) # ratio of generation in peak hours

        print()
        print('###### NEW Powerplant #########')
        print()
        print('CAPEX: ', capex, 'MUSD')
        print('OPEX: ', opex, 'MUSD')
        ppa = KPIs.PPA(capex,opex,combined_generaton[0],8760*peakProd,combined_generaton)
        print('PPA: ', ppa, 'USD/kWh')
        npv = KPIs.NPV(capex, opex, ppa, combined_generaton[0], 8760 * peakProd,combined_generaton)  # imputs needed for PPA!!!
        print('NPV: ', npv[0])
        #npv_deg = KPIs.NPV_Deg(capex, opex, ppa, combined_generaton, 8760 * peakProd)  # imputs needed for PPA!!!
        #print('NPV including deg: ', npv_deg)
        sheet.append(lcoe)
        print('LCOE:  ',lcoe, 'USD/MWh')
        sheet.append(cf)
        print('capacity factor: ', cf)
        sheet.append(peakProd)
        print('peakHours Ratio: ', peakProd)
        sheet.append(npv[0])
        sheet.append(ppa)
        sheet.append(capex)
        sheet.append(opex)
        sheet.append(combined_generaton[0]) # combined generation per hour
        sheet.append(combined_generaton[1]) # PV Prod after cutting
        sheet.append(combined_generaton[2])  # Tes_discharge
        sheet.append(combined_generaton[3])  # Tes_SOC in MWe
        sheet.append(npv[1])

        allSheets.append(sheet)
        print('Highest PV DC production: ' , max(sheet[21]))
        print('Highest CSP receiver production: ', max(sheet[20]))
        print('income first year: ', npv[1][0])

        print(sheet[0])
        #print(plant)

    #print(allSheets)

    #saveData.saveToExcel(file,allSheets)


    return allSheets

def combineGenerations ( csp_cap,csp,pv,inverterCap,inverterEff,TES_cap,PVselfCon,TES_loss):

    cut_good = 150000
    cut_bad = 100000
    #combined = noStrategy(csp,pv)

    combined1 = simpleStrategy(csp_cap,csp,pv,inverterCap,inverterEff,cut_good,cut_bad,TES_cap,PVselfCon,TES_loss)

    return combined1

def noStrategy(csp,pv):
    combined = []

    for i in range(len(pv)):

        gen = 0
        if (pv[i] + csp[i] > 150000):
            combined.append(150000)
        else:

            combined.append(pv[i] + csp[i])

    return combined

def simpleStrategy(csp_cap,csp,pv,inverterCap,inverterEff,cut_good,cut_bad,TES_cap,PVselfCon,TES_loss):

    TES_SOC = []
    for i in range(len(csp)):
        #initially empty storage
        TES_SOC.append(0)

    cspProd = []
    for i in range(len(csp)):
        #initially 0
        cspProd.append(0)
    pvProd = []
    for i in range(len(csp)):
        #initially 0
        pvProd.append(0)
    TES_dis = []
    # initially 0
    for i in range(len(csp)):
        TES_dis.append(0)
    combined = []
    for i in range(len(csp)):
        #initially 0
        combined.append(0)

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
        if max(days[i]) >= cut_good:
            goodDays.append(True)
        else:
            goodDays.append(False)

    for d in goodDays:

        daysToHours(hoursGood,d)

    t = 0 # hour of the day
    for hours in range(len(csp)):



        if hoursGood[hours]:
            #print(csp)
            help = csp[hours]
            #if len(TES_SOC) == 0:
                #nothing happens
                #pvProd =cspProd
                #t = t + 1
               # if t > 24:
                   # t = 0
            #else:

            outputSimple = SimpleGoodDay(csp_cap,csp,pv,cut_good,combined,pvProd,inverterCap,inverterEff,cspProd,TES_SOC,TES_cap,TES_dis,hours,t,PVselfCon,TES_loss)
            #TES_SOC[hours] = outputSimple.TES_SOC
            #print(TES_dis)

        else:
            #if len(TES_SOC) == 0:
            #    #nothing happens
            #    pvProd =cspProd
            #    t = t + 1
            #    if t > 24:
            #        t = 0
            #else:

            #outputSimple = SimpleBadDay(csp_cap,csp,pv,cut_bad,combined,pvProd,inverterCap,inverterEff,cspProd,TES_SOC,TES_cap,TES_dis,hours,t,PVselfCon,TES_loss)
            outputSimple = SimpleGoodDay(csp_cap, csp, pv, cut_bad, combined, pvProd, inverterCap, inverterEff,
                                         cspProd, TES_SOC, TES_cap, TES_dis, hours, t, PVselfCon, TES_loss)
            #TES_SOC[hours] = outputSimple.TES_SOC
            #print(TES_dis)

        t = t + 1
        if t >= 24:
            t = 0
    for i in range(len(combined)):
        combined[i] = TES_dis[i] + pvProd[i]

    return [combined, pvProd,TES_dis,TES_SOC]

def SimpleBadDay(csp_cap,csp,pv,cut,combined,pvProd,inverterCap,inverterEff,cspProd,TES_SOC,TES_cap,TES_dis,hour,t,PVselfCon,TES_loss):
    SimpleGoodDay(csp_cap, csp, pv, cut, combined, pvProd,inverterCap,inverterEff, cspProd, TES_SOC, TES_cap, TES_dis, hour, t,PVselfCon,TES_loss)


def SimpleGoodDay(csp_cap,csp,pv,cut,combined,pvProd,inverterCap,inverterEff,cspProd,TES_SOC,TES_cap,TES_dis,hour,t,PVselfCon,TES_loss):

    #pvSurplus = dispatchPV(cut,pv,pvProd,hour,t)
    pvSurplus = dispatchPVDC(cut,pv,inverterCap,inverterEff,pvProd,hour,t,PVselfCon)

    dispatchStorage(csp_cap,csp,cspProd,pvSurplus,pvProd,TES_SOC,TES_cap,TES_dis,hour,t,TES_loss)


def dispatchPV(cut,pv,pvProd,hour,t):

    pvSurplus = 0
    if pv[hour] >cut:
        pvProd[hour] = cut
        pvSurplus = pv[hour] - cut
    else:
        pvProd[hour] = pv[hour]

    return pvSurplus

def dispatchPVDC(cut,pv,inverterCap,inverterEff, pvProd,hour,t,selfCon):
    # pv needs to be DC values

    E_dc_max = min(cut,inverterCap)/inverterEff # maximum to grid

    pvSurplus = 0

    if pv[hour] >E_dc_max:

        pvProd[hour] = E_dc_max * inverterEff - selfCon

        pvSurplus = pv[hour] - E_dc_max
    else:
        pvProd[hour] = max(pv[hour]*inverterEff - selfCon,0)

    return pvSurplus

def dispatchStorage(csp_cap,csp,cspProd,pvSurplus,pvProd,TES_SOC,TES_cap,TES_dis,hour,t,TES_losses):

    SelfConCSP = 0.0055 * csp_cap


    minPbGeneration = 0.3*csp_cap # min of 30 % of gross power
    a = hour
    startUpFactor = 0.5
    csp_max = 150000 - pvProd[hour] # maximum dispatch of csp into grid
    eff = 0.42 * 0.98  # pv to heater to TES efficiency


    if (t > 15) and (t < 24):

        if TES_dis[hour-1] <= 0:
            #late startup of the turbine
            if (TES_SOC[hour - 1] > minPbGeneration) and (csp_max > minPbGeneration):
                TES_dis[hour] = min(startUpFactor * csp_cap,csp_max) - SelfConCSP
                TES_SOC[hour] = TES_SOC[hour - 1] - TES_dis[hour]
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], csp[hour])  # csp charge
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], pvSurplus * eff)
            else:
                if TES_SOC[hour - 1] >= TES_cap:
                    TES_dis[hour] = 0 #- SelfConCSP
                    TES_SOC[hour] = TES_SOC[hour - 1] + min(csp[hour], (TES_cap - TES_SOC[hour - 1]))
                    TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], pvSurplus * eff)
                    cspProd[hour] = 0 - SelfConCSP
                elif TES_SOC[hour - 1] < TES_cap:
                    TES_dis[hour] = 0 #- SelfConCSP
                    TES_SOC[hour] = TES_SOC[hour - 1] + min(csp[hour], (TES_cap - TES_SOC[hour - 1]))
                    TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], pvSurplus * eff)
                    #print()


        else:
            if TES_SOC[hour-1] > csp_cap and (csp_max >= minPbGeneration):
                #if stoarge is bigger than turbine capacity: dispatch
                TES_dis[hour] = min(csp_cap,csp_max) - SelfConCSP
                TES_SOC[hour] = TES_SOC[hour-1] - TES_dis[hour]
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap-TES_SOC[hour],csp[hour]) # csp charge
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap-TES_SOC[hour],pvSurplus*eff)

            elif (TES_SOC[hour-1] < csp_cap) and ((TES_SOC[hour-1] + csp[hour])> minPbGeneration):
                #if stoarge is bigger than turbine capacity: dispatch
                TES_dis[hour] = min(TES_SOC[hour-1],csp_max) - SelfConCSP
                TES_SOC[hour] = TES_SOC[hour-1] - TES_dis[hour]
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap-TES_SOC[hour],csp[hour]) # csp charge
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap-TES_SOC[hour],pvSurplus*eff)
            else:
                # otherwise dont dispatch
                TES_dis[hour] = 0 #- SelfConCSP
                #TES_SOC[hour] = TES_SOC[hour-1] +
                TES_SOC[hour] = TES_SOC[hour - 1] - TES_dis[hour]
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], csp[hour])  # csp charge
                TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], pvSurplus * eff)
    else:

        TES_dis[hour] = 0 #- SelfConCSP

        if TES_SOC[hour-1] >= TES_cap:

            TES_SOC[hour] = TES_SOC[hour-1] + min(csp[hour],(TES_cap-TES_SOC[hour-1]))
            TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], pvSurplus * eff)
            cspProd[hour] = 0 #- SelfConCSP
        elif TES_SOC[hour-1] < TES_cap:

            TES_SOC[hour] = TES_SOC[hour-1] + min(csp[hour],(TES_cap-TES_SOC[hour-1]))
            TES_SOC[hour] = TES_SOC[hour] + min(TES_cap - TES_SOC[hour], pvSurplus * eff)

    TES_SOC[hour] = max(TES_SOC[hour] - TES_losses,0)







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


