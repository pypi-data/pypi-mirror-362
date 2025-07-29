import asyncio
import shlex
import subprocess
import sys
from functools import partial
from pathlib import Path
from typing import Any, Optional

import click
import humanfriendly
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart

from tinybird.tb.client import TinyB
from tinybird.tb.modules.agent.animations import ThinkingAnimation
from tinybird.tb.modules.agent.banner import display_banner
from tinybird.tb.modules.agent.memory import clear_history, clear_messages, load_messages, save_messages
from tinybird.tb.modules.agent.models import create_model, model_costs
from tinybird.tb.modules.agent.prompts import agent_system_prompt, resources_prompt
from tinybird.tb.modules.agent.tools.analyze import analyze_file, analyze_url
from tinybird.tb.modules.agent.tools.append import append_file, append_url
from tinybird.tb.modules.agent.tools.build import build
from tinybird.tb.modules.agent.tools.create_datafile import create_datafile
from tinybird.tb.modules.agent.tools.deploy import deploy
from tinybird.tb.modules.agent.tools.deploy_check import deploy_check
from tinybird.tb.modules.agent.tools.diff_resource import diff_resource
from tinybird.tb.modules.agent.tools.execute_query import execute_query
from tinybird.tb.modules.agent.tools.get_endpoint_stats import get_endpoint_stats
from tinybird.tb.modules.agent.tools.get_openapi_definition import get_openapi_definition
from tinybird.tb.modules.agent.tools.mock import mock
from tinybird.tb.modules.agent.tools.plan import plan
from tinybird.tb.modules.agent.tools.preview_datafile import preview_datafile
from tinybird.tb.modules.agent.tools.request_endpoint import request_endpoint
from tinybird.tb.modules.agent.utils import AgentRunCancelled, TinybirdAgentContext, show_input
from tinybird.tb.modules.build_common import process as build_process
from tinybird.tb.modules.common import _analyze, _get_tb_client, echo_safe_humanfriendly_tables_format_pretty_table
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.deployment_common import create_deployment
from tinybird.tb.modules.exceptions import CLIBuildException, CLIDeploymentException, CLIMockException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.login_common import login
from tinybird.tb.modules.mock_common import append_mock_data, create_mock_data
from tinybird.tb.modules.project import Project


