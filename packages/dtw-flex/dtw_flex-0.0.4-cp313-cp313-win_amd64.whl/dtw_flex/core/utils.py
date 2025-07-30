import pickle
from pathlib import Path

#serialize object
def save_object(path_save, pickle_name, object):
    with open("{0}\{1}.pickle".format(path_save, pickle_name),"wb") as fp:
        pickle.dump(object ,fp)
    return None

#load object
def load_object(path_load, pickle_name):
    with open("{0}\{1}.pickle".format(path_load, pickle_name), 'rb') as fp:
        obj =  pickle.load(fp)
    return obj

