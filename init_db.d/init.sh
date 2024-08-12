# スクリプト

set -e  # エラーが起こったらスクリプトの実行を終了させる設定

# データベースを作成
psql -U "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE "$POSTGRES_DB";
EOSQL