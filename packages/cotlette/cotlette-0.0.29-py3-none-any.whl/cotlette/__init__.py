__version__ = "0.0.29"


import os
import logging
# import importlib.util
import importlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from cotlette.conf import settings
from cotlette import shortcuts



logger = logging.getLogger("uvicorn")


class Cotlette(FastAPI):

    def __init__(self):
        super().__init__()

        self.settings = settings
        self.shortcuts = shortcuts

        # Get absolute path to current directory
        self.cotlette_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Include routers
        self.include_routers()
        self.include_templates()
        self.include_static()

    def include_routers(self):
        # Check and import installed applications
        logger.info(f"Loading apps and routers:")
        for app_path in self.settings.INSTALLED_APPS:
            # Dynamically import module
            module = importlib.import_module(app_path)
            logger.info(f"✅'{app_path}'")

            # If module contains routers, include them
            if hasattr(module, "router"):
                self.include_router(module.router)
                logger.info(f"✅'{app_path}.router'")
            else:
                logger.warning(f"⚠️ '{app_path}.router'")

    def include_templates(self):
        # Include templates specified by user in SETTINGS
        for template in self.settings.TEMPLATES:
            template_dirs = template.get("DIRS")
            template_dirs = [os.path.join(self.settings.BASE_DIR, path) for path in template_dirs]

    def include_static(self):
        # Include framework static files
        static_dir = os.path.join(self.cotlette_directory, "static")
        self.mount("/static", StaticFiles(directory=static_dir), name="static")

        # Include static files specified by user in SETTINGS
        if self.settings.STATIC_URL:
            static_dir = os.path.join(self.settings.BASE_DIR, self.settings.STATIC_URL)
            self.mount("/static", StaticFiles(directory=static_dir), name="static")