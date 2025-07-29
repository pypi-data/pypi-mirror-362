from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from lite_dist2.curriculum_models.curriculum import Curriculum, CurriculumModel
from lite_dist2.curriculum_models.mapping import Mapping, MappingsStorage
from lite_dist2.curriculum_models.study import Study
from lite_dist2.curriculum_models.study_portables import StudyModel, StudyStorage
from lite_dist2.curriculum_models.study_status import StudyStatus
from lite_dist2.curriculum_models.trial import Trial, TrialModel, TrialStatus
from lite_dist2.curriculum_models.trial_table import TrialTable, TrialTableModel
from lite_dist2.expections import LD2ParameterError
from lite_dist2.study_strategies import BaseStudyStrategy, StudyStrategyModel
from lite_dist2.study_strategies.all_calculation_study_strategy import AllCalculationStudyStrategy
from lite_dist2.suggest_strategies import BaseSuggestStrategy, SequentialSuggestStrategy, SuggestStrategyModel
from lite_dist2.suggest_strategies.base_suggest_strategy import SuggestStrategyParam
from lite_dist2.trial_repositories.normal_trial_repository import NormalTrialRepository
from lite_dist2.value_models.aligned_space import ParameterAlignedSpace
from lite_dist2.value_models.line_segment import ParameterRangeInt
from lite_dist2.value_models.point import ScalarValue
from tests.const import DT

if TYPE_CHECKING:
    from lite_dist2.trial_repositories.base_trial_repository import BaseTrialRepository
    from lite_dist2.value_models.base_space import ParameterSpace

_DUMMY_TRIAL_PATH_DIR = Path(__file__).parent

