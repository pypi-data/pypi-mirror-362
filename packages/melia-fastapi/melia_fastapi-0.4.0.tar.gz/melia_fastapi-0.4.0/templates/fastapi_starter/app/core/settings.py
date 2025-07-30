from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

import pydantic

class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    database: str

class ApiSettings(BaseModel):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
    secured: bool = Field(default=False)
    url: str = ""
    title: str
    description: str = Field(default="")
    version: str = Field(default="dev")
    root_path: str = Field(default="")
    cors_origin: str = Field(default="http[s]?://.*")

    @pydantic.validator("url", always=True)
    def default_url(cls, v, *, values):
        return v or f"http{'s' if values['secured'] else ''}://{values['host']}:{values['port']}"

class Settings(BaseSettings):
    app_name: str = "{{project_name}}"
    api: ApiSettings = Field(default_factory=ApiSettings)
    db: DatabaseSettings
    page_size: int = 20
    max_page_size: int = 20

    class Config:
        env_nested_delimiter = "__"
        env_file = ".env"