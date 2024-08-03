# スクリプトの例(実際に実行したわけではない)

set -e  # エラーが起こったらスクリプトの実行を終了させる設定

# データベースとテーブルを作成し、初期データを挿入する
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE mydatabase;
    \c mydatabase;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    INSERT INTO users (name, email) VALUES 
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com');
EOSQL