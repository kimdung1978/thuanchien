import speech_recognition as sr
from gtts import gTTS
import os
from datetime import date, datetime
import subprocess
import requests
from bs4 import BeautifulSoup
import random
import pygame
from pytube import YouTube
import tkinter as tk
from tkinter import ttk
import webbrowser

# Khởi tạo pygame mixer để phát nhạc
pygame.mixer.init()

def get_system_info():
    try:
        system_info = subprocess.check_output("systeminfo", shell=True).decode()
    except Exception as e:
        system_info = str(e)
    return system_info

def google_search(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = ""

    search_result = soup.find(class_='BNeawe iBp4i AP7Wnd')
    if search_result:
        result = search_result.get_text()
    else:
        for g in soup.find_all(class_='BNeawe s3v9rd AP7Wnd'):
            result = g.get_text()
            break
    return result.strip()

def comfort():
    comforting_messages = [
        "Tôi hiểu cảm giác của bạn. Hãy cố gắng lên, mọi chuyện sẽ ổn thôi.",
        "Bạn không cô đơn đâu, tôi luôn ở đây để lắng nghe bạn.",
        "Hãy tìm điều gì đó vui vẻ để làm, có thể nó sẽ giúp bạn thấy khá hơn.",
        "Đôi khi, chúng ta chỉ cần một chút thời gian cho bản thân. Hãy dành thời gian chăm sóc bản thân bạn nhé."
    ]
    return random.choice(comforting_messages)

def speak(text):
    if text:
        tts = gTTS(text, lang='vi')
        tts.save("response.mp3")
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.unload()
        os.remove("response.mp3")
    else:
        print("Nothing to speak")

def tay_traichitrang():
    pygame.mixer.music.load("taytraichitrang.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.unload()

def thienhakhapbonphuong():
    pygame.mixer.music.load("thienhakhapbonphuong.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.unload()

def play_goodbye_song():
    # Phát nhạc chuông tạm biệt
    pygame.mixer.music.load("goodbye.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.unload()

def play_youtube_video(url):
    webbrowser.open(url)

def on_start_listen(text_widget):
    global robot_ear
    while True:
        with sr.Microphone() as mic:
            print("Robot: Tôi đang nghe")
            audio = robot_ear.listen(mic)
        print("Robot: ...")
        try:
            you = robot_ear.recognize_google(audio, language="vi-VN")
        except:
            you = ""
        print("Bạn: " + you)

        robot_brain = ""

        if you == "":
            robot_brain = "Tôi không nghe rõ, bạn thử lại nhé"
        elif "xin chào" in you or "chào" in you:
            robot_brain = "Xin chào bạn"
        elif "hôm nay" in you or "ngày" in you:
            today = date.today()
            robot_brain = today.strftime("%d tháng %m năm %Y")
        elif "giờ" in you or "thời gian" in you:
            robot_brain = datetime.now().strftime("%H:%M")
        elif "đẹp trai" in you:
            robot_brain = "Thuận"
        elif "máy tính" in you:
            robot_brain = get_system_info()
        elif "google" in you:
            query = you.replace("google", "").strip()
            robot_brain = google_search(query)
            if not robot_brain:
                robot_brain = f"Tôi không tìm thấy kết quả cho '{query}' trên Google"
        elif "tạm biệt" in you or "bye" in you:
            robot_brain = "Tạm biệt bạn!"
            print('robot_brain: ' + robot_brain)
            speak(robot_brain)
            play_goodbye_song()
            break
        elif "muốn được lời khuyên" in you:
            robot_brain = comfort()
        elif "hát" in you:
            robot_brain = "Bài hát mang tên: Tay trái chỉ trăng"
            #play_youtube_video("https://youtu.be/ATPulcGQ2SE?si=-rRZfoYXQvlHC48R")
            tay_traichitrang()
            # Mở video bài hát trên YouTube

        elif "ca nhạc" in you:
            robot_brain = "Bài hát mang tên: Thiên hạ khắp bốn phương"
            #play_youtube_video("https://www.youtube.com/watch?v=oYDfuGfd9eE")
            thienhakhapbonphuong()
            # Mở video bài hát trên YouTube

        else:
            query = you.strip()
            robot_brain = google_search(query)
            if not robot_brain:
                robot_brain = f"Tôi không tìm thấy kết quả cho '{query}' trên Google"

        print("Robot: " + robot_brain)
        text_widget.configure(state=tk.NORMAL)
        text_widget.insert(tk.END, "Bạn: " + you + "\n")
        text_widget.insert(tk.END, "Robot: " + robot_brain + "\n")
        text_widget.configure(state=tk.DISABLED)
        speak(robot_brain)

def start_listening_thread(text_widget):
    import threading
    listen_thread = threading.Thread(target=on_start_listen, args=(text_widget,))
    listen_thread.start()

def create_gui():
    root = tk.Tk()
    root.title("Trí tuệ nhân tạo")
    root.geometry("600x500")

    label = ttk.Label(root, text="Robot: Chào bạn, bạn cần giúp gì không?")
    label.pack(pady=10)

    text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=60)
    text_widget.pack(pady=20)

    listen_button = ttk.Button(root, text="Bắt đầu nghe", command=lambda: start_listening_thread(text_widget))
    listen_button.pack(pady=20)

    def on_closing():
        global robot_brain
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        robot_brain = "Tạm biệt bạn!"
        print("Robot: " + robot_brain)
        text_widget.configure(state=tk.NORMAL)
        text_widget.insert(tk.END, "Robot: " + robot_brain + "\n")
        text_widget.configure(state=tk.DISABLED)
        speak(robot_brain)
        root.destroy()

    root.protocol("Trí tuệ nhân tạo", on_closing)
    root.iconbitmap('logo.ico')

    quit_button = ttk.Button(root, text="Thoát", command=on_closing)
    quit_button.pack(pady=10)

    root.mainloop()

    # Dừng các hoạt động còn chạy khi thoát khỏi GUI
    pygame.mixer.music.stop()

    # Nếu chương trình vẫn chạy, dừng nó
    pygame.mixer.quit()

if __name__ == '__main__':
    robot_ear = sr.Recognizer()
    create_gui()
