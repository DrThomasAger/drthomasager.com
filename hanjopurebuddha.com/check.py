"""Run merge (if a scratch folder is given), integrity and build for every teacher.

    python3 check.py [scratch-folder-for-<slug>=path ...]
"""
import pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
scratch = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
for t in sorted(p for p in (ROOT / "teachers").iterdir() if p.is_dir() and not p.name.startswith("_")):
    if t.name in scratch and (t / "merge.py").exists():
        subprocess.run([sys.executable, str(t / "merge.py"), scratch[t.name]], check=True)
    if (t / "integrity.py").exists():
        subprocess.run([sys.executable, str(t / "integrity.py")], check=True, stdout=subprocess.DEVNULL)
        print(f"{t.name}: integrity-report.md written")
subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)
