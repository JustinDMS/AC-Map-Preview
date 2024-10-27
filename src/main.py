import dolphin_memory_engine as dme
from PIL import Image, ImageDraw
from pathlib import Path
import sys

# Acre overhead images from ACSE
# https://github.com/Cuyler36/ACSE/tree/master/ACSE.WinForms/Resources/Images/Acre_Images
# Acre ID spreadsheet, courtesy of Phil
# https://docs.google.com/spreadsheets/d/1x-tjUWEYibcYfP4WKkp2RVxXe7E1C0nWK9Ye1Wl_bdM/edit#gid=1297337054
# Data Megasheet
# https://docs.google.com/spreadsheets/d/13sRAcj9YbP9_i-u0Kg6S7ycHbaOQx1jFG4lYLm2DJ4c/edit?usp=sharing

# A1 - A5
# B1 - B5
# C1 - C5
# D1 - D5
# E1 - E5
# F1 - F5
acre_ids = [
    0x8127D7B8, 0x8127D7BA, 0x8127D7BC, 0x8127D7BE, 0x8127D7C0,
    0x8127D7C6, 0x8127D7C8, 0x8127D7CA, 0x8127D7CC, 0x8127D7CE,
    0x8127D7D4, 0x8127D7D6, 0x8127D7D8, 0x8127D7DA, 0x8127D7DC,
    0x8127D7E2, 0x8127D7E4, 0x8127D7E6, 0x8127D7E8, 0x8127D7EA,
    0x8127D7F0, 0x8127D7F2, 0x8127D7F4, 0x8127D7F6, 0x8127D7F8,
    0x8127D7FE, 0x8127D800, 0x8127D802, 0x8127D804, 0x8127D806,
]
acre_tile_ids = [
    0x81279C48, 0x81279E48, 0x8127A048, 0x8127A248, 0x8127A448,
    0x8127A5A8, 0x8127A7A8, 0x8127A9A8, 0x8127ABA8, 0x8127ADA8,
    0x8127AFA8, 0x8127B1A8, 0x8127B3A8, 0x8127B5A8, 0x8127B7A8,
    0x8127B9A8, 0x8127BBA8, 0x8127BDA8, 0x8127BFA8, 0x8127C1A8,
    0x8127C3A8, 0x8127C5A8, 0x8127C7A8, 0x8127C9A8, 0x8127CBA8,
    0x8127CDA8, 0x8127CFA8, 0x8127D1A8, 0x8127D3A8, 0x8127D5A8,
]

# Always start with 6 villagers
villager_ids = [0x8127D838, 0x8127E1C0, 0x8127EB48, 0x8127F4D0, 0x8127FE58, 0x812807E0]

##########

def getTileID(bytes : list) -> str:
    return (format(bytes[0], 'x') + format(bytes[1], 'x').zfill(2)).upper()


def getVillagerIDs() -> list:

    output = []

    for address in villager_ids:
        id = dme.read_bytes(address, 2)
        formatted = list((format(id[0], 'x') + format(id[1], 'x').zfill(2)).upper())
        formatted[0] = '5'
        output.append("".join(formatted))
    
    return output


def getAcreID(bytes : list) -> str:

    output = '0' + format(bytes[0], 'x')

    # Acre values change depending on its height
    # We subtract %4 from the second byte to account for this
    offset = bytes[1] % 4

    formatted = format(bytes[1] - offset, 'x').upper()
    formatted = formatted.zfill(2)
    
    return output + formatted


def main():
    dme.hook()
    dme.assert_hooked()

    # Images are 256x256
    size_x = 256
    size_y = 256

    map_preview = Image.new('RGB', (5*size_x, 6*size_y), (250, 250, 250))

    x = 0
    y = 0

    for a in acre_ids:
        id = getAcreID(dme.read_bytes(a, 2))
        image = Image.open(sys.argv[2] + id + '.jpg')
        map_preview.paste(image, (x*size_x, y*size_y))

        # Check for important structures and mark them on the map

        # Dump
        if id in ['0294', '0298', '0118']:
            image = Image.open(sys.argv[2] + 'Dump.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Nook's Shop
        elif id in ['0374', '037C', '0378']:
            image = Image.open(sys.argv[2] + 'Nook.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Post Office
        elif id in ['0370', '0380', '0384']:
            image = Image.open(sys.argv[2] + 'PostOffice.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Police Station
        elif id in ['034C', '0350', '0354']:
            image = Image.open(sys.argv[2] + 'PoliceStation.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Wishing Well
        elif id in ['0364', '0368', '036C']:
            image = Image.open(sys.argv[2] + 'WishingWell.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Museum
        elif id in ['0480', '0484', '0488']:
            image = Image.open(sys.argv[2] + 'Museum.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Able Sisters
        elif id in ['048C', '0490', '0494']:
            image = Image.open(sys.argv[2] + 'AbleSisters.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        x += 1
        if x % 5 == 0:
            y += 1
            x = 0

    villagers = getVillagerIDs()
    
    x = 0
    y = 0

    # Find and overlay villager houses
    for a in acre_tile_ids:

        tile_x = 1
        tile_y = 1

        # A tile's content's ID is 2 bytes, so we iterate through the tiles in steps of 2
        for i in range(0, 512, 2):

            id = getTileID(dme.read_bytes(a + i, 2))

            if id in villagers:
                if y > 0:
                    villagers.remove(id)
                    image = Image.open(sys.argv[2] + 'VillagerHouse.png')

                    map_preview.paste(image, (x*size_x + tile_x*16 - 32, y*size_y + tile_y*16 - 32), image)

            tile_x += 1
            if tile_x % 17 == 0:
                tile_y += 1
                tile_x = 1
        
        x += 1
        if x % 5 == 0:
            y += 1
            x = 0

    # Draw acre lines
    draw = ImageDraw.Draw(map_preview)
    line_width = 2
    line_color = (255, 0, 0, 255)
    for i in range(1, 5):
        draw.line([(size_x * i, 0), (size_x * i, 6*size_y)], width=line_width, fill=line_color)
    for i in range(1, 6):
        draw.line([(0, size_y * i), (6*size_x, size_y * i)], width=line_width, fill=line_color)

    path = Path(sys.argv[1] + "\preview.jpg")
    map_preview.save(path, "JPEG")
    map_preview.show()
    return


if __name__ == "__main__":
    main()
