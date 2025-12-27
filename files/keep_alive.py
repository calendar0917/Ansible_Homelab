import requests
import time
import urllib.parse
import sys
import subprocess

# ================= 配置区 =================
USER = os.getenv('RUIJIE_USER')
# 填入你那个超长的加密字符串
ENCRYPTED_PASS = os.getenv('RUIJIE_PASS')
# =========================================

def check_internet():
    """check the internet"""
    try:
        # ping baidu or 1.1.1.1，timeout 2 second
        subprocess.check_call(["ping", "-c", "1", "-W", "2", "223.5.5.5"], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def get_current_qs():
    try:
        r = requests.get("http://1.1.1.1", allow_redirects=False, timeout=3)
        if "Location" in r.headers:
            full = r.headers["Location"]
            if "?" in full: return full.split("?", 1)[1]
    except: pass
    return ""

def login():
    qs = get_current_qs()
    url = "http://172.25.249.64/eportal/InterFace.do?method=login"
    payload = {
        "userId": USER,
        "password": ENCRYPTED_PASS,
        "service": "",
        "queryString": qs,
        "passwordEncrypt": "true"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        print(f"[{time.strftime('%T')}] Detecting offline, trying to login...")
        requests.post(url, data=payload, headers=headers, timeout=5)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(">>> Watchdog started...")
    while True:
        if check_internet():
            # if ok,relax 60 seconds
            pass
        else:
            # if not ok,relogin
            login()
            # wait 5 second for internet connect
            time.sleep(5)
            
            # retry, if ok,print log
            if check_internet():
                print(f"[{time.strftime('%T')}] Re-connected successfully!")
        
        # check per 60 seconds
        time.sleep(60)
