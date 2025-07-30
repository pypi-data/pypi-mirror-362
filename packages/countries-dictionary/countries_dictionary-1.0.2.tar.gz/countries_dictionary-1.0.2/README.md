Countries Dictionary provides a dictionary contains all members and observer states of the United Nations and information about them:
- Continent(s) of the countries' mainland
- Area in square kilometre
- Population
- Nominal GDP in dollar

I created this module as a source of countries' information that is easy to access and use by coders using any programming language (as it can be converted into JSON).

After importing it:
```
from countries_dictionary import countries
```
you can do many things with the dictionary, such as convert it into a JSON string:
```
json.dumps(countries, indent=4)
```
calculate GDP per capita of a country: 
```
countries["Vietnam"]["nominal GDP"] /  countries["Vietnam"]["population"]
```
population density: 
```
countries["Russia"]["population"] /  countries["Russia"]["area"]
```