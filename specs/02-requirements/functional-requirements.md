# Functional Requirements

正式功能需求只能記錄已確認內容。

---

## FR-001

| Field | Value |
| --- | --- |
| ID | FR-001 |
| Title | 員工提交請假申請 |
| Description | 員工在系統中填寫請假資訊並提交，申請單進入待審核狀態。時間精度為半小時；時數計算排除週末與國定假日；申請時須指定代理人 |
| Actor | 員工（ROLE-001） |
| Trigger | 員工欲申請請假 |
| Preconditions | 員工已登入系統 |
| Source | FACT-013, DEC-003, DEC-011, DEC-013, DEC-019, DEC-020, SRC-001 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 員工已登入系統
When 員工填寫開始日期時間、結束日期時間（精度半小時）、假別、原因、代理人後提交
Then 系統依工作日計算實際時數（排除週末與國定假日），建立請假申請單，狀態設為「待審核」
```

```gherkin
Given 員工未選擇代理人
When 員工提交申請
Then 系統阻止提交並提示代理人為必填
```

```gherkin
Given 員工申請的時數超過該假別的剩餘配額
When 員工提交申請
Then 系統阻止提交並顯示剩餘配額不足的提示
```

```gherkin
Given 假別為病假，且請假時數大於 24 小時
When 員工提交申請
Then 系統要求上傳診斷書，未上傳時阻止提交並顯示提示
```

```gherkin
Given 假別為病假，且請假時數小於或等於 24 小時
When 員工提交申請
Then 診斷書欄位為選填，員工可不上傳即成功提交
```

---

## FR-002

| Field | Value |
| --- | --- |
| ID | FR-002 |
| Title | 主管審核請假申請 |
| Description | 主管查看所轄員工的待審核申請，執行核准或填寫原因後拒絕 |
| Actor | 主管（ROLE-002）或代理主管（ROLE-004） |
| Trigger | 主管轄下員工有待審核的請假申請 |
| Preconditions | 申請單狀態為「待審核」；申請員工屬於主管管轄範圍 |
| Source | FACT-015, FACT-016, DEC-005, DEC-006, SRC-001 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 主管查看待審核申請單
When 主管選擇核准
Then 申請單狀態更新為「已核准」
```

```gherkin
Given 主管查看待審核申請單
When 主管填寫拒絕原因後選擇拒絕
Then 申請單狀態更新為「已拒絕」，拒絕原因記錄於申請單
```

```gherkin
Given 主管選擇拒絕但未填寫原因
When 主管提交審核結果
Then 系統阻止提交並提示必須填寫拒絕原因
```

---

## FR-003

| Field | Value |
| --- | --- |
| ID | FR-003 |
| Title | 系統發送催辦通知給主管 |
| Description | 當請假申請提交後超過 3 天主管未回應，系統每日中午自動發送催辦通知，直到主管完成審核 |
| Actor | 系統（自動觸發） |
| Trigger | 申請單已處於待審核狀態超過 3 天，且主管尚未核准或拒絕 |
| Preconditions | 申請單狀態為「待審核」 |
| Source | FACT-017, DEC-004, DEC-008, SRC-001 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 請假申請單已待審核超過 3 天且主管未回應
When 每日中午 12:00
Then 系統同時發送系統內通知與 Email 給負責審核的主管
```

```gherkin
Given 催辦通知已發送，申請單仍處於待審核狀態
When 下一日中午 12:00
Then 系統繼續發送催辦通知
```

```gherkin
Given 申請單已被主管核准或拒絕
When 系統到達下一個催辦時間點
Then 系統不再發送催辦通知
```

---

## FR-004

| Field | Value |
| --- | --- |
| ID | FR-004 |
| Title | HR 查看所有員工請假紀錄 |
| Description | HR 可在系統中查閱所有員工的請假紀錄 |
| Actor | HR（ROLE-003） |
| Trigger | HR 欲查閱請假紀錄 |
| Preconditions | HR 已登入系統 |
| Source | FACT-006, SRC-001 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given HR 已登入系統
When HR 進入請假紀錄頁面
Then 系統顯示所有員工的請假紀錄
```

---

## FR-005

| Field | Value |
| --- | --- |
| ID | FR-005 |
| Title | HR 匯出請假報表 |
| Description | HR 可將請假紀錄匯出為 Excel 格式報表 |
| Actor | HR（ROLE-003） |
| Trigger | HR 欲匯出報表 |
| Preconditions | HR 已登入系統 |
| Source | FACT-007, DEC-007, SRC-001 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given HR 已登入系統
When HR 執行匯出報表
Then 系統產生 Excel 檔案，包含以下欄位：員工姓名、部門、假別、開始日期、結束日期、天數、狀態、申請日期
```

---

## FR-006

| Field | Value |
| --- | --- |
| ID | FR-006 |
| Title | 主管指定代理人 |
| Description | 主管在系統中指定代理人及代理期間，代理人在期間內擁有與主管相同的審核權限 |
| Actor | 主管（ROLE-002） |
| Trigger | 主管即將無法親自審核（如出差或請假） |
| Preconditions | 主管已登入系統 |
| Source | DEC-006, SRC-001 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 主管已登入系統
When 主管指定代理人並設定代理開始日期與結束日期
Then 代理人在代理期間內可對原主管管轄員工的申請執行核准或拒絕
```

```gherkin
Given 代理期間已結束
When 代理人嘗試執行審核動作
Then 系統拒絕操作，代理人審核權限已失效
```

---

## FR-007

| Field | Value |
| --- | --- |
| ID | FR-007 |
| Title | 員工取消待審核申請 |
| Description | 員工可自行取消尚未被主管審核的請假申請 |
| Actor | 員工（ROLE-001） |
| Trigger | 員工欲撤回申請 |
| Preconditions | 申請單狀態為「待審核」；申請單為該員工本人提交 |
| Source | DEC-014 |
| Status | Confirmed |

### Acceptance Criteria

```gherkin
Given 員工查看自己狀態為「待審核」的申請單
When 員工執行取消
Then 申請單狀態更新為「已取消」，已扣除的配額若有預扣則歸還（見 Q-018）
```

```gherkin
Given 申請單狀態為「已核准」或「已拒絕」
When 員工嘗試取消
Then 系統阻止操作，已完成審核的申請不可取消
```
