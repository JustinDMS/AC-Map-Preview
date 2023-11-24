import dolphin_memory_engine as dme
from PIL import Image
from pathlib import Path

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

# Villager ID : House ID
house_id_map = {
    "E000": "5000",
    "E001": "5001",
    "E002": "5002",
    "E003": "5003",
    "E004": "5004",
    "E005": "5005",
    "E006": "5006",
    "E007": "5007",
    "E008": "5008",
    "E009": "5009",
    "E00A": "500A",
    "E00B": "500B",
    "E00C": "500C",
    "E00D": "500D",
    "E00E": "500E",
    "E00F": "500F",
    "E010": "5010",
    "E011": "5011",
    "E012": "5012",
    "E013": "5013",
    "E014": "5014",
    "E015": "5015",
    "E016": "5016",
    "E017": "5017",
    "E018": "5018",
    "E019": "5019",
    "E01A": "501A",
    "E01B": "501B",
    "E01C": "501C",
    "E01D": "501D",
    "E01E": "501E",
    "E01F": "501F",
    "E020": "5020",
    "E021": "5021",
    "E022": "5022",
    "E023": "5023",
    "E024": "5024",
    "E025": "5025",
    "E026": "5026",
    "E027": "5027",
    "E028": "5028",
    "E029": "5029",
    "E02A": "502A",
    "E02B": "502B",
    "E02C": "502C",
    "E02D": "502D",
    "E02E": "502E",
    "E02F": "502F",
    "E030": "5030",
    "E031": "5031",
    "E032": "5032",
    "E033": "5033",
    "E034": "5034",
    "E035": "5035",
    "E036": "5036",
    "E037": "5037",
    "E038": "5038",
    "E039": "5039",
    "E03A": "503A",
    "E03B": "503B",
    "E03C": "503C",
    "E03D": "503D",
    "E03E": "503E",
    "E03F": "503F",
    "E040": "5040",
    "E041": "5041",
    "E042": "5042",
    "E043": "5043",
    "E044": "5044",
    "E045": "5045",
    "E046": "5046",
    "E047": "5047",
    "E048": "5048",
    "E049": "5049",
    "E04A": "504A",
    "E04B": "504B",
    "E04C": "504C",
    "E04D": "504D",
    "E04E": "504E",
    "E04F": "504F",
    "E050": "5050",
    "E051": "5051",
    "E052": "5052",
    "E053": "5053",
    "E054": "5054",
    "E055": "5055",
    "E056": "5056",
    "E057": "5057",
    "E058": "5058",
    "E059": "5059",
    "E05A": "505A",
    "E05B": "505B",
    "E05C": "505C",
    "E05D": "505D",
    "E05E": "505E",
    "E05F": "505F",
    "E060": "5060",
    "E061": "5061",
    "E062": "5062",
    "E063": "5063",
    "E064": "5064",
    "E065": "5065",
    "E066": "5066",
    "E067": "5067",
    "E068": "5068",
    "E069": "5069",
    "E06A": "506A",
    "E06B": "506B",
    "E06C": "506C",
    "E06D": "506D",
    "E06E": "506E",
    "E06F": "506F",
    "E070": "5070",
    "E071": "5071",
    "E072": "5072",
    "E073": "5073",
    "E074": "5074",
    "E075": "5075",
    "E076": "5076",
    "E077": "5077",
    "E078": "5078",
    "E079": "5079",
    "E07A": "507A",
    "E07B": "507B",
    "E07C": "507C",
    "E07D": "507D",
    "E07E": "507E",
    "E07F": "507F",
    "E080": "5080",
    "E081": "5081",
    "E082": "5082",
    "E083": "5083",
    "E084": "5084",
    "E085": "5085",
    "E086": "5086",
    "E087": "5087",
    "E088": "5088",
    "E089": "5089",
    "E08A": "508A",
    "E08B": "508B",
    "E08C": "508C",
    "E08D": "508D",
    "E08E": "508E",
    "E08F": "508F",
    "E090": "5090",
    "E091": "5091",
    "E092": "5092",
    "E093": "5093",
    "E094": "5094",
    "E095": "5095",
    "E096": "5096",
    "E097": "5097",
    "E098": "5098",
    "E099": "5099",
    "E09A": "509A",
    "E09B": "509B",
    "E09C": "509C",
    "E09D": "509D",
    "E09E": "509E",
    "E09F": "509F",
    "E0A0": "50A0",
    "E0A1": "50A1",
    "E0A2": "50A2",
    "E0A3": "50A3",
    "E0A4": "50A4",
    "E0A5": "50A5",
    "E0A6": "50A6",
    "E0A7": "50A7",
    "E0A8": "50A8",
    "E0A9": "50A9",
    "E0AA": "50AA",
    "E0AB": "50AB",
    "E0AC": "50AC",
    "E0AD": "50AD",
    "E0AE": "50AE",
    "E0AF": "50AF",
    "E0B0": "50B0",
    "E0B1": "50B1",
    "E0B2": "50B2",
    "E0B3": "50B3",
    "E0B4": "50B4",
    "E0B5": "50B5",
    "E0B6": "50B6",
    "E0B7": "50B7",
    "E0B8": "50B8",
    "E0B9": "50B9",
    "E0BA": "50BA",
    "E0BB": "50BB",
    "E0BC": "50BC",
    "E0BD": "50BD",
    "E0BE": "50BE",
    "E0BF": "50BF",
    "E0C0": "50C0",
    "E0C1": "50C1",
    "E0C2": "50C2",
    "E0C3": "50C3",
    "E0C4": "50C4",
    "E0C5": "50C5",
    "E0C6": "50C6",
    "E0C7": "50C7",
    "E0C8": "50C8",
    "E0C9": "50C9",
    "E0CA": "50CA",
    "E0CB": "50CB",
    "E0CC": "50CC",
    "E0CD": "50CD",
    "E0CE": "50CE",
    "E0CF": "50CF",
    "E0D0": "50D0",
    "E0D1": "50D1",
    "E0D2": "50D2",
    "E0D3": "50D3",
    "E0D4": "50D4",
    "E0D5": "50D5",
    "E0D6": "50D6",
    "E0D7": "50D7",
    "E0E8": "50E8",
    "E0EB": "50EB",
}

