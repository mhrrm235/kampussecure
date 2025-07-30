

import subprocess
import requests

VT_API_KEY = "97c207da8022a88fba336654652294c3dbf06026f84122f5431827226a60ea05"
GSB_API_KEY = "AIzaSyD4HH2xiy1vU6BZgq9G4fte7wpehBhEU6g"

def check_virustotal(url):
    vt_url = "https://www.virustotal.com/api/v3/urls"
    headers = {"x-apikey": VT_API_KEY}
    resp = requests.post(vt_url, headers=headers, data={"url": url})
    if resp.status_code == 200:
        analysis_id = resp.json()["data"]["id"]
        result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        result_resp = requests.get(result_url, headers=headers)
        if result_resp.status_code == 200:
            stats = result_resp.json()["data"]["attributes"]["stats"]
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0)
            return f"VirusTotal: {malicious} malicious, {suspicious} suspicious, {harmless} harmless"
        else:
            return "VirusTotal: Gagal mengambil hasil analisis."
    else:
        return "VirusTotal: Gagal submit URL."

def check_gsb(url):
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GSB_API_KEY}"
    payload = {
        "client": {
            "clientId": "kampussecure-app",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    try:
        resp = requests.post(api_url, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("matches"):
                return "Google Safe Browsing: Berbahaya! (Terdeteksi)"
            else:
                return "Google Safe Browsing: Aman (Tidak terdeteksi)"
        else:
            return "Google Safe Browsing: Gagal request."
    except Exception as e:
        return f"Google Safe Browsing: Error {e}"

def run_scan(target):
    import re
    try:
        # Validasi dan ekstrak domain/IP
        input_str = target.strip()
        # Jika input IP
        ip_pattern = r'^\d{1,3}(?:\.\d{1,3}){3}$'
        if re.match(ip_pattern, input_str):
            scan_target = input_str
        else:
            # Hilangkan protokol
            scan_target = re.sub(r'^https?://', '', input_str)
            # Hilangkan path/query/fragment
            scan_target = scan_target.split('/')[0].split('?')[0].split('#')[0]
        # Scan dengan nmap
        nmap_result = ""
        whatweb_result = ""
        try:
            nmap_result = subprocess.check_output(['nmap', '-F', scan_target], text=True)
        except Exception as e:
            nmap_result = f"Nmap error: {str(e)}"
        try:
            whatweb_result = subprocess.check_output(['whatweb', '--no-color', scan_target], text=True)
        except Exception as e:
            whatweb_result = f"WhatWeb error: {str(e)}"

        # Deteksi kata kunci berbahaya
        keywords = ['malware', 'phishing', 'suspicious', 'virus', 'trojan', 'attack', 'exploit']
        combined = (str(nmap_result) + str(whatweb_result)).lower()
        kategori = 'Tidak Berbahaya'
        for k in keywords:
            if k in combined:
                kategori = 'Berbahaya'
                break

        vt_result = check_virustotal(target)
        gsb_result = check_gsb(target)

        combined_result = (
            f"=== URL Target: {target} ===\n"
            f"=== Target Scan: {scan_target} ===\n"
            f"=== Kategori Link: {kategori} ===\n\n"
            f"{vt_result}\n{gsb_result}\n\n"
            f"=== Nmap Scan ({scan_target}) ===\n{nmap_result}\n\n=== WhatWeb Scan ({scan_target}) ===\n{whatweb_result}"
        )
        return combined_result

    except subprocess.CalledProcessError as e:
        return f"Terjadi kesalahan saat scan: {str(e)}"
    except Exception as e:
        return f"Terjadi error: {str(e)}"
