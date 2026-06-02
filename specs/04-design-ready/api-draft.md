# API Draft

API 草案只能對應已確認需求。所有 API 需要身份驗證（auth 機制尚未確認，設計時以 Bearer Token 佔位）。

| API ID | Method | Path | 說明 | 關聯需求 |
| --- | --- | --- | --- | --- |
| API-001 | POST | /api/leave-applications | 提交請假申請 | FR-001 |
| API-002 | GET | /api/leave-applications | 查詢自己的申請列表 | FR-001, PR-001 |
| API-003 | DELETE | /api/leave-applications/{id} | 取消待審核申請 | FR-007 |
| API-004 | PUT | /api/leave-applications/{id}/approve | 核准申請 | FR-002 |
| API-005 | PUT | /api/leave-applications/{id}/reject | 拒絕申請（需填原因） | FR-002 |
| API-006 | POST | /api/acting-managers | 設定代理主管 | FR-006 |
| API-007 | DELETE | /api/acting-managers/{id} | 移除代理主管記錄 | FR-006 |
| API-008 | GET | /api/hr/leave-records | HR 查看所有員工紀錄 | FR-004 |
| API-009 | GET | /api/hr/leave-records/export | HR 匯出 Excel 報表 | FR-005 |
| API-010 | POST | /api/employees | 建立員工 | PR-003 |
| API-011 | PUT | /api/employees/{id} | 更新員工資料 | PR-003 |
| API-012 | GET | /api/employees/{id}/leave-quota | 查詢員工假期配額 | DR-004 |
| API-013 | GET | /api/holidays | 查詢假日清單 | DR-007 |
| API-014 | POST | /api/holidays | 新增國定假日 | DR-007 |
| API-015 | GET | /api/notifications | 查詢系統通知 | FR-003 |

---

## API-001：提交請假申請

- **Method**：POST
- **Path**：/api/leave-applications
- **Auth**：Employee
- **Related Requirements**：FR-001, BR-002, BR-003, BR-005, DEC-011, DEC-019, DEC-020

**Request**
```json
{
  "leave_type": "sick",
  "start_datetime": "2026-06-10T09:00:00",
  "end_datetime": "2026-06-12T18:00:00",
  "reason": "就醫",
  "proxy_employee_id": "emp-456",
  "kinship_tier": null,
  "medical_certificate_url": "https://..."
}
```
> `kinship_tier` 僅喪假需填：`tier1`（父母/配偶）、`tier2`（祖父母/子女/配偶父母）、`tier3`（兄弟姊妹/配偶祖父母）

**Response 201**
```json
{
  "id": "app-789",
  "status": "pending",
  "total_hours": 16.0,
  "submitted_at": "2026-06-02T10:00:00"
}
```
> 若員工無上層主管，`status` 直接回傳 `"approved"`（BR-010）

**Errors**

| Status | Code | Condition | Related Requirement |
| --- | --- | --- | --- |
| 422 | PROXY_REQUIRED | proxy_employee_id 未填 | DEC-019 |
| 422 | QUOTA_EXCEEDED | 申請時數超過剩餘配額 | BR-002, BR-003 |
| 422 | MEDICAL_CERT_REQUIRED | 病假 > 24h 且未附診斷書 | BR-005 |

---

## API-002：查詢自己的申請列表

- **Method**：GET
- **Path**：/api/leave-applications?status=&page=
- **Auth**：Employee（只能查自己）
- **Related Requirements**：FR-001, PR-001

**Response 200**
```json
{
  "data": [
    {
      "id": "app-789",
      "leave_type": "sick",
      "start_datetime": "2026-06-10T09:00:00",
      "end_datetime": "2026-06-12T18:00:00",
      "total_hours": 16.0,
      "status": "pending",
      "submitted_at": "2026-06-02T10:00:00"
    }
  ],
  "total": 1
}
```

---

## API-003：取消待審核申請

- **Method**：DELETE
- **Path**：/api/leave-applications/{id}
- **Auth**：Employee（只能取消自己的）
- **Related Requirements**：FR-007, WR-007

**Response**：204 No Content

**Errors**

| Status | Code | Condition | Related Requirement |
| --- | --- | --- | --- |
| 409 | NOT_CANCELLABLE | 申請狀態非 pending | FR-007 |
| 403 | FORBIDDEN | 非申請人本人 | PR-001 |

---

## API-004：核准申請

- **Method**：PUT
- **Path**：/api/leave-applications/{id}/approve
- **Auth**：Manager / Acting Manager
- **Related Requirements**：FR-002, WR-002, BR-008, BR-009

**Response**：200 `{ "status": "approved" }`

**Errors**

