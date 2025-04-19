import uvicorn

from src.shared.environ import env

if __name__ == "__main__":
    uvicorn.run(
        "apps.http.apps:create_app",
        host=env.HOST,
        port=int(env.PORT),
        factory=True,
    )
