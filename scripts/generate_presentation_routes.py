import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "scripts" / "presentation_targets.json"


def build_route(route_src: str) -> str:
    return f"""---
layout: false
---

<iframe
  src="{route_src}"
  title="文章演示版"
  style="position: fixed; inset: 0; width: 100vw; height: 100vh; border: 0; background: #07130f;"
></iframe>
"""


def main() -> None:
    targets = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    for target in targets:
      route_path = ROOT / target["route"]
      route_path.parent.mkdir(parents=True, exist_ok=True)
      route_path.write_text(build_route(target["routeSrc"]), encoding="utf-8")
      print(route_path)


if __name__ == "__main__":
    main()
