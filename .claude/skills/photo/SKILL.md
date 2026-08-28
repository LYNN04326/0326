---
name: photo
description: >
  截圖存檔＋標註的**預設做法**：紅框、編號 badge、說明 callout 一律用 HTML 絕對定位疊在
  `<img>` 上方，**不修改原始圖片像素**，因此可隨時調位置、深色模式也讀得清楚。涵蓋「把 Figma／
  瀏覽器截圖存下來、標上紅框與編號、寫成 HackMD 內嵌 HTML 或存進 repo」「多圖點擊流程說明」
  「圖左說明右的步驟卡片」這類任務。觸發時機：使用者要求「截圖標一下」「框起來加編號」
  「做成點擊流程圖」「這段貼到 HackMD」。需要**蓋掉截圖裡既有文字並重寫**、或維護舊格式
  「規格書 UI 截圖標號慣例」時才改用 `png` skill（Pillow 燒進像素，舊版做法）。
---

# 截圖標註（photo，預設做法）

核心原則：**原始截圖永遠保持原樣**，紅框／badge／說明文字全部是疊在圖片上方的 HTML 元素。
好處是標註位置隨時可改（不用重新產圖）、文字用瀏覽器字型渲染（深色模式與高 DPI 都清楚）、
diff 看得出改了什麼。

需要真的**改寫圖片裡的文字**（HTML 疊圖只能蓋在上面、換不掉原字）時，才轉用
`.claude/skills/png/SKILL.md`。兩者分工表見該 skill 結尾。

---

## 規則一：圖片入庫與引用（上傳到 Cloudflare R2 圖床）

HackMD 的 `upload` 端點不可用，圖片一律先上傳到 Cloudflare R2，取回 `public_url` 後在 HTML／
Markdown 裡引用。**不再** commit 進 `.claude/assets/` 或走 `raw.githubusercontent.com`
（舊法棄用，只有 R2 環境變數不可用時當備案）。

需要的環境變數：

| 變數 | 用途 |
| :--- | :--- |
| `R2_ACCOUNT_ID` | Cloudflare 帳號 ID，組出 endpoint |
| `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` | R2 API token |
| `R2_BUCKET` | 目標 bucket |
| `R2_PUBLIC_BASE_URL` | bucket 對外網域，回傳 `public_url` 用 |

boto3 流程（R2 是 S3 相容 API，用 `s3` client 即可）：

```python
import os, mimetypes, boto3

s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
    region_name="auto",
)

def upload(local_path, key):
    ctype = mimetypes.guess_type(local_path)[0] or "image/png"
    s3.upload_file(local_path, os.environ["R2_BUCKET"], key,
                   ExtraArgs={"ContentType": ctype})
    return f"{os.environ['R2_PUBLIC_BASE_URL'].rstrip('/')}/{key}"

public_url = upload("out/step-1.png", "specs/e1/step-1.png")
```

* **key 帶語意路徑**（`{文件}/{章節}/{檔名}.png`），不要用亂數檔名，之後才找得回來。
* 同名覆蓋會直接蓋掉舊圖，改版時要嘛換 key、要嘛確定舊引用可以一起更新。
* **上傳前先 `Read` 看過圖**，別把破圖或半渲染的截圖送上去——上去了就會被別人引用。
* 環境變數缺失時才退回 commit 進 repo，並在回覆中明講用了備案。

---

## 規則二：版面規則（HTML overlay）

所有「截圖＋說明」的版面一律照這套骨架，**輸出成 HackMD 內嵌 HTML 或截圖成 PNG 都一樣**
（`png` skill 的「整段內容輸出成單一 PNG」直接沿用本節）。

1. **白底容器**：外層 `.page` 白底、`max-width` 收斂寬度、`padding` 留白，不要讓內容貼邊。
2. **步驟標題列**：每個步驟一張卡片，卡片頂部是標題列（步驟名稱），下面才是圖與說明。
3. **圖左說明右的 flex**：`display:flex; gap:20px; align-items:flex-start`，圖片欄 `flex:none`
   固定寬、說明欄 `flex:1`。畫面窄時才允許改為上下排。
