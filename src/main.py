from cadastro_notas_alunos.bd import (
    criar_banco, 
    inserir_aluno, 
    listar_alunos,
    buscar_por_id,
    buscar_por_nome,
    atualizar_notas,
    remover_aluno
)

if __name__ == "__main__":
    criar_banco()
    
    # inserir_aluno('Bia'), 7, 8)
    
    print("Todos os alunos:")
    alunos = listar_alunos()
    for aluno in alunos:
        print(aluno)

    """ print("\nBuscar por ID:")
    aluno_id = buscar_por_id(1)
    print(aluno_id)

    print("\nBuscar por nome:")
    alunos_por_nome = buscar_por_nome("Maria")
    for aluno in alunos_por_nome:
        print(aluno) """
    
    """ atualizar_notas(3, 1, 10)
    
    notas_atualizadas = buscar_por_id(3)
    print("\nNotas atualizadas:")
    print(notas_atualizadas) """

    """ remover_aluno(7)

print("Após remoção:")
alunos = listar_alunos()
for aluno in alunos:
    print(aluno)
  """