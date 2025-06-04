import tkinter as tk
from tkinter import messagebox
import sys
import os

pasta_atual_interface = os.path.dirname(os.path.abspath(__file__))
pasta_cadastro_alunos = os.path.join(pasta_atual_interface, 'cadastro_notas_alunos')
sys.path.append(pasta_cadastro_alunos)

try:
    from bd import (
        criar_banco,
        inserir_aluno,
        listar_alunos,
        buscar_por_id,
        atualizar_notas,
        remover_aluno
    )
except ImportError:
    messagebox.showerror("Erro Crítico", "Não foi possível encontrar o arquivo 'bd.py'. Verifique a estrutura de pastas.")
    sys.exit(1)


entry_id_operacao = None
entry_nome = None
entry_nota1 = None
entry_nota2 = None
listbox_alunos = None
label_status = None


def adicionar_aluno_interface():
    global label_status

    nome = entry_nome.get()
    nota1_texto = entry_nota1.get()
    nota2_texto = entry_nota2.get()

    if not nome or not nota1_texto or not nota2_texto:
        messagebox.showwarning("Atenção", "Por favor, preencha nome, nota 1 e nota 2.")
        if label_status: label_status.config(text="Erro: Faltam dados para adicionar.")
        return

    try:
        nota1 = float(nota1_texto)
        nota2 = float(nota2_texto)
        if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10):
            messagebox.showwarning("Atenção", "As notas devem ser entre 0 e 10.")
            if label_status: label_status.config(text="Erro: Notas fora do intervalo 0-10.")
            return
    except ValueError:
        messagebox.showerror("Erro de Entrada", "As notas 1 e 2 devem ser números.")
        if label_status: label_status.config(text="Erro: Notas inválidas.")
        return

    try:
        inserir_aluno(nome, nota1, nota2) 
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' adicionado!")
        limpar_campos_interface()
        atualizar_lista_alunos_interface()
        if label_status: label_status.config(text=f"Aluno '{nome}' adicionado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não consegui adicionar o aluno.\nDetalhe: {e}")
        if label_status: label_status.config(text="Erro ao adicionar no banco de dados.")

def atualizar_lista_alunos_interface():
    global listbox_alunos, label_status
    if listbox_alunos is None:
        return

    listbox_alunos.delete(0, tk.END)

    try:
        todos_os_alunos = listar_alunos()
        if todos_os_alunos:
            for aluno in todos_os_alunos:
                texto_aluno = f"ID: {aluno[0]} | {aluno[1]} | N1: {aluno[2]} | N2: {aluno[3]} | Média: {aluno[4]:.1f}"
                listbox_alunos.insert(tk.END, texto_aluno)
            if label_status: label_status.config(text="Lista de alunos atualizada.")
        else:
            if label_status: label_status.config(text="Nenhum aluno cadastrado.")

    except Exception as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não consegui listar os alunos.\nDetalhe: {e}")
        if label_status: label_status.config(text="Erro ao listar alunos do banco.")


def carregar_aluno_para_campos():
    global entry_id_operacao, entry_nome, entry_nota1, entry_nota2, label_status

    id_texto = entry_id_operacao.get()
    if not id_texto:
        messagebox.showwarning("Atenção", "Digite um ID para carregar o aluno.")
        if label_status: label_status.config(text="Digite um ID para carregar.")
        return

    try:
        id_aluno = int(id_texto)
    except ValueError:
        messagebox.showerror("Erro de Entrada", "O ID deve ser um número.")
        if label_status: label_status.config(text="ID inválido (não é número).")
        return

    try:
        aluno = buscar_por_id(id_aluno)
        if aluno:
            entry_nome.delete(0, tk.END)
            entry_nota1.delete(0, tk.END)
            entry_nota2.delete(0, tk.END)

            entry_nome.insert(0, aluno[1])
            entry_nota1.insert(0, str(aluno[2]))
            entry_nota2.insert(0, str(aluno[3]))
            if label_status: label_status.config(text=f"Aluno ID {id_aluno} carregado.")
        else:
            messagebox.showinfo("Não Encontrado", f"Aluno com ID {id_aluno} não existe.")
            if label_status: label_status.config(text=f"Aluno ID {id_aluno} não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não consegui buscar o aluno.\nDetalhe: {e}")
        if label_status: label_status.config(text="Erro ao buscar aluno no banco.")


