import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import AgentRunCancelled, TinybirdAgentContext, show_confirmation, show_input
from tinybird.tb.modules.feedback_manager import FeedbackManager


def append_file(
    ctx: RunContext[TinybirdAgentContext], datasource_name: str, fixture_pathname: str, cloud: bool = False
) -> str:
    """Append existing fixture to a datasource

    Args:
        datasource_name: Name of the datasource to append fixture to
        fixture_pathname: Path to the fixture file to append
        cloud: Whether to append the fixture to the cloud or local environment. Optional.

    Returns:
        str: Message indicating the success or failure of the appending
    """
    try:
        ctx.deps.thinking_animation.stop()
        cloud_or_local = "Cloud" if cloud else "Local"
        confirmation = show_confirmation(
            title=f"Append fixture {fixture_pathname} to datasource '{datasource_name}' in Tinybird {cloud_or_local}?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm appending {fixture_pathname} fixture in Tinybird {cloud_or_local} and gave the following feedback: {feedback}"

        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Appending {fixture_pathname} to {datasource_name}..."))
        if cloud:
            ctx.deps.append_data_cloud(datasource_name=datasource_name, path=fixture_pathname)
        else:
            ctx.deps.append_data_local(datasource_name=datasource_name, path=fixture_pathname)
        click.echo(FeedbackManager.success(message=f"✓ Data appended to {datasource_name}"))
        ctx.deps.thinking_animation.start()
        return f"Data appended to {datasource_name} in Tinybird {cloud_or_local}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        error_message = str(e)
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=error_message))
        error_message = handle_quarantine_error(ctx, error_message, datasource_name)
        ctx.deps.thinking_animation.start()
        return f"Error appending fixture {fixture_pathname} to {datasource_name} in Tinybird {cloud_or_local}: {error_message}"


def append_url(
    ctx: RunContext[TinybirdAgentContext], datasource_name: str, fixture_url: str, cloud: bool = False
) -> str:
    """Append existing fixture to a datasource

    Args:
        datasource_name: Name of the datasource to append fixture to
        fixture_url: external url to the fixture file to append
        cloud: Whether to append the fixture to the cloud or local environment. Optional.

    Returns:
        str: Message indicating the success or failure of the appending
    """
    try:
        ctx.deps.thinking_animation.stop()
        cloud_or_local = "Cloud" if cloud else "Local"
        confirmation = show_confirmation(
            title=f"Append URL {fixture_url} to datasource '{datasource_name}' in Tinybird {cloud_or_local}?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm appending URL {fixture_url} in Tinybird {cloud_or_local} and gave the following feedback: {feedback}"

        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Appending {fixture_url} to {datasource_name}..."))
        if cloud:
            ctx.deps.append_data_cloud(datasource_name=datasource_name, path=fixture_url)
        else:
            ctx.deps.append_data_local(datasource_name=datasource_name, path=fixture_url)
        click.echo(FeedbackManager.success(message=f"✓ Data appended to {datasource_name}"))
        ctx.deps.thinking_animation.start()
        return f"Data appended to {datasource_name} in Tinybird {cloud_or_local}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        error_message = str(e)
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=error_message))
        error_message = handle_quarantine_error(ctx, error_message, datasource_name)
        ctx.deps.thinking_animation.start()
        return f"Error appending URL {fixture_url} to {datasource_name} in Tinybird {cloud_or_local}: {error_message}"


def handle_quarantine_error(ctx: RunContext[TinybirdAgentContext], error_message: str, datasource_name: str) -> str:
    try:
        if "in quarantine" in error_message:
            click.echo(FeedbackManager.highlight(message=f"» Looking for errors in {datasource_name}_quarantine..."))
            query = (
                f"select * from {datasource_name}_quarantine order by insertion_date desc limit 5 FORMAT CSVWithNames"
            )
            quarantine_data = ctx.deps.execute_query_local(query=query)
            error_message = (
                error_message
                + f"\nThese are the first 5 rows of the quarantine table for datasource '{datasource_name}':\n{quarantine_data}. Use again `mock` tool but add this issue to the context."
            )

    except Exception as quarantine_error:
        error_message = error_message + f"\nError accessing to {datasource_name}_quarantine: {quarantine_error}"

    return error_message
