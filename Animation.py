import threading
import time
import random

current_anim = None
stop = False
animations = ["◤◥◢◣","-\\|/","◓◑◒◐","◶◵◴◷","◸◹◿◺","◇◈◆◈","←↖↑↗→↘↓↙","⇑⇗⇒⇘⇓⇙⇐⇖","▥▧▤▨","→⇒⇛⇒","⁎⁑⁂⁑","․‥…‥","·⁚⁝⁛⁙","◜◝◞◟","⊗⊕","ↀↂↈↂ"]

def start_wait_anim(count: list, total: int):
    global current_anim
    current_anim = threading.Thread(target=waiting_anim, name="AnimThread", kwargs={"count": count,"total": total})
    current_anim.start()

def join_anim():
    global stop
    stop = True
    current_anim.join()

def waiting_anim(count: list, total: int):
    global stop
    animation = random.choice(animations)
    idx = 0

    print(f"\r{animation[idx % len(animation)]} | lines done : {count[0]} / {total} ", end="")

    while count[0] != total and not stop:
        time.sleep(0.1)
        idx += 1
        print(f"\r{animation[idx % len(animation)]} | lines done : {count[0]} / {total} ", end="")
    print()