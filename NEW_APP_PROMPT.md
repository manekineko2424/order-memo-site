# 新アプリLPサイト作成 — AI指示書

Claude Code や Codex に新しいLPを作らせるときに使うプロンプトテンプレートです。
**このファイルを直接編集して Claude Code に貼り付けてください。**

---

## どのフォルダで Claude Code を起動するか

**必ず `/Users/manekineko/dev/lp/` （親フォルダ）で開いてください。**

```
/Users/manekineko/dev/lp/          ← ここで Claude Code を起動
├── automatic-app-landing-page-master/   ← テンプレ（AIが参照）
├── slot-count-web/                      ← 参考実装（AIが参照）
└── [新アプリ名]-web/                    ← AIがここに新規作成する
```

| 開き方 | 結果 |
|--------|------|
| `/dev/lp/` で開く ✅ | テンプレ参照 & 新フォルダを正しい場所に作れる |
| `automatic-app-landing-page-master/` で開く ❌ | 新フォルダがテンプレの中に作られてしまう |
| 新アプリフォルダで開く ❌ | フォルダがまだ存在しない・テンプレが見えない |

**Claude Code の起動方法:**
```bash
cd /Users/manekineko/dev/lp
claude  # または code . でVS Code + Claude Code拡張
```

---

## STEP 1: 事前に用意するもの（人間タスク）

Claude Code を起動する前に以下を準備してください。

| 項目 | 確認場所 | メモ欄 |
|------|---------|--------|
| iOS App ID（数字） | App Store Connect → アプリ情報 → Apple ID | |
| アプリのキャッチコピー | 自分で考える（1行） | |
| 機能リスト（3〜5個） | 自分で考える | |
| テーマカラー（HEX） | アプリのアクセントカラーを調べる | |
| GitHub リポジトリ名 | 例: `{アプリ名}-web` | |
| スクリーンショット | 撮影してファイル名を確認（`#` は使わない） | |

スクリーンショットは事前に以下に置いておく:
```
/Users/manekineko/dev/lp/automatic-app-landing-page-master/assets/screenshot/
```

---

## STEP 2: Claude Code に貼り付けるプロンプト

**2つのモードがあります。iOSアプリのソースがある場合は「自動検出モード」が楽です。**

---

### モードA: ソースから自動検出（推奨）

iOSアプリのソースコードパスを渡すと、テーマカラーや機能をAIが自動で読み取ります。

```
/Users/manekineko/dev/lp/automatic-app-landing-page-master のテンプレートを使って、
以下のアプリのLPサイトを作成してください。

【iOSアプリのソースコード】
/Users/manekineko/dev/ios/[アプリフォルダ名]

上記ソースを読んで以下を自動で判断してください:
- テーマカラー（.tint / Color 定義から）
- 主な機能（UIの構造・コメント・画面名から）
- アプリ名（.xcodeproj / Info.plist から）

【固定情報】
- iOS App ID: [App Store Connect の数字]
- GitHub リポジトリ: manekineko2424/[リポジトリ名（例: my-app-web）]

【スクリーンショット】
/Users/manekineko/dev/lp/automatic-app-landing-page-master/assets/screenshot/
に以下のファイルを配置済み:
- [ファイル名1.png]
- [ファイル名2.png]（任意）

【実行してほしい手順】
1. テンプレートを /Users/manekineko/dev/lp/[リポジトリ名]/ にコピー
   （automatic-app-landing-page-master は変更しない）
2. git init して remote を https://github.com/manekineko2424/[リポジトリ名].git に設定
3. ソースを読んで _config.yml を設定する
   - ios_app_id / ios_app_country: jp / app_description（キャッチコピー）
   - device_color: iphone17pro
   - link_color 等をテーマカラーに設定
   - feature_icons_background_color はテーマカラーの薄色版
   - your_link を https://manekineko2424.github.io/[リポジトリ名]/ に設定
4. _pages/privacypolicy.md の [アプリ名] と [制定日] を置換する
5. _pages/changelog.md をアプリの機能リストで更新する
6. スクリーンショットを assets/screenshot/ にコピーする
7. git add -A && git commit -m "Initial LP setup for [アプリ名]" && git push -u origin main
```

---

### モードB: 手動入力

ソースがない・情報を自分で指定したい場合はこちら。