##########

def getTileID(bytes : list) -> str:
    return (format(bytes[0], 'x') + format(bytes[1], 'x').zfill(2)).upper()


def getVillagerIDs() -> list:

    output = []

    for address in villager_ids:
        id = dme.read_bytes(address, 2)
        # Format second byte, adding zero if needed
        formatted = (format(id[0], 'x') + format(id[1], 'x').zfill(2)).upper()
        # Set to mapped house ID
        output.append(house_id_map[formatted])
    
    return output


def getAcreID(bytes : list) -> str:

    # Format first byte
    output = '0' + format(bytes[0], 'x')

    # Acre values change depending on its height
    # We subtract %4 from the second byte to account for this
    offset = bytes[1] % 4

    # Format second byte and add zero if needed
    formatted = format(bytes[1] - offset, 'x').upper()
    formatted = formatted.zfill(2)
    
    # Combine for the full ID and return
    return output + formatted


def main():
    # Make sure dolphin and Animal Crossing are running
    dme.hook()
    dme.assert_hooked()

    # Images are 256x256
    size_x = 256
    size_y = 256

    # Create new image for the map
    map_preview = Image.new('RGB', (5*size_x, 6*size_y), (250, 250, 250))

    # Keep track of which acre we're in
    x = 0
    y = 0

    # Build the base map
    for a in acre_ids:
        id = getAcreID(dme.read_bytes(a, 2))
        image = Image.open('Acre_Images/' + id + '.jpg')
        map_preview.paste(image, (x*size_x, y*size_y))

        # Check for important structures and mark them on the map

        # Dump
        if id in ['0294', '0298', '0118']:
            image = Image.open('Acre_Images/Dump.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Nook's Shop
        if id in ['0374', '037C', '0378']:
            image = Image.open('Acre_Images/Nook.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Post Office
        if id in ['0370', '0380', '0384']:
            image = Image.open('Acre_Images/PostOffice.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Police Station
        if id in ['034C', '0350', '0354']:
            image = Image.open('Acre_Images/PoliceStation.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Wishing Well
        if id in ['0364', '0368', '036C']:
            image = Image.open('Acre_Images/WishingWell.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Museum
        if id in ['0480', '0484', '0488']:
            image = Image.open('Acre_Images/Museum.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        # Able Sisters
        if id in ['048C', '0490', '0494']:
            image = Image.open('Acre_Images/AbleSisters.png')
            map_preview.paste(image, (x*size_x, y*size_y), image)

        x += 1
        # We're working with a 5x6 grid
        # When we place the 5th image in a row, move to the next row
        if x % 5 == 0:
            y += 1
            x = 0

    # Get and set the IDs for the villagers
    # We need to know which IDs to look for when searching for their houses
    villagers = getVillagerIDs()
    
    # Keep track of which acre we're in
    x = 0
    y = 0

    # Find and overlay villager houses
    for a in acre_tile_ids:

        # Track which tile we're on
        tile_x = 1
        tile_y = 1

        # A tile's content's ID is 2 bytes, so we iterate through the tiles in steps of 2
        for i in range(0, 512, 2):

            id = getTileID(dme.read_bytes(a + i, 2))

            # Check if ID matches a villager
            if id in villagers:
                # Make sure house is not in an A acre
                if y > 0:
                    villagers.remove(id)
                    image = Image.open('Acre_Images/VillagerHouse.png')

                    # Offset for house image takes into account acre, tile, and house image size (64x64)
                    map_preview.paste(image, (x*size_x + tile_x*16 - 32, y*size_y + tile_y*16 - 32), image)

            # Tile addresses go from left to right, top to bottom
            tile_x += 1
            if tile_x % 17 == 0:
                tile_y += 1
                tile_x = 1
        
        # Acre tracking
        x += 1
        if x % 5 == 0:
            y += 1
            x = 0

    # Output image
    map_preview.save("preview.jpg", "JPEG")
    map_preview.show()


if __name__ == "__main__":
    main()
