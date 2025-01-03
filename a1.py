import pandas as pd

csv = pd.read_csv('C:/python/trabalho/Preços casas.csv')

nomes_colunas = ['SquareFeet', 'Bedrooms', 'Bathrooms', 'YearBuilt', 'Price', 'valor_bairro']

csv['valor_bairro'] = (csv['Neighborhood'].str.replace("Urban", "1"))
csv['valor_bairro'] = (csv['valor_bairro'].str.replace("Rural", "2"))
csv['valor_bairro'] = (csv['valor_bairro'].str.replace("Suburb", "3"))

preco = csv.drop(columns=['Neighborhood'])

valores = preco.corr()

valores = valores['Price']

indices = []

maior1 = 0
valori = 0

for i in range(len(valores)):
    if valores.iloc[i] != 1.0 and valores.iloc[i] > maior1:
        maior1 = valores.iloc[i]
        valori = i
        
indices.append(valori)

maior2, valori = 0, 0

for i in range(len(valores)):
    if valores.iloc[i] != 1.0 and valores.iloc[i] < maior1 and valores.iloc[i] > maior2:
        maior2 = valores.iloc[i]
        valori = i
        
indices.append(valori)

print("os principais valores pra casa é: ")

for i in range(len(indices)):
    print(nomes_colunas[indices[i]])