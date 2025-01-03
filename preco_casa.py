#imports para csv
import vaex
import numpy as np

#imports para parte gráfica
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox

#import d'arquivo
import os

#import gráficos de estatística
import matplotlib.pyplot as plt

#funcao para carregar o csv
def carregar_dataframe(): 
    original = 'C:/python/trabalho/Preços casas.csv'
    caminho_arquivo = 'C:/python/trabalho/Backup_Preços casas.csv'
    caminho_csv_anterior = 'C:/python/trabalho/Anterior_Preços casas.csv'
    
    tamanho_original = 0
    tamanho_anterior = 0
    
    #verifica se um csv anterior já foi aberto alguma vez
    if os.path.exists(caminho_csv_anterior):
        tamanho_original = os.path.getsize(original)
        tamanho_anterior = os.path.getsize(caminho_csv_anterior)
        
        #se o csv original for maior que o anterior ele carrega o original
        #por seu conteúdo ter mudado em algumas linhas 
        if tamanho_original > tamanho_anterior:
            df = vaex.open(original)

            return df

    #se o arquivo original não foi modificado ele carrega o mapeado
    #se não, carrega o anterior
    if os.path.exists(caminho_arquivo):
        df = vaex.open(caminho_arquivo)
    else:
        df = vaex.open(original)

    return df

#função para filtrar o csv
def filtrar_df():
    #carrega o csv
    df = carregar_dataframe()

    #caso não seja o csv mapeado ele o mapeia
    if 'Neighborhood_int' not in df.get_column_names():
        neighborhood_map = {'Urban': 1, 'Rural': 2, 'Suburb': 3}
        df['Neighborhood_int'] = df['Neighborhood'].map(neighborhood_map)

    #organiza por maior preço para uma função posterior, 
    #por estética e eficiência
    df_sorted = df.sort('Price', ascending=False) 
    
    #fecha o csv anterior já que agora o csv está no df_sorted
    df.close()
    
    return df_sorted

def calcular_correlacao():
    #recebe o csv filtrado
    df_sorted = filtrar_df()

    #remove a coluna Neighborhood e adiciona a coluna mapeada Neighborhood_int no final
    colunas_numericas = ['Price', 'SquareFeet', 'Bedrooms', 'Bathrooms', 'YearBuilt', 'Neighborhood_int']
    
    #faz a correlação com preço (primeira casa do vetor)
    correlacao = df_sorted.correlation(colunas_numericas, y=None)
    
    #fecha o csv
    df_sorted.close()
    
    #retorna toda a linha da correlação de preço e as colunas
    return (correlacao[:, 0], colunas_numericas)

#função para printar a correlação
def printar_correlacao():
    #recebe a correlação e as colunas
    (correlacoes_com_price, colunas_numericas) = calcular_correlacao()

    #resultado sera criado posteriormente em código
    #porém criado primeira na parte de interpretação do python
    
    #deleta o conteúdo da caixa de texto
    resultado.delete(1.0, tk.END)

    #insere um título(guia) para a caixa de texto
    resultado.insert(tk.END, "As duas características que mais influenciam na compra de uma casa são:\n\n")
    
    #vetor para amazenar os índices dos maiores valores
    maiores_indices = []
    
    #consegue o valor e índice do maior valor resultante da correlação diferente de preço (1.0)
    maior = 0
    for i in range(len(np.argsort(np.abs(correlacoes_com_price))[::-1][1:6])):
        if correlacoes_com_price[i+1] > maior: maior = correlacoes_com_price[i+1]
        maiores_indices.append(i+1)
        
    #consegue o valor e índice do segundo maior valor resultante da correlação diferente de preço (1.0)    
    maior2 = 0
    for i in range(len(np.argsort(np.abs(correlacoes_com_price))[::-1][1:6])):
        if correlacoes_com_price[i] > maior2 and correlacoes_com_price[i] < maior: maior2 = correlacoes_com_price[i]
        maiores_indices.append(i)
        
    #atribui ao vetor os índices   
    maiores_valores = [maior, maior2]

    #printa na caixa de texto a coluna e o valor
    for i in range(len(maiores_valores)):
        resultado.insert(tk.END, f"{colunas_numericas[maiores_indices[i]]}: {maiores_valores[i]}\n")

    #pop-up de conclusão
    messagebox.showinfo("Concluído", "Correlações calculadas com sucesso!")

