import time
import threading
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

def play_audio(audio_path):
    """Joue un fichier audio via le câble audio virtuel VB-Audio et supprime le fichier temporaire."""
    try:
        if not os.path.exists(audio_path):
            print("Fichier audio introuvable :", audio_path)
            return
        
        print("Lecture audio en cours")
        
        # Conversion en WAV pour une lecture compatible
        audio = AudioSegment.from_file(audio_path)
        temp_audio_file = "temp.wav"
        audio.export(temp_audio_file, format="wav")

        data, samplerate = sf.read(temp_audio_file)
        # Lecture sur le périphérique virtuel spécifié
        sd.play(data, samplerate, device="CABLE Input (VB-Audio Virtual Cable)")
        sd.wait()  
        print("🎵 Audio terminé.")

        # Nettoyage du fichier temporaire
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
    
    except Exception as e:
        print("Erreur lors de la lecture audio :", e)

def wait_for_element(driver, xpath, timeout=20):
    """Attend qu'un élément soit cliquable et le retourne, ou None si non trouvé."""
    try:
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except Exception as e:
        print(f"Élement non trouvé pour XPath {xpath} : {e}")
        return None

def join_meet(meet_url):
    """Ouvre un Google Meet, rejoint la réunion, joue un fichier audio et quitte automatiquement."""
    chrome_options = Options()
    
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    
    # Utilisation d'un profil existant pour éviter de gérer l'authentification
    chrome_options.add_argument(r"--user-data-dir=C:\Users\khali\AppData\Local\Google\Chrome\User Data")
    chrome_options.add_argument(r"--profile-directory=Default")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(meet_url)
        time.sleep(10)  # Attendre le chargement complet de la page

        # Liste des XPath possibles pour le bouton de rejoindre la réunion
        join_xpaths = [
            "//button[contains(text(), 'Participer à la réunion')]",
            "//button[contains(text(), 'Participer')]",
            "//button[contains(., 'Rejoindre maintenant')]",
            "//div[@role='button' and contains(., 'Rejoindre')]"
        ]

        join_button = None
        for xpath in join_xpaths:
            join_button = wait_for_element(driver, xpath)
            if join_button:
                print("Bouton 'Rejoindre' trouvé, tentative de clic...")
                try:
                    join_button.click()
                except Exception as e:
                    driver.execute_script("arguments[0].click();", join_button)
                print("Le bot a cliqué sur 'Rejoindre'.")
                break

        if not join_button:
            print("Impossible de trouver le bouton 'Rejoindre'.")
            print("HTML de la page pour debugging :")
            print(driver.page_source)
            return

        # Pause pour être sûr d'être dans la réunion
        time.sleep(5)

        # Lancement de la lecture audio sur un thread séparé
        audio_path = "C:/Users/khali/Documents/google-meet-bot/assets/audio.mp3"
        audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
        audio_thread.start()
        audio_thread.join()  # Attend la fin de la lecture audio

        print("Audio terminé, tentative de quitter la réunion...")

        # Liste des XPath possibles pour le bouton de quitter la réunion
        leave_xpaths = [
            "//button[contains(@aria-label, 'Quitter')]",
            "//button[contains(@aria-label, 'Quit')]",
            "//div[@role='button' and contains(., 'Quitter')]"
        ]

        leave_button = None
        for xpath in leave_xpaths:
            leave_button = wait_for_element(driver, xpath)
            if leave_button:
                try:
                    leave_button.click()
                except Exception as e:
                    driver.execute_script("arguments[0].click();", leave_button)
                print("Réunion quittée.")
                break

        if not leave_button:
            print("Impossible de trouver le bouton 'Quitter'.")

    except Exception as e:
        print("Erreur inattendue :", e)
    finally:
        driver.quit()
        print("Navigateur fermé.")

if __name__ == "__main__":
    meet_link = "https://meet.google.com/iwp-xvns-vyu"  
    join_meet(meet_link)
