import pyxel
import random

class Sumaho:
    def __init__(self):
        # プレイヤーの初期位置
        self.player_x = 9
        self.player_y = 103

        # プレイヤーの4つの角の位置をリストで管理
        self.player_positions = [
            (self.player_x, self.player_y),  # 左上
            (self.player_x + 14, self.player_y),  # 右上
            (self.player_x + 14, self.player_y + 16),  # 右下
            (self.player_x, self.player_y + 16),  # 左下
        ]

        # スタート
        #self.start = False

        # 得点
        self.point = 0

    def move(self, dx, dy):
        # 移動先の座標をリストに代入
        new_positions = [
            (self.player_positions[0][0] + dx, self.player_positions[0][1] + dy),
            (self.player_positions[1][0] + dx, self.player_positions[1][1] + dy),
            (self.player_positions[2][0] + dx, self.player_positions[2][1] + dy),
            (self.player_positions[3][0] + dx, self.player_positions[3][1] + dy),
        ]

        # 四隅で移動判定
        for i in range(4):
            if App.is_tile_obstacle(new_positions[i][0] // 8, new_positions[i][1] // 8):
                break
            # ４回目まで行けたら更新
            if i == 3:
                for j in range(4):
                    self.player_positions[j] = new_positions[j]

class Enemy:
    def __init__(self):
        # 敵の初期位置
        self.enemy_x = 103
        self.enemy_y = 9
        self.speed = 1

        # 四隅
        self.enemy_positions = [
            (self.enemy_x, self.enemy_y),  # 左上
            (self.enemy_x + 16, self.enemy_y),  # 右上
            (self.enemy_x + 16, self.enemy_y + 16),  # 右下
            (self.enemy_x, self.enemy_y + 16),  # 左下
        ]
        # 敵の進行方向
        self.direction = (-1, 0)

    def move(self, dx, dy):
        # 移動先の座標をリストに代入
        new_enemy_positions = [
            (self.enemy_positions[0][0] + dx, self.enemy_positions[0][1] + dy),
            (self.enemy_positions[1][0] + dx, self.enemy_positions[1][1] + dy),
            (self.enemy_positions[2][0] + dx, self.enemy_positions[2][1] + dy),
            (self.enemy_positions[3][0] + dx, self.enemy_positions[3][1] + dy),
        ]

        # 四隅で移動判定
        for k in range(4):
            if App.is_tile_obstacle(new_enemy_positions[k][0] // 8, new_enemy_positions[k][1] // 8):
                print("Enemy hit obstacle")
                # 方向転換
                self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                break
            
            # ４回目まで行けたら更新
            if k == 3:
                for l in range(4):
                    self.enemy_positions[l] = new_enemy_positions[l]
            
            
            

class App:
    def __init__(self):
        pyxel.init(128, 128)

        self.sumaho = Sumaho()
        self.enemy = Enemy()
        
        self.gameover_flag = False
        self.clear_flag = False


        # タイルマップ呼び出し
        pyxel.load("sumaho.pyxres")
        pyxel.run(self.update, self.draw)
        
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            #リスタート
            pyxel.load("sumaho.pyxres")
            self.sumaho = Sumaho()
            self.enemy = Enemy()
            self.gameover_flag = False
            self.clear_flag = False
            self.sumaho.point = 0
            
        if not self.gameover_flag or not self.clear_flag:
            self.update_sumaho()
            self.update_wifi(self.sumaho.player_positions[0][0], self.sumaho.player_positions[0][1])
            self.update_enemy()
            if self.chase(self.sumaho, self.enemy):
                self.gameover_flag = True
            if self.sumaho.point == 32:
                self.clear_flag = True
            if self.gameover_flag or self.clear_flag:
                #lambdaでdy、dxを受け取って動けなくする
                self.sumaho.move = lambda dx, dy: None
                self.enemy.move = lambda dx, dy: None
            
        

    def draw(self):
        pyxel.cls(0)
        # map
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        # sumaho
        pyxel.blt(self.sumaho.player_positions[0][0],self.sumaho.player_positions[0][1],0,49,0,14,16)
        print(self.sumaho.point)
        # enemy
        pyxel.blt(self.enemy.enemy_positions[0][0],self.enemy.enemy_positions[0][1],0,32,16,16,16,13)
        
        pyxel.text(50,121,"internet speed",7)
        if self.sumaho.point < 8:
            pyxel.rectb(124, 119, 2, 8, 7)
            pyxel.rectb(120, 121, 2, 6, 7)
            pyxel.rectb(116, 123, 2, 4, 7)
            pyxel.rectb(112, 125, 2, 2, 7)
        elif 8 <= self.sumaho.point < 16:
            pyxel.rectb(124, 119, 2, 8, 7)
            pyxel.rectb(120, 121, 2, 6, 7)
            pyxel.rectb(116, 123, 2, 4, 7)
            pyxel.rectb(112, 125, 2, 2, 12)
        elif 16 <= self.sumaho.point < 24:
            pyxel.rectb(124, 119, 2, 8, 7)
            pyxel.rectb(120, 121, 2, 6, 7)
            pyxel.rectb(116, 123, 2, 4, 12)
            pyxel.rectb(112, 125, 2, 2, 12)
        elif 24 <= self.sumaho.point < 32:
            pyxel.rectb(124, 119, 2, 8, 7)
            pyxel.rectb(120, 121, 2, 6, 12)
            pyxel.rectb(116, 123, 2, 4, 12)
            pyxel.rectb(112, 125, 2, 2, 12)

        else:
            pyxel.rectb(124, 119, 2, 8, 12)
            pyxel.rectb(120, 121, 2, 6, 12)
            pyxel.rectb(116, 123, 2, 4, 12)
            pyxel.rectb(112, 125, 2, 2, 12)

        if self.sumaho.point == 32:
            pyxel.cls(0)
            pyxel.text(100,64,"CLEAR",7)
            pyxel.rectb(57, 61, 2, 8, 12)
            pyxel.rectb(61, 63, 2, 6, 12)
            pyxel.rectb(65, 65, 2, 4, 12)
            pyxel.rectb(69, 67, 2, 2, 12)
            pyxel.text(40,80,"R=Restart",7)
            
            

        if self.gameover_flag:
            pyxel.cls(0)
            pyxel.text(64, 64, "GAME OVER.", 6)
            pyxel.text(64,80,"R=Restart",7)
            

    def update_wifi(self, x, y):
        # wifiなら2,2に書き換え
        if pyxel.tilemap(0).pget(self.target_x, self.target_y) == (0, 2) :
            self.sumaho.point += 1
            pyxel.tilemap(0).pset(self.target_x, self.target_y, (2, 2))

    def update_sumaho(self):
        if not self.gameover_flag or not self.clear_flag:
        # 現在地のタイル単位の座標
            self.target_x = self.sumaho.player_positions[0][0] // 8
            self.target_y = self.sumaho.player_positions[0][1] // 8

        # 操作の設定
            if (pyxel.btn(pyxel.KEY_UP) and not self.is_tile_obstacle(self.target_x, self.target_y - 1)):
                 self.sumaho.move(0, -1)
            elif (pyxel.btn(pyxel.KEY_DOWN) and not self.is_tile_obstacle(self.target_x, self.target_y + 1)):
                 self.sumaho.move(0, 1)
            elif (pyxel.btn(pyxel.KEY_LEFT) and not self.is_tile_obstacle(self.target_x - 1, self.target_y)):
                self.sumaho.move(-1, 0)
            elif (pyxel.btn(pyxel.KEY_RIGHT) and not self.is_tile_obstacle(self.target_x + 1, self.target_y)):
                self.sumaho.move(1, 0)

    def update_enemy(self):
        if not self.gameover_flag or not self.clear_flag:
        # 移動処理
            self.enemy.move(self.enemy.direction[0] , self.enemy.direction[1] )

    def chase(self, sumaho, enemy):
        chase_x = sumaho.player_positions[0][0] - enemy.enemy_positions[0][0]
        chase_y = sumaho.player_positions[0][1] - enemy.enemy_positions[0][1]
        # 左上以外でも判定出るようにする！
        if -16 < chase_x < 16 and -16 < chase_y < 16:
            return True
        else:
            return False

    #第一引数(self)を受け取らないやつ
    @staticmethod
    def is_tile_obstacle(x, y):
        # タイルが色14であれば障害物があると判断
        if pyxel.tilemap(0).pget(x, y) == (0, 0):
            return True
        else:
            return False


App()
