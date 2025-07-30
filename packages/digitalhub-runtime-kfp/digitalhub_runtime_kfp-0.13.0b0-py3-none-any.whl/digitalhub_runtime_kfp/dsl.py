# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import os
from contextlib import contextmanager

from digitalhub.entities.function.crud import get_function
from digitalhub.entities.workflow.crud import get_workflow
from digitalhub.runtimes.enums import RuntimeEnvVar
from digitalhub.stores.credentials.enums import CredsEnvVar
from kfp import dsl

LABEL_PREFIX = "kfp-digitalhub-runtime-"


class PipelineParamEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dsl.PipelineParam):
            return str(obj)
        return super().default(obj)


@contextmanager
def pipeline_context():
    try:
        yield PipelineContext()
    finally:
        pass


class PipelineContext:
    def step(
        self,
        name: str,
        action: str,
        function: str | None = None,
        function_id: str | None = None,
        workflow: str | None = None,
        workflow_id: str | None = None,
        step_outputs: dict | None = None,
        **kwargs,
    ) -> dsl.ContainerOp:
        """
        Create a KFP ContainerOp to execute a DHCore function or workflow.

        This method builds the command and output mapping for a pipeline step,
        ensuring correct argument passing and output file handling.

        Parameters
        ----------
        name : str
            Name of the KFP step.
        action : str
            Action to execute.
        function : str
            Name of the DHCore function to execute.
        function_id : str
            ID of the DHCore function to execute.
        workflow : str
            Name of the DHCore workflow to execute.
        workflow_id : str
            ID of the DHCore workflow to execute.
        step_outputs : dict
            Output mapping for the KFP step.
        kwargs : dict
            Execution parameters.

        Returns
        -------
        dsl.ContainerOp
            The constructed KFP ContainerOp.
        """

        # Build command
        cmd = ["python", "step.py"]

        # Add executable entity
        try:
            project = os.environ.get(RuntimeEnvVar.PROJECT.value)
            if function is not None:
                exec_entity = get_function(function, project=project, entity_id=function_id)
            elif workflow is not None:
                exec_entity = get_workflow(workflow, project=project, entity_id=workflow_id)
            else:
                raise RuntimeError("Either function or workflow must be provided.")
        except Exception as e:
            raise RuntimeError("Function or workflow not found.") from e
        cmd.extend(["--entity", exec_entity.key])

        # Prepare execution kwargs
        exec_kwargs = {k: v for k, v in {**kwargs}.items() if v is not None}
        exec_kwargs["action"] = action
        exec_kwargs["wait"] = True
        cmd.extend(["--kwargs", json.dumps(exec_kwargs, cls=PipelineParamEncoder)])

        # Prepare outputs
        file_outputs = {"run_id": "/tmp/run_id"}
        if step_outputs is not None:
            for val in step_outputs.values():
                # Sanitize . in output names
                oname = str(val).replace(".", "_")
                file_outputs[oname] = f"/tmp/entity_{oname}"

        # Get image stepper
        image = os.environ.get(CredsEnvVar.DHCORE_WORKFLOW_IMAGE.value)
        if image is None:
            raise RuntimeError(f"Env var '{CredsEnvVar.DHCORE_WORKFLOW_IMAGE.value}' is not set")

        # Create ContainerOp
        cop = dsl.ContainerOp(
            name=name,
            image=image,
            command=cmd,
            file_outputs=file_outputs,
        )

        # Add labels
        for k, v in [
            (f"{LABEL_PREFIX}project", project),
            (f"{LABEL_PREFIX}{exec_entity.ENTITY_TYPE}", exec_entity.name),
            (f"{LABEL_PREFIX}{exec_entity.ENTITY_TYPE}_id", exec_entity.id),
            (f"{LABEL_PREFIX}action", action),
        ]:
            cop.add_pod_label(k, v)

        return cop
