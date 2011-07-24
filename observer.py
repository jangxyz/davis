#!/usr/bin/python
# -*- coding: utf-8 -*-

import web

import __builtin__
import datetime, time


urls = (
    '/observe', 'observe',
)


app = web.application(urls, globals())
render = web.template.render('templates/', 
    globals=web.utils.dictadd( globals(), __builtin__.__dict__, {
            'utils': web.utils,
        }
    )
)



class observe:

    def parse_data_string(self, s):
        return s.replace(',', ' ').split(' ')

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
            query:
                data[0-9] : numeric data, separated by comma or space
                label[0-9]: string
                type[0-9] : lines|bars

        '''
        user_input = web.input()

        keys = ('data', 'label', 'type')

        count = 0
        for key in keys:
            data_numbers = [int(k.partition(key)[-1]) for k in user_input.keys() if k.startswith(key) and k.partition(key)[-1].isdigit()]
            if data_numbers == []:
                continue
            max_n = max(data_numbers)
            count = max(max_n, count)

        keys_wo_data = [k for k in keys if k != 'data']
        if count is 0:
            dataobj = {'data': self.parse_data_string(user_input['data'])}
            dataobj.update([(k, user_input.get(k, None)) for k in keys_wo_data if user_input.get(k, None) is not None])
            dataobj_set = [dataobj]
        else:
            dataobj_set = []
            for i in range(count):
                num = `i+1`
                dataobj = {'data': self.parse_data_string(user_input['data' + num])}
                dataobj.update([(k, user_input.get(k+num, None)) for k in keys_wo_data if user_input.get(k+num, None) is not None])
                dataobj_set.append( dataobj )
        print dataobj_set

#        # data_set
#        data_set = self.get_query_with_key('data')
#        data_set = map(self.parse_data_string, data_set)
#
#        # label_set
#        label_set = self.get_query_with_key('label')
#
#        # type_set
#        type_set = self.get_query_with_key('type')
#
        #return render.observe(data_set)
        return render.observe(dataobj_set)

    def POST(self):
        return self.GET()


if __name__ == '__main__':
    app.run()

