import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import TinybirdAgentContext, show_confirmation, show_input
from tinybird.tb.modules.exceptions import CLIDeploymentException
from tinybird.tb.modules.feedback_manager import FeedbackManager


def deploy(ctx: RunContext[TinybirdAgentContext]) -> str:
    """Deploy the project"""
    try:
        ctx.deps.thinking_animation.stop()
        confirmation = show_confirmation(
            title="Deploy the project?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm deployment and gave the following feedback: {feedback}"

        click.echo(FeedbackManager.highlight(message="» Deploying project..."))
        ctx.deps.deploy_project()
        click.echo(FeedbackManager.success(message="✓ Project deployed successfully"))
        ctx.deps.thinking_animation.start()
        return "Project deployed successfully"
    except CLIDeploymentException as e:
        ctx.deps.thinking_animation.start()
        return f"Error depoying project: {e}"