_DUMMY_PARAMETER_SPACE = ParameterAlignedSpace(
    axes=[
        ParameterRangeInt(name="x", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
        ParameterRangeInt(name="y", type="int", size=2, start=0, ambient_size=2, ambient_index=0),
    ],
    check_lower_filling=True,
)

_DUMMY_STUDY_STRATEGY_MODEL = StudyStrategyModel(type="all_calculation", study_strategy_param=None)
_DUMMY_SUGGEST_STRATEGY_MODEL = SuggestStrategyModel(
    type="sequential",
    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
)
_DUMMY_TRIAL_TABLE = TrialTable(
    trials=[
        Trial(
            study_id="01",
            trial_id="01",
            reserved_timestamp=DT,
            trial_status=TrialStatus.done,
            const_param=None,
            parameter_space=_DUMMY_PARAMETER_SPACE,
            result_type="scalar",
            result_value_type="float",
            worker_node_name="w01",
            worker_node_id="w01",
            results=[
                Mapping(
                    params=(
                        ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                        ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                    ),
                    result=ScalarValue(
                        type="scalar",
                        value_type="float",
                        value="0x1.0000000000000p-1",
                    ),
                ),
                Mapping(
                    params=(
                        ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                        ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                    ),
                    result=ScalarValue(
                        type="scalar",
                        value_type="float",
                        value="0x1.0000000000000p-2",
                    ),
                ),
            ],
        ),
        Trial(
            study_id="01",
            trial_id="01",
            reserved_timestamp=DT,
            trial_status=TrialStatus.running,
            const_param=None,
            parameter_space=_DUMMY_PARAMETER_SPACE,
            result_type="scalar",
            result_value_type="float",
            worker_node_name="w01",
            worker_node_id="w01",
        ),
    ],
    aggregated_parameter_space={
        -1: [],
        0: [_DUMMY_PARAMETER_SPACE],
    },
)

_DUMMY_TRIAL_REPOSITORY = NormalTrialRepository(save_dir=Path("test/01"))

_DUMMY_MAPPINGS_STORAGE = MappingsStorage(
    params_info=(),
    result_info=ScalarValue(type="scalar", value_type="int", value="0x0"),
    values=[],
)


class MockStudyStrategy(BaseStudyStrategy):
    def __init__(self) -> None:
        super().__init__(None)

    def extract_mappings(self, trial_table: TrialTable) -> list[Mapping]:
        pass

    def extract_mappings2(self, trial_repository: BaseTrialRepository) -> MappingsStorage:
        pass

    def is_done(
        self,
        trial_table: TrialTable,
        parameter_space: ParameterAlignedSpace,
        trial_repository: BaseTrialRepository,
    ) -> bool:
        pass

    def to_model(self) -> StudyStrategyModel:
        return _DUMMY_STUDY_STRATEGY_MODEL


class MockSuggestStrategy(BaseSuggestStrategy):
    def __init__(self) -> None:
        super().__init__(SuggestStrategyParam(strict_aligned=False), _DUMMY_PARAMETER_SPACE)

    def suggest(self, trial_table: TrialTable, max_num: int) -> ParameterSpace:
        pass

    def to_model(self) -> SuggestStrategyModel:
        return _DUMMY_SUGGEST_STRATEGY_MODEL


class MockStudy(Study):
    def __init__(self, study_id: str, done: bool) -> None:
        super().__init__(
            study_id,
            study_id,
            set(),
            StudyStatus.wait,
            DT,
            MockStudyStrategy(),
            MockSuggestStrategy(),
            None,
            _DUMMY_PARAMETER_SPACE,
            "scalar",
            "int",
            TrialTable([], None),
            _DUMMY_TRIAL_REPOSITORY,
        )
        self.study_id = study_id
        self._done = done

    def is_done(self) -> bool:
        return self._done

    def update_status(self) -> None:
        pass

    def to_storage(self) -> StudyStorage:
        return StudyStorage(
            study_id=self.study_id,
            name=self.study_id,
            required_capacity=set(),
            registered_timestamp=DT,
            study_strategy=self.study_strategy.to_model(),
            suggest_strategy=self.suggest_strategy.to_model(),
            const_param=None,
            parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
            done_timestamp=DT,
            result_type="scalar",
            result_value_type="int",
            results=_DUMMY_MAPPINGS_STORAGE,
            done_grids=4,
            trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
        )


@pytest.fixture
def done_study_fixture() -> MockStudy:
    return MockStudy(study_id="done_study", done=True)


@pytest.fixture
def not_done_study_fixture() -> MockStudy:
    return MockStudy(study_id="not_done_study", done=False)


def test_curriculum_to_storage_if_done(done_study_fixture: MockStudy, not_done_study_fixture: MockStudy) -> None:
    curriculum = Curriculum(
        studies=[done_study_fixture, not_done_study_fixture],
        storages=[],
        trial_file_dir=_DUMMY_TRIAL_PATH_DIR,
    )
    curriculum.to_storage_if_done()

    assert len(curriculum.studies) == 1
    assert len(curriculum.storages) == 1
    assert curriculum.studies[0].study_id == "not_done_study"
    assert curriculum.storages[0].study_id == "done_study"


@pytest.fixture
def sample_curriculum_fixture() -> Curriculum:
    studies = [
        Study.from_model(
            StudyModel(
                study_id="01",
                name="s1",
                required_capacity=set(),
                status=StudyStatus.running,
                registered_timestamp=DT,
                study_strategy=StudyStrategyModel(type="all_calculation", study_strategy_param=None),
                suggest_strategy=SuggestStrategyModel(
                    type="sequential",
                    suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
                ),
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                result_type="scalar",
                result_value_type="int",
                trial_table=TrialTableModel(
                    trials=[
                        TrialModel(
                            study_id="01",
                            trial_id="01",
                            reserved_timestamp=DT,
                            trial_status=TrialStatus.done,
                            const_param=None,
                            parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                            result_type="scalar",
                            result_value_type="float",
                            worker_node_name="w01",
                            worker_node_id="w01",
                            results=[
                                Mapping(
                                    params=(
                                        ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                        ScalarValue(type="scalar", value_type="int", value="0x0", name="y"),
                                    ),
                                    result=ScalarValue(
                                        type="scalar",
                                        value_type="float",
                                        value="0x1.0000000000000p-1",
                                    ),
                                ),
                                Mapping(
                                    params=(
                                        ScalarValue(type="scalar", value_type="int", value="0x0", name="x"),
                                        ScalarValue(type="scalar", value_type="int", value="0x1", name="y"),
                                    ),
                                    result=ScalarValue(
                                        type="scalar",
                                        value_type="float",
                                        value="0x1.0000000000000p-2",
                                    ),
                                ),
                            ],
                        ),
                        TrialModel(
                            study_id="01",
                            trial_id="01",
                            reserved_timestamp=DT,
                            trial_status=TrialStatus.running,
                            const_param=None,
                            parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                            result_type="scalar",
                            result_value_type="float",
                            worker_node_name="w01",
                            worker_node_id="w01",
                        ),
                    ],
                    aggregated_parameter_space={
                        -1: [],
                        0: [_DUMMY_PARAMETER_SPACE.to_model()],
                    },
                ),
                trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
            ),
        ),
    ]
    storages = [
        StudyStorage(
            study_id="s2",
            name="s2",
            required_capacity=set(),
            registered_timestamp=DT,
            study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
            suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
            const_param=None,
            parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
            done_timestamp=DT,
            result_type="scalar",
            result_value_type="int",
            results=_DUMMY_MAPPINGS_STORAGE,
            done_grids=4,
            trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
        ),
    ]
    return Curriculum(studies, storages, _DUMMY_TRIAL_PATH_DIR)


def test_curriculum_save_and_load(tmp_path: str, sample_curriculum_fixture: Curriculum) -> None:
    json_path = Path(f"{tmp_path}/curriculum.json")
    assert not json_path.exists()

    sample_curriculum_fixture.save(json_path)
    assert json_path.exists()

    with json_path.open("r", encoding="utf-8") as f:
        json_data = json.load(f)
    model = CurriculumModel.model_validate(json_data)
    assert model is not None

    loaded_curriculum = Curriculum.load_or_create(json_path)
    assert len(loaded_curriculum.studies) == len(sample_curriculum_fixture.studies)
    assert len(loaded_curriculum.storages) == len(sample_curriculum_fixture.storages)
    assert loaded_curriculum.studies[0].name == sample_curriculum_fixture.studies[0].name
    assert loaded_curriculum.storages[0].name == sample_curriculum_fixture.storages[0].name


def test_curriculum_load_or_create_empty(tmp_path: str) -> None:
    json_path = Path(f"{tmp_path}/non_existent.json")
    curriculum = Curriculum.load_or_create(json_path)

    assert isinstance(curriculum, Curriculum)
    assert len(curriculum.studies) == 0
    assert len(curriculum.storages) == 0


@pytest.mark.parametrize(
    ("retaining_capacity", "expected_study_id"),
    [
        pytest.param(
            {"hash", "preimage"},
            "hash_2",
            id="obtain running",
        ),
        pytest.param(
            {"hash"},
            "hash_1",
            id="obtain low required wait",
        ),
        pytest.param(
            {"mandelbrot"},
            None,
            id="obtain nothing",
        ),
    ],
)
def test_curriculum_get_available_study(retaining_capacity: set[str], expected_study_id: str | None) -> None:
    _study_param = {
        "name": "",
        "registered_timestamp": DT,
        "study_strategy": AllCalculationStudyStrategy(None),
        "suggest_strategy": SequentialSuggestStrategy(
            SuggestStrategyParam(strict_aligned=True),
            _DUMMY_PARAMETER_SPACE,
        ),
        "const_param": None,
        "parameter_space": _DUMMY_PARAMETER_SPACE,
        "result_type": "scalar",
        "result_value_type": "int",
        "trial_table": TrialTable.from_model(TrialTableModel.create_empty()),
        "trial_repository": NormalTrialRepository(save_dir=Path("test/s01")),
    }
    curriculum = Curriculum(
        studies=[
            Study(
                study_id="hash_1",
                required_capacity={"hash"},
                status=StudyStatus.wait,
                **_study_param,
            ),
            Study(
                study_id="hash_2",
                required_capacity={"hash", "preimage"},
                status=StudyStatus.running,
                **_study_param,
            ),
            Study(
                study_id="hash_3",
                required_capacity={"hash", "preimage"},
                status=StudyStatus.wait,
                **_study_param,
            ),
        ],
        storages=[],
        trial_file_dir=_DUMMY_TRIAL_PATH_DIR,
    )

    study = curriculum.get_available_study(retaining_capacity)
    assert (study.study_id if study is not None else None) == expected_study_id


@pytest.mark.parametrize(
    ("study_id", "name", "expected_id", "expected_storages"),
    [
        pytest.param(
            "xxx",
            "xxx",
            None,
            [
                StudyStorage(
                    study_id="s01",
                    name="n01",
                    required_capacity=set(),
                    registered_timestamp=DT,
                    study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                    suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                    done_timestamp=DT,
                    result_type="scalar",
                    result_value_type="int",
                    results=_DUMMY_MAPPINGS_STORAGE,
                    done_grids=4,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
                ),
                StudyStorage(
                    study_id="s02",
                    name="n02",
                    required_capacity=set(),
                    registered_timestamp=DT,
                    study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                    suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                    done_timestamp=DT,
                    result_type="scalar",
                    result_value_type="int",
                    results=_DUMMY_MAPPINGS_STORAGE,
                    done_grids=4,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
                ),
            ],
            id="None",
        ),
        pytest.param(
            "s01",
            None,
            "s01",
            [
                StudyStorage(
                    study_id="s02",
                    name="n02",
                    required_capacity=set(),
                    registered_timestamp=DT,
                    study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                    suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                    done_timestamp=DT,
                    result_type="scalar",
                    result_value_type="int",
                    results=_DUMMY_MAPPINGS_STORAGE,
                    done_grids=4,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
                ),
            ],
            id="id pickup",
        ),
        pytest.param(
            None,
            "n02",
            "s02",
            [
                StudyStorage(
                    study_id="s01",
                    name="n01",
                    required_capacity=set(),
                    registered_timestamp=DT,
                    study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                    suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                    done_timestamp=DT,
                    result_type="scalar",
                    result_value_type="int",
                    results=_DUMMY_MAPPINGS_STORAGE,
                    done_grids=4,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
                ),
            ],
            id="name pickup",
        ),
        pytest.param(
            "s01",
            "n02",
            "s01",
            [
                StudyStorage(
                    study_id="s02",
                    name="n02",
                    required_capacity=set(),
                    registered_timestamp=DT,
                    study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                    suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                    done_timestamp=DT,
                    result_type="scalar",
                    result_value_type="int",
                    results=_DUMMY_MAPPINGS_STORAGE,
                    done_grids=4,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
                ),
            ],
            id="prior id",
        ),
    ],
)
def test_curriculum_pop_storage(
    study_id: str | None,
    name: str | None,
    expected_id: str | None,
    expected_storages: list[StudyStorage],
) -> StudyStorage | None:
    curr = Curriculum(
        studies=[],
        storages=[
            StudyStorage(
                study_id="s01",
                name="n01",
                required_capacity=set(),
                registered_timestamp=DT,
                study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                done_timestamp=DT,
                result_type="scalar",
                result_value_type="int",
                results=_DUMMY_MAPPINGS_STORAGE,
                done_grids=4,
                trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
            ),
            StudyStorage(
                study_id="s02",
                name="n02",
                required_capacity=set(),
                registered_timestamp=DT,
                study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                done_timestamp=DT,
                result_type="scalar",
                result_value_type="int",
                results=_DUMMY_MAPPINGS_STORAGE,
                done_grids=4,
                trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
            ),
        ],
        trial_file_dir=_DUMMY_TRIAL_PATH_DIR,
    )

    popped = curr.pop_storage(study_id, name)
    if expected_id is None:
        assert popped is None
    else:
        assert popped.study_id == expected_id
    assert curr.storages == expected_storages


def test_curriculum_pop_storage_raises() -> None:
    curr = Curriculum(studies=[], storages=[], trial_file_dir=_DUMMY_TRIAL_PATH_DIR)
    with pytest.raises(LD2ParameterError):
        _ = curr.pop_storage(None, None)


@pytest.mark.parametrize(
    ("study_id", "name", "expected_cancel_result", "expected_studies"),
    [
        pytest.param(
            "s01",
            None,
            True,
            [
                Study(
                    study_id="s02",
                    name="n02",
                    required_capacity=set(),
                    status=StudyStatus.running,
                    registered_timestamp=DT,
                    study_strategy=AllCalculationStudyStrategy(_DUMMY_STUDY_STRATEGY_MODEL.study_strategy_param),
                    suggest_strategy=SequentialSuggestStrategy(
                        _DUMMY_SUGGEST_STRATEGY_MODEL.suggest_strategy_param,
                        _DUMMY_PARAMETER_SPACE,
                    ),
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE,
                    result_type="scalar",
                    result_value_type="int",
                    trial_table=_DUMMY_TRIAL_TABLE,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY,
                ),
            ],
            id="cancel by id",
        ),
        pytest.param(
            None,
            "n02",
            True,
            [
                Study(
                    study_id="s01",
                    name="n01",
                    required_capacity=set(),
                    status=StudyStatus.wait,
                    registered_timestamp=DT,
                    study_strategy=AllCalculationStudyStrategy(_DUMMY_STUDY_STRATEGY_MODEL.study_strategy_param),
                    suggest_strategy=SequentialSuggestStrategy(
                        _DUMMY_SUGGEST_STRATEGY_MODEL.suggest_strategy_param,
                        _DUMMY_PARAMETER_SPACE,
                    ),
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE,
                    result_type="scalar",
                    result_value_type="int",
                    trial_table=_DUMMY_TRIAL_TABLE,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY,
                ),
            ],
            id="cancel by name",
        ),
        pytest.param(
            "xxxx",
            None,
            False,
            [
                Study(
                    study_id="s01",
                    name="n01",
                    required_capacity=set(),
                    status=StudyStatus.wait,
                    registered_timestamp=DT,
                    study_strategy=AllCalculationStudyStrategy(_DUMMY_STUDY_STRATEGY_MODEL.study_strategy_param),
                    suggest_strategy=SequentialSuggestStrategy(
                        _DUMMY_SUGGEST_STRATEGY_MODEL.suggest_strategy_param,
                        _DUMMY_PARAMETER_SPACE,
                    ),
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE,
                    result_type="scalar",
                    result_value_type="int",
                    trial_table=_DUMMY_TRIAL_TABLE,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY,
                ),
                Study(
                    study_id="s02",
                    name="n02",
                    required_capacity=set(),
                    status=StudyStatus.running,
                    registered_timestamp=DT,
                    study_strategy=AllCalculationStudyStrategy(_DUMMY_STUDY_STRATEGY_MODEL.study_strategy_param),
                    suggest_strategy=SequentialSuggestStrategy(
                        _DUMMY_SUGGEST_STRATEGY_MODEL.suggest_strategy_param,
                        _DUMMY_PARAMETER_SPACE,
                    ),
                    const_param=None,
                    parameter_space=_DUMMY_PARAMETER_SPACE,
                    result_type="scalar",
                    result_value_type="int",
                    trial_table=_DUMMY_TRIAL_TABLE,
                    trial_repository=_DUMMY_TRIAL_REPOSITORY,
                ),
            ],
            id="Not found",
        ),
    ],
)
def test_curriculum_cancel_study(
    study_id: str | None,
    name: str | None,
    expected_cancel_result: bool,
    expected_studies: list[Study],
) -> None:
    curr = Curriculum(
        storages=[],
        studies=[
            Study(
                study_id="s01",
                name="n01",
                required_capacity=set(),
                status=StudyStatus.wait,
                registered_timestamp=DT,
                study_strategy=AllCalculationStudyStrategy(_DUMMY_STUDY_STRATEGY_MODEL.study_strategy_param),
                suggest_strategy=SequentialSuggestStrategy(
                    _DUMMY_SUGGEST_STRATEGY_MODEL.suggest_strategy_param,
                    _DUMMY_PARAMETER_SPACE,
                ),
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE,
                result_type="scalar",
                result_value_type="int",
                trial_table=_DUMMY_TRIAL_TABLE,
                trial_repository=_DUMMY_TRIAL_REPOSITORY,
            ),
            Study(
                study_id="s02",
                name="n02",
                required_capacity=set(),
                status=StudyStatus.running,
                registered_timestamp=DT,
                study_strategy=AllCalculationStudyStrategy(_DUMMY_STUDY_STRATEGY_MODEL.study_strategy_param),
                suggest_strategy=SequentialSuggestStrategy(
                    _DUMMY_SUGGEST_STRATEGY_MODEL.suggest_strategy_param,
                    _DUMMY_PARAMETER_SPACE,
                ),
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE,
                result_type="scalar",
                result_value_type="int",
                trial_table=_DUMMY_TRIAL_TABLE,
                trial_repository=_DUMMY_TRIAL_REPOSITORY,
            ),
        ],
        trial_file_dir=_DUMMY_TRIAL_PATH_DIR,
    )

    actual_cancel_result = curr.cancel_study(study_id, name)
    assert actual_cancel_result == expected_cancel_result

    assert len(curr.studies) == len(expected_studies)
    for actual_study, expected_study in zip(curr.studies, expected_studies, strict=True):
        assert actual_study.to_model() == expected_study.to_model()


def test_curriculum_cancel_study_raises() -> None:
    curr = Curriculum(studies=[], storages=[], trial_file_dir=_DUMMY_TRIAL_PATH_DIR)
    with pytest.raises(LD2ParameterError):
        _ = curr.cancel_study(None, None)


@pytest.mark.parametrize(
    ("study_id", "name", "expected"),
    [
        pytest.param("xxx", "xxx", StudyStatus.not_found, id="not_found"),
        pytest.param("s01", None, StudyStatus.done, id="done (storage) by id"),
        pytest.param(None, "n01", StudyStatus.done, id="done (storage) by name"),
        pytest.param("s04", None, StudyStatus.done, id="done (study) by id"),
        pytest.param(None, "n02", StudyStatus.running, id="running by name"),
        pytest.param("s03", None, StudyStatus.wait, id="wait by id"),
        pytest.param("s03", "n02", StudyStatus.wait, id="prior id"),
    ],
)
def test_curriculum_get_study_status(study_id: str | None, name: str | None, expected: StudyStatus) -> None:
    _study_args = {
        "required_capacity": {"hash"},
        "registered_timestamp": DT,
        "study_strategy": AllCalculationStudyStrategy(None),
        "suggest_strategy": SequentialSuggestStrategy(
            SuggestStrategyParam(strict_aligned=True),
            _DUMMY_PARAMETER_SPACE,
        ),
        "const_param": None,
        "parameter_space": _DUMMY_PARAMETER_SPACE,
        "result_type": "scalar",
        "result_value_type": "int",
        "trial_table": TrialTable.from_model(TrialTableModel.create_empty()),
        "trial_repository": NormalTrialRepository(save_dir=Path("test/s01")),
    }
    curr = Curriculum(
        studies=[
            Study(
                study_id="s02",
                name="n02",
                status=StudyStatus.running,
                **_study_args,
            ),
            Study(
                study_id="s03",
                name="n03",
                status=StudyStatus.wait,
                **_study_args,
            ),
            Study(
                study_id="s04",
                name="n04",
                status=StudyStatus.done,
                **_study_args,
            ),
        ],
        storages=[
            StudyStorage(
                study_id="s01",
                name="n01",
                required_capacity=set(),
                registered_timestamp=DT,
                study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                done_timestamp=DT,
                result_type="scalar",
                result_value_type="int",
                results=_DUMMY_MAPPINGS_STORAGE,
                done_grids=4,
                trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
            ),
        ],
        trial_file_dir=_DUMMY_TRIAL_PATH_DIR,
    )

    actual = curr.get_study_status(study_id, name)
    assert actual == expected


def test_curriculum_get_study_status_raises() -> None:
    curr = Curriculum(studies=[], storages=[], trial_file_dir=_DUMMY_TRIAL_PATH_DIR)
    with pytest.raises(LD2ParameterError):
        _ = curr.get_study_status(None, None)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("n01", False, id="storage: False"),
        pytest.param("n02", False, id="running: False"),
        pytest.param("n03", False, id="wait: False"),
        pytest.param("n04", False, id="done: False"),
        pytest.param("n07", True, id="unique name: True"),
        pytest.param(None, True, id="None: True"),
    ],
)
def test_curriculum_try_insert_study(name: str | None, expected: bool) -> None:
    _study_args = {
        "required_capacity": {"hash"},
        "registered_timestamp": DT,
        "study_strategy": AllCalculationStudyStrategy(None),
        "suggest_strategy": SequentialSuggestStrategy(
            SuggestStrategyParam(strict_aligned=True),
            _DUMMY_PARAMETER_SPACE,
        ),
        "const_param": None,
        "parameter_space": _DUMMY_PARAMETER_SPACE,
        "result_type": "scalar",
        "result_value_type": "int",
        "trial_table": TrialTable.from_model(TrialTableModel.create_empty()),
        "trial_repository": NormalTrialRepository(save_dir=Path("test/s01")),
    }
    curr = Curriculum(
        studies=[
            Study(
                study_id="s02",
                name="n02",
                status=StudyStatus.running,
                **_study_args,
            ),
            Study(
                study_id="s03",
                name="n03",
                status=StudyStatus.wait,
                **_study_args,
            ),
            Study(
                study_id="s04",
                name="n04",
                status=StudyStatus.done,
                **_study_args,
            ),
            Study(
                study_id="s05",
                name=None,
                status=StudyStatus.done,
                **_study_args,
            ),
        ],
        storages=[
            StudyStorage(
                study_id="s01",
                name="n01",
                required_capacity=set(),
                registered_timestamp=DT,
                study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                done_timestamp=DT,
                result_type="scalar",
                result_value_type="int",
                results=_DUMMY_MAPPINGS_STORAGE,
                done_grids=4,
                trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
            ),
            StudyStorage(
                study_id="s06",
                name=None,
                required_capacity=set(),
                registered_timestamp=DT,
                study_strategy=_DUMMY_STUDY_STRATEGY_MODEL,
                suggest_strategy=_DUMMY_SUGGEST_STRATEGY_MODEL,
                const_param=None,
                parameter_space=_DUMMY_PARAMETER_SPACE.to_model(),
                done_timestamp=DT,
                result_type="scalar",
                result_value_type="int",
                results=_DUMMY_MAPPINGS_STORAGE,
                done_grids=4,
                trial_repository=_DUMMY_TRIAL_REPOSITORY.to_model(),
            ),
        ],
        trial_file_dir=_DUMMY_TRIAL_PATH_DIR,
    )
    new_study = Study(
        name=name,
        study_id="s07",
        status=StudyStatus.running,
        **_study_args,
    )
    actual = curr.try_insert_study(new_study)
    assert actual == expected