def atualizar_notas_interface():
    global label_status
    id_texto = entry_id_operacao.get()
    nova_nota1_texto = entry_nota1.get()
    nova_nota2_texto = entry_nota2.get()

    if not id_texto or not nova_nota1_texto or not nova_nota2_texto:
        messagebox.showwarning("Atenção", "Para atualizar, preencha o ID do aluno e as novas notas.")
        if label_status: label_status.config(text="Faltam dados para atualizar.")
        return

    try:
        id_aluno = int(id_texto)
        nova_nota1 = float(nova_nota1_texto)
        nova_nota2 = float(nova_nota2_texto)
        if not (0 <= nova_nota1 <= 10 and 0 <= nova_nota2 <= 10):
            messagebox.showwarning("Atenção", "As novas notas devem ser entre 0 e 10.")
            if label_status: label_status.config(text="Erro: Novas notas fora do intervalo.")
            return
    except ValueError:
        messagebox.showerror("Erro de Entrada", "ID deve ser número, e notas também.")
        if label_status: label_status.config(text="Erro: ID ou notas inválidas.")
        return

    aluno_existe = buscar_por_id(id_aluno)
    if not aluno_existe:
        messagebox.showerror("Erro", f"Aluno com ID {id_aluno} não encontrado. Não é possível atualizar.")
        if label_status: label_status.config(text=f"Aluno ID {id_aluno} não existe para atualizar.")
        return

    try:
        atualizar_notas(id_aluno, nova_nota1, nova_nota2)
        messagebox.showinfo("Sucesso", f"Notas do aluno ID {id_aluno} atualizadas!")
        limpar_campos_interface()
        atualizar_lista_alunos_interface()
        if label_status: label_status.config(text=f"Notas do ID {id_aluno} atualizadas.")
    except Exception as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não consegui atualizar as notas.\nDetalhe: {e}")
        if label_status: label_status.config(text="Erro ao atualizar notas no banco.")


def remover_aluno_interface():
    global label_status
    id_texto = entry_id_operacao.get()
    if not id_texto:
        messagebox.showwarning("Atenção", "Digite o ID do aluno para remover.")
        if label_status: label_status.config(text="Digite um ID para remover.")
        return

    try:
        id_aluno = int(id_texto)
    except ValueError:
        messagebox.showerror("Erro de Entrada", "O ID deve ser um número.")
        if label_status: label_status.config(text="ID inválido para remover.")
        return


    confirmar = messagebox.askyesno("Confirmar Remoção", f"Tem certeza que quer remover o aluno com ID {id_aluno}?")

    if confirmar:
        try:

            aluno_existe = buscar_por_id(id_aluno) #
            if not aluno_existe:
                messagebox.showerror("Erro", f"Aluno com ID {id_aluno} não encontrado. Nada para remover.")
                if label_status: label_status.config(text=f"Aluno ID {id_aluno} não existe para remover.")
                return

            remover_aluno(id_aluno) #
            messagebox.showinfo("Sucesso", f"Aluno ID {id_aluno} removido!")
            limpar_campos_interface()
            atualizar_lista_alunos_interface()
            if label_status: label_status.config(text=f"Aluno ID {id_aluno} removido.")
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não consegui remover o aluno.\nDetalhe: {e}")
            if label_status: label_status.config(text="Erro ao remover aluno do banco.")
    else:
        if label_status: label_status.config(text="Remoção cancelada.")


def limpar_campos_interface():
    global entry_id_operacao, entry_nome, entry_nota1, entry_nota2, label_status
    if entry_id_operacao: entry_id_operacao.delete(0, tk.END)
    if entry_nome: entry_nome.delete(0, tk.END)
    if entry_nota1: entry_nota1.delete(0, tk.END)
    if entry_nota2: entry_nota2.delete(0, tk.END)
    if entry_nome: entry_nome.focus_set()
    if label_status: label_status.config(text="Campos limpos.")