#função para mostrar o gráfico de correlação
def grafico():
    #recebe a correlação e as colunas
    (correlacoes_com_price, colunas_numericas) = calcular_correlacao()
    
    #consegue o indice e o valor das maiores correlações(valor absoluto, ou seja positivo)
    #em um intervalo que pegue todos os valores menos o preço
    indices_maiores_correlacoes = np.argsort(np.abs(correlacoes_com_price))[::-1][1:6]
    valores_maiores_correlacoes = correlacoes_com_price[indices_maiores_correlacoes]

    #cria figuras de tamanho 10 / 6
    plt.figure(figsize=(10, 6))
    
    #cria as colunas dos indices e valores absolutos em cor azul
    plt.bar([colunas_numericas[idx] for idx in indices_maiores_correlacoes], np.abs(valores_maiores_correlacoes), color='blue')
    
    #tabelas para indentificar sobre o que é
    plt.xlabel('Características das casas')
    plt.ylabel('Correlação com o Preço das casas')
    plt.title('Características que Mais Influenciam o Preço da Casa')
    
    #deixa um pouco maior na tela
    plt.tight_layout()
    
    #mostra o gráfico
    plt.show()
    
#funcao para mostrar as casas mais caras
def grafico2():
    #remove algo se já tiver na caixa de texto
    resultado2.delete(1.0, tk.END)
    
    #inseri um título de guia na caixa de texto
    resultado2.insert(tk.END, "As 20 casas mais caras são:\n\n")
    
    #recebe o csv já ordenado do maior para menor em preço
    df_sorted = filtrar_df()
    
    #printa na caixa as 20 primeiras casas
    resultado2.insert(tk.END, f"{df_sorted.head(20)}\n")

#função para exportar o csv
def exportar():
    #carrega o csv filtrado e sem filtragem
    df = filtrar_df()
    df2 = carregar_dataframe()
    
    #exporta o csv filtrado e modificado
    df.export_csv('C:/python/trabalho/Backup_Preços casas.csv')
    df.close()
    
    #exporta o csv original
    df2.export_csv('C:/python/trabalho/Anterior_Preços casas.csv') 
    df2.close()
    
    #mostra uma msg de conclusão
    messagebox.showinfo("Concluído", "CSV Exportado com sucesso!")

#cria a janela
janela = tk.Tk()

#define a escala da janela
janela.geometry("800x600")

#define o fundo da janela para preto
janela.configure(bg="black")

#titulo da janela
janela.title("Análise das Duas Maiores Influências na Compra de uma Casa")

#botao para printar a correlação
calcular = tk.Button(
    janela, text="Calcular Correlação", 
    command=printar_correlacao, 
    font=("Times New Roman", 16), 
    bg="black", 
    fg="white",
    borderwidth=2,
    relief="groove",
    highlightbackground="white",
    cursor="Hand2"
)

#posição do botão (semelhante a html)
calcular.pack(padx=40, pady=10)

#caixa de texto1
resultado = scrolledtext.ScrolledText(
    janela, 
    width=150, 
    height=5,
    font=("Times New Roman", 20), 
    bg="black", 
    fg="white",
    borderwidth=2,
    relief="groove",
    highlightbackground="white"
)

#posição da caixa de texto1 (semelhante a html)
resultado.pack(padx=40, pady=10)

#botão para o gráfico
graficos = tk.Button(
    janela, 
    text="mostrar gráfico", 
    command=grafico,
    font=("Times New Roman", 16), 
    bg="black", 
    fg="white",
    borderwidth=2,
    relief="groove",
    highlightbackground="white",
    cursor="Hand2"
)

#posição do botão (semelhante a html)
graficos.pack(padx=40, pady=10)

#botão para printar as 20 casas mais caras
graficos2 = tk.Button(
    janela, 
    text="20 casas mais caras", 
    command=grafico2,
    font=("Times New Roman", 16), 
    bg="black", 
    fg="white",
    borderwidth=2,
    relief="groove",
    highlightbackground="white",
    cursor="Hand2"
)

#posição do botão (semelhante a html)
graficos2.pack(padx=40, pady=10)

#caixa de texto2
resultado2 = scrolledtext.ScrolledText(
    janela, 
    width=150, 
    height=6,
    font=("Times New Roman", 20), 
    bg="black", 
    fg="white",
    borderwidth=2,
    relief="groove",
    highlightbackground="white"
)

#posição da caixa de texto2 (semelhante a html)
resultado2.pack(padx=40, pady=10)

#botão para exportar o csv
export = tk.Button(
    janela, 
    text="exportar csv", 
    command=exportar,
    font=("Times New Roman", 20), 
    bg="black", 
    fg="white",
    borderwidth=2,
    relief="groove",
    highlightbackground="white",
    cursor="Hand2"
)

#posição do botão (semelhante a html)
export.pack(padx=40, pady=20)

#loop para a janela ficar aberta até ser fechada
janela.mainloop()