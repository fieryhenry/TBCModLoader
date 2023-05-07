import enum
from tbcml.core.game_data import pack
from tbcml.core import io, anim


class Engineer:
    def __init__(self, limit: "EngineerLimit", anim: "EngineerAnim"):
        self.limit = limit
        self.anim = anim

    @staticmethod
    def from_game_data(game_data: "pack.GamePacks") -> "Engineer":
        limit = EngineerLimit.from_game_data(game_data)
        anim = EngineerAnim.from_game_data(game_data)
        return Engineer(
            limit,
            anim,
        )

    def to_game_data(self, game_data: "pack.GamePacks"):
        self.limit.to_game_data(game_data)
        self.anim.to_game_data(game_data)

    @staticmethod
    def create_empty() -> "Engineer":
        return Engineer(
            EngineerLimit.create_empty(),
            EngineerAnim.create_empty(),
        )


class EngineerLimit:
    def __init__(self, limit: int):
        self.limit = limit

    @staticmethod
    def get_file_name() -> str:
        return "CastleCustomLimit.csv"

    @staticmethod
    def from_game_data(game_data: "pack.GamePacks") -> "EngineerLimit":
        file = game_data.find_file(EngineerLimit.get_file_name())
        if file is None:
            return EngineerLimit.create_empty()
        csv = io.bc_csv.CSV(file.dec_data)
        return EngineerLimit(
            int(csv.lines[0][0]),
        )

    def to_game_data(self, game_data: "pack.GamePacks"):
        file = game_data.find_file(EngineerLimit.get_file_name())
        if file is None:
            return None
        csv = io.bc_csv.CSV(file.dec_data)
        csv.lines[0][0] = str(self.limit)
        game_data.set_file(EngineerLimit.get_file_name(), csv.to_data())

    @staticmethod
    def create_empty() -> "EngineerLimit":
        return EngineerLimit(0)


class EngineerAnim:
    class FilePath(enum.Enum):
        IMGCUT = "castleCustom_researcher_001.imgcut"
        MAMODEL = "castleCustom_researcher_001.mamodel"
        SPRITE = "castleCustom_researcher_001.png"

        MAANIM_ACTION_L = "castleCustom_researcher_actionL.maanim"
        MAANIM_ACTION_R = "castleCustom_researcher_actionR.maanim"

        MAANIM_HAPPY = "castleCustom_researcher_happy.maanim"

        MAANIM_RUN_L = "castleCustom_researcher_runL.maanim"
        MAANIM_RUN_R = "castleCustom_researcher_runR.maanim"

        MAANIM_SUCESS_00 = "castleCustom_researcher_success00.maanim"
        MAANIM_SUCESS_01 = "castleCustom_researcher_success01.maanim"

        MAANIM_WAIT_L = "castleCustom_researcher_waitL.maanim"
        MAANIM_WAIT_R = "castleCustom_researcher_waitR.maanim"

        MAANIM_WALK_L = "castleCustom_researcher_walkL.maanim"
        MAANIM_WALK_R = "castleCustom_researcher_walkR.maanim"

        @staticmethod
        def get_all_maanims() -> list["EngineerAnim.FilePath"]:
            all_maanims: list["EngineerAnim.FilePath"] = []
            for maanim in EngineerAnim.FilePath:
                if maanim.value.endswith(".maanim"):
                    all_maanims.append(maanim)
            return all_maanims

        @staticmethod
        def get_all_maanims_names() -> list[str]:
            all_maanims: list[str] = []
            for maanim in EngineerAnim.FilePath:
                if maanim.value.endswith(".maanim"):
                    all_maanims.append(maanim.value)
            return all_maanims

    def __init__(self, model: "anim.model.Model"):
        self.model = model

    @staticmethod
    def from_game_data(game_data: "pack.GamePacks") -> "EngineerAnim":
        an = anim.model.Model.load(
            EngineerAnim.FilePath.MAMODEL.value,
            EngineerAnim.FilePath.IMGCUT.value,
            EngineerAnim.FilePath.SPRITE.value,
            EngineerAnim.FilePath.get_all_maanims_names(),
            game_data,
        )
        return EngineerAnim(an)

    def to_game_data(self, game_data: "pack.GamePacks"):
        self.model.save(game_data)

    @staticmethod
    def create_empty() -> "EngineerAnim":
        an = anim.model.Model.create_empty()
        return EngineerAnim(an)
