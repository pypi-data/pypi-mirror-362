# JijZept Solver

Jij 製の数理最適化ソルバーである JijZept Solver を 、Web API 経由で実行するための クライアントパッケージです。以下に使用方法を説明します。 / Client package for executing JijZept Solver, Jij's mathematical optimization solver, via Web API. The following explains how to use it.

## Quick Start

### アクセストークンの取得 / Obtaining Access Token

JijZept Solver(無償WebAPI版) を使用するには、事前にアクセストークンを取得する必要があります。無償版の利用申請方法は以下の通りです。 / To use JijZept Solver (Free Web API version), you need to obtain an access token in advance. The application method for the free version is as follows.

#### 利用申請方法 / Application Method

1. 以下リンク先のフォームから利用申請を行ってください。 / Please apply for usage from the form at the following link.

   **申請フォーム / Application Form**: [JijZept Solver(無償WebAPI版) 利用申請フォーム / JijZept Solver (Free Web API version) Usage Application Form](https://docs.google.com/forms/d/e/1FAIpQLScLTRxXGaN7egRkoYcq2ZvFoFXRyYInsmPXlyxk9pF11E9--g/viewform)

2. 申請されたメールアドレス宛に、アクセスに必要な情報（API サーバーのホスト名、アクセストークン）が届きます。 / The information required for access (API server hostname, access token) will be sent to the email address you applied with.

### インストール / Installation

JijZept Solver のクライアントパッケージをインストールします / Install the JijZept Solver client package:

```bash
pip install jijzept-solver
```

### 環境変数の設定 / Environment Variable Setup

上記利用申請により入手した、以下の値を環境変数に設定します / Set the following values obtained from the above application as environment variables:

- **`JIJZEPT_SOLVER_SERVER_HOST`**: API サーバーのホスト名 / API server hostname

- **`JIJZEPT_SOLVER_ACCESS_TOKEN`**: アクセストークン / Access token

### 設定例 / Configuration Examples

環境変数の設定例 / Environment variable configuration example:

```bash
export JIJZEPT_SOLVER_SERVER_HOST="API サーバーのホスト名 / API server hostname"
export JIJZEPT_SOLVER_ACCESS_TOKEN="アクセストークン / Access token"
```

または Python コード内で設定する例 / Or example of setting within Python code:

```python
import os

os.environ["JIJZEPT_SOLVER_SERVER_HOST"] = "API サーバーのホスト名 / API server hostname"
os.environ["JIJZEPT_SOLVER_ACCESS_TOKEN"] = "アクセストークン / Access token"
```

### リクエスト実行例 / Request Execution Example

実行例の中で JijModeling を使用するため、事前にインストールしておきます。 / Install JijModeling in advance as it is used in the execution example.

```python
pip install jijmodeling
```

ナップサック問題を解く例 / Example of solving a knapsack problem:

```python

import logging
import jijzept_solver
import jijmodeling as jm

logging.basicConfig(level=logging.INFO)

# ナップサック問題を定義 / Define knapsack problem
v = jm.Placeholder("v", ndim=1)  # アイテムの価値 / Item values
w = jm.Placeholder("w", ndim=1)  # アイテムの重さ / Item weights
W = jm.Placeholder("W")          # ナップサックの容量 / Knapsack capacity
N = v.len_at(0, latex="N")       # アイテム数 / Number of items
x = jm.BinaryVar("x", shape=(N,))  # 決定変数 / Decision variables
i = jm.Element("i", belong_to=(0, N))

problem = jm.Problem("Knapsack", sense=jm.ProblemSense.MAXIMIZE)
problem += jm.sum(i, v[i] * x[i])  # 目的関数：価値の最大化 / Objective function: maximize value
problem += jm.Constraint("weight", jm.sum(i, w[i] * x[i]) <= W)  # 重量制約 / Weight constraint

# インスタンスデータ / Instance data
instance_data = {
    "v": [10, 13, 18, 31, 7, 15],   # アイテムの価値 / Item values
    "w": [11, 15, 20, 35, 10, 33],  # アイテムの重さ / Item weights
    "W": 47,                        # ナップサックの容量 / Knapsack capacity
}

# OMMX インスタンスを作成 / Create OMMX instance
interpreter = jm.Interpreter(instance_data)
instance = interpreter.eval_problem(problem)

# APIにリクエストを実行 / Execute API request
solution = jijzept_solver.solve(instance, time_limit_sec=2.0)

print(f"Value of the objective function: {solution.objective}")
```

## API リファレンス / API Reference

JijZept Solver を使用して最適化問題を解きます。 / Solve optimization problems using JijZept Solver.

**パラメータ:** / **Parameters:**

- `ommx_instance` (Instance): OMMX インスタンス / OMMX instance
- `time_limit_sec` (float): 最大求解時間（秒） / Maximum solving time (seconds)

**戻り値:** / **Return Value:**

- `Solution`: OMMX ソリューション / OMMX solution

**例:** / **Example:**

```python
solution = jijzept_solver.solve(
    ommx_instance=problem_instance,
    time_limit_sec=2.0
)
```
