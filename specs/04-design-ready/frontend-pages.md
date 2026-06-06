# Frontend Pages

| Page ID | 頁面名稱 | 主要角色 | 目的 | 關聯需求 |
| --- | --- | --- | --- | --- |
| PAGE-001 | 登入頁 | 全部 | 透過 HR API 驗證登入 | NFR-004, BR-030 |
| PAGE-002 | 員工儀表板 | 員工 | 顯示假別額度摘要與近期假單 | BR-025, FR-001 |
| PAGE-003 | 申請請假 | 員工 | 填寫並送出請假申請 | FR-001, FR-002, BR-014~016, BR-021~025 |
| PAGE-004 | 我的假單 | 員工 | 查看自己的假單列表與狀態 | FR-001, FR-005 |
| PAGE-005 | 假單詳情 | 員工/主管/HR | 查看單筆假單完整資訊 | FR-001, FR-003 |
| PAGE-006 | 待審核假單 | 主管/代理主管 | 列表顯示待審核假單，可同意/拒絕 | FR-003, BR-017, BR-028 |
| PAGE-007 | 代理主管設定 | 主管 | 設定/修改/移除代理主管 | FR-008, DR-006, BR-020 |
| PAGE-008 | HR 請假紀錄 | HR | 查看全公司請假紀錄 + 匯出 | FR-006, FR-007, DR-004, DR-005 |
| PAGE-009 | HR 代理主管總覽 | HR | 查看所有代理主管設定 | FR-009, PR-008 |
| PAGE-010 | 通知中心 | 全部 | 站內訊息列表與已讀標記 | FR-004, FR-010 |

---

## PAGE-001: 登入頁

- Route: /login
- Main Actions: 輸入帳號密碼 → 送出登入
- Required Data: 無（登入前）
- Permission Rules: 公開頁面
- Related Requirements: NFR-004, BR-030

### UI Elements

- 帳號輸入框
- 密碼輸入框
- 登入按鈕
- 錯誤訊息區（驗證失敗 / HR API 不可用）

---

## PAGE-002: 員工儀表板

- Route: /dashboard
- Main Actions: 查看額度摘要、快速申請請假、查看近期假單
- Required Data: 假別額度（API-009）、近期假單（API-005）、未讀通知數量（API-019）
- Permission Rules: 登入使用者皆可存取
- Related Requirements: BR-025, FR-001

### UI Elements

- 假別額度卡片（特休/病假/事假各顯示：總額、已用、預扣、可用）
- 近期假單列表（最近 5 筆，含狀態標籤）
- 「申請請假」快捷按鈕
- 通知鈴鐺（顯示未讀數量）

---

## PAGE-003: 申請請假

- Route: /leave-requests/new
- Main Actions: 選擇假別 → 填寫日期/原因 → 上傳附件（條件） → 送出
- Required Data: 假別列表、額度（API-009）
- Permission Rules: 員工角色
- Related Requirements: FR-001, FR-002, BR-014~016, BR-021~025, BR-033, BR-034

### UI Elements

- 假別選擇器（特休/病假/事假/喪假）
- 開始日期選擇器
- 結束日期選擇器
- 自動計算工作日天數與時數（排除週末，BR-024）
- 原因文字區
- 額度提示（顯示目前可用額度）
- 診斷書上傳區（病假 ≥ 3 天時顯示為必填，< 3 天顯示為選填）
  - 格式提示：PNG / JPG / PDF，≤ 5MB
- 喪假：親等關係選擇器 + 親人過世日期（僅喪假時顯示）
  - 100 天期限提示
- 送出按鈕
- 錯誤訊息區（額度不足 / 最低 30 分鐘 / 無工作日 / 無主管）

---

## PAGE-004: 我的假單

- Route: /leave-requests
- Main Actions: 查看假單列表、撤回待審核假單
- Required Data: 假單列表（API-005）
- Permission Rules: 員工角色（僅看自己的）
- Related Requirements: FR-001, FR-005

### UI Elements

- 假單列表表格（假別、日期、天數、狀態、審核人、操作）
- 狀態篩選標籤（全部/待審核/已核准/已拒絕/已撤回）
- 「撤回」按鈕（僅待審核假單顯示）
- 撤回確認彈窗

---

## PAGE-005: 假單詳情

- Route: /leave-requests/:id
- Main Actions: 查看假單資訊、附件、審核結果
- Required Data: 假單詳情（API-006）
- Permission Rules: 申請人本人 / 審核主管 / HR
- Related Requirements: FR-001, FR-003

### UI Elements

- 假單基本資訊（假別、日期、天數、時數、原因、狀態）
- 附件下載區（若有）
- 審核資訊（審核人、審核時間、拒絕原因）
- 主管/代理主管：同意/拒絕按鈕（僅待審核狀態）

---

## PAGE-006: 待審核假單

- Route: /approvals
- Main Actions: 查看待審核假單列表、同意或拒絕
- Required Data: 待審核假單（API-010）
- Permission Rules: 主管或代理主管（BR-028 並行）
- Related Requirements: FR-003, BR-017, BR-028

### UI Elements

- 待審核假單列表（申請人、假別、日期、天數、申請時間）
- 逾期標記（> 3 天未處理）
- 「同意」按鈕
- 「拒絕」按鈕 → 彈出拒絕原因輸入框（必填）
- 批次操作（可選）

---

## PAGE-007: 代理主管設定

- Route: /acting-manager
- Main Actions: 新增/修改/移除代理主管設定
- Required Data: 當前代理設定（API-013）、可選代理人列表
- Permission Rules: 主管角色
- Related Requirements: FR-008, DR-006, BR-020

### UI Elements

- 當前代理設定顯示（代理人、起訖日期）
- 代理人選擇器
- 起始日期選擇器
- 結束日期選擇器
- 儲存/移除按鈕

---

## PAGE-008: HR 請假紀錄

- Route: /hr/leave-records
- Main Actions: 查看全公司紀錄、篩選、匯出 Excel
- Required Data: 全公司假單（API-016）
- Permission Rules: HR 角色
- Related Requirements: FR-006, FR-007, DR-004, DR-005

### UI Elements

- 篩選列：部門下拉選單 + 日期區間選擇器
- 假單列表表格（員工姓名、部門、假別、開始日期、結束日期、時數、申請日期、審核狀態、審核人）
- 「匯出 Excel」按鈕（API-017）
- 分頁控制

---

## PAGE-009: HR 代理主管總覽

- Route: /hr/acting-managers
- Main Actions: 查看所有主管的代理設定
- Required Data: 全部代理設定（API-018）
- Permission Rules: HR 角色
- Related Requirements: FR-009, PR-008

### UI Elements

- 代理設定列表（主管姓名、代理人姓名、起始日期、結束日期、狀態）
- 狀態標籤（生效中/未生效/已過期）

---

## PAGE-010: 通知中心

- Route: /notifications
- Main Actions: 查看站內訊息、標記已讀
- Required Data: 訊息列表（API-019）
- Permission Rules: 登入使用者皆可存取
- Related Requirements: FR-004, FR-010

### UI Elements

- 訊息列表（類型圖示、標題、時間、已讀狀態）
- 未讀/全部篩選
- 點擊可跳轉至相關假單詳情
- 「標記已讀」按鈕
