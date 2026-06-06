# Permission Requirements

| ID | Role | Allowed Action | Denied Action or Scope | Source | Status |
| --- | --- | --- | --- | --- | --- |
| PR-001 | 員工 | 申請請假（建立假單） | — | FACT-005 | Confirmed |
| PR-002 | 員工 | 撤回自己的待審核假單 | 不可撤回他人的假單；不可撤回非「待審核」狀態的假單 | FACT-033 | Confirmed |
| PR-003 | 主管 | 審核（同意/拒絕）下屬的假單 | 不可審核非自己下屬的假單（隸屬關係由外部 HR 系統提供） | FACT-006, FACT-028, Q-010 | Confirmed |
| PR-004 | 主管 | 指定代理主管並設定起訖日期 | — | FACT-039, FACT-040 | Confirmed |
| PR-005 | 代理主管 | 在代理期間內審核原主管下屬的假單，審核結果為最終結果 | 僅限代理起訖日期內 | FACT-039, FACT-040, Q-015 | Confirmed |
| PR-006 | HR | 查看全公司所有員工的請假紀錄 | — | FACT-007 | Confirmed |
| PR-007 | HR | 匯出 Excel 格式請假報表 | — | FACT-036 | Confirmed |
| PR-008 | HR | 查看所有主管的代理人設定 | — | FACT-042 | Confirmed |
