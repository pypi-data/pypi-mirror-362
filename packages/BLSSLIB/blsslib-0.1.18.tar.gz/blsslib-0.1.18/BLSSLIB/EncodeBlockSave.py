from BLSSLIB.EncodeBlockItem import EncodeBlockItem

def EncodeBlockSave(blocks:list[dict[str:str|list|tuple]]) -> str:
    return ("".join([EncodeBlockItem(i) for i in blocks]))[1:]