4. **說明文字 callout**：`font-size:15px; color:#222; line-height:1.65`、**左對齊**。
   不要用置中小字。
5. **紅框＋圓形 badge**：紅框 `border:2px solid #FF3B30`、圓角 `4px`；badge 是紅底白字**圓形**
   （`background:#FF3B30; color:#fff; border-radius:50%; font-weight:700`），貼在紅框左上角。
6. **badge 與 callout 數字呼應**：圖上的 ① 一定對應說明欄的第 1 條，數字是圖文之間唯一的橋樑，
   不可錯位、不可跳號。
7. **紅框／badge 用百分比絕對定位**，父容器必須設 `aspect-ratio:{native_w}/{native_h}`，
   這樣不論顯示寬度怎麼縮放，標註都黏在正確位置。
8. **純圖片（無紅框）也要用外層 `div` 帶 `max-width` 包住**，不能只靠 `<img>` 自己的 inline
   `max-width`——HackMD 會覆寫 `img` 樣式，圖會爆版。這條沒有例外，即使這次輸出的是 PNG 也照寫，
   因為同一段版面程式碼常被 copy 回 HackMD 情境。

### 版面骨架

```html
<div class="page" style="background:#fff; max-width:760px; margin:0 auto; padding:24px;">
  <div style="border:1px solid #e5e5e5; border-radius:8px; overflow:hidden; margin-bottom:20px;">
    <div style="background:#f5f6f8; padding:10px 16px; font-size:15px; font-weight:700; color:#222;">
      步驟 1　進入聯繫人才頁
    </div>
    <div style="display:flex; gap:20px; align-items:flex-start; padding:16px;">
      <!-- 圖片欄：容器扛寬度與 aspect-ratio，紅框/badge 用百分比定位 -->
      <div style="position:relative; width:560px; flex:none; aspect-ratio:1102/860;">
        <img src="https://img.example.com/specs/e1/step-1.png"
             style="display:block; width:100%; height:100%; object-fit:fill;">
        <div style="position:absolute; left:12.4%; top:31.2%; width:38.6%; height:9.1%;
                    border:2px solid #FF3B30; border-radius:4px;"></div>
        <div style="position:absolute; left:9.6%; top:29.0%; width:24px; height:24px;
                    background:#FF3B30; color:#fff; border-radius:50%;
                    font:700 14px/24px Inter,'Noto Sans TC',sans-serif; text-align:center;">1</div>
      </div>
      <!-- 說明欄 -->
      <div style="flex:1; font-size:15px; color:#222; line-height:1.65;">
        <p style="margin:0 0 8px;"><b>1</b>　點「聯繫人才」進入列表，預設帶入最近一次的篩選條件。</p>
        <p style="margin:0;"><b>2</b>　列表為空時顯示空狀態插圖與「立即搜尋人才」按鈕。</p>
      </div>
    </div>
  </div>

  <!-- 純圖片（無紅框）也要有外層容器扛 max-width -->
  <div style="max-width:560px;">
    <img src="https://img.example.com/specs/e1/overview.png" style="display:block; width:100%;">
  </div>
</div>
```

### 輸出成 PNG 時的補充

需要交付 PNG（而不是內嵌 HTML）時，版面照上面組，再用 Playwright 截圖：

* `deviceScaleFactor` **至少 2**（截圖內原始 UI 文字很小就用 3），**絕不用 1**。
* 圖片顯示寬度滿足 `CSS 寬度 × dsf ≥ 原生寬`，否則等於在縮圖。實務：`disp = min(原生寬, 520~620)`。
  但**可讀性優先於像素完美**，小圖用原生寬顯示即可，不要為了整除把圖壓到看不清楚。
* 截圖範圍貼齊最外層容器，不要 `fullPage`：`await (await page.$('.page')).screenshot({path})`。

