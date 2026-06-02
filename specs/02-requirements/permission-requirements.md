# Permission Requirements

正式權限需求只能記錄已確認內容。

---

## PR-001

| Field | Value |
| --- | --- |
| ID | PR-001 |
| Role | 員工（ROLE-001） |
| Allowed Action | 提交自己的請假申請；查看自己的請假紀錄 |
| Denied Action or Scope | 查看他人請假紀錄；審核任何請假申請 |
| Source | FACT-004, SRC-001 |
| Status | Confirmed |

---

## PR-002

| Field | Value |
| --- | --- |
| ID | PR-002 |
| Role | 主管（ROLE-002） |
| Allowed Action | 查看所轄員工的請假申請；核准或拒絕所轄員工的申請；指定代理人及代理期間 |
| Denied Action or Scope | 查看非所轄員工的請假申請 |
| Source | FACT-005, DEC-005, DEC-006, SRC-001 |
| Status | Confirmed |

---

## PR-003

| Field | Value |
| --- | --- |
| ID | PR-003 |
| Role | HR（ROLE-003） |
| Allowed Action | 查看所有員工的請假紀錄；匯出 Excel 報表；建立與維護員工基本資料 |
| Denied Action or Scope | 核准或拒絕請假申請 |
| Source | FACT-006, FACT-007, DEC-007, DEC-009, DEC-010, SRC-001 |
| Status | Confirmed |

---

## PR-004

| Field | Value |
| --- | --- |
| ID | PR-004 |
| Role | 代理主管（ROLE-004） |
| Allowed Action | 在代理期間內，對原主管管轄員工的申請執行核准或拒絕 |
| Denied Action or Scope | 代理期間外執行任何審核；審核非原主管管轄員工的申請 |
| Source | DEC-006, SRC-001 |
| Status | Confirmed |
