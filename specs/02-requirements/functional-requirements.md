# Functional Requirements

正式功能需求只能記錄已確認內容。

| ID | Title | Actor | 優先級 | 來源 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| FR-001 | 員工申請請假 | 員工 | High | FACT-005, FACT-025 | Confirmed |
| FR-002 | 病假上傳診斷書 | 員工 | High | FACT-026, FACT-027 | Confirmed |
| FR-003 | 主管審核假單 | 主管 | High | FACT-006, FACT-028, FACT-029 | Confirmed |
| FR-004 | 逾期未審核催辦通知 | 系統 | Medium | FACT-030, FACT-031, FACT-032, Q-013, Q-014 | Confirmed |
| FR-005 | 員工撤回待審核假單 | 員工 | High | FACT-033 | Confirmed |
| FR-006 | HR 查看所有請假紀錄 | HR | High | FACT-007 | Confirmed |
| FR-007 | HR 匯出 Excel 報表 | HR | High | FACT-036, FACT-037, FACT-038 | Confirmed |
| FR-008 | 主管指定代理主管 | 主管 | Medium | FACT-039, FACT-040, FACT-041, Q-015 | Confirmed |
| FR-009 | HR 查看代理主管設定 | HR | Medium | FACT-042 | Confirmed |
| FR-010 | 審核結果通知申請人 | 系統 | Medium | Q-016 | Confirmed |

---

## FR-001: 員工申請請假

| Field | Value |
| --- | --- |
| ID | FR-001 |
| Title | 員工申請請假 |
| Description | 員工可透過系統填寫請假申請，包含開始日期、結束日期、假別與原因，送出後進入待審核狀態。系統於送出前檢查假別額度是否足夠，不足時阻擋申請 |
| Actor | 員工（ROLE-001） |
| Trigger | 員工發起請假申請 |
| Preconditions | 員工已登入系統 |
| Source | FACT-005, FACT-025, Q-009 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 員工已登入系統
When 員工填寫開始日期、結束日期、假別、原因並送出申請
Then 系統建立一筆假單，狀態為「待審核」

Given 員工申請的假別剩餘額度不足以涵蓋申請天數
When 員工送出申請
Then 系統阻擋送出並提示額度不足
```

---

## FR-002: 病假上傳診斷書

| Field | Value |
| --- | --- |
| ID | FR-002 |
| Title | 病假上傳診斷書 |
| Description | 員工申請病假時，若天數達 3 天（含）以上，系統要求上傳診斷書；未滿 3 天則不強制 |
| Actor | 員工（ROLE-001） |
| Trigger | 員工申請病假 |
| Preconditions | 假別選擇為病假 |
| Source | FACT-026, FACT-027 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 員工申請病假且天數 >= 3 天
When 員工送出申請
Then 系統要求上傳診斷書，未上傳不得送出

Given 員工申請病假且天數 < 3 天
When 員工送出申請
Then 系統不強制要求上傳診斷書
```

### File Constraints

- 檔案格式：PNG、JPG、PDF
- 檔案大小：單一檔案不超過 5MB

---

## FR-003: 主管審核假單

| Field | Value |
| --- | --- |
| ID | FR-003 |
| Title | 主管審核假單 |
| Description | 主管可對待審核的假單進行同意或拒絕操作，拒絕時必須填寫原因 |
| Actor | 主管（ROLE-002） |
| Trigger | 主管開啟待審核假單 |
| Preconditions | 假單狀態為「待審核」 |
| Source | FACT-006, FACT-028, FACT-029 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 假單狀態為「待審核」
When 主管選擇「同意」
Then 假單狀態變更為「已核准」

Given 假單狀態為「待審核」
When 主管選擇「拒絕」並填寫拒絕原因
Then 假單狀態變更為「已拒絕」且記錄拒絕原因

Given 假單狀態為「待審核」
When 主管選擇「拒絕」但未填寫原因
Then 系統阻擋送出，提示必須填寫拒絕原因
```

---

## FR-004: 逾期未審核催辦通知

| Field | Value |
| --- | --- |
| ID | FR-004 |
| Title | 逾期未審核催辦通知 |
| Description | 假單自申請送出時間起算超過 3 天主管仍未審核時，系統於每天 0 點與 12 點發送 Email 與站內訊息提醒主管 |
| Actor | 系統（自動） |
| Trigger | 假單自送出起超過 3 天未處理 |
| Preconditions | 假單狀態為「待審核」 |
| Source | FACT-030, FACT-031, FACT-032, Q-013, Q-014 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 假單狀態為「待審核」且自申請送出時間起已超過 3 天未處理
When 系統排程於每日 0:00 與 12:00 執行
Then 系統發送 Email 通知給該假單的審核主管
And 系統發送站內訊息給該假單的審核主管

Given 假單狀態為「待審核」且自申請送出時間起未超過 3 天
When 系統排程於每日 0:00 與 12:00 執行
Then 系統不發送催辦通知
```

