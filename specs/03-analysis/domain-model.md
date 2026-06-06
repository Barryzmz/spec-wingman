# Domain Model

## Entities

| Entity ID | 實體名稱 | 描述 | 關聯資料需求 |
| --- | --- | --- | --- |
| ENT-001 | Employee（員工） | 系統使用者，可申請請假。基本資料由外部 HR 系統提供（NFR-005） | DR-009 |
| ENT-002 | Manager（主管） | 員工的直屬主管，負責審核下屬假單。隸屬關係由外部 HR 系統提供 | DR-009, PR-003 |
| ENT-003 | LeaveRequest（假單） | 一筆請假申請紀錄，包含假別、起訖日期、原因、狀態等 | DR-001, DR-003 |
| ENT-004 | LeaveType（假別） | 假別類型定義：特休、病假、事假、喪假 | DR-001 |
| ENT-005 | LeaveBalance（假別額度） | 員工在特定年度的各假別剩餘額度，每年到職周年日重置 | DR-007, DR-008, BR-013 |
| ENT-006 | ActingManager（代理主管設定） | 主管指定的代理人與代理起訖日期 | DR-006 |
| ENT-007 | Attachment（附件） | 假單附帶的診斷書等檔案 | DR-002 |
| ENT-008 | Notification（通知） | 系統產生的站內訊息，包含催辦通知與審核結果通知 | FR-004, FR-010 |
| ENT-009 | AnnualLeaveRule（特休年資規則） | 年資與特休天數的對照規則 | DR-007 |
| ENT-010 | BereavementLeaveRule（喪假親等規則） | 親等關係與喪假天數的對照規則 | DR-008 |

## Relationships

| Relationship ID | 關係 | 描述 | 來源 |
| --- | --- | --- | --- |
| REL-001 | Employee → Manager | 每位員工隸屬一位直屬主管（由 HR 系統提供） | PR-003, NFR-005, ASM-002 |
| REL-002 | Employee → LeaveRequest | 一位員工可有多筆假單（1:N） | FR-001 |
| REL-003 | LeaveRequest → LeaveType | 每筆假單對應一種假別（N:1） | DR-001 |
| REL-004 | LeaveRequest → Manager | 每筆假單指派給一位審核主管（N:1）；代理期間可為代理主管 | FR-003, FR-008 |
| REL-005 | LeaveRequest → Attachment | 假單可附帶零至多個附件（1:N）；病假 >= 3 天時至少 1 個 | DR-002, BR-015 |
| REL-006 | Employee → LeaveBalance | 每位員工對每種假別有一筆年度額度（1:N per LeaveType） | BR-008, BR-009, BR-013 |
| REL-007 | Manager → ActingManager | 一位主管可設定一筆代理設定（1:0..1） | DR-006, FR-008 |
| REL-008 | LeaveRequest → Notification | 假單狀態變更可觸發通知（1:N） | FR-004, FR-010 |
| REL-009 | LeaveBalance → AnnualLeaveRule | 特休額度依年資規則計算（N:1） | DR-007 |
| REL-010 | LeaveBalance → BereavementLeaveRule | 喪假額度依親等規則決定（N:1） | DR-008 |

## Entity Relationship Diagram（文字描述）

```
Employee (from HR API)
  ├── 1:N ──→ LeaveRequest
  │              ├── N:1 ──→ LeaveType
  │              ├── N:1 ──→ Manager (reviewer)
  │              ├── 1:N ──→ Attachment (optional)
  │              └── 1:N ──→ Notification
  ├── 1:N ──→ LeaveBalance
  │              ├── N:1 ──→ AnnualLeaveRule
  │              └── N:1 ──→ BereavementLeaveRule
  └── N:1 ──→ Manager (supervisor, from HR API)
                 └── 1:0..1 ──→ ActingManager
```