```
/Users/manekineko/dev/lp/automatic-app-landing-page-master のテンプレートを使って、
以下のアプリのLPサイトを作成してください。

【アプリ情報】
- アプリ名: [アプリ名（日本語可）]
- iOS App ID: [App Store Connect の数字 例: 1234567890]
- キャッチコピー: [1行のアプリ説明]
- テーマカラー(HEX): [例: #FF9500]
- GitHub リポジトリ: manekineko2424/[リポジトリ名（例: my-app-web）]

【機能リスト】（3〜5個）
1. タイトル: [機能名] / 説明: [機能の説明文] / FontAwesomeアイコン: [アイコン名（例: lock）]
2. タイトル: [機能名] / 説明: [機能の説明文] / FontAwesomeアイコン: [アイコン名]
3. タイトル: [機能名] / 説明: [機能の説明文] / FontAwesomeアイコン: [アイコン名]
4. タイトル: [機能名] / 説明: [機能の説明文] / FontAwesomeアイコン: [アイコン名]
5. タイトル: [機能名] / 説明: [機能の説明文] / FontAwesomeアイコン: [アイコン名]

【スクリーンショット】
/Users/manekineko/dev/lp/automatic-app-landing-page-master/assets/screenshot/
に以下のファイルを配置済み:
- [ファイル名1.png]
- [ファイル名2.png]（任意）

【実行してほしい手順】
1. テンプレートを /Users/manekineko/dev/lp/[リポジトリ名]/ にコピーする
   （automatic-app-landing-page-master は変更しない）
2. git init して remote を https://github.com/manekineko2424/[リポジトリ名].git に設定
3. _config.yml を上記情報で設定する
   - ios_app_id / ios_app_country: jp / app_description
   - device_color: iphone17pro
   - link_color / feature_icons_foreground_color 等をテーマカラーに変更
   - feature_icons_background_color はテーマカラーの薄色版（透明度20%程度）
   - your_link を https://manekineko2424.github.io/[リポジトリ名]/ に設定
4. _pages/privacypolicy.md の [アプリ名] と [制定日] を置換する
5. _pages/changelog.md をアプリの機能リストで更新する
6. スクリーンショットを assets/screenshot/ にコピーする
7. git add -A && git commit -m "Initial LP setup for [アプリ名]" && git push -u origin main
```

---

## STEP 3: よくある追加指示

LP作成後に使える追加プロンプト例です。

### サポートページを追加したい
```
slot-count-web のサポートページを参考に、[アプリ名] 用の
support/index.html と privacy/index.html と style.css を作成してください。
よくある質問は以下の通りです:
- Q: [質問1] → A: [回答1]
- Q: [質問2] → A: [回答2]
お問い合わせフォームURL: [Google フォームURL]
```

### スクリーンショットが表示されない
```
LP のスクリーンショットが表示されていません。
assets/screenshot/ のファイル名に問題がないか確認して修正してください。
（ファイル名に # が含まれているとURLが壊れます）
```

### デバイスフレームを変えたい
```
measure_frame.py を使って [フレーム画像パス] を測定し、
_sass/layout.scss と _config.yml の device_color を更新してください。
```

### Apple ID を修正したい
```
Apple ID が間違っていました。正しい値は [正しい数字] です。
_config.yml の ios_app_id を修正して push してください。
```

### アップデート履歴を追加したい
```
_pages/changelog.md に以下のバージョンを追加してください。
バージョン: [x.x]
新機能: [機能1], [機能2]
バグ修正: [修正内容]
```

---

## STEP 4: 完成後の確認チェックリスト

- [ ] GitHub リポジトリの Settings → Pages → Source を `main` ブランチに設定
- [ ] 公開URL `https://manekineko2424.github.io/[リポジトリ名]/` にアクセスできる
- [ ] iPhone モックアップにスクリーンショットが表示されている
- [ ] App Store アイコン・アプリ名・価格が自動取得されている（数分かかる場合あり）
- [ ] 「アップデート履歴」ページが開ける
- [ ] フッターに Twitter リンクが表示されている

---

## 参考情報

| ファイル | 役割 |
|---------|------|
| `HOW_TO_USE.md` | 手動でLPを作る場合の詳細手順 |
| `measure_frame.py` | カスタムデバイスフレームのスクリーン座標を測定するツール |
| `assets/iphone17pro.png` | デフォルトのデバイスフレーム画像 |
| `slot-count-web/` | 実際に作ったLPの参考実装（小役カウンター） |

**FontAwesome アイコン一覧:** https://fontawesome.com/v5/icons  
（v5 の名前を使用。例: `lock`, `star`, `chart-bar`, `mobile`, `bell`）
