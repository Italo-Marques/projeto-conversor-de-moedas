import requests
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Função para pegar a taxa de câmbio entre duas moedas
def pegar_taxa_cambio(api_key, moeda_origem):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{moeda_origem}"
    
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        
        if resposta.status_code != 200:
            raise Exception(f"Erro ao buscar a taxa de câmbio: {dados['error-type']}")

        return dados['conversion_rates']

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao acessar a API: {e}")
        return None

# Função para converter valores
def converter_moeda(valor, taxa_cambio, moeda_destino):
    return valor * taxa_cambio.get(moeda_destino, 1)

# Função para exibir histórico de conversão
def exibir_historico(historico_text):
    historico_window = tk.Toplevel()
    historico_window.title("Histórico de Conversão")
    historico_text_area = tk.Text(historico_window, wrap=tk.WORD, width=50, height=10)
    historico_text_area.insert(tk.END, historico_text)
    historico_text_area.pack()

# Função para realizar a conversão
def realizar_conversao():
    moeda_origem = origem_combobox.get().upper()
    moedas_destino = destino_combobox.get().upper().split(',')
    valor = float(valor_entry.get())
    taxa_cambio = pegar_taxa_cambio(api_key, moeda_origem)

    if taxa_cambio:
        resultado = ""
        historico = f"Conversão realizada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        for moeda in moedas_destino:
            valor_convertido = converter_moeda(valor, taxa_cambio, moeda)
            resultado += f"{valor:.2f} {moeda_origem} = {valor_convertido:.2f} {moeda}\n"
            historico += f"{valor:.2f} {moeda_origem} -> {valor_convertido:.2f} {moeda}\n"
        
        resultado_label.config(text=resultado)
        historico_conversao.append(historico)

# Função para exibir histórico completo
def mostrar_historico():
    if historico_conversao:
        exibir_historico('\n'.join(historico_conversao))
    else:
        messagebox.showinfo("Histórico", "Nenhum histórico de conversão disponível.")

# Função para limpar a interface
def limpar_campos():
    origem_combobox.set('')
    destino_combobox.set('')
    valor_entry.delete(0, tk.END)
    resultado_label.config(text="")

# Função para fechar o aplicativo
def sair():
    window.destroy()

# Função para salvar histórico em um arquivo
def salvar_historico():
    with open('historico_conversao.txt', 'w') as file:
        file.write('\n'.join(historico_conversao))
    messagebox.showinfo("Salvar Histórico", "Histórico salvo em 'historico_conversao.txt'.")

# Função de ajuda
def mostrar_ajuda():
    help_message = "Use o conversor para converter valores entre diferentes moedas. \n" \
                "Selecione a moeda de origem e a moeda(s) de destino, \n" \
                "digite o valor e clique em 'Converter'. \n" \
                "Use 'Mostrar Histórico' para ver suas conversões anteriores."
    messagebox.showinfo("Ajuda", help_message)

# Chave de API
api_key = "c819e4bf47367fd09549d654"  # Insira sua chave de API aqui
historico_conversao = []

# Configuração da interface gráfica
window = tk.Tk()
window.title("Conversor de Moedas")
window.geometry("400x400")
window.configure(bg="#f0f8ff")  # Cor de fundo

# Elementos da interface
moedas = ['USD', 'EUR', 'BRL', 'JPY', 'GBP', 'AUD']  # Lista de moedas

# Moeda de origem
origem_label = tk.Label(window, text="Moeda de origem:", bg="#f0f8ff")
origem_label.pack(pady=5)
origem_combobox = ttk.Combobox(window, values=moedas, state='readonly', font=("Helvetica", 12))
origem_combobox.pack(pady=5)

# Moeda(s) de destino
destino_label = tk.Label(window, text="Moeda(s) de destino (separar por vírgula):", bg="#f0f8ff")
destino_label.pack(pady=5)
destino_combobox = ttk.Combobox(window, values=moedas, state='readonly', font=("Helvetica", 12))
destino_combobox.pack(pady=5)

# Valor a ser convertido
valor_label = tk.Label(window, text="Valor a ser convertido:", bg="#f0f8ff")
valor_label.pack(pady=5)
valor_entry = tk.Entry(window)
valor_entry.pack(pady=5)

# Resultado da conversão
resultado_label = tk.Label(window, text="", font=("Helvetica", 12), fg="green", bg="#f0f8ff")
resultado_label.pack(pady=5)

# Botões da interface
converter_button = tk.Button(window, text="Converter", command=realizar_conversao, bg="#4CAF50", fg="white")
converter_button.pack(pady=5)

historico_button = tk.Button(window, text="Mostrar Histórico", command=mostrar_historico, bg="#2196F3", fg="white")
historico_button.pack(pady=5)

salvar_button = tk.Button(window, text="Salvar Histórico", command=salvar_historico, bg="#FF9800", fg="white")
salvar_button.pack(pady=5)

ajuda_button = tk.Button(window, text="Ajuda", command=mostrar_ajuda, bg="#9C27B0", fg="white")
ajuda_button.pack(pady=5)

limpar_button = tk.Button(window, text="Limpar", command=limpar_campos, bg="#f44336", fg="white")
limpar_button.pack(pady=5)

sair_button = tk.Button(window, text="Sair", command=sair, bg="#607D8B", fg="white")
sair_button.pack(pady=5)

# Inicializa a interface gráfica
window.mainloop()
