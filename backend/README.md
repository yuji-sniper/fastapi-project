## ディレクトリ構成
```bash
fastapi_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI アプリケーションインスタンスとルートルーターの設定
│   ├── dependencies.py        # 依存関係の定義
│   │
│   ├── models/                # データモデル (ORM モデル)
│   │
│   ├── schemas/               # リクエストとレスポンスモデル (Pydantic モデル)
│   │
│   ├── db/                    # データベース接続とセッションの設定
│   │
│   ├── repository/            # リポジトリ層 - データソースとのやり取りを担当
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── item_repository.py
│   │
│   ├── services/              # サービス層 - ビジネスロジックの実装
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   │
│   ├── usecases/              # ユースケース層 - アプリケーションのユースケースを管理
│   │   ├── __init__.py
│   │   ├── user_usecase.py
│   │   └── item_usecase.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── v1/                # バージョン1のAPIエンドポイント
│       │   ├── __init__.py
│       │   ├── router.py
│       │   └── endpoints/
│       │       ├── __init__.py
│       │       ├── users.py
│       │       └── items.py
│       │
│       └── v2/                # バージョン2のAPIエンドポイント
│           ├── __init__.py
│           ├── router.py
│           └── endpoints/
│               ├── __init__.py
│               ├── users.py
│               └── items.py
│
├── database/                  # データベース設定
│   ├── migrations/            # Alembic マイグレーションディレクト
│
└── tests/                     # テスト

```
