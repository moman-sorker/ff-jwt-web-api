import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
from colorama import Fore

from pprint import pprint 

import requests

def get_token(password, uid):
    # Liste des URLs à tester
    urls = [
        "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant",
        "https://100067.connect.garena.com/oauth/guest/token/grant",
    ]
    
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }

    for url in urls:
        # Extraction dynamique du Host pour les headers
        host = url.split("//")[1].split("/")[0]
        headers = {
            "Host": host,
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A; Android 9; en; US;)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }

        try:
            response = requests.post(url, headers=headers, data=data, verify=False, timeout=10)
            
            # Si le code est 200, on a réussi
            # pprint(response.json())
      
            if response.status_code == 200:
                return False , response.json()
            
            # Si ce n'est pas 200, le code continue vers l'URL suivante
            print(f"Echec {url} (Status: {response.status_code}). Essai de la suivante...")
            
        except:
            # En cas d'erreur de connexion, on passe aussi à la suivante
            print(f"Erreur de connexion sur {url}")
            continue

    # Si aucune URL n'a fonctionné (après avoir parcouru toute la liste)
    return True , response.json()



def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message


def load_tokens(file_path, limit=None):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            tokens = list(data.items())
            if limit is not None:
                tokens = tokens[:limit]  # Set token limit
            return tokens
    except Exception as e:
        print(Fore.RED + f"Failed to load tokens: {e}")
        return []


