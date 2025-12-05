from pygame import *
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import numpy as np 

# ==========================================
# НАЛАШТУВАННЯ (Змінюй тут інтерфейс)
# ==========================================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (20, 20, 40)  # Темно-синій фон (R, G, B)
LINE_COLOR = (0, 255, 255)       # Блакитна хвиля
LINE_THICKNESS = 3               # Товщина лінії
BUTTON_COLOR_OFF = (50, 200, 50) # Зелена кнопка
BUTTON_COLOR_ON = (200, 50, 50)  # Червона кнопка (коли запис)
TEXT_COLOR = (255, 255, 255)     # Білий текст

# Назва твого файлу з музикою (має лежати поруч!)
MINUS_TRACK = "mic-wave-pygame/MinusDuHast.mp3"
# ==========================================

# Технічні змінні
fs = 44100
chunk = 1024 
recording = None
is_recording = False
voice_file = "voice_record.wav"
vis_data = [0.0] * chunk # Дані для хвилі

# Ініціалізація
init()
mixer.init()
mixer.music.set_volume(0.5)

screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("My Karaoke Project")
clock = time.Clock()

font.init()
# Можна змінити шрифт, наприклад "Comic Sans MS" або "Impact"
font_big = font.SysFont("Arial", 30, bold=True) 

# Кнопка по центру знизу
btn_rect = Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 120, 300, 60)
current_btn_color = BUTTON_COLOR_OFF
btn_text = "ЗАПИС"

# === ЛОГІКА ===

def audio_callback(indata, frames, time_info, status):
    global vis_data
    if status: print(status)
    vis_data = indata[:, 0]

def start_voice_record():
    global recording
    # Запис 10 секунд (можна змінити цифру 10)
    recording = sd.rec(int(fs * 10), samplerate=fs, channels=1, dtype='int16')

def stop_voice_record():
    global recording
    sd.stop()
    if recording is not None:
        wav.write(voice_file, fs, recording)
        return True
    return False

def play_song_and_voice_together():
    if os.path.exists(voice_file):
        # Перезавантажуємо мінус, щоб грало з початку
        mixer.music.load(MINUS_TRACK)
        mixer.music.play()
        
        voice_sound = mixer.Sound(voice_file)
        voice_sound.play()

# Запуск візуалізації
stream = sd.InputStream(
    callback=audio_callback, channels=1, samplerate=fs, 
    blocksize=chunk, dtype='float32'
)
stream.start()

# === ГОЛОВНИЙ ЦИКЛ ===
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        if e.type == MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(e.pos):
                if not is_recording:
                    # ПОЧАТОК ЗАПИСУ
                    current_btn_color = BUTTON_COLOR_ON
                    btn_text = "СТОП І СЛУХАТИ"
                    is_recording = True
                    
                    mixer.music.load(MINUS_TRACK)
                    mixer.music.play()
                    start_voice_record()
                else:
                    # КІНЕЦЬ ЗАПИСУ
                    current_btn_color = BUTTON_COLOR_OFF
                    btn_text = "ЗАПИС"
                    is_recording = False
                    
                    mixer.music.stop()
                    if stop_voice_record():
                        play_song_and_voice_together()

    # 1. Заливка фону
    screen.fill(BACKGROUND_COLOR)
    
    # (Опціонально) Якщо хочеш картинку на фон, розкоментуй рядки нижче:
    # bg_image = image.load('background.jpg') 
    # bg_image = transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    # screen.blit(bg_image, (0, 0))

    # 2. Малювання хвилі
    points = []
    for i, sample in enumerate(vis_data):
        x = int(i * WINDOW_WIDTH / chunk)
        # 300 - це масштаб висоти хвилі
        y = int(WINDOW_HEIGHT / 2 + sample * 300) 
        points.append((x, y))
    
    if len(points) > 1:
        draw.lines(screen, LINE_COLOR, False, points, LINE_THICKNESS)

    # 3. Малювання кнопки
    draw.rect(screen, current_btn_color, btn_rect, border_radius=15) # Закруглені кути
    
    # Текст на кнопці
    text_surface = font_big.render(btn_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=btn_rect.center)
    screen.blit(text_surface, text_rect)

    display.update()
    clock.tick(60)

stream.stop()
quit()
