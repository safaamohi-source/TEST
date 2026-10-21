import sys
import numpy as np, torch, cv2
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
W, H = im.size
mask = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(mask)
# white + orange caption boxes
d.polygon([(112, 1092), (836, 1028), (846, 1182), (896, 1180), (902, 1392), (84, 1428), (68, 1234), (118, 1232)], fill=255)
d.polygon([(340, 1440), (728, 1404), (730, 1376), (340, 1410)], fill=255)  # underline swoosh
d.rectangle((14, 1102, 138, 1232), fill=255)   # left burst strokes
d.rectangle((852, 1150, 932, 1258), fill=255)  # right burst strokes
m = cv2.dilate(np.array(mask), np.ones((25, 25), np.uint8))
Image.fromarray(m).save(out.replace(".png", "_mask.png"))

model = torch.jit.load("models/big-lama.pt", map_location="cpu").eval()
img = np.array(im).astype(np.float32) / 255
ph, pw = (8 - H % 8) % 8, (8 - W % 8) % 8
img_p = np.pad(img, ((0, ph), (0, pw), (0, 0)), mode="symmetric")
m_p = np.pad((m > 0).astype(np.float32), ((0, ph), (0, pw)), mode="symmetric")
with torch.no_grad():
    r = model(torch.from_numpy(img_p).permute(2, 0, 1)[None], torch.from_numpy(m_p)[None, None])
res = np.clip(r[0].permute(1, 2, 0).numpy() * 255, 0, 255).astype(np.uint8)[:H, :W]
# keep original pixels outside the mask
keep = (m == 0)[..., None]
Image.fromarray(np.where(keep, np.array(im), res)).save(out)
print(out)
