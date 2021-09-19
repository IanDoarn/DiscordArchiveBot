from typing import Dict, Hashable, Any, List


class Archive:

    config: Dict[Hashable, Any]

    # configured setting
    limit: int

    def __init__(self, config: Dict[Hashable, Any]):
        self.config = config["archive"]
        self.limit = self.config["message"]["limit"]


