import tkinter as tk
import time
import ttkbootstrap as ttk
from datetime import datetime

# Inicialize a aplicação tkinter com ttkbootstrap
root = ttk.Window(themename="darkly")
root.title("Interface Locadora")
root.geometry("860x560")  # Ajustado para mais espaço
root.resizable(False, False)

# Valor da hora no estacionamento
valorPorHora = 15

# Lista de cores
cores = ["Branco", "Preto", "Azul", "Rosa", "Vermelho", "Amarelo", "Prateado"]

# Criação de campos de entrada e labels
campos = [
    {"campo": "nome", "label": "Nome", "x_label": 10, "y_label": 100, "y_entry": 130},
    {"campo": "placa", "label": "Placa", "x_label": 218, "y_label": 100, "y_entry": 130},
    {"campo": "modelo", "label": "Modelo", "x_label": 425, "y_label": 100, "y_entry": 130},
    {"campo": "cor", "label": "Cor", "x_label": 633, "y_label": 100, "y_entry": 130}
]

entries = {}

def criarCampos(campos):
    for campo in campos:
        label = ttk.Label(root, text=campo["label"])
        label.place(x=campo["x_label"], y=campo["y_label"])
        entry = ttk.Entry(root, bootstyle="DEFAULT")
        entry.place(x=campo["x_label"], y=campo["y_entry"])
        entries[campo["campo"]] = entry

criarCampos(campos)

# Título da aplicação
labelTitulo = ttk.Label(root, text="Locadora de Veículos", font=("Arial", 20))
labelTitulo.place(x=350, y=10)

# Configuração de estilo da Treeview
def configurarEstiloTreeview():
    style = ttk.Style()
    style.configure("Treeview",
                    font=("Arial", 12),
                    rowheight=25,
                    background="#343a40",
                    foreground="white",
                    fieldbackground="#343a40")
    style.configure("Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#212529",
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading",
              background=[("active", "#343a40")])

configurarEstiloTreeview()

# Adicionar a Treeview
colunas = ['nome', 'placa', 'modelo', 'cor', 'entrada', 'saida', 'pago']
larguras = [100, 100, 100, 100, 80, 80, 100]

table = ttk.Treeview(root, columns=colunas, show='headings')
for coluna, largura in zip(colunas, larguras):
    table.heading(coluna, text=coluna.upper(), anchor=tk.W)
    table.column(coluna, minwidth=0, width=largura)
table.place(x=10, y=300, width=840, height=250)

# Dados iniciais
listaNomes = [
    ['Kalita Trevisan', '1234-5678', 'Ferrari', "Branco", "10:30", "-", "-"],
    ['Super Peko', '1234-5678', 'Mustang', "Preto", "12:30", "-", "-"],
    ['Lulinha Trevisan', '1234-5678', 'Tesla Model X', "Prateado", "13:30", "-", "-"]
]

for dados in listaNomes:
    table.insert("", "end", values=dados)

def limparCampos():
    for entry in entries.values():
        entry.delete(0, tk.END)

# Função para Check-in
def checkIn():
    dados = (
        entries["nome"].get(),
        entries["placa"].get(),
        entries["modelo"].get(),
        entries["cor"].get(),
        time.strftime("%H:%M"),
        "-",
        "-"
    )
    table.insert("", "end", values=dados)
    limparCampos()

# Botão Check-in
buttonCheckIn = ttk.Button(root, command=checkIn, text="Check-in", width=20, padding=(5, 10), bootstyle="Primary")
buttonCheckIn.place(x=10, y=200)

# Função para calcular o valor a pagar
def calcularValorPagar(horaEntrada):
    horaAtual = datetime.now().strftime("%H:%M")
    formatoHora = "%H:%M"
    delta = datetime.strptime(horaAtual, formatoHora) - datetime.strptime(horaEntrada, formatoHora)
    horas = delta.total_seconds() / 3600
    valorPagar = horas * valorPorHora
    return round(valorPagar, 2), horaAtual

# Função para exibir a nova janela com informações de check-out
def exibirJanelaCheckout(valores, valorPagar, horaSaida):
    janelaCheckout = tk.Toplevel(root)
    janelaCheckout.title("Check-out")
    janelaCheckout.geometry("500x300")

    colunasCheckout = ['entrada', 'saida', 'valor a pagar']
    largurasCheckout = [150, 150, 150]

    tableCheckout = ttk.Treeview(janelaCheckout, columns=colunasCheckout, show='headings')
    for coluna, largura in zip(colunasCheckout, largurasCheckout):
        tableCheckout.heading(coluna, text=coluna.upper(), anchor=tk.W)
        tableCheckout.column(coluna, minwidth=0, width=largura)
    tableCheckout.place(x=10, y=10, width=480, height=200)

    tableCheckout.insert("", "end", values=(valores[4], horaSaida, f"R$ {valorPagar:.2f}"))

    def marcarPago():
        # Atualiza as colunas "Saida" e "Pago" na tabela principal
        for item in table.selection():
            valores = table.item(item, 'values')
            novos_valores = list(valores)
            novos_valores[5] = horaSaida
            novos_valores[6] = f"R$ {valorPagar:.2f}"
            table.item(item, values=novos_valores)

        janelaCheckout.destroy()

    buttonPago = ttk.Button(janelaCheckout, text="Pago", command=marcarPago, bootstyle="Success")
    buttonPago.place(x=200, y=250)

# Função para Check-out
def checkOut():
    selectedItem = table.selection()
    if selectedItem:
        item = table.item(selectedItem)
        valores = item['values']
        horaEntrada = valores[4]
        valorPagar, horaSaida = calcularValorPagar(horaEntrada)
        exibirJanelaCheckout(valores, valorPagar, horaSaida)

# Botão Check-out
buttonCheckOut = ttk.Button(root, command=checkOut, text="Check-out", width=20, padding=(5, 10), bootstyle="Danger")
buttonCheckOut.place(x=633, y=200)

# Execute o loop principal da aplicação
root.mainloop()
