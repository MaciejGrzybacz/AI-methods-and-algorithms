from dataclasses import dataclass, asdict


@dataclass
class AlgorithmConfig:
    local_optimum_moves_threshold: int = 10
    local_optimum_escapes_max: int = -1  # -1 means "infinity"

    def asdict(self):
        return asdict(self)


DEFAULT_CONFIG = AlgorithmConfig()
