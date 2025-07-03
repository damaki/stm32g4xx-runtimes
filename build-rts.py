# This script extends bb-runtimes to define the stm32g4xx target

import sys
import os
import pathlib

# Add bb-runtimes to the search path so that we can include and extend it
sys.path.append(str(pathlib.Path(__file__).parent / "bb-runtimes"))

import arm.cortexm
import build_rts
from support import add_source_search_path


class Stm32G4(arm.cortexm.CortexM4F):
    @property
    def name(self):
        return "stm32g4xx"

    @property
    def use_semihosting_io(self):
        return True

    @property
    def loaders(self):
        return ("ROM", "RAM")

    @property
    def system_ads(self):
        return {
            "light": "system-xi-arm.ads",
            "light-tasking": "system-xi-cortexm4-sfp.ads",
            "embedded": "system-xi-cortexm4-full.ads",
        }

    def __init__(self):
        super(Stm32G4, self).__init__()

        self.add_linker_script("stm32g4_src/ld/common-RAM.ld")
        self.add_linker_script("stm32g4_src/ld/common-ROM.ld")

        # Common source files
        self.add_gnat_sources(
            "bb-runtimes/arm/stm32/start-common.S",
            "bb-runtimes/arm/stm32/start-ram.S",
            "bb-runtimes/arm/stm32/start-rom.S",
            "stm32g4_src/setup_pll.ads",
            "stm32g4_src/setup_pll.adb",
            "stm32g4_src/s-bbpara.ads",
            "stm32g4_src/s-bbbopa.ads",
            "stm32g4_src/s-bbmcpa.ads",
            "stm32g4_src/svd/handler.S",
            "stm32g4_src/svd/i-stm32.ads",
            "stm32g4_src/svd/i-stm32-flash.ads",
            "stm32g4_src/svd/i-stm32-pwr.ads",
            "stm32g4_src/svd/i-stm32-rcc.ads",
        )

        self.add_gnarl_sources(
            "stm32g4_src/svd/a-intnam-G4A1.ads",
            "stm32g4_src/svd/a-intnam-G431.ads",
            "stm32g4_src/svd/a-intnam-G441.ads",
            "stm32g4_src/svd/a-intnam-G473.ads",
            "stm32g4_src/svd/a-intnam-G474.ads",
            "stm32g4_src/svd/a-intnam-G483.ads",
            "stm32g4_src/svd/a-intnam-G484.ads",
            "stm32g4_src/svd/a-intnam-G491.ads",
        )


def build_configs(target):
    if target == "stm32g4xx":
        return Stm32G4()
    else:
        assert False, "unexpected target: %s" % target

def patch_bb_runtimes():
    """Patch some parts of bb-runtimes to use our own targets and data"""
    add_source_search_path(os.path.dirname(__file__))

    build_rts.build_configs = build_configs

if __name__ == "__main__":
    patch_bb_runtimes()
    build_rts.main()