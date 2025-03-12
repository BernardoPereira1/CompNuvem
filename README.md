# Configuração e Execução da Aplicação

## Instalação inicial e configuração das máquinas virtuais com o WSL

1. **Instale as máquinas:**
   ```bash
   wsl --install
   wsl --install -d "Ubuntu 24.04"
   ```

Uma vez que as máquinas foram instaladas definir o nome de utilizador e password.
- Na primeira máquina "Ubuntu" defini o utilizador como "berna" e a password como "berna"
- Na segunda máquina "Ubuntu 24.04" defini o utilizador como  "berna1" e a password como "berna"


## Instalação e configuração do MySQL Server e da base de dados para Acesso Externo

Na primeira máquina siga os seguintes passos:

1. **Instale o mysql-server na primeira máquina:**
   ```bash
   sudo apt install mysql-server
   ```
2. **Corra o serviço mysql:**
   ```bash
   sudo service mysql start
   ```
3. **Abra o arquivo de configuração do MySQL:**
   ```sh
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   ```
4. **Encontre a linha contendo `bind-address` e altere para:**
   ```ini
   bind-address = 0.0.0.0
   ```
5. **Salve o arquivo e feche o mesmo**

6. **Aceda ao mysql:**
   ```sh
   sudo mysql
   ```
7. **Crie um usuário remoto:**
   ```sql
   CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';
   ```
8. **Conceda permissões ao usuário:**
   ```sql
   GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
   ```
9. **Aplique as alterações:**
   ```sql
   FLUSH PRIVILEGES;
   ```
10. **Saia do MySQL:**
   ```sql
   EXIT;
   ```
11. **Reenicie o serviço mysql:**
   ```bash
   sudo service mysql restart
   ```
12. **Volte a aceder ao mysql:**
   ```bash
   sudo mysql
   ```
13. **Crie uma base de dados de teste:**
   ```sql
   Create database db_teste;
   ```
14. **Saia do MySQL:**
   ```sql
   EXIT;
   ```

## Acesso e teste à base de dados pela segunda máquina.

Já na segunda máquina siga os seguintes passos:

1. **Instale o mysql client:**
   ```bash
   sudo apt install mysql-client
   ```

2. **Descubra o ip da primeira máquina:**
   Este comando deve ser executado na primera maquina!
   ```bash
   hostname -I
   ```

3. **Corra o comando de acesso ao mysql server:**
   ```bash
   mysql -h ip_PrimeiraMaquina -u admin -p
   ```
   O sistema vai pedir para inserir a password que será a que foi definida na primeira máquina no mysql ao criar o utilizador!

Se o mysql for aberto é porque a conexão foi concluida com sucesso e temos acesso à base de dados.

## Configuração da aplicação

   Esta configuração deve ser feita na segunda máquina uma vez que só utilizamos a primeira para a base de dados

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

   4. **Crie um arquivo `.env` na raiz do projeto com as configurações do banco:**
   ```ini
   SECRET_KEY=sua-chave-secreta-aqui
   DB_USER=admin
   DB_PASSWORD=passwordMysql
   DB_HOST=ip_PrimeiraMaquina
   DB_NAME=db_exemplo
   ```

   5. **Execute a aplicação:**
   ```bash
   python3 app.py
   ```











