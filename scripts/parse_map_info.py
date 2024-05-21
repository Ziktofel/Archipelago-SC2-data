"""
A script for parsing MapInfo files and potentially writing some data to them.

Assumes it is run from the repository's root directory.
"""


from typing import NamedTuple
import glob
import struct
import json

map_info_files = glob.glob("Maps/ArchipelagoCampaign/*/ap_*.SC2Map/MapInfo", recursive=True)

def unpack_string(contents: bytes, offset: int) -> tuple[str, int]:
    parts = contents[offset:].split(b'\0', 1)
    return parts[0].decode('utf-8'), len(parts[0]) + (len(parts) > 1)

def prettyhex(num: int) -> str:
    if num < 0x10:
        return "0" + hex(num)[2:]
    return hex(num)[2:]

class Player(NamedTuple):
    player_id: int
    control: int
    colour: int
    faction: str
    unknown: int
    start_point: int
    ai: int
    decal: str

class MapInfo(NamedTuple):
    map_version: int
    noise: int
    width: int
    height: int
    small_preview_path: str
    large_preview_path: str
    fog_type: str
    tileset: str
    left: int
    bottom: int
    right: int
    top: int
    load_screen_path_offset: int
    load_screen_path_offset_end: int
    load_screen_fit_offset: int
    load_screen_path: str
    load_screen_race: str
    load_screen_fit: int
    data_flags_offset: int
    data_flags: int
    players: list[dict]


class Reader:
    def __init__(self, contents: bytes) -> None:
        self.offset = 0
        self.contents = contents
    def i32(self) -> int:
        result, = struct.unpack_from('<I', self.contents, self.offset)
        self.offset += 4
        return result
    def i16(self) -> int:
        result, = struct.unpack_from('<H', self.contents, self.offset)
        self.offset += 2
        return result
    def i8(self) -> int:
        result, = struct.unpack_from('<B', self.contents, self.offset)
        self.offset += 1
        return result
    def fmt(self, fmt: str, size: int) -> tuple:
        result = struct.unpack_from(fmt, self.contents, self.offset)
        self.offset += size
        return result
    def c4(self) -> str:
        result = b''.join(struct.unpack_from('cccc', self.contents, self.offset)).decode('utf-8')
        self.offset += 4
        return result
    def cstring(self) -> str:
        result, increment = unpack_string(self.contents, self.offset)
        self.offset += increment
        return result
    def nbytes(self, n: int) -> bytes:
        result = self.contents[self.offset:self.offset + n]
        self.offset += n
        return result

def parse_player(reader: Reader) -> Player:
    player_id = reader.i8()
    control = reader.i32()
    colour = reader.i32()
    faction = reader.cstring()
    unknown = reader.i32()
    start_point = reader.i32()
    ai = reader.i32()
    decal = reader.cstring()
    return Player(player_id, control, colour, faction, unknown, start_point, ai, decal)

