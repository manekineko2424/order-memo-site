"""
フレーム画像のスクリーン境界を自動測定するスクリプト。
透明スクリーン型のデバイスフレーム画像（iPhone 17 Pro 等）に使用。

使い方:
    python3 measure_frame.py assets/iphone17pro.png

出力:
    layout.scss / default.html に必要な数値一覧
"""

import sys
from PIL import Image


def find_screen_bounds(pixels, w, h):
    """
    フレームの内側（透明スクリーン領域）の境界を検出する。
    外側の透明パディングは無視し、「不透明フレーム→透明スクリーン」の境界を返す。
    """
    mid_y = h // 2
    mid_x = w // 2

    # --- 左端: 外側透明を飛ばして不透明フレームに入り、次に透明になる点 ---
    screen_left = None
    in_frame = False
    for x in range(w):
        a = pixels[x, mid_y][3]
        if not in_frame and a > 128:
            in_frame = True
        elif in_frame and a < 128:
            screen_left = x
            break

    # --- 右端: 右から同様 ---
    screen_right = None
    in_frame = False
    for x in range(w - 1, -1, -1):
        a = pixels[x, mid_y][3]
        if not in_frame and a > 128:
            in_frame = True
        elif in_frame and a < 128:
            screen_right = x
            break

    # --- 上端: 外側透明→不透明フレーム→透明スクリーン ---
    screen_top = None
    in_frame = False
    for y in range(h):
        a = pixels[mid_x, y][3]
        if not in_frame and a > 128:
            in_frame = True
        elif in_frame and a < 128:
            screen_top = y
            break

    # --- 下端: 下から同様 ---
    screen_bottom = None
    in_frame = False
    for y in range(h - 1, -1, -1):
        a = pixels[mid_x, y][3]
        if not in_frame and a > 128:
            in_frame = True
        elif in_frame and a < 128:
            screen_bottom = y
            break

    return screen_left, screen_right, screen_top, screen_bottom


def measure(path: str, display_width: int = 400) -> None:
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    pixels = img.load()
    scale = display_width / w

    print(f"\n画像サイズ: {w}x{h} px  →  表示幅 {display_width}px (scale={scale:.4f})\n")

    screen_left, screen_right, screen_top, screen_bottom = find_screen_bounds(pixels, w, h)

    if any(v is None for v in [screen_left, screen_right, screen_top, screen_bottom]):
        print("❌ 境界の検出に失敗しました。スクリーン部分が透明な画像か確認してください。")
        return

    screen_w = screen_right - screen_left + 1
    screen_h = screen_bottom - screen_top + 1

    # --- 表示サイズ換算 ---
    d_left    = round(screen_left * scale)
    d_top     = round(screen_top  * scale)
    d_width   = round(screen_w    * scale)
    d_height  = round(screen_h    * scale)
    d_frame_h = round(h           * scale)

    # --- clip-path rx / ry（角丸はスクリーン幅の約10.9%） ---
    corner_px = round(d_width * 0.109)
    rx = round(corner_px / d_width,  3)
    ry = round(corner_px / d_height, 3)

    print("=" * 50)
    print(f"  スクリーン左端   : {screen_left}px  → {d_left}px")
    print(f"  スクリーン上端   : {screen_top}px  → {d_top}px")
    print(f"  スクリーン幅     : {screen_w}px  → {d_width}px")
    print(f"  スクリーン高さ   : {screen_h}px  → {d_height}px")
    print(f"  フレーム全高     : {h}px  → {d_frame_h}px")
    print("=" * 50)

    print("\n▼ _sass/layout.scss に記入する値:\n")
    print(f"  .iphonePreview  {{ width: {display_width}px; height: {d_frame_h}px; }}")
    print(f"  .iphoneFrame    {{ width: {display_width}px; }}")
    print(f"  .iphoneScreen   {{ top: {d_top}px; left: {d_left}px; width: {d_width}px; }}")
    print(f"  .videoContainer {{ top: {d_top}px; left: {d_left}px; width: {d_width}px; height: {d_height}px; }}")

    print("\n▼ _layouts/default.html の clipPath に記入する値:\n")
    print(f"  <rect x=\"0\" y=\"0\" width=\"1\" height=\"1\" rx=\"{rx}\" ry=\"{ry}\"/>")

    print("\n▼ レスポンシブ用 (370px / 260px):\n")
    for dw in [370, 260]:
        s = dw / w
        print(f"  [{dw}px] top={round(screen_top*s)}px  left={round(screen_left*s)}px  "
              f"width={round(screen_w*s)}px  height={round(screen_h*s)}px  "
              f"frame-h={round(h*s)}px")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python3 measure_frame.py <フレーム画像パス> [表示幅px(省略時400)]")
        sys.exit(1)
    image_path = sys.argv[1]
    display_w = int(sys.argv[2]) if len(sys.argv) >= 3 else 400
    measure(image_path, display_w)
