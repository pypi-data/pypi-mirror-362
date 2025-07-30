"""
Defines the settings for scubalspy.
"""

import os
import pathlib


class ScubalspySettings:
    """
    Provides the various settings for scubalspy.
    """
    @staticmethod
    def get_language_server_directory() -> str:
        """Returns the directory for language servers"""
        user_home = pathlib.Path.home()
        scubalspy_dir = str(pathlib.PurePath(user_home, ".scubalspy"))
        lsp_dir = str(pathlib.PurePath(scubalspy_dir, "lsp"))
        os.makedirs(lsp_dir, exist_ok=True)
        return lsp_dir

    @staticmethod
    def get_global_cache_directory() -> str:
        """Returns the cache directory"""
        global_cache_dir = os.path.join(str(pathlib.Path.home()), ".scubalspy", "global_cache")
        os.makedirs(global_cache_dir, exist_ok=True)
        return global_cache_dir
