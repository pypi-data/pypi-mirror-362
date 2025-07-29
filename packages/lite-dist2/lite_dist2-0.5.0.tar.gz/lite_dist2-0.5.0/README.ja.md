# lite_dist2
Simple distributed computing system

## 1. 概要
LiteDist2 は簡易的な分散処理システムです。LAN内に配置された３種類のノードを使用して処理を行います。

## 2. アーキテクチャ
### 管理ノード（Management Node）
`Study` の登録や結果の取得を行います。この動作は `TableNodeClient` に実装されているのでそれを使用してもいいですし 、
curl や talend などのAPIツールを使用することもできます（[API リファレンス](#7-api-リファレンス)を参照してください）。  
一連の処理の始まりと終わり（タスクの登録と結果の受け取り）を担う部分なので「クライアント」と呼んでもいいかもしれません。

### テーブルノード（Table Node）
`Study` を細切れにした `Trial` や `Study` をまとめた `Curriculum` を管理するノードです。`Trial` の提案とその結果の集約を行います。
このノードの台数は常に1台にしてください。このノードは実際に行われる計算タスクの実装を知る必要はありません。
従って、直接このリポジトリをクローンしてサーバを起動しても事足りますが、管理上はワーカーノードと揃えた方が望ましいでしょう。

### ワーカーノード（Worker Node）
テーブルノードから取得した `Trial` を実行し、結果をテーブルノードに返却します。
このノードは分散処理する関数を実装してある必要があります。
多くの場合、このライブラリを利用したプロジェクトのリポジトリが展開（クローンや Docker イメージの展開など）されているはずです。

### ノード間の通信
上記のノードは以下のように連携して動作します。
```mermaid
flowchart LR
    管理ノード -->|1 /study/register| テーブルノード
    管理ノード -->|4 /study| テーブルノード
    ワーカーノード -->|2 /trial/reserve| テーブルノード
    ワーカーノード -->|3 /trial/register| テーブルノード
```
数字は典型的な使い方でのAPIアクセスの順番を表しています。
1. 管理ノードがテーブルノードに `Study` を登録する（/study/register）
2. ワーカーノードがその `Study` から生成される `Trial` を取得（/trial/reserve）して、実行する
3. ワーカーノードが完了した `Trial` をテーブルノードに登録する（/trial/register）
4. 2~3を終了するまで繰り返したら、最後に結果を取得する（/study）

## 3. 主要概念
LiteDist2 を説明する際にはいくつかの用語が必要です。既に出てきた `Study`、`Trial` がそれです。
このセクションではそれらの用語について説明します。

### Curriculum
複数の `Study` を束ねたもので、実行予定、実行中、実行済みのタスクの一覧です。テーブルノード全体の状態とも言います。
/study/register で `Curriculum` に `Study` を追加し、/study でポップされます。  
テーブルノードは定期的にこのオブジェクトをバックアップします。

### Study
ワーカーノードを使って処理する大きなタスクのことです。
必ず１次元以上のパラメータ空間を持ち、その空間内のグリッドの座標がワーカーノードに与えられ、所定の計算を行います。
１つのテーブルノードで、複数種類の計算を実行させることも可能で、その場合は `Study` に `required_capacity: list[str]` を設定します。
ワーカノードも同様に自分が実行できる計算の種類を `retaining_capacity: list[str]` として宣言することができ、
これにより各ノードの能力に応じたタスクを実行させることができます。

### Trial
`Study` を分割したタスクの一部です。１つの `Trial` は必ず１つのワーカーノードで実行されます。
ワーカーノードでは `TrialRunner` で与えられた `Trial` を実行します。その後、 `Trial` に結果を追加してテーブルノードに送り返されます。
`Trial` に含まれるグリッドの数は /trial/reserve で取得する際に送信する `max_size: int` で変更できます。

### ParameterSpace
ワーカーノードが計算する際の引数の組を生成する空間のことです。パラメータ空間は必ず１つ以上の次元を持ちます。
例えば、以下の例は３つの次元を持つ `ParameterSpace` の定義です。（数値の表し方については [PortableValueType](#portablevaluetype) を参照）
```json
{
  "type": "aligned",
  "axes": [
    {"type": "bool", "name": "x", "size": "0x2", "step": "0x1", "start": false},
    {"type": "int", "name": "y", "size": "0x65", "step": "0x1", "start": "-0x32"},
    {"type": "float", "name": "y", "size": "0xc8", "step": "0x1.0p-2", "start": "0x0p+0"}
  ]
}
```
これは「x は ブール値の `True` か `False`、 y は整数の `-50` から `50` まで `1` 刻み、z は浮動小数の `0.0` から `50.0` まで `0.25` 刻み」を意味します。
この場合、パラメータ空間では 2\*101\*200 = 40400 個のグリッドがあることになります。
具体的な `ParameterSpace` の実装については [ParameterSpace の実装について](#parameterspace-の実装について) を参照してください。

### PortableValueType
上記のように JSON 内で利用できる数値は文字列かブール値のみ許可されています。つまり、ブール値はそのまま利用できますが、整数値は hex 表記しなければなりません。
これは異なる処理系を間に挟んでも、値が正確に表せるようにするためです。  
通常の型とこれらの `PortableValueType` への相互変換には以下の関数が利用できます。
```python
from lite_dist2.common import numerize, portablize

n = 0.24
p = portablize("float", n)  # "0x1.eb851eb851eb8p-3"
assert n == numerize("float", p)
```

### StudyStrategy
分散処理の種別によって処理の終了条件や結果の取得方法が変わったりします。
用途に適した運用ができるように LiteDist2 では以下の3つの `StudyStrategy` を用意しています。
- `all_calculation`: 与えられたパラメータ空間全体にわたって所定の計算を行う。
- `find_exact`: ある関数の値が特定の値になるようなパラメータの組を探す。（ハッシュ関数の原像生成など）
- `minimize`: **未実装**。ある関数の値が最小になるようなパラメータの組を探す。（機械学習のハイパーパラメータチューニングなど）

`all_calculation` の例は次の通りです。`all_calculation` では必要なパラメータはありません。
```json
{
  "type": "all_calculation",
  "study_strategy_param": null
}
```
`find_exact` の例は次の通りです。こちらの例ではパラメータとして目標となる値、 `target_value` が必要です。
```json
{
  "type": "find_exact",
  "study_strategy_param": {"target_value": "aff97160474a056e838c1f721af01edf"}
}
```

### SuggestStrategy
それぞれのワーカーノードに対して `Trial` としてどの部分空間を割り当てるかは一意には定まりません。
これを司るのが `SuggestStrategy` です。現在、以下の２種類が用意されています。
- `sequential`: パラメータ空間の最初から順番に割り当てる。
- `random`: **未実装**。パラメータ空間内をランダムに選んで割り当てる。

`sequential` 例は次の通りです。`strict_aligned: true` を指定することで [`ParameterAlignedSpace`](#parameteralignedspace) の使用を強制できます。
```json
{
  "type": "sequential",
  "suggest_strategy_param": {"strict_aligned": true}
}
```

### TrialRunner
ワーカーノードで `Trial` を実行するクラスのことです。このクラスは利用者が望む処理を実行するようにカスタマイズする必要があります。
具体的には `BaseTrialRunner` を実装する必要があります。`example/generate_mandelbrot_set.py` では次のように実装しています。

```python
from lite_dist2.type_definitions import RawParamType, RawResultType
from lite_dist2.worker_node.trial_runner import AutoMPTrialRunner


class Mandelbrot(AutoMPTrialRunner):
    _ABS_THRESHOLD = 2.0
    _MAX_ITER = 255

    def func(self, parameters: RawParamType, *args: tuple, **kwargs: dict) -> RawResultType:
        x = float(parameters[0])
        y = float(parameters[1])
        c = complex(x, y)
        z = complex(0, 0)
        iter_count = 0
        while abs(z) <= self._ABS_THRESHOLD and iter_count < self._MAX_ITER:
            z = z ** 2 + c
            iter_count += 1
        return iter_count
```
ここでは `BaseTrialRunner` に手を加えて自動でマルチプロセス処理を行ってくれる `AutoMPTrialRunner` という抽象クラスを利用しています。
注目すべきポイントは `func` メソッドの引数と戻り値の型です。**`func` メソッドの引数と戻り値の型は必ずこの形式に準拠する必要があります。**  
引数は `parameters: RawParamType` で、パラメータの組の `tuple` です（例えば `(-0.5, 1.4)` など）。
一方で戻り値は `RawResultType` となっています。これは計算された値です（例えば `15` など）。戻り値がベクトル量の場合は `(1.2, 4)` のような `tuple` を利用することが可能です。  
他の引数である `args` や `kwargs` は何らかの定数を渡したい時に利用でき、後述する `worker.start()` メソッドから値を代入できます。
`BaseTrialRunner` の実装については `AutoMPTrialRunner` の他にも `SemiAutoMPTrialRunner`、`ManualMPTrialRunner` があります。
詳細は [高度な TrialRunner の実装](#高度な-trialrunner-の実装) を参照してください。

## 4. インストール方法
### 必要要件
- Python >= 3.13

### 推奨要件
- uv >= 0.7.0

### インストール手順
```commandline
uv add lite-dist2
```
あるいは
```commandline
pip install lite-dist2
```

## 5. 使用方法
> [!CAUTION]  
> グローバルIPが必要な環境では使用できません。必ずLAN内で使用してください。  
> また、テーブルノードはIPをLAN内に開放しているので、必ず信頼できるネットワーク内でのみ利用してください。

`example/generate_mandelbrot_set.py` で基本的な使用例を紹介します。このセクションでは API のリファレンスやスキーマについては説明しないので、
知りたい場合は [7. API リファレンス](#7-api-リファレンス) や [8. API のスキーマ](#8-api-のスキーマ) を参照してください。

### TrialRunner の実装
[TrialRunner の説明](#trialrunner) や [高度な TrialRunner の実装](#高度な-trialrunner-の実装) を参考にしながら、
あなたのプロジェクトで `TrialRunner` を実装してください。そのプロジェクトが各ノード（少なくとも各ワーカーノード）で動くことになります。

### テーブルノードの起動
このライブラリかあるいはこのライブラリを利用したあなたのプロジェクトをテーブルノードにデプロイします。デプロイされたテーブルノードでは以下のコマンドでサーバを起動できます。
```shell
uv run start-table
```
あるいはこのライブラリがインストールされた仮想環境内であれば単に
```shell
start-table
```
で起動できます。このとき、
```text
$ uv run start-table
INFO:lite_dist2.table_node_api.start_table_api:Table Node IP: xxx.xxx.xxx.xxx
INFO:     Started server process [17836]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
のような表示がされます。`Table Node IP: xxx.xxx.xxx.xxx` の部分がこのノードのプライベートIPです。**続くワーカーノードの起動ではこの値を利用します。**  

テーブルノードの設定ファイルがもし所定のパス（`your_project_root/table_config.json`）にあれば起動時に読み込みます。
無ければ起動前に作成され、デフォルト値が書き込まれます。この値は起動コマンドの `-c` オプションで変更できます。
```shell
uv run start-table -c path/to/table_config.json
```

### Study の登録
管理ノードからテーブルノードに /study/register で `Study` を登録します。登録は Python でクライアントクラスを経由して行う方法と、curl などの API ツールを使用する方法があります。  
Python の場合:
```python
from lite_dist2.common import float2hex, int2hex
from lite_dist2.curriculum_models.study_portables import StudyRegistry
from lite_dist2.study_strategies import StudyStrategyModel
from lite_dist2.suggest_strategies import SuggestStrategyModel
from lite_dist2.suggest_strategies.base_suggest_strategy import SuggestStrategyParam
from lite_dist2.table_node_api.table_param import StudyRegisterParam
from lite_dist2.value_models.aligned_space_registry import LineSegmentRegistry, ParameterAlignedSpaceRegistry
from lite_dist2.worker_node.table_node_client import TableNodeClient

_resolution = 10
_half_size = 2.0

study_register_param = StudyRegisterParam(
    study=StudyRegistry(
        name="mandelbrot",
        required_capacity=set(),
        study_strategy=StudyStrategyModel(type="all_calculation", study_strategy_param=None),
        suggest_strategy=SuggestStrategyModel(
            type="sequential",
            suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
        ),
        result_type="scalar",
        result_value_type="int",
        const_param=None,
        parameter_space=ParameterAlignedSpaceRegistry(
            type="aligned",
            axes=[
                LineSegmentRegistry(
                    name="x",
                    type="float",
                    size=int2hex(_resolution),
                    step=float2hex(2 * _half_size / _resolution),
                    start=float2hex(-1 * _half_size),
                ),
                LineSegmentRegistry(
                    name="y",
                    type="float",
                    size=int2hex(_resolution),
                    step=float2hex(2 * _half_size / _resolution),
                    start=float2hex(-1 * _half_size),
                ),
            ],
        ),
    ),
)
client = TableNodeClient("xxx.xxx.xxx.xxx", port=8000)
client.register_study(study_register_param)
```
curl の場合:
```shell
curl -X POST -H "Content-Type: application/json" \
-d '{
  "study": {
    "name": "mandelbrot",
    "required_capacity": [],
    "study_strategy": {"type": "all_calculation", "study_strategy_param": null},
    "suggest_strategy": {
      "type": "sequential",
      "suggest_strategy_param": {"strict_aligned": true}
    },
    "result_type": "scalar",
    "result_value_type": "int",
    "parameter_space": {
      "type": "aligned",
      "axes": [
        {"name": "x", "type": "float", "size": "0xa", "step": "0x1.999999999999ap-2", "start": "-0x1.0000000000000p+1"},
        {"name": "y", "type": "float", "size": "0xa", "step": "0x1.999999999999ap-2", "start": "-0x1.0000000000000p+1"}
      ]
    }
  }
}' xxx.xxx.xxx.xxx:8000/study/register
```
`xxx.xxx.xxx.xxx` にはテーブルノードのプライベート IP を指定してください。

### ワーカーノードの起動
あなたのプロジェクトをワーカーノードにデプロイします。

```python
from lite_dist2.config import WorkerConfig
from lite_dist2.worker_node.worker import Worker
from lite_dist2.type_definitions import RawParamType, RawResultType
from lite_dist2.worker_node.trial_runner import AutoMPTrialRunner

class Mandelbrot(AutoMPTrialRunner):
    def func(self, parameters: RawParamType, *args: tuple, **kwargs: dict) -> RawResultType:
        ...

worker_config = WorkerConfig(
    name="w_01",
    process_num=2,
    max_size=10,
    wait_seconds_on_no_trial=5,
    table_node_request_timeout_seconds=60,
)
worker = Worker(
    trial_runner=Mandelbrot(),
    ip="xxx.xxx.xxx.xxx",
    port=8000,
    config=worker_config,
)
worker.start()
```
実装した `TrialRunner` と `WorkerConfig` を `Worker` に渡した後、`worker.start()` を実行すればそのワーカーノードは自動でテーブルノードから `Trial` を取得して実行します。
`WorkerConfig` の具体的な設定については [WorkerConfig](#workerconfig) を参照してください。

### 結果の取得
`Study` の完了如何にかかわらず、/study で `Study` を取得できます。
`Study` の特定は /study/register の際に発行される `study_id` か、/study/register のパラメータとしてあなたが指定した `name` のどちらかが使用できます。
この工程も同様に Python でクライアントクラスを経由して行う方法と、curl などの API ツールを使用する方法があります。  
Python の場合:
```python
from lite_dist2.worker_node.table_node_client import TableNodeClient
client = TableNodeClient("xxx.xxx.xxx.xxx", port=8000)
study = client.study(name="mandelbrot")
```

curl の場合:
```shell
curl 'xxx.xxx.xxx.xxx:8000/study?name=mandelbrot'
```
`Study` がまだ実行中の場合は次のようなレスポンスが得られるはずです。ステータスコードは 202 です。
```json
{"status": "running", "result": null}
```
終了していた場合は `"status": "done"` になり、`result` に実行結果が格納されます。

### 結果の見方
/study で取得した結果は次のような形式です（`results.values` は１つだけ表示しています）。

```json
{
  "name": "mandelbrot",
  "required_capacity": [],
  "study_strategy": {
    "type": "all_calculation",
    "study_strategy_param": null
  },
  "suggest_strategy": {
    "type": "sequential",
    "suggest_strategy_param": {
      "strict_aligned": true
    }
  },
  "result_type": "scalar",
  "result_value_type": "int",
  "study_id": "b4fed0ba-394d-11f0-b30f-e8d45b580c23",
  "registered_timestamp": "2025-05-25T18:50:36.034909+09:00",
  "parameter_space": {
    "type": "aligned",
    "axes": [
      {
        "name": "x",
        "type": "float",
        "size": "0xa",
        "step": "0x1.999999999999ap-2",
        "start": "-0x1.0000000000000p+1",
        "ambient_index": "0x0",
        "ambient_size": "0xa",
        "is_dummy": false
      },
      {
        "name": "y",
        "type": "float",
        "size": "0xa",
        "step": "0x1.999999999999ap-2",
        "start": "-0x1.0000000000000p+1",
        "ambient_index": "0x0",
        "ambient_size": "0xa",
        "is_dummy": false
      }
    ],
    "check_lower_filling": true
  },
  "done_timestamp": "2025-05-25T18:50:42.078755+09:00",
  "results": {
    "params_info": [
      {
        "type": "scalar",
        "value_type": "float",
        "value": "0x0.0p+0",
        "name": "x"
      },
      {
        "type": "scalar",
        "value_type": "float",
        "value": "0x0.0p+0",
        "name": "y"
      }
    ],
    "result_info": {
      "type": "scalar",
      "value_type": "int",
      "value": "0x0",
      "name": null
    },
    "values": [
      [
        "-0x1.0000000000000p+1",
        "-0x1.0000000000000p+1",
        "0x0"
      ]
    ]
  },
  "done_grids": 100
}
```
`results` に注目すると、`param_info` と `result_info` が含まれていることが分かります。これらは入力と出力の型情報で、値はダミーです。
実際の値は `results.values` に格納されたおり、param と result が順番に並んでいます。上の例では先頭から順に `x`, `y`, `result` です。

## 6. 設定
### TableConfig
| 名前                               | 型    | デフォルト値                           | 説明                               |
|----------------------------------|------|----------------------------------|----------------------------------|
| port                             | int  | 8000                             | テーブルノードが使用するポート番号                |
| trial_timeout_seconds            | int  | 600                              | `Trial` が予約されてから登録されるまでのタイムアウト時間 |
| timeout_check_interval_seconds   | int  | 60                               | `Trial` のタイムアウトを確認する間隔           |
| curriculum_path                  | Path | {project root}/"curriculum.json" | `Curriculum` を保存する際のファイルパス       |
| trial_file_dir                   | Path | {project root}/"trials"          | `Trial` を保存する際のファイルパス            |
| curriculum_save_interval_seconds | int  | 600                              | `Curriculum` を保存する時間間隔           |

### WorkerConfig
| 名前                                 | 型           | デフォルト値 | 説明                                                                                        |
|------------------------------------|-------------|--------|-------------------------------------------------------------------------------------------|
| name                               | str \| None | None   | ワーカーノードの名前。                                                                               |
| process_num                        | int \| None | None   | `AutoMPTrialRunner` を使用した際に生成されるプロセス数。`None` であれば `os.cpu_count()` の値を利用する。               |
| chunk_size                         | int         | 1      | プロセスに渡すチャンクのサイズ。`AutoMPTrialRunner` 及び `SemiAutoMPTrialRunner` を使用した際に有効になる。              |
| max_size                           | int         | 1      | `Trial` の最大サイズ。`SuggestStrategy` で `"strict_aligned": true` を設定していた場合、これより小さいサイズになることがある。 |
| disable_function_progress_bar      | bool        | False  | 進捗バーを非表示にするかどうか。                                                                          |
| retaining_capacity                 | list[str]   | []     | そのワーカーノードが持っている能力をタグ(内部的な型は `set[str]`)。１つのテーブルノードで複数種類の `Study` を処理するときに利用する。            |
| wait_seconds_on_no_trial           | int         | 5      | テーブルノードに実行できる `Study` が無かった際に次の `Trial` 取得を待機する時間。                                        |
| table_node_request_timeout_seconds | int         | 30     | テーブルノードに対するリクエストのタイムアウト時間。                                                                |

## 7. API リファレンス
| パス               | メソッド   | パラメータ                                                                             | ボディ                                       | レスポンス                                                   | 説明                      |
|------------------|--------|-----------------------------------------------------------------------------------|-------------------------------------------|---------------------------------------------------------|-------------------------|
| /ping            | GET    | なし                                                                                | なし                                        | [OkResponse](#okresponse)                               | 死活監視用API                |
| /save            | GET    | なし                                                                                | なし                                        | [OkResponse](#okresponse)                               | `Curriculum` を保存する      |
| /status          | GET    | なし                                                                                | なし                                        | [CurriculumSummaryResponse](#curriculumsummaryresponse) | `Curriculum` の概要情報を取得する |
| /status/progress | GET    | `cutoff_sec`: 終了予想時刻推定に利用する集計期間。デフォルト値は600                                        | なし                                        | [ProgressSummaryResponse](#progresssummaryresponse)     | 実行中の `Study` の進捗状況を表示する |
| /study/register  | POST   | なし                                                                                | [StudyRegisterParam](#studyregisterparam) | [StudyRegisteredResponse](#studyregisteredresponse)     | `Study` を登録する           |
| /trial/reserve   | POST   | なし                                                                                | [TrialReserveParam](#trialreserveparam)   | [TrialReserveResponse](#trialreserveresponse)           | `Trial` を予約する           |
| /trial/register  | POST   | なし                                                                                | [TrialRegisterParam](#trialregisterparam) | [OkResponse](#okresponse)                               | 完了した `Trial` を登録する      |
| /study           | GET    | `study_id`: 取得したい `Study` のID<br>`name`: 取得したい `Study` の名前<br>※どちらか一方のみ指定可能       | なし                                        | [StudyResponse](#studyresponse)                         | `Study` の情報を取得する        |
| /study           | DELETE | `study_id`: キャンセルしたい `Study` のID<br>`name`: キャンセルしたい `Study` の名前<br>※どちらか一方のみ指定可能 | なし                                        | [OkResponse](#okresponse)                               | `Study` をキャンセルする        |

## 8. API のスキーマ
### StudyRegisterParam
| 名前    | 型                               | 必須 | 説明            |
|-------|---------------------------------|----|---------------|
| study | [StudyRegistry](#studyregistry) | ✓  | 登録する `Study`。 |

### TrialReserveParam
| 名前                 | 型           | 必須 | 説明                                         |
|--------------------|-------------|----|--------------------------------------------|
| retaining_capacity | list[str]   | ✓  | そのワーカーノードが対応できるタスクの種類 (内部的な型は `set[str]`)。 |
| max_size           | int         | ✓  | 予約するパラメータ空間の最大サイズ。                         |
| worker_node_name   | str \| None |    | ワーカーノードの名前。                                |
| worker_node_id     | str         |    | ワーカーノードのID。                                |

### TrialRegisterParam
| 名前    | 型                         | 必須 | 説明                    |
|-------|---------------------------|----|-----------------------|
| trial | [TrialModel](#trialmodel) | ✓  | テーブルノードに登録する `Trial`。 |

### TrialReserveResponse
| 名前    | 型                                 | 必須 | 説明                                                                                 |
|-------|-----------------------------------|----|------------------------------------------------------------------------------------|
| trial | [TrialModel](#trialmodel) \| None |    | そのワーカーノードに対して予約された `Trial`。`Curriculum` が空か、そのワーカーノードで対応できる `Trial` がない場合は `None`。 |

### StudyRegisteredResponse
| 名前       | 型   | 必須 | 説明                          |
|----------|-----|----|-----------------------------|
| study_id | str | ✓  | 登録された `Study` に対して発行された ID。 |

### StudyResponse
| 名前     | 型                                     | 必須 | 説明                                                          |
|--------|---------------------------------------|----|-------------------------------------------------------------|
| status | [StudyStatus](#studystatus-enum)      | ✓  | 対象の `Study` の状態。                                            |
| result | [StudyStorage](#studystorage) \| None |    | 完了した `Study` の結果。もし対象の `Study` が完了していないか見つからなかった場合は `None`。 |

### CurriculumSummaryResponse
| 名前        | 型                                   | 必須 | 説明                                                     |
|-----------|-------------------------------------|----|--------------------------------------------------------|
| summaries | list[[StudySummary](#studysummary)] | ✓  | `Curriculum` が現在保持している `Study` 及び `StudyStorage` のリスト。 |

### ProgressSummaryResponse
| 名前                 | 型                                                   | 必須 | 説明               |
|--------------------|-----------------------------------------------------|----|------------------|
| now                | str                                                 | ✓  | 終了時刻推定に利用した現在時刻。 |
| cutoff_sec         | int                                                 | ✓  | 終了時刻推定に利用した集計期間。 |
| progress_summaries | list[[StudyProgressSummary](#studyprogresssummary)] | ✓  | 進捗状況一覧。          |

### StudyProgressSummary
| 名前                  | 型                                           | 必須 | 説明                                                               |
|---------------------|---------------------------------------------|----|------------------------------------------------------------------|
| study_id            | str                                         | ✓  | 対象の `Study` の ID。                                                |
| study_name          | str \| None                                 | ✓  | 対象の `Study` の名前                                                  |
| total_grid          | int \| Literal["infinite"]                  | ✓  | この `Study` で計算する可能性のあるパラメータの組の数。                                 |
| done_grid           | int                                         | ✓  | 既に計算が終了したパラメータの組の数。                                              |
| grid_velocity       | float                                       | ✓  | 1秒間で計算できるパラメータの組の数。                                              |
| eta                 | str \| Literal["unpredictable"]             | ✓  | 終了予定時刻。パラメータ空間が無限だったり、grid_velocity が 0 の時は "unpredictable" になる。 |
| worker_efficiencies | list[[WorkerEfficiency](#workerefficiency)] | ✓  | ワーカーノードごとの能率。                                                    |

### WorkerEfficiency
| 名前            | 型           | 必須 | 説明                            |
|---------------|-------------|----|-------------------------------|
| worker_id     | str         | ✓  | ワーカーノードのID。                   |
| worker_name   | str \| None | ✓  | ワーカーノードの名前。                   |
| grid_velocity | float       | ✓  | ワーカーノードごとの1秒間で計算できるパラメータの組の数。 |

### OkResponse
| 名前 | 型    | 必須 | 説明 |
|----|------|----|----|
| ok | bool | ✓  |    |

### StudyRegistry
| 名前                    | 型                                                               | 必須 | 説明                                                                                                                                   |
|-----------------------|-----------------------------------------------------------------|----|--------------------------------------------------------------------------------------------------------------------------------------|
| name                  | str \| None                                                     |    | この `Study` の名前                                                                                                                       |
| required_capacity     | list[str]                                                       | ✓  | この `Study` を実行するのに必要な能力を表すタグ。この `required_capacity` がワーカーノードの `retaining_capacity` の部分集合だった場合にこの `Study` は実行できる。 (内部的な型は `set[str]`) |
| study_strategy        | [StudyStrategyModel](#studystrategymodel)                       | ✓  | この `Study` を実行する際に使う [`StudyStrategy`](#studystrategy) 。                                                                             |
| suggest_strategy      | [SuggestStrategyModel](#suggeststrategymodel)                   | ✓  | この `Study` を実行する際に使う [`SuggestStrategy`](#suggeststrategy) 。                                                                         |
| result_type           | Literal["scalar", "vector"]                                     | ✓  | この `Study` の戻り値が１変数か、多変数かを表す値。                                                                                                       |
| result_value_type     | Literal["bool", "int", "float"]                                 | ✓  | この `Study` の戻り値の型。                                                                                                                   |
| const_param           | [ConstParam](#constparam)  \| None                              | ✓  | ワーカーノードで利用する定数の一覧。                                                                                                                   |
| parameter_space       | [ParameterAlignedSpaceRegistry](#parameteralignedspaceregistry) | ✓  | この `Study` で計算する[パラメータ空間](#parameterspace)。                                                                                          |
| trial_repository_type | Literal["normal"]                                               |    | 使用する `TrialRepository` の種類。デフォルト値は "normal"。                                                                                         |

### StudySummary
| 名前                   | 型                                                         | 必須 | 説明                                                                                                                                   |
|----------------------|-----------------------------------------------------------|----|--------------------------------------------------------------------------------------------------------------------------------------|
| name                 | str \| None                                               |    | この `Study` の名前                                                                                                                       |
| required_capacity    | list[str]                                                 | ✓  | この `Study` を実行するのに必要な能力を表すタグ。この `required_capacity` がワーカーノードの `retaining_capacity` の部分集合だった場合にこの `Study` は実行できる。 (内部的な型は `set[str]`) |
| study_strategy       | [StudyStrategyModel](#studystrategymodel)                 | ✓  | この `Study` を実行する際に使う [`StudyStrategy`](#studystrategy) 。                                                                             |
| suggest_strategy     | [SuggestStrategyModel](#suggeststrategymodel)             | ✓  | この `Study` を実行する際に使う [`SuggestStrategy`](#suggeststrategy) 。                                                                         |
| result_type          | Literal["scalar", "vector"]                               | ✓  | この `Study` の戻り値が１変数か、多変数かを表す値。                                                                                                       |
| result_value_type    | Literal["bool", "int", "float"]                           | ✓  | この `Study` の戻り値の型。                                                                                                                   |
| study_id             | str                                                       | ✓  | この `Study` の ID。                                                                                                                     |
| status               | [StudyStatus](#studystatus-enum)                          | ✓  | この `Study` の状態。                                                                                                                      |
| registered_timestamp | str                                                       | ✓  | この `Study` が登録された時刻を表すタイムスタンプ（内部的な型は `datetime`）。                                                                                    |
| const_param          | [ConstParam](#constparam)  \| None                        | ✓  | ワーカーノードで利用する定数の一覧。                                                                                                                   |
| parameter_space      | [ParameterAlignedSpaceModel](#parameteralignedspacemodel) | ✓  | この `Study` で計算する[パラメータ空間](#parameterspace)。                                                                                          |
| total_grids          | int \| None                                               |    | この `Study` で計算する可能性のあるパラメータの組の数。パラメータ空間が無限の場合は `None`。                                                                               |
| done_grids           | int                                                       | ✓  | この `Study` で実際に計算が完了したパラメータの組の数。                                                                                                     |

### StudyStorage
| 名前                   | 型                                                         | 必須 | 説明                                                                                                                                   |
|----------------------|-----------------------------------------------------------|----|--------------------------------------------------------------------------------------------------------------------------------------|
| name                 | str \| None                                               |    | この `Study` の名前                                                                                                                       |
| required_capacity    | list[str]                                                 | ✓  | この `Study` を実行するのに必要な能力を表すタグ。この `required_capacity` がワーカーノードの `retaining_capacity` の部分集合だった場合にこの `Study` は実行できる。 (内部的な型は `set[str]`) |
| study_strategy       | [StudyStrategyModel](#studystrategymodel)                 | ✓  | この `Study` を実行する際に使う [`StudyStrategy`](#studystrategy) 。                                                                             |
| suggest_strategy     | [SuggestStrategyModel](#suggeststrategymodel)             | ✓  | この `Study` を実行する際に使う [`SuggestStrategy`](#suggeststrategy) 。                                                                         |
| result_type          | Literal["scalar", "vector"]                               | ✓  | この `Study` の戻り値が１変数か、多変数かを表す値。                                                                                                       |
| result_value_type    | Literal["bool", "int", "float"]                           | ✓  | この `Study` の戻り値の型。                                                                                                                   |
| study_id             | str                                                       | ✓  | この `Study` の ID。                                                                                                                     |
| registered_timestamp | str                                                       | ✓  | この `Study` が登録された時刻を表すタイムスタンプ（内部的な型は `datetime`）。                                                                                    |
| const_param          | [ConstParam](#constparam)  \| None                        | ✓  | ワーカーノードで利用する定数の一覧。                                                                                                                   |
| parameter_space      | [ParameterAlignedSpaceModel](#parameteralignedspacemodel) | ✓  | この `Study` で計算する[パラメータ空間](#parameterspace)。                                                                                          |
| done_timestamp       | str                                                       | ✓  | この `Study` が完了した時刻を表すタイムスタンプ（内部的な型は `datetime`）。                                                                                     |
| results              | [MappingsStorage](#mappingsstorage)                       | ✓  | 計算結果一覧。                                                                                                                              |
| done_grids           | int                                                       | ✓  | この `Study` で実際に計算が完了したパラメータの組の数。                                                                                                     |
| trial_repository     | [TrialRepositoryModel](#trialrepositorymodel)             | ✓  | この `Study` の実行時に使用する [`TrialRepository`](#trialrepository-について) 。                                                                    |

### StudyStrategyModel
| 名前    | 型                                                    | 必須 | 説明                          |
|-------|------------------------------------------------------|----|-----------------------------|
| type  | Literal["all_calculation", "find_exact", "minimize"] | ✓  | 対象の `Study` で実行する計算の種類を表す値。 |
| param | [StudyStrategyParam](#studystrategyparam) \|None     |    | この strategy の動作に必要なパラメータ。   |

### StudyStrategyParam
| 名前           | 型                       | 必須 | 説明                         |
|--------------|-------------------------|----|----------------------------|
| target_value | [ResultType](#エイリアスの一覧) | ✓  | 探索対象の値。`find_exact` で利用する。 |

### SuggestStrategyModel
| 名前    | 型                                             | 必須 | 説明                        |
|-------|-----------------------------------------------|----|---------------------------|
| type  | Literal["sequential", "random", "designated"] | ✓  | `Trial` 提案の種類を表す値。        |
| param | [SuggestStrategyParam](#suggeststrategyparam) | ✓  | この strategy の動作に必要なパラメータ。 |

### SuggestStrategyParam
| 名前             | 型    | 必須 | 説明                                                                                                                                                                                 |
|----------------|------|----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| strict_aligned | bool | ✓  | `Trial` 提案時のパラメータ空間を必ず [`ParameterAlignedSpace`](#parameteralignedspacemodel) にするかどうか。この値が `False` かつパラメータ空間が１次元のときのみ [`ParameterJaggedSpace`](#parameterjaggedspacemodel) が使用される。 |

### TrialModel
| 名前                | 型                                                                                                                    | 必須 | 説明                                                                                   |
|-------------------|----------------------------------------------------------------------------------------------------------------------|----|--------------------------------------------------------------------------------------|
| study_id          | str                                                                                                                  | ✓  | 親の `Study` のID。                                                                      |
| trial_id          | str                                                                                                                  | ✓  | `Trial` のID。                                                                         |
| timestamp         | str                                                                                                                  | ✓  | この `Trial` が予約された時間を表すタイムスタンプ（内部的な型は `datetime`）。                                    |
| trial_status      | [TrialStatus](#trialstatus-enum)                                                                                     | ✓  | この `Trial` の状態。                                                                      |
| const_param       | [ConstParam](#constparam)  \| None                                                                                   | ✓  | ワーカーノードで利用する定数の一覧。                                                                   |
| parameter_space   | [ParameterAlignedSpaceModel](#parameteralignedspacemodel) \| [ParameterJaggedSpaceModel](#parameterjaggedspacemodel) | ✓  | この `Trial` で計算する[パラメータ空間](#parameterspace)。必ず親の `Study.parameter_space` の部分空間になっている。 |
| result_type       | Literal["scalar", "vector"]                                                                                          | ✓  | この `Trial` の戻り値が１変数か、多変数かを表す値。必ず親の `Study.result_type` と一致する。                        |
| result_value_type | Literal["bool", "int", "float"]                                                                                      | ✓  | この `Trial` の戻り値の型。必ず親の `Study.result_value_type` と一致する。                              |
| worker_node_name  | str \| None                                                                                                          |    | 実行するワーカーノードの名前。                                                                      |
| worker_node_id    | str                                                                                                                  |    | 実行するワーカーノードのID。                                                                      |
| results           | list[[Mapping](#mapping)] \| None                                                                                    |    | この `Trial` の結果。                                                                      |

### Mapping
| 名前     | 型                       | 必須 | 説明                       |
|--------|-------------------------|----|--------------------------|
| params | [ParamType](#エイリアスの一覧)  | ✓  | パラメータの組。                 |
| result | [ResultType](#エイリアスの一覧) | ✓  | 上のパラメータの組で所定の計算を行った結果の値。 |

### MappingsStorage
| 名前          | 型                                          | 必須 | 説明                                      |
|-------------|--------------------------------------------|----|-----------------------------------------|
| params_info | [ParamType](#エイリアスの一覧)                     | ✓  | パラメータの型情報。値はダミー。                        |
| result_info | [ResultType](#エイリアスの一覧)                    | ✓  | 結果の型情報。値はダミー                            |
| values      | list[list[[PortableValueType](#エイリアスの一覧)]] | ✓  | パラメータと結果の一覧。内部のリストはパラメータと結果が順番に格納されている。 |

### ParameterAlignedSpaceRegistry
| 名前   | 型                                                 | 必須 | 説明                             |
|------|---------------------------------------------------|----|--------------------------------|
| type | Literal["aligned"]                                | ✓  | パラメータ空間の種類。必ず `"aligned"` にする。 |
| axes | list[[LineSegmentRegistry](#linesegmentregistry)] | ✓  | このパラメータ空間が持っている軸。              |

### LineSegmentRegistry
| 名前    |   | 型                               | 必須 | 説明                                    |
|-------|:--|---------------------------------|----|---------------------------------------|
| name  |   | str \| None                     |    | 軸の名前。                                 |
| type  |   | Literal["bool", "int", "float"] | ✓  | この軸が生成する値の型。                          |
| size  |   | str \| None                     | ✓  | この軸が生成するパラメータの数。`None` の場合はサイズが無限となる。 |
| step  |   | [PortableValueType](#エイリアスの一覧)  | ✓  | パラメータ間の数値の幅。                          |
| start |   | [PortableValueType](#エイリアスの一覧)  | ✓  | この軸が生成する値の最小値。                        |

### ParameterAlignedSpaceModel
| 名前                  | 型                                           | 必須 | 説明                                                                                  |
|---------------------|---------------------------------------------|----|-------------------------------------------------------------------------------------|
| type                | Literal["aligned"]                          | ✓  | パラメータ空間の種類。必ず `"aligned"` にする。                                                      |
| axes                | list[[LineSegmentModel](#linesegmentmodel)] | ✓  | このパラメータ空間が持っている軸。                                                                   |
| check_lower_filling | bool                                        | ✓  | このパラメータ空間からパラメータを取得する際に、低い次元（`axes` の末尾）から値を取得することを強制するフラグ。内部的な利用を除き、常に `True` にする。 |

### ParameterJaggedSpaceModel
| 名前              | 型                                                | 必須 | 説明                                     |
|-----------------|--------------------------------------------------|----|----------------------------------------|
| type            | Literal["jagged"]                                | ✓  | パラメータ空間の種類。必ず `"jagged"` にする。          |
| parameters      | list[tuple[[PortableValueType](#エイリアスの一覧), ...]] | ✓  | パラメータの組のリスト。                           |
| ambient_indices | list[list[str, ...]]                             | ✓  | `parameters` の値が母空間でどの位置にあるかを指すインデックス。 |
| axes_info       | list[[LineSegmentModel](#linesegmentmodel)]      | ✓  | 各軸の名前や型情報。                             |

### LineSegmentModel
| 名前            | 型                               | 必須 | 説明                                                                                                               |
|---------------|---------------------------------|----|------------------------------------------------------------------------------------------------------------------|
| name          | str \| None                     |    | 軸の名前。                                                                                                            |
| type          | Literal["bool", "int", "float"] | ✓  | この軸が生成する値の型。                                                                                                     |
| size          | str \| None                     | ✓  | この軸が生成するパラメータの数。`None` の場合はサイズが無限となる。                                                                            |
| step          | [PortableValueType](#エイリアスの一覧)  | ✓  | パラメータ間の数値の幅。                                                                                                     |
| start         | [PortableValueType](#エイリアスの一覧)  | ✓  | この軸が生成する値の最小値。                                                                                                   |
| ambient_index | str                             | ✓  | `start` の値が母空間でどの位置にあるかを指すインデックス。                                                                                |
| ambient_size  | str \| None                     |    | この軸が母空間で生成するパラメータの総数。                                                                                            |
| is_dummy      | bool                            |    | この軸が [ParameterJaggedSpaceModel](#parameterjaggedspacemodel) に属する場合に `True` になり、`name`, `type` の情報のみが有効であることを表す。 |

### ScalarValue
| 名前         | 型                               | 必須 | 説明                                   |
|------------|---------------------------------|----|--------------------------------------|
| type       | Literal["scalar"]               | ✓  | 値の種別。スカラー量かベクトル量かを区別するための識別子。        |
| value_type | Literal["bool", "int", "float"] | ✓  | 値の型。                                 |
| value      | [PortableValueType](#エイリアスの一覧)  | ✓  | 値。                                   |
| name       | str \| None                     |    | 値につける名前。パラメータ空間から生成されたものであれば軸の名前が入る。 |

### VectorValue
| 名前         | 型                                    | 必須 | 説明                                   |
|------------|--------------------------------------|----|--------------------------------------|
| type       | Literal["vector"]                    | ✓  | 値の種別。スカラー量かベクトル量かを区別するための識別子。        |
| value_type | Literal["bool", "int", "float"]      | ✓  | 値の型。                                 |
| values     | list[[PortableValueType](#エイリアスの一覧)] | ✓  | 値。                                   |
| name       | str \| None                          |    | 値につける名前。パラメータ空間から生成されたものであれば軸の名前が入る。 |

### ConstParam
| 名前     | 型                                             | 必須 | 説明      |
|--------|-----------------------------------------------|----|---------|
| consts | list[[ConstParamElement](#constparamelement)] | ✓  | 定数のリスト。 |

### ConstParamElement
| 名前    | 型                                      | 必須 | 説明                |
|-------|----------------------------------------|----|-------------------|
| type  | Literal["int", "float", "bool", "str"] | ✓  | 定数の型を区別するための識別子。  |
| key   | str                                    | ✓  | 定数を取り出す際に利用するキー。  |
| value | str \| bool                            | ✓  | portablize された定数。 |

### TrialRepositoryModel
| 名前       | 型              | 必須 | 説明                                           |
|----------|----------------|----|----------------------------------------------|
| type     | Literal["int"] | ✓  | 使用する `TrialRepository` の種類。デフォルト値は "normal"。 |
| save_dir | str            | ✓  | `Trial` を保存するディレクトリを表す文字列(内部的な型は `Path`)。    |

### StudyStatus (Enum)
| 名前        | 説明                                      |
|-----------|-----------------------------------------|
| wait      | 実行待ち                                    |
| running   | 実行中                                     |
| done      | 完了                                      |
| not_found | 対象の `Study` が存在しない。/study のレスポンスにのみ現れる。 |

### TrialStatus (Enum)
| 名前      | 説明  |
|---------|-----|
| running | 実行中 |
| done    | 完了  |

### エイリアスの一覧
| エイリアス             | 元の型                                                        |
|-------------------|------------------------------------------------------------|
| ParamType         | list[[ScalarValue](#scalarvalue), ...]                     |
| ResultType        | [ScalarValue](#scalarvalue) \| [VectorValue](#vectorvalue) |
| PortableValueType | bool \| str                                                |

## 9. 高度な使用方法
### ParameterSpace の実装について
#### ParameterAlignedSpace
[ParameterSpace](#parameterspace)の例は最も簡単なパラメータ空間の表し方の例で、最初に `Study` を登録する時に使用できる型（`ParameterAlignedSpaceRegistry`）です。
テーブルノードとワーカノードの間でやり取りをする場合はもう少し追加で情報が必要になります。
これは、上の例では空間全体を表せばそれで十分ですが、テーブルノードとワーカノードの間でやり取りでは「全体（母空間）に対してどの部分か」を表す必要があるためです。  
次の例は母空間の一部を切り取った部分空間を表したものです。
```json
{
  "type": "aligned",
  "axes": [
    {
      "type": "bool",
      "name": "x",
      "size": "0x1",
      "step": "0x1",
      "start": false,
      "ambient_size": "0x2",
      "ambient_index": "0x0"
    },
    {
      "type": "int",
      "name": "y",
      "size": "0x1",
      "step": "0x1",
      "start": "-0x23",
      "ambient_size": "0x65",
      "ambient_index": "0xf"
    },
    {
      "type": "float",
      "name": "y",
      "size": "0xc8",
      "step": "0x1.0p-2",
      "start": "0x0p+0",
      "ambient_size": "0xc8",
      "ambient_index": "0x0"
    }
  ]
}
```
x, y のサイズが変わっていることに注目してください。それぞれ `size` が 1 になっています。z は変化がありません。一方で新たに `ambient_size`, `ambient_index` が追加されています。
これはそれぞれ、母空間のサイズ、`start`の値の母空間でのインデックス、を表しています。  
これら追加の値はワーカーノードでの計算が終了した後にテーブルノードで集計する際に必要な値です。ワーカーノードでは単に `size`, `size`, `start` を見ればよく、
この例では 「x=false, y=-35, z は 0.0 から 50.0 まで」の１次元空間を表していることが分かります。

#### ParameterJaggedSpace
`ParameterAlignedSpace` のような「ここからここまで」の表記では必ず四角で区切られた範囲（正確には「超直方体」）を表すことしかできません。
一方で、「この点とあの点」のように具体的に列挙した方が便利な場面があります。
```json
{
  "type": "jagged",
  "parameters": [
    ["0x4e", "0x1"], ["0x38", "0xa"]
  ],
  "ambient_index": [
    ["0x4e", "0x1"], ["0x38", "0xa"]
  ],
  "axes_info": [
    {
      "type": "int",
      "name": "x",
      "size": "0x1",
      "step": "0x1",
      "start": "0x0",
      "ambient_size": "0x64",
      "ambient_index": "0x0",
      "is_dummy": true
    },
    {
      "type": "int",
      "name": "y",
      "size": "0x1",
      "step": "0x1",
      "start": "0x0",
      "ambient_size": "0x64",
      "ambient_index": "0x0",
      "is_dummy": true
    }
  ]
}
```
`parameters` が実際のパラメータを表し、`ambient_index` がそのパラメータが母空間でどのインデックスであるかを表しています。  
ただし、名前や型に関する情報は依然として必要であるので `axes_info` が定義されています。
最後のフィールドに `"is_dummy": true` とあることからも分かる通り、このオブジェクトは `type`, `name`, `ambient_size` のみが有効な値です。

### 半直線の利用
パラメータ空間の軸には長さ無限の半直線を１つだけ含めることができます。この半直線は必ず最初の軸にする必要があります。半直線の定義は以下の通りです。
```json
{
  "type": "int",
  "name": "infinite_axis",
  "size": null,
  "step": "0x1",
  "start": "0x0",
  "ambient_size": null,
  "ambient_index": "0x0"
}
```
`ambient_size` が `null` になります。また `Study` 登録時などのパラメータ空間全体を表す必要があるときなどは更に `size` も `null` になります。
> [!WARNING]
> 半直線が含まれるパラメータ空間で、`StudyStrategy` のタイプを all_calculation にすることはできません。

### 高度な TrialRunner の実装
#### SemiAutoMPTrialRunner
`AutoMPTrialRunner` ではプロセスプール (`multiprocessing.pool.Pool`) をこの `TrialRunner` 内部で生成していました。
子プロセスの生成は重い処理であるので、繰り返し使用することが分かっている場合は最初に生成したものを使いまわす方が効率的です。  
`SemiAutoMPTrialRunner` ではこの問題を解決するためにプロセスプールを外から注入できるようになっています。
定義の方法は `AutoMPTrialRunner` とほとんど同じで、継承元が変わるだけです。
```diff
from lite_dist2.type_definitions import RawParamType, RawResultType
- from lite_dist2.worker_node.trial_runner import AutoMPTrialRunner
+ from lite_dist2.worker_node.trial_runner import SemiAutoMPTrialRunner


- class Mandelbrot(AutoMPTrialRunner):
+ class Mandelbrot(SemiAutoMPTrialRunner):
    _ABS_THRESHOLD = 2.0
    _MAX_ITER = 255

    def func(self, parameters: RawParamType, *args: object, **kwargs: object) -> RawResultType:
        x = float(parameters[0])
        y = float(parameters[1])
        c = complex(x, y)
        z = complex(0, 0)
        iter_count = 0
        while abs(z) <= self._ABS_THRESHOLD and iter_count < self._MAX_ITER:
            z = z ** 2 + c
            iter_count += 1
        return iter_count
```

実行する際は外からプロセスプールを注入します。また `WorkerConfig.process_num` は無視されます。

```diff
+ from multiprocessing.pool import Pool

from lite_dist2.config import WorkerConfig
from lite_dist2.worker_node.worker import Worker

def run_worker(table_ip: str) -> None:
    worker_config = WorkerConfig(
        name="w_01",
-         process_num=2,
        max_size=10,
        wait_seconds_on_no_trial=5,
        table_node_request_timeout_seconds=60,
    )
-     worker = Worker(
-         trial_runner=Mandelbrot(),
-         ip=table_ip,
-         config=worker_config,
-     )
-     worker.start()
+     with Pool(processes=2) as pool:
+         worker = Worker(
+             trial_runner=Mandelbrot(),
+             ip=table_ip,
+             config=worker_config,
+             pool=Pool,
+         )
+         worker.start()
```

#### ManualMPTrialRunner
もしあなたがパラメータの組のリストを受け取って処理する部分を自分で実装したい場合（例えば、並列処理の部分を自分で実装したい）、`ManualMPTrialRunner` が利用できます。
このクラスを利用する場合は `func` メソッドの代わりに `batch_func` メソッドを実装します。  
例えば以下の例は `AutoMPTrialRunner` と等価です。
```python
import functools
from typing import Iterator
from multiprocessing.pool import Pool

from lite_dist2.config import WorkerConfig
from lite_dist2.type_definitions import RawParamType, RawResultType
from lite_dist2.worker_node.trial_runner import ManualMPTrialRunner


class ManualMandelbrot(ManualMPTrialRunner):
    def batch_func(self, raw_params: Iterator[RawParamType], config: WorkerConfig, *args: object, **kwargs: object) -> list[tuple[RawParamType, RawResultType]]:
        raw_mappings: list[tuple[RawParamType, RawResultType]] = []
        parameter_pass_func = functools.partial(self.parameter_pass_func, args=args, kwargs=kwargs)
        with Pool(processes=2) as pool:
            for arg_tuple, result_iter in pool.imap_unordered(parameter_pass_func, raw_params):
                raw_mappings.append((arg_tuple, result_iter))
        return raw_mappings
```

### 定数の登録と利用
何かの大規模計算をするにあたって定数を利用しないことは稀でしょう。上記の `Mandelbrot` クラスのように `TrialRunner` に定数を持たせるのはその実現方法の1つです（`_ABS_THRESHOLD` や `_MAX_ITER`）。
しかし、`TrialRunner` はワーカーノードにデプロイされているものなので、この定数を変更したい場合は全てのワーカーノードを再デプロイしなおさなくてはなりません。  
この問題はこの定数を `Study` に持たせることで解決できます。[Study の登録時](#study-の登録) に以下のインスタンスを `StudyRegister` に渡します。
```python
from lite_dist2.common import float2hex, int2hex
from lite_dist2.value_models.const_param import ConstParam, ConstParamElement

const_param = ConstParam(
    consts=[
        ConstParamElement(type="float", key="abs_threshold", value=float2hex(2.0)),
        ConstParamElement(type="int", key="max_iter", value=int2hex(255)),
    ],
)
```
あるいは辞書から生成することも可能です。
```python
from lite_dist2.value_models.const_param import ConstParam

_const_dict = {
    "abs_threshold": 2.0,
    "max_iter": 255
}
const_param = ConstParam.from_dict(_const_dict)
```
これらの定数は、`int`、`float`、`bool` のほかに `str` も使用できます。  
`TrialRunner` ではキーワード引数からこの値を取得できます。
```diff
from lite_dist2.type_definitions import RawParamType, RawResultType
from lite_dist2.worker_node.trial_runner import AutoMPTrialRunner


class Mandelbrot(AutoMPTrialRunner):
-     _ABS_THRESHOLD = 2.0
-     _MAX_ITER = 255
-
    def func(self, parameters: RawParamType, *args: object, **kwargs: object) -> RawResultType:
+         abs_threshold = self.get_typed("abs_threshold", float, kwargs)
+         max_iter = self.get_typed("max_iter", int, kwargs)
        x = float(parameters[0])
        y = float(parameters[1])
        c = complex(x, y)
        z = complex(0, 0)
        iter_count = 0
-         while abs(z) <= self._ABS_THRESHOLD and iter_count < self._MAX_ITER:
+         while abs(z) <= abs_threshold and iter_count < max_iter:
            z = z ** 2 + c
            iter_count += 1
        return iter_count
```
ここで、`BaseTrialRunner` に定義されている `get_typed` メソッドを利用しています。これは型を厳密に指定するためのヘルパーメソッドです。
型チェッカーや例外処理を気にしないのであれば次の書き方でも問題ありません。
```diff
from lite_dist2.type_definitions import RawParamType, RawResultType
from lite_dist2.worker_node.trial_runner import AutoMPTrialRunner


class Mandelbrot(AutoMPTrialRunner):
-     _ABS_THRESHOLD = 2.0
-     _MAX_ITER = 255
-
    def func(self, parameters: RawParamType, *args: object, **kwargs: object) -> RawResultType:
+         abs_threshold = kwargs["abs_threshold"]
+         max_iter = kwargs["max_iter"]
        x = float(parameters[0])
        y = float(parameters[1])
        c = complex(x, y)
        z = complex(0, 0)
        iter_count = 0
-         while abs(z) <= self._ABS_THRESHOLD and iter_count < self._MAX_ITER:
+         while abs(z) <= abs_threshold and iter_count < max_iter:
            z = z ** 2 + c
            iter_count += 1
        return iter_count
```

### Python スクリプト内でのテーブルノードの起動
[テーブルノードの起動](#テーブルノードの起動) では uv コマンドでテーブルノードを起動していました。  
もしこれを Python スクリプトで起動したい場合は次のようにします。
```python
from lite_dist2.table_node_api.start_table_api import start

start()
```
この例ではテーブルノードはブロッキング処理で動いているので、サーバを終了しない限り `start` 関数から抜けることはありません。
テーブルノードをノンブロッキングに起動したい場合は別スレッドでサーバを立ち上げる必要があります。  
次の例では別スレッドでサーバを起動しています。
```python
from lite_dist2.table_node_api.start_table_api import start_in_thread

start_in_thread()
```

### TrialRepository について
`TrialRepository` とは計算済みの `Trial` をテーブルノードが保存するための仕組みです。
現在利用可能な `TrialRepository` は `NormalTrialRepository` だけです（[`TrialRepositoryModel`](#trialrepositorymodel) の `type` や [`StudyRegistry`](#studyregistry) の `trial_repository_type` を参照してください）。
`NormalTrialRepository` は `TableConfig.trial_file_dir` （デフォルト設定では実行ディレクトリの配下の `trials` というディレクトリ）の下に `Study` ごとに `study_id` を名前にしたディレクトリを作成し、更にその配下に `Trial` を表す json ファイルを保存します。

最終的に /study API で結果を取得した後は `Study` ごとのディレクトリは削除されます。この保存場所を変更したい場合は `TableConfig.trial_file_dir` を変更してください。

## 10. 開発
### 必要要件
- Python >= 3.13
- uv >= 0.7.0

### 開発環境のセットアップ
```shell
uv sync --dev
```

### テスト実行方法
```shell
uv run pytest
```
また、以下のオプションをつけることでカバレッジ情報を取得できます。
```shell
uv run pytest --cov --cov-config=pyproject.toml
```
