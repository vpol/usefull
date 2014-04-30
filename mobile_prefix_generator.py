# -*- coding: utf-8 -*-
import time

__author__ = 'vpol'

def fill(root, prefix, value, parent, pkey):
    if len(prefix) > 1:
        if prefix[0] in root:
            fill(root[prefix[0]], prefix[1:], value, root, prefix[0])
            if pkey:
                if len(parent[pkey]) == 10 and all(val=='value' for val in parent[pkey].values()):
                    parent[pkey] = value
        elif type(root) == type({}):
            root[prefix[0]] = {}
            fill(root[prefix[0]], prefix[1:], value, root, prefix[0])
            if pkey:
                if len(parent[pkey]) == 10 and all(val=='value' for val in parent[pkey].values()):
                    parent[pkey] = value
    elif type(root) == type({}):
        root[prefix[0]] = value
        if pkey:
            if len(parent[pkey]) == 10 and all(val=='value' for val in parent[pkey].values()):
                parent[pkey] = value
    return root

def compact(prefixes, current):
    if not type(prefixes) == type({}):
        return [current]
    else:
        rlist = []
        for k, v in prefixes.items():
            rlist.extend(compact(v, current + k))
            continue
        return rlist

if __name__ == '__main__':
    '''
    Генератор префиксов для мобильных телефонов СПб и ЛО из файла Kody_DEF-9kh.csv который можно скачать тут:

    http://www.rossvyaz.ru/docs/articles/Kody_DEF-9kh.csv

    '''
    start_time = time.time()
    codes = {}
    our_region = 'Санкт - Петербург и Ленинградская область'
    with open('Kody_DEF-9kh.csv', encoding='cp1251') as f:
        counter = 0
        for line in f:
            ## skip header
            counter += 1
            if counter == 1:
                continue
            plist = {}
            code, start, end, amount, operator, region = line.strip().split(';')
            if not region == our_region:
                continue
            if not code in codes:
                codes[code] = []
            for x in range(int(start), int(end)+1):
                fill(plist, str(x).zfill(7), 'value', plist, None)
            codes[code].extend(sorted(compact(plist, '')))
    keys = sorted(codes.keys())
    for c in keys:
        print('\n'.join('{0}{1}'.format(c, k) for k in sorted(set(codes[c]))))
    print('operation took {0:0.2f} sec'.format(time.time() - start_time))
