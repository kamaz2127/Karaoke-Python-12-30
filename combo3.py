from pygame import *
import sounddevice as sd
import scipy.io.wavfile as wav
import os

# ==========================================
# ТУТ ДІТИ МОЖУТЬ ЗМІНЮВАТИ ДИЗАЙН
# ==========================================
W = 800   # Ширина вікна
H = 600   # Висота вікна
BACKGROUND = (30, 30, 30)      # Колір фону (червоний, зелений, синій)
LINE_COLOR = (0, 255, 0)       # Колір лінії хвилі
BTN_COLOR  = (255, 255, 0)     # Колір кнопки
TEXT_COLOR = (0, 0, 0)         # Колір тексту на кнопці
MINUS_TRACK = "mic-wave-pygame/MinusDuHast.mp3" # Назва файлу з мінусовкою
# ==========================================

# Технічні налаштування (краще не чіпати)
fs = 44100
chunk = 1024 
vis_data = [0.0] * chunk 
recording = None
is_recording = False

init()
mixer.init()
mixer.music.set_volume(0.5)

window = display.set_mode((W, H))
display.set_caption("My Karaoke")
timer = time.Clock()

# Шрифти
font.init()
my_font = font.SysFont('Arial', 40) # МОЖНА МІНЯТИ РОЗМІР ШРИФТУ (40)

# Створення кнопки (X, Y, Ширина, Висота)
btn_rect = Rect(W // 2 - 100, H - 100, 200, 60) 

# Функція, яка постійно слухає мікрофон для малювання лінії
def audio_callback(indata, frames, time, status):
    global vis_data
    vis_data = indata[:, 0]

# Запускаємо "слухача" мікрофона
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs)
stream.start()

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        if e.type == MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(e.pos):
                if not is_recording:
                    # --- ПОЧАТОК ЗАПИСУ ---
                    is_recording = True
                    # Запис 10 секунд (можна змінити число 10)
                    recording = sd.rec(int(fs * 10), samplerate=fs, channels=1)
                    mixer.music.load(MINUS_TRACK)
                    mixer.music.play()
                else:
                    # --- КІНЕЦЬ ЗАПИСУ ---
                    is_recording = False
                    sd.stop()
                    wav.write("voice_record.wav", fs, recording) # Зберегли
                    
                    # Відтворення результату
                    mixer.music.stop()
                    mixer.music.play()
                    if os.path.exists("voice_record.wav"):
                        voice = mixer.Sound("voice_record.wav")
                        voice.play()

    # 1. Малюємо фон
    window.fill(BACKGROUND) 

    # 2. Малюємо хвилю (візуалізація)
    points = []
    for i, value in enumerate(vis_data):
        x = int(i * W / chunk)          # <--- Додали int()
        y = int(H / 2 + value * 500)    # <--- Додали int()
        points.append((x, y))
    
    if len(points) > 1:
        draw.lines(window, LINE_COLOR, False, points, 2)

    # 3. Малюємо кнопку і текст
    if is_recording:
        draw.rect(window, (255, 0, 0), btn_rect) # Червона кнопка, коли йде запис
        text = my_font.render("СТОП", True, TEXT_COLOR)
    else:
        draw.rect(window, BTN_COLOR, btn_rect)   # Звичайна кнопка
        text = my_font.render("ЗАПИС", True, TEXT_COLOR)
    
    # Центруємо текст на кнопці
    window.blit(text, (btn_rect.x + 40, btn_rect.y + 10))

    display.update()
    timer.tick(60)

stream.stop()
quit()