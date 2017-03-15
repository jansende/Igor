import contextlib
import json

@contextlib.contextmanager
def openJSON(File, ObjectClass, mode = 'r'):
    if mode not in ['r', 'u', 'w']:
        raise ValueError('must have exactly one of read/write/update mode')
    if mode in ['r', 'u']:
        json_file = open(File)
        Object = json.load(json_file, cls=ObjectClass.Decoder)
        json_file.close()
    else:
        Object = ObjectClass()
    if mode in ['u', 'w']:
        json_file = open(File, 'w')
    yield Object
    if mode in ['u', 'w']:
        json_file.write(json.dumps(Object, sort_keys=True, indent=2, cls=ObjectClass.Encoder))
        json_file.close()