import requests


def save_bin(fn, data):
    fp = open(fn, "wb")
    fp.write(data)
    fp.close()
    return True


fn = "images/reiki_s1.jpg"
url = "http://guzanov.info/"+fn
r = requests.get(url)
if not r.ok:
    print("{} load error: {}".format(fn, r.status_code))
    exit(0)
if save_bin(fn, r.content):
    print("{} loaded and stored OK".format(fn))
