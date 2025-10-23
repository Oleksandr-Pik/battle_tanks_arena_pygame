class Game():
    def __init__(self):
        try:
            with open("hiscore.txt", "r") as file:
                hiscore = file.read().strip()
                self.hiscore = int(hiscore)
        except(FileNotFoundError):
            self.hiscore = 100
        self.score = 0
        self.enemy_count = 30
        self.max_tanks_quantity = 5
        self.max_detection_distance = 400
        self.running = True
        self.menu_running = False
        self.is_gameover = False
        self.paused_music = False
        self.stage = 1
        self.timer = 0
        self.bonus_timer = 180
        self.title_y = 0
        self.usertanks = []
        self.bullets = []
        self.bullets_enemy = []
        self.my_tank = None


    def new_stage(self):
        self.timer = 0
        self.stage += 1
        self.enemy_count = 30
        self.max_tanks_quantity = 5
        self.title_y = 0
        # self.usertanks = []
        self.bullets.clear()
        self.bullets_enemy.clear()
