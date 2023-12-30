from tbcml import core
from typing import List, Union


class ModLoader:
    """
    The ModLoader class is responsible for loading and managing mods in the game.

    Args:
        country_code (CountryCode): The country code for the game.
        game_version (str | GameVersion): The version of the game.
        mod_instance (Mod): An instance of the Mod class.

    Attributes:
        country_code (CountryCode): The country code for the game.
        game_version (GameVersion): The version of the game.
        mod (Mod): An instance of the Mod class.
        game_packs (GamePacks): The game packs loaded from the APK.
        apk (Apk): The APK file used for loading mods.
        mods (List[Mod]): A list of mods.

    Methods:
        initialize(): Initializes the ModLoader by getting the APK file.
        add_cat(cat: Cat): Adds a cat to the mod.
        add_shop(shop: ItemShop): Adds an item shop to the mod.
        add_item(localizable: Localizable): Adds a localizable item to the mod.
        compile(open_path: bool): Compiles the APK with the loaded mods.

    """

    def __init__(
        self,
        country_code: "core.CountryCode",
        game_version: Union[str, "core.GameVersion"],
        mod_instance: "core.Mod",
    ):
        self.country_code = country_code
        if isinstance(game_version, str):
            self.game_version = core.GameVersion.from_string(game_version)
        else:
            self.game_version = game_version
        self.mod = mod_instance

        # not initialized in constructor
        self.game_packs = None
        self.apk = None
        self.mods = List[core.Mod]

    def initialize(self):
        self.__get_apk()

    def __get_apk(self):
        self.apk = core.Apk(
            game_version=self.game_version, country_code=self.country_code
        )
        self.apk.download()
        self.apk.extract()
        # older versions don't have server files
        try:
            self.apk.download_server_files()
        except:
            pass

        self.game_packs = core.GamePacks.from_apk(self.apk)

    def add_cat(self, cat: "core.Cat"):
        edit = core.ModEdit(["cats", cat.cat_id], cat.to_dict())

        self.__add_mod_edit(edit)

    def add_shop(self, shop: "core.ItemShop"):
        edit = core.ModEdit(["item_shop"], shop.to_dict())

        self.__add_mod_edit(edit)

    def add_localizable(self, localizable: "core.Localizable"):
        edit = core.ModEdit(["localizable"], localizable.to_dict())

        self.__add_mod_edit(edit)

    def __add_mod_edit(self, edit: "core.ModEdit"):
        self.mod.add_mod_edit(edit)

    def compile(self, open_path: bool):
        if self.apk is None:
            raise Exception("APK not initialized. Call initialize() first.")

        self.apk.load_mods([self.mod], self.game_packs)

        if open_path:
            self.apk.output_path.open()