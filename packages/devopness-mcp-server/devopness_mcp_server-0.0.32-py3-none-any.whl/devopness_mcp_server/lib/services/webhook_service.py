from devopness.models import Hook, HookPipelineCreate, HookTypeParam

from ..types import ServerContext


class WebHookService:
    @staticmethod
    async def tool_create_webhook(
        ctx: ServerContext,
        pipeline_id: int,
        hook_type: HookTypeParam,
        hook_settings: HookPipelineCreate,
    ) -> Hook:
        response = await ctx.devopness.hooks.add_pipeline_hook(
            hook_type,
            pipeline_id,
            hook_settings,
        )

        return response.data
