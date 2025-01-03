import pandas as pd

csv = pd.read_csv('D:/trabalho/Banco.csv', sep=';')

csv = csv.dropna()

apr = csv[csv['Loan_Status'] == 'Y']

csv['patrimônio'] = csv['Total_Income'] + apr['LoanAmount']

baixo_medio_patrimonio = csv[csv['patrimônio'] < 15000]

baixo_medio_patrimonio['filho'] = baixo_medio_patrimonio['Dependents'].astype(str).replace("0.0", "Não")

baixo_medio_patrimonio.loc[baixo_medio_patrimonio['filho'] != "Não", 'filho'] = "Sim"

baixo_medio_patrimonio['formado'] = baixo_medio_patrimonio['Education'].replace('Graduate', "Sim")
baixo_medio_patrimonio['formado'] = baixo_medio_patrimonio['formado'].replace('Not Graduate', "Não")

print(baixo_medio_patrimonio[['Property_Area', 'filho', 'formado', 'patrimônio']])