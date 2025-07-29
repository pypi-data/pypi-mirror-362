from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from pydantic import BaseModel

from lite_dist2.curriculum_models.trial import Trial, TrialDoneRecord, TrialModel, TrialStatus
from lite_dist2.expections import LD2ParameterError
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace, ParameterAlignedSpaceModel
from lite_dist2.value_models.base_space import FlattenSegment
from lite_dist2.value_models.parameter_aligned_space_helper import remap_space, simplify

if TYPE_CHECKING:
    from datetime import datetime

    from lite_dist2.curriculum_models.mapping import Mapping
    from lite_dist2.value_models.point import ResultType


class TrialTableModel(BaseModel):
    trials: list[TrialModel]
    aggregated_parameter_space: dict[int, list[ParameterAlignedSpaceModel]] | None

    @staticmethod
    def create_empty() -> TrialTableModel:
        return TrialTableModel(
            trials=[],
            aggregated_parameter_space=None,
        )


class TrialTable:
    def __init__(
        self,
        trials: list[Trial],
        aggregated_parameter_space: dict[int, list[ParameterAlignedSpace]] | None,
    ) -> None:
        self.trials = trials
        self.aggregated_parameter_space = aggregated_parameter_space

    def is_not_defined_aps(self) -> bool:
        return self.aggregated_parameter_space is None

    def is_empty(self) -> bool:
        return self.is_not_defined_aps() or len(self.trials) == 0

    def register(self, trial: Trial) -> None:
        self.trials.append(trial)

    def receipt_trial_result(self, receipted_trial_id: str, worker_node_id: str) -> None:
        for trial in reversed(self.trials):
            if trial.trial_id != receipted_trial_id:
                continue
            if trial.worker_node_id != worker_node_id:
                p = "worker_node_id"
                t = "This trial is reserved by other worker"
                raise LD2ParameterError(p, t)
            if trial.trial_status == TrialStatus.done:
                p = "receipted_trial_id"
                t = f"Cannot override result of done trial(id={receipted_trial_id})"
                raise LD2ParameterError(p, t)

            # Normal
            trial.trial_status = TrialStatus.done
            trial.set_registered_timestamp()
            self.aggregated_parameter_space[self.trials[0].parameter_space.get_dim() - 1].extend(
                trial.parameter_space.to_aligned_list(),
            )
            return

        p = "receipted_trial_id"
        t = f"Not found trial that id={receipted_trial_id}"
        raise LD2ParameterError(p, t)

    def count_grid(self) -> int:
        return sum(
            trial.parameter_space.get_total() for trial in self.trials if trial.trial_status == TrialStatus.done
        )

    def count_trial(self) -> int:
        return len(self.trials)

    def simplify_aps(self) -> None:
        if self.aggregated_parameter_space is None:
            return

        dim = max(self.aggregated_parameter_space.keys()) + 1
        remapped_spaces: list[dict[int, list[ParameterAlignedSpace]]] = []
        for d in reversed(range(dim)):
            simplified = simplify(self.aggregated_parameter_space[d], d)
            remapped_spaces.append(remap_space(simplified, dim))

        self.aggregated_parameter_space = {
            d: list(itertools.chain.from_iterable(remapped_space[d] for remapped_space in remapped_spaces))
            for d in range(-1, dim)
        }

    def find_least_division(self, total_num: int | None) -> FlattenSegment:
        if self.aggregated_parameter_space is None:
            return FlattenSegment(0, None)

        aps_segments = [
            space.get_flatten_ambient_start_and_size()
            for spaces in self.aggregated_parameter_space.values()
            for space in spaces
        ]

        running_segments = simplify([segment for trial in self.trials for segment in trial.get_running_segments()])

        merged = simplify(aps_segments + running_segments)
        match len(merged):
            case 0:
                return FlattenSegment(0, None)
            case 1:
                start_index = merged[0].next_start_index()
                if total_num is None or start_index < total_num:
                    return FlattenSegment(start_index, None)
                return FlattenSegment(start_index, 0)
            case _:
                start = merged[0].next_start_index()
                return FlattenSegment(start, merged[1].get_start_index() - start)

    def init_aps(self, trial: Trial) -> None:
        self.aggregated_parameter_space = {i: [] for i in range(-1, trial.parameter_space.get_dim())}

    def find_target_value(self, target_value: ResultType) -> Mapping | None:
        # find_exact 用
        # NOTE: 並列処理してもよい
        for trial in self.trials:
            finding = trial.find_target_value(target_value)
            if finding:
                return finding
        return None

    def check_timeout_trial(self, now: datetime, timeout_seconds: int) -> list[str]:
        new_trials = []
        outdated_ids = []
        for trial in self.trials:
            if trial.trial_status != TrialStatus.running:
                new_trials.append(trial)
                continue
            delta_sec = trial.measure_seconds_from_registered(now)
            if delta_sec < timeout_seconds:
                # まだ期限内
                new_trials.append(trial)
            else:
                outdated_ids.append(trial.trial_id)
        self.trials = new_trials
        return outdated_ids

    def gen_done_record_list(self, cutoff_datetime: datetime) -> list[TrialDoneRecord]:
        return [trial.to_done_record() for trial in self.trials if trial.done_in_after(cutoff_datetime)]

    def to_model(self) -> TrialTableModel:
        if self.aggregated_parameter_space is None:
            aps = None
        else:
            aps = {d: [space.to_model() for space in spaces] for d, spaces in self.aggregated_parameter_space.items()}
        return TrialTableModel(
            trials=[trial.to_model() for trial in self.trials],
            aggregated_parameter_space=aps,
        )

    @staticmethod
    def from_model(model: TrialTableModel) -> TrialTable:
        if model.aggregated_parameter_space is None:
            aps = None
        else:
            aps = {
                d: [ParameterAlignedSpace.from_model(space) for space in spaces]
                for d, spaces in model.aggregated_parameter_space.items()
            }
        return TrialTable(
            trials=[Trial.from_model(trial) for trial in model.trials],
            aggregated_parameter_space=aps,
        )
