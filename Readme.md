# Google Meet Bot avec Lecture Audio

Ce projet permet d'automatiser la connexion à une réunion Google Meet, de jouer un fichier audio via un câble audio virtuel (VB-Audio Virtual Cable) et de quitter automatiquement la réunion. Le script utilise Selenium pour automatiser l'interaction avec l'interface de Google Meet et des bibliothèques audio en Python pour la lecture du son.

## Fonctionnalités

- **Connexion automatique à Google Meet** : Ouvre un navigateur Chrome et se connecte à une réunion via son URL.
- **Interaction automatisée** : Recherche et clique sur le bouton "Rejoindre" pour intégrer la réunion.
- **Lecture audio** : Joue un fichier audio (format MP3 converti en WAV) sur un périphérique audio virtuel.
- **Quitter la réunion** : Recherche et clique sur le bouton "Quitter" pour sortir de la réunion une fois l'audio terminé.
- **Utilisation d'un profil Chrome existant** : Évite la gestion manuelle de l'authentification en utilisant un profil Chrome pré-configuré.

## Prérequis

- **Python 3.6+**
- **Google Chrome** installé sur votre machine.
- **ChromeDriver** compatible avec votre version de Chrome (le script utilise `webdriver-manager` pour l'installation automatique).
- **VB-Audio Virtual Cable** : Assurez-vous d'avoir installé et configuré VB-Audio Virtual Cable pour rediriger la lecture audio.
- **Bibliothèques Python** suivantes :
  - `selenium`
  - `webdriver-manager`
  - `sounddevice`
  - `soundfile`
  - `pydub`
  
### Installation des dépendances

Vous pouvez installer toutes les dépendances via pip :

```bash
pip install selenium webdriver-manager sounddevice soundfile pydub
