# sc_cli/main.py ―― Solar Circuit ルート CLI

from __future__ import annotations

import importlib.metadata
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

# finish サブコマンド用 Typer インスタンス
from sc_cli.commands.finish import finish_app

# --------------------------------------------------
# ルート CLI
# --------------------------------------------------
app = typer.Typer()
# Expose a .name attribute for click.testing to pick up
app.name = "sc"
# Alias .main so CliRunner.invoke() finds it
app.main = app.__call__

console = Console()


@app.command("version", help="CLI のバージョンを表示")
def version_cmd():
    """
    CLI のバージョンを表示します。
    """
    ver = importlib.metadata.version("solar-circuit-v2")
    typer.echo(f"Solar Circuit v{ver}")


@app.command("init", help="プロジェクトの雛形を生成します")
def init_cmd():
    """
    プロジェクトの雛形を現在のディレクトリに生成します。
    """
    here = Path(__file__).parent
    template_dir = here / "templates"
    dest = Path.cwd()
    typer.echo(f"✅ テンプレートを {dest} に展開中…")
    shutil.copytree(template_dir, dest, dirs_exist_ok=True)
    typer.secho("完了！", fg=typer.colors.GREEN)


@app.command("new", help="新規 Work-Order を作成します")
def new_cmd(id: str | None = typer.Option(None, "--id", help="カスタム ID を指定")):
    """
    新規 Work-Order を作成します。カスタム ID を指定することもできます。
    """
    wo_dir = Path.cwd() / "work_orders"
    wo_dir.mkdir(exist_ok=True)
    if id:
        filename = f"{id}.md"
    else:
        today = datetime.now().strftime("%Y%m%d")
        seq = len(list(wo_dir.glob(f"WO-{today}-*.md"))) + 1
        filename = f"WO-{today}-{seq:03d}.md"
    (wo_dir / filename).touch()
    typer.echo(f"Work-Order 生成: {filename}")


@app.command("save", help="dev_memory.md に今日の学びを追記します")
def save_cmd():
    """
    dev_memory.md に今日の学びを追記します。
    ファイルが存在しない場合は作成し、日付ヘッダーを追加します。
    """
    # 1) Ensure the .sc/knowledge_base path
    kb_file = Path.cwd() / ".sc" / "knowledge_base" / "dev_memory.md"
    kb_file.parent.mkdir(parents=True, exist_ok=True)
    kb_file.touch(exist_ok=True)

    # 2) Add header if missing
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"\n\n## {today}\n\n"
    text = kb_file.read_text(encoding="utf-8")
    if header not in text:
        kb_file.write_text(text + header, encoding="utf-8")

    # 3) Invoke editor on the correct path
    editor = os.environ.get("EDITOR", "vi")
    subprocess.run([editor, str(kb_file)])

    typer.secho("Saved! 👍", fg=typer.colors.GREEN)


@app.command("status", help="プロジェクトのステータスを表示します")
def status_cmd():
    """
    現在のプロジェクトのステータスを表示します。
    今日の記憶、未完了のWork-Order、添付ファイル/アウトバウンドの情報を表示します。
    """
    # Today's Memory
    console.rule("[bold blue]Today's Memory[/]")
    mem_file = Path.cwd() / "dev_memory.md"
    if mem_file.exists():
        lines = mem_file.read_text(encoding="utf-8").splitlines()
        console.print(
            lines[-1] if lines else "[italic]Memory file is empty.[/]"
        )
    else:
        console.print("[italic]No memory file found.[/]")

    # Open Work Orders
    console.rule("[bold green]Open Work Orders[/]")
    wo_dir = Path.cwd() / "work_orders"
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("WO-ID", style="dim", width=12)
    table.add_column("Title")
    if wo_dir.is_dir():
        for p in sorted(wo_dir.glob("*.md")):
            lines = p.read_text(encoding="utf-8").splitlines()
            title = (
                lines[0].lstrip("# ").strip()
                if lines and lines[0].strip()
                else "(no title)"
            )  # E501 修正
            table.add_row(p.stem, title)
    console.print(table)

    # Attachments / Outbound
    console.rule("[bold yellow]Attachments / Outbound[/]")
    for d in ("attachments", "outbound"):
        dirp = Path.cwd() / d
        if dirp.is_dir():
            files = list(dirp.rglob("*"))
            total = sum(f.stat().st_size for f in files if f.is_file())
            console.print(f"{d}: {len(files)} files, {total/1024:.1f} KB")
        else:
            console.print(f"{d}: [italic]none[/]")


@app.command("attach", help="attachments/ にファイルをコピーします")
def attach_cmd(
    path: Path = typer.Argument(..., exists=True),
    name: str | None = typer.Option(None, "--name", "-n"),
):
    """
    指定されたファイルを 'attachments/' ディレクトリにコピーします。
    任意でコピー後のファイル名を指定できます。
    """
    dest_dir = Path.cwd() / "attachments"
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / (name or path.name)
    shutil.copy(path, dest)
    console.print(f"Attached: {dest}", style="green")


@app.command("outbound", help="outbound/ にファイルをコピーします")
def outbound_cmd(
    path: Path = typer.Argument(..., exists=True),
    name: str | None = typer.Option(None, "--name", "-n"),
):
    """
    指定されたファイルを 'outbound/' ディレクトリにコピーします。
    任意でコピー後のファイル名を指定できます。
    """
    dest_dir = Path.cwd() / "outbound"
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / (name or path.name)
    shutil.copy(path, dest)
    # Use exact "Outbound:" prefix to satisfy test expectations
    typer.echo(f"Outbound: {dest}")


@app.command("list", help="Work-Order 一覧を表示します")
def list_cmd():
    """
    Work-Order の一覧を表示します。
    """
    wo_dir = Path.cwd() / "work_orders"
    # If no MD files, print message and return
    if not wo_dir.is_dir() or not any(wo_dir.glob("*.md")):
        typer.echo("No work orders")
        return
    for p in sorted(wo_dir.glob("*.md")):
        typer.echo(p.stem)


# ==================================================
# finish サブコマンドを登録
# ==================================================
app.add_typer(finish_app, name="finish")


if __name__ == "__main__":
    app()
