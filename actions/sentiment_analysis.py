from textblob import TextBlob

def analisis_sentimen(pesan: str) -> str:
    analysis = TextBlob(pesan)
    # Menggunakan polarity untuk menentukan sentimen
    if analysis.sentiment.polarity > 0:
        return "bahagia"
    elif analysis.sentiment.polarity < 0:
        return "marah"
    else:
        return "netral"

def ambil_waktu_hari() -> str:
    from datetime import datetime
    jam = datetime.now().hour
    if jam < 12:
        return "pagi"
    elif jam < 18:
        return "siang"
    else:
        return "malam"

def generate_response(pesan_pengguna: str) -> str:
    sentimen = analisis_sentimen(pesan_pengguna)
    waktu_hari = ambil_waktu_hari()
    
    if sentimen == "bahagia":
        response = "Senang mendengar itu! Ada yang bisa saya bantu hari ini?"
    elif sentimen == "marah":
        response = "Maaf mendengar Anda marah. Bagaimana saya bisa membantu Anda dengan lebih baik?"
    else:  # netral atau sedih
        response = "Saya mengerti. Jika Anda butuh bantuan, saya siap membantu."

    # Menyesuaikan respon dengan waktu
    if waktu_hari == "pagi":
        response = f"Selamat pagi! {response}"
    elif waktu_hari == "siang":
        response = f"Selamat siang! {response}"
    else:  # malam
        response = f"Selamat malam! {response}"

    return response
