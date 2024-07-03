# APIの設計
## Todo-APIのエンドポイント
- GET /api/todos (全てのタスクを取得)
- GET /api/todos/done (完了したタスクのみを取得)
- GET /api/todos/undone (未完了のタスクのみを取得)
- POST /api/todos/ (タスクの新規作成)
- PUT /api/todos/{id} (タスクの内容を編集)
- DELETE /api/todos/{id} (タスクを削除)

## ユーザ認証のエンドポイント
セッションベースの認証ではなく、JWTベースの認証なのでログアウト用のエンドポイントは不要
- POST /api/auth/signup (ユーザ情報の新規登録)
- POST /api/auth/login (ユーザログイン)
- DELETE /api/auth/delete (ユーザ情報の削除)