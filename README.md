# fast-api-crud-tests

Este é um exemplo de testes de aplicação CRUD utilizando o framework FastAPI.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/MateusZ36/fast-api-crud-tests.git
```

Acesse o diretório do projeto:

```bash
cd fastapi-crud-example
```

Instale as dependências do projeto:

###### Com dependencias para testes:
```bash
pip install -r requirements-dev.txt 
```

###### Sem dependencias para testes:
```bash
pip install -r requirements.txt
```

## Executando o servidor

Para executar o servidor, execute o seguinte comando:

```bash
uvicorn main:app --reload
```

Este comando irá iniciar o servidor no endereço http://localhost:8000. Para acessar a documentação da API, acesse o
endereço http://localhost:8000/docs.

## Executando os testes

Para executar os testes do projeto, execute o seguinte comando:

```bash
pytest
```

Este comando irá executar todos os testes do projeto e exibir os resultados no terminal.
