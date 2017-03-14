import contextlib
import json

@contextlib.contextmanager
def loadJSON(File, ObjectClass):
    json_file = open(File)
    yield json.load(json_file, cls=ObjectClass.Decoder)
    json_file.close()
@contextlib.contextmanager
def saveJSON(File, ObjectClass):
    json_file = open(File, 'w')
    Object = ObjectClass()
    yield Object
    json_file.write(json.dumps(Object, sort_keys=True, indent=2, cls=ObjectClass.Encoder))
    json_file.close()