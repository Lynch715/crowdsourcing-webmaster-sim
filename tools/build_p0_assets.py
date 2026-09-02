#!/usr/bin/env python3
"""Normalize all generated art masters to the exact delivery sizes."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path(
    "/Users/ruis/.codex/generated_images/"
    "01a060a4-23ba-7dc0-92f0-7be9e9a88a3f"
)

ASSETS = {
    "char/char_boss_smug.png": (
        "exec-c90eae22-c34e-4df2-9828-7a5577dfd2a2.png",
        (1024, 1536),
        True,
    ),
    "char/char_boss_anxious.png": (
        "exec-b21b7d85-1135-47c8-8780-174151ec1612.png",
        (1024, 1536),
        True,
    ),
    "char/char_boss_ruined.png": (
        "exec-7ec380be-fb55-44a7-b1fc-37104ff60b68.png",
        (1024, 1536),
        True,
    ),
    "char/char_rider_a.png": (
        "exec-a8655496-35c5-477c-abe3-d270b1569a77.png",
        (1024, 1536),
        True,
    ),
    "char/char_rider_b.png": (
        "exec-8c3025b4-ac67-4e43-9130-505be53efe5e.png",
        (1024, 1536),
        True,
    ),
    "char/char_rider_c.png": (
        "exec-06aba171-99c3-45f3-bb62-028e55c70640.png",
        (1024, 1536),
        True,
    ),
    "char/char_brother.png": (
        "exec-d90044f4-1f36-4f26-a6f4-eb5bfb0f2a4b.png",
        (1024, 1536),
        True,
    ),
    "char/char_brother_wheelchair.png": (
        "exec-a4f35147-3991-481a-a666-fe45149b57fc.png",
        (1024, 1536),
        True,
    ),
    "char/char_son.png": (
        "exec-339aa20f-da31-4262-8ecc-d66aa1bbf4bf.png",
        (1024, 1536),
        True,
    ),
    "char/char_mother.png": (
        "exec-89310466-1663-44a9-ab3e-222a5af218ab.png",
        (1024, 1536),
        True,
    ),
    "char/char_police.png": (
        "exec-0b33343c-8395-4349-ba28-b047dca14ca6.png",
        (1024, 1536),
        True,
    ),
    "char/char_kbro.png": (
        "exec-77d37826-c372-4ced-89e7-4e6e7492db4b.png",
        (1024, 1536),
        True,
    ),
    "ui/ui_btn_primary.png": (
        "exec-fe0ea58c-466a-4f9f-b192-fc233858f307.png",
        (512, 160),
        True,
    ),
    "ui/ui_btn_primary_pressed.png": (
        "exec-3958fb63-38d5-49ea-8887-0a533bd896c9.png",
        (512, 160),
        True,
    ),
    "ui/ui_btn_danger.png": (
        "exec-d02ab14e-452f-4bd4-b4e5-f9a7392a48f7.png",
        (512, 160),
        True,
    ),
    "ui/ui_btn_danger_pressed.png": (
        "exec-857030d0-d6ca-447b-95cc-91e8e5ba6970.png",
        (512, 160),
        True,
    ),
    "ui/ui_panel.png": (
        "exec-e3e7fc85-1508-4fc5-a241-a1db4d1fe342.png",
        (1024, 768),
        True,
    ),
    "ui/ui_card.png": (
        "exec-bc0b69fc-2dc7-4366-982d-594828435b62.png",
        (800, 1100),
        True,
    ),
    "ui/icon_money.png": (
        "exec-6cd705d7-85a3-44d7-a2de-4301326ecb13.png",
        (256, 256),
        True,
    ),
    "ui/icon_anger.png": (
        "exec-46ba5007-86a6-4a78-9b5f-ffb8c87fcdab.png",
        (256, 256),
        True,
    ),
    "ui/icon_risk.png": (
        "exec-d8fad066-27b3-47a3-bf85-fa21f6aa9679.png",
        (256, 256),
        True,
    ),
    "ui/icon_family.png": (
        "exec-ec78ffb2-b647-498e-8118-8bc207bf1126.png",
        (256, 256),
        True,
    ),
    "ui/icon_squeeze.png": (
        "exec-da151970-fe7e-4e7a-98b3-db7170fe7060.png",
        (256, 256),
        True,
    ),
    "ui/logo_title.png": (
        "exec-f32ff92e-e56d-4071-ab6a-8d67796b5d89.png",
        (1600, 600),
        False,
    ),
    "bg/bg_station_day.png": (
        "exec-8fb8c3c1-d8e4-42c6-9d4d-e538057f109b.png",
        (1920, 1080),
        False,
    ),
    "bg/bg_station_night.png": (
        "exec-3cba5b08-4cf8-4716-a56d-2991e69f1c5a.png",
        (1920, 1080),
        False,
    ),
    "bg/bg_street_rain.png": (
        "exec-0f32a1e5-ef76-44ad-a8ed-51c11fd27f6e.png",
        (1920, 1080),
        False,
    ),
    "bg/bg_hospital.png": (
        "exec-bd2a33e1-d8c6-48f7-a44f-242bd993886b.png",
        (1920, 1080),
        False,
    ),
    "bg/bg_court.png": (
        "exec-bace3597-b949-410e-986f-b837c00218df.png",
        (1920, 1080),
        False,
    ),
    "bg/bg_cell.png": (
        "exec-2ebe658a-96e5-49da-885a-59cce4d1c760.png",
        (1920, 1080),
        False,
    ),
    "event/ev_crash_scene.png": (
        "exec-c7c35645-8cfe-4cc7-9819-cdf1fdc1e77c.png",
        (1280, 720),
        False,
    ),
    "event/ev_truck_aftermath.png": (
        "exec-8e114349-6392-4c31-8fd8-2ae2da97e8f3.png",
        (1280, 720),
        False,
    ),
    "event/ev_arrest.png": (
        "exec-21a6a64b-ae71-4aba-b28b-75bb1ac5f000.png",
        (1280, 720),
        False,
    ),
    "event/ev_gaokao.png": (
        "exec-21efcdd4-c476-4f0a-a400-580d72123e98.png",
        (1280, 720),
        False,
    ),
    "event/ev_strike.png": (
        "exec-a77ad844-beba-4d70-b7b7-ffd3dc37358f.png",
        (1280, 720),
        False,
    ),
    "event/ev_money.png": (
        "exec-7903de7c-8d78-4b1e-8f36-d32d874390b1.png",
        (1280, 720),
        False,
    ),
}


def normalize(source: Path, target: Path, size: tuple[int, int], alpha: bool) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    with Image.open(source) as image:
        mode = "RGBA" if alpha else "RGB"
        normalized = image.convert(mode).resize(size, Image.Resampling.LANCZOS)
        if alpha:
            alpha_band = normalized.getchannel("A")
            low, high = alpha_band.getextrema()
            if low == high == 255:
                raise ValueError(f"Expected real transparency in {source.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        normalized.save(target, format="PNG", optimize=True)


def checker_tile(size: tuple[int, int]) -> Image.Image:
    tile = Image.new("RGB", size, "#1b222b")
    draw = ImageDraw.Draw(tile)
    step = 24
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2 == 0:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill="#27313d")
    return tile


def contact_sheet(
    paths: list[Path],
    output_name: str,
    title: str,
    columns: int,
    cell_size: tuple[int, int],
) -> None:
    margin = 36
    title_height = 82
    rows = (len(paths) + columns - 1) // columns
    canvas_size = (
        margin * 2 + columns * cell_size[0],
        title_height + margin + rows * cell_size[1],
    )
    canvas = Image.new("RGB", canvas_size, "#10151b")
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.load_default(size=34)
    label_font = ImageFont.load_default(size=18)
    draw.text((margin, 24), title, fill="#ffc300", font=title_font)

    for index, path in enumerate(paths):
        column = index % columns
        row = index // columns
        x = margin + column * cell_size[0]
        y = title_height + row * cell_size[1]
        image_area = (cell_size[0] - 24, cell_size[1] - 54)
        with Image.open(path) as source:
            item = source.convert("RGBA")
            item.thumbnail(image_area, Image.Resampling.LANCZOS)
            tile = checker_tile(image_area)
            tile.paste(
                item,
                ((image_area[0] - item.width) // 2, (image_area[1] - item.height) // 2),
                item,
            )
        canvas.paste(tile, (x, y))
        draw.text((x, y + image_area[1] + 8), path.name, fill="#e7edf4", font=label_font)

    canvas.save(ROOT / "assets" / output_name, quality=90, optimize=True)


def make_full_previews() -> None:
    character_names = [
        "char_boss_smug.png",
        "char_boss_anxious.png",
        "char_boss_ruined.png",
        "char_rider_a.png",
        "char_rider_b.png",
        "char_rider_c.png",
        "char_brother.png",
        "char_brother_wheelchair.png",
        "char_son.png",
        "char_mother.png",
        "char_police.png",
        "char_kbro.png",
    ]
    scene_names = [
        "bg/bg_station_day.png",
        "bg/bg_station_night.png",
        "bg/bg_street_rain.png",
        "bg/bg_hospital.png",
        "bg/bg_court.png",
        "bg/bg_cell.png",
        "event/ev_crash_scene.png",
        "event/ev_truck_aftermath.png",
        "event/ev_arrest.png",
        "event/ev_gaokao.png",
        "event/ev_strike.png",
        "event/ev_money.png",
    ]
    ui_names = [
        "ui_btn_primary.png",
        "ui_btn_primary_pressed.png",
        "ui_btn_danger.png",
        "ui_btn_danger_pressed.png",
        "ui_panel.png",
        "ui_card.png",
        "icon_money.png",
        "icon_anger.png",
        "icon_risk.png",
        "icon_family.png",
        "icon_squeeze.png",
        "logo_title.png",
    ]

    contact_sheet(
        [ROOT / "assets/char" / name for name in character_names],
        "PREVIEW_CHARACTERS.jpg",
        "Characters - 12 assets",
        6,
        (300, 520),
    )
    contact_sheet(
        [ROOT / "assets" / name for name in scene_names],
        "PREVIEW_SCENES_EVENTS.jpg",
        "Backgrounds and Events - 12 assets",
        3,
        (600, 390),
    )
    contact_sheet(
        [ROOT / "assets/ui" / name for name in ui_names],
        "PREVIEW_UI.jpg",
        "UI - 12 assets",
        4,
        (450, 390),
    )


def make_preview() -> None:
    canvas = Image.new("RGB", (1920, 1450), "#10151b")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=22)
    title_font = ImageFont.load_default(size=36)
    draw.text((48, 30), "Crowdsource Station Simulator - P0 Art Batch", fill="#ffc300", font=title_font)

    char_names = [
        "char_boss_smug.png",
        "char_boss_anxious.png",
        "char_boss_ruined.png",
        "char_rider_a.png",
    ]
    for index, name in enumerate(char_names):
        target_box = (330, 495)
        tile = checker_tile(target_box)
        with Image.open(ROOT / "assets/char" / name) as image:
            figure = image.convert("RGBA")
            figure.thumbnail(target_box, Image.Resampling.LANCZOS)
            tile.paste(figure, ((target_box[0] - figure.width) // 2, 0), figure)
        x = 48 + index * 450
        y = 100
        canvas.paste(tile, (x, y))
        draw.text((x, y + 505), name, fill="#e7edf4", font=font)

    with Image.open(ROOT / "assets/bg/bg_station_day.png") as image:
        background = image.convert("RGB")
        background.thumbnail((860, 484), Image.Resampling.LANCZOS)
        canvas.paste(background, (48, 665))
    draw.text((48, 1160), "bg_station_day.png", fill="#e7edf4", font=font)

    with Image.open(ROOT / "assets/ui/ui_panel.png") as image:
        panel = image.convert("RGBA")
        panel.thumbnail((430, 323), Image.Resampling.LANCZOS)
        tile = checker_tile(panel.size)
        tile.paste(panel, (0, 0), panel)
        canvas.paste(tile, (960, 665))
    draw.text((960, 998), "ui_panel.png", fill="#e7edf4", font=font)

    with Image.open(ROOT / "assets/ui/ui_card.png") as image:
        card = image.convert("RGBA")
        card.thumbnail((260, 358), Image.Resampling.LANCZOS)
        tile = checker_tile(card.size)
        tile.paste(card, (0, 0), card)
        canvas.paste(tile, (1460, 665))
    draw.text((1460, 1034), "ui_card.png", fill="#e7edf4", font=font)

    button_names = [
        "ui_btn_primary.png",
        "ui_btn_primary_pressed.png",
        "ui_btn_danger.png",
        "ui_btn_danger_pressed.png",
    ]
    for index, name in enumerate(button_names):
        with Image.open(ROOT / "assets/ui" / name) as image:
            button = image.convert("RGBA")
            button.thumbnail((360, 113), Image.Resampling.LANCZOS)
            tile = checker_tile(button.size)
            tile.paste(button, (0, 0), button)
        x = 960 + (index % 2) * 450
        y = 1080 + (index // 2) * 155
        canvas.paste(tile, (x, y))
        draw.text((x, y + 118), name, fill="#e7edf4", font=font)

    canvas.save(ROOT / "assets/P0_PREVIEW.jpg", quality=90, optimize=True)


def main() -> None:
    for relative, (source_name, size, alpha) in ASSETS.items():
        normalize(GENERATED / source_name, ROOT / "assets" / relative, size, alpha)
    make_preview()
    make_full_previews()
    print(f"Built {len(ASSETS)} assets and four preview sheets")


if __name__ == "__main__":
    main()
