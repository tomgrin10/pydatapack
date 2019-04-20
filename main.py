from pathlib import Path

import mcpack
import pydatapack.compiler.core as core
from examples import example

if __name__ == "__main__":
    pack = mcpack.DataPack("Pack", "Description")
    core.parse_module_to_datapack(pack, "pack", example)

    pack.dump(
        Path.home() / r"AppData\Roaming\.minecraft\saves\Superflat Testing\datapacks",
        overwrite=True)
