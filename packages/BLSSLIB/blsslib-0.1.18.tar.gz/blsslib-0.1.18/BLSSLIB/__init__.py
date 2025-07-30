import random
from BLSSLIB.sharedInfo import encode_eeprom
from BLSSLIB.DecodeBlockItem import DecodeBlockItem
from BLSSLIB.EncodeBlockItem import EncodeBlockItem
from BLSSLIB.EncodeBlockSave import EncodeBlockSave
from BLSSLIB.DecodeBlockSave import DecodeBlockSave
from BLSSLIB.base64Decode import base64Decode
from BLSSLIB.base64Encode import base64Encode
from BLSSLIB.addEeprom import addEeprom8
from BLSSLIB.Ver import Ver

def base64Test():
    print("Running base64 tests..")
    test_string = "Hello, World!"
    print(f"Original string: {test_string}")
    encoded = base64Encode(test_string)
    print(f"Encoded string: {encoded}")
    decoded = base64Decode(encoded)
    print(f"Decoded string: {decoded}")
    assert decoded == test_string, "Base64 decode failed"
    print("Base64 tests passed.")

def blockItemTest():
    print("Running block item test..")
    save = "GAAAAA"
    print(f"Save : {save}")
    item = DecodeBlockItem(save)
    print(f"Decoded item: {item}")
    save_ = EncodeBlockItem(item)
    print(f"Encoded item: {save}")
    assert save_ == save, "Block item encode/decode failed"
    print("Block item tests passed.")

def blockSaveTest():
    print("Running block save test..")
    save = "GAAAAA;GCAAAA;GDAAAA;GBAAAA"
    print(f"Save : {save}")
    item = DecodeBlockSave(save)
    print(f"Decoded save: {item}")
    save_ = EncodeBlockSave(item)
    print(f"Encoded save: {save_}")
    assert save_ == save, "Block save encode/decode failed"
    print("Block save tests passed.")

def eepromMakeTest():
    print("Running EEPROM Make test..")
    data = [random.randint(0, 255) for _ in range(255)]
    eeprom = addEeprom8(data, [], (0, 0, 0), "A", )
    print(f"EEPROM data: {eeprom}")
    assert eeprom == {"id":"EEPROM", "position":(0, 0, 0), "rotation":"A", "colour":None, "data":data}, "EEPROM add failed"
    print("EEPROM tests passed.")

def eepromEncodeTest():
    print("Running EEPROM ENCODE test..")
    encode_eeprom()



print(f"running BLSSLIB version {Ver()} : ALPHA")
print("Running start up tests...")
base64Test()
blockItemTest()
blockSaveTest()
eepromMakeTest()
eepromEncodeTest()