import json
from pathlib import Path

from lite_dist2.curriculum_models.trial import TrialModel, TrialStatus
from lite_dist2.trial_repositories.normal_trial_repository import NormalTrialRepository
from lite_dist2.value_models.aligned_space import ParameterAlignedSpaceModel
from lite_dist2.value_models.line_segment import LineSegmentModel
from tests.const import DT


def test_normal_trial_repository_get_repository_type() -> None:
    repo = NormalTrialRepository(Path("test/s01"))
    actual = repo.get_repository_type()
    expected = "normal"
    assert actual == expected


def test_normal_trial_repository_clean_save_dir_empty(tmp_path: str) -> None:
    save_dir = Path(tmp_path) / "some_study"

    # 空であることを確認
    assert not save_dir.exists()

    repo = NormalTrialRepository(save_dir)
    repo.clean_save_dir()
    assert save_dir.exists()
    assert save_dir.is_dir()
    assert not bool(list(save_dir.iterdir()))


def test_normal_trial_repository_clean_save_dir_filled(tmp_path: str) -> None:
    save_dir = Path(tmp_path) / "some_study"

    # 空であることを確認
    assert not save_dir.exists()

    # ディレクトリとファイルを作成する
    save_dir.mkdir(parents=False, exist_ok=False)
    dummy_file = save_dir / "dummy.txt"
    dummy_file.touch(exist_ok=False)
    assert bool(list(save_dir.iterdir()))

    repo = NormalTrialRepository(save_dir)
    repo.clean_save_dir()

    # 初期状態が空じゃなくても空になることを確認
    assert save_dir.exists()
    assert save_dir.is_dir()
    assert not bool(list(save_dir.iterdir()))


def test_normal_trial_repository_save(tmp_path: str) -> None:
    save_dir = Path(tmp_path) / "s01"
    trial_model = TrialModel(
        study_id="s01",
        trial_id="t01",
        reserved_timestamp=DT,
        trial_status=TrialStatus.running,
        const_param=None,
        parameter_space=ParameterAlignedSpaceModel(
            type="aligned",
            axes=[
                LineSegmentModel(
                    name="x",
                    type="int",
                    size="0x64",
                    step="0x1",
                    start="0x0",
                    ambient_size="0x64",
                    ambient_index="0x0",
                ),
            ],
            check_lower_filling=True,
        ),
        result_type="scalar",
        result_value_type="int",
        worker_node_id="n01",
        worker_node_name="n01",
        registered_timestamp=DT,
    )

    repo = NormalTrialRepository(save_dir)
    repo.clean_save_dir()

    # save
    repo.save(trial_model)

    # save されているか確認
    trial_file = save_dir / "t01.json"
    assert trial_file.exists()

    # マニュアル load
    with trial_file.open() as f:
        d = json.load(f)
        loaded_trial_model = TrialModel.model_validate(d)

    # 同じものか確認
    assert trial_model == loaded_trial_model


def test_normal_trial_repository_load(tmp_path: str) -> None:
    save_dir = Path(tmp_path) / "s01"
    trial_model = TrialModel(
        study_id="s01",
        trial_id="t01",
        reserved_timestamp=DT,
        trial_status=TrialStatus.running,
        const_param=None,
        parameter_space=ParameterAlignedSpaceModel(
            type="aligned",
            axes=[
                LineSegmentModel(
                    name="x",
                    type="int",
                    size="0x64",
                    step="0x1",
                    start="0x0",
                    ambient_size="0x64",
                    ambient_index="0x0",
                ),
            ],
            check_lower_filling=True,
        ),
        result_type="scalar",
        result_value_type="int",
        worker_node_id="n01",
        worker_node_name="n01",
        registered_timestamp=DT,
    )

    repo = NormalTrialRepository(save_dir)
    repo.clean_save_dir()

    # マニュアル save
    trial_file = save_dir / "t01.json"
    with trial_file.open("w") as f:
        d = trial_model.model_dump(mode="json")
        json.dump(d, f)

    # save されているか確認
    trial_file = save_dir / "t01.json"
    assert trial_file.exists()

    # load
    loaded_trial_model = repo.load("t01")

    # 同じものか確認
    assert trial_model == loaded_trial_model


def test_normal_trial_repository_load_all(tmp_path: str) -> None:
    save_dir = Path(tmp_path) / "s01"
    trial_models = [
        TrialModel(
            study_id="s01",
            trial_id=f"t0{i}",
            reserved_timestamp=DT,
            trial_status=TrialStatus.running,
            const_param=None,
            parameter_space=ParameterAlignedSpaceModel(
                type="aligned",
                axes=[
                    LineSegmentModel(
                        name="x",
                        type="int",
                        size="0x64",
                        step="0x1",
                        start="0x0",
                        ambient_size="0x64",
                        ambient_index="0x0",
                    ),
                ],
                check_lower_filling=True,
            ),
            result_type="scalar",
            result_value_type="int",
            worker_node_id="n01",
            worker_node_name="n01",
            registered_timestamp=DT,
        )
        for i in range(1, 4)
    ]

    # マニュアル save
    repo = NormalTrialRepository(save_dir)
    repo.clean_save_dir()
    for trial in trial_models:
        path = save_dir / f"{trial.trial_id}.json"
        with path.open("w") as f:
            json.dump(trial.model_dump(mode="json"), f)

    loaded_trials = repo.load_all()
    assert loaded_trials == trial_models


def test_normal_trial_repository_delete_save_dir_not_exist(tmp_path: str) -> None:
    save_dir = Path(tmp_path) / "some_study"

    # 空であることを確認
    assert not save_dir.exists()

    repo = NormalTrialRepository(save_dir)
    repo.delete_save_dir()

    assert not save_dir.exists()


def test_normal_trial_repository_delete_save_dir_exist(tmp_path: str) -> None:
    save_dir = Path(tmp_path) / "some_study"

    # 空であることを確認
    assert not save_dir.exists()

    # ディレクトリとファイルを作成する
    save_dir.mkdir(parents=False, exist_ok=False)
    dummy_file = save_dir / "dummy.txt"
    dummy_file.touch(exist_ok=False)
    assert bool(list(save_dir.iterdir()))

    repo = NormalTrialRepository(save_dir)
    repo.delete_save_dir()

    assert not save_dir.exists()
