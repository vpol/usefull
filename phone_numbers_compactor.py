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
    Например, у вас есть диапазон телефонных номеров из базы Россвязи.

    К примеру (запись из базы):

    900;100000;199999;100000;Смоленская Сотовая Связь;Тверская область

    Но для большинства АТС или SoftSwitch, нельзя указать диапазон номеров. Можно только префикс.

    Соответственно данный код генерирует список префиксов

    '''
    start_time = time.time()
    plist = {}
    for x in range(3333333, 5555555):
        fill(plist, str(x), 'value', plist, None)
    print('\n'.join(sorted(compact(plist, ''))))
    print('operation took {0:0.2f} sec'.format(time.time() - start_time))
