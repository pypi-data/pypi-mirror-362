# mcp-uuid-gen

UUID生成用のMCPサーバー

このプロジェクトは、UUID（Universally Unique Identifier）を生成するためのMCP（Model Context Protocol）サーバーです。

## 概要

MCPサーバーとして動作し、クライアントアプリケーションからのリクエストに応じてUUIDを生成します。また、コマンドラインツールとしても使用できます。

## 機能

- UUID v4の生成
- MCPプロトコル対応
- コマンドライン実行モード
- シンプルで高速な生成処理

## インストール

```bash
# 依存関係のインストール
uv pip install -e .
```

## 使用方法

### MCPサーバーとして使用

MCPクライアントから本サーバーに接続し、UUID生成リクエストを送信することで新しいUUIDを取得できます。

```bash
python uuid_gen.py
```

### コマンドラインツールとして使用

`--noserver`オプションを使用することで、MCPサーバーを起動せずに直接UUIDを生成できます。

```bash
python uuid_gen.py --noserver
```

出力例：
```
a9e55db6-4c34-4e2e-a3cf-b77d7bdbec03
```

## 必要環境

- Python 3.13以上
- mcp[cli] >= 1.9.4