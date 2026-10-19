from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pygame


def asset_root() -> Path:
    return Path(__file__).resolve().parent.parent


def make_placeholder_background(size: Tuple[int, int], title: str, top_rgb: Tuple[int, int, int], bottom_rgb: Tuple[int, int, int]) -> pygame.Surface:
    w, h = size
    surf = pygame.Surface((w, h))
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top_rgb[0] * (1 - t) + bottom_rgb[0] * t)
        g = int(top_rgb[1] * (1 - t) + bottom_rgb[1] * t)
        b = int(top_rgb[2] * (1 - t) + bottom_rgb[2] * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (w, y))
    font = pygame.font.SysFont("georgia", 36, bold=True)
    txt = font.render(title, True, (240, 235, 220))
    surf.blit(txt, (w // 2 - txt.get_width() // 2, h // 2 - txt.get_height() // 2))
    hint = pygame.font.SysFont("arial", 18).render("Add PNG to assets/backgrounds/", True, (200, 200, 200))
    surf.blit(hint, (w // 2 - hint.get_width() // 2, h // 2 + 40))
    return surf


def load_background_cover(path: Path, target_w: int, target_h: int) -> pygame.Surface:
    if path.is_file():
        img = pygame.image.load(str(path)).convert()
    else:
        name = path.stem.lower()
        if "cave" in name:
            return make_placeholder_background((target_w, target_h), "Cave (placeholder)", (35, 28, 55), (12, 10, 22))
        if "forest" in name:
            return make_placeholder_background((target_w, target_h), "Forest (placeholder)", (20, 55, 35), (10, 28, 18))
        return make_placeholder_background((target_w, target_h), "Background", (40, 40, 60), (15, 15, 25))

    return scale_cover(img, target_w, target_h)


def scale_cover(surface: pygame.Surface, target_w: int, target_h: int) -> pygame.Surface:
    iw, ih = surface.get_size()
    if iw <= 0 or ih <= 0:
        return make_placeholder_background((target_w, target_h), "?", (30, 30, 30), (10, 10, 10))

    scale = max(target_w / iw, target_h / ih)
    nw = max(1, int(iw * scale))
    nh = max(1, int(ih * scale))
    scaled = pygame.transform.smoothscale(surface, (nw, nh))
    x = max(0, (nw - target_w) // 2)
    y = max(0, (nh - target_h) // 2)
    rect = pygame.Rect(x, y, min(target_w, nw), min(target_h, nh))
    out = pygame.Surface((target_w, target_h))
    out.blit(scaled, (0, 0), rect)
    return out.convert()


def load_ui_image(path: Path, max_w: int, max_h: int) -> pygame.Surface:
    if path.is_file():
        img = pygame.image.load(str(path)).convert_alpha()
        iw, ih = img.get_size()
        scale = min(max_w / iw, max_h / ih, 1.0)
        nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
        return pygame.transform.smoothscale(img, (nw, nh))
    surf = pygame.Surface((max_w, int(max_h * 0.7)), pygame.SRCALPHA)
    surf.fill((232, 216, 180, 240))
    pygame.draw.rect(surf, (120, 90, 55), surf.get_rect(), 4)
    t = pygame.font.SysFont("georgia", 22).render("Parchment (placeholder)", True, (60, 45, 30))
    surf.blit(t, (surf.get_width() // 2 - t.get_width() // 2, surf.get_height() // 2 - t.get_height() // 2))
    return surf
