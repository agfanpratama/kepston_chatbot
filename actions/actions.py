import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

class ActionGreetUser(Action):
    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Menyapa pengguna dan meminta nama
        dispatcher.utter_message(response="utter_pembuka")

        return []

class ActionSaveNama(Action):

    def name(self) -> str:
        return "action_save_nama"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Mengambil pesan terakhir dari pengguna
        user_message = tracker.latest_message.get('text')
        
        # Mengambil nama dari input (misalkan nama adalah kata terakhir dari input)
        # Ini bisa disesuaikan sesuai dengan cara kamu ingin mengambil nama
        nama_pengguna = user_message.split()[-1]

        # Memberikan respons ke pengguna
        dispatcher.utter_message(response=f"utter_sapa_pengguna")
        
        # Mengembalikan SlotSet untuk menyimpan nama pengguna
        return [SlotSet("nama_pengguna", nama_pengguna)]

class ActionLaptopLenovo(Action):
    
    def name(self) -> Text:
        return "action_laptop_lenovo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Mengambil data produk dari file JSON
        with open('F:/rasa_projects/capstone/actions/produk.json', 'r') as file:
            produk_data = json.load(file)

        # Mengacak dan memilih 5 produk
        produk_acak = random.sample(produk_data, min(5, len(produk_data)))

        # Menyiapkan tombol produk
        buttons = []
        for produk in produk_acak:
            produk_id = produk.get("ID")
            nama = produk.get("nama")
            harga = produk.get("harga")

            # Menambahkan tombol untuk setiap produk
            buttons.append({
                "title": f"{nama} - {harga}",
                "payload": f'/pilih_produk{{"produk_id":"{produk_id}"}}'
            })

        # Mengirimkan pesan dengan tombol produk
        dispatcher.utter_message(text="Berikut 5 produk Lenovo di toko kami:", buttons=buttons)

        return []

class ActionPilihProduk(Action):

    def name(self) -> Text:
        return "action_pilih_produk"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Mendapatkan produk_id dari slot
        produk_id = tracker.get_slot("produk_id")

        # Memuat data produk dari file JSON
        with open('F:/rasa_projects/capstone/actions/produk.json', 'r') as file:
            produk_data = json.load(file)

        # Mencari produk berdasarkan produk_id
        produk_terpilih = next((produk for produk in produk_data if produk.get("ID") == produk_id), None)

        if produk_terpilih:
            nama_produk = produk_terpilih.get("nama")
            dispatcher.utter_message(text=f"Kamu memilih produk: {nama_produk}")
        else:
            dispatcher.utter_message(text="Produk tidak ditemukan.")

        return [SlotSet("produk_id", produk_id)]

class ActionDeskripsiLenovo(Action):
    
    def name(self) -> Text:
        return "action_deskripsi_lenovo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Mendapatkan produk_id dari slot
        produk_id = tracker.get_slot("produk_id")

        # Memuat data produk dari file JSON
        with open('F:/rasa_projects/capstone/actions/produk.json', 'r') as file:
            produk_data = json.load(file)

        # Mencari produk berdasarkan produk_id
        produk_terpilih = next((produk for produk in produk_data if produk.get("ID") == produk_id), None)

        if produk_terpilih:
            deskripsi = produk_terpilih.get("deskripsi")
            dispatcher.utter_message(text=f"Deskripsi produk:\n{deskripsi}")
        else:
            dispatcher.utter_message(text="Deskripsi untuk produk ini tidak ditemukan.")

        return []

#Sentiment Analysis##
from datetime import datetime

class ActionRespondBasedOnSentiment(Action):
    def name(self) -> Text:
        return "action_respond_based_on_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Mendapatkan intent terbaru
        latest_intent = tracker.latest_message['intent'].get('name')

        # Mendapatkan waktu saat ini
        current_hour = datetime.now().hour

        # Menentukan ucapan waktu sesuai waktu saat ini
        if 5 <= current_hour < 12:
            time_response = "utter_pagi"
        elif 12 <= current_hour < 15:
            time_response = "utter_siang"
        elif 15 <= current_hour < 19:
            time_response = "utter_greet_evening"
        else:
            time_response = "utter_sore"

        # Memberikan respons sesuai intent dan waktu
        if latest_intent == "marah":
            dispatcher.utter_message(response="utter_marah")
        elif latest_intent == "bahagia":
            dispatcher.utter_message(response="utter_bahagia")
        elif latest_intent == "sedih":
            dispatcher.utter_message(response="utter_sedih")
        else:
            dispatcher.utter_message(response=time_response)
        
        return []


