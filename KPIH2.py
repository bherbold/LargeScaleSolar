from sympy import symbols,Eq, solve

# --- financial KPIs --- #
def LCOE (capex,opex,energy_gen):
    """
    USE LCOE_simple
    :param opex: opex per year
    :param energy_gen: Array of all annual energy generations
    :return: LCOE
    """
    op_costs = opex * len(energy_gen)
    total_energy = 0 # total energy generation over the years
    for year in energy_gen:
        #year = annual generation
        total_energy = total_energy + year
    lcoe = (capex + op_costs)/total_energy
    return lcoe

def LCOE_simple (capex,opex,energy_gen):
    """
    only takes total energy produced into account
    :param capex:MUSD
    :param opex:MSD
    :param energy_gen: MWh
    :param time: time horizon
    :return: USD/MWH
    """
    irr = 0.08
    equityRatio = 0.2
    debtRatio = 0.8
    interestRate = 0.05

    wacc = equityRatio * irr + debtRatio * interestRate

    a = ((1+wacc)**30)*wacc/(((1+wacc)**30)-1)


    lcoe_cal = (a*capex + opex)*1000000/energy_gen
    return lcoe_cal

def lcoh (H2_capex,H2_opex,kg_H2):
    irr = 0.08
    equityRatio = 0.2
    debtRatio = 0.8
    interestRate = 0.05

    wacc = equityRatio * irr + debtRatio * interestRate

    a = ((1 + wacc) ** 30) * wacc / (((1 + wacc) ** 30) - 1)

    lcoh_cal = (a * H2_capex + H2_opex)*1000000 / kg_H2

    return lcoh_cal

#----- technical KPIs ----#


def cf (capacity,energy):
    """

    :param capacity: capacity of pv (DC) and CSP (MWe turbine)
    :param energy:
    :return: capacity factor
    """
    #WATCH OUT FOR SAME UNITS

    return energy/(8760 * capacity)


def peak_prod ( hour_E):
    """

    :param annual_E: overall energy prod
    :param hour_E: hourly energy prod data for 376 days (8760 hrs)
    :return: ratio of generation in peak hours (5pm to 12am)
    """
    sumProd = sum(hour_E)
    count = 0

    hour_count = 1

    for i in range(len(hour_E)):

        if (hour_count <=24) & (hour_count >= 18):
            count = count + hour_E[i]
            hour_count = hour_count + 1
        else:
            hour_count = hour_count + 1

        if hour_count > 24:
            hour_count = 1

    peakRatio = count/sumProd
    return peakRatio

def PPA (capex, opex, combinedGeneration, bonushours,allGen):
    """

    :param capex:
    :param opex:
    :param combinedGeneration: the total combined generation of the year in kwh (hybrid system inkl. strategy)
    :param bonushours: not needed
    :return: PPA in USD/kWh
    """

    #ppa = symbols('ppa')


    priceH2 = 4.25#USD/kg
    totalH2 = sum(allGen[4])
    revenueH2 = priceH2*totalH2

    ratios= hourlyRevenue (combinedGeneration,1)#i=0 is revenue (start at 1)
    irr = 0.08

    equityRatio = 0.2
    debtRatio = 0.8
    interestRate = 0.05
    degrPV = 1-0.013
    degrCSP = 1-0.002
    degrTotal = degrPV*(sum(allGen[1])/(sum(allGen[1])+sum(allGen[2]))) + degrCSP*(sum(allGen[2])/(sum(allGen[1])+sum(allGen[2])))
    degRatio = sum(allGen[1])/(sum(allGen[1])+sum(allGen[2]))

    wacc = equityRatio * irr + debtRatio * interestRate
    constr_years = 2
    lifetime = 30
    #bonus = 0.2*ppa*bonushours # might be too simple, as we would say each yer same prod
    total_gen = sum(combinedGeneration)
    bonus_gen = 0.2*hourlyRevenue(combinedGeneration,1)[4]

    capexSum = 0


    for i in range(0,constr_years):
        capexSum = capexSum + ((capex)/(constr_years*(1+wacc)**i))*1000000
        #capexSum = capexSum + ((capex*(1.02**i))/(constr_years*(1+wacc)**i))*1000000 # including inflation

    opexSum = 0
    for i in range(2,constr_years+30):

        opexSum = opexSum + ((opex* (1.02 ** i))/(1+wacc)**i)*1000000
        #opexSum = opexSum + ((opex * (1.02 ** i)) / (1 + wacc) ** i) * 1000000 # including inflation

    generationSum = 0
    for i in range(2,constr_years+30):
        #generationSum = generationSum + (total_gen*(0.5*ratios[1]+1*ratios[2]+2*ratios[3])+bonus_gen)/(1+wacc)**i
        generationSum = generationSum + ((total_gen * (0.5 * ratios[1] + 1 * ratios[2] + 2 * ratios[3]) + bonus_gen)*(degrTotal **(i-1)) ) / (
                    1 + wacc) ** i

    H2Sum = 0
    for i in range(2, constr_years + 30):
        # generationSum = generationSum + (total_gen*(0.5*ratios[1]+1*ratios[2]+2*ratios[3])+bonus_gen)/(1+wacc)**i
        H2Sum = H2Sum + revenueH2 / (1 + wacc) ** i

    result = (capexSum+opexSum-H2Sum)/generationSum


    return result

