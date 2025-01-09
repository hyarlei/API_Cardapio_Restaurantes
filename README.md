# **API de Cardápio de Restaurantes**

Uma API desenvolvida para gerenciar cardápios de restaurantes, clientes e pedidos. Permite a criação, leitura, atualização e exclusão (CRUD) de dados, com armazenamento em banco de dados SQLite e manipulação de arquivos CSV para persistência.

---

## **Índice**

- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Rotas da API](#rotas-da-api)
- [Autores](#autores)

---

## **Funcionalidades**

- Gerenciar **cardápios** (criar, listar, atualizar e excluir pratos).
- Gerenciar **clientes** (adicionar e listar clientes).
- Registrar e listar **pedidos** com cálculo automático do valor total.
- Manipulação de arquivos CSV e compactação para ZIP.
- Persistência de dados em **SQLite**.
- Download e verificação de integridade de arquivos.

---

## **Tecnologias Utilizadas**

- **Python 3.12**: Linguagem principal.
- **FastAPI**: Framework para criação da API.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **SQLite**: Banco de dados para persistência.
- **CSV**: Para armazenar dados relacionados ao cardápio.
- **dotenv**: Para gerenciamento de variáveis de ambiente.

---

## **Instalação**

### Pré-requisitos

Certifique-se de ter instalado:

- **Python 3.10 ou superior**
- **Git**

### Passos para Instalar

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/API_Cardapio_Restaurantes.git
   cd API_Cardapio_Restaurantes
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/MacOS
   .venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o ambiente criando um arquivo `.env` na raiz do projeto:

   ```env
   DATABASE_URL=sqlite:///./database.db
   ```

---

## **Uso**

1. Inicie a aplicação com o Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

2. Acesse a documentação interativa da API:
   - [Swagger UI](http://127.0.0.1:8000/docs)
   - [Redoc](http://127.0.0.1:8000/redoc)

---

## **Estrutura do Projeto**

```
.
├── app
│   ├── data
│   │   ├── menu.csv          # Dados do cardápio
|   |   ├── database.db       # Banco de dados SQLite
│   ├── models
│   │   ├── menu.py           # Modelo de dados do cardápio
│   ├── routes
│   │   ├── menu_routes.py    # Rotas relacionadas ao cardápio
│   ├── services
│   │   ├── csv_service.py    # Serviço de manipulação de arquivos CSV
│   ├── db.py                 # Configuração do banco de dados
│   └── main.py               # Ponto de entrada da aplicação
├── requirements.txt          # Dependências do projeto
├── README.md                 # Documentação do projeto
└── .env                      # Variáveis de ambiente
```

---

## **Rotas da API**

### **Cardápio**

| Método | Endpoint         | Descrição                      |
|--------|------------------|--------------------------------|
| GET    | `/menu`          | Listar todos os itens do cardápio. |
| POST   | `/menu`          | Adicionar um item ao cardápio. |
| PUT    | `/menu/{id}`     | Atualizar um item do cardápio. |
| DELETE | `/menu/{id}`     | Excluir um item do cardápio.   |

### **Clientes**

| Método | Endpoint         | Descrição                      |
|--------|------------------|--------------------------------|
| GET    | `/clientes`      | Listar todos os clientes.      |
| POST   | `/clientes`      | Adicionar um cliente.          |

### **Pedidos**

| Método | Endpoint         | Descrição                      |
|--------|------------------|--------------------------------|
| GET    | `/pedidos`       | Listar todos os pedidos.       |
| POST   | `/pedidos`       | Criar um novo pedido.          |

---

## **Autores**

- **Hyarlei Silva**  
  Desenvolvedor do projeto. Sinta-se à vontade para entrar em contato:
  - [LinkedIn](https://www.linkedin.com/in/hyarlei-silva)
  - [GitHub](https://github.com/hyarlei)
