# Aplicação Web de Gerenciamento de Arquivos

Uma aplicação web para upload, gerenciamento e download de arquivos, com suporte a múltiplos usuários. Cada usuário possui uma área privada onde pode enviar e acessar seus próprios arquivos.

## Funcionalidades

- Cadastro e login de usuários
- Upload de arquivos
- Download de arquivos
- Gerenciamento de arquivos (listar, excluir)
- Área privada para cada usuário

## Tecnologias Utilizadas

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

## Requisitos

- Python 3.x
- Pip

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie um ambiente virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente:
    ```sh
    cp .env.example .env
    # Edite o arquivo .env com suas configurações
    ```

5. Inicialize o banco de dados:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Executando a Aplicação

1. Ative o ambiente virtual, se ainda não estiver ativo:
    ```sh
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

2. Execute a aplicação:
    ```sh
    flask run
    ```

3. Acesse a aplicação no navegador:
    ```
    http://127.0.0.1:5000
    ```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça o push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.