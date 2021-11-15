"""User Class"""


class Client:
    def __init__(self, chat_ip):
        self.chat_ip = chat_ip
        self.total = 0

    def addition(self, new_sum):
        """Add new cost to total.
        new cost: cost, which will be added
        """
        self.total += new_sum
