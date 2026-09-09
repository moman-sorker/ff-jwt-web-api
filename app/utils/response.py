import requests
from app.proto import my_pb2, output_pb2
from app.utils.gen_token import encrypt_message, get_token
from config import AES_KEY, AES_IV
import binascii
from datetime import datetime, timezone
from app.utils.decode_token import decode
from pprint import pprint
import json
from byte import *
from app.utils.xthug import DeCode_PackEt
from config import VERSION
import base64
def parse_response(response_content):
    # Parse the response to extract key fields
    response_dict = {}
    lines = response_content.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            response_dict[key.strip()] = value.strip().strip('"')
    return response_dict

def current_timestamp(fmt="iso", tz=timezone.utc):
    now = datetime.now(tz)
    if fmt == "iso":
        return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if fmt == "epoch":
        return int(now.timestamp())
    return now.strftime(fmt)

def GeT_PLayer_level(uid, Token,api):
    try:
        payload_hex = "08" + Encrypt_ID(str(uid)) + "1801"
        data = bytes.fromhex(encrypt_api(payload_hex))

        url = api+"/GetPlayerPersonalShow"
        
        headers = {
            "Authorization": f"Bearer {Token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion":VERSION,
            "Content-Type": "application/octet-stream",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }

        response = requests.post(url, headers=headers, data=data, verify=False)
        
        if response.status_code != 200:
            
            return None,None,None
            
        # --- D?codage de la r?ponse ---
        packet = binascii.hexlify(response.content).decode('utf-8')
        decoded = DeCode_PackEt(packet)
        Thug_data = json.loads(decoded)
        # pprint(Thug_data)
        # --- Extraction s?curis?e des infos joueur ---
        player_data = Thug_data.get("1", {}).get("data", {})

        level = player_data.get("6", {}).get("data", "0")
        exp = player_data.get("7", {}).get("data", "0")
        nickname = player_data.get("3", {}).get("data", "0")
        #print(level,exp)
        return level,exp,nickname

    except Exception:
        return None,None,None

def build_game_data(token_data: dict, platform: int):
    game_data = my_pb2.GameData()



    game_data.timestamp = current_timestamp()  # ← conservé
    game_data.game_name = "free fire"
    game_data.game_version = 1  # ← mis à jour
    game_data.version_code = "1.126.3"  # ← mis à jour
    game_data.os_info = "Android OS 9 / API-28 (TP1A.220624.014/S908EXXS2BWA2)"  # ← mis à jour
    game_data.device_type = "Handheld"
    game_data.network_provider = "Bouygues Telecom"  # ← mis à jour
    game_data.connection_type = "WIFI"
    game_data.screen_width = 1600  # ← mis à jour
    game_data.screen_height = 900  # ← mis à jour
    game_data.dpi = "240"
    game_data.cpu_info = "x86-64 SSE3 SSE4.1 SSE4.2 AVX | 2000 | 4"  # ← mis à jour
    game_data.total_ram = 3940  # ← mis à jour
    game_data.gpu_name = "Adreno (TM) 540"  # ← mis à jour
    game_data.gpu_version = "OpenGL ES 3.2 (4.5.0 NVIDIA 596.36)"  # ← mis à jour
    game_data.user_id = "Google|c5e5916a-9e46-43ac-80eb-ac5c8d7c79f4"  # ← mis à jour
    game_data.ip_address = "165.169.250.93"  # ← mis à jour
    game_data.language = "en"
    game_data.open_id = token_data["open_id"]  # ← conservé
    game_data.access_token = token_data["access_token"]  # ← conservé
    game_data.platform_type = platform  # ← conservé
    game_data.device_form_factor = "Handheld"
    game_data.device_model = "samsung SM-S908E"  # ← mis à jour

    # Champs supplémentaires
    game_data.field_60 = 128886  # ← mis à jour
    game_data.field_61 = 110217  # ← mis à jour
    game_data.field_62 = 7998  # ← mis à jour
    game_data.field_63 = 5785  # ← mis à jour
    game_data.field_64 = 116787  # ← mis à jour
    game_data.field_65 = 128886  # ← mis à jour
    game_data.field_66 = 116787  # ← mis à jour
    game_data.field_67 = 128886  # ← mis à jour
    game_data.field_70 = platform  # ← conservé
    game_data.field_73 = 3  # ← mis à jour
    game_data.library_path = "/data/app/com.dts.freefireth-nJXwOmOfD2wUXNTgtBx3oA==/lib/arm64"  # ← mis à jour
    game_data.field_76 = 1
    game_data.apk_info = "4c322aeb56444feaa151d1ea91a8f7f2|/data/app/com.dts.freefireth-nJXwOmOfD2wUXNTgtBx3oA==/base.apk"  # ← mis à jour
    game_data.field_78 = 3  # ← mis à jour
    game_data.field_79 = 2  # ← mis à jour
    game_data.os_architecture = "64"  # ← mis à jour
    game_data.build_number = "2019120776"  # ← mis à jour
    game_data.field_85 = 3  # ← mis à jour
    game_data.graphics_backend = "OpenGLES2"
    game_data.max_texture_units = 4095  # ← mis à jour
    game_data.rendering_api = platform  # ← conservé
    game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"  # ← gardé comme avant
    game_data.field_92 = 9996  # ← mis à jour
    game_data.marketplace = "android"  # ← mis à jour
    game_data.encryption_key = "KqsHT76xOs3o2Fr8LodmV+W+JM/vI4bNY0LviMpTOCwVS9T4b5jAyexNTWuIvnuVZQkZg8GYDirA1+MzO0uoEYvRFMo="  # ← mis à jour
    game_data.total_storage = 111207  # ← mis à jour
    game_data.field_97 = 1
    game_data.field_98 = 1
    game_data.field_99 = str(platform)  # ← conservé
    game_data.field_100 = str(platform)  # ← conservé


    return game_data

