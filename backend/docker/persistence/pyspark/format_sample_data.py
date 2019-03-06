from MongoOps import MongoOps
from os import listdir
from os.path import isfile, join
from pprint import pprint
from ICSParser import ICSParser

mops = MongoOps()

sample_data_files = [f for f in listdir("/data") if isfile(join("/data", f))]
i = 0
for open_house_file in sample_data_files:
    parser = ICSParser("/data/%s" % open_house_file)
    event = parser.to_dict()
    result = mops.safe_query_for_location_info(event)
    i += 1
print("%d locations evaluated." % i)