import os
from pathlib import Path

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    Datafile,
    TinybirdAgentContext,
    create_terminal_box,
    show_confirmation,
    show_input,
)
from tinybird.tb.modules.exceptions import CLIBuildException
from tinybird.tb.modules.feedback_manager import FeedbackManager


def create_datafile(ctx: RunContext[TinybirdAgentContext], resource: Datafile) -> str:
    """Given a resource representation, create a file in the project folder

    Args:
        resource (Datafile): The resource to create. Required.

    Returns:
        str: If the resource was created or not.
    """
    try:
        ctx.deps.thinking_animation.stop()
        resource.pathname = resource.pathname.removeprefix("/")
        path = Path(ctx.deps.folder) / resource.pathname
        content = resource.content
        exists = str(path) in ctx.deps.get_project_files()
        if exists:
            content = create_terminal_box(path.read_text(), resource.content, title=resource.pathname)
        else:
            content = create_terminal_box(resource.content, title=resource.pathname)
        click.echo(content)
        action = "Create" if not exists else "Update"
        confirmation = show_confirmation(
            title=f"{action} '{resource.pathname}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message=f"» Building {resource.pathname}..."))
        folder_path = path.parent
        folder_path.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        path.write_text(resource.content)
        ctx.deps.build_project(test=False, silent=True)
        action_text = "created" if not exists else "updated"
        click.echo(FeedbackManager.success(message=f"✓ {resource.pathname} {action_text}"))
        ctx.deps.thinking_animation.start()
        return f"{action_text} {resource.pathname}"
    except AgentRunCancelled as e:
        raise e
    except CLIBuildException as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error building project: {e}"
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.error(message=e))
        ctx.deps.thinking_animation.start()
        return f"Error creating {resource.pathname}: {e}"


def read_file(ctx: RunContext[TinybirdAgentContext], path: str) -> str:
    """Reads the content of a file.

    Args:
        path (str): The path to the file to read. Required.

    Returns:
        str: The content of the file.
    """
    try:
        ctx.deps.thinking_animation.stop()
        click.echo(FeedbackManager.highlight(message=f"» Reading file {path}..."))
        result = ""
        with open(os.path.join(ctx.deps.folder, path), "r") as f:
            result = f.read()
        ctx.deps.thinking_animation.start()
    except FileNotFoundError:
        result = f"Error: File {path} not found (double check the file path)"

    ctx.deps.thinking_animation.start()
    return result


def update_file(ctx: RunContext[TinybirdAgentContext], path: str, content: str):
    """Updates the content of a file.

    Args:
        path (str): The path to the file to update. Required.
        content (str): The full file content to write. Required.
    """
    try:
        with open(os.path.join(ctx.deps.folder, path), "w") as f:
            f.write(content)
    except FileNotFoundError:
        return f"Error: File {path} not found (double check the file path)"

    return "ok"


def create_file(ctx: RunContext[TinybirdAgentContext], path: str, content: str):
    """Creates a new file with the given content.

    Args:
        path (str): The path to the file to create. Required.
        content (str): The full file content to write. Required.
    """
    os.makedirs(os.path.dirname(os.path.join(ctx.deps.folder, path)), exist_ok=True)
    with open(os.path.join(ctx.deps.folder, path), "w") as f:
        f.write(content)

    return "ok"
