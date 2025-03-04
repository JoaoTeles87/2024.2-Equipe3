# 🚀 Guia de Integração do Frontend

Este guia explica como configurar, estruturar e integrar o frontend do projeto React com o backend Flask.

---

# ESS Front-end React

This is the Front-end base project in React for the Software and Systems Engineering discipline, offered by the Informatics Center (CIn) of the Federal University of Pernambuco (UFPE).

## Table of Contents

1. [Getting Started](##getting-started)
2. [Running the tests](#running-the-tests)
3. [Scripts](#scripts)
4. [Dependencies](#dependencies)
5. [Architecture](#architecture)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run this project, you'll need to have the following software installed on your system:

- Node.js
- npm (Node Package Manager)

### Installing

Clone the repository and install the dependencies by running the following command in the project directory:

```
npm install
```

### First time running ?

Run the follow scripts

```
chmod +x .husky/pre-commit
chmod +x .husky/pre-push
```

```
npm run
```

### Environment

This project uses `.env` files to manage environment variables. You can create a `.env.development` file in the project directory and set the environment variables in the file (iou can create it from .`env.example`). The `env` script in the `package.json` file uses the `env-cmd` package to load the environment variables from the `.env.development` file.

Crie um arquivo .env na raiz do frontend e adicione a URL da API:
```
VITE_API_URL=http://127.0.0.1:5000
```

── 📂 src/ → Código-fonte do projeto
│ ├── 📂 app/ → Páginas principais (leva a estilização das telas)
│ │ ├── home/pages/Login.tsx → Tela de Login
│ │ ├── home/pages/Cadastro.tsx → Tela de Cadastro
│ │ ├── home/pages/Reservas.tsx → Tela após login
│ │
│ ├── 📂 shared/services/ → Serviços de integração com a API
│ │ ├── autorizacao.tsx → Requisições de login/cadastro
│ │
│ ├── App.tsx → Arquivo principal do React onde você adiciona suas rotas criadas nas pages!
│ ├── main.tsx → Ponto de entrada da aplicação
│
├── .env → Configuração da API
├── package.json → Lista de dependências
├── README.md → Você está aqui! 📌
### Running the App

To start the app, run the following command:

```
npm run dev
```

This command will run the React app in development with Vite.js script



## Rodando  o backend Flask

No powerShell mude para o diretório backend
```
cd backend
```
Crie arquivos __init__.py em todos diretórios dentro de backend, inclusive nele.

backend/
   __init__.py
   main.py
   testes/
      __init__.py
      teste_exemplo.py

MacOS
Dentro da pasta backend no terminal, execute os seguintes comandos:

```
export PYTHONPATH=$(pwd)/backend
export FLASK_APP=main
flask run
```

Dentro da pasta backend/testes, execute:

```
export PYTHONPATH=$(pwd)/backend
pytest
Windows (Powershell)
```
Dentro da pasta backend no PowerShell, execute os seguintes comandos:

```
$env:PYTHONPATH = "$(pwd)/backend"
$env:FLASK_APP = "main"
flask run
```


Crie a venv
```
python -m venv venv
```
Ative a venv
```
venv\Scripts\activate
```
e agora você deve instalar todas as dependencias do projeto 

```
pip install -r requirements.txt
```

obs: caso sejam necessárias novas bibliotecas e deseja atualizar o requirements.txt por favor recirar arquivo.
```
pip freeze > requirements.txt
```

Rodando servidor Flask localmente na rota 5000.
```
python main.py
```


## Running the tests

There are two types of tests configured in the base project: unit tests using Vitest with React Testing Library and E2E acceptance tests using Cypress with Cucumber. It's interesting to create the **.env.testing** at the root of the project the same way it was created to run in development, changing the necessary values.

To run unit tests

```
npm run test
```

To run E2E tests in **interactive mode**

```
npm run cy:e2e-interactive
```

To run E2E tests in **headless mode**

```
npm run cy:e2e-headless
```

**Note:** To run E2E tests that test flows that involve connecting to the back-end, such as login, the back-end must be running. Remember to provide a valid URL for the backend in the **.env.testing** file.

## Scripts

The following scripts are available in the `package.json` file:

- `dev`: Runs the app in development mode.
- `build`: Compiles the TypeScript code.
- `test`: Runs the Vitest tests for the project.
- `prettier`: Formats the code using Prettier.
- `lint`: Lints the code using ESLint.

## Dependencies

The following dependencies are used in the project:

- [vite](https://github.com/microsoft/TypeScript): Vite is a new breed of frontend build tooling that significantly improves the frontend development experience.
- [react](https://github.com/facebook/react): React is a JavaScript library for building user interfaces.
- [react-router-dom](https://github.com/remix-run/react-router): React Router is a lightweight, fully-featured routing library for the React JavaScript library.
- [react-hook-form](https://github.com/react-hook-form/react-hook-form): React Hook Form is a library for React that simplifies form validation and input data handling.
- [zod](https://github.com/colinhacks/zod): Zod is a TypeScript-first schema declaration and validation library. I'm using the term "schema" to broadly refer to any data type, from a simple string to a complex nested object.

## Architecture

To understand and learn more details about the structure of the project, click [here](./docs/architecture-pattern.md) to be redirected to the README that contains this information.
