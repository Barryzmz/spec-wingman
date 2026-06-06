# API Draft

API 草案只能對應已確認需求。

| API ID | Method | Path | Purpose | Related Requirement |
| --- | --- | --- | --- | --- |
| API-001 | POST | /api/auth/login | 登入（proxy HR API） | NFR-004, BR-030 |
| API-002 | POST | /api/auth/logout | 登出 | NFR-004 |
| API-003 | GET | /api/me | 取得當前使用者資訊 | DR-009 |
| API-004 | POST | /api/leave-requests | 建立請假申請 | FR-001, BR-025 |
| API-005 | GET | /api/leave-requests | 查詢自己的假單列表 | FR-001 |
| API-006 | GET | /api/leave-requests/:id | 查詢假單詳情 | FR-001 |
| API-007 | PATCH | /api/leave-requests/:id/withdraw | 撤回待審核假單 | FR-005, BR-027 |
| API-008 | POST | /api/leave-requests/:id/attachments | 上傳診斷書附件 | FR-002, BR-033, BR-034 |
| API-009 | GET | /api/leave-balances | 查詢自己的假別額度 | BR-025 |
| API-010 | GET | /api/approvals/pending | 查詢待審核假單（主管/代理） | FR-003, BR-028 |
| API-011 | PATCH | /api/leave-requests/:id/approve | 核准假單 | FR-003, WR-002 |
| API-012 | PATCH | /api/leave-requests/:id/reject | 拒絕假單 | FR-003, BR-017, WR-003 |
| API-013 | GET | /api/acting-managers | 查詢自己的代理設定 | FR-008 |
| API-014 | POST | /api/acting-managers | 建立代理主管設定 | FR-008, DR-006 |
| API-015 | DELETE | /api/acting-managers/:id | 移除代理主管設定 | FR-008, BR-020 |
| API-016 | GET | /api/hr/leave-records | HR 查詢全公司假單 | FR-006, PR-006 |
| API-017 | GET | /api/hr/leave-records/export | HR 匯出 Excel 報表 | FR-007, DR-004, DR-005 |
| API-018 | GET | /api/hr/acting-managers | HR 查詢所有代理設定 | FR-009, PR-008 |
| API-019 | GET | /api/notifications | 查詢站內訊息列表 | FR-004, FR-010 |
| API-020 | PATCH | /api/notifications/:id/read | 標記訊息已讀 | FR-004, FR-010 |

---

## API-001: 登入

- Related Requirements: NFR-004, BR-030
- Method: POST
- Path: /api/auth/login
- Auth Required: No

### Request

```json
{
  "username": "string",
  "password": "string"
}
```

### Response

```json
{
  "token": "string",
  "user": {
    "id": "number",
    "name": "string",
    "department": "string",
    "role": "employee | manager | hr",
    "hire_date": "date"
  }
}
```

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 401 | AUTH_FAILED | 驗證失敗 | HR API 回傳驗證不通過 | NFR-004 |
| 503 | HR_API_UNAVAILABLE | HR 系統無法連線 | HR API 無回應 | BR-030 |

---

## API-004: 建立請假申請

- Related Requirements: FR-001, BR-014, BR-024, BR-025, BR-029
- Method: POST
- Path: /api/leave-requests
- Auth Required: Yes (Employee)

### Request

```json
{
  "leave_type": "annual | sick | personal | bereavement",
  "start_date": "date",
  "end_date": "date",
  "reason": "string",
  "bereavement_relation": "string (optional, required if bereavement)",
  "bereavement_death_date": "date (optional, required if bereavement)"
}
```

### Response

```json
{
  "id": "number",
  "status": "pending",
  "working_days": "number",
  "working_hours": "number",
  "reviewer_id": "number",
  "submitted_at": "datetime"
}
```

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 400 | INSUFFICIENT_BALANCE | 額度不足 | 可用額度 < 申請天數 | BR-025 |
| 400 | MIN_DURATION | 最低請假時數為 30 分鐘 | 申請時數 < 0.5h | BR-014 |
| 400 | NO_WORKING_DAYS | 所選區間無工作日 | 起訖日全為週末 | BR-024 |
| 400 | BEREAVEMENT_EXPIRED | 喪假已超過 100 天期限 | 過世日 + 100 天 < 申請日 | BR-021 |
| 400 | NO_MANAGER | 無審核主管 | 員工主管欄位空值 | BR-032 |
| 400 | CERTIFICATE_REQUIRED | 病假 3 天以上須上傳診斷書 | 病假 ≥ 3 天且無附件 | BR-015 |

