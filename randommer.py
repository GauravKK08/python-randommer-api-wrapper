import requests
import time
import json

class Randommer():
    def __init__(self, api_key=None, json_response=True, prefetch_cultures=True):
        with open('config.json') as fp:
            self.config = json.load(fp)

        if api_key is None:
            self.api_key = self.config.get('api_key')

        if self.api_key is None:
            raise Exception('API key could not be loaded from config/not passed via param.')
        self.api_url = self.config['api_url']
        self.request_headers = {'X-Api-Key': self.api_key, 'accept': '*/*'}
        self.json_response = json_response
        self.cultures = None
        if prefetch_cultures:
            self.cultures = self.get_misc_cultures()
        self.nameTypes = ['firstname', 'surname', 'fullname']
        self.country_codes = []
        self.get_phone_countries()
        self.loremTypes = ['normal', 'business']
        self.text_types = ['paragraph', 'words']

    def make_request(self, api_url, params={}, method='GET', contentType = None):
        start_time = time.time()
        print('Hitting URL: %s'%api_url)
        if contentType:
            self.request_headers['Content-Type'] = contentType
        if method == 'GET':
            response = requests.get(url=api_url, headers=self.request_headers, params=params)
        elif method == 'POST':
            response = requests.get(url=api_url, headers=self.request_headers, params=params)

        end_time = time.time()
        print("Execution took {} seconds".format(end_time-start_time))
        if response.status_code !=200:
            raise Exception('Non OK status code. Response text: %s'%response.text)
        if self.json_response:
            result = response.json()
        else:
            result= response.text
        return result

    def get_random_card_numbers(self):
        return self.make_request(api_url=self.api_url+'Card')

    def get_available_card_types(self):
        return self.make_request(api_url=self.api_url+'Card/Types')

    def get_misc_cultures(self):
        return self.make_request(api_url=self.api_url+'Misc/Cultures')

    def get_random_address(self, number=1, culture='en'):
        if number < 1 or number > 1000:
            raise Exception('You can only ask for address(es) 1 to 1000.')
        is_valid_culture = False
        if not self.cultures:
            self.cultures = self.get_misc_cultures()

        for _culture in self.cultures:
            if _culture['code'] == culture.lower():
                is_valid_culture = True

        if not is_valid_culture:
            raise Exception('Provided culture: %s does not seem valid.'%culture)

        params = {'number': number, 'culture': culture}
        return self.make_request(api_url=self.api_url+'Misc/Random-Address', params=params)

    def get_random_name(self, quantity=1, nameType='firstname'):
        if nameType not in self.nameTypes:
            raise Exception('Invalid nameType:%s can only be one of %s'%(nameType, self.nameTypes))
        if quantity < 1 or quantity > 5000:
            raise Exception('Can only ask for 1 to 5000 random names at a time.')
        params = {'nameType': nameType, 'quantity': quantity}
        return self.make_request(api_url=self.api_url+'Name', params=params)

    def get_business_suggestions(self, startingWords='Lorem Ipsum'):
        if len(startingWords) > 100:
            raise Exception('starting words can only be less than 100 chaaracters.')
        params = {'startingWords': startingWords}
        return self.make_request(api_url=self.api_url+'Name/Suggestions', params=params)
    
    def get_phone_countries(self):
        country_codes = self.make_request(api_url=self.api_url+'Phone/Countries')
        for country_code in country_codes:
            self.country_codes.append(country_code['countryCode'])
        return country_codes

    def validate_phone_number(self, telephone, countryCode):
        if countryCode not in self.country_codes:
            raise Exception('Invalid country code: %s'%countryCodes)
        if len(telephone) > 25:
            raise Exception('Invalid telephone number: %s'%telephone)
        params = {'telephone': telephone, 'countryCode': countryCode}
        return self.make_request(api_url=self.api_url+'Phone/Validate', params=params)

    def get_bulk_telephone_numbers(self, countryCode='IN', quantity=10):
        if countryCode not in self.country_codes:
            raise Exception('Invalid country code: %s'%countryCodes)
        if quantity < 1 or quantity > 1000:
            raise Exception('Can only ask for 1 to 1000 random nos at a time.')
        params = {'countryCode': countryCode, 'quantity': quantity}
        return self.make_request(api_url=self.api_url+'Phone/Generate', params=params)

    def generate_ssn(self):
        return self.make_request(api_url=self.api_url+'SocialNumber', params={})

    def generate_lorem_ipsum(self, loremType='normal', text_type='words', number=10):
        if loremType not in self.loremTypes:
            raise Exception('Unknown lorem type: %s'%loremType)
        if text_type not in self.text_types:
            raise Exception('Unknown text type: %s'%text_type)
        params = {'loremType': loremType, 'type': text_type, 'number': number}
        return self.make_request(api_url=self.api_url+'Text/LoremIpsum', params=params)

    def generate_password(self, length=16, hasDigits=True, hasUppercase=True, hasSpecial = True):
        if length <3 or length > 250:
            raise Exception('Password length can only be 3 to 250 chars max.')
        params = {'length': length, 'hasDigits': hasDigits, 'hasUppercase': hasUppercase, 'hasSpecial': hasSpecial}
        return self.make_request(api_url=self.api_url+'Text/Password', params=params)

    def humanize_text(self, text='Lorem Ipsum Dolor Sit Amet.'):
        params = {'text': text}
        return self.make_request(api_url=self.api_url+'Text/Humanize', params=params, method='POST', contentType='application/json-patch+json')

rm = Randommer()
print(rm.get_random_card_numbers())
print(rm.get_available_card_types())
print(rm.get_misc_cultures())
print(rm.get_random_address(culture='cz'))
print(rm.get_random_name(nameType='fullname'))
print(rm.get_business_suggestions())
print(rm.get_phone_countries())
print('Is valid?', rm.validate_phone_number(telephone='+919545667788', countryCode='IN'))
print(rm.get_bulk_telephone_numbers())
print(rm.generate_ssn())
print(rm.generate_lorem_ipsum())
print(rm.generate_password())
## Seems to have some issues.
#print(rm.humanize_text())

