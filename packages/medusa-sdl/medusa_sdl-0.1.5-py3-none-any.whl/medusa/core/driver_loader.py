from importlib.metadata import entry_points
from typing import Dict, Tuple, Type
import inspect, json

_EP_GROUP = "medusa.devices"

def discover() -> dict[str, type]:
    """Return {'TecanXCPump': <class ...>, ...} for *all* installed plugins."""
    return {ep.name: ep.load() for ep in entry_points(group=_EP_GROUP)}

# global, evaluated once at import-time
DEVICE_REGISTRY: dict[str, type] = discover()

def get_driver(name: str):
    """Return the concrete driver class, or raise a clear error."""
    try:
        return DEVICE_REGISTRY[name]
    except KeyError as e:
        raise ValueError(
            f"No driver named '{name}'. Install the plugin, e.g.  pip install medusa-devices-{name.lower()}"
        ) from e
    
def get_classes_by_category(category: str) -> Tuple[Type, ...]:
    """All drivers whose class attribute  `category == category` ."""
    return tuple(
        cls for cls in DEVICE_REGISTRY.values()
        if getattr(cls, "category", None) == category
    )

def get_classes_by_category_or_name(category: str) -> Tuple[Type, ...]:
    cat_lower = category.lower()
    out = []
    for cls in DEVICE_REGISTRY.values():
        cls_cat = getattr(cls, "category", "").lower()
        name   = cls.__name__.lower()
        # match exact category OR substring match on class name
        if cls_cat == cat_lower or cat_lower in name:
            out.append(cls)
    return tuple(out)

def get_category_map() -> Dict[Type, str]:
    """{DriverClass: 'Pump' | 'Valve' | ...} for every installed class."""
    return {
        cls: getattr(cls, "category", cls.__name__)
        for cls in DEVICE_REGISTRY.values()
    }

def node_definitions() -> dict:
    """
    Build the JSON sent to the front end:
    {
      "pump":  { "options": ["TecanXCPump", "JKemPump"], "settings": [...] },
      "valve": { ... },
      ...
    }
    Only parameters listed in `ui_fields` *or* that have **no default**
    appear in the `settings` array.
    """
    defs: dict[str, dict[str, list|dict]] = {}

    for cls in DEVICE_REGISTRY.values():

        # ---------- 1) CATEGORY ------------------------------------------------
        cat = getattr(cls, "category", None)
        if not cat:                 # try to infer from class-name suffix
            for suffix in ("Pump", "Valve", "Hotplate", "Relay", "Vessel", "Shaker", "Balance"):
                if cls.__name__.lower().endswith(suffix.lower()):
                    cat = suffix; break
        if not cat:
            cat = "Device"          # last-ditch catch-all

        base = cat.lower()          # pump / valve / …

        defs.setdefault(base, {"options": [], "settings": [], "driver_defaults": {}})
        defs[base]["options"].append(cls.__name__)

        # ---------- 2) WHICH FIELDS TO EXPOSE ---------------------------------
        ui_only = getattr(cls, "ui_fields", None)  # may be None

        sig = inspect.signature(cls.__init__)
        driver_defaults = defs[base]["driver_defaults"].setdefault(cls.__name__, {})
        for p in list(sig.parameters.values())[1:]:     # skip self
            driver_defaults[p.name] = (None if p.default is inspect._empty else p.default)

            # a) ui_fields takes absolute priority
            if ui_only is not None and p.name not in ui_only:
                continue

            # b) if ui_fields absent → show **only** params with *no* default
            if ui_only is None and p.default is not inspect._empty:
                continue

            # avoid duplicates when multiple drivers share the same key
            # if any(f["key"] == p.name for f in defs[base]["settings"]):
            #     continue
            # driver_defaults[p.name] = None if p.default is inspect._empty else p.default
            existing = next((f for f in defs[base]["settings"] if f["key"] == p.name), None)
            
            kind = "string"
            if p.annotation in (int,   "int"):   kind = "int"
            if p.annotation in (float, "float"): kind = "float"
            if p.annotation in (bool,  "bool"):  kind = "bool"
            # driver_defaults.setdefault(cls.__name__, {})[p.name] = ( None if p.default is inspect._empty else p.default)

            def _merged_default(old, new):
                if old is None:          return None
                if old == new:           return old
                return None
            
            new_def = None if p.default is inspect._empty else p.default

            if existing:
                existing["default"] = _merged_default(existing["default"], new_def)
            else:
                defs[base]["settings"].append(
                    {"key": p.name,
                    "label": p.name.replace('_', ' ').title(),
                    "type":  kind,
                    "default": driver_defaults#(None if p.default is inspect._empty else p.default)
                    }
                )

    return defs