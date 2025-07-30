from BLSSLIB.sharedInfo import IDBlocks, encode_eeprom
from BLSSLIB.base64Encode import base64Encode


def EncodeBlockItem(block:dict[str:str|list|tuple]) -> str:
    raw = f"{IDBlocks[block['id']]}{base64Encode(bytes(block['position']))}{block['rotation']}" 

    if block["colour"] is not None:
        raw += f"{base64Encode(bytes(block['colour']))}"
    
    if block["id"] == "EEPROM" :
        raw += "/" + encode_eeprom(block["data"]).split("/")[1]
    elif block["id"] == "16 bit EEPROM":
        raw += "/" + encode_eeprom(block["data"], True).split("/")[1]
    
    return raw
