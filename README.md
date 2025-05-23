# Transcrição de Áudio de Vídeo

Este projeto é uma aplicação simples em Python que permite extrair o áudio de arquivos de vídeo, dividir o áudio em trechos de 3 minutos, transcrever o áudio para texto utilizando a API do Google Speech Recognition e salvar as transcrições em arquivos de texto.

A aplicação possui uma interface gráfica feita com Tkinter para facilitar o uso, permitindo selecionar o vídeo, acompanhar o progresso da transcrição e receber notificações sobre o status do processo.

---

## Funcionalidades

- Seleção de arquivos de vídeo (`.mp4`).
- Extração do áudio do vídeo em formato `.mp3`.
- Divisão do áudio em pedaços de até 3 minutos para facilitar a transcrição.
- Transcrição de cada trecho usando o serviço de reconhecimento de fala do Google (`speech_recognition`).
- Salvamento das transcrições em arquivos `.txt` separados por trecho, além de uma transcrição completa consolidada com timestamp.
- Interface gráfica simples para acompanhar o progresso e interagir com o programa.

---

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - `moviepy`
  - `pydub`
  - `speech_recognition`
  - `tkinter` (já incluído na maioria das distribuições Python)
- **FFmpeg** instalado e configurado no sistema (necessário para o `moviepy` e `pydub` funcionarem corretamente)

---

## Instalação das dependências

Para instalar as bibliotecas Python necessárias, use o comando:

```bash
pip install moviepy pydub speechrecognition