---

## API-007: 撤回假單

- Related Requirements: FR-005, BR-027, WR-004
- Method: PATCH
- Path: /api/leave-requests/:id/withdraw
- Auth Required: Yes (Employee, owner only)

### Request

無 request body。

### Response

```json
{
  "id": "number",
  "status": "withdrawn",
  "balance_restored": "number"
}
```

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 403 | NOT_OWNER | 無權撤回 | 非本人假單 | PR-002 |
| 409 | INVALID_STATUS | 僅待審核可撤回 | 假單非 pending 狀態 | PR-002 |

---

## API-008: 上傳診斷書

- Related Requirements: FR-002, BR-033, BR-034
- Method: POST
- Path: /api/leave-requests/:id/attachments
- Auth Required: Yes (Employee, owner only)
- Content-Type: multipart/form-data

### Request

```
file: binary (PNG / JPG / PDF, max 5MB)
```

### Response

```json
{
  "id": "number",
  "file_name": "string",
  "file_type": "string",
  "file_size": "number",
  "uploaded_at": "datetime"
}
```

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 400 | INVALID_FILE_TYPE | 僅接受 PNG、JPG、PDF | 檔案格式不符 | BR-033 |
| 400 | FILE_TOO_LARGE | 檔案不得超過 5MB | 檔案 > 5MB | BR-034 |

---

## API-011: 核准假單

- Related Requirements: FR-003, WR-002, BR-026, BR-028
- Method: PATCH
- Path: /api/leave-requests/:id/approve
- Auth Required: Yes (Manager / Acting Manager)

### Request

無 request body。

### Response

```json
{
  "id": "number",
  "status": "approved",
  "reviewed_by": "number",
  "reviewed_at": "datetime"
}
```

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 403 | NOT_REVIEWER | 無審核權限 | 非該假單的審核主管/代理主管 | PR-003, PR-005 |
| 409 | INVALID_STATUS | 僅待審核可核准 | 假單非 pending 狀態 | WR-002 |
| 409 | ALREADY_REVIEWED | 假單已被審核 | 並行審核先審先得 | BR-028 |

---

## API-012: 拒絕假單

- Related Requirements: FR-003, BR-017, WR-003, BR-027
- Method: PATCH
- Path: /api/leave-requests/:id/reject
- Auth Required: Yes (Manager / Acting Manager)

### Request

```json
{
  "rejection_reason": "string (required)"
}
```

### Response

```json
{
  "id": "number",
  "status": "rejected",
  "rejection_reason": "string",
  "balance_restored": "number",
  "reviewed_by": "number",
  "reviewed_at": "datetime"
}
```

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 400 | REASON_REQUIRED | 拒絕必須填寫原因 | rejection_reason 為空 | BR-017 |
| 403 | NOT_REVIEWER | 無審核權限 | 非審核主管/代理主管 | PR-003, PR-005 |
| 409 | INVALID_STATUS | 僅待審核可拒絕 | 假單非 pending | WR-003 |
| 409 | ALREADY_REVIEWED | 假單已被審核 | 並行審核先審先得 | BR-028 |

---

## API-014: 建立代理主管設定

- Related Requirements: FR-008, DR-006
- Method: POST
- Path: /api/acting-managers
- Auth Required: Yes (Manager)

### Request

```json
{
  "acting_manager_id": "number",
  "start_date": "date",
  "end_date": "date"
}
```

### Response

```json
{
  "id": "number",
  "manager_id": "number",
  "acting_manager_id": "number",
  "start_date": "date",
  "end_date": "date"
}
```

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 403 | NOT_MANAGER | 僅主管可設定代理 | 使用者非主管角色 | PR-004 |

---

## API-017: HR 匯出 Excel 報表

- Related Requirements: FR-007, DR-004, DR-005, BR-023
- Method: GET
- Path: /api/hr/leave-records/export
- Auth Required: Yes (HR)

### Query Parameters

```
department: string (optional)
start_date: date (optional)
end_date: date (optional)
```

### Response

- Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- Content-Disposition: attachment; filename="leave-report-{date}.xlsx"

Excel 欄位：員工姓名、部門、假別、開始日期、結束日期、時數（8hr=1天）、申請日期、審核狀態、審核人

### Errors

| Status | Code | Message | Condition | Related Requirement |
| --- | --- | --- | --- | --- |
| 403 | NOT_HR | 僅 HR 可匯出 | 使用者非 HR 角色 | PR-007 |
