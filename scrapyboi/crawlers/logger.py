import os
import json
import time


def write_logger(text):
    if not os.path.exists("logger"):
        os.mkdir('logger')
    with open('logger/scrappy.log', 'a+') as outfile:
        time_f = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        outfile.write(time_f + " >> " + " ".join(text.split()) + "\n")


def write_file(dict_arr, platform, product_query):
    if not os.path.exists("json/{}".format(platform)):
        os.makedirs("json/{}".format(platform))
    with open('json/{}/{}.json'.format(platform, product_query), 'w+') as outfile:
        json.dump(dict_arr, outfile, sort_keys=True, indent=4)
