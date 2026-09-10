# ChangeType 語意與規則

## Vocabulary
| ChangeType | 意義 | 對 CodeNo 的影響 | 耦合風險 |
|---|---|---|---|
| add | 新增項目/中類 | 新碼 | 無（除非碰撞既有碼） |
| edit | 既有列內容更新 | 不變 | 無 |
| rename | 改名（CodeNameA 或 CodeNameB） | 不變 | 無（純顯示） |
| move | 重複對中保留的早碼，名稱不變 | 不變 | 來源碼資料需遷入 |
| move_edit | 保留的早碼，且需改名 | 不變 | 同上 |
| delete | 移除（重複對中晚碼，或淘汰） | 移除 | 引用需先遷移 |

**輸出/公告時：RENAME 一律當成 EDIT 呈現。** 比對 ChangeType 一律不分大小寫。
Export 套用後會把所有 ChangeType 重設為 `UnChange`（代表「已完成」，不是「沒變動」）。

## 代碼耦合分析 (coupling)
- **add**：新碼與既有碼零碰撞 → 無耦合。插入前用 `compare.py collide` 確認。
- **rename / edit**：CodeNo 不變，履歷/職缺引用仍有效 → 無資料耦合（純顯示層）。
- **合併/重複 (merge/dup)**：來源碼被併入目標碼，所有指向來源碼的既有履歷/職缺
  必須先 `UPDATE … SET code=目標 WHERE code=來源` 遷移，再停用來源碼（勿先硬刪，
  避免孤兒引用）。這才是真正耦合。**問題碼數 < 10 視為低耦合，可直接產檔。**

## 重複對 → delete / move / move_edit (需求表用語，非 merge)
對每組重複（來源/目標兩碼）：
- 後方（較晚新增、CodeNo 較大）→ **delete**；`New_CodeNo` 填保留碼。
- 前方（較早、CodeNo 較小）→ 保留：
  - 名稱已正確 → **move**
  - 名稱需修正（含縮寫/錯字/別名）→ **move_edit**，更新 CodeNameA + 四語名稱欄。
- 保留(move/move_edit)列：`Old_CodeNo = 消失(被刪)代碼`，`New_CodeNo = 目標(自身)代碼`。
- 被動到的列底色標**橘色 FFC000**。

### 已驗證的 5 組 Certify 範例（實作參考）
| 保留碼(早) | ChangeType | 刪除碼(晚) |
|---|---|---|
| 180537 MySQL-Core | move_edit（MySQL- Core→MySQL-Core） | 180601 |
| 180518 AZ-900 Azure雲端基礎認證 | move | 180540 |
| 180535 Microsoft Office Specialist (Formerly MOUS) | move | 180701 |
| 180536 MOS Master Instructor (Formerly MOUS MI) | move | 180702 |
| 183901 Dell Certified Storage Networking Professional | move_edit（DCSNP→全名） | 183902 |

三種合併型態：重複登錄（同名差空格）/ 通用名↔考試代碼（Azure↔AZ-900）/
縮寫↔全名或舊名↔新名（MOUS↔MOS, DCSNP↔全名）。全部可上網查證屬實再執行。

## 代碼重用 (code reuse) — 高風險耦合點
舊碼被刪/搬走後，其 CodeNo 被指派給**完全不同**的新項目（CodeNo 保留、項目換掉）。
偵測：某 add 項目的 CodeNo == 某 delete/move 列的 CodeNo。上線前舊資料必須先遷移，
否則更新後既有履歷會指到不相干技能（例：1255 jQuery→Win32）。逐筆列出舊碼→新碼→
重用後新項目給 RD。

## delete list 能否重新放回 Completed
某代碼可重新插入的條件：Completed 內**無同名**項目（避免重複）且原 CodeNo 未被
不同項目佔用。名稱比對需正規化（去括號、半/全形、大小寫）。已在 Completed 有同名
者不可重放（應指向既有碼）。
