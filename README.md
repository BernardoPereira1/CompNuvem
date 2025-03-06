# Configuração e Execução da Aplicação

## Pré-requisitos
Certifique-se de que tem os seguintes itens instalados:
- Python 3.x
- Pip (gerenciador de pacotes do Python)
- MySQL Server
- Virtualenv (opcional, mas recomendado)

## Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuração do Banco de Dados

1. **Crie o banco de dados MySQL:**
   ```sql
   CREATE DATABASE todo;
   ```

2. **Crie um arquivo `.env` na raiz do projeto com as configurações do banco:**
   ```ini
   SECRET_KEY=sua-chave-secreta-aqui
   DB_USER=admin
   DB_PASSWORD=admin
   DB_HOST=172.30.249.128
   DB_NAME=todo
   ```

## Execução da Aplicação

1. **Inicialize o banco de dados:**
   ```bash
   flask db upgrade  # Se estiver usando Flask-Migrate
   ```

2. **Execute a aplicação:**
   ```bash
   flask run
   ```
   A aplicação estará disponível em `http://127.0.0.1:5000/`.

## Observações
- Certifique-se de que o MySQL está rodando antes de iniciar a aplicação.
- O arquivo `.env` não deve ser compartilhado ou versionado no Git por questões de segurança.
- Para desativar o ambiente virtual, use `deactivate`.