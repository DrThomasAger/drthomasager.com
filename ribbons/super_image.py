"""Compose the ten weavings into one labeled review grid."""
from PIL import Image, ImageDraw

SHOTS = r"C:\Users\hanjo\Claude\Projects\DrThomasAger\shots"
NAMES = {
    1: "v1  Mandorla Braid", 2: "v2  Gathered Sheaf",
    3: "v3  Rosette of Rings", 4: "v4  Plaited Lattice",
    5: "v5  Braided Rainbow Arch", 6: "v6  Falling Helix Banners",
    7: "v7  Rivers of Symbols", 8: "v8  Woven Smile",
    9: "v9  Great Rope", 10: "v10  Fountain",
}
FILES = {8: "ribbon-v8b.png", 10: "ribbon-v10w.png"}
CW, CH, LAB = 700, 260, 26
grid = Image.new("RGB", (CW * 2, (CH + LAB) * 5), "#111111")
d = ImageDraw.Draw(grid)
for i in range(1, 11):
    f = FILES.get(i, f"ribbon-v{i}.png")
    im = Image.open(f"{SHOTS}\\{f}").crop((0, 0, 1400, 520)).resize((CW, CH))
    col, row = (i - 1) % 2, (i - 1) // 2
    x, y = col * CW, row * (CH + LAB)
    grid.paste(im, (x, y + LAB))
    d.text((x + 10, y + 6), NAMES[i], fill="#ffe066")
grid.save(f"{SHOTS}\\super-image-weavings.png")
print("saved")
