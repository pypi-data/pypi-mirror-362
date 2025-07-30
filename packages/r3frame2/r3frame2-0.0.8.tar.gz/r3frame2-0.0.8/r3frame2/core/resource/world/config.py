from ...atom import R3atom
import r3frame2 as r3

from r3frame2.core.resource.world.partition.config import R3gridConfig
from r3frame2.core.resource.world.partition.config import R3zoneConfig

class R3worldConfig(R3atom):
    def __init__(self, partition_config: R3gridConfig | R3zoneConfig):
        super().__init__()
        self.partition_config: R3gridConfig | R3zoneConfig = partition_config
