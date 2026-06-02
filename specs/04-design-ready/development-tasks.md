# Development Tasks

| Task ID | 任務 | 類型 | 關聯需求 | 依賴 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| TASK-001 | DB Schema：employees、leave_quotas | Backend | DR-001, DR-004 | — | Todo |
| TASK-002 | DB Schema：leave_applications | Backend | DR-002 | TASK-001 | Todo |
| TASK-003 | DB Schema：acting_manager_records、holidays | Backend | DR-005, DR-007 | TASK-001 | Todo |
| TASK-004 | 工作時數計算邏輯（排除假日與週末） | Backend | DEC-020, DR-007 | TASK-003 | Todo |
| TASK-005 | 假期配額計算邏輯（含特休年資規則） | Backend | BR-001~004, DEC-017, DEC-018 | TASK-001 | Todo |
| TASK-006 | API-001：提交請假申請 | Backend | FR-001 | TASK-002, TASK-004, TASK-005 | Todo |
| TASK-007 | API-003：取消申請 | Backend | FR-007 | TASK-002 | Todo |
| TASK-008 | API-004/005：主管核准 / 拒絕 | Backend | FR-002, BR-006, BR-008, BR-009 | TASK-002, TASK-003 | Todo |
| TASK-009 | API-006/007：代理主管設定 | Backend | FR-006, DR-005 | TASK-003 | Todo |
| TASK-010 | API-008：HR 查看所有請假紀錄 | Backend | FR-004 | TASK-002 | Todo |
| TASK-011 | API-009：HR 匯出 Excel（篩選條件 Q-017 Pending） | Backend | FR-005, DR-006 | TASK-010 | Todo |
| TASK-012 | API-010/011：員工資料管理 CRUD | Backend | PR-003, DR-001 | TASK-001 | Todo |
| TASK-013 | API-012：員工假期配額查詢 | Backend | DR-004 | TASK-005 | Todo |
| TASK-014 | API-013/014：假日曆管理 | Backend | DR-007 | TASK-003 | Todo |
| TASK-015 | API-015：系統通知查詢 | Backend | FR-003 | TASK-018 | Todo |
| TASK-016 | 排程 Job：每日中午催辦逾期申請（含 Email 發送） | Backend | FR-003, BR-007, DEC-008 | TASK-002, TASK-025 | Todo |
| TASK-017 | 排程 Job：代理主管期間到期自動失效 | Backend | WR-006, BR-009 | TASK-003 | Todo |
| TASK-018 | 系統通知寫入邏輯 | Backend | FR-003 | TASK-002 | Todo |
| TASK-019 | 無上層主管自動核准邏輯 | Backend | BR-010, WR-008 | TASK-006 | Todo |
| TASK-020 | PAGE-001：請假申請表單 | Frontend | FR-001 | TASK-006 | Todo |
| TASK-021 | PAGE-002：我的請假紀錄 | Frontend | FR-001, FR-007 | TASK-006, TASK-007 | Todo |
| TASK-022 | PAGE-003：待審核申請清單 | Frontend | FR-002 | TASK-008 | Todo |
| TASK-023 | PAGE-004：申請審核詳情 | Frontend | FR-002 | TASK-008 | Todo |
| TASK-024 | PAGE-005：代理主管設定 | Frontend | FR-006 | TASK-009 | Todo |
| TASK-025 | PAGE-006：HR 請假紀錄總覽 | Frontend | FR-004 | TASK-010 | Todo |
| TASK-026 | PAGE-007：HR 報表匯出（篩選條件 Q-017 Pending） | Frontend | FR-005 | TASK-011 | Todo |
| TASK-027 | PAGE-008：員工資料管理 | Frontend | PR-003, DR-001 | TASK-012 | Todo |
| TASK-028 | PAGE-009：通知中心 | Frontend | FR-003 | TASK-015 | Todo |
| TASK-029 | Email 服務整合 | Infra | FR-003, BR-007 | — | Todo |
| TASK-030 | 初始國定假日資料匯入 | Data | DR-007, DEC-020 | TASK-003 | Todo |

---

## 依賴關係（Critical Path）

```
TASK-001（DB: employees）
  ├── TASK-002（DB: leave_applications）
  │     ├── TASK-006（API: 提交申請）──→ TASK-020（頁面）
  │     ├── TASK-007（API: 取消）──────→ TASK-021（頁面）
  │     ├── TASK-008（API: 審核）──────→ TASK-022, TASK-023（頁面）
  │     └── TASK-010（API: HR紀錄）────→ TASK-025（頁面）
  ├── TASK-005（配額計算）──→ TASK-013（API: 配額查詢）
  └── TASK-012（API: 員工管理）────────→ TASK-027（頁面）

TASK-003（DB: 代理/假日）
  ├── TASK-004（時數計算）──→ TASK-006
  ├── TASK-009（API: 代理）───────────→ TASK-024（頁面）
  ├── TASK-014（API: 假日曆）─────────→ TASK-030（資料匯入）
  └── TASK-017（Job: 代理失效）

TASK-029（Email）──→ TASK-016（Job: 催辦）──→ TASK-018（通知）──→ TASK-015, TASK-028
```

---

## 注意事項

| 項目 | 說明 |
| --- | --- |
| TASK-011, TASK-026 | HR 報表篩選條件 Q-017 Pending，完成設計前建議先實作無篩選版本 |
| TASK-020 | 代理人選單、配額即時顯示、診斷書條件顯示邏輯較複雜，需多方串接 |
| TASK-016 | 需確保定時 Job 冪等（同一申請同一天不重複發送） |
| TASK-005 | 特休配額須依到職日週年計算，需處理跨年度邏輯 |
