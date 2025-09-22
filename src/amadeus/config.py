from pathlib import Path

class Config:
    class Paths:
        ROOT: Path = Path(__file__).resolve().parent.parent.parent
        ASSETS: Path = ROOT / "assets"
        WEIGHTS: Path = ASSETS / "weights"
