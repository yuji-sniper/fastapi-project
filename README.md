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
│   ├── __init__.py
│   ├── main.py                # FastAPI アプリケーションインスタンスとルートルーターの設定
│   ├── dependencies/        # 依存関係の定義
│   │
│   ├── models/                # データモデル (ORM モデル)
│   │
│   ├── schemas/               # リクエストとレスポンスモデル (Pydantic モデル)
│   │
│   ├── db/                    # データベース接続とセッションの設定
│   │
│   ├── repository/            # リポジトリ層 - データソースとのやり取りを担当
│   │
│   ├── services/              # サービス層 - ビジネスロジックの実装
│   │
│   ├── usecases/              # ユースケース層 - アプリケーションのユースケースを管理
│   │
│   └── api/
│       ├── __init__.py
│       ├── v1/                # バージョン1のAPIエンドポイント
│       │   ├── __init__.py
│       │   ├── router.py
│       │   └── endpoints/
│       │
│       └── v2/                # バージョン2のAPIエンドポイント
│           ├── __init__.py
│           ├── router.py
│           └── endpoints/
│
├── migrations/                  # Alembic マイグレーションディレクトリ
│
└── tests/                     # テスト

```
