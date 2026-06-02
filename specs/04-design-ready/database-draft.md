# Database Draft

資料庫草案根據 `requirement-spec.md` 產生。

| Table ID | Table Name | 說明 | 關聯需求 |
| --- | --- | --- | --- |
| TBL-001 | employees | 員工基本資料 | DR-001 |
| TBL-002 | leave_applications | 請假申請單 | DR-002 |
| TBL-003 | leave_quotas | 假期配額 | DR-004 |
| TBL-004 | acting_manager_records | 代理主管記錄 | DR-005 |
| TBL-005 | holidays | 國定假日曆 | DR-007 |

---

## TBL-001：employees

- **Related Requirements**：DR-001, PR-003, DEC-010
- **Purpose**：儲存員工基本資料，包含部門與主管關係

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | UUID | Yes | gen_random_uuid() | PK | DR-001 |
| name | VARCHAR(100) | Yes | — | — | DR-001 |
| department | VARCHAR(100) | Yes | — | — | DR-001, BR-008 |
| manager_id | UUID | No | NULL | FK → employees.id；NULL 表示最高層主管，申請自動核准 | DR-001, BR-010 |
| hire_date | DATE | Yes | — | 特休年資計算起算日 | BR-001, DEC-017 |
| created_at | TIMESTAMP | Yes | NOW() | — | — |
| updated_at | TIMESTAMP | Yes | NOW() | — | — |

**Indexes**

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| IDX_employees_manager | manager_id | No | 快速查詢某主管的所轄員工 |

**Relationships**

| From | To | Cardinality | Rule |
| --- | --- | --- | --- |
| employees.manager_id | employees.id | Many-to-1 | 自關聯；NULL = 無主管 |

---

## TBL-002：leave_applications

- **Related Requirements**：DR-002, FR-001, FR-002, FR-007, DEC-011, DEC-019, DEC-020
- **Purpose**：儲存每筆請假申請，包含時間、假別、狀態與審核資訊

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | UUID | Yes | gen_random_uuid() | PK | DR-002 |
| employee_id | UUID | Yes | — | FK → employees.id | DR-002 |
| leave_type | ENUM | Yes | — | 'annual','sick','personal','bereavement' | DR-003 |
| start_datetime | DATETIME | Yes | — | 精度半小時（DEC-011） | DR-002 |
| end_datetime | DATETIME | Yes | — | 精度半小時（DEC-011） | DR-002 |
| total_hours | DECIMAL(5,1) | Yes | — | 工作時數，排除週末與國定假日（DEC-020） | DR-002 |
| reason | TEXT | Yes | — | — | DR-002 |
| proxy_employee_id | UUID | Yes | — | FK → employees.id；申請時必填（DEC-019） | DR-002 |
| kinship_tier | ENUM | No | NULL | 僅喪假填寫：'tier1','tier2','tier3'（BR-004） | DR-002, BR-004 |
| status | ENUM | Yes | 'pending' | 'pending','approved','rejected','cancelled' | DR-002, WR-001~008 |
| medical_certificate_url | VARCHAR(500) | No | NULL | 病假 > 24h 時必填（BR-005） | DR-002 |
| rejection_reason | TEXT | No | NULL | 拒絕時必填（BR-006） | DR-002 |
| reviewer_id | UUID | No | NULL | FK → employees.id；審核人 | DR-002 |
| reviewed_at | DATETIME | No | NULL | 審核時間 | DR-002 |
| last_reminder_sent_at | DATETIME | No | NULL | 最後一次催辦發送時間 | FR-003, BR-007 |
| submitted_at | DATETIME | Yes | NOW() | — | DR-002 |

**Indexes**

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| IDX_leave_app_employee | employee_id | No | 員工查自己的申請 |
| IDX_leave_app_status | status | No | 篩選待審核申請 |
| IDX_leave_app_submitted | submitted_at | No | 催辦排程查詢 |

**Relationships**

| From | To | Cardinality | Rule |
| --- | --- | --- | --- |
| leave_applications.employee_id | employees.id | Many-to-1 | — |
| leave_applications.proxy_employee_id | employees.id | Many-to-1 | — |
| leave_applications.reviewer_id | employees.id | Many-to-1 | Nullable |

---

## TBL-003：leave_quotas

- **Related Requirements**：DR-004, BR-001~004, DEC-017, DEC-018
- **Purpose**：記錄每位員工每年每種假別的配額與使用量（以小時計）

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | UUID | Yes | gen_random_uuid() | PK | DR-004 |
| employee_id | UUID | Yes | — | FK → employees.id | DR-004 |
| leave_type | ENUM | Yes | — | 'annual','sick','personal','bereavement' | DR-004 |
| year | INT | Yes | — | 特休以到職週年年度計；其他以日曆年計 | DR-004, DEC-017 |
| total_hours | DECIMAL(5,1) | Yes | — | 特休依年資（BR-001）；病假240h（BR-002）；事假112h（BR-003） | BR-001~003 |
| used_hours | DECIMAL(5,1) | Yes | 0.0 | — | DR-004 |

> `remaining_hours` = `total_hours - used_hours`（計算欄位，不儲存）

**Indexes**

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| UQ_quota | employee_id, leave_type, year | Yes | 每人每假別每年只有一筆 |

---

## TBL-004：acting_manager_records

- **Related Requirements**：DR-005, FR-006, WR-005, WR-006, BR-009
- **Purpose**：記錄代理主管的指定關係與有效期間

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | UUID | Yes | gen_random_uuid() | PK | DR-005 |
| original_manager_id | UUID | Yes | — | FK → employees.id | DR-005 |
| acting_manager_id | UUID | Yes | — | FK → employees.id | DR-005 |
| start_date | DATE | Yes | — | — | DR-005 |
| end_date | DATE | Yes | — | 到期後代理人權限自動失效（WR-006） | DR-005, BR-009 |
| created_at | TIMESTAMP | Yes | NOW() | — | — |

**Indexes**

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| IDX_acting_mgr_period | acting_manager_id, start_date, end_date | No | 查詢代理人目前是否有效 |

---

## TBL-005：holidays

- **Related Requirements**：DR-007, DEC-020
- **Purpose**：儲存國定假日清單，供工作時數計算使用（週末以日期星期判斷，不另儲存）

| Column | Type | Required | Default | Rule | Related Requirement |
| --- | --- | --- | --- | --- | --- |
| id | UUID | Yes | gen_random_uuid() | PK | DR-007 |
| date | DATE | Yes | — | UNIQUE；僅儲存國定假日（週末以程式邏輯排除） | DR-007, DEC-020 |
| name | VARCHAR(100) | Yes | — | 例：國慶日、元旦 | DR-007 |
| created_at | TIMESTAMP | Yes | NOW() | — | — |

**Indexes**

| Index Name | Columns | Unique | Purpose |
| --- | --- | --- | --- |
| UQ_holiday_date | date | Yes | 避免重複新增同一日期 |
