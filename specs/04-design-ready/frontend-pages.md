# Frontend Pages

> ⚠️ 系統平台（Web / Mobile）尚未確認（ASM-001 Pending）。本文件以路由與功能描述為主，不指定 UI 框架。

| Page ID | 頁面名稱 | 主要角色 | 目的 | 關聯需求 |
| --- | --- | --- | --- | --- |
| PAGE-001 | 請假申請表單 | 員工 | 提交請假申請 | FR-001 |
| PAGE-002 | 我的請假紀錄 | 員工 | 查看與取消自己的申請 | FR-001, FR-007 |
| PAGE-003 | 待審核申請清單 | 主管 / 代理主管 | 查看與審核管轄員工申請 | FR-002 |
| PAGE-004 | 申請審核詳情 | 主管 / 代理主管 | 查看申請細節並執行審核 | FR-002 |
| PAGE-005 | 代理主管設定 | 主管 | 指定代理人及代理期間 | FR-006 |
| PAGE-006 | HR 請假紀錄總覽 | HR | 查看所有員工紀錄 | FR-004 |
| PAGE-007 | HR 報表匯出 | HR | 匯出 Excel 報表 | FR-005 |
| PAGE-008 | 員工資料管理 | HR | 建立與維護員工資料 | PR-003, DR-001 |
| PAGE-009 | 通知中心 | 所有角色 | 查看系統通知（含催辦訊息） | FR-003 |

---

## PAGE-001：請假申請表單

- **Route**：/leave/apply
- **Role**：員工（ROLE-001）
- **Related Requirements**：FR-001, BR-002~005, DEC-011, DEC-019, DEC-020

**表單欄位**

| 欄位 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| 假別 | Select | Yes | 特休 / 病假 / 事假 / 喪假 |
| 親等 | Select | 條件 | 僅喪假顯示：tier1 / tier2 / tier3（BR-004） |
| 開始日期時間 | Datetime picker | Yes | 精度半小時（DEC-011） |
| 結束日期時間 | Datetime picker | Yes | 精度半小時（DEC-011） |
| 預計時數 | 唯讀計算 | — | 系統依工作日自動計算（DEC-020） |
| 請假原因 | Textarea | Yes | — |
| 代理人 | Employee select | Yes | 從員工清單選取（DEC-019） |
| 診斷書上傳 | File upload | 條件 | 病假 > 24h 時必填（BR-005） |

**Page Actions**
- 提交：呼叫 API-001；驗證配額、代理人、診斷書
- 即時顯示剩餘配額（呼叫 API-012）

---

## PAGE-002：我的請假紀錄

- **Route**：/leave/my-records
- **Role**：員工（ROLE-001）
- **Related Requirements**：FR-001, FR-007, PR-001

**顯示欄位**：假別、開始/結束時間、時數、狀態、申請日期、拒絕原因（若已拒絕）

**Page Actions**
- 取消：僅狀態為「待審核」的申請可操作；確認對話框後呼叫 API-003

---

## PAGE-003：待審核申請清單

- **Route**：/manager/approvals
- **Role**：主管（ROLE-002）/ 代理主管（ROLE-004，代理期間內）
- **Related Requirements**：FR-002, BR-008, BR-009

**顯示欄位**：員工姓名、假別、開始/結束時間、時數、申請日期、等待天數

**Page Actions**
- 點入申請：導向 PAGE-004
- 標示超過 3 天未審核（BR-007）

---

## PAGE-004：申請審核詳情

- **Route**：/manager/approvals/{id}
- **Role**：主管（ROLE-002）/ 代理主管（ROLE-004）
- **Related Requirements**：FR-002, BR-006

**顯示欄位**：完整申請資訊、員工資料、代理人、診斷書連結（若有）

**Page Actions**
- 核准：呼叫 API-004
- 拒絕：彈出輸入框填寫原因（必填，BR-006），呼叫 API-005

---

## PAGE-005：代理主管設定

- **Route**：/manager/acting
- **Role**：主管（ROLE-002）
- **Related Requirements**：FR-006, WR-005, WR-006, BR-009

**顯示欄位**：目前代理記錄（代理人姓名、期間）

**Page Actions**
- 新增代理：選擇代理人（員工清單）+ 設定期間；呼叫 API-006
- 移除代理：呼叫 API-007

---

## PAGE-006：HR 請假紀錄總覽

- **Route**：/hr/records
- **Role**：HR（ROLE-003）
- **Related Requirements**：FR-004, PR-003

**顯示欄位**：員工姓名、部門、假別、開始/結束時間、時數、狀態、申請日期

**Page Actions**
- 篩選（篩選條件 Q-017 Pending）
- 導向 PAGE-007 匯出

---

## PAGE-007：HR 報表匯出

- **Route**：/hr/export
- **Role**：HR（ROLE-003）
- **Related Requirements**：FR-005, DR-006

**Page Actions**
- 設定篩選條件（Q-017 Pending，欄位待確認）
- 匯出 Excel：呼叫 API-009，下載 .xlsx 檔案

---

## PAGE-008：員工資料管理

- **Route**：/hr/employees
- **Role**：HR（ROLE-003）
- **Related Requirements**：PR-003, DR-001, DEC-010

**顯示欄位**：員工姓名、部門、主管、到職日

**Page Actions**
- 新增員工：呼叫 API-010；`manager_id` 為空時員工申請將自動核准（BR-010）
- 編輯員工：呼叫 API-011

---

## PAGE-009：通知中心

- **Route**：/notifications
- **Role**：所有角色
- **Related Requirements**：FR-003, BR-007

**顯示內容**：系統通知列表（含催辦訊息）、已讀 / 未讀標示

**Page Actions**
- 標記已讀
- 點擊催辦訊息導向 PAGE-003 / PAGE-004
