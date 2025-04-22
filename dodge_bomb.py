import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
# 画面のサイズ
DELTA = {
    pg.K_UP:    (0,-5),
    pg.K_DOWN:  (0,+5),
    pg.K_LEFT:  (-5,0),
    pg.K_RIGHT: (+5,0),
}
# 辞書の定理

# 飛ぶ方向の切り替え
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """"
    引数：こうかとんRectかばくだんRect
    戻り値:タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue、画面外ならFalse

    """
    yoko, tate = True, True
    # 縦横方向判定
    if rct.left < 0 or WIDTH < rct.right: # 画面外の話
       yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom :
        tate =False  
    return yoko, tate


# gameoverの表示
def gameover(screen: pg.Surface.set_alpha) -> None:
    screen = pg.display.set_mode((1100, 650))
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True, (255, 255, 255))
    kkc_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0, 0.9)
    #black_img = pg.Rect(1600,900)
    screen.blit(txt,[250, 200])
    screen.blit(kkc_img,[200, 200])
    screen.blit(kkc_img,[600, 200])
    #screen.blit(black_img)
    pg.display.update()
    time.sleep(5)
# 爆弾を変化
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_accs = [a for a in range(1,11)]
    for r in range (1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
# こうかとんの向きを変える
def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    key_lst = pg.key.get_pressed()
    sum_mv = [0, 0]
    for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #上下方向
                sum_mv[1] += mv[1] #左右方向
                return

# 追従型   
# メインコード
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    #kk_img = get_kk_img((0,0))
    #kk_img = get_kk_img(tuple(sum_mv))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # ↓爆弾の描写
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH),random.randint(0,HEIGHT)
    bb_img.set_colorkey((0, 0, 0))  # 色黒
    vx,vy = +5,+5 # 爆弾の速さ
    
    
    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #上下方向
                sum_mv[1] += mv[1] #左右方向
       

      #  if key_lst[pg.K_UP]:
      #      sum_mv[1] -= 5
      #  if key_lst[pg.K_DOWN]:
      #      sum_mv[1] += 5
      #  if key_lst[pg.K_LEFT]:
      #      sum_mv[0] -= 5
      #  if key_lst[pg.K_RIGHT]:
      #      sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)         # 爆弾の移動
        yoko, tate =check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1    
        screen.blit(bb_img, bb_rct)   # 爆弾の表示
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
