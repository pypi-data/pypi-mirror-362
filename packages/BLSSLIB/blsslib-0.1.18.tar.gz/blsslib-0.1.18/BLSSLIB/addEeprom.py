from BLSSLIB.sharedInfo import encode_eeprom


def addEeprom8(data: list[int | str], world: list[dict], position: tuple[int, int, int], rotation: str) -> dict:
    # generate the list of positions from z to z+8
    positions_to_check = [(position[0], position[1], position[2] + i) for i in range(9)]

    for item in world:
        # normalize the position to a list
        item_positions = item["position"]
        if isinstance(item_positions, tuple):
            item_positions = [item_positions]

        # check for collisions
        for pos in item_positions:
            if pos in positions_to_check:
                raise ValueError(f"Block is colliding at position {pos} with block ID '{item['id']} at index {world.index(item)}'")
    return {
        "id": "EEPROM",
        "position": position,
        "rotation": rotation,
        "colour": None,
        "data":data
    }
