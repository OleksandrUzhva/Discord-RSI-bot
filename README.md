# Discord RSI Bot

## Description
A Discord bot that fetches SOL/USDT K-line data from Bybit, calculates RSI, and sends a message to a Discord channel if RSI is over 70 or below 30.

## Setup

### Prerequisites
- Docker
- Discord Bot Token
- Bybit API

### Steps
1. Clone the repository:

    git clone git@github.com:OleksandrUzhva/Discord-RSI-bot.git

2. Create a `.env` file and add your Discord token and channel ID:
        env
    DISCORD_TOKEN = your_discord_token
    CHANNEL_ID = your_channel_id

3. Build the Docker image:
        bash
    docker compose build 

4. Run the Docker container:
        bash
    docker compose up -d 
    