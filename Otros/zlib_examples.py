import zlib

a = b'x\x9cm\x8eM\x0b\xc20\x0c\x86\xef\xfd\x159\x0bvi\xd2\xce\r\xc6`S\xe7\xc9\x83X\xf0,C\x05Q\xf1\x13\xfc\xf9f\xebd;,!\xb4\xc9\xdb\xbey4q\xda\x06\xa0\xe4T\x0f\xdaYJP_\xd5C\x19B\x9d0\xb3\xb50\xb8\x12\x1b\xd2\x0e\x91\xc0:\xd4(\xc1\xf0<\xa8\xdd\x04n\xf2\x87\xb5!\x11Em|\xfbn\xdcK\xd6D+\x86\xd3K\x95^E\x95h1\xf8\xa32\x01\xca\x00\x13\xc42\xb9\xaaL<JD\x9bHU\xa1\x1cI%\xcdz9\x8b\xaew\x9d>\x93\xb9\xcd\xc1\x9f\xd5\xd2\xb7\xde\xdb\xfb\xfe\x96eQQ\xbf?\xfb\x8b?|\xdf\x90U\xcbJ\x9eb\x91C\x9eC\xb9\x98\x8f\x01\x18\x8auL\xae\xa7@\x0e\xae\xeb\xf9\xdfy\x94:\xc5\x01uC\xd6R\xd9\x8e\x16\x03\xb93\x81\xb4\xd1{\xda\x8d\xe4\x0f\xe6\x8fU\xb9'
b = b"x\x9c]\x91\xcbn\x830\x10E\xf7\xfe\x8aY\xa6\x8b\xc8@\xa0d\x81\x90R\xaaH,\xfaPi?\x00\xec\x81X*\xb6e\xcc\x82\xbf\xaf\x1fyH\xb5d\xa4\xe3\x99{\xc7\\\xd3\xa6}m\xa5\xb0@?\x8db\x1dZ\x18\x85\xe4\x06\x17\xb5\x1a\x860\xe0$$I3\xe0\x82\xd9+\x85/\x9b{M\xa8\x13w\xdbbqn\xe5\xa8HU\x01\xd0/W]\xac\xd9`w\xe2j\xc0'B?\x0cG#\xe4\x04\xbb\x9f\xa6s\xdc\xadZ\xff\xe2\x8c\xd2BB\xea\x1a8\x8e\xce\xe9\xad\xd7\xef\xfd\x8c@\x83l\xdfrW\x17v\xdb;\xcd\xa3\xe3{\xd3\x08Y\xe04\xde\x86)\x8e\x8b\xee\x19\x9a^NH\xaa\xc4\xad\x1a\xaa\xb3[5A\xc9\xff\xd5\x8b\xa8\x1aFv\xe9\x8d\xef\xce^\\w\x92\xe4\xc7\xdaS\x9e\x07zN\x03\x15E\xa02\x8bt\x8cTD:E*\xc3\x94\xab\xdf\xe1\xe6\xfe\xb8\xcc!\xb4%\xd17K\xe2\x94\xf263\x0c\xcb\xe3\xe19P\x91\xc5\xc3\xe6\xea\x1b\x9d\xfc\x8f\xf8\xc0\xef)\xb1\xd5\x18\x17Px\x95\x90\x8c\xcfDH\xbc?\x9cV\xda\xab\xfc\xfe\x03\x04\x11\x8f\xc8"

c = zlib.decompress(b)

print(c)