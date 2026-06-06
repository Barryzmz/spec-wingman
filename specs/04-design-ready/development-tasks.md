# Development Tasks

| Task ID | Task | Area | Related Requirement | Dependencies | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | 建立專案架構與開發環境 | Infra | NFR-001 | — | TBD | Todo |
| TASK-002 | 建立資料庫 Schema（全部 9 張表） | Backend | DR-001~009 | TASK-001 | TBD | Todo |
| TASK-003 | 實作 HR API 整合 — 身份驗證 proxy | Backend | NFR-004, BR-030 | TASK-001 | TBD | Todo |
| TASK-004 | 實作 HR API 整合 — 員工資料同步 + 本地快取 | Backend | NFR-005, BR-031, DR-009 | TASK-002, TASK-003 | TBD | Todo |
| TASK-005 | 實作登入/登出 API（API-001, API-002, API-003） | Backend | NFR-004, BR-030 | TASK-003 | TBD | Todo |
| TASK-006 | 實作假別額度管理（預扣/歸還/重置邏輯） | Backend | BR-025, BR-027, BR-013, BR-029 | TASK-002, TASK-004 | TBD | Todo |
| TASK-007 | 實作請假申請 API（API-004） | Backend | FR-001, BR-014, BR-024, BR-025, BR-032 | TASK-006 | TBD | Todo |
| TASK-008 | 實作工作日計算邏輯（排除週末） | Backend | BR-024, BR-023 | TASK-001 | TBD | Todo |
| TASK-009 | 實作喪假規則驗證（親等/100 天期限） | Backend | BR-010~012, BR-021 | TASK-002 | TBD | Todo |
| TASK-010 | 實作診斷書上傳 API（API-008） | Backend | FR-002, BR-015, BR-033, BR-034 | TASK-002 | TBD | Todo |
| TASK-011 | 實作假單查詢 API（API-005, API-006） | Backend | FR-001 | TASK-002 | TBD | Todo |
| TASK-012 | 實作撤回假單 API（API-007） | Backend | FR-005, BR-027, WR-004 | TASK-006 | TBD | Todo |
| TASK-013 | 實作審核 API — 同意/拒絕（API-011, API-012） | Backend | FR-003, BR-017, BR-028, WR-002, WR-003 | TASK-006 | TBD | Todo |
| TASK-014 | 實作代理主管 CRUD API（API-013~015） | Backend | FR-008, DR-006, BR-020, BR-028 | TASK-002 | TBD | Todo |
| TASK-015 | 實作代理主管審核邏輯（並行先審先得） | Backend | BR-028, BR-026, PR-005 | TASK-013, TASK-014 | TBD | Todo |
| TASK-016 | 實作站內訊息服務（建立/查詢/已讀） | Backend | FR-004, FR-010 | TASK-002 | TBD | Todo |
| TASK-017 | 實作 Email 發送服務 | Backend | FR-004, FR-010 | TASK-001 | TBD | Todo |
| TASK-018 | 實作審核結果通知（Email + 站內，API-019, API-020） | Backend | FR-010, WR-006, WR-007 | TASK-016, TASK-017 | TBD | Todo |
| TASK-019 | 實作催辦通知排程（Cron 0:00/12:00） | Backend | FR-004, NFR-003, WR-005 | TASK-016, TASK-017 | TBD | Todo |
| TASK-020 | 實作 HR 假單查詢 API（API-016） | Backend | FR-006, PR-006 | TASK-002 | TBD | Todo |
| TASK-021 | 實作 HR Excel 報表匯出 API（API-017） | Backend | FR-007, DR-004, DR-005, BR-023 | TASK-020 | TBD | Todo |
| TASK-022 | 實作 HR 代理主管查詢 API（API-018） | Backend | FR-009, PR-008 | TASK-014 | TBD | Todo |
| TASK-023 | 實作到職周年日額度重置排程 | Backend | BR-013, BR-018, BR-001~009 | TASK-006, TASK-004 | TBD | Todo |
| TASK-024 | 前端 — 登入頁（PAGE-001） | Frontend | NFR-004, BR-030 | TASK-005 | TBD | Todo |
| TASK-025 | 前端 — 員工儀表板（PAGE-002） | Frontend | BR-025, FR-001 | TASK-007, TASK-011 | TBD | Todo |
| TASK-026 | 前端 — 申請請假頁（PAGE-003） | Frontend | FR-001, FR-002, BR-014~025, BR-033, BR-034 | TASK-007, TASK-008, TASK-010 | TBD | Todo |
| TASK-027 | 前端 — 我的假單頁 + 撤回（PAGE-004） | Frontend | FR-001, FR-005 | TASK-011, TASK-012 | TBD | Todo |
| TASK-028 | 前端 — 假單詳情頁（PAGE-005） | Frontend | FR-001, FR-003 | TASK-011 | TBD | Todo |
| TASK-029 | 前端 — 待審核假單頁 + 審核操作（PAGE-006） | Frontend | FR-003, BR-017, BR-028 | TASK-013, TASK-015 | TBD | Todo |
| TASK-030 | 前端 — 代理主管設定頁（PAGE-007） | Frontend | FR-008, DR-006, BR-020 | TASK-014 | TBD | Todo |
| TASK-031 | 前端 — HR 請假紀錄 + Excel 匯出（PAGE-008） | Frontend | FR-006, FR-007, DR-004, DR-005 | TASK-020, TASK-021 | TBD | Todo |
| TASK-032 | 前端 — HR 代理主管總覽（PAGE-009） | Frontend | FR-009, PR-008 | TASK-022 | TBD | Todo |
| TASK-033 | 前端 — 通知中心（PAGE-010） | Frontend | FR-004, FR-010 | TASK-016, TASK-018 | TBD | Todo |
| TASK-034 | 權限中介層（角色驗證 + API 路由保護） | Backend | PR-001~008 | TASK-005 | TBD | Todo |
| TASK-035 | 整合測試 — 請假申請流程 | Testing | TC-001~011 | TASK-007~010 | TBD | Todo |
| TASK-036 | 整合測試 — 審核流程 | Testing | TC-012~016 | TASK-013, TASK-015 | TBD | Todo |
| TASK-037 | 整合測試 — 通知與排程 | Testing | TC-017~020 | TASK-018, TASK-019 | TBD | Todo |
| TASK-038 | 整合測試 — HR 功能 | Testing | TC-025~028 | TASK-020~022 | TBD | Todo |
| TASK-039 | 整合測試 — 額度管理與邊界案例 | Testing | TC-029~032 | TASK-006, TASK-023 | TBD | Todo |
| TASK-040 | E2E 測試 — 完整請假審核流程 | Testing | UC-001~004 | TASK-035~039 | TBD | Todo |

