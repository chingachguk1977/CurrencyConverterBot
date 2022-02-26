import requests
import json

def get_data():
    cbr_data = requests.get('https://www.cbr-xml-daily.ru/latest.js')
    currencies = json.loads(cbr_data.content)['rates']
    return currencies
    
if __name__ == '__main__':
    print(get_data())