# Contributing Guide

Thank you for your interest in this project! This document describes the folder structure, naming conventions, and contribution guidelines to keep the codebase consistent.

---

## Table of Contents

- [Environment Requirements](#environment-requirements)
- [Folder Structure](#folder-structure)
- [Naming Conventions](#naming-conventions)
- [Contribution Workflow](#contribution-workflow)
- [Coding Style](#coding-style)
- [Commit Messages](#commit-messages)

---

## Environment Requirements

- Python >= 3.10
- pygame >= 2.x
- pip or virtualenv

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
python src/main.py
```

---

## Folder Structure

```
project-root/
│
├── assets/                  # Static game resources
│   ├── images/              # Sprites, backgrounds, icons (PNG/JPG)
│   ├── sounds/              # Sound effects (WAV/OGG)
│   ├── music/               # Background music (MP3/OGG)
│   └── fonts/               # Font files (.ttf / .otf)
│
├── components/              # Reusable UI components
│   ├── button.py            # Button component
│   ├── label.py             # Static text component
│   ├── healthbar.py         # Health / energy bar
│   ├── panel.py             # UI panel / background box
│   └── __init__.py
│
├── scenes/                  # Game screens / states
│   ├── base_scene.py        # Abstract base class for all scenes
│   ├── menu_scene.py        # Main menu screen
│   ├── game_scene.py        # Main gameplay screen
│   ├── pause_scene.py       # Pause screen
│   ├── gameover_scene.py    # Game over screen
│   └── __init__.py
│
├── entities/                # Game objects with state and behavior
│   ├── base_entity.py       # Abstract base class for all entities
│   ├── player.py            # Player character
│   ├── enemy.py             # Enemy characters
│   ├── projectile.py        # Bullets / projectiles
│   └── __init__.py
│
├── systems/                 # Game logic systems
│   ├── collision.py         # Collision detection and resolution
│   ├── physics.py           # Gravity, velocity, acceleration
│   ├── input_handler.py     # Keyboard / mouse input handling
│   ├── camera.py            # Camera / viewport following
│   └── __init__.py
│
├── utils/                   # Shared utilities across the project
│   ├── constants.py         # Constants (FPS, colors, screen size...)
│   ├── config.py            # Read / write config files
│   ├── helpers.py           # Miscellaneous helper functions
│   ├── asset_loader.py      # Load and cache images, sounds
│   └── __init__.py
│
├── data/                    # Config data, level definitions, save files
│   ├── levels/              # JSON / TMX files defining each level
│   ├── settings.json        # User settings (volume, resolution...)
│   └── savegame.json        # Game progress save file
│
├── tests/                   # Unit and integration tests
│   ├── test_entities.py
│   ├── test_systems.py
│   ├── test_components.py
│   └── __init__.py
│
├── src/
│   └── main.py              # Single entry point — initializes and runs the game
│
├── requirements.txt         # Project dependencies
├── README.md                # Project overview
└── CONTRIBUTING.md          # This document
```

### Folder Responsibilities

| Folder | Responsibility |
|---|---|
| `assets/` | All static resources — no logic code |
| `components/` | Reusable UI elements — no game logic |
| `scenes/` | Manages game flow; each scene is a self-contained screen |
| `entities/` | Objects with a lifecycle: init, update, draw, destroy |
| `systems/` | Pure logic, decoupled from specific entities |
| `utils/` | Shared functions and constants — no side effects |
| `data/` | External data that can change without touching code |
| `tests/` | Isolated tests — do not import `src/main.py` |
| `src/` | Contains only `main.py` — initializes pygame and runs the game loop |

---

## Naming Conventions

| Target | Convention | Example |
|---|---|---|
| Files / folders | `snake_case` | `game_scene.py`, `asset_loader.py` |
| Classes | `PascalCase` | `GameScene`, `PlayerEntity` |
| Functions / variables | `snake_case` | `load_image()`, `player_speed` |
| Constants | `UPPER_SNAKE_CASE` | `SCREEN_WIDTH`, `MAX_FPS` |
| Asset files | `snake_case` + description | `player_idle.png`, `jump_sfx.wav` |

---

## Contribution Workflow

### 1. Fork and create a new branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/description-of-bug
```

### 2. Write code and tests

- Each class/module should have **a single responsibility**
- Add tests to `tests/` when introducing new logic
- Do not commit `.pyc`, `__pycache__`, or save game files

### 3. Verify before pushing

```bash
python -m pytest tests/
python src/main.py          # manual smoke test
```

### 4. Open a Pull Request

- Clearly describe **what changed** and **why**
- Reference any related issue (e.g., `Closes #12`)
- Include screenshots if the change affects the UI

---

## Coding Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Keep each file under **300 lines** — split into modules if longer
- Prefer clarity over brevity
- Add docstrings to all public classes and functions:

```python
def load_image(path: str, scale: float = 1.0) -> pygame.Surface:
    """
    Load an image from the given path and scale it by the given factor.

    Args:
        path: Relative path from the assets/images/ directory.
        scale: Scale factor to resize the image (default 1.0).

    Returns:
        A processed pygame.Surface object.
    """
```

---

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
<type>(<scope>): <short description>
```

| Type | When to use |
|---|---|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug |
| `refactor` | Restructuring code without changing behavior |
| `assets` | Adding or updating assets (images, sounds) |
| `docs` | Updating documentation |
| `test` | Adding or modifying tests |
| `chore` | Miscellaneous tasks (deps update, config...) |

**Examples:**

```
feat(scenes): add pause screen with resume and quit buttons
fix(collision): fix player clipping through platform at high fall speed
assets(sounds): add item pickup sound effect
```
