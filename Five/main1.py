## 调用pygame库
import pygame
import sys
##
## 调用常用关键字常量
from pygame.locals import QUIT, KEYDOWN
import numpy as np
import os
import time
from playsound import playsound
##
##画布尺寸
display_width = 1000
display_height = 720
##
##颜色宏
WHITE = (255, 255, 255)
BLACK=(0,0,0)
RED = (255, 0, 0)
YELLOW = (221, 177, 0)
BLUE = (0,155,160)
##
## 初始化pygame
pygame.init()
pygame.mixer.init()
##
## 获取对显示系统的访问，并创建一个窗口screen
screen = pygame.display.set_mode((1000, 720))# 窗口大小为900*720
screen_color = [200, 150, 72]  # 设置画布颜色,[238,154 ,73]对应为棕黄色
line_color = [0, 0, 0]  # 设置线条颜色，[0,0,0]对应黑色
##
##设置字体
font_name = pygame.font.match_font('fangsong')  # 2.获得字体文件
font = pygame.font.Font(font_name, 36)  # 1.获取font对象（需要字体文件）
##
ROOT_DIRECTORY = os.getcwd()##找到根目录
##
##播放路径
bg_music_path = ROOT_DIRECTORY+"/Music"+"/bg.mp3"
click_music_path = ROOT_DIRECTORY+"/Music"+"/click.mp3"
over_music_path = ROOT_DIRECTORY+"/Music"+"/over.mp3"
pos_music_path = ROOT_DIRECTORY+"/Music"+"/pos.mp3"
##
##音乐导入
###播放背景音乐
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.play(-1,0)
###音效
click_sound=pygame.mixer.Sound(click_music_path)#按键音效
over_sound=pygame.mixer.Sound(over_music_path)#游戏结束音效
pos_sound=pygame.mixer.Sound(pos_music_path)#落子音效
###
###yi
##
#按钮类
class Button(object):#定义按钮
    def __init__(self, text, color,backgroundcolor, x, y):
        self.color=color
        self.text=text
        self.surface = font.render(text, True, color,backgroundcolor)#render返回的是一个surface对象
        #获取按钮长宽，长宽在设置字号的时候就已经自动配置好了
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        self.x = x
        self.y = y
    #显示按钮
    def display(self):
        #blit在主屏幕上显示surface对象
        screen.blit(self.surface, (self.x, self.y))
    #把按钮颜色设置为跟棋盘一样，隐藏按钮
    def hide(self):
        self.surface = font.render(self.text, True, screen_color,screen_color)#透明
        screen.blit(self.surface, (self.x, self.y))
    #判断鼠标有没有在按钮上
    def check_click(self, position,bg_color=BLUE): ##传入按钮背景颜色bG_color
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT
        #判断有没有点击
        if x_match and y_match:
            keys_pressed = pygame.mouse.get_pressed()  # 获取鼠标按键信息,用来判断按钮有没有被点击，放上去按钮变蓝色
            if keys_pressed[0]:
                self.surface = font.render(self.text, True, self.color, YELLOW)
                screen.blit(self.surface, (self.x, self.y))
                #清屏，重新绘制网格，棋子在主函数重新画
                screen.fill(screen_color)  # 清屏
                _draw_line()
                click_sound.play()
                #返回1确认点击了按钮
                return 1
            else:
                self.surface = font.render(self.text, True, self.color, bg_color)
                screen.blit(self.surface, (self.x, self.y))
                #返回2只是鼠标放上去，没有点击
                return 2

        else:
            return 0

