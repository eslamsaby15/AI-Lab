import os
import torchaudio
from fastapi import Depends
from .BaseController import BaseController
from .ProjectController import ProjectController
import librosa
import soundfile as sf
import yt_dlp
import warnings
warnings.filterwarnings("ignore")
import tempfile
import whisper
import subprocess
import numpy as np

class Youtube(BaseController):
    def __init__(self):
        super().__init__()
        self.project_controller = ProjectController()
        self.transcribe_model = whisper.load_model('small')

    def Download(self, url: str):
        project_key = self.generate_random_string()
        video_id = url.rstrip('/').split('/')[-1].split('?')[0]

        project_path = ProjectController().get_project_path(video_id)
        output_path = os.path.join(project_path, "%(id)s.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_path,
            "quiet": True,
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
        except yt_dlp.utils.DownloadError as e:
            raise Exception(f"❌ Unable to download video: {e}")

        y, sr = librosa.load(downloaded_file, sr=None)
        wav_path = os.path.join(project_path, project_key + ".wav")
        sf.write(wav_path, y, sr)

        return wav_path

        
    def save_dir(self, upload_file):
        project_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(upload_file.name)
        
        filename = f"{project_key}_{upload_file.name}"
        output_path = os.path.join(project_path, filename)
        
        with open(output_path, 'wb') as f:
            f.write(upload_file.getbuffer())
        
        return output_path
   