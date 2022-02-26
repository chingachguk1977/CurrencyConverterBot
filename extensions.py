from config import get_data
from codes_human import codes_human


class APIException(Exception):
    pass

class Converter:
    
    @staticmethod
    def get_price(source_key='RUB', target_key='USD', amount='100') -> float:
        """
        Converts one currency to another.

        Args:
            base (str, optional): source currency. Defaults to 'RUB'.
            quote (str, optional): target currency. Defaults to 'USD'.
            amount (int, optional): how much of source currency to convert. Defaults to 100.

        Returns:
            float: the result of conversion.
        """
        
        currencies = get_data()
        currencies['RUB'] = 1
        
        try:
            source_value = currencies[source_key]
        except KeyError:
            raise APIException(f"{source_key} is not found in the currencies list.")
        try:
            target_value = currencies[target_key]
        except KeyError:
            raise APIException(f"{target_key} is not found in the currencies list.")
        if source_key == target_key:
            raise APIException(f"You're trying to convert {source_key} into itself.")
        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Something wrong with the sum representation.")
        
        result = 0
        
        result = round((target_value / source_value) * amount, 2)
        return result
        

if __name__ == '__main__':        
    p = Converter()
    source='RUB'
    target='HUF'
    amount='1'
    print(f"{amount} {codes_human[source]} = {p.get_price(source, target, amount)} {codes_human[target]}.")