# Roughly following along view-source:
# (seems old and not very workable) https://repos.sc2mapster.com/sc2/sc2-map-analyzer/trunk/read.cpp
# https://github.com/ggtracker/sc2reader/blob/upstream/sc2reader/objects.py
def process_map_info(filename:str, contents: bytes):
    reader = Reader(contents)
    magic = reader.c4()
    assert magic == 'IpaM', (filename, magic)

    map_version = reader.i32()

    # unknown 2 words
    assert map_version >= 0x18
    noise, unknown0 = reader.fmt('<II', 8)
    assert unknown0 == 0

    width, height = reader.fmt('<II', 8)

    small_preview_path = ''
    small_preview_type = reader.i32()

    if small_preview_type == 2:
        small_preview_path = reader.cstring()

    large_preview_path = ''
    large_preview_type = reader.i32()

    CUTOFF_VERSION = 34

    large_preview_path = reader.cstring()
    
    if map_version <= CUTOFF_VERSION:
        reader.offset += 8
    else:
        reader.offset += 9

    fog_type = reader.cstring()

    tileset = reader.cstring()

    left, bottom, right, top = reader.fmt('<IIII', 4*4)
    assert left < right
    assert bottom < top
    assert top <= height
    assert right <= width

    # some kind of base height value
    reader.offset += 4

    load_screen_type = reader.i32()
    assert load_screen_type == 1

    load_screen_path_offset = reader.offset
    load_screen_path = reader.cstring()
    load_screen_path_offset_end = reader.offset

    load_screen_loadbar_type = reader.i16()
    if load_screen_loadbar_type == 0:
        load_screen_race = ''
    else:
        assert load_screen_loadbar_type == 4
        load_screen_race = reader.c4()
        assert load_screen_race in ('Terr', 'Prot', 'Zerg'), (filename, load_screen_race)

    load_screen_fit_offset = reader.offset
    load_screen_fit = reader.i32()

    load_text_position_type = reader.i32()

    load_text_offset_x, load_text_offset_y, load_text_size_x, load_text_size_y = reader.fmt('<IIII', 4*4)

    data_flags_offset = reader.offset
    data_flags = reader.i32()
    # 0x21 means you don't need to press anything after loading to start
    # print(f"{hex(data_flags):>8} | {filename}")

    unknown_int = reader.i32()
    # print(f"v{map_version} | {unknown_int} | {filename}")
    unknown_range = reader.nbytes(17)  # version >= 0x1f according to sc2reader
    # print(f"v{map_version} | {' '.join(prettyhex(x) for x in unknown_range)} | {filename}")
    # Measurements from last 'Zerg', 'Prot', 'Terr'
    # we are at: 3 * 16 + 1
    mystery_5b = b''
    if map_version == 0x1f:
        # see prophecy missions
        # 5 * 16 + 5 to player race
        pass
    elif map_version in (0x20, 0x22):
        # see death from above
        # see back in the saddle
        # normally 5 * 16 + 9 to player race
        num_strings = reader.i32()
        mystery_strings = []
        for _ in range(num_strings):
            string1 = reader.cstring()
            reader.offset += 8

            # print(f"{filename}: {string1}")
            mystery_strings.append(string1)
    elif map_version == 38:
        # see forbidden weapon
        # normally 5 * 16 + 14

        # see steps of the rite
        # possible string at 3*16 + 8, controlled by int(1) immediately preceding it
        # See templar's return for an example of 3 strings/structs preceded by int(3)
        reader.offset += 3

        num_strings = reader.i32()
        mystery_strings = []
        for _ in range(num_strings):
            string1 = reader.cstring()
            reader.offset += 12
            mystery_strings.append(string1)

        # see into the void
        # 3 * 16 + 8 holds a short length for the string path to loading music
        load_music_string_len = reader.i16()
        assert load_music_string_len < 100
        load_music_file = reader.nbytes(load_music_string_len).decode('utf-8')
    elif map_version == 39:
        # see haven's fall
        # normally 6 * 16

        # string in Brothers in Arms at 3*16+10, immediately preceded by int(1)
        mystery_5b = reader.nbytes(5)
        num_strings = reader.i32()
        mystery_strings = []
        for _ in range(num_strings):
            string1 = reader.cstring()
            reader.offset += 12
            mystery_strings.append(string1)

        # string in Amon's Fall at 3*16 + 12
        # interestingly, this is not a null-terminated string;
        # its length is controlled by a short immediately before
        load_music_string_len = reader.i16()
        assert load_music_string_len < 100
        load_music_file = reader.nbytes(load_music_string_len).decode('utf-8')
    else:
        assert False, "Unsupported map file version"

    num_players = reader.i32()
    players = []
    for _ in range(num_players):
        players.append(parse_player(reader))
    # The majority of the bytes remaining are always 0. Only Conviction and Sudden strike have non-zero bytes
    remaining = contents[reader.offset:]
    # if any(x for x in remaining if x != 0):
    #     print(f"v{map_version} | {''.join(prettyhex(x) for x in remaining)} | {filename}")

    return MapInfo(
        map_version,
        noise,
        width,
        height,
        small_preview_path,
        large_preview_path,
        fog_type,
        tileset,
        left,
        bottom,
        right,
        top,
        load_screen_path_offset,
        load_screen_path_offset_end,
        load_screen_fit_offset,
        load_screen_path,
        load_screen_race,
        load_screen_fit,
        data_flags_offset,
        data_flags,
        [x._asdict() for x in players],
    )

def analyze_file(filename: str) -> dict:
    with open(filename, 'rb') as fp:
        contents = fp.read()
    map_info = process_map_info(filename, contents)
    return map_info._asdict()

def modify_file(filename: str, new_bg: str) -> None:
    filename = f"Maps/ArchipelagoCampaign/{filename}"
    if not new_bg.lower().startswith("assets"):
        new_bg = f"Assets\\Textures\\{new_bg}"
    DESIRED_FIT = 1
    with open(filename, 'rb') as fp:
        contents = fp.read()
    map_info = process_map_info(filename, contents)
    if map_info.load_screen_path == new_bg and map_info.load_screen_fit == DESIRED_FIT:
        return
    
    path_offset = map_info.load_screen_path_offset

    # find the fit offset
    path_end_offset = map_info.load_screen_path_offset_end
    fit_offset = map_info.load_screen_fit_offset
    remaining_offset = fit_offset + 4

    new_contents = (
        contents[:path_offset]
        + new_bg.encode('utf-8') + b'\0'
        + contents[path_end_offset:fit_offset]
        + struct.pack('<I', DESIRED_FIT)
        + contents[remaining_offset:]
    )
    print(f"Writing {filename}")
    with open(filename, 'wb') as fp:
        fp.write(new_contents)