def ao_selecionar_item_na_lista(event_qualquer):

    global listbox_alunos, entry_id_operacao, label_status

    if not listbox_alunos.curselection():
        return

    indice_selecionado = listbox_alunos.curselection()[0]
    texto_do_item = listbox_alunos.get(indice_selecionado)


    try:
        id_str = texto_do_item.split('|')[0].split(':')[1].strip()
        if entry_id_operacao:
            entry_id_operacao.delete(0, tk.END)
            entry_id_operacao.insert(0, id_str)
        if label_status: label_status.config(text=f"ID {id_str} selecionado. Use 'Carregar' para ver detalhes.")
    except Exception:
        if label_status: label_status.config(text="Não consegui pegar o ID do item selecionado.")



if __name__ == "__main__":

    try:
        criar_banco() #
    except Exception as e:
        messagebox.showerror("Erro Crítico de Banco", f"Não foi possível criar o banco de dados.\nO programa não pode continuar.\nDetalhe: {e}")
        sys.exit(1)

    janela = tk.Tk()
    janela.title("Sistema de Notas (Versão Simples)")
    janela.geometry("600x550") # Tamanho da janela

    frame_entradas = tk.Frame(janela, pady=10)
    frame_entradas.pack(fill=tk.X)

    tk.Label(frame_entradas, text="ID (p/ Carregar/Atualizar/Remover):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    entry_id_operacao = tk.Entry(frame_entradas, width=10)
    entry_id_operacao.grid(row=0, column=1, padx=5, pady=2, sticky="w")

    tk.Label(frame_entradas, text="Nome do Aluno:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    entry_nome = tk.Entry(frame_entradas, width=40)
    entry_nome.grid(row=1, column=1, padx=5, pady=2, sticky="w")

    tk.Label(frame_entradas, text="Nota 1:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    entry_nota1 = tk.Entry(frame_entradas, width=10)
    entry_nota1.grid(row=2, column=1, padx=5, pady=2, sticky="w")

    tk.Label(frame_entradas, text="Nota 2:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    entry_nota2 = tk.Entry(frame_entradas, width=10)
    entry_nota2.grid(row=3, column=1, padx=5, pady=2, sticky="w")


    frame_botoes = tk.Frame(janela, pady=10)
    frame_botoes.pack()

    tk.Button(frame_botoes, text="Adicionar Novo Aluno", command=adicionar_aluno_interface, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Carregar Aluno (por ID)", command=carregar_aluno_para_campos, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Atualizar Notas", command=atualizar_notas_interface, width=15).pack(side=tk.LEFT, padx=5)

    frame_botoes2 = tk.Frame(janela, pady=5) # Segunda linha de botões
    frame_botoes2.pack()
    tk.Button(frame_botoes2, text="Remover Aluno (por ID)", command=remover_aluno_interface, width=20, bg="salmon").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes2, text="Listar Todos na Lista Abaixo", command=atualizar_lista_alunos_interface, width=25).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes2, text="Limpar Campos", command=limpar_campos_interface, width=15).pack(side=tk.LEFT, padx=5)


    tk.Label(janela, text="Alunos Cadastrados:").pack(pady=(10,0))
    listbox_alunos = tk.Listbox(janela, height=10, width=80)
    listbox_alunos.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

    listbox_alunos.bind('<<ListboxSelect>>', ao_selecionar_item_na_lista)


    scrollbar_lista = tk.Scrollbar(listbox_alunos, orient="vertical")
    scrollbar_lista.config(command=listbox_alunos.yview)
    scrollbar_lista.pack(side="right", fill="y")
    listbox_alunos.config(yscrollcommand=scrollbar_lista.set)



    label_status = tk.Label(janela, text="Bem-vindo! Clique em 'Listar' para ver os alunos.", relief=tk.SUNKEN, anchor=tk.W, bd=1)
    label_status.pack(side=tk.BOTTOM, fill=tk.X, pady=(5,0), padx=0)


    atualizar_lista_alunos_interface()

    janela.mainloop()