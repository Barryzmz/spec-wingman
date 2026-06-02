# 測試驗證報告：員工請假管理系統

- **測試日期**：2026-06-02
- **測試情境**：員工請假管理系統需求工程全流程
- **Git Branch**：test/validation-run-20260602-employee-leave-1
- **輸入來源**：SRC-001（PM 口頭訪談，非正式口述）、SRC-002（特休年資表，由訪談內容補充確認）

---

## 執行步驟摘要

| Step | 名稱 | 狀態 | 產出 |
| --- | --- | --- | --- |
| Step 0 | 準備輸入 | ✅ | `specs/00-inputs/user-description.md` |
| Step 1 | 讀取輸入 | ✅ | 01-discovery 全部 5 個檔案 |
| Step 3b | 釐清問題（Q-001~Q-010） | ✅ | open-questions、decision-log 更新 |
| Step 2 | 提取需求 | ✅ | 02-requirements 全部 8 個檔案 |
| Step 3b | 釐清問題（Q-011~Q-021） | ✅ | 需求文件回填、decision-log 更新 |
| Step 4 | 分析需求 | ✅ | 03-analysis 全部 6 個檔案 |
| Step 5 | 產出需求規格書 | ✅ | `specs/04-design-ready/requirement-spec.md` |
| Step 6 | 產出設計文件 | ✅ | 04-design-ready 全部 6 個設計文件 |
| Step 7 | 版本記錄 | ✅ | 全流程持續維護（changelog v0.1.0 → v1.1.0） |

---

## 需求產出統計

| 類型 | 數量 |
| --- | --- |
| 功能需求（FR） | 7 |
| 商業規則（BR） | 10 |
| 資料需求（DR） | 7 |
| 流程需求（WR） | 8 |
| 權限需求（PR） | 4 |
| 驗收條件（AC） | 18 |
| Use Cases | 7 |
| User Stories | 9 |
| Edge Cases | 14（全部 Confirmed） |

## 設計產出統計

| 類型 | 數量 |
| --- | --- |
| API | 15 |
| DB Table | 5 |
| Frontend Page | 9 |
| Test Cases | 28 |
| Development Tasks | 30 |
| Decision Log（DEC） | 21 |

---

## 問題釐清過程（Q 軌跡）

| Q ID | 問題摘要 | 來源步驟 | 最終狀態 |
| --- | --- | --- | --- |
| Q-001 | 特休年資天數對照表 | Step 1 | Answered（DEC-001） |
| Q-002 | 喪假親等天數對照表 | Step 1 | Answered（DEC-002） |
| Q-003 | 病假診斷書是否強制 | Step 1 | Answered（DEC-003） |
| Q-004 | 催辦方式 | Step 1 | Answered（DEC-004） |
| Q-005 | 跨部門審核主管 | Step 1 | Answered（DEC-005） |
| Q-006 | 代理主管機制 | Step 1 | Answered（DEC-006） |
| Q-007 | HR 報表格式與欄位 | Step 1 | Answered（DEC-007） |
| Q-008 | 催辦頻率 | Q-004 衍生 | Answered（DEC-008） |
| Q-009 | HR 是否可審核 | Step 2 | Answered（DEC-009） |
| Q-010 | 員工資料由誰管理 | Step 2 | Answered（DEC-010） |
| Q-011 | 請假最小單位 | Step 3 | Answered：半小時（DEC-011） |
| Q-012 | 特休 10 年整邊界 | Step 3 | Answered（DEC-012） |
| Q-013 | 配額不足系統行為 | Step 3 | Answered：阻止提交（DEC-013） |
| Q-014 | 員工能否取消申請 | Step 3 | Answered：可取消（DEC-014） |
| Q-015 | 喪假對照表正式確認 | Step 3 | Answered（DEC-015） |
| Q-016 | 年中到職特休計算 | Step 3 | Answered：從到職日起算（DEC-017） |
| Q-017 | HR 報表篩選條件 | Step 3 | **Partial（篩選條件 TBD）** |
| Q-018 | 天與小時換算 | Q-011 衍生 | Answered：1天=8小時（DEC-018） |
| Q-019 | 所有員工申請須綁代理人 | Step 4 | Answered（DEC-019） |
| Q-020 | 週末假日是否計入時數 | Step 4 | Answered：不計入（DEC-020） |
| Q-021 | 主管本人申請由誰審核 | Q-019 衍生 | Answered：無上層主管自動核准（DEC-021） |

---

## 重要決策記錄（關鍵 DEC）

| DEC ID | 決策內容 |
| --- | --- |
| DEC-011 | 請假最小單位為半小時 |
| DEC-012 | 特休年資 10 年整仍為 15 天，第 11 年起+1天 |
| DEC-017 | 特休年資從到職日起算，於週年日重新計算 |
| DEC-018 | 1天=8工作小時（影響所有配額與門檻換算） |
| DEC-019 | 所有員工申請請假時必填代理人 |
| DEC-020 | 請假時數排除週末與國定假日 |
| DEC-021 | 無上層主管員工申請自動核准 |

---

## Assumptions 狀態

| ASM ID | 內容 | 最終狀態 |
| --- | --- | --- |
| ASM-001 | 系統為 Web 應用程式 | **Pending（未確認）** |
| ASM-002 | 病假/事假以勞基法為基準 | Confirmed |
| ASM-003 | 每位員工有一個主要部門 | Confirmed |
| ASM-004 | 請假以天為單位 | **Disproven**（實際為半小時） |

---

## 開放項目（不阻擋設計）

| 項目 | 說明 | 影響範圍 |
| --- | --- | --- |
| Q-017 | HR 報表篩選條件待確認 | FR-005、DR-006、TASK-011、TASK-026 |
| ASM-001 | 系統平台（Web/Mobile）未確認 | 前端技術選型 |

---

## 工作流程觀察

**運作良好**
- 每個 Step 的 prompt 檔案引導清楚，AI 能正確區分已確認需求與假設
- 問題釐清（Step 3）有效攔截多個會影響設計的關鍵決策（如半小時單位、到職日起算、代理人必填）
- 自動核准（BR-010）是在 Step 4 edge case 分析過程中發現的缺口，流程有捕捉到
- changelog 與 decision-log 全程維護，可追溯每個決策的來源與時間點

**待改善觀察**
- Step 3 Phase 1（只問問題）的結果沒有寫入文件的機制，若對話中斷問題會消失；建議未來版本 Phase 1 也寫入 open-questions.md
- Q-017 報表篩選條件雖然不阻擋但 TASK-011/026 需要特別備注，可考慮在 development-tasks.md 加入「blocked_by」欄位
- ASM-001（平台確認）建議在 Step 0 就要求 PM 明確填入，避免設計文件中一直有 Pending 標注
