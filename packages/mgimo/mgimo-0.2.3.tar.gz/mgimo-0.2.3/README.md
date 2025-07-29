# Данные и программные утилиты МГИМО

## Установка

```console
pip install mgimo
```

## Использование

### Названия стран-членов ООН и столицы стран 

```python
from random import choice

from mgimo.data import country_to_capital

countries = list(country_to_capital.keys())
assert len(countries) == 193
country = choice(countries)
city = country_to_capital[country]
print(f"Выбрана страна: {country}, столица - {city}.")
```