import typing

try:
    from sqlalchemy import JSON, Column, DateTime, Float, Integer, LargeBinary, String, Text
    from sqlalchemy.orm import DeclarativeBase

    ORM = True
except ImportError:
    ORM = False


if ORM:

    def idcolumn():
        """
        Creates an id column. This method creates an unbounded text field for platforms that support it.

        Returns:
            id column definition
        """

        return String(512).with_variant(Text(), "sqlite", "postgresql")

    class Base(DeclarativeBase):
        """
        Base mapping.
        """

    class Batch(Base):
        """
        Batch temporary table mapping.
        """

        __tablename__ = "batch"
        __table_args__: typing.ClassVar = {"prefixes": ["TEMPORARY"]}

        autoid = Column(Integer, primary_key=True, autoincrement=True)
        indexid = Column(Integer)
        id = Column(idcolumn())
        batch = Column(Integer)

    class Score(Base):
        """
        Scores temporary table mapping.
        """

        __tablename__ = "scores"
        __table_args__: typing.ClassVar = {"prefixes": ["TEMPORARY"]}

        indexid = Column(Integer, primary_key=True, autoincrement=False)
        score = Column(Float)

    class Document(Base):
        """
        Documents table mapping.
        """

        __tablename__ = "documents"

        id = Column(idcolumn(), primary_key=True)
        data = Column(JSON)
        tags = Column(Text)
        entry = Column(DateTime(timezone=True))

    class Object(Base):
        """
        Objects table mapping.
        """

        __tablename__ = "objects"

        id = Column(idcolumn(), primary_key=True)
        object = Column(LargeBinary)
        tags = Column(Text)
        entry = Column(DateTime(timezone=True))

    class SectionBase(Base):
        """
        Generic sections table mapping. Allows multiple section table names for reindexing.
        """

        __abstract__ = True

        indexid = Column(Integer, primary_key=True, autoincrement=False)
        id = Column(idcolumn(), index=True)
        text = Column(Text)
        tags = Column(Text)
        entry = Column(DateTime(timezone=True))

    class Section(SectionBase):
        """
        Section table mapping.
        """

        __tablename__ = "sections"
else:

    def idcolumn():
        return None

    class Base:
        pass

    class Batch(Base):
        __tablename__ = "batch"
        __table_args__: typing.ClassVar = {"prefixes": ["TEMPORARY"]}
        autoid = None
        indexid = None
        id = None
        batch = None

    class Score(Base):
        __tablename__ = "scores"
        __table_args__: typing.ClassVar = {"prefixes": ["TEMPORARY"]}
        indexid = None
        score = None

    class Document(Base):
        __tablename__ = "documents"
        id = None
        data = None
        tags = None
        entry = None

    class Object(Base):
        __tablename__ = "objects"
        id = None
        object = None
        tags = None
        entry = None

    class SectionBase(Base):
        __abstract__ = True
        indexid = None
        id = None
        text = None
        tags = None
        entry = None

    class Section(SectionBase):
        __tablename__ = "sections"
