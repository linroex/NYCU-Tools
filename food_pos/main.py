import json
import re

from datetime import datetime
from glob import glob
from os import path

folder = path.dirname(path.realpath(__file__))

def clear():
    from os import system, name as os_name
    system('cls' if os_name == 'nt' else 'clear')

def save_db(user_db_f, user_db):
    user_db_f.seek(0)
    user_db_f.truncate()
    user_db_f.write(json.dumps(user_db))

_action = ""

products = {}
with open("products.json", "r", encoding="utf8") as prod_f:
    products = json.loads(prod_f.read())

while True:
    clear()
    user = input("請輸入你的 CC ID： ").strip()
    if not user.isalnum():
        print('請重新輸入。\n')
        continue
    user_db_path = f'{folder}/data/{user}.json'
    
    # check user exists
    if len(glob(user_db_path)) == 0:
        print('\n{} 您似乎是第一次使用該程式？'.format(user))
        choose = (input('若確認 CC ID 無誤請輸入 Y (default=N)： ') or 'N').upper().strip()
        
        if choose == 'Y':
            with open(user_db_path, 'w', encoding='utf8') as f:
                f.write(json.dumps({
                    'user': user,
                    'created_at': datetime.now().timestamp(),
                    'transactions': []
                }))
                print('已成功建立帳號。\n')
                
        elif choose == 'N':
            print('請重新輸入。\n')
            continue
    
    while True:
        with open(user_db_path, 'r+', encoding='utf8') as user_db_f:
            user_db = json.loads(user_db_f.read())

            total = 0
            for transaction in user_db['transactions']:
                if transaction['deleted_at'] is None:
                    total += transaction['amount']

            prod_name = ""
            amount = 0

            if _action == "":
                clear()
                print('\n=====功能選單=====\n購物： \t\t\tdefault\n計算未結金額： \t\ts\n結帳： \t\t\tc\n離開： \t\t\tq\n')
                cmd = input(f'\n({user}: {total}) 請輸入購物金額（或掃描條碼）： ')
            else:
                cmd = _action
                _action = ""

            if cmd == "q":
                break

            if cmd in ("s", "c"):
                
                print(f'\n您目前的未結金額： {total}\n')
            
                if cmd == 'c':
                    input('若要結帳，請將上列金額放到零錢區，完成後請按 Enter。')
                    if input('我已經把錢放到零錢區（Y/N）： ').upper().strip() == 'Y':
                        
                        # 感覺可以更乾淨？
                        for i, transaction in enumerate(user_db['transactions']):
                            if transaction['deleted_at'] is None:
                                user_db['transactions'][i]['deleted_at'] = datetime.now().timestamp()
                        
                        print(f'已結清 {total} 元\n')

                        save_db(user_db_f, user_db)
                    
                    else:
                        print('也許你改變心意決定先不結帳。\n')
                
                input()
                continue
                        
            elif bool(re.match(r"(\d{7,})|(^CC-Food-\d+)", cmd)):

                if cmd not in products:
                    print("此商品不存在")
                    input()
                    continue

                # if barcode
                prod_name = products[cmd]['name']
                amount = int(products[cmd]['price'])
            
            else:
                # if amount
                try:
                    amount = int(cmd)
                except ValueError:
                    continue

            user_db['transactions'] += [{
                'created_at': datetime.now().timestamp(),
                'deleted_at': None,
                'action': 'buy',
                'amount': amount
            }]
            
            if prod_name != "":
                print(f"{prod_name} 已購買成功。\n")
            else:
                print(f'已儲存購買記錄 {amount} 元。\n')
            
            save_db(user_db_f, user_db)

            _action = input()


