"""
sc_cli パッケージ初期化モジュール

ここではバージョンだけを公開し、Typer アプリの生成や
finish サブコマンドの登録は sc_cli/main.py に一元化します。
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("solar-circuit")
except PackageNotFoundError:
    __version__ = "0.0.0"
