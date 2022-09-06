import requests
from requests.structures import CaseInsensitiveDict
import json

j_paths = {
    'get': 'get_card.json',
    'update': 'update_card.json',
    'list': 'imt_list.json',
}

def get_token():
    with open('TOKEN') as f:
        return f.read()

def get_headers():
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = get_token()
    return headers


def get_json(p_key):
    with open(j_paths[p_key]) as fp:
        return json.load(fp)

def api_post(url, json):
    with requests.post(url, headers=get_headers(), json=json) as resp:
        return resp.json()


def get_test():
    url = 'https://suppliers-api.wildberries.ru/card/cardByImtID'
    imtID = 106933073

    j_data = get_json('get')
    j_data['params']['imtID'] = imtID
    print('SEND:')
    print(f'>> {j_data}')
    
    resp_json = api_post(url, j_data)

    print('GET:')
    print(f'>> {resp_json}')
    with open('resp.json', 'w') as f:
        json.dump(resp_json, f)

def update_test():
    url = 'https://suppliers-api.wildberries.ru/card/update'
    
    with open('resp.json') as f:
        card = json.load(f)
    
    for a in card['result']['card']['addin']:
        if a['type'] == 'Наименование':
            for b in a['params']:
                b['value'] = 'Ситечко для заваривания'
                break
    
    A = card
    card['params'] = card['result']
    del card['result']
    # print(card)
    print(card)
    with open('A.json', 'w') as f:
        json.dump(card, f)
    return
    res = api_post(url, card)
    print(res)

def list_test():
    url = 'https://suppliers-api.wildberries.ru/card/list'

    j_data = get_json('list')
    # j_data['params']['filter']['find'][0]['search'] = 119053230
    resp_json = api_post(url, j_data)
    # print('GET:')
    print(j_data) 
    print(f'>> {resp_json}')
    with open('list.json', 'w') as f:
        json.dump(resp_json, f)

def get_all_valuse(D):
    res_v = []
    if isinstance(D, dict):
        D_values = D.values()
    else:
        D_values = D

    for v in D_values:
        if isinstance(v, (int, str)):
            res_v.append(v)
        elif isinstance(v, (list, dict)):
            res_v += get_all_valuse(v)

    return res_v

def list_read():
    with open('list.json') as f:
        data = json.load(f)
    for D in data['result']['cards']:
        if D['object'] == 'Ситечки для заваривания':
            C = get_all_valuse(D)
            print(C)
            print()
                    

def main():
    # list_test()
    # list_read()

    # get_test()
    update_test()
    
 

if __name__ == '__main__':
    main()
