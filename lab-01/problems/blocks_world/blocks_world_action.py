from dataclasses import dataclass
from problems.blocks_world.blocks_world_state import BlocksWorldState
from copy import deepcopy

@dataclass
class BlocksWorldAction:
    column_from: int
    column_to: int

    def apply(self, state: BlocksWorldState) -> BlocksWorldState:
        new_columns = [list(col) for col in state.columns]
        block = new_columns[self.column_from].pop()
        new_columns[self.column_to].append(block)

        return BlocksWorldState(new_columns)
    
    def __str__(self) -> str:
        return f"move block from col: {self.column_from} to col: {self.column_to}"
