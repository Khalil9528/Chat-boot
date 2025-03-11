import time                      # Module pour gérer les fonctions liées au temps (ex: sleep)
import threading                 # Module pour gérer l'exécution de tâches en parallèle (multithreading)
import os                        # Module pour interagir avec le système d'exploitation (vérifier/supprimer des fichiers)

# Importation des modules Selenium pour automatiser le navigateur
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Gère automatiquement l'installation du ChromeDriver

# Modules pour la lecture et la manipulation de fichiers audio
import sounddevice as sd         # Pour lire l'audio sur un périphérique spécifique
import soundfile as sf           # Pour lire et récupérer les données d'un fichier audio
from pydub import AudioSegment   # Pour manipuler et convertir des fichiers audio

def play_audio(audio_path):
    """
    Joue un fichier audio via le câble audio virtuel VB-Audio et supprime le fichier temporaire.
    """
    try:
        # Vérifie si le fichier audio existe, sinon affiche une erreur et sort de la fonction
        if not os.path.exists(audio_path):
            print("Fichier audio introuvable :", audio_path)
            return
        
        print("Lecture audio en cours")
        
        # Charge le fichier audio avec pydub et le convertit en WAV pour garantir la compatibilité
        audio = AudioSegment.from_file(audio_path)
        temp_audio_file = "temp.wav"
        audio.export(temp_audio_file, format="wav")  # Sauvegarde le fichier converti en WAV
        
        # Lit le fichier WAV pour récupérer les données audio et le taux d'échantillonnage
        data, samplerate = sf.read(temp_audio_file)
        # Joue l'audio sur le périphérique virtuel spécifié (VB-Audio Virtual Cable)
        sd.play(data, samplerate, device="CABLE Input (VB-Audio Virtual Cable)")
        sd.wait()  # Attend la fin de la lecture audio
        print("Audio terminé.")

        # Supprime le fichier temporaire une fois la lecture terminée
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
    
    except Exception as e:
        # Affiche toute erreur rencontrée durant la lecture audio
        print("Erreur lors de la lecture audio :", e)

def wait_for_element(driver, xpath, timeout=20):
    """
    Attend qu'un élément soit cliquable et le retourne, ou None si non trouvé.
    - driver : instance du navigateur Selenium
    - xpath : chaîne de caractères définissant le chemin XPath de l'élément recherché
    - timeout : temps maximum d'attente (en secondes)
    """
    try:
        # Attend que l'élément identifié par le XPath soit cliquable
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except Exception as e:
        # En cas d'échec, affiche un message d'erreur et retourne None
        print(f"Élement non trouvé pour XPath {xpath} : {e}")
        return None

def join_meet(meet_url):
    """
    Ouvre un Google Meet, rejoint la réunion, joue un fichier audio et quitte automatiquement.
    - meet_url : URL de la réunion Google Meet
    """
    # Configuration des options pour Chrome
    chrome_options = Options()
    
    chrome_options.add_argument("--remote-debugging-port=9222")   # Permet le débogage à distance
    chrome_options.add_argument("--no-sandbox")                   # Désactive le sandboxing pour éviter certains problèmes
    chrome_options.add_argument("--disable-dev-shm-usage")          # Réduit l'utilisation de la mémoire partagée
    chrome_options.add_argument("--disable-gpu")                    # Désactive l'accélération GPU
    chrome_options.add_argument("--disable-extensions")             # Désactive les extensions Chrome
    chrome_options.add_argument("--use-fake-ui-for-media-stream")     # Permet de bypasser les pop-ups d'autorisation pour le média
    chrome_options.add_argument("--use-fake-device-for-media-stream") # Utilise des périphériques médias fictifs
    
    # Utilisation d'un profil existant pour éviter de gérer l'authentification Google
    chrome_options.add_argument(r"--user-data-dir=C:\Users\khali\AppData\Local\Google\Chrome\User Data")
    chrome_options.add_argument(r"--profile-directory=Default")

    # Installe et configure automatiquement le ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Ouvre la page Google Meet avec l'URL fournie
        driver.get(meet_url)
        time.sleep(10)  # Pause de 10 secondes pour attendre le chargement complet de la page

        # Liste de différents XPath possibles pour trouver le bouton "Rejoindre" sur la page
        join_xpaths = [
            "//button[contains(text(), 'Participer à la réunion')]",
            "//button[contains(text(), 'Participer')]",
            "//button[contains(., 'Rejoindre maintenant')]",
            "//div[@role='button' and contains(., 'Rejoindre')]"
        ]

        join_button = None
        # Parcourt chaque XPath pour trouver le bouton "Rejoindre"
        for xpath in join_xpaths:
            join_button = wait_for_element(driver, xpath)
            if join_button:
                print("Bouton 'Rejoindre' trouvé, tentative de clic...")
                try:
                    # Tente de cliquer sur le bouton directement
                    join_button.click()
                except Exception as e:
                    # En cas d'erreur, utilise JavaScript pour forcer le clic
                    driver.execute_script("arguments[0].click();", join_button)
                print("Le bot a cliqué sur 'Rejoindre'.")
                break  # Sort de la boucle dès qu'un bouton est trouvé et cliqué

        # Si aucun bouton n'a été trouvé, affiche un message d'erreur et affiche le HTML pour débogage
        if not join_button:
            print("Impossible de trouver le bouton 'Rejoindre'.")
            print("HTML de la page pour debugging :")
            print(driver.page_source)
            return

        # Attendre quelques secondes pour s'assurer que la réunion est bien rejointe
        time.sleep(5)

        # Définir le chemin du fichier audio à jouer
        audio_path = "C:/Users/khali/Documents/google-meet-bot/assets/audio.mp3"
        # Démarrer la lecture audio dans un thread séparé pour ne pas bloquer le script principal
        audio_thread = threading.Thread(target=play_audio, args=(audio_path,))
        audio_thread.start()
        audio_thread.join()  # Attend que le thread de lecture audio se termine

        print("Audio terminé, tentative de quitter la réunion...")

        # Liste de différents XPath possibles pour trouver le bouton "Quitter" sur la page
        leave_xpaths = [
            "//button[contains(@aria-label, 'Quitter')]",
            "//button[contains(@aria-label, 'Quit')]",
            "//div[@role='button' and contains(., 'Quitter')]"
        ]

        leave_button = None
        # Parcourt chaque XPath pour trouver le bouton "Quitter"
        for xpath in leave_xpaths:
            leave_button = wait_for_element(driver, xpath)
            if leave_button:
                try:
                    # Tente de cliquer sur le bouton directement
                    leave_button.click()
                except Exception as e:
                    # En cas d'échec, force le clic via JavaScript
                    driver.execute_script("arguments[0].click();", leave_button)
                print("Réunion quittée.")
                break  # Sort de la boucle dès qu'un bouton est trouvé et cliqué

        # Si aucun bouton de quitter n'a été trouvé, affiche un message d'erreur
        if not leave_button:
            print("Impossible de trouver le bouton 'Quitter'.")

    except Exception as e:
        # Capture et affiche toute erreur inattendue survenue pendant l'exécution
        print("Erreur inattendue :", e)
    finally:
        # Ferme toujours le navigateur pour libérer les ressources, même en cas d'erreur
        driver.quit()
        print("Navigateur fermé.")

# Bloc principal du script
if __name__ == "__main__":
    # Demande à l'utilisateur d'entrer le lien de la réunion Google Meet via la console
    meet_link = input("Veuillez entrer le lien de la réunion Google Meet : ")
    # Lance la fonction pour rejoindre la réunion avec le lien fourni
    join_meet(meet_link)