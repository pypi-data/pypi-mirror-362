# tests/test_changelog.py

import os
from pathlib import Path

from sc_cli.utils.changelog import ChangelogUpdater


def test_changelog_append(tmp_path):
    # テスト用ディレクトリに移動
    os.chdir(tmp_path)
    # ファイルパスを上書き
    ChangelogUpdater.FILE = tmp_path / "CHANGELOG.md"

    # 初回追記
    ChangelogUpdater.update(
        "0.1.2.dev1", {"added": ["機能Xを追加"], "fixed": ["バグYを修正"]}
    )

    content = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert "0.1.2.dev1" in content
    assert "- 機能Xを追加" in content
    assert "- バグYを修正" in content

    # 2回目追記（内容が累積されること）
    ChangelogUpdater.update("0.1.3.dev1", {"added": [], "fixed": []})
    content2 = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert "0.1.3.dev1" in content2
    assert content2.count("## [") == 2
