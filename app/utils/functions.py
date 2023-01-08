from aiogram.utils.deep_linking import get_start_link
from sqlalchemy.orm import Session

from db.models.user import User
from db.models.group import Group

from common.variables import engine


async def get_invite_link(user_uuid: int) -> str | None:
    """Return invite link to group by user TELEGRAM id or None.

    Args:
        user_uuid (int): TELEGRAM USER ID

    Returns:
        str | None: link
    """
    with Session(engine) as s:
        me: User = s.query(User).filter_by(uuid=user_uuid).first()
        if me.group_id is None:
            return None
        group: Group = s.query(Group).filter_by(id=me.group_id).first()

    return await get_start_link(str(group.uuid), encode=True)

