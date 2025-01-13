import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from src.google_sync import sincronizar_tarefas_com_google
from src.database import adicionar_tarefa, listar_tarefas, limpar_tarefas
import tkinter.messagebox as messagebox

def iniciar_interface():
    def adicionar_tarefa_na_interface():
        titulo = entrada_titulo.get()
        descricao = entrada_descricao.get()
        data = calendario.selection_get()  # Obtém a data escolhida no calendário
        hora = entrada_hora.get()

        # Verifica se o título foi preenchido
        if not titulo:
            messagebox.showerror("Erro", "Por favor, preencha o título.")
            return

        # Se a hora não foi preenchida, atribui uma hora padrão
        if not hora:
            hora = "08:00"  # Hora padrão

        # Combina a data e hora escolhidas
        try:
            data_hora = f"{data} {hora}"
            # Valida o formato da data_hora
            datetime.strptime(data_hora, '%Y-%m-%d %H:%M')
        except ValueError:
            messagebox.showerror("Erro", "Formato de data ou hora inválido. Por favor, verifique.")
            return  # Não adiciona a tarefa se o formato for inválido

        # Chama a função para adicionar a tarefa no banco de dados
        adicionar_tarefa(titulo, descricao, data_hora)

        # Limpa os campos após adicionar a tarefa
        entrada_titulo.delete(0, tk.END)
        entrada_descricao.delete(0, tk.END)
        entrada_hora.delete(0, tk.END)

        # Atualiza a lista de tarefas
        atualizar_lista()

    def atualizar_lista():
        tarefas = listar_tarefas()  # Atualiza a lista a partir do banco de dados
        lista_tarefas.delete(0, tk.END)
        for tarefa in tarefas:
            lista_tarefas.insert(tk.END, f"{tarefa[1]} - {tarefa[3]}")  # Exibe título e data

    def limpar_lista():
        # Confirma se o usuário deseja limpar todas as tarefas
        if messagebox.askyesno("Limpar Tarefas", "Tem certeza de que deseja limpar todas as tarefas?"):
            # Limpar as tarefas do banco de dados
            limpar_tarefas()
            lista_tarefas.delete(0, tk.END)

    def sincronizar():
        sincronizar_tarefas_com_google()
        tk.messagebox.showinfo("Sincronização", "Tarefas sincronizadas com o Google Agenda!")

    # Função chamada quando o usuário escolhe uma data no calendário
    def data_selecionada(event):
        data = calendario.selection_get()
        entrada_hora.delete(0, tk.END)
        entrada_hora.insert(0, "08:00")  # Define uma hora padrão quando a data é selecionada

        # Exibe o campo para selecionar a hora
        entrada_hora.grid(row=2, column=1)  # Torna o campo de hora visível

    # Janela Principal
    janela = tk.Tk()
    janela.title("Gerenciador de Tarefas")

    # Título
    tk.Label(janela, text="Título:").grid(row=0, column=0)
    entrada_titulo = tk.Entry(janela)
    entrada_titulo.grid(row=0, column=1)

    # Descrição
    tk.Label(janela, text="Descrição:").grid(row=1, column=0)
    entrada_descricao = tk.Entry(janela)
    entrada_descricao.grid(row=1, column=1)

    # Calendário para escolher a data
    calendario = Calendar(janela, selectmode='day')  # Usando o widget Calendar do tkcalendar
    calendario.grid(row=3, column=0, columnspan=2)
    calendario.bind("<<CalendarSelected>>", data_selecionada)  # Chama a função quando a data for selecionada

    # Campo para escolher a hora
    tk.Label(janela, text="Hora:").grid(row=4, column=0)
    entrada_hora = tk.Entry(janela)  # Inicialmente invisível
    entrada_hora.grid(row=4, column=1)
    entrada_hora.grid_remove()  # Oculta o campo até a seleção de uma data

    # Botão para adicionar tarefa
    tk.Button(janela, text="Adicionar Tarefa", command=adicionar_tarefa_na_interface).grid(row=5, column=1)

    # Botão para sincronizar com o Google Agenda
    tk.Button(janela, text="Sincronizar com Google", command=sincronizar).grid(row=6, column=1)

    # Botão para limpar a lista de tarefas
    tk.Button(janela, text="Limpar Lista", command=limpar_lista).grid(row=7, column=1)

    # Lista de tarefas
    lista_tarefas = tk.Listbox(janela, width=50)
    lista_tarefas.grid(row=8, column=0, columnspan=2)

    # Atualizar lista
    atualizar_lista()

    janela.mainloop()
