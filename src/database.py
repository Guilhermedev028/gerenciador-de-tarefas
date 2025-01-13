import sqlite3

DB_PATH = "database/tarefas.db"

def conectar():
    conn = sqlite3.connect(DB_PATH)  # Ou o nome do seu banco de dados
    return conn

# Função para criar a tabela de tarefas (caso não exista)
def criar_tabela_tarefas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data_hora TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para adicionar uma tarefa no banco de dados
def adicionar_tarefa(titulo, descricao, data_hora):
    conn = conectar()
    cursor = conn.cursor()

    # Criando a tabela, se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data_hora TEXT NOT NULL
    )
    """)

    # Inserindo a tarefa no banco de dados
    cursor.execute("""
    INSERT INTO tarefas (titulo, descricao, data_hora) VALUES (?, ?, ?)
    """, (titulo, descricao, data_hora))

    # Confirmando a transação e fechando a conexão
    conn.commit()
    conn.close()
    print(f"Tarefa '{titulo}' adicionada ao banco de dados")  # Depuração

# Função para listar as tarefas no banco de dados
def listar_tarefas():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    
    conn.close()
    return tarefas

# Função para limpar as tarefas (remover todas)
def limpar_tarefas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas")  # Apaga todas as tarefas
    conn.commit()
    conn.close()

# Criar a tabela ao iniciar o programa
criar_tabela_tarefas()
