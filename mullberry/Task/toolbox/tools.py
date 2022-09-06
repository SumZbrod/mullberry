import os
import requests
from requests.structures import CaseInsensitiveDict
import json
from .tool_config import *
from .api_exception import *
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
handler = logging.FileHandler('api.log')
formater = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formater)
logger.addHandler(handler)

def get_token():
    with open(TOKEN_PATH) as f:
        return f.read()

def get_headers():
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = get_token()
    return headers

def load_json(p_key):
    print(os.getcwd() + JSON_PATHS[p_key])
    with open(JSON_PATHS[p_key]) as fp:
        return json.load(fp)

def dump_json(obj, p_key):
    with open(JSON_PATHS[p_key], 'w') as fp:
        json.dump(obj, fp)

def api_post(url, json):    
    with requests.post(url, headers=get_headers(), json=json) as resp:
        return resp.json()

def update_base(base_json=None):
    """
    Load list of items and save
    """

    j_data = load_json('api_list')
    if not base_json:
        base_json = api_post(LIST_URL, j_data)
    try:
        dump_json(base_json, 'base')
    except Exception as e:
        logger.error(str(e), base_json)
 
def get_item_by_article(target_nmId: int):
    if not isinstance(target_nmId, int):
        raise TypeError('target_nmId must be number')
    print(JSON_PATHS)
    if not os.path.exists(JSON_PATHS['base']):
        logger.debug('load base')
        update_base()

    base = load_json('base')

    for item in base['result']['cards']:
        item_nmId = item['nomenclatures'][0]['nmId'] 
        item_imtId = item['imtId']
        if item_nmId == target_nmId:
            res_item = item
            res_imtId = item_imtId
            break
    else:
        logger.error(target_nmId)
        raise nmId_not_found('Данный артикул не был найдет')

    res_item_json = ITEM_JSON
    res_item_json['params']['card'] = res_item
    return res_item_json

def rename_item(item, new_name):
    for option in item['params']['card']['addin']: 
        if option['type'] == 'Наименование':
            if not len(option['params']):
                logger.warning(item)
                raise TypeError("Name doesn't exist")
            elif len(option['params']) > 1:
                logger.warning(option['params'])
            if option['params'][0]['value'] == new_name:
                logger.warning(new_name)
                raise ValueError('Этот товар уже имеет такое имя')
            option['params'][0]['value'] = new_name

def change_name(nm_Id:int, new_name:str, **kwargs):
    logger.debug(f'{nm_Id=}, {new_name=}')
    
    item = get_item_by_article(nm_Id)
    rename_item(item, new_name)
    post_res = api_post(UPDATE_URL, item)

    if post_res['result']:
        logger.warning(post_res)
        return
    else:
        logger.debug(post_res)
    base = load_json('base')
    
    for i, item in enumerate(base['result']['cards']):
        item_nmId = item['nomenclatures'][0]['nmId'] 
        if item_nmId == nm_Id:
            base['result']['cards'][i] = item
            break
    else:
        logger.error(target_nmId)
        raise nmId_not_found()

    update_base(base)

# def test_change_name():
#     nm_Id = 119053206
#     change_name(nm_Id, 'Ситечко для заваривания.')

# def main():
#     test_change_name()

# def test_base():
    # #update_base()
#     base = load_json('base')
#     print(base)
#     print(len(base))
#     print(len(base['result']['cards']))

# if __name__ == '__main__':
#     test_base()
    

