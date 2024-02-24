# API rinha de backend.

## Sobre esta api.

> Está é uma simples api para a a rinha de backend, *https://github.com/zanfranceschi/rinha-de-backend-2024-q1* desenvolvida em python com  bottle e psycopg2. uma api simples que tem o objetivo de ser leve para ser conteinerizada, rodando atrás de um load balancer. Esta api ainda realizar o intermediario entre o load balancer e banco de dados em postgresql.

### Instruções de Instalação

Para instalar e configurar esta API, siga estas etapas:

1. Clone este repositório para o seu ambiente.
2. Navegue até o diretório do projeto.
3. Crie uma virtual env com o comando:

   -Windows
   ```
    python -m venv <nome-virtualenv>
   ```
   -Linux
   ```
    virtualenv <nome-virtualenv>
   ```
4. Ative sua virtualenv

   -Windows
   ```
    ./<nome-virtualenv>/Scripts/activate
   ```
   -Linux
   ```
    source <nome-virtualenv>/bin/activate
   ```
4. Na raiz da api instale as dependências do projeto:

   ```
   pip install -r requirements.txt
   ```
5. Prencha as informações do exemple.env com informações da sua conexão postgresql e renomei-o para ".env":
6. Execute o projeto:

   ```
   python index.py
   ```
