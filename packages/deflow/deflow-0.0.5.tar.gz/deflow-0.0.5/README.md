# DeFlow

[![test](https://github.com/ddeutils/deflow/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/ddeutils/deflow/actions/workflows/tests.yml)
[![pypi version](https://img.shields.io/pypi/v/deflow)](https://pypi.org/project/deflow/)
[![python support version](https://img.shields.io/pypi/pyversions/deflow)](https://pypi.org/project/deflow/)
[![size](https://img.shields.io/github/languages/code-size/ddeutils/deflow)](https://github.com/ddeutils/deflow)
[![gh license](https://img.shields.io/github/license/ddeutils/deflow)](https://github.com/ddeutils/deflow/blob/main/LICENSE)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A **Lightweight Declarative Data Framework** that allow you to run data pipelines
by YAML config template.

> [!NOTE]
> I want to use this project is the real-world use-case for my [Workflow](https://github.com/ddeutils/ddeutil-workflow)
> package that able to handle production data pipeline with the DataOps strategy.

> [!WARNING]
> This framework does not allow you to custom your pipeline yet. If you want to
> create your workflow, you can implement it by your custom template reference this
> package.

In my opinion, I think it should not create duplicate workflow codes if I can
write with dynamic input parameters on the one template workflow that just change
the input parameters per use-case instead.
This way I can handle a lot of logical workflows in our orgs with only metadata
configuration. It called **Metadata Driven Data Workflow**.

## 📦 Installation

```shell
pip install -U deflow
```

## :dart: Usage

### Version 1

> [!NOTE]
> This project will create the data framework **Version 1** first.

After initialize your data framework project with **Version 1**, your data pipeline
config files will store with this file structure:

```text
conf/
 ├─ conn/
 │   ├─ c_conn_01.yml
 │   ╰─ c_conn_02.yml
 ├─ routes/
 │   ╰─ routing.yml
 ├─ stream/
 │   ╰─ s_stream_01/
 │       ├─ g_group_01.tier.priority/
 │       │   ├─ p_proces_01.yml
 │       │   ╰─ p_proces_02.yml
 │       ├─ g_group_02.tier.priority/
 │       │   ├─ p_proces_01.yml
 │       │   ╰─ p_proces_02.yml
 │       ╰─ config.yml
 ╰─ .configore
```

You can run the data flow by:

```python
from deflow.flow import Flow
from ddeutil.workflow import Result

flow: Result = (
    Flow(name="s_stream_01")
    .option("conf_paths", ["./data/conf"])
    .run(mode="N")
)
```

### Version 2

After initialize your data framework project with **Version 2**, your data pipeline
config files will store with this file structure:

```text
conf/
 ├─ pipeline/
 │   ╰─ p_pipe_01/
 │       ├─ config.yml
 │       ├─ n_node_01.yml
 │       ╰─ n_node_02.yml
 ╰─ .configore
```


### Version 3

> [!NOTE]
> This version is the same DAG and Task strategy like Airflow.

## :cookie: Configuration

| Name                            | Component | Default  | Description                                        |
|:--------------------------------|:---------:|:---------|:---------------------------------------------------|
| **DEFLOW_CORE_CONF_PATH**       |   CORE    | `./conf` | A config path to get data framework configuration. |
| **DEFLOW_CORE_VERSION**         |   CORE    | `v1`     | A specific data framework version.                 |
| **DEFLOW_CORE_REGISTRY_CALLER** |   CORE    | `.`      | A registry of caller function.                     |

**Support data framework version:**

| Version | Supported | Description                                                                |
|:-------:|:---------:|:---------------------------------------------------------------------------|
|    1    | Progress  | A data framework that base on `stream`, `group`, `process`, and `routing`. |
|    2    | Progress  | A data framework that base on `pipeline`, and `node`.                      |
|    3    |   Draft   | A data framework that base on `dag`, and `task`.                           |

## 💬 Contribute

I do not think this project will go around the world because it has specific propose,
and you can create by your coding without this project dependency for long term
solution. So, on this time, you can open [the GitHub issue on this project 🙌](https://github.com/ddeutils/fastflow/issues)
for fix bug or request new feature if you want it.
