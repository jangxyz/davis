#!/usr/bin/python
# -*- coding: utf-8 -*-

import web

import helper

import __builtin__
import datetime, time


urls = (
    '/', 'davis',
)


app = web.application(urls, globals())
render = web.template.render('templates/', 
    globals=web.utils.dictadd( 
        globals(), __builtin__.__dict__, 
        { 
            'utils': web.utils,
            'helper': helper,
        }
    )
)



class davis:
    KEYS = ('data', 'label', 'type')
    
    def parse_data_string(self, s):
        return s.replace(',', ' ').split(' ')

    def is_multiple_key(self, key):
        ''' return True only if key is of pattern /(data|label|type)[0-9]+/ '''
        for __key in self.KEYS:
            if key.startswith(__key):
                if key.partition(__key)[-1].isdigit():
                    return True
        return False

    def strip_key_num(self, key):
        ''' return suffix number if key is given key (one of data, label, type), else None 
        
        >>> davis().strip_key_num('data1')
        1
        >>> davis().strip_key_num('type108')
        108
        >>> print davis().strip_key_num('nothing3')
        None
        '''
        for k in self.KEYS:
            if key.startswith(k):
                suffix = key.partition(k)[-1]
                if suffix.isdigit():
                    return int(suffix)
        return None

    def get_query_with_key(self, key, user_input=None):
        '''
            return subset from user_input dictionary 
            whose key matches /key[0-9]+/
        '''
        if user_input is None:
            user_input = web.input()
        if key in user_input.keys():
            return [ user_input[key] ]
        else:
            return [user_input[k] for k in sorted(user_input.keys()) if k.startswith(key) and k.partition(key)[-1].isdigit()]

    def GET(self):
        '''
            parse query:
                data[0-9] : numeric data, separated by comma or space
                label[0-9]: string
                type[0-9] : lines|bars

        '''
        user_input = web.input()

        keys_wo_data = [k for k in self.KEYS if k != 'data']

        data_numbers    = [self.strip_key_num(key) for key in user_input.keys()]
        max_data_number = max(data_numbers) if data_numbers else 0

        # dataobj_set
        #   dataobj is dict of {'data': [], 'label': '', 'type': ''}
        dataobj_set = []
        if not max_data_number:
            dataobj = {'data': self.parse_data_string(user_input['data'])}
            dataobj.update([(k, user_input.get(k, None)) for k in keys_wo_data if user_input.get(k, None) is not None])

            dataobj_set.append( dataobj )
        else:
            for i in range(max_data_number):
                num = `i+1`
                dataobj = {'data': self.parse_data_string(user_input['data' + num])}
                dataobj.update([(k, user_input.get(k+num, None)) for k in keys_wo_data if user_input.get(k+num, None) is not None])
                dataobj_set.append( dataobj )

        return render.davis(dataobj_set)

    def POST(self):
        return self.GET()


if __name__ == '__main__':
    app.run()

