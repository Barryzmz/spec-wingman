# Workflow Requirements

正式流程需求只能記錄已確認內容。

---

## WR-001

| Field | Value |
| --- | --- |
| ID | WR-001 |
| Title | 請假申請狀態轉換流程 |
| From State | （新建） |
| Action | 員工填寫申請資訊並提交 |
| To State | 待審核 |
| Actor or System | 員工（ROLE-001） |
| Source | FACT-013, FACT-015, SRC-001 |
| Status | Confirmed |

---

## WR-002

| Field | Value |
| --- | --- |
| ID | WR-002 |
| Title | 主管核准申請 |
| From State | 待審核 |
| Action | 主管核准 |
| To State | 已核准 |
| Actor or System | 主管（ROLE-002）或代理主管（ROLE-004） |
| Source | FACT-015, DEC-006, SRC-001 |
| Status | Confirmed |

---

## WR-003

| Field | Value |
| --- | --- |
| ID | WR-003 |
| Title | 主管拒絕申請 |
| From State | 待審核 |
| Action | 主管填寫原因後拒絕 |
| To State | 已拒絕 |
| Actor or System | 主管（ROLE-002）或代理主管（ROLE-004） |
| Source | FACT-015, FACT-016, SRC-001 |
| Status | Confirmed |

---

## WR-004

| Field | Value |
| --- | --- |
| ID | WR-004 |
| Title | 系統催辦通知流程 |
| From State | 待審核（超過 3 天未處理） |
| Action | 系統每日中午 12:00 自動發送系統內通知與 Email |
| To State | 待審核（持續，直到主管完成審核） |
| Actor or System | 系統（自動） |
| Source | FACT-017, DEC-004, DEC-008, SRC-001 |
| Status | Confirmed |

---

## WR-005

| Field | Value |
| --- | --- |
| ID | WR-005 |
| Title | 代理主管指派流程 |
| From State | 主管登入系統 |
| Action | 主管指定代理人及代理期間 |
| To State | 代理人在指定期間內擁有審核權限 |
| Actor or System | 主管（ROLE-002） |
| Source | DEC-006, SRC-001 |
| Status | Confirmed |

---

## WR-006

| Field | Value |
| --- | --- |
| ID | WR-006 |
| Title | 代理權限自動失效 |
| From State | 代理期間進行中 |
| Action | 系統時間超過代理結束日期 |
| To State | 代理人審核權限失效 |
| Actor or System | 系統（自動） |
| Source | DEC-006, SRC-001 |
| Status | Confirmed |

---

## WR-008

| Field | Value |
| --- | --- |
| ID | WR-008 |
| Title | 無上層主管時申請自動核准 |
| From State | （新建） |
| Action | 員工提交申請，且系統中無指定上層主管 |
| To State | 已核准（自動） |
| Actor or System | 系統（自動） |
| Source | DEC-021 |
| Status | Confirmed |

---

## WR-007

| Field | Value |
| --- | --- |
| ID | WR-007 |
| Title | 員工取消待審核申請 |
| From State | 待審核 |
| Action | 員工執行取消 |
| To State | 已取消 |
| Actor or System | 員工（ROLE-001） |
| Source | DEC-014 |
| Status | Confirmed |
