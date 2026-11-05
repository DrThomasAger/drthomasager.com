@echo off
rem Fetch every PDF, tape and radio recording, scan, photograph, video and transcript the archive lists.
rem Run it again at any time; it continues where it stopped. Files land in teachers\<teacher>\downloads\, outside git.
cd /d "%~dp0"
python -m pip install --upgrade internetarchive yt-dlp requests pypdf
for /d %%T in (teachers\*) do (
  if exist "%%T\fetch.py" if not "%%~nxT"=="_template" (
    echo === %%~nxT
    pushd "%%T"
    python fetch.py
    python extract-text.py
    python find-quotes.py
    popd
  )
)
python coverage.py
echo Done. holdings.json in each teacher folder records what is held; COVERAGE.md counts it.
pause
