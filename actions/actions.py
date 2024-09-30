import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCallLlamaAPI(Action):
    def name(self):
        return "action_call_llama_api"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Mengambil input pengguna
        user_input = tracker.latest_message.get('text')

        # Memanggil API LM Studio
        url = "http://localhost:1234/v1/completions"
        payload = {
            "model": "LLaMA-3.1",
            "prompt": user_input,
            "max_tokens": 100,
            "temperature": 0.7
        }

        response = requests.post(url, json=payload)

        # Mengirim respons chatbot
        if response.status_code == 200:
            result = response.json().get("choices", [{}])[0].get("text", "")
            dispatcher.utter_message(text=result)
        else:
            dispatcher.utter_message(text="Maaf, saya tidak dapat menjawab saat ini.")

        return []
