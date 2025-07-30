# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.function.huggingfaceserve.builder import FunctionHuggingfaceserveBuilder
from digitalhub_runtime_modelserve.entities.function.kubeaiserve.builder import FunctionKubeaiserveBuilder
from digitalhub_runtime_modelserve.entities.function.kubeaiservespeechtotext.builder import (
    FunctionKubeaiserveSpeechtotextBuilder,
)
from digitalhub_runtime_modelserve.entities.function.kubeaiservetext.builder import FunctionKubeaiserveTextBuilder
from digitalhub_runtime_modelserve.entities.function.mlflowserve.builder import FunctionMlflowserveBuilder
from digitalhub_runtime_modelserve.entities.function.sklearnserve.builder import FunctionSklearnserveBuilder
from digitalhub_runtime_modelserve.entities.run.huggingfaceserve_run.builder import RunHuggingfaceserveRunBuilder
from digitalhub_runtime_modelserve.entities.run.kubeaiservespeechtotext_run.builder import (
    RunKubeaiserveSpeechtotextRunBuilder,
)
from digitalhub_runtime_modelserve.entities.run.kubeaiservetext_run.builder import RunKubeaiserveTextRunBuilder
from digitalhub_runtime_modelserve.entities.run.mlflowserve_run.builder import RunMlflowserveRunBuilder
from digitalhub_runtime_modelserve.entities.run.sklearnserve_run.builder import RunSklearnserveRunBuilder
from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.builder import TaskHuggingfaceserveServeBuilder
from digitalhub_runtime_modelserve.entities.task.kubeaiserve_serve.builder import TaskKubeaiserveServeBuilder
from digitalhub_runtime_modelserve.entities.task.kubeaiservespeechtotext_serve.builder import (
    TaskKubeaiserveSpeechtotextServeBuilder,
)
from digitalhub_runtime_modelserve.entities.task.kubeaiservetext_serve.builder import TaskKubeaiserveTextServeBuilder
from digitalhub_runtime_modelserve.entities.task.mlflowserve_serve.builder import TaskMlflowserveServeBuilder
from digitalhub_runtime_modelserve.entities.task.sklearnserve_serve.builder import TaskSklearnserveServeBuilder

entity_builders = (
    (EntityKinds.FUNCTION_HUGGINGFACESERVE.value, FunctionHuggingfaceserveBuilder),
    (EntityKinds.FUNCTION_KUBEAISERVESPEECHTOTEXT.value, FunctionKubeaiserveSpeechtotextBuilder),
    (EntityKinds.FUNCTION_KUBEAISERVETEXT.value, FunctionKubeaiserveTextBuilder),
    (EntityKinds.FUNCTION_MLFLOWSERVE.value, FunctionMlflowserveBuilder),
    (EntityKinds.FUNCTION_SKLEARNSERVE.value, FunctionSklearnserveBuilder),
    (EntityKinds.RUN_HUGGINGFACESERVE.value, RunHuggingfaceserveRunBuilder),
    (EntityKinds.RUN_KUBEAISERVESPEECHTOTEXT.value, RunKubeaiserveSpeechtotextRunBuilder),
    (EntityKinds.RUN_KUBEAISERVETEXT.value, RunKubeaiserveTextRunBuilder),
    (EntityKinds.RUN_MLFLOWSERVE.value, RunMlflowserveRunBuilder),
    (EntityKinds.RUN_SKLEARNSERVE.value, RunSklearnserveRunBuilder),
    (EntityKinds.TASK_HUGGINGFACESERVE_SERVE.value, TaskHuggingfaceserveServeBuilder),
    (EntityKinds.TASK_KUBEAISERVESPEECHTOTEXT_SERVE.value, TaskKubeaiserveSpeechtotextServeBuilder),
    (EntityKinds.TASK_KUBEAISERVETEXT_SERVE.value, TaskKubeaiserveTextServeBuilder),
    (EntityKinds.TASK_MLFLOWSERVE_SERVE.value, TaskMlflowserveServeBuilder),
    (EntityKinds.TASK_SKLEARNSERVE_SERVE.value, TaskSklearnserveServeBuilder),
)

try:
    from digitalhub_runtime_modelserve.runtimes.builder import RuntimeModelserveBuilder

    runtime_builders = ((kind, RuntimeModelserveBuilder) for kind in [e.value for e in EntityKinds])
except ImportError:
    runtime_builders = tuple()
