import argparse
import sys
from pathlib import Path

import yaml

from .rules import check_unpinned_actions


def scan(repo):
    findings = []
    for f in sorted(Path(repo).glob(".github/workflows/*.y*ml")):
        workflow = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        findings += check_unpinned_actions(str(f), workflow)
    return findings


def main():
    parser = argparse.ArgumentParser(
        prog="ghaudit",
        description="Audit keamanan workflow GitHub Actions",
    )
    parser.add_argument("path", nargs="?", default=".", help="path ke repo")
    args = parser.parse_args()

    findings = scan(args.path)
    for x in findings:
        print(f"[{x.severity}] {x.rule} - {x.file}\n    {x.message}")
    print(f"\n{len(findings)} temuan")
    sys.exit(1 if findings else 0)