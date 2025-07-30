from pathlib import Path
from typing import Optional

import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    TinybirdAgentContext,
    create_terminal_box,
    show_confirmation,
    show_input,
)
from tinybird.tb.modules.feedback_manager import FeedbackManager


def create_tests(ctx: RunContext[TinybirdAgentContext], pipe_name: str, test_content: str) -> str:
    """Given a pipe name, create or update a test for it

    Args:
        pipe_name (str): The pipe name to create a test for. Required.
        test_content (str): The content of the test. Required.

    Returns:
        str: If the test was created or updated and the result of running the tests.
    """
    running_tests = False
    try:
        ctx.deps.thinking_animation.stop()
        path = Path(ctx.deps.folder) / "tests" / f"{pipe_name}.yaml"
        current_test_content: Optional[str] = None
        if path.exists():
            current_test_content = path.read_text()

        if current_test_content:
            content = create_terminal_box(current_test_content, new_content=test_content, title=path.name)
        else:
            content = create_terminal_box(test_content, title=path.name)

        click.echo(content)
        action_text = "Create" if not current_test_content else "Update"
        confirmation = show_confirmation(
            title=f"{action_text} '{path.name}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        folder_path = path.parent
        folder_path.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        path.write_text(test_content)
        action_text = "created" if not current_test_content else "updated"
        click.echo(FeedbackManager.success(message=f"✓ {path.name} {action_text}"))
        running_tests = True
        test_output = ctx.deps.run_tests(pipe_name=pipe_name)
        click.echo(test_output)
        ctx.deps.thinking_animation.start()
        return f"Test {action_text} for '{pipe_name}' endpoint in {path} and ran successfully\n{test_output}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        error_message = str(e).replace("test_error__error__", "")
        ctx.deps.thinking_animation.stop()
        if not running_tests:
            click.echo(FeedbackManager.error(message=error_message))
        ctx.deps.thinking_animation.start()
        if running_tests:
            return f"Test {action_text} for '{pipe_name}' endpoint in {path} but there were errors running the tests: {error_message}"
        return f"Error creating test for '{pipe_name}' endpoint: {error_message}"


def run_tests(ctx: RunContext[TinybirdAgentContext], pipe_name: Optional[str] = None) -> str:
    """Run tests for a given pipe name or all tests in the project

    Args:
        pipe_name (Optional[str]): The pipe name to run tests for. If not provided, all tests in the project will be run.

    Returns:
        str: The result of running the tests.
    """

    try:
        ctx.deps.thinking_animation.stop()
        path = Path(ctx.deps.folder) / "tests" / f"{pipe_name}.yaml"

        title = f"Run tests for '{pipe_name}'?" if pipe_name else "Run all tests in the project?"
        confirmation = show_confirmation(
            title=title,
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm the proposed changes and gave the following feedback: {feedback}"

        test_output = ctx.deps.run_tests(pipe_name=pipe_name)
        click.echo(test_output)
        ctx.deps.thinking_animation.start()
        if pipe_name:
            return f"Tests for '{pipe_name}' endpoint in {path} and ran successfully\n{test_output}"
        else:
            return f"All tests in the project ran successfully\n{test_output}"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        error_message = str(e)
        test_exit_code = "test_error__error__"
        test_error = test_exit_code in error_message
        ctx.deps.thinking_animation.stop()
        if not test_error:
            click.echo(FeedbackManager.error(message=error_message))
        else:
            error_message = error_message.replace(test_exit_code, "")
        ctx.deps.thinking_animation.start()
        return f"Error running tests: {error_message}"
