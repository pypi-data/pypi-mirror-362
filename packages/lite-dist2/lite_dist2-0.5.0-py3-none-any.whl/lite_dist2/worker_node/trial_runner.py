from __future__ import annotations

import abc
import functools
from multiprocessing.pool import Pool
from typing import TYPE_CHECKING, Any

import tqdm

from lite_dist2.expections import LD2TypeError
from lite_dist2.type_definitions import ConstParamType

if TYPE_CHECKING:
    from collections.abc import Iterator

    from lite_dist2.config import WorkerConfig
    from lite_dist2.curriculum_models.trial import Trial
    from lite_dist2.type_definitions import RawParamType, RawResultType
    from lite_dist2.value_models.base_space import ParameterSpace


class BaseTrialRunner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def func(self, parameters: RawParamType, *args: object, **kwargs: object) -> RawResultType:
        pass

    @abc.abstractmethod
    def wrap_func(
        self,
        parameter_space: ParameterSpace,
        config: WorkerConfig,
        pool: Pool | None = None,
        *args: object,
        **kwargs: object,
    ) -> list[tuple[RawParamType, RawResultType]]:
        pass

    def parameter_pass_func(
        self,
        parameters: RawParamType,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> tuple[RawParamType, RawResultType]:
        return parameters, self.func(parameters, *args, **kwargs)

    def run(
        self,
        trial: Trial,
        config: WorkerConfig,
        pool: Pool | None = None,
        *args: object,
        **kwargs: object,
    ) -> Trial:
        raw_mappings = self.wrap_func(trial.parameter_space, config, pool, *args, **kwargs)
        mappings = trial.convert_mappings_from(raw_mappings)
        trial.set_result(mappings)
        return trial

    @staticmethod
    def get_typed[T](key: str, value_type: type[T], d: dict[str, object]) -> T:
        v = d.get(key)
        if isinstance(v, value_type):
            return v
        raise LD2TypeError(key, ConstParamType.__value__, type(v))


class AutoMPTrialRunner(BaseTrialRunner, metaclass=abc.ABCMeta):
    def wrap_func(
        self,
        parameter_space: ParameterSpace,
        config: WorkerConfig,
        _: Pool | None = None,
        *args: object,
        **kwargs: object,
    ) -> list[tuple[RawParamType, RawResultType]]:
        raw_mappings: list[tuple[RawParamType, RawResultType]] = []
        total = parameter_space.get_total()
        tqdm_kwargs = {"total": total, "disable": config.disable_function_progress_bar}
        if config.process_num is None or config.process_num > 1:
            parameter_pass_func = functools.partial(self.parameter_pass_func, args=args, kwargs=kwargs)
            with Pool(processes=config.process_num) as pool, tqdm.tqdm(**tqdm_kwargs) as p_bar:
                for arg_tuple, result_iter in pool.imap_unordered(
                    func=parameter_pass_func,
                    iterable=parameter_space.grid(),
                    chunksize=config.chunk_size,
                ):
                    raw_mappings.append((arg_tuple, result_iter))
                    p_bar.update(1)
            return raw_mappings
        return [
            self.parameter_pass_func(arg_tuple, args, kwargs)
            for arg_tuple in tqdm.tqdm(parameter_space.grid(), **tqdm_kwargs)
        ]


class SemiAutoMPTrialRunner(BaseTrialRunner, metaclass=abc.ABCMeta):
    def wrap_func(
        self,
        parameter_space: ParameterSpace,
        config: WorkerConfig,
        pool: Pool | None = None,
        *args: object,
        **kwargs: object,
    ) -> list[tuple[RawParamType, RawResultType]]:
        raw_mappings: list[tuple[RawParamType, RawResultType]] = []
        total = parameter_space.get_total()
        tqdm_kwargs = {"total": total, "disable": config.disable_function_progress_bar}
        if pool is not None:
            parameter_pass_func = functools.partial(self.parameter_pass_func, args=args, kwargs=kwargs)
            with tqdm.tqdm(**tqdm_kwargs) as p_bar:
                for arg_tuple, result_iter in pool.imap_unordered(
                    func=parameter_pass_func,
                    iterable=parameter_space.grid(),
                    chunksize=config.chunk_size,
                ):
                    raw_mappings.append((arg_tuple, result_iter))
                    p_bar.update(1)
            return raw_mappings
        return [
            self.parameter_pass_func(arg_tuple, args, kwargs)
            for arg_tuple in tqdm.tqdm(parameter_space.grid(), **tqdm_kwargs)
        ]


class ManualMPTrialRunner(BaseTrialRunner, metaclass=abc.ABCMeta):
    def func(self, *parameters: RawParamType) -> tuple[RawParamType, RawResultType]:
        pass

    @abc.abstractmethod
    def batch_func(
        self,
        raw_params: Iterator[RawParamType],
        config: WorkerConfig,
        *args: object,
        **kwargs: object,
    ) -> list[tuple[RawParamType, RawResultType]]:
        pass

    def wrap_func(
        self,
        parameter_space: ParameterSpace,
        config: WorkerConfig,
        _: Pool | None = None,
        *args: object,
        **kwargs: object,
    ) -> list[tuple[RawParamType, RawResultType]]:
        return self.batch_func(parameter_space.grid(), config, *args, **kwargs)
