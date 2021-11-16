"""User Class"""


class Client:
    # make with database in future
    price_list = {'30m': 0.90, '30m_s': 0.45,
                  '60m': 1.30, '60m_s': 0.65}

    def __init__(self, chat_ip):
        self.chat_ip = chat_ip
        self.total = 0
        self.start_road_time = None  # start - use for count time of road
        self.last_road = None        # list of prices of last road and time, for confirm menu

    def add_to_total(self, new_sum):
        """Add new cost to total.
        :param new_sum: cost, which will be added
        """
        self.total += new_sum

    def count_price(self, minutes):
        """Count price for the road.
        :param minutes: time, spent for road
        :return: all possible prices
        """

        if minutes <= 30:
            return self.price_list['30m'], self.price_list['30m_s']
        elif 30 < minutes <= 60:
            return self.price_list['60m'], self.price_list['60m_s']

    def count_time(self, end_road_time):
        """Count how many minutes were spent in road
        :param end_road_time: time of the road's end
        :return: minutes"""

        if self.start_road_time[0] <= end_road_time[0]:  # add check for date
            minutes_spent = 60 * (end_road_time[0] - self.start_road_time[0]) \
                            + (end_road_time[1] - self.start_road_time[1])

            self.start_road_time = None
            return minutes_spent
