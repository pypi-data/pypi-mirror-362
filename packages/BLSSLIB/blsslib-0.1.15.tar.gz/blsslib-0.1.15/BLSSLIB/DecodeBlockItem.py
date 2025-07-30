from BLSSLIB.sharedInfo import BlockIDs
from BLSSLIB.base64Decode import base64Decode

def DecodeBlockItem(raw:str) -> dict[str:str|list|tuple]:
    return {
        "id": BlockIDs[raw[0]],
        "positon": tuple(base64Decode(raw[1:5])),
        "rotation": raw[5],
        "colour": tuple(base64Decode(raw[6:]))
    } if raw[0] != "#" else {
        "id": BlockIDs[raw[0:2]],
        "positon": tuple(base64Decode(raw[2:6])),
        "rotation": raw[6],
        "colour": tuple(base64Decode(raw[7:]))
    }
