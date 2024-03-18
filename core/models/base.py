import re

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped


class Base(DeclarativeBase):
    """
    Создание PK и преобразоывавыние имени таблице из PascalCase в snake_case, дял таблиц БД
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        words_in_name = re.findall("[A-Z][a-z]*", cls.__name__)
        snake_case_name = "_".join(word.lower() for word in words_in_name)
        return snake_case_name
