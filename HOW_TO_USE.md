# テンプレート使い方ガイド

このフォルダ（`automatic-app-landing-page-master/`）はJekyll製のアプリLPテンプレートです。
**このフォルダ自体は編集しない。** 新アプリのたびにコピーして使い回します。

---

## フォルダ構成ルール

```
dev/lp/
├── automatic-app-landing-page-master/   ← テンプレ（触らない）
│   ├── HOW_TO_USE.md                    ← このファイル
│   └── assets/screenshot/
│       └── yourscreenshot.png           ← プレースホルダー（触らない）
│
├── slot-count-web/                      ← 小役カウンター用（GitHub: manekineko2424/slot-count-web）
├── next-app-web/                        ← 次のアプリ用（命名例）
└── ...
```

**命名規則:** `{アプリ名}-web/`（GitHub リポジトリ名と揃える）

---

## 新アプリのLP作成手順

### Step 1: テンプレをコピー

```bash
cp -r automatic-app-landing-page-master/ {アプリ名}-web/
cd {アプリ名}-web/
```

### Step 2: git 初期化 & リモート設定

```bash
git init
git remote add origin https://github.com/manekineko2424/{アプリ名}-web.git
```

### Step 3: `_config.yml` を編集

最低限必要な設定:

| キー | 内容 | 取得場所 |
|------|------|---------|
| `ios_app_id` | App Store の数字ID | App Store Connect → アプリ情報 → Apple ID |
| `ios_app_country` | `jp`（日本） | 固定 |
| `app_description` | アプリのキャッチコピー | 自分で書く |
| `your_name` | 開発者名 | `Takuya Oku` |
| `email_address` | 連絡先メール | `okidoki.app.dev@gmail.com` |
| `twitter_username` | Twitter ID（@なし） | `pochi_slot_post` |
| `your_link` | LP の公開URL | `https://manekineko2424.github.io/{アプリ名}-web/` |

### Step 4: スクリーンショットを配置

```
assets/screenshot/screenshot1.png   ← メイン画面
assets/screenshot/screenshot2.png   ← サブ画面（任意）
```

**注意:**
- ファイル名に `#` を使わない（URLが壊れる）
- 英数字・ハイフン・アンダースコアのみ使用
- 解像度: 828×1792 または 1125×2436（縦向きPNG）
- 複数置くと最後の1枚が表示される（スライドショーにはならない）

### Step 5: 各ページを更新

- `_pages/privacypolicy.md` — アプリ用のプライバシーポリシー（日本語）
- `_pages/changelog.md` — バージョン履歴

### Step 6: サポートページが必要な場合

App Store Connect の「サポートURL」欄に使える独立HTMLページを追加:

```bash
# slot-count-web の例を参考にコピーして内容を書き換える
cp -r ../slot-count-web/support/ support/
cp -r ../slot-count-web/privacy/ privacy/
cp ../slot-count-web/style.css style.css
```

### Step 7: ローカル確認（任意）

```bash
bundle install
bundle exec jekyll serve
# http://localhost:4000 で確認
```

### Step 8: GitHub へ push

```bash
git add -A
git commit -m "Initial LP setup for {アプリ名}"
git push -u origin main
```

GitHub リポジトリの **Settings → Pages → Source: main ブランチ** を有効化すれば公開される。

---

## テーマカラー設定のポイント

アプリのメインカラーに合わせて以下を変える:

```yaml
link_color                            : "#FF9500"   # アクセントカラー（オレンジ等）
feature_icons_foreground_color        : "#FF9500"
feature_icons_background_color        : "#FFF3E0"   # アクセントの薄色版
social_icons_foreground_color         : "#FF9500"
social_icons_background_color         : "#FFF3E0"
```

デバイスモックアップの色（標準）:
```yaml
device_color : white   # white / black / blue / yellow / coral
```

---

## カスタムデバイスフレームを使う場合（iPhone 17 Pro 等）

標準の `white.png` 等は**スクリーン部分が不透明**（背景画像 + 前面スクショ方式）。  
`iphone17pro.png` のような**スクリーン部分が透明**なフレーム画像は、フレームを前面オーバーレイとして配置する方式に変更が必要。

### 透明スクリーン型フレームの追加手順

**1. フレーム画像を `assets/` に配置**
```bash
cp "iPhone 17 Pro Silver.png" assets/iphone17pro.png
```

**2. `_config.yml` を更新**
```yaml
device_color : iphone17pro
```

**3. `_layouts/default.html` を変更**

SVG clip-path を rounded-rect に簡略化し、`<img class="iphoneFrame">` を追加:

```html
<div class="iphonePreview">
    <!-- rounded-rect clip-path（rx/ry は スクリーン幅・高さに対する角丸の比率） -->
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 0" style="position: absolute;">
        <clipPath id="screenMask" clipPathUnits="objectBoundingBox">
            <rect x="0" y="0" width="1" height="1" rx="0.109" ry="0.050"/>
        </clipPath>
    </svg>

    <div class="videoContainer hidden">...</div>
    <img class="iphoneScreen hidden" src="" alt="">
    {% include screencontent.html %}

    <!-- フレームを最前面に重ねる -->
    <img class="iphoneFrame" src="{{ site.github.baseurl }}/assets/{{ site.device_color }}.png" alt="">
</div>
```

**4. `_sass/layout.scss` を変更**

`.iphonePreview` の `background-image` を削除し、absolute 配置に切り替え:

```scss
.iphonePreview {
    grid-area: p;
    position: relative;
    width: 400px;
    height: {フレーム高さ}px;   // 画像高さ × (400/画像幅)
    margin-top: 68px;
}
.iphoneFrame {
    position: absolute;
    top: 0; left: 0;
    width: 400px;
    z-index: 10;
    pointer-events: none;
}
.iphoneScreen {
    position: absolute;
    top: {スクリーン上端}px;
    left: {スクリーン左端}px;
    width: {スクリーン幅}px;
    clip-path: url(#screenMask);
    z-index: 1;
}
```

### iPhone 17 Pro Silver（440×916 px）の実測値

| 項目 | 元画像(px) | 400px表示時 | 370px表示時 | 260px表示時 |
|------|-----------|------------|------------|------------|
| スクリーン左端 | 19 | 17px | 16px | 11px |
| スクリーン上端 | 21 | 19px | 18px | 12px |
| スクリーン幅 | 402 | 365px | 338px | 237px |
| スクリーン高さ | 873 | 794px | 735px | 516px |
| フレーム全高 | 916 | 833px | 770px | 541px |
| clip rx / ry | — | 0.109 / 0.050 | 同左 | 同左 |

> 新しいフレーム画像を使う場合は Python で測定:
> ```python
> from PIL import Image
> img = Image.open("frame.png").convert("RGBA"); pixels = img.load()
> w, h = img.size; mid_y = h // 2
> # 左端: 最初の透明ピクセルのx座標
> for x in range(w):
>     if pixels[x, mid_y][3] == 0: print(f"screen_left={x}"); break
> ```

---

## 適用済みアプリ一覧

| アプリ名 | フォルダ | GitHub リポジトリ | 公開URL | デバイス |
|---------|---------|-----------------|---------|---------|
| 小役カウンター ロック画面 | `slot-count-web/` | `manekineko2424/slot-count-web` | https://manekineko2424.github.io/slot-count-web/ | iPhone 17 Pro Silver（透明スクリーン型） |
