# Configuração das Vms e Execução da Aplicação

Se **ainda não tem os ficheiros das máquinas virtuais**, segue os passos abaixo para instalar e configurá-las corretamente.  
➡️ [Já tem os ficheiros das VMs? Passe direto para iniciar a aplicação.](#execução-da-aplicação)

## Instalação inicial e configuração das máquinas virtuais com o WSL 

1. **Instale as máquinas:**
   
   ```bash
   wsl --install
   wsl --install -d "Ubuntu 24.04"
   ```

Uma vez que as máquinas foram instaladas deve definir o nome de utilizador e password.

---

## Instalação e configuração do MySQL Server e da base de dados para Acesso Externo

Na primeira máquina siga os seguintes passos:

1. **Instale o mysql-server:**
   ```bash
   sudo apt install mysql-server
   ```
   
2. **Corra o serviço mysql:**
   ```bash
   sudo service mysql start
   ```
   
3. **Abra o arquivo de configuração do MySQL:**
   ```bash
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   ```
   
4. **Encontre a linha contendo `bind-address` e altere para:**
   ```bash
   bind-address = 0.0.0.0
   ```

5. **Aceda ao mysql:**
   ```bash
   sudo mysql
   ```
   
6. **Crie um usuário remoto:**
   ```sql
   CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';
   ```
   
7. **Conceda permissões ao usuário:**
   ```sql
   GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
   ```
   
8. **Aplique as alterações:**
   ```sql
   FLUSH PRIVILEGES;
   ```
   
9. **Saia do MySQL:**
   ```sql
   EXIT;
   ```
10. **Reenicie o serviço mysql:**
   ```bash
   sudo service mysql restart
   ```

11. **Volte a aceder ao mysql:**
   ```bash
   sudo mysql
   ```

12. **Corra o script para criar a base de dados:**
   ```sql
      CREATE DATABASE IF NOT EXISTS todo;
      USE todo;
      
      -- Criar a tabela de usuários
      CREATE TABLE IF NOT EXISTS user (
          id INT AUTO_INCREMENT PRIMARY KEY,
          email VARCHAR(100) NOT NULL UNIQUE,
          password VARCHAR(255) NOT NULL
      );
      
      -- Criar a tabela de tarefas
      CREATE TABLE IF NOT EXISTS task (
          id INT AUTO_INCREMENT PRIMARY KEY,
          descricao VARCHAR(255) NOT NULL,
          data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          user_id INT,
          FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
      );
   ```

13. **Saia do MySQL:**
   ```sql
   EXIT;
   ```

---

## Acesso e teste à base de dados pela segunda máquina

Já na segunda máquina siga os seguintes passos:

1. **Instale o mysql client:**
   ```bash
   sudo apt install mysql-client
   ```

2. **Descubra o ip da primeira máquina:**
   **Este comando deve ser executado na primera maquina!**
   ```bash
   hostname -I
   ```

3. **Corra o comando de acesso ao mysql server:**
   ```bash
   mysql -h ip_PrimeiraMaquina -u admin -p
   ```
   **O sistema vai pedir para inserir a password que será a que foi definida na primeira máquina no mysql ao criar o utilizador!**

Se o mysql for aberto é porque a conexão foi concluida com sucesso e temos acesso à base de dados. Podemos também voltar a entrar no mysql (utilizando o comando de cima) e fazer **SHOW DATABASES;** e verificar que a base de dados **todo** está na lista.

---

## Configuração da aplicação

   **Esta configuração deve ser feita na segunda máquina uma vez que só utilizamos a primeira para a base de dados**

   1. **Clone o repositório:**
   ```bash
   git clone https://github.com/BernardoPereira1/CompNuvem.git
   cd CompNuvem
   ```

   2. **Após entrar na pasta aceda ao projeto pelo vscode:**
   ```bash
   code .
   ```

   3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

   4. **Crie um arquivo `.env` na raiz do projeto com as configurações da base de dados:**
   ```ini
   SECRET_KEY=sua-chave-secreta-aqui
   DB_USER=admin
   DB_PASSWORD=admin
   DB_HOST=ip_PrimeiraMaquina
   DB_NAME=todo
   ```

   5. **Execute a aplicação:**
   ```bash
   python3 app.py
   ```

---

# Execução da Aplicação









