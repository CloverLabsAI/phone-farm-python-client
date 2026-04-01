"""
Pure humanization math — no async, no ADB, no I/O.

Provides functions that compute jittered coordinates, randomized delays,
and per-character typing timings. Consumers apply these values to their
own device control layer (ADB subprocess, ppadb, etc.).
"""

import random

PUNCTUATION = frozenset(".,!?;:'\"-")


def jitter_tap(x: int, y: int, radius: int = 5) -> tuple[int, int]:
    """Return tap coordinates with random jitter within +-radius pixels."""
    return (
        max(0, x + random.randint(-radius, radius)),
        max(0, y + random.randint(-radius, radius)),
    )


def jitter_swipe(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    duration: int,
    *,
    coord_radius: int = 3,
    duration_variance: float = 0.15,
) -> tuple[int, int, int, int, int]:
    """Return swipe parameters with jittered coords and randomized duration."""
    r = coord_radius
    return (
        max(0, x1 + random.randint(-r, r)),
        max(0, y1 + random.randint(-r, r)),
        max(0, x2 + random.randint(-r, r)),
        max(0, y2 + random.randint(-r, r)),
        int(duration * random.uniform(1 - duration_variance, 1 + duration_variance)),
    )


def char_delay(
    char: str,
    prev_char: str = "",
    min_delay: int = 40,
    max_delay: int = 100,
) -> float:
    """Return inter-key delay in seconds for a single typed character."""
    delay_ms = random.randint(min_delay, max_delay)

    if char == " ":
        delay_ms += random.randint(10, 20)
    elif char in PUNCTUATION:
        delay_ms += random.randint(20, 50)

    if char == prev_char:
        delay_ms += random.randint(30, 80)

    # Occasional thinking pause (3% chance)
    if random.random() < 0.03:
        delay_ms += random.randint(100, 250)

    return delay_ms / 1000


def random_delay(base: float, jitter: float = 0.5) -> float:
    """Return a randomized delay in seconds around a base value."""
    return max(0.0, random.uniform(base - jitter, base + jitter))


def post_tap_delay() -> float:
    """Return a small post-tap delay in seconds (simulates finger lift)."""
    return random.randint(50, 150) / 1000


def pre_keyevent_delay() -> float:
    """Return a small pre-keyevent delay in seconds."""
    return random.randint(30, 80) / 1000
