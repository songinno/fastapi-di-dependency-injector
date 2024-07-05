import os
from dependency_injector import containers, providers
from pydantic_settings import BaseSettings
from pydantic import Field
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession

from database import url_object, get_engine
from sqlalchemy import URL, create_engine
from sqlalchemy.pool import StaticPool
from repository import Repository
from service import Service


class DatabaseSettings(BaseSettings):
    url: URL = Field(default=url_object)


class ApplicationSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()


"""
    DeclarativeContainer
      ㅇ 의존성 관리 기본 컨테이너
      ㅇ 의존성 관리 뿐만 아니라, 애플리케이션의 설정도 가능 - 구성(Configuration) provider 이용
        - ini, yaml 파일 / Pydantic Settings 클래스 / dictionary / 환경 변수 등 다양한 소스로 부터 구성 관련 정보를 가져와 프로바이더에 주입
"""


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()  # 구성 프로바이더
    engine = providers.Singleton(get_engine)

    ## Session - Singleton Provider
    session_factory = providers.Singleton(sessionmaker, bind=engine)
    session = providers.Singleton(ScopedSession, session_factory)
    ## Repository, Service - Factory Provider
    repository = providers.Factory(Repository, session_factory=session)
    service = providers.Factory(Service, repository=repository)