def NPV (capex, opex, ppa, combinedGeneration, bonushours,allGen):
    """
    Things might be arrays as we need to analyze years

    :param capex:
    :param opex:
    :param ppa:
    :param combinedGeneration: hourly combined generation
    :param ratioshours: ratio of how much of that prod was generated in which tariff hour
    :param bonushours: bonushours
    :return:
    """
    priceH2 = 4.25 #USD/kg
    totalH2 = sum(allGen[4])
    revenueH2 = priceH2*totalH2

    equityRatio = 0.2
    debtRatio = 0.8
    interestRate = 0.05
    irr = 0.08
    inflation = 0.02
    degrPV = 1-0.013
    degrCSP = 1-0.002
    degrTotal = degrPV*(sum(allGen[1])/(sum(allGen[1])+sum(allGen[2]))) + degrCSP*(sum(allGen[2])/(sum(allGen[1])+sum(allGen[2])))
    RatioPV = sum(allGen[1])/(sum(allGen[1])+sum(allGen[2]))

    wacc =  equityRatio*irr + debtRatio*interestRate
    realDisc = ((1+wacc)/(1+inflation))-1
    constr_years = 2
    lifetime = 30
    bonus = 0.2*ppa*hourlyRevenue(combinedGeneration,1)[4] # might be too simple, as we would say each yer same prod
    capexList = []
    opexList = []
    incomeList =[]

    capexSum = 0

    for i in range(0,constr_years):
        capexSum = capexSum + (capex)/(constr_years*(1+wacc)**i)
        #capexSum = capexSum + (capex) / (constr_years * (1 + realDisc) ** i)
        #capexList.append(capexSum/constr_years)
    operationSum = 0

    for i in range(constr_years,constr_years+lifetime):


        #operationSum = operationSum + (bonus/1000000 + sum(hourlyRevenue(combinedGeneration,ppa/1000000)[0]) - opex)/(1+wacc)**i
        income = bonus/1000000 + sum(hourlyRevenue(combinedGeneration,ppa/1000000)[0])*degrTotal**(i-1)
        #operationSum = operationSum + (
        #        (bonus*(degrTotal**i)) / 1000000 + sum(hourlyRevenue(combinedGeneration, ppa / 1000000)[0])*(degrTotal**i) - opex*(1.02**i)) / (1 + wacc) ** i # with degradation and inflation

        operationSum = operationSum + (
                (bonus / 1000000 + sum(hourlyRevenue(combinedGeneration, ppa / 1000000)[0]))*degrTotal**(i-1) + revenueH2/1000000 - opex* (1.02 ** i)) / (1 + wacc) ** i
        #opexList.append(opex)
        incomeList.append(bonus / 1000000 + sum(hourlyRevenue(combinedGeneration, ppa / 1000000)[0]))

    npv = -capexSum + operationSum

    for i in range(0,8730):
        incomeList.append(0)
    print('income Electricty: ', incomeList[0])
    print('income H2: ', revenueH2/1000000)

    return npv,incomeList