---

## FR-005: 員工撤回待審核假單

| Field | Value |
| --- | --- |
| ID | FR-005 |
| Title | 員工撤回待審核假單 |
| Description | 員工可撤回自己尚在待審核狀態的假單 |
| Actor | 員工（ROLE-001） |
| Trigger | 員工對自己的待審核假單發起撤回 |
| Preconditions | 假單狀態為「待審核」且為該員工本人的假單 |
| Source | FACT-033 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 假單狀態為「待審核」且屬於該員工
When 員工選擇「撤回」
Then 假單狀態變更為「已撤回」
```

---

## FR-006: HR 查看所有請假紀錄

| Field | Value |
| --- | --- |
| ID | FR-006 |
| Title | HR 查看所有請假紀錄 |
| Description | HR 可在系統中查看全公司所有員工的請假紀錄 |
| Actor | HR（ROLE-003） |
| Trigger | HR 進入請假紀錄頁面 |
| Preconditions | 使用者具有 HR 角色 |
| Source | FACT-007 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 使用者為 HR 角色
When HR 進入請假紀錄頁面
Then 系統顯示全公司所有員工的請假紀錄
```

---

## FR-007: HR 匯出 Excel 報表

| Field | Value |
| --- | --- |
| ID | FR-007 |
| Title | HR 匯出 Excel 報表 |
| Description | HR 可依部門與日期區間篩選後，匯出包含指定欄位的 Excel 格式報表 |
| Actor | HR（ROLE-003） |
| Trigger | HR 設定篩選條件後點擊匯出 |
| Preconditions | 使用者具有 HR 角色 |
| Source | FACT-036, FACT-037, FACT-038 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given HR 設定了部門與日期區間篩選條件
When HR 點擊匯出
Then 系統產生 Excel 檔案
And 檔案包含欄位：員工姓名、部門、假別、開始日期、結束日期、時數、申請日期、審核狀態、審核人

Given HR 未設定任何篩選條件
When HR 點擊匯出
Then 系統匯出全部請假紀錄的 Excel 檔案
```

---

## FR-008: 主管指定代理主管

| Field | Value |
| --- | --- |
| ID | FR-008 |
| Title | 主管指定代理主管 |
| Description | 主管可在系統上指定代理主管並設定代理起訖日期；代理期間內由代理主管行使審核權限，代理審核即為最終結果。未設定代理人時維持原主管審核，系統不自動指派 |
| Actor | 主管（ROLE-002） |
| Trigger | 主管設定代理主管 |
| Preconditions | 使用者具有主管角色 |
| Source | FACT-039, FACT-040, FACT-041, Q-015 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 主管進入代理設定頁面
When 主管指定代理人並填寫代理起訖日期
Then 系統記錄代理設定，在代理期間內假單自動指派給代理主管審核

Given 主管未設定代理人
When 有新假單送出
Then 假單維持由原主管審核，系統不自動指派其他人

Given 代理主管已審核某假單
When 原主管回歸
Then 該假單不需原主管再次確認，代理審核為最終結果
```

---

## FR-009: HR 查看代理主管設定

| Field | Value |
| --- | --- |
| ID | FR-009 |
| Title | HR 查看代理主管設定 |
| Description | HR 可在後台查看目前所有主管的代理人設定狀態 |
| Actor | HR（ROLE-003） |
| Trigger | HR 進入代理主管管理頁面 |
| Preconditions | 使用者具有 HR 角色 |
| Source | FACT-042 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 使用者為 HR 角色
When HR 進入代理主管管理頁面
Then 系統顯示所有主管的代理人設定，包含代理人姓名與代理起訖日期
```

---

## FR-010: 審核結果通知申請人

| Field | Value |
| --- | --- |
| ID | FR-010 |
| Title | 審核結果通知申請人 |
| Description | 假單被核准或拒絕後，系統透過 Email 與站內訊息通知申請人 |
| Actor | 系統（自動） |
| Trigger | 假單狀態由「待審核」變更為「已核准」或「已拒絕」 |
| Preconditions | 假單審核完成 |
| Source | Q-016 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 假單狀態由「待審核」變更為「已核准」
When 狀態變更完成
Then 系統發送 Email 通知給申請人，告知假單已核准
And 系統發送站內訊息給申請人，告知假單已核准

Given 假單狀態由「待審核」變更為「已拒絕」
When 狀態變更完成
Then 系統發送 Email 通知給申請人，告知假單已拒絕及拒絕原因
And 系統發送站內訊息給申請人，告知假單已拒絕及拒絕原因
```
