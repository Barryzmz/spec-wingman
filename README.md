# ReqForge

ReqForge 是一個需求規格工作流專案，用來協助 PM、開發者與 AI 協作者，將使用者口頭需求、會議紀錄、PPT、Excel、Word、PDF 等資料，整理、釐清並產出正式需求規格文件。

本專案的核心目標不是快速產生文件，而是建立一個可追溯、可審核、可逐步確認的需求整理流程。所有正式需求必須能回到來源、確認狀態與決策紀錄。

## 工作流

1. 01 read inputs
   - Prompt: `prompts/01-read-inputs.prompt.md`
   - Input: `CONSTITUTION.md`, `specs/00-inputs/`
   - Output: `specs/01-discovery/`
   - 放置原始輸入摘要或使用者描述。
   - 不在此階段判斷需求正確性。

2. 02 extract requirements
   - Prompt: `prompts/02-extract-requirements.prompt.md`
   - Input: `CONSTITUTION.md`, `specs/01-discovery/`
   - Output: `specs/02-requirements/`
   - 從已確認事實萃取正式需求。
   - 不確定內容必須回寫 `open-questions.md`。
   - 推測性內容必須回寫 `assumptions.md`。

3. 03 clarify requirements
   - Prompt: `prompts/03-clarify-requirements.prompt.md`
   - Input: `CONSTITUTION.md`, `specs/01-discovery/`, `specs/02-requirements/`
   - Output: `specs/01-discovery/open-questions.md`, `specs/01-discovery/assumptions.md`
   - 釐清需求中的矛盾、缺漏、未確認內容與假設。

4. 04 analyze requirements
   - Prompt: `prompts/04-analyze-requirements.prompt.md`
   - Input: `CONSTITUTION.md`, `specs/01-discovery/`, `specs/02-requirements/`
   - Output: `specs/03-analysis/`
   - 根據已確認需求建立 use cases、user stories、acceptance criteria、domain model、state transitions 與 edge cases。

5. 05 generate spec
   - Prompt: `prompts/05-generate-spec.prompt.md`
   - Input: `CONSTITUTION.md`, `specs/01-discovery/`, `specs/02-requirements/`, `specs/03-analysis/`, `templates/requirement-spec-template.md`
   - Output: `specs/04-design-ready/requirement-spec.md`
   - 只記錄已確認需求。
   - 使用 `FR`、`BR`、`DR`、`WR`、`PR`、`NFR` 等編號。

6. 06 generate design-ready documents
   - Prompt: `prompts/06-generate-design-ready.prompt.md`
   - Input: `CONSTITUTION.md`, `specs/04-design-ready/requirement-spec.md`, `templates/`
   - Output: `specs/04-design-ready/`
   - 產出可交付給設計、前端、後端、測試與專案管理使用的文件。
   - 設計文件只能根據已確認需求產生。

7. 07 update versions
   - Prompt: `prompts/07-update-versions.prompt.md`
   - Input: `CONSTITUTION.md`, `specs/01-discovery/`, `specs/02-requirements/`, `specs/03-analysis/`, `specs/04-design-ready/`
   - Output: `specs/05-versions/changelog.md`, `specs/05-versions/decision-log.md`
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
