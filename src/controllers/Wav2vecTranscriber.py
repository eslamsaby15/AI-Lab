import librosa
import os
import torch

class Wav2VecTranscriber:
    def __init__(self, model_name="facebook/wav2vec2-base-960h", device=None):
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
        import torch

        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        self.model.to(self.device)

    def transcribe(self, audio_path: str, chunk_sec: int = 30):
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(audio_path)

        speech, sr = librosa.load(audio_path, sr=16000, mono=True)
        samples_per_chunk = chunk_sec * sr

        texts = []
        for i in range(0, len(speech), samples_per_chunk):
            chunk = speech[i:i + samples_per_chunk]
            input_values = self.processor(
                chunk,
                sampling_rate=sr,
                return_tensors="pt"
            ).input_values.to(self.device)

            with torch.no_grad():
                logits = self.model(input_values).logits

            predicted_ids = torch.argmax(logits, dim=-1)
            text = self.processor.batch_decode(predicted_ids)[0]
            texts.append(text)

        return " ".join(texts).strip()
