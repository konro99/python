import time
import keyboard
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# 7-segment font mapping for numbers and colon
SEGMENT_MAP = {
    "0": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "1": ["  █  ", " ██  ", "  █  ", "  █  ", " ███ "],
    "2": [" ███ ", "    █", " ███ ", "█    ", "█████"],
    "3": [" ███ ", "    █", " ███ ", "    █", " ███ "],
    "4": ["█   █", "█   █", " ████", "    █", "    █"],
    "5": ["█████", "█    ", " ███ ", "    █", " ███ "],
    "6": [" ███ ", "█    ", "████ ", "█   █", " ███ "],
    "7": ["█████", "    █", "   █ ", "  █  ", " █   "],
    "8": [" ███ ", "█   █", " ███ ", "█   █", " ███ "],
    "9": [" ███ ", "█   █", " ████", "    █", " ███ "],
    ":": ["   ", " █ ", "   ", " █ ", "   "]
}

def render_time(minutes, seconds):
    time_str = f"{minutes:02}:{seconds:02}"
    lines = ["" for _ in range(5)]
    
    for char in time_str:
        for i in range(5):
            lines[i] += SEGMENT_MAP[char][i] + "  "
    
    return "\n".join(lines)

def stopwatch(duration_minutes=15):
    console = Console()
    total_seconds = duration_minutes * 60
    paused = False
    remaining = total_seconds
    
    with Live(auto_refresh=True, console=console) as live:
        try:
            while remaining >= 0:
                if keyboard.is_pressed("r"):
                    remaining = total_seconds
                    paused = False  # Reset juga harus menghilangkan pause
                if keyboard.is_pressed("p"):
                    paused = not paused
                    time.sleep(0.5)
                if keyboard.is_pressed("s"):
                    break
                
                if not paused:
                    minutes, seconds = divmod(remaining, 60)
                    time_display = render_time(minutes, seconds)
                    centered_display = Align.center(Text(time_display), vertical="middle")
                    live.update(Panel(centered_display, title="Stopwatch | [cyan]R[/cyan]: Reset | [yellow]P[/yellow]: Pause/Resume | [red]S[/red]: Stop", border_style="cyan", height=10))
                    time.sleep(1)
                    remaining -= 1
            
            live.update(Panel(Align.center("[bold green]Stopwatch stopped![/bold green]", vertical="middle"), border_style="red", height=10))
        except KeyboardInterrupt:
            live.update(Panel(Align.center("[bold red]Stopwatch interrupted![/bold red]", vertical="middle"), border_style="red", height=10))

if __name__ == "__main__":
    stopwatch()
