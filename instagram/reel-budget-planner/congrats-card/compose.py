import sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter

base_src, mask_src, content_src, out = sys.argv[1:5]
OW, OH = 941, 1672
W, H = 1080, 1920
sx, sy = W / OW, H / OH

# --- 1. grain in the inpainted area so it matches the photo texture
orig = np.array(Image.open(base_src).convert("RGB")).astype(np.float32)
m = np.array(Image.open(mask_src).convert("L").filter(ImageFilter.GaussianBlur(6))).astype(np.float32)[..., None] / 255
rng = np.random.default_rng(7)
noise = rng.normal(0, 4.5, orig.shape[:2])[..., None]
orig = np.clip(orig + noise * m, 0, 255).astype(np.uint8)
src = Image.fromarray(orig)

# --- 2. which pixels belong to the card (not the man's head in front of it)
Q = [(24, 198), (536, 262), (547, 952), (28, 992)]  # outer card corners (orig px)
a = np.array(src).astype(int)
L = a.mean(2); sat = a.max(2) - a.min(2)
cardlike = (L > 215) & (sat < 40)

def right_edge(y):  # quad's right edge x at row y
    (x1, y1), (x2, y2) = Q[1], Q[2]
    return x1 + (x2 - x1) * (y - y1) / (y2 - y1)

bound = np.full(OH, 0.0)
for y in range(190, 1000):
    lim = int(right_edge(y))
    bound[y] = lim
    if y >= 760:
        continue
    # scan left->right: card ends where a long run of non-card pixels starts (the head)
    for x in range(468, lim):
        if not cardlike[y, x:x + 8].any():
            bound[y] = x
            break
# smooth the head outline (wide median ignores small badges/lines on the card)
k = 30
pad = np.pad(bound, k, mode="edge")
bound = np.array([np.median(pad[i:i + 2 * k + 1]) for i in range(OH)])
# step-1 badge sits right against the hair: bridge over it; keep the top corner straight
bound[395:475] = np.linspace(bound[394], bound[475], 80)
bound[:290] = np.maximum(bound[:290], bound[290])
bound[:760] -= 2
np.save("bound.npy", bound)

# --- 3. white fill mask (inset from the glowing border, rounded corners), at final scale
SS = 4
def inset(q, d):
    c = np.mean(q, 0)
    return [tuple(c + (np.array(p) - c) * (1 - d / np.linalg.norm(np.array(p) - c))) for p in q]
fill = Image.new("L", (W * SS, H * SS), 0)
dq = [(x * sx * SS, y * sy * SS) for x, y in inset(Q, 12)]
ImageDraw.Draw(fill).polygon(dq, fill=255)
# round the corners by eroding+dilating
f = np.array(fill)
r = 16 * SS
kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
f = cv2.dilate(cv2.erode(f, kern), kern)
fill = Image.fromarray(f).resize((W, H), Image.LANCZOS)

person = Image.new("L", (W, H), 255)
pd = ImageDraw.Draw(person)
for y in range(H):
    yo = min(OH - 1, int(y / sy))
    pd.line([(bound[yo] * sx, y), (W, y)], fill=0)
person = person.filter(ImageFilter.GaussianBlur(2))
mask = np.minimum(np.array(fill), np.array(person)).astype(np.float32)[..., None] / 255

big = np.array(src.resize((W, H), Image.LANCZOS)).astype(np.float32)
white = np.array([254, 253, 250], np.float32)
# soft top-left light falloff like the original card
yy, xx = np.mgrid[0:H, 0:W]
shade = 1 - 0.025 * np.clip((xx + yy - 300) / 1500, 0, 1)
card = white * shade[..., None]
outimg = big * (1 - mask) + card * mask

# --- 4. warp content onto the card plane
c = np.array(Image.open(content_src).convert("RGBA")).astype(np.float32)
ch, cw = c.shape[:2]
dst = np.float32([(x * sx, y * sy) for x, y in Q])
srcq = np.float32([(0, 0), (cw, 0), (cw, ch), (0, ch)])
M = cv2.getPerspectiveTransform(srcq, dst)
warp = cv2.warpPerspective(c, M, (W, H), flags=cv2.INTER_AREA, borderValue=(0, 0, 0, 0))
al = warp[..., 3:4] / 255 * mask
outimg = outimg * (1 - al) + warp[..., :3] * al
Image.fromarray(np.clip(outimg, 0, 255).astype(np.uint8)).save(out, optimize=True)
print(out)
