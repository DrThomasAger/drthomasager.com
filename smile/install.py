"""Install the /C-guru commands everywhere a command reaches.

    python hanjopurebuddha.com/smile/install.py

1. Writes every smile/commands/C-guru*.md into ~/.claude/commands, with the
   path of this folder written in, so Claude Code in every project has them.
   THE MAP Viewer's composer lists every C- command there, so they appear in
   its module list at its next /modules call.
2. Rebuilds Pi's prompt templates from the Claude commands, the way Pi
   Integration does, when Pi Integration and babashka are on this machine.
3. Writes the same commands into this repository's .claude/commands with a
   path relative to the repository, for any session working here.

It changes nothing else and prints each file it writes. Run it again after
the commands change.
"""
import os
import pathlib
import shutil
import subprocess

HERE = pathlib.Path(__file__).resolve().parent          # .../hanjopurebuddha.com/smile
SITE = HERE.parent                                       # .../hanjopurebuddha.com
REPO = SITE.parent if (SITE.parent / "build.py").exists() else SITE
HOME = pathlib.Path.home()


def write(dest_dir, guru_home):
    dest_dir.mkdir(parents=True, exist_ok=True)
    for f in sorted((HERE / "commands").glob("C-guru*.md")):
        text = f.read_text(encoding="utf-8").replace("__GURU_HOME__", guru_home)
        (dest_dir / f.name).write_text(text, encoding="utf-8")
        print(f"wrote {dest_dir / f.name}")


def main():
    write(HOME / ".claude" / "commands", str(SITE).replace("\\", "/"))
    rel = os.path.relpath(SITE, REPO).replace("\\", "/")
    write(REPO / ".claude" / "commands", rel if rel != "." else ".")
    smile_home = os.environ.get("SMILE_HOME") or str(HOME / "Claude" / "Projects" / "Smile")
    pi = pathlib.Path(smile_home).parent / "Pi Integration" / "bb.edn"
    if pi.exists() and shutil.which("bb"):
        r = subprocess.run(["bb", "--config", str(pi), "-m", "pi-integration.compose"], capture_output=True, text=True)
        print("Pi prompt templates rebuilt" if r.returncode == 0 else f"Pi Integration said: {r.stderr.strip()[:400]}")
    else:
        print("Pi Integration or bb not found here; Pi picks the commands up at its next rebuild of ~/.pi/agent/prompts")


if __name__ == "__main__":
    main()
