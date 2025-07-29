from dataclasses import dataclass

from judo.config import set_config_overrides
from judo.optimizers.cem import CrossEntropyMethodConfig
from judo.tasks import CylinderPush, CylinderPushConfig

from .utils.asdf import asdf


@dataclass
class MyCylinderPushConfig(CylinderPushConfig):
    """Custom configuration for MyCylinderPush task."""

class MyCylinderPush(CylinderPush):
    """Custom task to test registration."""

set_config_overrides(
    "my_cylinder_push",
    CrossEntropyMethodConfig,
    {
        "num_nodes": 5,
    },
)

if __name__ == "__main__":
    from judo.cli import app
    from judo.tasks import get_registered_tasks, register_task

    # on running this app, you should see my_cylinder_push in the dropdown
    # you should also see that num_nodes is set to 5 for it, and all other
    # values are set to global defaults with no overrides (so the task will
    # not perform well, but it will run)
    register_task("my_cylinder_push", MyCylinderPush, MyCylinderPushConfig)
    tasks = get_registered_tasks()
    
    app()
