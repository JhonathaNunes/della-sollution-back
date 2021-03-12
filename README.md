# Della solution back

## Como rodar o projeto localmente
- Verifique a versão de instalação do seu python, o projeto está usando a versão 3.7.9
- Instale a lib para acessar a virtual env `pip install virtualenv`
- Crie uma virtual env `virtualenv venv`
- Ative a virtual env `.venv\Scripts\activate`
- Verifique a instalação dos pacotes rodando o comando `pip install -r requirements.txt`
- Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
```
DB_USER=<user>
DB_PASSWORD=<password>
DB_HOST=<host>
DB_PORT=3306
DB_NAME=<db_name>
```
- Para iniciar o servidor flask basta rodar o arquivo `.\app\app.py`
- Para iniciar o servidor com auto reload coloque o atributo `debug=True` na função `app.run()` no arquivo `app.py` **(Lembre de não comentar com o `debug=True`)**
