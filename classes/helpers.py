import contextlib
import json

def convertToJSON(obj):
    try:
        try:
            dic = { obj.JSONName : obj.__dict__ }
        except:
            dic = { obj.__class__.__name__ : obj.__dict__ }
        return json.dumps(dic, sort_keys=True, indent=2)
    except Exception:
        raise RuntimeError('JSON could not be created')
def convertFromJSON(jsn, cls):
    try:
        dic = json.loads(jsn)
        obj = cls()
        try:
            obj.__dict__.update(dic[cls.JSONName])
        except Exception:
            obj.__dict__.update(dic[cls.__name__])
        return obj
    except Exception:
        raise RuntimeError('JSON could not be interpreted')

@contextlib.contextmanager
def openJSON(File, ObjectClass, mode = 'r'):
    if mode not in ['r', 'u', 'w']:
        raise ValueError('must have exactly one of read/write/update mode')
    if mode in ['r', 'u']:
        json_file = open(File)
        Object = convertFromJSON(json_file.read(), ObjectClass)
        json_file.close()
    else:
        Object = ObjectClass()
    if mode in ['u', 'w']:
        json_file = open(File, 'w')
    yield Object
    if mode in ['u', 'w']:
        json_file.write(convertToJSON(Object))
        json_file.close()