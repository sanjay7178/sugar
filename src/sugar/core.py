"""Sugar core libraries."""

from __future__ import annotations

from typing import Dict, Type

from sugar.extensions.base import SugarBase
from sugar.extensions.compose import SugarCompose
from sugar.extensions.compose_ext import SugarComposeExt
from sugar.extensions.podman_compose import SugarPodmanCompose
from sugar.extensions.podman_compose_ext import SugarPodmanComposeExt
from sugar.extensions.stats import SugarStats

# from sugar.extensions.swarm import SugarSwarm

# Extensions registry - maps extension name to extension class
extensions: Dict[str, Type[SugarBase]] = {
    'compose': SugarCompose,
    'compose-ext': SugarComposeExt,
    'stats': SugarStats,
    # 'swarm': SugarSwarm,
    'podman-compose': SugarPodmanCompose,
    'podman-compose-ext': SugarPodmanComposeExt,
}
