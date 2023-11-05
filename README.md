## 初回環境構築
```
$ make init
```

## Dev Containers起動
DockerコンテナとVSCodeの統合を行います。<br>
これによってDockerコンテナ内のファイルに対してVSCodeからアクセスできます。

- `Cmd/Ctrl + Shift + P`でコマンドパレットを開き、`Dev-Containers: Open Folder in Container`を選択。
- プロジェクトフォルダ`fastapi-project`を選択（compose.ymlファイルがあるフォルダ）。

## Dev Containers終了・再開
### 終了
```
$ make down
```
### 再開
VSCode左下の`開発コンテナー`をクリックし、`ウィンドウの再読み込み`を選択。

## マイグレーション
### マイグレーションファイル生成
```
$ make app
$ poetry run alembic revision --autogenerate -m "create hoge table"
```

app/database/migrations/versionsにマイグレーションファイルが生成される。

### マイグレーション実行
```
$ make migrate
```

## ディレクトリ構成
### バックエンド
```bash
fastapi_project/
│
├── app/
│   ├── main.py                          # FastAPI アプリケーションインスタンスとルートルーターの設定
│   │
│   ├── middleware/                      # ミドルウェア
│   │
│   ├── dependencies/                    # 依存関係の定義
│   │
│   ├── db/                              # データベース接続とセッションの設定
│   │
│   ├── models/                          # データモデル (ORM モデル)
│   │
│   ├── schemas/                         # リクエストとレスポンスモデル (Pydantic モデル)
│   │
│   ├── repository/                      # リポジトリ層 - データソースとのやり取りを担当
│   │
│   ├── services/                        # サービス層 - ビジネスロジックの実装
│   │
│   ├── usecases/                        # ユースケース層 - アプリケーションのユースケースを管理
│   │
│   └── api/                             # APIエンドポイントの定義
│       ├── v1/                          # バージョン1のAPIエンドポイント
│       │   ├── router.py
│       │   └── endpoints/              # v1エンドポイントの具体的な定義
│       │
│       └── v2/                          # バージョン2のAPIエンドポイント
│           ├── router.py
│           └── endpoints/              # v2エンドポイントの具体的な定義
│
├── migrations/                          # Alembic マイグレーションディレクトリ
│
└── tests/                               # テストディレクトリ
```
