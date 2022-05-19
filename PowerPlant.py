import KPIs

class PowerPlant (object):

    #DATA
    csp_cap = 0 #KW
    sf_area = 0 # m2
    thermal_storage = 0 #MWh_th
    receiver_power = 0 #MW_th
    tower_height = 0 #m
    el_heater = 0 #KW_th
    csp_land = 0 #m2
    pv_cap = 0 #Wdc
    inverter_cap = 0 #Wdc
    batt_pp = 0 #MW
    batt_cap = 0 # MWh_e
    batt_an_gen = 0 # GWh/y
    pv_land = 0 #m2
    csp_an_gen = 0 # GWh/y
    distance_grid = 0 #km
    distance_road = 0 #km
    distance_gas = 0 #km
    distance_water = 0 #km
    other_comp = 0 #unit
    #H2_capex = (0.000450 + 0.000926 + 0.18/270 + 0.195/270) * 110000 # per KW
    #H2_capex = (0.000500 + 0.000926 + 50/1000000 ) * 95000  # per KW
    #DIRECT CAPEX
    ref_csp_powerblock = [190000,87.5] # MUSD
    ref_csp_bop = [110000,74.8] # MUSD
    ref_csp_tes = [3271,66] # MUSD
    ref_csp_sf = [1000000,125] # MUSD
    ref_csp_receiver = [565,55] # MUSD
    ref_csp_Tower = [200,30] # MUSD
    ref_csp_site_prep = [5000000,10] # MUSD
    ref_electric_heater = [1000000,70] #MUSD
    ref_grid_connection = [1,1.5] #MUSD
    ref_road_costs = [1,1.2] #MUSD
    ref_gas_pip = [1,1] #MUSD
    ref_water_pip = [1,1] #MUSD
    ref_battery_power = [1,0.225] #MUSD
    ref_battery_cap = [1,0.303] #MUSD
    ref_other_components = [1,0] #MUSD

    ref_pv_modules = [1000000,0.33*1.038] #MUSD
    ref_pv_inverter = [1000000,0.1] #MUSD
    ref_pv_bos = [1000000,0.3] #MUSD
    ref_pv_add_rack = [1000000,0.2] #MUSD
    ref_pv_site_prep = [5000,0.01] #MUSD
    #ref_H2_capex = (0.000450 + 0.000926 + 0.18/279 + 0.195/270) * 110000

    ref_direct_capex_subtotal = [ref_csp_powerblock,ref_csp_bop,ref_csp_tes ,ref_csp_sf,ref_csp_receiver,ref_csp_Tower,
                             ref_csp_site_prep,ref_electric_heater,ref_grid_connection,ref_road_costs,ref_gas_pip,
                             ref_water_pip,ref_battery_power,ref_battery_cap,ref_other_components,
                             ref_pv_modules,ref_pv_inverter, ref_pv_bos,ref_pv_add_rack,ref_pv_site_prep]

    # real costs -[amount,coefficient,cost_total] -will be set with the set_capex
    csp_powerblock = [csp_cap,0.8,0] # MUSD
    csp_bop = [csp_cap,0.8,0] # MUSD
    csp_tes = [thermal_storage,0.8,0]# MUSD
    csp_sf = [sf_area,1,0] # MUSD
    csp_receiver = [receiver_power,0.2,0]# MUSD
    csp_Tower = [tower_height,0.8,0]# MUSD
    csp_site_prep =[csp_land,0.9,0] # MUSD
    electric_heater =[el_heater,1,0] #MUSD
    grid_connection =  [distance_grid,1,0]#MUSD
    road_costs = [distance_road,1,0] #MUSD
    gas_pip = [distance_gas,1,0] #MUSD
    water_pip =[distance_water,1,0]  #MUSD
    battery_power = [batt_cap,1,0] #MUSD
    battery_cap = [batt_cap,1,0] #MUSD
    other_components = [other_comp,1,0] #MUSD


    pv_modules = [pv_cap,1,0] #MUSD
    pv_inverter = [inverter_cap,1,0] #MUSD
    pv_bos = [pv_cap,1,0] #MUSD
    pv_add_rack = [pv_cap,1,0] #MUSD
    pv_site_prep = [pv_land,1,0] #MUSD

    direct_capex_subtotal = [csp_powerblock, csp_bop, csp_tes, csp_sf, csp_receiver, csp_Tower,
                             csp_site_prep, electric_heater, grid_connection, road_costs, gas_pip,
                             water_pip, battery_power, battery_cap, other_components,
                             pv_modules, pv_inverter, pv_bos, pv_add_rack, pv_site_prep]
    direct_capex_subtotal_musd = 0 # USD
    direct_capex_subtotal_usd_kw = 0 # USD/KW

    contingencies = 0 #usd/KW

    direct_capex_total_musd = 0  # USD
    direct_capex_total_usd_kw = 0  # USD/KW

    #INDIRET CAPEX

    developer_costs = 0# usd/kw
    financial_costs = 0
    engineering_costs = 0

    indirect_capex_total_musd = 0  # USD
    indirect_capex_total_usd_kw = 0  # USD/KW

    #TOTAL CAPEX
    capex_total = 0
    capex_total_usd_kw = 0

    ### ------ OPEX -------- #####

    # refernces
    ref_admin_cost = [110000, 0.196100]  # MUSD
    ref_op_labor = [110000, 1.335600]  # MUSD
    ref_main_labor = [110000, 0.286200]  # MUSD
    ref_field_main_labor = [977628, 0.212]  # MUSD
    ref_subcontract = [516, 0.2279]  # MUSD
    ref_battery_pp = [0.001, 0.0000069]  # MUSD
    ref_battery_an_gen = [0.001, 0.0000021]  # MUSD
    ref_electricity = [110000, 1.431]  # MUSD
    ref_water = [110000, 1.025232]  # MUSD
    ref_other = [1, 0]  # MUSD
    ref_machinery = [110000, 0.216240]  # MUSD
    ref_spare_parts = [516, 1.331360]  # MUSD


    ref_opex_list = [ref_admin_cost, ref_op_labor, ref_main_labor, ref_field_main_labor, ref_subcontract,
                     ref_battery_pp,
                     ref_battery_an_gen, ref_electricity, ref_water, ref_other, ref_machinery,
                     ref_spare_parts]

    # real OPEX
    admin_cost = [0, 1, 0]  #
    op_labor = [0, 0.7, 0]  #
    main_labor = [0, 0.7, 0]  #
    field_main_labor = [0, 1, 0]  #
    subcontract = [0, 0.7, 0]  #
    battery_pp = [0, 1, 0]  #
    battery_an_gen = [0, 1, 0]  #
    electricity = [0, 1, 0]  #
    water = [0, 1, 0]  #
    other = [0, 1, 0]  #
    machinery = [0, 0.7, 0]  #
    spare_parts = [0, 0.7, 0]  #
    fixed_pv = [0, 0.0175, 0]

    #H2_opex = H2_capex * 0.01

    opex_list = [admin_cost, op_labor, main_labor, field_main_labor, subcontract, battery_pp,
                 battery_an_gen, electricity, water, other, machinery,
                 spare_parts,fixed_pv]

    opex_total_musd = 0  # USD
    opex_total_usd_kw = 0  # USD/KW

    ##------- KPIs -----##
    lcoe = 0
    capacityFactor = 0


    def __init__(self,plant):
        """self.csp_powerblock[0] = plant[0] # MUSD
        self.csp_bop[0] = plant[0] # MUSD
        self.csp_tes[0] = plant[0] # MUSD
        self.csp_sf [0]= plant[0] # MUSD
        self.csp_receiver[0] = plant[0]  # MUSD
        self.csp_Tower[0] = plant[0]  # MUSD
        self.csp_site_prep[0] = plant[0]  # MUSD
        self.electric_heater[0] = plant[0] # MUSD
        self.grid_connection[0] = plant[0] # MUSD
        self.road_costs[0] = plant[0] # MUSD
        self.gas_pip [0]= plant[0] # MUSD
        self.water_pip[0] = plant[0] # MUSD
        self.battery_power[0] = plant[0] # MUSD
        self.battery_cap[0] = plant[0] # MUSD
        self.other_components[0] = plant[0] # MUSD

        self.pv_modules[0] = plant[0] # MUSD
        self.pv_inverter[0] = plant[0] # MUSD
        self.pv_bos[0] = plant[0] # MUSD
        self.pv_add_rack[0] = plant[0]# MUSD
        self.pv_site_prep[0] = plant[0] # MUSD"""


        i=0
        #set the amount values
        self.csp_cap = plant[0]  # KW
        self.sf_area = plant[1]  # m2
        self.thermal_storage = plant[2] # MWh_th
        self.receiver_power = plant[4]  # MW_th
        self.tower_height = plant[5]  # m
        self.el_heater = plant[6]  # KW_th
        self.csp_land = plant[7]  # m2
        self.pv_cap = plant[8]  # Wdc
        self.batt_pp = plant[9]  # MW
        self.batt_cap = plant[10]  # MWh_e
        self.batt_an_gen = plant[11]  # GWh/y
        self.pv_land = plant[12]  # m2
        self.csp_an_gen = plant[13]/1000000  # GWh/y
        self.distance_grid = plant[14]  # km
        self.distance_road = plant[15]  # km
        self.distance_gas = plant[16]  # km
        self.distance_water = plant[17]  # km
        self.other_comp = plant[18]  # unit
        self.inverter_cap = plant[30] # wdc


        self.csp_powerblock = [self.csp_cap, 0.8, 0]  # MUSD
        self.csp_bop = [self.csp_cap, 0.8, 0]  # MUSD
        self.csp_tes = [self.thermal_storage, 0.8, 0]  # MUSD
        self.csp_sf = [self.sf_area, 1, 0]  # MUSD
        self.csp_receiver = [self.receiver_power, 0.2, 0]  # MUSD
        self.csp_Tower = [self.tower_height, 0.8, 0]  # MUSD
        self.csp_site_prep = [self.csp_land, 0.9, 0]  # MUSD
        self.electric_heater = [self.el_heater, 1, 0]  # MUSD
        self.grid_connection = [self.distance_grid, 1, 0]  # MUSD
        self.road_costs = [self.distance_road, 1, 0]  # MUSD
        self.gas_pip = [self.distance_gas, 1, 0]  # MUSD
        self.water_pip = [self.distance_water, 1, 0]  # MUSD
        self.battery_power = [self.batt_pp, 1, 0]  # MUSD
        self.battery_cap = [self.batt_cap, 1, 0]  # MUSD
        self.other_components = [self.other_comp, 1, 0]  # MUSD
        self.pv_modules = [self.pv_cap, 1, 0]  # MUSD
        self.pv_inverter = [self.inverter_cap, 1, 0]  # MUSD
        self.pv_bos = [self.pv_cap, 1, 0]  # MUSD
        self.pv_add_rack = [self.pv_cap, 1, 0]  # MUSD
        self.pv_site_prep = [self.pv_land, 1, 0]  # MUSD


        #print(self.csp_cap)
        #print(self.csp_powerblock[0])

        self.direct_capex_subtotal = [self.csp_powerblock, self.csp_bop, self.csp_tes, self.csp_sf, self.csp_receiver, self.csp_Tower,
                                 self.csp_site_prep, self.electric_heater, self.grid_connection, self.road_costs,self.gas_pip,
                                 self.water_pip, self.battery_power, self.battery_cap, self.other_components,
                                 self.pv_modules, self.pv_inverter, self.pv_bos, self.pv_add_rack, self.pv_site_prep]

        for j in range(len(self.direct_capex_subtotal)):
            self.direct_capex_subtotal[j][2] = self.ref_direct_capex_subtotal[j][1]*(self.direct_capex_subtotal[j][0]/
                                                                                     self.ref_direct_capex_subtotal[j][0])**self.direct_capex_subtotal[j][1]
        for cost in self.direct_capex_subtotal:
            self.direct_capex_subtotal_musd = self.direct_capex_subtotal_musd + cost[2]



        # add H2 to capex
        #self.direct_capex_subtotal_musd = self.direct_capex_subtotal_musd + self.H2_capex



        self.direct_capex_subtotal_usd_kw = self.direct_capex_subtotal_musd*1000000/(self.csp_powerblock[0] +
                                                                                     (self.pv_modules[0]/1000))

        self.contingencies = 0.1*self.direct_capex_subtotal_musd

        self.direct_capex_total_musd = self.direct_capex_subtotal_musd + self.contingencies  # USD
        self.direct_capex_total_usd_kw =self.direct_capex_total_musd*1000000/(self.csp_powerblock[0] +
                                                                                     (self.pv_modules[0]/1000))  # USD/KW  # USD/KW

        self.developer_costs = 0.07*self.direct_capex_total_musd
        self.financial_costs = 0
        self.engineering_costs = 0.14*self.direct_capex_total_musd


        self.indirect_capex_total_musd = self.developer_costs+self.financial_costs+ self.engineering_costs# USD
        self.indirect_capex_total_usd_kw = self.indirect_capex_total_musd*1000000/(self.csp_powerblock[0] +
                                                                                     (self.pv_modules[0]/1000))  # USD/KW


        self.capex_total = self.indirect_capex_total_musd + self.direct_capex_total_musd
        self.capex_total_usd_kw = self.capex_total*1000000/(self.csp_powerblock[0] +
                                                            (self.pv_modules[0]/1000))  # USD/KW

        # real OPEX
        self.admin_cost = [self.csp_cap, 1, 0]  #
        self.op_labor = [self.csp_cap, 0.7, 0]  #
        self.main_labor = [self.csp_cap, 0.7, 0]  #
        self.field_main_labor = [self.sf_area, 1, 0]  #
        self.subcontract = [self.csp_an_gen, 0.7, 0]  #
        self.battery_pp = [self.batt_pp, 1, 0]  #
        self.battery_an_gen = [self.batt_an_gen, 1, 0]  #
        self.electricity = [self.csp_cap, 1, 0]  #
        self.water = [self.csp_cap, 1, 0]  #
        self.other = [self.other_comp, 1, 0]  #
        self.machinery = [self.csp_cap, 0.7, 0]  #
        self.spare_parts = [self.csp_an_gen, 0.7, 0]  #


        capex_pv = self.pv_modules[2] + self.pv_inverter[2] + self.pv_bos[2] + self.pv_add_rack[2] + self.pv_site_prep[2]

        self.fixed_pv = [capex_pv, 0.0175, 0]

        self.opex_list = [self.admin_cost, self.op_labor, self.main_labor, self.field_main_labor, self.subcontract, self.battery_pp,
                     self.battery_an_gen, self.electricity, self.water, self.other, self.machinery,
                     self.spare_parts,self.fixed_pv]

        for j in range(len(self.opex_list)):
            if j < len(self.opex_list) - 1:
                self.opex_list[j][2] = self.ref_opex_list[j][1]*(self.opex_list[j][0]/
                                                                 self.ref_opex_list[j][0])**self.opex_list[j][1]
            else:
                self.opex_list[j][2] = self.fixed_pv[0]*self.fixed_pv[1]

            #print("opex list: ", self.opex_list[j])


        for cost in self.opex_list:

            self.opex_total_musd = (self.opex_total_musd + cost [2])  # USD

        #add H2 opex

        #self.opex_total_musd = self.opex_total_musd + self.H2_opex

        self.opex_total_usd_kw = self.opex_total_musd*1000000/(self.csp_cap +(self.pv_cap/1000))# USD/KW

        #self.lcoe = KPIs.LCOE_simple(self.capex_total,self.opex_total_musd,self.)
