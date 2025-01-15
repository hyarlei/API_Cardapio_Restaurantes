from app.db import init_db

def main():
    init_db()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    main()