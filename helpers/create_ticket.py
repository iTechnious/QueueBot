import random
import time

from globals import tickets


def run(member):
    ticket_id = 0

    while ticket_id == 0:
        ticket_id = random.getrandbits(32)
        for item in tickets.keys():
            if tickets[item]["id"] == ticket_id:
                ticket_id = 0

    tickets[member.id] = {
        "id": ticket_id,
        "guild": member.guild.id,
        "time": time.time()
    }
