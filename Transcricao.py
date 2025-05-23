import os
import threading
import shutil
from datetime import datetime
from tkinter import Tk, filedialog, Label, Button, messagebox
from moviepy import VideoFileClip
from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr

def extrair_audio(video_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile("audio.mp3", codec='mp3')

def dividir_audio():
    audio = AudioSegment.from_file("audio.mp3", format="mp3")
    chunk_length_ms = 180000  # 3 minutos
    return make_chunks(audio, chunk_length_ms)

def transcrever_chunks(chunks, update_status):
    recognizer = sr.Recognizer()
    output_dir = "transcricoes"
    os.makedirs(output_dir, exist_ok=True)
    transcricao_completa = ""

    for i, chunk in enumerate(chunks):
        chunk_filename = os.path.join(output_dir, f"audio{i}.wav")
        chunk.export(chunk_filename, format="wav")

        update_status(f"Processando trecho {i + 1} de {len(chunks)}...")

        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language='pt-BR')
            except sr.UnknownValueError:
                text = "[Inaudível]"
            except sr.RequestError as e:
                text = f"[Erro na solicitação: {e}]"

        transcript_filename = chunk_filename.replace(".wav", ".txt")
        with open(transcript_filename, "w", encoding="utf-8") as f:
            f.write(text)

        transcricao_completa += f"Trecho {i}:\n{text}\n\n"

    # Salva transcrição final com data e hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"transcricao_completa_{timestamp}.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(transcricao_completa)

    # Limpa arquivos temporários
    if os.path.exists("audio.mp3"):
        os.remove("audio.mp3")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    return f"Transcrição salva como '{output_filename}'"

def iniciar_processo_thread(file_path, update_status):
    try:
        update_status("Extraindo áudio...")
        extrair_audio(file_path)

        update_status("Dividindo áudio...")
        chunks = dividir_audio()

        update_status("Transcrevendo áudio...")
        resultado = transcrever_chunks(chunks, update_status)

        update_status(resultado)
        messagebox.showinfo("Sucesso", resultado)
    except Exception as e:
        update_status("Erro no processo.")
        messagebox.showerror("Erro", str(e))

def iniciar_processo():
    file_path = filedialog.askopenfilename(filetypes=[("Vídeos", "*.mp4 *.opus")])
    if not file_path:
        return

    threading.Thread(
        target=iniciar_processo_thread,
        args=(file_path, lambda msg: status_label.config(text=msg)),
        daemon=True
    ).start()

# Interface Gráfica
janela = Tk()
janela.title("Transcrição de Áudio de Vídeo")
janela.geometry("400x200")

titulo = Label(janela, text="Transcrever Áudio de um Vídeo", font=("Helvetica", 14))
titulo.pack(pady=20)

botao = Button(janela, text="Selecionar vídeo .mp4", command=iniciar_processo)
botao.pack(pady=10)

status_label = Label(janela, text="", fg="blue")
status_label.pack(pady=10)

desenvolvimento = Label(janela, text="Desenvolvido por Carlos H S N A Feu")
desenvolvimento.pack(pady=8)

janela.mainloop()
