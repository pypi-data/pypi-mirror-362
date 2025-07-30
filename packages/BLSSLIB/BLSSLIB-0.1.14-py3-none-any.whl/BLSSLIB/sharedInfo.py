chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#$"
ver = "1.4"

BlockIDs = {
                "1": "AND Gate",
                "b": "NAND Gate",
                "c": "NOR Gate",
                "d": "NOT Gate",
                "e": "OR Gate",
                "f": "Splitter",
                "g": "XNOR Gate",
                "2": "XOR Gate",
                "h": "Counter",
                "i": "8 Bit Shifter Counter",
                "j": "Num. Counter",
                "k": "Color No Light",
                "l": "Gated SR Latch",
                "m": "Full Adder",
                "n": "SR Latch",
                "o": "Toggle Output",
                "p": "Delay",
                "q": "Timer",
                "3": "Randomizer",
                "r": "Wifi",
                "s": "Button",
                "t": "Sign",
                "u": "Lever",
                "v": "Toggle Button",
                "w": "Instant Button",
                "x": "HEX Color Display",
                "y": "HEX Squared Color Display",
                "4": "HEX LCD Display",
                "5": "HEX Pixel Color Display",
                "6": "Barrier",
                "7": "Read Output",
                "8": "Color Neon Light",
                "0": "Color Light",
                "z": "RGB Light",
                "a": "Barrier Block",
                "K": "Invisible Block",
                "A": "Torch WATT_Down",
                "B": "Sign WATT_Down",
                "C": "Sign WATT",
                "D": "Torch WATT",
                "E": "Day Controller",
                "F": "Kill Module",
                "G": "Block",
                "H": "Stair",
                "I": "Ladder",
                "J": "Torch",
                "9": "Green Screen",
                "L": "Slab",
                "M": "Inner Stair",
                "N": "Outer Stair",
                "O": "Color Neon Light 2",
                "P": "Full Subtractor",
                "Q": "Plate",
                "R": "Piston",
                "S": "4 Bit Register",
                "T": "Dip Switches",
                "U": "8x8 RGB2 Panel",
                "V": "Interval Calculator",
                "W": "8 Bit Splitter",
                "X": "EEPROM",
                "Y": "LED",
                "Z": "8 Bit AND Gate",
                "`": "8 Bit NOR Gate",
                "!": "8 Bit OR Gate",
                "@": "8 Bit XOR Gate",
                "&": "8 Bit NAND Gate",
                "*": "8 Bit XNOR Gate",
                "(": "Text Button",
                ")": "Command Block",
                ".": "4 Bit Shifter Counter",
                ",": "Chair",
                "<": "HEX Color Display 2",
                ">": "Text Panel",
                "-": "2 Bit Multiplier",
                "+": "Door",
                "=": "Electric Door",
                "[": "Sticky Piston",
                "]": "TNT",
                "{": "Empty Block",
                "}": "RGB2 Light",
                "/": "Corner Pane",
                ":": "Glass Pane",
                "_": "RGB2 Light Panel",
                "|": "Block Placer",
                "#0": "8 Bit Buffer",
                "#1": "4 Sides Pole",
                "#2": "5 Sides Pole",
                "#3": "6 Sides Pole",
                "#4": "4 LEDs",
                "#5": "TNT Activator",
                "#6": "4 Bit Comparator",
                "#7": "8 Bit Register",
                "#8": "16x16 RGB2 Panel",
                "#9": "4 RGB Lights Panels",
                "#a": "D Flip Flop",
                "#b": "Beam 1x4",
                "#c": "Beam 1x7",
                "#d": "16 Bit EEPROM",
                "#e": "Double Dabble Chip",
                "#f": "Laser",
                "#g": "Laser Detector",
                "#h": "Transmitter",
                "#i": "D Latch",
                "#j": "T Flip Flop",
                "#k": "4 Sides Pole 2",
                "#l": "Color Light Panel",
                "#m": "Corner Pole",
                "#n": "Pole",
                "#o": "T Pole",
                "#p": "3 Sides Pole",
                "#q": "RGB Light Panel",
                "#r": "Buzzer",
                "#s": "Spawn",
                "#t": "EMERGENCY",
                "#u": "Speaker",
                "#v": "Teleport Module A",
                "#w": "Teleport Module B",
                "#x": "Pressure Plate",
                "#y": "Don't Press Button",
                "#z": "Plate Button",
                "#A": "Complex Counter",
                "#B": "NUCLEAR TNT",
                "#D": "Trap Door",
                "#E": "Electric Trap Door",
                "#F": "RGB Neon Light",
                "#G": "RGB2 Neon Light",
                "#H": "Inverted Double Dabble Chip",
                "#I": "Triangular Stair",
                "#J": "Physics Block",
                "#K": "Sticky Block",
                "#L": "8 Bit Multiplier",
                "#M": "16 Bit Multiplier",
                "#N": "8 Bit Divider",
                "#O": "16 Bit Divider",
                "#P": "Obsidian",
                "#Q": "Air Block",
                "#R": "Player Detector",
                "#S": "Quick NOT",
                "#T": "Reinforced Block",
                "#U": "Clay Block",
                "#V": "Color Detector",
                "#W": "8 Bit Adder",
                "#X": "16 Bit Adder",
                "#Y": "D Flip",
                "#Z": "Mini HEX Color Display",
                "#!": "HTTP Transmitter",
                "#|": "Stair Chair",
                "#-": "Solid Chair",
                "#(": "Slab Chair",
                "#)": "Junction Block",
                "#@": "_Legacy Keypad",
                "#&": "Keypad",
                "#[": "16 Bit Shifter Counter",
                "#^": "Illegal Piston",
                "#:": "Illegal Sticky Piston",
                "#>": "Super Sticky Piston",
                "#*": "1 Bit 1:16 Demux",
                "#=": "1 Bit 1:8 Demux",
                "#+": "4 Bit 4:1 Mux",
                "#_": "8 Bit 2:1 Mux",
                "#$": "8 Bit 8:1 Mux",
                "#<": "4 Bit 16:1 Mux",
                "#,": "4 Bit Wifi",
                "#/": "Perfect TNT",
                "#`": "Loki Spawner",
                "%0": "Controllable Color Display",
                "%1": "Loaded Gate",
                "%2": "Light Button"
            }
IDBlocks = {v: k for k, v in BlockIDs.items()}

def flip_byte(n, type16=False):
    bits = 16 if type16 else 8
    return int(f'{n:0{bits}b}'[::-1], 2)

def base71(n):
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%?&<()"

    if n == 0:
        return "00"
    base71_str = ""
    while n > 0:
        n, remainder = divmod(n, 71)
        base71_str = digits[remainder] + base71_str
    return base71_str.rjust(2, "0")


def encode_eeprom(data_lines, type16=False):
    address = -1
    Save = "#dHCAgA/" if type16 else "XDCAgA/"


    for line in data_lines:
        try:
            address, value = line.split()
            address = int(address)
        except ValueError:
            address += 1
            value = line

        Save += base71(flip_byte(address))
        if int(value) >= 2 ** (8 * (type16 + 1)) or len(value) >= 3 + (2 * type16):
            Save += base71(flip_byte(int(value, 2)))
            continue
        Save += base71(flip_byte(int(value)))
        
    Save += "=1"
    return Save


