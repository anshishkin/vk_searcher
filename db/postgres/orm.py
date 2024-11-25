import os
from db.base import BaseEvent
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, inspect
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, relationship

engine = create_engine(os.environ["POSTGRES_PARSER_DATABASE_CONNECTION_URL"], future=True)
Session = sessionmaker(engine, future=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():

    if not inspect(engine).has_table(VK_User.__tablename__):
        VK_User.__table__.create(engine)

    if not inspect(engine).has_table(VK_Contact.__tablename__):
        VK_Contact.__table__.create(engine)


class VK_User(Base):
    __tablename__ = "vk_user"
    vkontakte_id = Column(Integer, primary_key=True)
    full_name: Column = Column(String, nullable=True)
    region: Column = Column(String, nullable=True)
    country: Column = Column(String, nullable=True)
    date_of_birth: Column = Column(String, nullable=True)
    gender: Column = Column(String, nullable=True)

    # vk_contact = relationship("VK_Contact", back_populates="vk_user")


class VK_Contact(Base):
    __tablename__ = "vk_contact"

    id = Column(Integer, primary_key=True)
    vkontakte_id = Column(Integer, nullable=True)  # ForeignKey("vk_user.vkontakte_id")
    last_name: Column = Column(String, nullable=True)
    first_name: Column = Column(String, nullable=True)
    phone_number: Column = Column(String, nullable=True)
    email_address: Column = Column(String, nullable=True)
    vkontakte_url: Column = Column(String, nullable=True)

    # vk_user = relationship("VK_User", foreign_keys=[vkontakte_id], back_populates="vk_contact")


if __name__ == "__main__":
    init_db()
