# FastAPI todo-api

## todo機能
GET /todos : Todoリストの一覧を表示  
GET /todos/{id} : 指定したIDのTodoを取得  
POST /todos : 新規Todoを作成  
PATCH /todos/{id} : Todoの内容を修正  
DELETE /todos/{id} : Todoを削除

## ユーザー認証
POST /auth/signin : 新規ユーザーの登録  
POST /auth/login : トークン方式のログイン

## その他
GET / : Hello, World!  
GET /docs : SwaggerUIのドキュメント  
GET /redoc : ドキュメント