```js
const page = await browser.newPage({ viewport: {width: 1060, height: 900}, deviceScaleFactor: 2 });
await page.goto('file://' + __dirname + '/page.html');
await page.waitForLoadState('networkidle');
await (await page.$('.page')).screenshot({ path: 'out.png' });
```

---

## 座標怎麼抓

紅框與 badge 的位置要換算成父容器的百分比，來源依下列**優先順序**：

0. **素材是 Figma 來源時，優先用 `mcp__Figma__get_metadata`／`get_design_context` 拿 node 的精確
   bounding box**，再除以父 frame 的寬高換成百分比。這是唯一「精確」的來源——設計稿本來就知道每個
   元件在哪，不需要猜。**不要截圖之後才用像素掃描去猜位置。**
1. 素材是瀏覽器畫面時，用 Playwright `elementHandle.boundingBox()` 取實際座標，同樣換成百分比。
2. **像素顏色掃描（掃描邊框色、找色塊邊界）只是沒有更好資料來源時的退場方案**，例如手上只有一張
   來路不明的 PNG。用了就要 `Read` 出來確認框有沒有對齊。
3. 純手動目測填百分比是最後手段，一定要看過產出再交付。

換算：`left% = (node.x - frame.x) / frame.width * 100`，`top%`、`width%`、`height%` 同理。

---

## PATCH 前跟同文件既有段落並排比對

**產完一定要 `Read` 出來自己看過，而且要跟同一份文件裡既有的區塊比對風格。**

這不是「整頁有沒有明顯錯」（那是有沒有渲染成功的問題），而是要把新產出跟舊區塊的截圖
**並排放在一起看**，逐項核對：

- [ ] 圖片顯示寬度與卡片寬度是同一個量級？
- [ ] 標題列字級、顏色、底色一致？
- [ ] 說明文字是不是同樣的 `15px / #222 / line-height:1.65` 左對齊？
- [ ] 卡片間距、內距一致？
- [ ] badge 大小、顏色、形狀一致？
- [ ] 整體視覺層次（卡片分組→標題→圖文並排）沒有退化成單欄置中？

機械檢查（渲染成功、沒有溢出）**測不出**「比例不對／風格花俏／後面章節比前面退步」這類問題，
只有並排肉眼比對才看得出來。同一份文件內不同章節的視覺風格必須一致——這是實際被使用者打回過的
問題，見 `.claude/skills/png/SKILL.md`〈整段內容輸出成單一 PNG〉的事故記錄。

---

## 多圖點擊流程

「點這裡 → 跳到這頁 → 再點這裡」這種流程說明：

* **一個步驟一張卡片**，卡片依序往下排，不要把多張圖硬塞進同一列。
* 每張圖只標**這一步要點的那一個**紅框，不要把全部步驟的框都畫在第一張圖上。
* 步驟編號連續：卡片標題「步驟 N」、圖上 badge `N`、說明欄第 N 條，三者同號。
* 步驟之間要接續關係時，用卡片之間的向下箭頭（`↓` 文字或 CSS 三角形），**不要用 Pillow 畫箭頭**。
* 截圖裁切到 UI 元件本身邊界，不含周圍空白背景；badge 不可壓在畫面元素上，必要時在元件上緣
  補一條剛好容納 badge 的留白（做法見 `png` skill）。

---

## 深色模式可讀性

HackMD 與多數閱讀器有深色模式，疊圖的文字是 HTML，不是燒進像素，所以要顧到兩種背景：

* 說明文字**不要**寫死 `color:#222` 在**沒有底色的**區塊上——上例的 callout 位於白底卡片內，
  所以安全；若 callout 直接放在文件背景上，改用不指定 `color`（繼承主題色）。
* 卡片、圖片容器一律**明確給白底**，避免深色模式下白色 UI 截圖直接貼在深色背景上、邊界糊掉。
* 紅色 `#FF3B30` 在深淺底都夠對比，badge 白字紅底不用另外處理。
* 這也是 photo 優於 png 的理由之一：燒進像素的文字沒辦法隨主題調整。
