from pygame import *
import sounddevice as sd
import scipy.io.wavfile as wav
import os # Для перевірки наявності файлу

# === Налаштування ===
fs = 44100
recording = None
is_recording = False
voice_file = "voice_record.wav"
minus_track = "mic-wave-pygame/MinusDuHast.mp3" 

# Ініціалізація
init()
mixer.init()
mixer.music.set_volume(0.5)

window_size = 1200, 600
window = display.set_mode(window_size)
display.set_caption("Karaoke Recorder") # Заголовок вікна
clock = time.Clock()

font.init()
font_big = font.SysFont("Arial", 32)

btn_rect = Rect(425, 250, 350, 80)
rect_color = 'white'
btn_text = "Запис"

def start_voice_record():
    global recording
    # Записуємо у фоновому режимі (без блокування вікна)
    recording = sd.rec(int(fs * 5), samplerate=fs, channels=1, dtype='int16') 

def stop_voice_record():
    global recording
    sd.stop()
    # Зберігаємо тільки якщо запис існує
    if recording is not None:
        wav.write(voice_file, fs, recording)
        return True
    return False

def play_song_and_voice_together():
    # Перевіряємо, чи існує файл перед завантаженням
    if os.path.exists(voice_file):
        # 1. Запускаємо мінусовку
        mixer.music.load(minus_track)
        mixer.music.play()
        
        # 2. Запускаємо записаний голос
        voice_sound = mixer.Sound(voice_file)
        voice_sound.play()
    else:
        print("Файл запису ще не створено!")

# === Головний цикл ===
run = True 

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False # Правильний вихід
            
        if e.type == MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(e.pos):
                if not is_recording:
                    # --- ПОЧАТОК ЗАПИСУ ---
                    rect_color = 'red'
                    btn_text = "Стоп та прослухати"
                    is_recording = True
                    
                    # Граємо музику, щоб співати під неї
                    mixer.music.load(minus_track)
                    mixer.music.play()
                    
                    start_voice_record()
                else:
                    # --- КІНЕЦЬ ЗАПИСУ ---
                    rect_color = 'white'
                    btn_text = "Запис"
                    is_recording = False
                    
                    mixer.music.stop() # Зупиняємо музику перед прослуховуванням
                    
                    if stop_voice_record(): # Зберігаємо файл
                        play_song_and_voice_together() # Слухаємо результат

    # Малювання
    window.fill('grey')
    draw.rect(window, rect_color, btn_rect)
    
    # Центрування тексту на кнопці (трохи математики для краси)
    text_surface = font_big.render(btn_text, True, 'black')
    text_rect = text_surface.get_rect(center=btn_rect.center)
    window.blit(text_surface, text_rect)

    display.update()
    clock.tick(60)

# Вихід з програми
quit()