# ReqForge

ReqForge 是一個需求規格工作流專案，用來協助 PM、開發者與 AI 協作者，將使用者口頭需求、會議紀錄、PPT、Excel、Word、PDF 等資料，整理、釐清並產出正式需求規格文件。

本專案的核心目標不是快速產生文件，而是建立一個可追溯、可審核、可逐步確認的需求整理流程。所有正式需求必須能回到來源、確認狀態與決策紀錄。

## 工作流

1. `specs/00-inputs/`
   - 放置原始輸入摘要或使用者描述。
   - 不在此階段判斷需求正確性。

2. `specs/01-discovery/`
   - 摘要來源、擷取事實、整理問題、列出假設與名詞定義。
   - 不確定內容必須進入 `open-questions.md`。
   - 推測性內容必須進入 `assumptions.md`。

3. `specs/02-requirements/`
   - 只記錄已確認需求。
   - 使用 `FR`、`BR`、`DR`、`WR`、`PR`、`NFR` 等編號。

4. `specs/03-analysis/`
   - 根據已確認需求建立 use cases、user stories、acceptance criteria、domain model、state transitions 與 edge cases。

5. `specs/04-design-ready/`
   - 產出可交付給設計、前端、後端、測試與專案管理使用的文件。
   - 設計文件只能根據已確認需求產生。

6. `specs/05-versions/`
   - 維護 changelog 與 decision log。

## 需求編號

| 類型 | 前綴 | 說明 |
| --- | --- | --- |
| Functional Requirement | `FR` | 功能需求 |
| Business Rule | `BR` | 商業規則 |
| Data Requirement | `DR` | 資料需求 |
| Workflow Requirement | `WR` | 流程需求 |
| Permission Requirement | `PR` | 權限需求 |
| Non-functional Requirement | `NFR` | 非功能需求 |

範例：`FR-001`、`BR-001`、`DR-001`、`WR-001`、`PR-001`、`NFR-001`。

## AI 使用原則

- AI 不得自行腦補需求。
- 不確定的需求必須寫入 `specs/01-discovery/open-questions.md`。
- 假設必須寫入 `specs/01-discovery/assumptions.md`。
- 已確認需求才可以寫入正式需求文件。
- 設計文件只能根據已確認需求產生。
- 所有需求都要盡量可追溯來源。
- 文件全部使用 Markdown。

詳細原則請見 `CONSTITUTION.md`。
