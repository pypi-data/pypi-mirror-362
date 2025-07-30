from devopness.models import UserMe

from ..types import ServerContext


class UserService:
    @staticmethod
    async def tool_get_user_profile(
        ctx: ServerContext,
    ) -> UserMe:
        current_user = await ctx.devopness.users.get_user_me()

        return current_user.data
