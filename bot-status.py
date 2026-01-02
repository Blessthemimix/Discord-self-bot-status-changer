import discord
from discord.ext import tasks
import asyncio
import random

# Вставь сюда свой токен
TOKEN = 'TOKEN'

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_index = 0
        
        # Список твоих статусов с ID эмодзи
        self.statuses = [
            {
                "text": "worker, trust me.", 
                "emoji_name": "microsoft", 
                "emoji_id": 904792337606144022,
                "animated": False
            },
            {
                "text": "developer, for rice.", 
                "emoji_name": "github", 
                "emoji_id": 904792338512105523,
                "animated": False
            },
            {
                "text": "status by mimix :)", 
                "emoji_name": "aorange_2", 
                "emoji_id": 1116795122265378846,
                "animated": False #Если оно будет анимированное пишешь TRUE
            }
        ]

    async def on_ready(self):
        print(f'Бот успешно запущен на аккаунте: {self.user}')
        if not self.change_status.is_running():
            self.change_status.start()

    @tasks.loop(seconds=60)
    async def change_status(self):
        current = self.statuses[self.status_index]
        
        # Формируем объект эмодзи для Discord
        emoji_obj = discord.PartialEmoji(
            name=current["emoji_name"], 
            id=current["emoji_id"], 
            animated=current["animated"]
        )
        
        try:
            # Установка "Custom Status" (именно тот, что в редакторе профиля)
            await self.change_presence(
                activity=discord.CustomActivity(name=current["text"], emoji=emoji_obj),
                status=discord.Status.online
            )
            print(f'>>> Статус обновлен: {current["emoji_name"]} | {current["text"]}')
            
            # Переход к следующему статусу
            self.status_index = (self.status_index + 1) % len(self.statuses)
            
            # Рандомизация интервала (от 55 до 75 секунд), чтобы не выглядеть как робот
            new_wait = random.randint(55, 75)
            self.change_status.change_interval(seconds=new_wait)
            
        except Exception as e:
            print(f'Ошибка при обновлении статуса: {e}')

client = MyClient()

# Запуск
try:
    client.run(TOKEN)
except discord.LoginFailure:
    print("Ошибка: Неверный токен! Проверь его еще раз.")
except Exception as e:
    print(f"Произошла ошибка при запуске: {e}")
