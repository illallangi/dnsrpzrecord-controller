import logging
import os
import pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from os.path import join
import time
from more_itertools import one

LABEL_COMPONENT = "app.kubernetes.io/component"
LABEL_CONTROLLER = "app.kubernetes.io/controller"
LABEL_INSTANCE = "app.kubernetes.io/instance"
LABEL_NAME = "app.kubernetes.io/name"

env = Environment(
    loader=FileSystemLoader(pathlib.Path(__file__).parent.absolute()),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)
env.filters["path_join"] = lambda paths: join(*paths)
env.filters["match_object_by_labels"] = lambda objs, labels: one(
    [
        obj
        for obj in objs
        if all(
            [
                obj.get("metadata", {}).get("labels", {}).get(label, None)
                == labels[label]
                for label in labels
            ]
        )
    ]
)
env.filters["match_objects_by_labels"] = lambda objs, labels: [
    obj
    for obj in objs
    if all(
        [
            obj.get("metadata", {}).get("labels", {}).get(label, None) == labels[label]
            for label in labels
        ]
    )
]

env.filters["match_instance_label"] = lambda objs, instance: [
    obj
    for obj in objs
    if obj.get("metadata", {}).get("labels", {}).get(LABEL_INSTANCE, None) == instance
]


async def rpz_zone(**kwargs):
    try:
        del kwargs["namespace"]
    except KeyError:
        pass

    zone = os.environ.get("ZONE", "dnsrpzrecords.rpz")
    notify = os.environ.get("NOTIFY", "")
    transfer = os.environ.get("TRANSFER", "")

    body = env.get_template("zone.j2").render(
        zone=zone,
        notify=notify,
        transfer=transfer,
        serial=str(int(time.time())),
        **kwargs,
    )

    pathlib.Path("/etc/coredns/zones").mkdir(parents=True, exist_ok=True)

    with open(f"/etc/coredns/zones/{zone}", "w") as writer:
        writer.write(body)
    
    logging.info(body)
