# Non-functional Requirements

| ID | 類別 | 非功能需求 | 衡量方式 | 來源 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | 平台 | 系統為 Web 應用程式 | 可透過瀏覽器存取使用 | FACT-003 | Confirmed |
| NFR-002 | 規模 | 系統需支援約 100 人以上的公司使用 | 同時在線使用者可正常操作 | FACT-001 | Confirmed |
| NFR-003 | 排程 | 催辦通知需於每日 0:00 與 12:00 準時觸發 | 排程任務按時執行 | FACT-032 | Confirmed |
| NFR-004 | 整合 | 系統透過外部 HR 系統提供的 API 進行身份驗證 | 可透過 HR API 完成登入驗證 | Q-011 | Confirmed |
| NFR-005 | 整合 | 員工基本資料（姓名、部門、到職日、主管隸屬）由外部 HR 系統 API 提供 | 系統可從 HR API 取得並同步員工資料 | Q-010, Q-012 | Confirmed |
