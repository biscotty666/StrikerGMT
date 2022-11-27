# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 20:49:07 2018

@author: platzman
"""

import requests
from json import loads, dumps

class SWGOHhelp():
    def __init__(self, settings):
        self.user = "username="+settings.username     
        self.user += "&password="+settings.password
        self.user += "&grant_type=password"
        self.user += "&client_id="+settings.client_id
        self.user += "&client_secret="+settings.client_secret
    	    	
        self.token = str()
        
        self.urlBase = 'https://api.swgoh.help'
        self.signin = '/auth/signin'
        self.data_type = {'guilds': '/swgoh/guilds',
                          'guild': '/swgoh/guilds',  # alias to support typos in client code
                          'players': '/swgoh/players',
                          'player': '/swgoh/players',  # alias to support typos in client code
                          'roster': '/swgoh/roster',
                          'data': '/swgoh/data',
                          'units': '/swgoh/units',
                          'zetas': '/swgoh/zetas',
                          'squads': '/swgoh/squads',
                          'events': '/swgoh/events',
                          'battles': '/swgoh/battles'}

        
    def get_token(self):
        sign_url = self.urlBase+self.signin
        payload = self.user
        head = {"Content-type": "application/x-www-form-urlencoded",
                'Content-Length': str(len(payload))}
        r = requests.request('POST',sign_url, headers=head, data=payload, timeout = 10)
        if r.status_code != 200:
            error = 'Cannot login with these credentials'
            return  {"status_code" : r.status_code,
                     "message": error}
        _tok = loads(r.content.decode('utf-8'))['access_token']
        self.token = { 'Authorization':"Bearer "+_tok} 
        return(self.token)

    def get_data(self, data_type, spec):
        token = self.get_token()
        head = {'Method': 'POST','Content-Type': 'application/json','Authorization': token['Authorization']}
        if data_type == 'data':
            payload = {'collection': str(spec)}
        else:
            payload = {'allycode': spec}
        data_url = self.urlBase+self.data_type[data_type]
        try:
            r = requests.request('POST',data_url, headers=head, data = dumps(payload))
            if r.status_code != 200:
                error = 'Cannot fetch data - error code'
                data = {"status_code" : r.status_code,
                         "message": error}
            data = loads(r.content.decode('utf-8'))
        except:
            data = {"message": 'Cannot fetch data'}
        return data
    
    def getVersion(self):
        data_url = self.urlBase + '/version'
        try:
            r = requests.get(data_url)
            if r.status_code != 200:
                data = {"status_code": r.status_code,
                        "message": "Unable to fetch version"}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch version', "exception": str(e)}
        return data

    def fetchAPI(self, url, payload):
        self._get_access_token()
        head = {'Content-Type': 'application/json', 'Authorization': self.token['Authorization']}
        data_url = self.urlBase + url
        try:
            r = requests.request('POST', data_url, headers=head, data=dumps(payload))
            if r.status_code != 200:
                # error = 'Cannot fetch data - error code'
                error = r.content.decode('utf-8')
                data = {"status_code": r.status_code,
                        "message": error}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch data', "exception": str(e)}
        return data

    def fetchZetas(self):
        try:
            return self.fetchAPI(self.endpoints['zetas'], {})
        except Exception as e:
            return str(e)

    def fetchSquads(self):
        try:
            return self.fetchAPI(self.endpoints['squads'], {})
        except Exception as e:
            return str(e)

    def fetchBattles(self, payload=None):
        if payload is None:
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        try:
            return self.fetchAPI(self.endpoints['battles'], payload)
        except Exception as e:
            return str(e)

    def fetchEvents(self, payload=None):
        if payload is None:
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        try:
            return self.fetchAPI(self.endpoints['events'], payload)
        except Exception as e:
            return str(e)

    def fetchData(self, payload):
        if not isinstance(payload, dict):
            return {'message': "Payload ERROR: dict expected."}
        if 'collection' not in payload.keys():
            return {'message': "Payload ERROR: No collection element in provided dictionary."}
        try:
            return self.fetchAPI(self.endpoints['data'], payload)
        except Exception as e:
            return str(e)

    def fetchPlayers(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'language': "eng_us", 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['players'], payload)
        except Exception as e:
            return str(e)

    def fetchGuilds(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'language': "eng_us", 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['guilds'], payload)
        except Exception as e:
            return str(e)

    def fetchUnits(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'language': "eng_us", 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['units'], payload)
        except Exception as e:
            return str(e)

    def fetchRoster(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['roster'], payload)
        except Exception as e:
            return str(e)

    

class settings():
    def __init__(self, _username, _password, _client_id, _client_secret):
        self.username = _username
        self.password = _password
        self.client_id = _client_id
        self.client_secret = _client_secret

