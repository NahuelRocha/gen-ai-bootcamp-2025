import requests

def test_whisper():
    url = "http://localhost:7066/v1/audio/transcriptions"
    
    files = {
        'file': ('test.wav', open('test.wav', 'rb'), 'audio/wav'),
    }
    
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print("Respuesta completa:", response.json())

if __name__ == "__main__":
    test_whisper()