def NPV_Deg (capex, opex, ppa, combinedGeneration, bonushours):
    """
    NPV with degredation.

    :param capex:
    :param opex:
    :param ppa:
    :param combinedGeneration: hourly combined generation of different pp
    :param ratioshours: ratio of how much of that prod was generated in which tariff hour
    :param bonushours: bonushours
    :return:
    """
    equityRatio = 0.2
    debtRatio = 0.8
    interestRate = 0.05
    irr = 0.08
    degrPV = 1-0.005
    degrCSP = 1-0.0005
    degrTotal = 1

    wacc =  equityRatio*irr + debtRatio*interestRate
    constr_years = 2
    lifetime = 30
    bonus = 0.2*ppa*hourlyRevenue(combinedGeneration,1)[4] # might be too simple, as we would say each yer same prod

    capexSum = 0

    for i in range(0,constr_years):
        capexSum = capexSum + (capex)/(constr_years*(1+wacc)**i)
        #capexSum = capexSum + (capex * (1.02 ** i)) / (constr_years * (1 + wacc) ** i)

    operationSum = 0

    for i in range(constr_years,constr_years+lifetime):


        operationSum = operationSum + ((0.2*ppa*hourlyRevenueDeg(combinedGeneration,1,i)[4])/1000000 + sum(hourlyRevenueDeg(combinedGeneration,ppa/1000000,i)[0]) - opex)/(1+wacc)**i
        income = bonus/1000000 + sum(hourlyRevenue(combinedGeneration,ppa/1000000)[0])
        #operationSum = operationSum + (
        #        (bonus*(0.995**i)) / 1000000 + sum(hourlyRevenue(combinedGeneration, ppa / 1000000)[0])*(0.995**i) - opex*(1.02**i)) / (1 + wacc) ** i # with degradation and inflation
    npv = -capexSum + operationSum

    return npv

def hourlyRevenueDeg (comGen,ppa,year):
    """
    with degradation
    :param comGen: array of the combined hybrd prod. in kwh for each hour after strategy
    :param ppa: PPA previously camlculated
    :return: revenue without the bonus included, generation ratios for different hours, and ratio of how much
    prod kwh was valid for the bonus
    """

    revenueNoBonus = []

    multi = [0.5,1,2]

    degrPV = 1-0.005
    degrCSP = 1-0.0005

    countnight = 0
    countday = 0
    countPeak = 0

    hour_count = 1

    for i in range(len(comGen)):

        if (hour_count <= 24) & (hour_count >= 18):
            #peak hour
            revenueNoBonus.append(comGen[1][i] * ppa * multi[2]*(degrPV**year))
            revenueNoBonus[i] = revenueNoBonus[i] + comGen[2][i] * ppa * multi[2]*(degrCSP**year)
            countPeak = countPeak + comGen[i]
            hour_count = hour_count + 1
        elif (hour_count < 18) & (hour_count > 5):
            #daytime
            revenueNoBonus.append(comGen[1][i] * ppa * multi[1] * (degrPV**year))
            revenueNoBonus[i] = revenueNoBonus[i] + comGen[2][i] * ppa * multi[1] * (degrCSP**year)
            countday = countday + comGen[i]
            hour_count = hour_count + 1

        elif (hour_count >= 1) & (hour_count <=5):
            #night
            revenueNoBonus.append(comGen[1][i] * ppa * multi[0] * (degrPV**year))
            revenueNoBonus[i] = revenueNoBonus[i] + comGen[2][i] * ppa * multi[0] * (degrCSP**year)
            countnight = countnight + comGen[i]
            hour_count = hour_count + 1
        if (hour_count > 24):
            hour_count = 1

    hoursBonus = []# if 1 than it has bonus second value is the base

    for i in range(len(comGen)):
        hoursBonus.append([0,0])

    zeroPrev = 0.0000000001 #prevent zero divition

    for i in range(len(comGen)):

        if comGen[i] == 0:
            continue
        if i == 0:
            continue
        if i >= 8756:
            break

        if ((abs(comGen[i]-comGen[i+1])/comGen[i]) <= 0.05) & ((abs(comGen[i]-comGen[i+2])/comGen[i]) <= 0.05) & ((abs(comGen[i]-comGen[i+3])/comGen[i]) <= 0.05) & (hoursBonus[i][1] == 0):
            #finding first 3
            #print(hoursBonus[i][0])
            hoursBonus[i][0] = 1
            hoursBonus[i][1] = comGen[i]
            hoursBonus[i+1][0]= 1
            hoursBonus[i+1][1] = comGen[i]
            hoursBonus[i+2][0] = 1
            hoursBonus[i+2][1] = comGen[i]
            #i = i + 2
        if (hoursBonus[i-1][0] == 1) & (hoursBonus[i][1] == 0) & ((abs(hoursBonus[i-1][1]-comGen[i])/(hoursBonus[i-1][1]+zeroPrev)) <= 0.05) :
            hoursBonus[i][0] = 1
            hoursBonus[i][1] = hoursBonus[i-1][1]

    numberOfbonusGen = 0

    for i in range(len(comGen)):
        numberOfbonusGen = numberOfbonusGen + comGen[i]*hoursBonus[i][0]

    ratioNight = max(0,countnight)/sum(comGen)
    ratioDay = max(0,countday)/sum(comGen)
    ratioPeak = max(countPeak,0)/sum(comGen)
    ratiobonus = numberOfbonusGen/sum(comGen)

    return [revenueNoBonus, ratioNight, ratioDay, ratioPeak, numberOfbonusGen,ratiobonus]

