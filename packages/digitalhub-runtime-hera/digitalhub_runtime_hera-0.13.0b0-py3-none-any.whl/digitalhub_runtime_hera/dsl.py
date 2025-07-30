# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import os
from uuid import uuid4

from digitalhub.entities.function.crud import get_function
from digitalhub.entities.workflow.crud import get_workflow
from digitalhub.runtimes.enums import RuntimeEnvVar
from digitalhub.stores.credentials.enums import CredsEnvVar
from hera.workflows import Artifact, Container, Parameter
from hera.workflows import models as m


def oai_step(
    action: str,
    function: str | None = None,
    function_id: str | None = None,
    workflow: str | None = None,
    workflow_id: str | None = None,
    step_name: str | None = None,
    step_outputs: list | None = None,
    step_inputs: list | None = None,
    **kwargs,
) -> None:
    """
    Create a Hera step as container.

    Parameters
    ----------
    action : str
        Action to execute.
    function : str
        Function name.
    function_id : str
        Function ID.
    workflow : str
        Workflow name.
    workflow_id : str
        Workflow ID.
    step_name : str
        Step name.
    step_outputs : list
        Step outputs.
    step_inputs : list
        Step inputs.
    kwargs : dict
        Execution parameters.

    Returns
    -------
    Container
        Hera container.
    """

    cmd = ["python"]
    args = ["step.py"]

    # Add entity
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
    args.extend(["--entity", str(exec_entity.id)])

    # Add kwargs
    if kwargs is None:
        kwargs = {}
    kwargs["action"] = action
    kwargs["wait"] = True
    args.extend(["--kwargs", json.dumps(kwargs)])

    # Get image stepper
    image = os.environ.get(CredsEnvVar.DHCORE_WORKFLOW_IMAGE.value)
    if image is None:
        raise RuntimeError(f"Env var '{CredsEnvVar.DHCORE_WORKFLOW_IMAGE.value}' is not set")

    # Get step outputs
    outputs = None
    if step_outputs is not None:
        outputs = []
        for o in step_outputs:
            path = "/tmp/entity_" + str(o).replace(".", "_").replace("/", "_")
            outputs.append(Parameter(name=o, value_from=m.ValueFrom(path=path), output=True))
            outputs.append(Artifact(name=o, path=path))

    # Get step inputs
    inputs = None if step_inputs is None else [Parameter(name=i) for i in step_inputs]

    # Get step name
    name = step_name if step_name is not None else uuid4().hex

    return Container(
        name=name,
        image=image,
        command=cmd,
        args=args,
        outputs=outputs,
        inputs=inputs,
    )
