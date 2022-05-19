import CAPEX
import PowerPlant
import Analysis1
import KPIs
import readData
import saveData
import Analysis
import AnalysisH2
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import toText

print('##### START #####')
#data = readData.readExcelSimple('data/CSPonly_Data_1.xlsx', 82)
#simpleData = Analysis.simpleAnalysis(data,'data/results/CSP_LCOE_results.xlsx')
#print(data)

#dataBigREF = readData.readExcelIndepth('data/Hybrid_Data_input.xlsx',23)

#analysisdata = Analysis.indepthAnalysis(dataBIG, 'data/results/CSPonly_results_BIG.xlsx')
#saveData.saveToExcelInDepth('data/results/CSPonly_results_BIG_new.xlsx',analysisdata)
#d1 = Analysis1.indepthAnalysis(dataBigREF, 'data/Hybrid_Data_input.xlsx')





#use bigData, d and save Data

#dataBIG = readData.readExcelIndepth('data/Hybrid_Data_input_new.xlsx',28)
#d = Analysis1.indepthAnalysis(dataBIG, 'data/results/Stratege1.xlsx')

dataBIGH2 = readData.readExcelIndepth('data/Hybrid_Data_input_HYDRO.xlsx',28)
h2 = AnalysisH2.indepthAnalysis(dataBIGH2, 'data/results/Results_Hydro.xlsx')
#saveData.saveToExcelInDepth('data/results/Results_Hydro.xlsx',h2)

#saveData.saveToExcelInDepth('data/results/Strategy1.xlsx',d)





#toText.toGAMS(dataBIG,'data/results/gamstest.txt')
#toText.OneWeek(dataBIG,'data/results/Weektest.txt')
#toText.genPrice(7,d[0][35])

print('#### END ####')

#analysisBig = Analysis.indepthAnalysis(data,'data/results/CSPonly_resultsBIG.xlsx')

#saveData.saveToExcel('data/testExcel.xlsx',data)