class TinybirdAgent:
    def __init__(
        self,
        token: str,
        user_token: str,
        host: str,
        workspace_id: str,
        project: Project,
        dangerously_skip_permissions: bool,
        prompt_mode: bool,
    ):
        self.token = token
        self.user_token = user_token
        self.host = host
        self.dangerously_skip_permissions = dangerously_skip_permissions or prompt_mode
        self.project = project
        if prompt_mode:
            self.messages: list[ModelMessage] = load_messages()[-5:]
        else:
            self.messages = []
        self.agent = Agent(
            model=create_model(user_token, host, workspace_id),
            deps_type=TinybirdAgentContext,
            system_prompt=agent_system_prompt,
            tools=[
                Tool(preview_datafile, docstring_format="google", require_parameter_descriptions=True, takes_ctx=False),
                Tool(create_datafile, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(plan, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(build, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(deploy, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(deploy_check, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(mock, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(analyze_file, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(analyze_url, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(append_file, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(append_url, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(
                    get_endpoint_stats, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True
                ),
                Tool(
                    get_openapi_definition,
                    docstring_format="google",
                    require_parameter_descriptions=True,
                    takes_ctx=True,
                ),
                Tool(execute_query, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(request_endpoint, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
                Tool(diff_resource, docstring_format="google", require_parameter_descriptions=True, takes_ctx=True),
            ],
            # history_processors=[self._keep_recent_messages],
        )

        @self.agent.instructions
        def get_local_host(ctx: RunContext[TinybirdAgentContext]) -> str:
            return f"Tinybird Local host: {ctx.deps.local_host}"

        @self.agent.instructions
        def get_cloud_host(ctx: RunContext[TinybirdAgentContext]) -> str:
            return f"Tinybird Cloud host: {ctx.deps.host}"

        @self.agent.instructions
        def get_local_token(ctx: RunContext[TinybirdAgentContext]) -> str:
            return f"Tinybird Local token: {ctx.deps.local_token}"

        @self.agent.instructions
        def get_cloud_token(ctx: RunContext[TinybirdAgentContext]) -> str:
            return f"Tinybird Cloud token: {ctx.deps.token}"

        @self.agent.instructions
        def get_project_files(ctx: RunContext[TinybirdAgentContext]) -> str:
            return resources_prompt(self.project)

        self.thinking_animation = ThinkingAnimation()

    def add_message(self, message: ModelMessage) -> None:
        self.messages.append(message)

    def _keep_recent_messages(self, messages: list[ModelMessage]) -> list[ModelMessage]:
        """Keep only the last 5 messages to manage token usage."""
        return messages[-5:] if len(messages) > 5 else messages

    def _build_agent_deps(self, config: dict[str, Any]) -> TinybirdAgentContext:
        client = TinyB(token=self.token, host=self.host)
        project = self.project
        folder = self.project.folder
        local_client = get_tinybird_local_client(config, test=False, silent=False)
        return TinybirdAgentContext(
            # context does not support the whole client, so we need to pass only the functions we need
            explore_data=client.explore_data,
            build_project=partial(build_project, project=project, config=config),
            deploy_project=partial(deploy_project, project=project, config=config),
            deploy_check_project=partial(deploy_check_project, project=project, config=config),
            mock_data=partial(mock_data, project=project, config=config),
            append_data_local=partial(append_data_local, config=config),
            append_data_cloud=partial(append_data_cloud, config=config),
            analyze_fixture=partial(analyze_fixture, config=config),
            execute_query_cloud=partial(execute_query_cloud, config=config),
            execute_query_local=partial(execute_query_local, config=config),
            request_endpoint_cloud=partial(request_endpoint_cloud, config=config),
            request_endpoint_local=partial(request_endpoint_local, config=config),
            get_datasource_datafile_cloud=partial(get_datasource_datafile_cloud, config=config),
            get_datasource_datafile_local=partial(get_datasource_datafile_local, config=config),
            get_pipe_datafile_cloud=partial(get_pipe_datafile_cloud, config=config),
            get_pipe_datafile_local=partial(get_pipe_datafile_local, config=config),
            get_connection_datafile_cloud=partial(get_connection_datafile_cloud, config=config),
            get_connection_datafile_local=partial(get_connection_datafile_local, config=config),
            get_project_files=project.get_project_files,
            folder=folder,
            thinking_animation=self.thinking_animation,
            workspace_name=self.project.workspace_name,
            dangerously_skip_permissions=self.dangerously_skip_permissions,
            token=self.token,
            user_token=self.user_token,
            host=self.host,
            local_host=local_client.host,
            local_token=local_client.token,
        )

    def run(self, user_prompt: str, config: dict[str, Any]) -> None:
        user_prompt = f"{user_prompt}\n\n{resources_prompt(self.project)}"
        self.thinking_animation.start()
        result = self.agent.run_sync(
            user_prompt,
            deps=self._build_agent_deps(config),
            message_history=self.messages,
        )
        new_messages = result.new_messages()
        self.messages.extend(new_messages)
        save_messages(new_messages)
        self.thinking_animation.stop()
        click.echo(result.output)
        self._echo_usage(config, result)

    async def run_iter(self, user_prompt: str, config: dict[str, Any]) -> None:
        user_prompt = f"{user_prompt}\n\n"
        self.thinking_animation.start()
        deps = self._build_agent_deps(config)

        async with self.agent.iter(user_prompt, deps=deps, message_history=self.messages) as agent_run:
            async for node in agent_run:
                if hasattr(node, "model_response"):
                    for _i, part in enumerate(node.model_response.parts):
                        if hasattr(part, "content") and not agent_run.result:
                            animation_running = self.thinking_animation.running
                            if animation_running:
                                self.thinking_animation.stop()
                            click.echo(FeedbackManager.info(message=part.content))
                            if animation_running:
                                self.thinking_animation.start()

        if agent_run.result is not None:
            new_messages = agent_run.result.new_messages()
            self.messages.extend(new_messages)
            save_messages(new_messages)
            self.thinking_animation.stop()
            self._echo_usage(config, agent_run.result)

    def _echo_usage(self, config: dict[str, Any], result: AgentRunResult) -> None:
        if "@tinybird.co" in config.get("user_email", ""):
            usage = result.usage()
            request_tokens = usage.request_tokens or 0
            response_tokens = usage.response_tokens or 0
            total_tokens = usage.total_tokens or 0
            cost = (
                request_tokens * model_costs["input_cost_per_token"]
                + response_tokens * model_costs["output_cost_per_token"]
            )
            click.echo(f"Input tokens: {request_tokens}")
            click.echo(f"Output tokens: {response_tokens}")
            click.echo(f"Total tokens: {total_tokens}")
            click.echo(f"Cost: ${cost:.6f}")


def run_agent(
    config: dict[str, Any], project: Project, dangerously_skip_permissions: bool, prompt: Optional[str] = None
):
    click.echo(FeedbackManager.highlight(message="» Initializing Tinybird Code..."))
    token = config.get("token", None)
    host = config.get("host", None)
    user_token = config.get("user_token", None)
    workspace_id = config.get("id", "")
    workspace_name = config.get("name", "")
    try:
        if not token or not host or not workspace_id or not user_token:
            yes = click.confirm(
                FeedbackManager.warning(
                    message="Tinybird Code requires authentication. Do you want to authenticate now? [Y/n]"
                ),
                prompt_suffix="",
                show_default=False,
                default=True,
            )
            if yes:
                login(host, auth_host="https://cloud.tinybird.co", workspace=None, interactive=False, method="browser")
                cli_config = CLIConfig.get_project_config()
                config = {**config, **cli_config.to_dict()}
                token = cli_config.get_token()
                user_token = cli_config.get_user_token()
                host = cli_config.get_host()
                workspace_id = cli_config.get("id", "")
                workspace_name = cli_config.get("name", "")

            if not token or not host or not user_token:
                click.echo(
                    FeedbackManager.error(message="Tinybird Code requires authentication. Run 'tb login' first.")
                )
                return

        build_project(config, project, test=False, silent=True)

        # In prompt mode, always skip permissions to avoid interactive prompts
        prompt_mode = prompt is not None
        agent = TinybirdAgent(token, user_token, host, workspace_id, project, dangerously_skip_permissions, prompt_mode)

        # Print mode: run once with the provided prompt and exit
        if prompt:
            agent.run(prompt, config)
            return

        # Interactive mode: show banner and enter interactive loop
        display_banner()
        click.echo(FeedbackManager.info(message="Describe what you want to create and I'll help you build it"))
        click.echo(FeedbackManager.info(message="Run /help for more commands"))

    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Failed to initialize agent: {e}"))
        return

    # Interactive loop
    try:
        while True:
            try:
                user_input = show_input(workspace_name)
                if user_input.startswith("tb "):
                    cmd_parts = shlex.split(user_input)
                    subprocess.run(cmd_parts)
                    continue
                if user_input.lower() in ["/exit", "/quit", "exit", "quit"]:
                    click.echo(FeedbackManager.info(message="Goodbye!"))
                    break
                elif user_input.lower() in ["/clear", "clear"]:
                    clear_history()
                    click.echo(FeedbackManager.info(message="Message history cleared!"))
                    clear_messages()
                    continue
                elif user_input.lower().startswith("select ") or user_input.lower().startswith("with "):
                    query = f"SELECT * FROM ({user_input.strip()}) FORMAT JSON"
                    result = execute_query_local(config, query=query)
                    stats = result["statistics"]
                    seconds = stats["elapsed"]
                    rows_read = humanfriendly.format_number(stats["rows_read"])
                    bytes_read = humanfriendly.format_size(stats["bytes_read"])

                    click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

                    if not result["data"]:
                        click.echo(FeedbackManager.info_no_rows())
                    else:
                        echo_safe_humanfriendly_tables_format_pretty_table(
                            data=[d.values() for d in result["data"][:10]], column_names=result["data"][0].keys()
                        )
                        click.echo("Showing first 10 results\n")
                    continue
                elif user_input.lower() == "/login":
                    subprocess.run(["tb", "login"], check=True)

                    continue
                elif user_input.lower() == "/help":
                    click.echo("• Describe what you want to create: 'Create a user analytics system'")
                    click.echo("• Ask for specific resources: 'Create a pipe to aggregate daily clicks'")
                    click.echo("• Connect to external services: 'Set up a Kafka connection for events'")
                    click.echo("• Type '/exit' or '/quit' to leave")

                    continue
                elif user_input.strip() == "":
                    continue
                else:
                    asyncio.run(agent.run_iter(user_input, config))
            except AgentRunCancelled:
                click.echo(FeedbackManager.info(message="User cancelled the operation"))
                agent.add_message(
                    ModelRequest(
                        parts=[
                            UserPromptPart(
                                content="User cancelled the operation",
                            )
                        ]
                    )
                )
                continue
            except KeyboardInterrupt:
                click.echo(FeedbackManager.info(message="Goodbye!"))
                break
            except EOFError:
                click.echo(FeedbackManager.info(message="Goodbye!"))
                break

    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Error: {e}"))
        sys.exit(1)


def build_project(config: dict[str, Any], project: Project, silent: bool = True, test: bool = True) -> None:
    local_client = get_tinybird_local_client(config, test=test, silent=silent)
    build_error = build_process(
        project=project, tb_client=local_client, watch=False, silent=silent, exit_on_error=False
    )
    if build_error:
        raise CLIBuildException(build_error)


def deploy_project(config: dict[str, Any], project: Project) -> None:
    client = _get_tb_client(config["token"], config["host"])
    try:
        create_deployment(
            project=project,
            client=client,
            config=config,
            wait=True,
            auto=True,
            allow_destructive_operations=False,
        )
    except SystemExit as e:
        raise CLIDeploymentException(e.args[0])


def deploy_check_project(config: dict[str, Any], project: Project) -> None:
    client = _get_tb_client(config["token"], config["host"])
    try:
        create_deployment(project=project, client=client, config=config, check=True, wait=True, auto=True)
    except SystemExit as e:
        raise CLIDeploymentException(e.args[0])


def append_data_local(config: dict[str, Any], datasource_name: str, path: str) -> None:
    client = get_tinybird_local_client(config, test=False, silent=False)
    append_mock_data(client, datasource_name, path)


def append_data_cloud(config: dict[str, Any], datasource_name: str, path: str) -> None:
    client = _get_tb_client(config["token"], config["host"])
    append_mock_data(client, datasource_name, path)


def mock_data(
    config: dict[str, Any],
    project: Project,
    datasource_name: str,
    data_format: str,
    rows: int,
    context: Optional[str] = None,
) -> list[dict[str, Any]]:
    client = get_tinybird_local_client(config, test=False, silent=False)
    cli_config = CLIConfig.get_project_config()
    datasource_path = project.get_resource_path(datasource_name, "datasource")

    if not datasource_path:
        raise CLIMockException(f"Datasource {datasource_name} not found")

    datasource_content = Path(datasource_path).read_text()
    return create_mock_data(
        datasource_name,
        datasource_content,
        rows,
        context or "",
        cli_config,
        config,
        cli_config.get_user_token() or "",
        client,
        data_format,
        project.folder,
    )


def analyze_fixture(config: dict[str, Any], fixture_path: str, format: str = "json") -> dict[str, Any]:
    local_client = get_tinybird_local_client(config, test=False, silent=True)
    meta, _data = _analyze(fixture_path, local_client, format)
    return meta


def execute_query_cloud(config: dict[str, Any], query: str, pipe_name: Optional[str] = None) -> dict[str, Any]:
    client = _get_tb_client(config["token"], config["host"])
    return client.query(sql=query, pipeline=pipe_name)


def execute_query_local(config: dict[str, Any], query: str, pipe_name: Optional[str] = None) -> dict[str, Any]:
    local_client = get_tinybird_local_client(config, test=False, silent=True)
    return local_client.query(sql=query, pipeline=pipe_name)


def request_endpoint_cloud(
    config: dict[str, Any], endpoint_name: str, params: Optional[dict[str, str]] = None
) -> dict[str, Any]:
    client = _get_tb_client(config["token"], config["host"])
    return client.pipe_data(endpoint_name, format="json", params=params)


def request_endpoint_local(
    config: dict[str, Any], endpoint_name: str, params: Optional[dict[str, str]] = None
) -> dict[str, Any]:
    local_client = get_tinybird_local_client(config, test=False, silent=True)
    return local_client.pipe_data(endpoint_name, format="json", params=params)


def get_datasource_datafile_cloud(config: dict[str, Any], datasource_name: str) -> str:
    try:
        client = _get_tb_client(config["token"], config["host"])
        return client.datasource_file(datasource_name)
    except Exception:
        return "Datasource not found"


def get_datasource_datafile_local(config: dict[str, Any], datasource_name: str) -> str:
    try:
        local_client = get_tinybird_local_client(config, test=False, silent=True)
        return local_client.datasource_file(datasource_name)
    except Exception:
        return "Datasource not found"


def get_pipe_datafile_cloud(config: dict[str, Any], pipe_name: str) -> str:
    try:
        client = _get_tb_client(config["token"], config["host"])
        return client.pipe_file(pipe_name)
    except Exception:
        return "Pipe not found"


def get_pipe_datafile_local(config: dict[str, Any], pipe_name: str) -> str:
    try:
        local_client = get_tinybird_local_client(config, test=False, silent=True)
        return local_client.pipe_file(pipe_name)
    except Exception:
        return "Pipe not found"


def get_connection_datafile_cloud(config: dict[str, Any], connection_name: str) -> str:
    try:
        client = _get_tb_client(config["token"], config["host"])
        return client.connection_file(connection_name)
    except Exception:
        return "Connection not found"


def get_connection_datafile_local(config: dict[str, Any], connection_name: str) -> str:
    try:
        local_client = get_tinybird_local_client(config, test=False, silent=True)
        return local_client.connection_file(connection_name)
    except Exception:
        return "Connection not found"
