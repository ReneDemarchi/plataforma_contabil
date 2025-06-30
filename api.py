import json
import requests

def consultar(cnpj):
    """Consulta dados do CNPJ usando a API pública da ReceitaWS."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "Python-requests/2.x"
        )
    }
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code == 200:
        dados = resp.json()
        return dados
    elif resp.status_code == 429:
        return 'Esperar 30 segundos'
    else:
        print(f"Erro {resp.status_code}: {resp.text}")
        return 'Erro'

if __name__ == "__main__":
    a = consultar("00242184000104")
    print(a)