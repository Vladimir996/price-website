import requests
from bs4 import BeautifulSoup
from telegram import Bot
import json
import schedule
import time
import os

# TOKEN = '7415903848:AAEoQ5jVnhXxEQgp4RbAfBddGEM5tIA_Qpw'
# CHAT_ID = '6890676641'

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# Asinhrona funkcija za preuzimanje trenutne cene sa web stranice
async def get_price(url, price_id, name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Provera da li je zahtev uspeo
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Pronalaženje cena koristeći specifični ID
        price_tag = soup.find(id=price_id)
        
        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Greška prilikom zahteva za cenu na {url}: {e}")
        return None
    
    except Exception as e:
        print(f"Nepredviđena greška prilikom preuzimanja cene na {url}: {e}")
        return None

# Asinhrona funkcija za slanje poruke putem Telegram bota
async def send_message(bot, message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Asinhrona glavna funkcija
async def main():
    bot = Bot(token=TOKEN)
    
    # Učitavanje konfiguracionih podataka iz JSON datoteke
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    
    for item in config_data:
        url = item.get('url')
        price_id = item.get('price_id')
        name = item.get('name')
        
        if url and price_id:
            current_price = await get_price(url, price_id, name)
            
            if current_price:
                message = f"Cena za {name} je: {current_price}"
                await send_message(bot, message)
            else:
                error_message = f"Došlo je do greške prilikom preuzimanja cene sa {url}."
                await send_message(bot, error_message)
        else:
            print(f"Neispravni podaci u konfiguraciji: {item}")

# Funkcija za pokretanje main() funkcije svaki dan u 14:00
def run_daily():
    schedule.every().day.at("14:00").do(asyncio.run, main())

if __name__ == '__main__':
    import asyncio
    
    # Pokretanje funkcije run_daily() koja će pokrenuti main() svaki dan u 14:00
    run_daily()
    
    # Beskonačna petlja za izvršavanje schedule zadatka
    while True:
        schedule.run_pending()
        time.sleep(60)  # Provera svaki minut
