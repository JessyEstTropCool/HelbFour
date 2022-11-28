import threading
import time
import random

animations = ["◤◥◢◣","-\\|/","◓◑◒◐","◶◵◴◷","◸◹◿◺","◇◈◆◈","←↖↑↗→↘↓↙","⇑⇗⇒⇘⇓⇙⇐⇖","▥▧▤▨","→⇒⇛⇒","⁎⁑⁂⁑","․‥…‥","·⁚⁝⁛⁙","◜◝◞◟"]

def start_wait_anim(count: list, total: int):
    threading.Thread(target=waiting_anim, name="AnimThread", kwargs={"count": count,"total": total}).start()

def waiting_anim(count: list, total: int):
    animation = random.choice(animations)
    idx = 0
    while count[0] != total:
        print(f"\r{animation[idx % len(animation)]} | lines done : {count[0]} / {total} ", end="")
        idx += 1
        time.sleep(0.1)

    print(f"\r{animation[idx % len(animation)]} | lines done : {count[0]} / {total} ")