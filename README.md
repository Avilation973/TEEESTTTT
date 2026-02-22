# Flappy Bird (Python / Tkinter)

Basit bir Flappy Bird klonu.

## Çalıştırma

```bash
python3 flappy_bird.py
```

## EXE alma (Windows)

1. PyInstaller kur:

```bash
pip install pyinstaller
```

2. EXE üret:

```bash
pyinstaller --onefile --windowed --name FlappyBird flappy_bird.py
```

Çıktı dosyası `dist/FlappyBird.exe` olur.

## Kontroller

- **Space** veya **sol tık**: zıpla
- Oyun bitince **Space**: yeniden başlat