def check_win(over_pos):  # 判断五子连心
    mp = np.zeros([15, 15], dtype=int)
    for val in over_pos:
        x = int((val[0][0] - 27) / 44)
        y = int((val[0][1] - 27) / 44)
        if val[1] == WHITE:
            mp[x][y] = 2  # 表示白子
        else:
            mp[x][y] = 1  # 表示黑子

    for i in range(15):
        pos1 = []##分别存储黑色、白色
        pos2 = []
        for j in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:  # 五子连心
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]

    for j in range(15):
        pos1 = []
        pos2 = []
        for i in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i + k >= 15 or j + k >= 15:
                    break
                if mp[i + k][j + k] == 1:
                    pos1.append([i + k, j + k])
                else:
                    pos1 = []
                if mp[i + k][j + k] == 2:
                    pos2.append([i + k, j + k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i + k >= 15 or j - k < 0:
                    break
                if mp[i + k][j - k] == 1:
                    pos1.append([i + k, j - k])
                else:
                    pos1 = []
                if mp[i + k][j - k] == 2:
                    pos2.append([i + k, j - k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    return [0, []]
def find_pos(x, y):  # 找到显示的可以落子的位置
    for i in range(27, 670, 44):
        for j in range(27, 670, 44):
            L1 = i - 22
            L2 = i + 22
            R1 = j - 22
            R2 = j + 22
            if x >= L1 and x <= L2 and y >= R1 and y <= R2:
                return i, j
    return x, y
def check_over_pos(x, y, over_pos):  # 检查当前的位置是否已经落子
    for val in over_pos:
        if val[0][0] == x and val[0][1] == y:
            return False
    if x>692 or y>692:#670+22
            return False
    return True  # 表示没有落子
def _draw_line():
    for i in range(27, 670, 44):
        # 先画竖线
        if i == 27 or i == 670 - 27:  # 边缘线稍微粗一些
            pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 4)
        else:
            pygame.draw.line(screen, line_color, [i, 27], [i, 670 - 27], 2)
        # 再画横线
        if i == 27 or i == 670 - 27:  # 边缘线稍微粗一些
            pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 4)
        else:
            pygame.draw.line(screen, line_color, [27, i], [670 - 27, i], 2)


over_pos = []  # 表示已经落子的位置,收集棋的位置信息和颜色信息

while True:  # 不断训练刷新画布

    for event in pygame.event.get():  # 获取事件，如果鼠标点击右上角关闭按钮，关闭
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    screen.fill(screen_color)  # 清屏
    _draw_line()
    # 在棋盘中心画个小圆表示正中心位置
    pygame.draw.circle(screen, line_color, [27 + 44 * 7, 27 + 44 * 7], 8, 0)
    Restart_button = Button('重新开始', RED,WHITE,700,100 )
    black_play_button = Button('黑色方落子中', RED, None, 700, 300)
    white_play_button = Button('白色方落子中', RED, None, 700, 300)
    Win_black_button = Button('黑色方胜利', RED, None, 700, 300)
    Win_white_button = Button('白色方胜利', RED, None, 700, 300)
    Regret_button = Button('悔棋', RED,WHITE,700,500)
    Restart_button.display()##显示按钮
    Regret_button.display()
    for val in over_pos:  # 显示所有落下的棋子
        pygame.draw.circle(screen, val[1], val[0], 20, 0)
    x, y = pygame.mouse.get_pos()#获取鼠标物理位置
    x, y = find_pos(x, y)##找到能落点的位置
    if Restart_button.check_click((x,y))==1:##如果按下重新开始，列表元素被删除，清屏在类的静态函数check_click（（x，y））里面使用了
        over_pos = []
        time.sleep(0.3)
    res = check_win(over_pos)# 判断是否存在五子连心
    if over_pos==[]:
        play_sound_flag=0#胜利胜利音效播放次数标志,当场上无棋子时重新填充为0
    if res[0] != 0:#五子连心
        if play_sound_flag==0:
            play_sound_flag=1
            over_sound.play()
        black_play_button.hide()#游戏结束时不显示“落子中“
        white_play_button.hide()
        if res[0]==1:#黑色获胜，返回res的第0项为1
            Win_black_button.display()
        if res[0]==2:#白色获胜，返回res的第0项为2
            Win_white_button.display()
        for pos in res[1]:
            #把连线的五子框起来
            pygame.draw.rect(screen, [238, 0, 0], [pos[0] * 44 + 27 - 22, pos[1] * 44 + 27 - 22, 44, 44], 2)#五子框起来
        # Playing_button.hide()
        pygame.display.update()  # 刷新显示
        continue  # 游戏结束，停止下面的操作
    #按钮显示或隐藏设置
    Win_black_button.hide()
    Win_white_button.hide()
    # 获取鼠标坐标信息
    if Regret_button.check_click((x, y))==1:
        length=len(over_pos)
        print(length)
        time.sleep(0.3)
        del over_pos[length-1]
    if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再显示
        pygame.draw.rect(screen, [0, 80, 238], [x - 22, y - 22, 44, 44], 2)
    keys_pressed = pygame.mouse.get_pressed()  # 获取鼠标按键信息
    # 鼠标左键表示落黑色子
    length_pos=len(over_pos)
    if len(over_pos) % 2 == 0:
        white_play_button.hide()
        black_play_button.display()
    else:
        black_play_button.hide()
        white_play_button.display()
    if keys_pressed[0]:
        # flag = True
        if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再落子
            pos_sound.play()#落子音效
            if len(over_pos) % 2 == 0:  # 黑子
                over_pos.append([[x, y], BLACK])
            else:
                pass
    # 鼠标右键表示落白色子
    if keys_pressed[2]:
        # flag = True
        if check_over_pos(x, y, over_pos):  # 判断是否可以落子，再落子
            pos_sound.play()
            if len(over_pos) % 2 == 0:  # 黑子
                pass
            else:
                over_pos.append([[x, y], WHITE])  # 白子
    pygame.display.update()  # 刷新显示
