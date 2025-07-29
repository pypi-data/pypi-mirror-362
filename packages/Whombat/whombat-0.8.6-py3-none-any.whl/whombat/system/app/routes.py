from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from whombat.plugins import add_plugin_pages, add_plugin_routes, load_plugins
from whombat.system.settings import Settings

ROOT_DIR = Path(__file__).parent.parent.parent


__all__ = ["add_routes"]


def add_routes(app: FastAPI, settings: Settings):
    # NOTE: Import routes here to avoid circular imports
    from whombat.routes import get_main_router

    # Add default routes.
    main_router = get_main_router(settings)
    app.include_router(main_router)

    # Load plugins.
    for name, plugin in load_plugins():
        add_plugin_routes(app, name, plugin)
        add_plugin_pages(app, name, plugin)

    # Make sure the user guide directory exists.
    # Otherwise app initialization will fail.
    user_guide_dir = ROOT_DIR / "user_guide"
    if not user_guide_dir.exists():
        user_guide_dir.mkdir(parents=True, exist_ok=True)

    statics_dir = ROOT_DIR / "statics"
    if not statics_dir.exists():
        statics_dir.mkdir(parents=True, exist_ok=True)

    app.mount(
        "/guide/",
        StaticFiles(
            packages=[("whombat", "user_guide")],
            html=True,
            check_dir=False,
        ),
        name="guide",
    )

    # NOTE: It is important that the static files are mounted after the
    # plugin routes, otherwise the plugin routes will not be found.
    app.mount(
        "/",
        StaticFiles(packages=["whombat"], html=True),
        name="static",
    )
