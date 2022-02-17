#!/usr/local/bin/python3
import json

from datetime import datetime
from glob import glob
from os import path

folder = path.dirname(path.realpath(__file__))

def clear():
    from os import system, name as os_name
    system('cls' if os_name == 'nt' else 'clear')

while True:
    clear()
    user = input("請輸入你的 CC ID： ").strip()
    user_db_path = '{}/data/{}.json'.format(folder, user)
    
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
    
    print('\n=====功能選單=====\n購物： \t\t\t1\n計算未結金額： \t\t2\n結帳： \t\t\t3\n離開： \t\t\t4\n')
    while True:
        with open(user_db_path, 'r+', encoding='utf8') as user_db_f:
            user_db = json.loads(user_db_f.read())
            
            choose = input('請輸入要進行的功能： ').strip().lower()
            
            if choose == '1':
                amount = int(input('\n請輸入購物金額： '))

                user_db['transactions'] += [{
                    'created_at': datetime.now().timestamp(),
                    'deleted_at': None,
                    'action': 'buy',
                    'amount': amount
                }]
                
                print('已儲存購買記錄。\n')
            
            elif choose == '2' or choose == '3':
                total = 0
                for transaction in user_db['transactions']:
                    if transaction['deleted_at'] is None:
                        total += transaction['amount']
                
                print('\n您目前的未結金額： {}\n'.format(total))
            
                if choose == '3':
                    input('若要結帳，請將上列金額放到零錢區，完成後再繼續進行下一步。')
                    if input('我已經把錢放到零錢區（Y/N）： ').upper().strip() == 'Y':
                        
                        # 感覺可以更乾淨？
                        for i, transaction in enumerate(user_db['transactions']):
                            if transaction['deleted_at'] is None:
                                user_db['transactions'][i]['deleted_at'] = datetime.now().timestamp()
                        
                        print('已結清 {} 元\n'.format(total))
                    
                    else:
                        print('也許你改變心意決定先不結帳。\n')
                        
            elif choose == '4':
                break
            
            user_db_f.seek(0)
            user_db_f.truncate()
            user_db_f.write(json.dumps(user_db))