if __name__ == '__main__':
    result = {}
    # modify_file("HotS\\ap_rendezvous.SC2Map\\MapInfo", "ui_hots_loading_missionselect_zlab03.dds")
    # modify_file("HotS\\ap_harvest_of_screams.SC2Map\\MapInfo", "ui_hots_loading_missionselect_zkaldir01.dds")
    # modify_file("HotS\\ap_shoot_the_messenger.SC2Map\\MapInfo", "ui_hots_loading_missionselect_zkaldir01.dds")
    # modify_file("HotS\\ap_back_in_the_saddle.SC2Map\\MapInfo", "ui_hots_loading_missionselect_zlab02a.dds")
    # modify_file("HotS\\ap_lab_rat.SC2Map\\MapInfo", "ui_hots_loading_missionselect_zlab01.dds")
    # modify_file("WoL\\ap_zero_hour.SC2Map\\MapInfo", "loading-terran05.dds")
    # modify_file("WoL\\ap_the_outlaws.SC2Map\\MapInfo", "loading-marsarabarexterior.dds")
    # modify_file("WoL\\ap_all_in.SC2Map\\MapInfo", "loading-charbattlezone.dds")
    # modify_file("WoL\\ap_whispers_of_doom.SC2Map\\MapInfo", "loading-ulaan.dds")
    # modify_file("WoL\\ap_a_sinister_turn.SC2Map\\MapInfo", "loading-zhakuldas.dds")
    # modify_file("WoL\\ap_echoes_of_the_future.SC2Map\\MapInfo", "loading-aiur.dds")
    # modify_file("WoL\\ap_in_utter_darkness.SC2Map\\MapInfo", "loading-ulnar.dds")
    # modify_file("LotV\\ap_evil_awoken.SC2Map\\MapInfo", "ui_void_loading_prologue03.dds")
    # modify_file("LotV\\ap_the_growing_shadow.SC2Map\\MapInfo", "ui_void_loading_aiur02.dds")
    # modify_file("LotV\\ap_the_spear_of_adun.SC2Map\\MapInfo", "ui_void_loading_aiur03.dds")
    # modify_file("LotV\\ap_amon_s_reach.SC2Map\\MapInfo", "ui_void_loading_shakuras01.dds")
    # modify_file("LotV\\ap_last_stand.SC2Map\\MapInfo", "ui_void_loading_shakuras02.dds")
    # modify_file("LotV\\ap_forbidden_weapon.SC2Map\\MapInfo", "ui_void_loading_purifier01.dds")
    # modify_file("LotV\\ap_sky_shield.SC2Map\\MapInfo", "ui_void_loading_korhal01.dds")
    # modify_file("LotV\\ap_brothers_in_arms.SC2Map\\MapInfo", "ui_void_loading_korhal02.dds")
    # modify_file("LotV\\ap_the_infinite_cycle.SC2Map\\MapInfo", "ui_void_loading_ulnar02.dds")
    # modify_file("LotV\\ap_harbinger_of_oblivion.SC2Map\\MapInfo", "ui_void_loading_ulnar03.dds")
    # modify_file("LotV\\ap_steps_of_the_rite.SC2Map\\MapInfo", "ui_void_loading_taldarim01.dds")
    # modify_file("LotV\\ap_rak_shir.SC2Map\\MapInfo", "ui_void_loading_taldarim02.dds")
    # modify_file("LotV\\ap_unsealing_the_past.SC2Map\\MapInfo", "ui_void_loading_purifier02.dds")
    # modify_file("LotV\\ap_purification.SC2Map\\MapInfo", "ui_void_loading_purifier03.dds")
    # modify_file("LotV\\ap_templar_s_charge.SC2Map\\MapInfo", "ui_void_loading_alpha02.dds")
    # modify_file("LotV\\ap_templar_s_return.SC2Map\\MapInfo", "ui_void_loading_aiur04.dds")
    # modify_file("LotV\\ap_the_host.SC2Map\\MapInfo", "ui_void_loading_aiur05.dds")
    # modify_file("LotV\\ap_salvation.SC2Map\\MapInfo", "ui_void_loading_aiur06.dds")
    # modify_file("LotV\\ap_into_the_void.SC2Map\\MapInfo", "ui_void_loading_epilogue01.dds")
    # modify_file("LotV\\ap_the_essence_of_eternity.SC2Map\\MapInfo", "ui_void_loading_epilogue02.dds")
    # modify_file("LotV\\ap_amon_s_fall.SC2Map\\MapInfo", "ui_void_loading_epilogue03.dds")
    for file in map_info_files:
        result[file] = analyze_file(file)
    with open("mapinfos.json", 'w') as fp:
        json.dump(result, fp, indent=2)


