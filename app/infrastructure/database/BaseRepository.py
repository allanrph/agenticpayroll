from sqlalchemy.ext.asyncio.session import AsyncSession


class BaseRepository:
    """
    A base class for repository implementations.
    It expects an AsyncSession to be injected upon instantiation.
    """
    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """Provides access to the SQLAlchemy AsyncSession."""
        return self._session
