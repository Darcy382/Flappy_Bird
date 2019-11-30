import random

class Post:
    def __init__(self, post_num, width=400, post_gap=150):
        self.post_num = post_num
        self.width = width
        self.post_gap=150
        bottom = random.randint(200, 500)
        self.bottom_y = bottom
        self.top_y = bottom - self.post_gap - 500
        self.postx = width

    def move_post(self, speed):
        self.postx -= speed

    def reset(self):
        bottom = random.randint(200, 500)
        self.bottom_y = bottom
        self.top_y = bottom - self.post_gap - 500
        self.postx = 400

    @property
    def top_tup(self):
        return (self.postx, self.top_y)

    @property
    def bottom_tup(self):
        return (self.postx, self.bottom_y)