def process_token(uid, password):
    error, token_data = get_token(password, uid)
    

    if error ==True:
        error =token_data.get("error")
        return {"error": True,"message1":error,"status_code": 500}
    

    if not token_data.get("access_token") or not token_data.get("open_id"):
        return {"error": True,"message2":"Failed to retrieve token data or account not working ","status_code": 500}
    


    game_data = build_game_data(token_data, 4)
    serialized_data = game_data.SerializeToString()

    # Encrypt the data
    encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)
    hex_encrypted_data = binascii.hexlify(encrypted_data).decode("utf-8")

    # Send the encrypted data to the server
    url = "https://loginbp.ggpolarbear.com/MajorLogin"
    headers = {  
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PPR1.180720.122)",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": VERSION
    }
    edata = bytes.fromhex(hex_encrypted_data)
    # print(edata)
    try:
        response = requests.post(
            url, data=edata, headers=headers, verify=False, timeout=10
        )
        if response.status_code == 200:
            example_msg = output_pb2.Lokesh()
            try:
                example_msg.ParseFromString(response.content)
                # Parse the response to extract key fields
                response_dict = parse_response(str(example_msg))
         
                
                if not response_dict.get("token"):  
                    packet = binascii.hexlify(response.content).decode('utf-8')
                    decoded = DeCode_PackEt(packet)
                    Thug_data = json.loads(decoded)
                    d = Thug_data.get("13", {}).get("data", {})
                  
                    message = d.get("4", {}).get("data", "Unknown")
                    ban_value = d.get("2", {}).get("data")  # pr?sent seulement sur temp ban ?
                    timestamp = d.get("3", {}).get("data")

                    if ban_value is not None:
                        ban_type = "ban_temporary"
                    else:
                        ban_type = "ban_permanent"
                        
                    if timestamp:
                        ban_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    return {"uid": uid, "status_code":400, "reason": message,"ban_date":ban_date if timestamp else "N/A", "ban_type": ban_type,"error":False}
                token = response_dict.get("token", "N/A")
                region=response_dict.get("region", "N/A")
                api = response_dict.get("api", "N/A")
                
                account_id ,nickname0,release_version =decode(token)
                
                level,exp,nickname = GeT_PLayer_level(account_id,token,api)
                if not level or not exp:
                    level,exp = 0,0

                
                mssg= {
                    "status_code":response.status_code,
                    "server":region ,
                    "credits": "M. Sarker",
                    "token": token,
                    "token_access" : game_data.access_token,
                    "open_id":game_data.open_id,
                    "account_id":account_id,
                    "nickname":nickname,
                    "api":api,
                    "error":False,
                    "exp":exp,
                    "level":level,
                }
                
                return mssg
            except Exception as e:
                return {"uid": uid, "error": f"Failed to deserialize the response: {e}"}
        else:
            print(f"Failed to retrieve token2 for UID {uid}: {response.text}")
            return {
                "uid": uid,
                "status_code":response.status_code,
                "message5":{response.reason},
                "error": True,
            }
    except requests.RequestException as e:
        return {"status_code":response.status_code,"uid": uid, "message": f"An error occurred while making the request: {e}","error": True}
