from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Enterprise Incident MCP Server"
    app_env: str = "local"


settings = Settings()
