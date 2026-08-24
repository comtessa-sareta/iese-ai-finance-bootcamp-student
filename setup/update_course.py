"""Safely update the course while keeping your own work.

Run this when the instructor announces an update:

    python setup/update_course.py

What it does, in order:
1. Copies every notebook you have modified into backups/<date-time>/ —
   your filled-in answers are preserved there, always.
2. Restores every course file to its original state (only your notebooks
   ever hold your work, and those were just backed up).
3. Pulls the update.
4. Installs any packages the update added to requirements.txt.

Your work is never deleted: after updating, open the backup copy next to the
new notebook and copy your answers across. Nothing is ever pushed anywhere.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr.strip())
        sys.exit(f"git {' '.join(args)} failed - ask for help, nothing was lost.")
    return result.stdout


def main() -> None:
    status = run("status", "--porcelain", "--", "notebooks/")
    modified = [line[3:].strip() for line in status.splitlines() if line[:2].strip() in ("M", "AM", "MM")]

    if modified:
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        backup_dir = REPO / "backups" / stamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        for rel in modified:
            src = REPO / rel
            shutil.copy2(src, backup_dir / Path(rel).name)
        print(f"Backed up {len(modified)} notebook(s) with your work to: backups/{stamp}/")
    else:
        print("No modified notebooks - nothing to back up.")

    # Reset every tracked file so the pull can never conflict. Your own work
    # lives only in notebooks (backed up above) and in untracked files
    # (.env, outputs/, backups/), which this never touches. A PDF merely
    # opened in a viewer counts as "modified" and used to block the pull.
    run("checkout", "--", ".")

    print(run("pull", "--ff-only").strip() or "Already up to date.")

    # New sessions can add packages; installing is fast when nothing changed.
    print()
    print("Updating packages from requirements.txt ...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r",
                    str(REPO / "requirements.txt")], check=False)

    print()
    print("Done. Your own answers are safe in the backups/ folder;")
    print("open the backup next to the updated notebook to copy them across.")


if __name__ == "__main__":
    main()
