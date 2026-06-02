# Domain Model

## Entities

| Entity ID | 實體名稱 | 描述 | 關聯資料需求 |
| --- | --- | --- | --- |
| ENT-001 | Employee（員工） | 公司員工，可提交請假申請；每人有一個主要部門與對應主管 | DR-001 |
| ENT-002 | Manager（主管） | 負責審核所轄員工申請的人員；本身也是員工 | DR-001, ROLE-002 |
| ENT-003 | LeaveApplication（請假申請單） | 每筆請假申請的核心記錄，包含時間、假別、狀態、原因等 | DR-002 |
| ENT-004 | LeaveType（假別） | 系統支援的假別清單：特休、病假、事假、喪假 | DR-003 |
| ENT-005 | LeaveQuota（假期配額） | 每位員工每年每種假別的配額、已使用與剩餘時數 | DR-004 |
| ENT-006 | ActingManagerRecord（代理主管記錄） | 記錄主管與代理人的關係及代理有效期間 | DR-005 |
| ENT-007 | HR | 人力資源人員，可查看紀錄、匯出報表、管理員工資料 | ROLE-003 |

## Relationships

| Relationship ID | 關係 | 描述 | 來源 |
| --- | --- | --- | --- |
| REL-001 | Employee → LeaveApplication | 一位員工可提交多筆請假申請（1 對多） | FR-001, DR-002 |
| REL-002 | Employee → LeaveQuota | 一位員工每種假別每年有一筆配額記錄（1 對多） | DR-004, BR-001~004 |
| REL-003 | LeaveApplication → LeaveType | 每筆申請對應一種假別（多 對 1） | DR-002, DR-003 |
| REL-004 | Manager → LeaveApplication | 主管可審核所轄員工的多筆申請（1 對多） | FR-002, BR-008 |
| REL-005 | Manager → ActingManagerRecord | 主管可建立代理記錄，指定代理人及期間（1 對多） | FR-006, DR-005 |
| REL-006 | Employee → Manager | 每位員工歸屬一位主要部門主管（多 對 1，BR-008） | DR-001, BR-008 |
| REL-007 | HR → Employee | HR 建立與維護員工基本資料（1 對多） | PR-003, DR-001, DEC-010 |

## 重要約束

| 約束 ID | 描述 | 來源 |
| --- | --- | --- |
| CON-001 | 每位員工只有一個主要部門主管（跨部門以建檔時指定者為準） | BR-008, ASM-003 |
| CON-002 | 代理主管的審核範圍限於原主管的管轄員工，且僅在代理期間有效 | BR-009, DR-005 |
| CON-003 | 假期配額以小時為單位，最小申請單位為 0.5 小時 | DEC-011, DEC-018 |
| CON-004 | 特休配額以員工到職日為週年計算基準 | DEC-017, BR-001 |
