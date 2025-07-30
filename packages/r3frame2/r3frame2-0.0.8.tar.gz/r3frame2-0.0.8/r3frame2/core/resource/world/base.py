from ...atom import R3atom
from ...log import R3logger
from ...flags import R3flags
from ...globals import pg
from ...utils import div_v2i
import r3frame2 as r3

class R3world(R3atom):
    def __init__(self, app: "r3.app.R3app", config: "r3.resource.R3worldConfig") -> None:
        super().__init__()
        self.app: r3.app.R3app = app

        match type(config.partition_config):
            case r3.resource.R3gridConfig:
                self.partition: r3.resource.R3gridPartition = r3.resource.R3gridPartition(
                    config.partition_config.cell_size,
                    config.partition_config.world_origin
                )
            case r3.resource.R3zoneConfig:
                self.partition: r3.resource.R3zonePartition = r3.resource.R3zonePartition(
                    config.partition_config.cell_size,
                    config.partition_config.zone_size,
                    config.partition_config.world_origin
                )
            case _:
                R3logger.error(f"[R3world] invalid world partition configuration passed: (config){config}\n[R3world] application shutting down...\n")
                self.app.rem_flag(R3flags.app.RUNNING)
                return

        self._freeze()
        
    def _write_to_disk(self) -> None: pass
    def _read_from_disk(self) -> None: pass