def hourlyRevenue (comGen,ppa):
    """

    :param comGen: array of the combined hybrd prod. in kwh for each hour after strategy
    :param ppa: PPA previously camlculated
    :return: revenue without the bonus included, generation ratios for different hours, and ratio of how much
    prod kwh was valid for the bonus
    """

    revenueNoBonus = []

    multi = [0.5,1,2]

    countnight = 0
    countday = 0
    countPeak = 0

    hour_count = 1

    for i in range(len(comGen)):

        if (hour_count <= 24) & (hour_count >= 18):
            #peak hour
            revenueNoBonus.append(comGen[i] * ppa * multi[2])
            countPeak = countPeak + comGen[i]
            hour_count = hour_count + 1
        elif (hour_count < 18) & (hour_count > 5):
            #daytime
            revenueNoBonus.append(comGen[i] * ppa * multi[1])
            countday = countday + comGen[i]
            hour_count = hour_count + 1

        elif (hour_count >= 1) & (hour_count <=5):
            #night
            revenueNoBonus.append(comGen[i] * ppa * multi[0])
            countnight = countnight + comGen[i]
            hour_count = hour_count + 1
        if (hour_count > 24):
            hour_count = 1

    hoursBonus = []# if 1 than it has bonus second value is the base

    for i in range(len(comGen)):
        hoursBonus.append([0,0])

    zeroPrev = 0.0000000001 #prevent zero divition

    for i in range(len(comGen)):

        if comGen[i] == 0:
            continue
        if i == 0:
            continue
        if i >= 8756:
            break

        if ((abs(comGen[i]-comGen[i+1])/comGen[i]) <= 0.05) & ((abs(comGen[i]-comGen[i+2])/comGen[i]) <= 0.05) & ((abs(comGen[i]-comGen[i+3])/comGen[i]) <= 0.05) & (hoursBonus[i][1] == 0):
            #finding first 3
            #print(hoursBonus[i][0])
            hoursBonus[i][0] = 1
            hoursBonus[i][1] = comGen[i]
            hoursBonus[i+1][0]= 1
            hoursBonus[i+1][1] = comGen[i]
            hoursBonus[i+2][0] = 1
            hoursBonus[i+2][1] = comGen[i]
            #i = i + 2
        if (hoursBonus[i-1][0] == 1) & (hoursBonus[i][1] == 0) & ((abs(hoursBonus[i-1][1]-comGen[i])/(hoursBonus[i-1][1]+zeroPrev)) <= 0.05) :
            hoursBonus[i][0] = 1
            hoursBonus[i][1] = hoursBonus[i-1][1]

    numberOfbonusGen = 0

    for i in range(len(comGen)):
        numberOfbonusGen = numberOfbonusGen + comGen[i]*hoursBonus[i][0]

    ratioNight = max(0,countnight)/sum(comGen)
    ratioDay = max(0,countday)/sum(comGen)
    ratioPeak = max(countPeak,0)/sum(comGen)
    ratiobonus = numberOfbonusGen/sum(comGen)

    return [revenueNoBonus, ratioNight, ratioDay, ratioPeak, numberOfbonusGen,ratiobonus]
