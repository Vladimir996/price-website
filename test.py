import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import json

TOKEN = '7415903848:AAEoQ5jVnhXxEQgp4RbAfBddGEM5tIA_Qpw'
CHAT_ID = '6890676641'


async def get_price(url, price_id, name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
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


async def send_message(bot, message):
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def main():
    bot = Bot(token=TOKEN)
    
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


if __name__ == '__main__':
    asyncio.run(main())
