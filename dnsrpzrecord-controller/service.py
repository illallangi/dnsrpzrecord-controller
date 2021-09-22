from .zone import rpz_zone
import kopf


@kopf.index(
    "service",
)
def service_idx(namespace, body, **_):
    return {
        namespace: {k: body[k] for k in body},
    }


@kopf.on.probe(id=service_idx.__name__)
def service_probe(service_idx: kopf.Index, **_):
    return {namespace: [o for o in service_idx[namespace]] for namespace in service_idx}


@kopf.on.event("service")
async def service_event(**kwargs):
    await rpz_zone(**kwargs)
