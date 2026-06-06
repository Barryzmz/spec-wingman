# System Design Brief

## Scope

員工請假管理系統 — Web 應用程式，支援員工線上請假、主管審核、HR 紀錄管理。身份驗證與員工資料由外部 HR 系統 API 提供。

## Key Requirements

| Requirement ID | 設計影響 |
| --- | --- |
| NFR-001 | Web 應用，前後端分離架構 |
| NFR-002 | 支援 100+ 人同時使用 |
| NFR-003 | 需排程服務（催辦通知 0:00/12:00） |
| NFR-004 | 後端需整合 HR 驗證 API（登入失敗直接阻擋） |
| NFR-005 | 後端需整合 HR 資料 API（含本地快取容錯） |
| FR-004, FR-010 | 需 Email 發送服務 + 站內訊息機制 |
| BR-025 | 額度預扣需確保併發安全（樂觀鎖或資料庫交易） |

## High-Level Architecture

```
┌──────────────┐     ┌──────────────────────────────────────┐
│   Browser    │────→│           Frontend (SPA)              │
│  (員工/主管/ │     │  - 請假申請  - 審核頁面  - HR 報表    │
│    HR)       │     │  - 通知中心  - 代理設定               │
└──────────────┘     └──────────────┬───────────────────────┘
                                    │ REST API
                     ┌──────────────▼───────────────────────┐
                     │          Backend API Server           │
                     │  - Auth (proxy to HR API)             │
                     │  - Leave Request CRUD                 │
                     │  - Balance Management (預扣/歸還)     │
                     │  - Approval Workflow                  │
                     │  - Acting Manager Management          │
                     │  - Report Export (Excel)              │
                     │  - Notification Service               │
                     └──┬─────────┬─────────┬───────────────┘
                        │         │         │
              ┌─────────▼──┐ ┌───▼────┐ ┌──▼──────────────┐
              │  Database   │ │ Email  │ │  HR System API  │
              │  (主要資料) │ │ Service│ │  - 驗證 API     │
              │  + 本地快取 │ │ (SMTP) │ │  - 員工資料 API │
              └────────────┘ └────────┘ └─────────────────┘
                        │
              ┌─────────▼──────────┐
              │  Scheduler Service  │
              │  - 催辦通知 (cron)  │
              │  - 員工資料同步     │
              └────────────────────┘
```

## Key Design Decisions

| 項目 | 決策 | 原因 |
| --- | --- | --- |
| 架構 | 前後端分離（SPA + REST API） | NFR-001 Web 應用，便於維護與擴展 |
| 驗證 | 後端 proxy 至 HR API，回傳 JWT/Session | NFR-004，BR-030 登入失敗阻擋 |
| 員工資料 | 定期同步至本地資料庫，API 失敗時用快取 | NFR-005，BR-031 |
| 額度管理 | 資料庫交易確保預扣/歸還的原子性 | BR-025，EC-002 併發安全 |
| 代理審核 | 代理期間假單同時對原主管與代理主管可見 | BR-028 並行先審先得 |
| 通知 | Email（SMTP）+ 站內訊息（DB records） | FR-004, FR-010，DEC-013 |
| 排程 | Cron job 每日 0:00/12:00 掃描逾期假單 | NFR-003 |
| 報表 | Server-side Excel 生成，串流下載 | FR-007 |

## Constraints

- 身份驗證完全依賴外部 HR API，無自建帳號功能（NFR-004）
- 組織架構（部門、主管隸屬）由 HR API 提供，系統不管理（DEC-009）
- 第一期不含銷假功能（BR-019）
- 第一期不含國定假日行事曆（DEC-007），僅排除週六日

## Out of Scope

- 銷假流程（第二期，BR-019）
- 公司行事曆 / 國定假日管理（DEC-007）
- 組織架構管理（DEC-009）
- 多租戶、多語系
