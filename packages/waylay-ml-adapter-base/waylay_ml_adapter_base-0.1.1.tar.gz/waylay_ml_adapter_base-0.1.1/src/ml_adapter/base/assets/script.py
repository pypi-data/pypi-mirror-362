"""Default ml adapter scripts."""


def no_script(adapter: type, **kwargs):
    """Produce a placeholder script."""
    return """
# Script not provided, please use the correct ML Adapter.
"""


def default_webscript_script(
    adapter_class: type, model_path=None, model_class=None
) -> str:
    """Get a default model loading script for webscripts."""
    adapter_fqn = f"{adapter_class.__module__}.{adapter_class.__name__}"
    model_class_ref = (
        f"'{model_class.__module__}.{model_class.__name__}'" if model_class else "None"
    )
    model_path_ref = f"'{model_path}'" if model_path else "None"
    return f"""
# {adapter_fqn} model adapter
import os
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from {adapter_class.__module__} import {adapter_class.__name__}

MODEL_PATH = os.environ.get('MODEL_PATH', {model_path_ref})
MODEL_CLASS = os.environ.get('MODEL_CLASS', {model_class_ref})

# Initialize the model adapter.
# Provide a `model` argument if you want to create/load the model yourself.
adapter = {adapter_class.__name__}(
    model_path=MODEL_PATH, model_class=MODEL_CLASS
)

# Webscript handler
async def execute(request: Request):
    if request.method == 'GET':
        return JSONResponse(adapter.openapi)
    if request.method != 'POST':
        raise HTTPException(
            status_code=405,
            detail='This webscript only accepts `POST` calls.',
        )
    # use request body as input
    request_json = await request.json()
    # call the model adapter using the V1
    response_json = await adapter.call(request_json)
    return JSONResponse(response_json)
"""


def default_plug_v1_script(
    adapter_class: type,
    model_path: str | None = None,
    model_class: type | None = None,
    state_ok="PREDICTED",
    state_nok="FAILED",
) -> str:
    """Get a default model loading script for plugs."""
    adapter_fqn = f"{adapter_class.__module__}.{adapter_class.__name__}"
    model_class_ref = (
        f"'{model_class.__module__}.{model_class.__name__}'" if model_class else "None"
    )
    model_path_ref = f"'{model_path}'" if model_path else "None"
    return f"""
# {adapter_fqn} model adapter
import os
from ml_adapter.api.data import v1 as V1
from {adapter_class.__module__} import {adapter_class.__name__}

# optional type alias for plug response
StatusAndRawData = tuple[str, V1.V1PredictionResponse|V1.V1ErrorResponse]

STATE_OK = '{state_ok}'
STATE_NOK = '{state_nok}'

MODEL_PATH = os.environ.get('MODEL_PATH', {model_path_ref})
MODEL_CLASS = os.environ.get('MODEL_CLASS', {model_class_ref})

# Initialize the model adapter.
# Provide a `model` argument if you want to create/load the model yourself.
adapter = {adapter_class.__name__}(
    model_path=MODEL_PATH, model_class=MODEL_CLASS
)

async def execute(properties: V1.V1Request, console, logger) -> StatusAndRawData:
    try:
        result = await adapter.call(properties)
        return (STATE_OK, result)
    except Exception as err:
        logger.exception(err)
        error_message = str(err)
        console.error(error_message)
        return (STATE_NOK, {{ 'error': error_message, 'predictions': [] }})
"""
