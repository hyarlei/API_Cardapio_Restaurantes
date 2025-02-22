# **API de Cardápio de Restaurantes**

Uma API desenvolvida para gerenciar cardápios de restaurantes, clientes e pedidos. Permite a criação, leitura, atualização e exclusão (CRUD) de dados, com armazenamento em banco de dados MongoDB e manipulação de dados usando Beanie ODM.

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

- Gerenciar **menu** (criar, listar, atualizar e excluir pratos).
- Gerenciar **clientes** (adicionar e listar clientes, excluir).
- Registrar e listar **pedidos** com cálculo automático do valor total.
- Persistência de dados em **SQLite**.

---

## **Tecnologias Utilizadas**

- **Python 3.12**: Linguagem principal.
- **FastAPI**: Framework para criação da API.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **SQLite**: Banco de dados para persistência.
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
   MONGO_URI=sua_uri_do_mongodb
   DB_NAME=API_Cardapio_Restaurante
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
│   ├── models
│   │   ├── modelagem.py       # Modelos de dados (Cliente, Menu, Pedido)
│   ├── routes
│   │   ├── menu_routes.py     # Rotas relacionadas ao menu
│   │   ├── pedido_routes.py   # Rotas relacionadas ao pedido
│   │   ├── cliente_routes.py  # Rotas relacionadas ao cliente
│   ├── services
│   │   ├── menu_service.py    # Serviço de manipulação do menu
│   │   ├── pedido_service.py  # Serviço de manipulação de pedidos
│   │   ├── cliente_service.py # Serviço de manipulação de clientes
│   ├── db.py                  # Configuração do banco de dados
│   └── main.py                # Ponto de entrada da aplicação
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação do projeto
└── .env                       # Variáveis de ambiente
```

---

## **Rotas da API**

### **Menu**

| Método | Endpoint         | Descrição                      |
|--------|------------------|--------------------------------|
| GET    | `/menu`          | Listar todos os itens do cardápio. |
| POST   | `/menu`          | Adicionar um item ao cardápio. |
| PUT    | `/menu/{id}`     | Atualizar um item do cardápio. |
| DELETE | `/menu/{id}`     | Excluir um item do cardápio.   |

### **Clientes**


| Método | Endpoint         | Descrição                      |
|--------|------------------|--------------------------------|
| GET    | `/cliente`          | Listar todos os itens do cardápio. |
| POST   | `/cliente`          | Adicionar um item ao cardápio. |
| PUT    | `/cliente/{id}`     | Atualizar um item do cardápio. |
| DELETE | `/cliente/{id}`     | Excluir um item do cardápio.   |

### **Pedidos**

| Método | Endpoint         | Descrição                      |
|--------|------------------|--------------------------------|
| GET    | `/pedido`          | Listar todos os itens do cardápio. |
| POST   | `/pedido`          | Adicionar um item ao cardápio. |
| PUT    | `/pedido/{id}`     | Atualizar um item do cardápio. |
| DELETE | `/pedido/{id}`     | Excluir um item do cardápio.   |

---

## **Requisições**

Criação de pedido:

```
{
  "cliente_id": "id",
  "itens_ids": ["id", "id"],
  "status": "pendente"
}
```

## **Autores**

- **Hyarlei Silva**  
  Desenvolvedor do projeto. Sinta-se à vontade para entrar em contato:
  - [LinkedIn](https://www.linkedin.com/in/hyarlei-silva)
  - [GitHub](https://github.com/hyarlei)