| Status | Code | Condition | Related Requirement |
| --- | --- | --- | --- |
| 403 | OUT_OF_SCOPE | 申請員工非審核者管轄範圍 | BR-008, BR-009 |
| 409 | NOT_PENDING | 申請狀態非 pending | FR-002 |

---

## API-005：拒絕申請

- **Method**：PUT
- **Path**：/api/leave-applications/{id}/reject
- **Auth**：Manager / Acting Manager
- **Related Requirements**：FR-002, WR-003, BR-006

**Request**
```json
{
  "rejection_reason": "與重要會議時間衝突"
}
```

**Response**：200 `{ "status": "rejected" }`

**Errors**

| Status | Code | Condition | Related Requirement |
| --- | --- | --- | --- |
| 422 | REASON_REQUIRED | rejection_reason 未填或空字串 | BR-006 |
| 403 | OUT_OF_SCOPE | 申請員工非審核者管轄範圍 | BR-008, BR-009 |
| 409 | NOT_PENDING | 申請狀態非 pending | FR-002 |

---

## API-006：設定代理主管

- **Method**：POST
- **Path**：/api/acting-managers
- **Auth**：Manager
- **Related Requirements**：FR-006, WR-005, DR-005

**Request**
```json
{
  "acting_employee_id": "emp-123",
  "start_date": "2026-06-10",
  "end_date": "2026-06-20"
}
```

**Response 201**
```json
{
  "id": "act-001",
  "acting_employee_id": "emp-123",
  "start_date": "2026-06-10",
  "end_date": "2026-06-20"
}
```

---

## API-007：移除代理主管記錄

- **Method**：DELETE
- **Path**：/api/acting-managers/{id}
- **Auth**：Manager（只能移除自己建立的）
- **Related Requirements**：FR-006

**Response**：204 No Content

---

## API-008：HR 查看所有員工請假紀錄

- **Method**：GET
- **Path**：/api/hr/leave-records?（篩選參數 Q-017 Pending）
- **Auth**：HR
- **Related Requirements**：FR-004, PR-003

**Response 200**
```json
{
  "data": [
    {
      "employee_name": "王小明",
      "department": "工程部",
      "leave_type": "sick",
      "start_datetime": "2026-06-10T09:00:00",
      "end_datetime": "2026-06-12T18:00:00",
      "total_hours": 16.0,
      "status": "approved",
      "submitted_at": "2026-06-02T10:00:00"
    }
  ],
  "total": 1
}
```

---

## API-009：HR 匯出 Excel 報表

- **Method**：GET
- **Path**：/api/hr/leave-records/export?（篩選參數 Q-017 Pending）
- **Auth**：HR
- **Related Requirements**：FR-005, DR-006
- **Response**：Excel 二進位檔案（Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet）
- **欄位**：員工姓名、部門、假別、開始日期、結束日期、天數、狀態、申請日期（DEC-007）

---

## API-010：建立員工

- **Method**：POST
- **Path**：/api/employees
- **Auth**：HR
- **Related Requirements**：PR-003, DR-001

**Request**
```json
{
  "name": "張三",
  "department": "產品部",
  "manager_id": "emp-001",
  "hire_date": "2026-01-15"
}
```
> `manager_id` 為 null 時，該員工申請請假自動核准（BR-010）

---

## API-011：更新員工資料

- **Method**：PUT
- **Path**：/api/employees/{id}
- **Auth**：HR
- **Related Requirements**：PR-003, DR-001
- **Request**：同 API-010（部分欄位）

---

## API-012：查詢員工假期配額

- **Method**：GET
- **Path**：/api/employees/{id}/leave-quota?year=2026
- **Auth**：Employee（自己）/ HR / Manager（管轄範圍）
- **Related Requirements**：DR-004, BR-001~004

**Response 200**
```json
{
  "employee_id": "emp-123",
  "year": 2026,
  "quotas": [
    { "leave_type": "annual", "total_hours": 120.0, "used_hours": 16.0, "remaining_hours": 104.0 },
    { "leave_type": "sick", "total_hours": 240.0, "used_hours": 0.0, "remaining_hours": 240.0 },
    { "leave_type": "personal", "total_hours": 112.0, "used_hours": 0.0, "remaining_hours": 112.0 }
  ]
}
```

---

## API-013：查詢假日清單

- **Method**：GET
- **Path**：/api/holidays?year=2026
- **Auth**：All
- **Related Requirements**：DR-007, DEC-020

---

## API-014：新增國定假日

- **Method**：POST
- **Path**：/api/holidays
- **Auth**：HR
- **Related Requirements**：DR-007

**Request**
```json
{ "date": "2026-10-10", "name": "國慶日" }
```

---

## API-015：查詢系統通知

- **Method**：GET
- **Path**：/api/notifications?read=false
- **Auth**：All
- **Related Requirements**：FR-003
