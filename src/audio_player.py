import sounddevice as sd
import soundfile as sf

def play_audio_via_virtual_cable(file_path):
    data, samplerate = sf.read(file_path)
    
    #FORÇONS 48000 Hz POUR MIEUX PASSER SUR MEET
    if samplerate != 48000:
        import librosa
        data = librosa.resample(data.T, orig_sr=samplerate, target_sr=48000).T
        samplerate = 48000
    
    print(f"Lecture de : {file_path} à {samplerate} Hz")
    sd.play(data, samplerate, device=15)  # Remplace 15 par le bon ID
    sd.wait()
    print("Lecture terminée !")

play_audio_via_virtual_cable("C:/Users/khali/Documents/google-meet-bot/assets/audio.mp3")
