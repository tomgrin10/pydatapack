from pathlib import Path

import mcpack

from pydatapack.compiler import core
from examples import example


def main():
    pack = mcpack.DataPack("example", "Description")
    core.parse_module_to_datapack(pack, "pack", example)

    while True:
        try:
            pack.dump(
                Path.home() / r"AppData\Roaming\.minecraft\saves\Flat Testing\datapacks",
                overwrite=True)

            pack.dump(
                r"examples",
                overwrite=True)

            break
        except OSError:
            pass


if __name__ == "__main__":
    main()
