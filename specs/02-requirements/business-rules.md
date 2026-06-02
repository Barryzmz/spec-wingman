# Business Rules

正式商業規則只能記錄已確認內容。

---

## BR-001

| Field | Value |
| --- | --- |
| ID | BR-001 |
| Rule | 特休年資天數規則 |
| Condition | 員工服務年資落入對應區間 |
| Expected Result | 年資從員工到職日起算，並於每個到職週年日重新計算。天數換算為小時（1天=8小時）：6個月~未滿1年：3天（24小時）；1年~未滿2年：7天（56小時）；2年~未滿3年：10天（80小時）；3年~未滿5年：14天（112小時）；5年~未滿11年（含10年整）：15天（120小時）；第11年起每滿1年加1天（+8小時），上限30天（240小時） |
| Source | DEC-001, DEC-012, DEC-017, DEC-018, SRC-001 |
| Status | Confirmed |

---

## BR-002

| Field | Value |
| --- | --- |
| ID | BR-002 |
| Rule | 病假年度上限 |
| Condition | 員工當年度病假累計使用時數達 240 小時（30天×8小時） |
| Expected Result | 系統不允許再提交病假申請 |
| Source | FACT-010, ASM-002, DEC-018, SRC-001 |
| Status | Confirmed |

---

## BR-003

| Field | Value |
| --- | --- |
| ID | BR-003 |
| Rule | 事假年度上限 |
| Condition | 員工當年度事假累計使用時數達 112 小時（14天×8小時） |
| Expected Result | 系統不允許再提交事假申請 |
| Source | FACT-011, ASM-002, DEC-018, SRC-001 |
| Status | Confirmed |

---

## BR-004

| Field | Value |
| --- | --- |
| ID | BR-004 |
| Rule | 喪假依親等天數規則 |
| Condition | 員工申請喪假並填寫親等關係 |
| Expected Result | 父母或配偶：8天；祖父母、子女或配偶父母：6天；兄弟姊妹或配偶祖父母：3天 |
| Source | DEC-002, SRC-001 |
| Status | Confirmed |

---

## BR-005

| Field | Value |
| --- | --- |
| ID | BR-005 |
| Rule | 病假診斷書強制要求規則 |
| Condition | 病假請假時數大於 24 小時（3天×8小時） |
| Expected Result | 系統要求上傳診斷書，未上傳時不得提交 |
| Source | DEC-003, DEC-018, SRC-001 |
| Status | Confirmed |

---

## BR-006

| Field | Value |
| --- | --- |
| ID | BR-006 |
| Rule | 拒絕申請必須填寫原因 |
| Condition | 主管選擇拒絕請假申請 |
| Expected Result | 主管必須填寫拒絕原因，未填寫時系統阻止提交 |
| Source | FACT-016, SRC-001 |
| Status | Confirmed |

---

## BR-007

| Field | Value |
| --- | --- |
| ID | BR-007 |
| Rule | 催辦通知觸發與頻率規則 |
| Condition | 請假申請單已處於待審核狀態超過 3 天，主管尚未回應 |
| Expected Result | 系統每日中午 12:00 同時發送系統內通知與 Email 給主管，直到主管完成審核 |
| Source | FACT-017, DEC-004, DEC-008, SRC-001 |
| Status | Confirmed |

---

## BR-008

| Field | Value |
| --- | --- |
| ID | BR-008 |
| Rule | 跨部門員工審核主管認定規則 |
| Condition | 員工同時屬於多個部門 |
| Expected Result | 以員工建檔時指定的主要部門主管為唯一審核人 |
| Source | DEC-005, SRC-001 |
| Status | Confirmed |

---

## BR-009

| Field | Value |
| --- | --- |
| ID | BR-010 |
| Rule | 無上層主管時自動核准規則 |
| Condition | 員工提交請假申請，且系統中該員工無指定上層主管 |
| Expected Result | 申請單自動設為「已核准」，無需等待人工審核 |
| Source | DEC-021 |
| Status | Confirmed |

---

## BR-009

| Field | Value |
| --- | --- |
| ID | BR-009 |
| Rule | 代理主管權限範圍規則 |
| Condition | 代理主管在代理期間執行審核 |
| Expected Result | 代理主管只能審核原主管管轄員工的申請，代理期間外審核權限自動失效 |
| Source | DEC-006, SRC-001 |
| Status | Confirmed |
