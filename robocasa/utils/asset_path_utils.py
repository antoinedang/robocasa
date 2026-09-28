import os
import re

import robocasa
import robosuite


LOCAL_ROBOCASA_ASSET_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(robocasa.__file__), "models", "assets")
)
LOCAL_ROBOSUITE_ASSET_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(robosuite.__file__), "models", "assets")
)


def normalize_robocasa_asset_path(path):
    """Rebase stale RoboCasa or RoboSuite asset paths onto active installations."""
    if not path:
        return path

    path = os.path.normpath(path)
    if os.path.exists(path):
        return path

    asset_marker = "models/assets/"
    if asset_marker not in path:
        return path

    suffix = path.split(asset_marker, 1)[1]
    robocasa_marker = "/robocasa/models/assets/"
    robosuite_marker = "/robosuite/models/assets/"
    robocasa_index = path.rfind(robocasa_marker)
    robosuite_index = path.rfind(robosuite_marker)

    if robosuite_index > robocasa_index:
        asset_roots = (LOCAL_ROBOSUITE_ASSET_ROOT, LOCAL_ROBOCASA_ASSET_ROOT)
    else:
        asset_roots = (LOCAL_ROBOCASA_ASSET_ROOT, LOCAL_ROBOSUITE_ASSET_ROOT)

    candidates = [os.path.normpath(os.path.join(root, suffix)) for root in asset_roots]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return candidates[0]


def rewrite_mjcf_asset_paths(xml_string):
    """Rewrite stale RoboCasa asset paths in MJCF file attributes."""

    def replace_path(match):
        path = normalize_robocasa_asset_path(match.group(1))
        return f'file="{path}"'

    return re.sub(r'file="([^"]+)"', replace_path, xml_string)