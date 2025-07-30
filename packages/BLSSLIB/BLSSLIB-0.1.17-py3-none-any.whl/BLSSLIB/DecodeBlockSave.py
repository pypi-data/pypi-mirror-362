from BLSSLIB.DecodeBlockItem import DecodeBlockItem

def DecodeBlockSave(raw:str) -> list[dict[str:str|list|tuple]]:
    return [DecodeBlockItem(i) for i in raw.split(";")]
