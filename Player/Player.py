class Player():
    def __init__(self, user, id) -> None:
        self.user = user
        self.id = id
        self.is_vampire = False
        self.is_dracula = False
        self.is_hero = True
    
    async def send(self, message, view=None) -> None:
        message = f"Player {self.id}:\n" + message
        await self.user.send(message, view=view)

    def parseCardAsNarrator(self, card, is_blind=False) -> str:
        message = ""
        if card.is_luck:
            message += "Luck"
        else:
            message += "Curse"
        
        if is_blind and not card.is_always_visible:
            return message

        if card.boon:
            message += f" Boon: {card.boon}"
        elif card.bane:
            message += f" Bane: {card.bane}"

        return message
    
    def parseCardAsAuthor(self, card, is_blind=False) -> str:
        message = ""
        if card.is_luck:
            message += "Luck"
        else:
            message += "Curse"
        
        if is_blind:
            return message

        if card.boon:
            message += " (Boon)"
        elif card.bane:
            message += " (Bane)"

        return message