@echo off
python -m pip install --upgrade pyinstaller
pyinstaller --onefile --windowed --name FlappyBird flappy_bird.py
echo EXE olusturuldu: dist\FlappyBird.exe
pause
