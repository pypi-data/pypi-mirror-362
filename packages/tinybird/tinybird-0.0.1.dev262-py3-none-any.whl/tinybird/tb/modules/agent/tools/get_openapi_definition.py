import click
import requests
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.feedback_manager import FeedbackManager


def get_openapi_definition(ctx: RunContext[TinybirdAgentContext], endpoint_name: str, cloud: bool = False):
    """Get the OpenAPI definition for an endpoint:

    Args:
        endpoint_name (str): The name of the endpoint to get the OpenAPI definition for. Required.
        cloud (bool): Whether to get the OpenAPI definition from cloud or local. Optional.

    Returns:
        str: The OpenAPI definition for the endpoint.
    """

    cloud_or_local = "Cloud" if cloud else "Local"
    ctx.deps.thinking_animation.stop()

    click.echo(
        FeedbackManager.highlight(
            message=f"» Checking OpenAPI definition for '{endpoint_name}' in Tinybird {cloud_or_local}"
        )
    )
    try:
        host = ctx.deps.host if cloud else ctx.deps.local_host
        token = ctx.deps.token if cloud else ctx.deps.local_token
        url = f"{host}/v0/pipes/openapi.json"

        result = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if result.status_code != 200:
            raise Exception(f"Failed to get OpenAPI definition: {result.status_code} {result.text}")

        data = result.json()
        openapi_definition = str(data["paths"].get(f"/pipes/{endpoint_name}.{{format}}", ""))

        if not openapi_definition:
            raise Exception(f"Endpoint {endpoint_name} not found in OpenAPI definition")

        if not cloud:
            # TODO(rafa): This is a temporary fix to get the correct host for the local environment.
            openapi_definition = openapi_definition.replace("http://localhost:8001", host)

        click.echo(FeedbackManager.success(message="✓ Done!"))
        ctx.deps.thinking_animation.start()
        return f"OpenAPI definition for {cloud_or_local} endpoints: {openapi_definition}. <dev_note>Add the base url to each path so the user can copy paste if needed: {host}</dev_note>"
    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Error getting OpenAPI definition: {e}"))
        ctx.deps.thinking_animation.start()
        return f"Error getting OpenAPI definition: {e}"
