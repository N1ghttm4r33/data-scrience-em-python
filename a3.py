import pandas as pd

csv = pd.read_csv('D:/trabalho/Analise de sálarios e profissões.csv')

csv = csv.dropna()

csv['Salary_In_Rupees'] = csv['Salary_In_Rupees'].str.replace(',', '').astype(float)

salarios_medios = csv.groupby(['Designation', 'Employee_Location'])['Salary_In_Rupees'].mean().to_dict()

melhor_profissao, melhor_localizacao = max(salarios_medios, key=salarios_medios.get)
salario_maximo = salarios_medios[(melhor_profissao, melhor_localizacao)]

print("Profissão com maior salário médio:", melhor_profissao)
print("Localização com maior salário médio:", melhor_localizacao)
print("Maior média salárial encontrada:", salario_maximo)