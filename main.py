import os
from time import sleep

import requests
from dotenv import load_dotenv


load_dotenv()


def get_data():
    r = requests.get('https://vitemadose.gitlab.io/vitemadose/92.json')
    if r.status_code == 200:
        return r.json()


def push_notifications(message):
    requests.post("https://api.pushover.net/1/messages.json", data=({
        "token": os.getenv("TOKEN"),
        "user": os.getenv("USER_TOKEN"),
        "message": message,
    }))


def main():
    while True:
        data = get_data()

        if data:
            available_centers = data.get('centres_disponibles')

            for center in available_centers:
                center_name = center.get('nom')
                appointment_url = center.get('url')

                appointment_schedules = center.get('appointment_schedules')

                for appointment_schedule in appointment_schedules:
                    appointment_type = appointment_schedule.get('name')

                    if appointment_type != "chronodose":
                        continue
                    doses = appointment_schedule.get("total")

                    if doses > 0:
                        message = f"{center_name}: {doses} dose(s).\
                        Prendre rendez-vous: {appointment_url}"
                        push_notifications(message)
                        print(message)

        print("Fin de la vérif")
        sleep(600)


if __name__ == "__main__":
    main()
