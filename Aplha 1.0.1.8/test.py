from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from time import sleep

console = Console()

# Список доступных стилей спиннеров
spinner_styles = [
    "line",
    "pipe",
    "simpleDots",
    "simpleDotsScrolling",
    "star",
    "star2",
    "flip",
    "hamburger",
    "growVertical",
    "growHorizontal",
    "balloon",
    "balloon2",
    "noise",
    "bounce",
    "boxBounce",
    "boxBounce2",
    "triangle",
    "arc",
    "circle",
    "squareCorners",
    "circleQuarters",
    "circleHalves",
    "squish",
    "toggle",
    "toggle2",
    "toggle3",
    "toggle4",
    "toggle5",
    "toggle6",
    "toggle7",
    "toggle8",
    "toggle9",
    "toggle10",
    "toggle11",
    "toggle12",
    "toggle13",
    "arrow",
    "arrow2",
    "arrow3",
    "bouncingBar",
    "bouncingBall",
    "smiley",
    "monkey",
    "hearts",
    "clock",
    "earth",
    "moon",
    "runner",
    "pong",
    "shark",
    "dqpb",
    "weather",
    "christmas",
    "grenade",
    "point",
    "layer",
]

for style in spinner_styles:
    console.clear()
    spinner = Spinner(style, text=f"Loading with {style}...")
    with Live(spinner, console=console, refresh_per_second=10):
        sleep(5)
