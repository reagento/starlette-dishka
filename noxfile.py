import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

INSTALL_CMD = ("-e", ".", "--group", "tests")


@nox.session(tags=["ci"])
def starlette_0270(session: nox.Session) -> None:
    session.install(
        "starlette == 0.27.0",
        *INSTALL_CMD,
        silent=False,
    )
    session.run("pytest", "tests/")


@nox.session(tags=["latest"])
def starlette_latest(session: nox.Session) -> None:
    session.install(
        "starlette",
        *INSTALL_CMD,
        silent=False,
    )
    session.run("pytest", "tests/")


