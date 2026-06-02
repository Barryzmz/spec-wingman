# Data Requirements

正式資料需求只能記錄已確認內容。

---

## DR-001

| Field | Value |
| --- | --- |
| ID | DR-001 |
| Title | 員工基本資料 |
| Description | 系統需要記錄每位員工的基本資訊以支援請假申請與審核流程 |
| Required Fields | 員工姓名、所屬部門（主要）、對應主管 |
| Constraints | 每位員工有且僅有一個主要部門（ASM-003）；由 HR 負責建立與維護 |
| Source | FACT-001, DEC-005, DEC-010, ASM-003, SRC-001 |
| Status | Confirmed |

---

## DR-002

| Field | Value |
| --- | --- |
| ID | DR-002 |
| Title | 請假申請單資料 |
| Description | 每筆請假申請所需記錄的欄位 |
| Required Fields | 申請 ID、員工 ID、假別、開始日期時間、結束日期時間（精度半小時）、時數（工作時數，排除週末與國定假日）、原因、代理人 ID（必填）、申請日期、狀態、診斷書（條件性必填） |
| Constraints | 時間精度為半小時（DEC-011）；時數計算排除週末與國定假日（DEC-020）；代理人為必填（DEC-019）；假別為病假且時數 > 24 小時時，診斷書為必填（BR-005） |
| Source | FACT-013, FACT-014, DEC-003, DEC-011, DEC-019, DEC-020, SRC-001 |
| Status | Confirmed |

---

## DR-003

| Field | Value |
| --- | --- |
| ID | DR-003 |
| Title | 假別參考資料 |
| Description | 系統支援的假別清單 |
| Values | 特休、病假、事假、喪假 |
| Source | FACT-008, SRC-001 |
| Status | Confirmed |

---

## DR-004

| Field | Value |
| --- | --- |
| ID | DR-004 |
| Title | 員工假期配額資料 |
| Description | 記錄每位員工每種假別的年度配額、已使用天數與剩餘天數 |
| Required Fields | 員工 ID、假別、年度、總配額（小時）、已使用（小時）、剩餘（小時） |
| Constraints | 特休依年資計算，從到職日起算（BR-001）；病假上限 240 小時/年（BR-002）；事假上限 112 小時/年（BR-003）；喪假依親等（BR-004） |
| Source | FACT-009, FACT-010, FACT-011, FACT-012, DEC-001, SRC-001 |
| Status | Confirmed |

---

## DR-005

| Field | Value |
| --- | --- |
| ID | DR-005 |
| Title | 代理主管記錄資料 |
| Description | 記錄主管與代理人的指定關係及代理期間 |
| Required Fields | 原主管 ID、代理人 ID、代理開始日期、代理結束日期 |
| Source | DEC-006, SRC-001 |
| Status | Confirmed |

---

## DR-006

| Field | Value |
| --- | --- |
| ID | DR-006 |
| Title | 報表匯出欄位規格 |
| Description | HR 匯出 Excel 報表時所包含的欄位 |
| Required Fields | 員工姓名、部門、假別、開始日期、結束日期、天數、狀態、申請日期 |
| Format | Excel |
| Filter | 可篩選後匯出，具體篩選條件待確認（見 Q-017） |
| Source | DEC-007, DEC-017, SRC-001 |
| Status | Confirmed（篩選條件 Pending） |

---

## DR-007

| Field | Value |
| --- | --- |
| ID | DR-007 |
| Title | 國定假日曆 |
| Description | 系統計算請假時數時，需排除國定假日與週末，因此需要維護一份假日清單 |
| Required Fields | 日期、假日名稱、類型（國定假日 / 週末） |
| Constraints | 時數計算邏輯依賴此資料（DEC-020）；需每年更新 |
| Source | DEC-020 |
| Status | Confirmed |
