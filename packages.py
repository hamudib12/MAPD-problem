class Package:

    AVAILABLE = 0
    PICKED_UP = 1
    DELIVERED = 2

    def __init__(self, x, y, time, d_x, d_y, d_time):
        self.x = x
        self.y = y
        self.s_time = time
        self.d_x = d_x
        self.d_y = d_y
        self.d_time = d_time
        self.status = Package.AVAILABLE  # 0 for available, 1 for pickup, 2 for delivered

    def is_available(self, curr_time):
        return (self.s_time <= curr_time <= self.d_time) and self.status == Package.AVAILABLE

    def mark_as_picked_up(self):
        if self.status == Package.AVAILABLE:
            self.status = Package.PICKED_UP

    def mark_as_delivered(self):
        if self.status == Package.PICKED_UP:
            self.status = Package.DELIVERED

    def check_picked_up(self):
        return self.status == Package.PICKED_UP

    def arrive(self, x, y):
        return self.d_x == x and self.d_y == y

    def check_if_delivered(self):
        return self.status == Package.DELIVERED



