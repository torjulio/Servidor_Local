from app import db

# Adicionar a coluna 'upload_time' à tabela 'file'
with db.engine.connect() as connection:
    connection.execute('ALTER TABLE file ADD COLUMN upload_time DATETIME')
    print("Coluna 'upload_time' adicionada com sucesso.")
