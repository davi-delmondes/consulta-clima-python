# Consulta de Clima com WeatherAPI

Aplicação de terminal desenvolvida em Python para consultar o clima atual de uma cidade usando a WeatherAPI.

## Sobre o projeto

Este projeto permite que o usuário digite o nome de uma cidade e receba informações climáticas em tempo real, como temperatura, sensação térmica, umidade, vento, pressão atmosférica, visibilidade e horário da última atualização.

O objetivo do projeto foi praticar consumo de API, organização de código, tratamento de erros e uso de variáveis de ambiente com arquivo `.env`.

## Funcionalidades

* Consulta do clima atual de uma cidade
* Exibição de dados de localização
* Exibição de temperatura e sensação térmica
* Exibição de informações sobre vento e ambiente
* Tratamento de erros da WeatherAPI
* Validação para cidade vazia
* Configuração segura da API Key usando `.env`
* Menu interativo no terminal

## Tecnologias utilizadas

* Python
* Requests
* Python-dotenv
* WeatherAPI

## Estrutura do projeto

```
consulta-clima-python/
├── consultar_clima.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Como usar

### 1. Clone o repositório

```
git clone https://github.com/davi-delmondes/consulta-clima-python.git
```

### 2. Acesse a pasta do projeto

```
cd consulta-clima-python
```

### 3. Instale as dependências

```
pip install -r requirements.txt
```

### 4. Crie uma conta na WeatherAPI

Acesse o site da WeatherAPI, crie uma conta e gere sua própria API Key.

### 5. Crie o arquivo `.env`

Na pasta principal do projeto, crie um arquivo chamado `.env`.

Dentro dele, adicione sua chave da API:

```
API_KEY=sua_chave_aqui
```

Exemplo:

```
API_KEY=123456789abcdef
```

### 6. Execute o programa

```
python consultar_clima.py
```

## Exemplo de uso

Ao executar o programa, será exibido um menu no terminal:

```
╔════════════════════════════════════════════╗
║             CONSULTA DE CLIMA              ║
║    WeatherAPI - Dados em tempo real        ║
╠════════════════════════════════════════════╣
║ [1] Consultar clima                        ║
║ [0] Sair                                   ║
╚════════════════════════════════════════════╝
```

Depois, basta escolher a opção de consulta e digitar o nome de uma cidade para visualizar os dados climáticos atuais.

## Segurança

O arquivo `.env` não deve ser enviado para o GitHub, pois contém a chave privada da API.

Por isso, este projeto possui um arquivo `.env.example`, que serve apenas como modelo para outros usuários configurarem suas próprias chaves.

Cada pessoa que baixar este projeto deve usar sua própria API Key da WeatherAPI.

## Aprendizados

Durante o desenvolvimento deste projeto, foram praticados:

* Consumo de API com Python
* Uso da biblioteca `requests`
* Uso da biblioteca `python-dotenv`
* Uso de variáveis de ambiente
* Organização de código em funções
* Tratamento de erros
* Validação de entrada do usuário
* Criação de menu no terminal
* Boas práticas para publicar projetos no GitHub

## Autor

Desenvolvido por Davi de Carvalho Delmondes.
