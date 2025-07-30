from devopness.models import ActionTargetLogStep

from ..models import ActionSummary
from ..response import MCPResponse
from ..types import ServerContext
from ..utils import (
    get_instructions_format_resource_table,
    get_instructions_format_table,
)


class ActionService:
    @staticmethod
    async def tool_get_action_details(
        ctx: ServerContext,
        action_id: int,
    ) -> MCPResponse[ActionSummary]:
        response = await ctx.devopness.actions.get_action(action_id)

        action = ActionSummary.from_sdk_model(response.data)

        resource_url = (
            "https://app.devopness.com"
            "/projects/{action.project_id}/"
            "environments/{action.environment_id}/"
            "{action.resource_type}s/{action.resource_id}"
        )

        target_url = (
            "https://app.devopness.com"
            "/projects/{action.project_id}/"
            "environments/{action.environment_id}/"
            "{action_target.target_type}s/{action_target.target_id}"
        )

        return MCPResponse.ok(
            action,
            [
                get_instructions_format_resource_table(
                    [
                        (
                            "ID",
                            "[{action.id}]({action.url_web_permalink})",
                        ),
                        (
                            "Resource",
                            "[{action.resource_name}"
                            " ({action.resource_type}, ID: {action.resource_id})]"
                            f"({resource_url})",
                        ),
                        (
                            "Operation",
                            "{action.type}",
                        ),
                        (
                            "Status",
                            "MATCHING {action.status}"
                            " CASE 'completed' THEN '🟢 {action.status}'"
                            " CASE 'failed'    THEN '🔴 {action.status}'"
                            " ELSE                  '🟠 {action.status}'",
                        ),
                    ]
                ),
                "For each target, show the information in the format below:",
                "Target: "
                "[{action_target.target_name}"
                " ({action_target.target_type}, ID {action_target.target_id})]"
                f"({target_url})",
                get_instructions_format_table(
                    [
                        (
                            "Step",
                            "{action_target.step.name}"
                            " ({action_target.step.action_target_step_order}/{action_target.steps_count})",  # noqa: E501
                        ),
                        (
                            "Status",
                            "MATCHING {action_target.step.status}"
                            " CASE 'completed' THEN '🟢 {action_target.step.status}'"
                            " CASE 'failed'    THEN '🔴 {action_target.step.status}'"
                            " ELSE                  '🟠 {action_target.step.status}'",
                        ),
                    ]
                ),
                "You MUST offer to investigate and fix the failed steps.",
                "Use imperative language and avoid ambiguity.",
            ],
        )

    @staticmethod
    async def tool_get_action_step_logs(
        ctx: ServerContext,
        action_id: int,
        action_target_id: int,
        action_target_step_order: int,
    ) -> MCPResponse[ActionTargetLogStep]:
        response = await ctx.devopness.actions.get_action_log(
            action_id,
            action_target_step_order,
            action_target_id,
        )

        return MCPResponse.ok(
            response.data.step,
            [
                "You MUST analyze the log to determine the cause of the failure.",
                "You MUST summarize the issue clearly and concisely for the user.",
                "You MUST explicitly offer to investigate and resolve the problem.",
                "You MUST offer to attempt to retry the action,"
                " using the exact same targets (eg, servers) as the original action.",
                "You MUST extract all necessary information"
                " (eg, resource ID, type, and targets (eg, server)) from the original"
                " action details to perform the retry.",
                "Do NOT ask the user for information already present in the action.",
            ],
        )
