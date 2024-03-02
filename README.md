BramBot is a Discord bot designed to help manage the deck for the game BloodMoon. Currently, several tokens and real world items are needed in order to successfully play the game


## Installation guide:
### No Docker
This bot was programmed and tested using python 3.10.4
Run `py main.py`

### Using Docker
1. Checkout repository
2. run `docker build -t bloodmoon-bot .`
3. run `docker run -rm bloodmoon-bot`
    - Note: this will remove the container after it's done running. If you want to keep the container use `docker run -d bloodmoon-bot`