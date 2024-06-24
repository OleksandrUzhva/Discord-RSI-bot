import discord
from discord.ext import tasks, commands
from pybit.unified_trading import HTTP
import numpy as np
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True  
client = commands.Bot(command_prefix="!", intents=intents)

def fetch_bybit_klines(symbol="SOLUSD", interval='60', start=None, end=None):
    session = HTTP(testnet=True)
    data = session.get_kline(
        category="inverse",  
        symbol=symbol,
        interval=interval,
        start=start,
        end=end,
        limit=1000  
    )
    if data['retCode'] == 0:
        return data['result']['list']
    else:
        raise ValueError(f"Failed to fetch kline data: {data['retMsg']}")


def calculate_rsi(data, period=14):
    if len(data) < period:
        raise ValueError("Insufficient data points to calculate RSI")

    closes = np.array([float(item[4]) for item in data]) 
    deltas = np.diff(closes)
    
    up = np.maximum(0, deltas)
    down = np.maximum(0, -deltas)
    
    avg_gain = np.mean(up[:period])
    avg_loss = np.mean(down[:period])
    
    rsi_values = []
    
    if avg_loss == 0:
        rs = np.inf  
    else:
        rs = avg_gain / avg_loss
    
    if rs > 0:
        rsi = 100 - (100 / (1 + rs))
    else:
        rsi = 100 
    
    rsi_values.append(rsi)
    
    for delta in deltas[period:]:
        avg_gain = (avg_gain * (period - 1) + delta) / period
        avg_loss = (avg_loss * (period - 1) - delta) / period
        
        if avg_loss == 0:
            rs = np.inf  
        else:
            rs = avg_gain / avg_loss
        
        if rs > 0:
            rsi = 100 - (100 / (1 + rs))
        else:
            rsi = 100  
        
        rsi_values.append(rsi)
        
    return rsi_values


async def send_discord_message(channel_id, message):
    channel = client.get_channel(channel_id)
    await channel.send(message)

@tasks.loop(minutes=60)
async def fetch_and_check_rsi():
    try:
        data = fetch_bybit_klines(symbol="SOLUSD", interval='60')
        rsi_values = calculate_rsi(data)
        
        if rsi_values:
            last_rsi = rsi_values[-1]  
            if last_rsi > 70:
                await send_discord_message(CHANNEL_ID, f"RSI higher than 70: {last_rsi:.2f}")
            elif last_rsi < 30:
                await send_discord_message(CHANNEL_ID, f"RSI lower than 30: {last_rsi:.2f}")
        else:
            print("No valid RSI data available.")

    except ValueError as x:
        print(f"Error calculating RSI: {x}")

@client.event
async def on_ready():
    fetch_and_check_rsi.start()

client.run(DISCORD_TOKEN)
