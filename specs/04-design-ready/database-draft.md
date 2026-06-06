# Database Draft

資料庫草案只能根據已確認資料需求產生。

## Tables Overview

| Table ID | Table Name | Purpose | Related Requirement |
| --- | --- | --- | --- |
| TBL-001 | employees | 員工基本資料（HR API 快取） | DR-009, NFR-005, BR-031 |
| TBL-002 | leave_types | 假別定義 | DR-001 |
| TBL-003 | leave_requests | 請假申請紀錄 | DR-001, DR-003, FR-001 |
| TBL-004 | leave_balances | 假別年度額度 | BR-025, BR-013 |
| TBL-005 | attachments | 假單附件（診斷書） | DR-002, BR-033, BR-034 |
| TBL-006 | acting_managers | 代理主管設定 | DR-006, FR-008 |
| TBL-007 | notifications | 站內訊息 | FR-004, FR-010 |
| TBL-008 | annual_leave_rules | 特休年資對照規則 | DR-007, BR-001~007 |
| TBL-009 | bereavement_leave_rules | 喪假親等對照規則 | DR-008, BR-010~012 |

---

## TBL-001: employees

- Related Requirements: DR-009, NFR-005, BR-031
- Purpose: 從 HR API 同步的員工資料本地快取

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | 系統內部 ID | DR-009 |
| hr_employee_id | VARCHAR(50) | Yes | — | HR 系統員工編號，唯一 | DR-009 |
| name | VARCHAR(100) | Yes | — | 員工姓名 | DR-009 |
| department | VARCHAR(100) | Yes | — | 部門名稱 | DR-009 |
| hire_date | DATE | Yes | — | 到職日期（用於額度計算） | DR-009, BR-013 |
| manager_id | BIGINT FK | No | NULL | 直屬主管 ID（自參照） | DR-009, PR-003, BR-032 |
| role | ENUM('employee','manager','hr') | Yes | 'employee' | 系統角色 | ROLE-001~003 |
| is_active | BOOLEAN | Yes | true | 是否在職 | DR-009 |
| synced_at | TIMESTAMP | Yes | — | 最後同步時間 | NFR-005, BR-031 |
| created_at | TIMESTAMP | Yes | CURRENT | — | — |
| updated_at | TIMESTAMP | Yes | CURRENT | — | — |

### Indexes

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| UQ_hr_employee_id | hr_employee_id | Yes | HR 系統員工編號唯一 |
| IDX_manager_id | manager_id | No | 查詢下屬 |
| IDX_department | department | No | 部門篩選 |

---

## TBL-002: leave_types

- Related Requirements: DR-001
- Purpose: 假別定義（靜態資料）

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | DR-001 |
| code | VARCHAR(20) | Yes | — | annual / sick / personal / bereavement | DR-001 |
| name | VARCHAR(50) | Yes | — | 特休 / 病假 / 事假 / 喪假 | DR-001 |
| annual_quota_days | DECIMAL(5,1) | No | NULL | 年度固定額度（病假 30、事假 14） | BR-008, BR-009 |
| requires_certificate | BOOLEAN | Yes | false | 是否可能需要附件 | BR-015 |
| certificate_threshold_days | DECIMAL(5,1) | No | NULL | 須附件的天數門檻（病假 = 3） | BR-015 |

### Indexes

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| UQ_code | code | Yes | 假別代碼唯一 |

---

## TBL-003: leave_requests

- Related Requirements: DR-001, DR-003, FR-001, WR-001~007
- Purpose: 請假申請紀錄

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | DR-001 |
| employee_id | BIGINT FK | Yes | — | 申請人 → employees.id | FR-001 |
| leave_type_id | BIGINT FK | Yes | — | 假別 → leave_types.id | DR-001 |
| start_date | DATE | Yes | — | 請假開始日期 | DR-001 |
| end_date | DATE | Yes | — | 請假結束日期 | DR-001 |
| reason | TEXT | Yes | — | 請假原因 | DR-001 |
| working_days | DECIMAL(5,1) | Yes | — | 計算後的工作日天數 | BR-024 |
| working_hours | DECIMAL(6,1) | Yes | — | working_days × 8 | BR-023 |
| status | ENUM('pending','approved','rejected','withdrawn') | Yes | 'pending' | 假單狀態 | WR-001~004 |
| reviewer_id | BIGINT FK | No | NULL | 實際審核人 → employees.id | FR-003 |
| rejection_reason | TEXT | No | NULL | 拒絕原因（拒絕時必填） | DR-003, BR-017 |
| bereavement_relation | VARCHAR(50) | No | NULL | 喪假親等關係 | BR-010~012 |
| bereavement_death_date | DATE | No | NULL | 喪假親人過世日期 | BR-021 |
| balance_year_start | DATE | Yes | — | 額度歸屬年度起始日 | BR-029 |
| submitted_at | TIMESTAMP | Yes | CURRENT | 申請送出時間（催辦起算） | FR-004 |
| reviewed_at | TIMESTAMP | No | NULL | 審核時間 | FR-003 |
| created_at | TIMESTAMP | Yes | CURRENT | — | — |
| updated_at | TIMESTAMP | Yes | CURRENT | — | — |

### Indexes

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| IDX_employee_status | employee_id, status | No | 查詢員工假單 + 狀態篩選 |
| IDX_reviewer_status | reviewer_id, status | No | 主管查詢待審核 |
| IDX_status_submitted | status, submitted_at | No | 催辦排程掃描逾期假單 |
| IDX_start_date | start_date | No | 報表日期篩選 |
| IDX_balance_year | employee_id, leave_type_id, balance_year_start | No | 額度歸屬年度查詢 |

---

## TBL-004: leave_balances

