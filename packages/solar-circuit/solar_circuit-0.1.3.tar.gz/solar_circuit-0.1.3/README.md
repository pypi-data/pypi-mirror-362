# solar-circuit-v2

[![CI](https://github.com/seishinshigo/solar_circuit_v2/actions/workflows/ci.yml/badge.svg)](https://github.com/seishinshigo/solar_circuit_v2/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/seishinshigo/solar_circuit_v2/branch/main/graph/badge.svg)](https://codecov.io/gh/seishinshigo/solar_circuit_v2)
[![Coverage](https://codecov.io/gh/あなたのユーザー名/solar_circuit_v2/branch/main/graph/badge.svg)](https://codecov.io/gh/あなたのユーザー名/solar_circuit_v2)
[![PyPI version](https://badge.fury.io/py/solar-circuit.svg)](https://pypi.org/project/solar-circuit/)
[![License](https://img.shields.io/github/license/seishinshigo/solar_circuit_v2)](LICENSE)

> “Markdown 1 枚 × 最小コマンド” で AI 主導開発を完遂する CLI ワークフロー
> Python 3.12｜Typer｜GitHub Actions｜pytest＋coverage｜OS Keyring

---

## 🎯 目的・ゴール

* **ソロ開発者向け** に、Markdown＋CLI だけで日々の開発ワークフローを完結
* **MVP**：`init` → `new` → `save` → `finish` の 4 コマンドで基本サイクルを実現
* **拡張ロードマップ** に基づき、今後もコマンドを追加予定

---

## 🚀 特徴

* **シンプルなプロジェクト初期化**：`sc init` でテンプレート一式を展開
* **Work Order 自動管理**：`sc new` で作業票を自動採番＆Markdown生成
* **開発メモ追記**：`sc save` で日付ヘッダー付きに統一ファイルへ記録
* **ステータス可視化**：`sc status` でメモ／未完了 WO／添付・出力ファイルを一覧
* **作業指示書一覧**：`sc list` で既存 WO をテーブル表示
* **ファイル添付**：`sc attach` で資料や成果物を attachments/outbound に整理
* **CLI 完結**：Gemini API 鍵は OS Keyring に安全保存
* **テストカバレッジ**：pytest＋coverage ≥80%
* **CI**：GitHub Actions で lint／pytest／coverage／（将来的に markdownlint）自動チェック

---

## 📦 インストール

```bash
# Python 3.12 を用意
git clone https://github.com/seishinshigo/solar_circuit_v2.git
cd solar_circuit_v2
python -m venv .venv
source .venv/bin/activate

# 本体インストール
pip install -e .

# 開発用（テスト・lint）を整える場合
pip install -e .[dev]
```

---

## 📸 コマンドリファレンス（実行例）

Solar Circuit CLI の各コマンド操作を VSCode ターミナル上で実行した様子
（`new` → `save` → 不正 → 対象ファイル無し → `list` など、一連の典型的操作のデモ）

![スクリーンショット](docs/images/ss800_01.png)

---

### `sc init`

```bash
sc init
```

プロジェクトの雛形をカレントディレクトリにコピーします。
`.sc/`, `work_orders/`, `attachments/`, `outbound/` などを生成。

---

### `sc new [--id <ID>]`

```bash
sc new
sc new --id WO-20250713-005
```

新しい Work Order を作成します。
ID は自動または手動で指定可能。

---

### `sc save`

```bash
sc save
```

`dev_memory.md` に今日のメモを追記します。エディタが立ち上がり、編集内容が保存されます。

---

### `sc attach [--name <NAME>] <ファイルパス>`

```bash
sc attach report.pdf
sc attach --name summary.docx path/to/file.docx
```

ファイルを `attachments/` にコピーします。

---

### `sc outbound [--name <NAME>] <ファイルパス>`

```bash
sc outbound data.csv
```

ファイルを `outbound/` ディレクトリにコピーします。

---

### `sc status`

```bash
sc status
```

以下の情報を一覧表示します：

* Today’s Memory（最新メモ）
* Open Work Orders
* Attachments / Outbound のファイル数と容量

---

### `sc list [--open] [--closed]`

```bash
sc list
sc list --open
sc list --closed
```

作業指示書（WO）をテーブル形式で一覧表示します。オプションで絞り込み可能。

---

### `sc version`

```bash
sc version
# → solar-circuit-v2 version 0.1.x
```

CLI のバージョンを表示します。

---

### `sc help`

```bash
sc help
sc <command> --help
```

各コマンドのヘルプを表示します。

---

## ✅ Quickstart

```bash
pip install solar-circuit-v2
mkdir my-solar-project
cd my-solar-project
sc init
sc new
sc save
sc status
sc list
```

---

This project is licensed under the MIT License.
