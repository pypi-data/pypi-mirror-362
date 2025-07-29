from pathlib import Path

from pydantic import BaseModel

from lite_dist2.type_definitions import TrialRepositoryType


class TrialRepositoryModel(BaseModel):
    type: TrialRepositoryType
    save_dir: Path
