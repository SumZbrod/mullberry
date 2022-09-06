TOKEN_PATH = 'mulberry/Task/static/Task/TOKEN'

super_dir = 'mulberry/Task/static/'
json_folder = super_dir + 'Task/json/'
JSON_PATHS = {
    'get':    'get_card.json',
    'update': 'update_card.json',
    'api_list':   'imt_list.json',
    'base': 'base.json',
}
for k, v in JSON_PATHS.items():
    JSON_PATHS[k] = json_folder + v


_card_url = 'https://suppliers-api.wildberries.ru/card/'

LIST_URL = _card_url + 'list'
CARDBYIMTID_URL = _card_url + 'cardByImtID'
UPDATE_URL = _card_url + 'update'
 
ITEM_JSON = {'id': '43654833587442639633', 'jsonrpc': '2.0', 'params': {'card': None}}

# nmId -> imtId

# nomenclatures

if __name__ == '__main__':
    print(JSON_PATHS)