- Related Requirements: BR-025, BR-027, BR-013, BR-018
- Purpose: 員工各假別年度額度與使用狀況

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | — |
| employee_id | BIGINT FK | Yes | — | → employees.id | BR-013 |
| leave_type_id | BIGINT FK | Yes | — | → leave_types.id | BR-013 |
| year_start_date | DATE | Yes | — | 額度年度起始日（到職周年日） | BR-013 |
| year_end_date | DATE | Yes | — | 額度年度結束日 | BR-013 |
| total_days | DECIMAL(5,1) | Yes | — | 年度總額度 | BR-001~012 |
| used_days | DECIMAL(5,1) | Yes | 0 | 已核准使用天數 | BR-025 |
| reserved_days | DECIMAL(5,1) | Yes | 0 | 待審核預扣天數 | BR-025 |
| created_at | TIMESTAMP | Yes | CURRENT | — | — |
| updated_at | TIMESTAMP | Yes | CURRENT | — | — |

可用額度 = total_days - used_days - reserved_days（BR-025）

### Indexes

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| UQ_employee_type_year | employee_id, leave_type_id, year_start_date | Yes | 每人每假別每年度唯一 |

---

## TBL-005: attachments

- Related Requirements: DR-002, BR-033, BR-034
- Purpose: 假單附件（診斷書等）

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | DR-002 |
| leave_request_id | BIGINT FK | Yes | — | → leave_requests.id | DR-002 |
| file_name | VARCHAR(255) | Yes | — | 原始檔名 | DR-002 |
| file_path | VARCHAR(500) | Yes | — | 儲存路徑 | DR-002 |
| file_type | VARCHAR(10) | Yes | — | png / jpg / pdf | BR-033 |
| file_size | INT | Yes | — | bytes（≤ 5MB = 5242880） | BR-034 |
| uploaded_at | TIMESTAMP | Yes | CURRENT | — | — |

### Indexes

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| IDX_leave_request_id | leave_request_id | No | 查詢假單附件 |

---

## TBL-006: acting_managers

- Related Requirements: DR-006, FR-008, BR-020, BR-028
- Purpose: 代理主管設定

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | DR-006 |
| manager_id | BIGINT FK | Yes | — | 原主管 → employees.id | FR-008 |
| acting_manager_id | BIGINT FK | Yes | — | 代理人 → employees.id | FR-008 |
| start_date | DATE | Yes | — | 代理起始日 | DR-006 |
| end_date | DATE | Yes | — | 代理結束日 | DR-006 |
| created_at | TIMESTAMP | Yes | CURRENT | — | — |

### Indexes

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| IDX_manager_dates | manager_id, start_date, end_date | No | 查詢主管的代理設定 |
| IDX_acting_dates | acting_manager_id, start_date, end_date | No | 查詢代理主管需審核的假單 |

---

## TBL-007: notifications

- Related Requirements: FR-004, FR-010
- Purpose: 站內訊息

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | — |
| user_id | BIGINT FK | Yes | — | 接收人 → employees.id | FR-004, FR-010 |
| type | ENUM('reminder','approval_result') | Yes | — | 催辦 / 審核結果 | FR-004, FR-010 |
| title | VARCHAR(200) | Yes | — | 訊息標題 | — |
| content | TEXT | Yes | — | 訊息內容 | — |
| leave_request_id | BIGINT FK | No | NULL | 相關假單 | — |
| is_read | BOOLEAN | Yes | false | 已讀狀態 | — |
| created_at | TIMESTAMP | Yes | CURRENT | — | — |

### Indexes

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| IDX_user_read | user_id, is_read | No | 查詢未讀訊息 |
| IDX_user_created | user_id, created_at | No | 訊息列表排序 |

---

## TBL-008: annual_leave_rules

- Related Requirements: DR-007, BR-001~007
- Purpose: 特休年資對照規則（靜態設定）

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | DR-007 |
| min_months | INT | Yes | — | 年資下限（月） | BR-001~007 |
| max_months | INT | No | NULL | 年資上限（月），NULL 表示無上限 | BR-001~007 |
| days | DECIMAL(5,1) | Yes | — | 特休天數 | BR-001~007 |
| increment_per_year | DECIMAL(3,1) | No | NULL | 每年遞增天數（10 年以上 = 1） | BR-007 |
| max_days | DECIMAL(5,1) | No | NULL | 天數上限（30） | BR-007 |

---

## TBL-009: bereavement_leave_rules

- Related Requirements: DR-008, BR-010~012
- Purpose: 喪假親等對照規則（靜態設定）

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | BIGINT PK | Yes | AUTO | — | DR-008 |
| relation | VARCHAR(50) | Yes | — | 親等關係描述 | BR-010~012 |
| days | DECIMAL(5,1) | Yes | — | 喪假天數 | BR-010~012 |
| deadline_days | INT | Yes | 100 | 過世後可申請期限（天） | BR-021 |

---

## Cross-table Relationships

| From | To | Cardinality | FK Column | Rule |
| --- | --- | --- | --- | --- |
| leave_requests | employees | N:1 | employee_id | 申請人 |
| leave_requests | employees | N:1 | reviewer_id | 審核人 |
| leave_requests | leave_types | N:1 | leave_type_id | 假別 |
| leave_balances | employees | N:1 | employee_id | 額度擁有者 |
| leave_balances | leave_types | N:1 | leave_type_id | 假別 |
| attachments | leave_requests | N:1 | leave_request_id | 所屬假單 |
| acting_managers | employees | N:1 | manager_id | 原主管 |
| acting_managers | employees | N:1 | acting_manager_id | 代理人 |
| notifications | employees | N:1 | user_id | 接收人 |
| notifications | leave_requests | N:1 | leave_request_id | 相關假單 |
| employees | employees | N:1 | manager_id | 直屬主管（自參照） |
