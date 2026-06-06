# Changelog

| Version / Datetime | Changed Files | Summary | Reason | Related Prompt Step |
| --- | --- | --- | --- | --- |
| 1.1.0 / 2026-06-07 | system-design-brief.md, api-draft.md, database-draft.md, frontend-pages.md, test-cases.md, development-tasks.md | 生成完整設計文件：系統架構、20 支 API、9 張 DB 表、10 個前端頁面、32 個測試案例、40 個開發任務（含依賴圖） | 執行步驟 6 — 生成設計文件 | Step 6 - swm.design |
| 1.0.1 / 2026-06-07  | requirement-spec.md, functional-requirements.md, business-rules.md, data-requirements.md, decision-log.md | FR-002 Confirmed：新增 BR-033/034（診斷書格式 PNG/JPG/PDF、大小 ≤ 5MB），DR-002 更新，DEC-020 記錄。所有 FR 皆為 Confirmed | FR-002 診斷書檔案限制釐清 | Step 5 - swm.spec (patch) |
| 1.0.0 / 2026-06-07  | requirement-spec.md | 生成完整需求規格書 v1.0.0：10 FR、34 BR、9 DR、7 WR、8 PR、5 NFR、23 AC、9 UC、10 Entity、18 Edge Case、完整追溯矩陣 | 執行步驟 5 — 生成需求規格書 | Step 5 - swm.spec |
| 0.5.1 / 2026-06-07 | business-rules.md, edge-cases.md, state-transitions.md, decision-log.md | 釐清 4 個邊界案例決策：新增 BR-027~032（預扣歸還、並行審核、年度歸屬、API 容錯），更新 EC-002/010/016/017/018 為 Confirmed，新增 DEC-016~019 | 邊界案例釐清（步驟 4 補充） | Step 4 - swm.analyze (supplement) |
| 0.5.0 / 2026-06-07  | use-cases.md, user-stories.md, acceptance-criteria.md, domain-model.md, state-transitions.md, edge-cases.md | 完成需求分析：9 個 Use Case、13 個 User Story、23 個 AC、10 個 Entity + 10 個 Relationship、5 個狀態轉換、18 個邊界案例 | 執行步驟 4 — 分析需求 | Step 4 - swm.analyze |
| 0.4.0 / 2026-06-07 | open-questions.md, answer-draft.md, assumptions.md, business-rules.md, functional-requirements.md, data-requirements.md, workflow-requirements.md, permission-requirements.md, non-functional-requirements.md, decision-log.md | 釐清 16 個開放問題，新增 6 項 BR（BR-021~026）、1 項 FR（FR-010）、2 項 NFR（NFR-004~005）、1 項 DR（DR-009）、2 項 WR（WR-006~007），確認 15 項決策，2 項假設升格為需求 | 執行步驟 3 — 釐清需求 | Step 3 - swm.clarify |
| 0.3.0 / 2026-06-07  | product-vision.md, functional-requirements.md, business-rules.md, data-requirements.md, workflow-requirements.md, permission-requirements.md, non-functional-requirements.md, user-roles.md | 從 42 項事實提取需求：9 項 FR、20 項 BR、8 項 DR、5 項 WR、8 項 PR、3 項 NFR、4 個角色 | 執行步驟 2 — 提取需求 | Step 2 - swm.extract |
| 0.2.0 / 2026-06-07 | source-summary.md, extracted-facts.md, open-questions.md, assumptions.md, glossary.md | 完成初步探索：從 3 個來源提取 42 項事實、16 個開放問題、6 項假設、12 個術語 | 執行步驟 1 — 讀取輸入 | Step 1 - swm.discover |
| 0.1.0 / 2026-06-07 | Project structure | 初始專案結構建立 | Initial setup | Step 0 - project init |