## Task Dependency Graph

```
TASK-001 (專案架構)
  ├─→ TASK-002 (DB Schema)
  │     ├─→ TASK-009 (喪假規則)
  │     ├─→ TASK-010 (診斷書上傳)
  │     ├─→ TASK-011 (假單查詢)
  │     ├─→ TASK-014 (代理主管 CRUD)
  │     │     ├─→ TASK-015 (並行審核)
  │     │     ├─→ TASK-022 (HR 代理查詢)
  │     │     └─→ TASK-030 (前端:代理設定)
  │     ├─→ TASK-016 (站內訊息)
  │     └─→ TASK-020 (HR 假單查詢)
  │           └─→ TASK-021 (Excel 匯出)
  ├─→ TASK-003 (HR API 驗證)
  │     ├─→ TASK-004 (員工同步)
  │     │     └─→ TASK-006 (額度管理)
  │     │           ├─→ TASK-007 (請假申請 API)
  │     │           ├─→ TASK-012 (撤回 API)
  │     │           ├─→ TASK-013 (審核 API)
  │     │           └─→ TASK-023 (額度重置排程)
  │     └─→ TASK-005 (登入 API)
  │           └─→ TASK-034 (權限中介層)
  ├─→ TASK-008 (工作日計算)
  └─→ TASK-017 (Email 服務)
        ├─→ TASK-018 (審核結果通知)
        └─→ TASK-019 (催辦排程)
```
