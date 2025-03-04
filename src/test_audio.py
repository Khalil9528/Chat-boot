import sounddevice as sd
import soundfile as sf

def play_audio_via_virtual_cable(audio_path):
    data, samplerate = sf.read(audio_path)
    print(f"Lecture de : {audio_path} à {samplerate} Hz")
    sd.play(data, samplerate, device=13)
    sd.wait()
    print("Lecture terminée !")

play_audio_via_virtual_cable("C:/Users/khali/Documents/google-meet-bot/assets/audio.mp3")
