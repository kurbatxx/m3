import binascii
import os
import m3u8
from moviepy.editor import AudioFileClip
from Crypto.Cipher import AES
from urllib.request import urlopen


def get_key(data):
    host_uri = None
    for i in range(data.media_sequence):
        try:
            key_uri = data.keys[i].uri
            host_uri = "/".join(key_uri.split("/")[:-1])
            return host_uri
        except Exception as e:
            continue


def read_keys(path):
    content = b""

    data_response = urlopen(path)
    content = data_response.read()

    return content


def get_ts(url):
    data = m3u8.load(url)
    key_link = get_key(data)
    ts_content = b""
    key = None

    #
    fpath = "ts.txt"
    if os.path.exists(fpath):
        os.remove(fpath)
    #

    for i, segment in enumerate(data.segments):
        def decrypt_func(x): return x
        if segment.key.method == "AES-128":
            if not key:
                key_uri = segment.key.uri
                key = read_keys(key_uri)
            ind = i + data.media_sequence
            iv = binascii.a2b_hex('%032x' % ind)
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            decrypt_func = cipher.decrypt

        tsf = open(fpath, "a+")
        ts_url = f'{key_link}/{segment.uri}'  # orig
        tsf.write(ts_url + "\n")
        coded_data = read_keys(ts_url)  # orig
        ts_content += decrypt_func(coded_data)  # orig
    tsf.close
    return ts_content


def m3u8_to_mp3_converter(name, url):
    ts_content = get_ts(url)
    if ts_content is None:
        raise TypeError("Empty mp3 content to save.")
    with open(f'{name}.m3u8_de', 'wb') as out:
        out.write(ts_content)


url = 'https://cs9-20v4.vkuseraudio.net/s/v1/ac/FAsAgXafXlX3miW-nm9UYBfDp_NvAA5OzEQ1QfH47mkXrkL3qe5kXR0LBKT_SEKCU3VmZX0SFhM4cH-4rfWI2QJl4ud2MH1ZOZ6WYHzUXSMQxAXzXrVRlVBcyG5J8V9IMnePxhDGTtqxHt4c9orN6CSws3iO9Zsz5tJDmG33FMF3AM0/index.m3u8'
m3u8_to_mp3_converter('result', url)
