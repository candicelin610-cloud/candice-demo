# Claude 使用偏好

## 語言
- 預設使用**繁體中文**回覆
- 技術術語可保留英文原文（如 API、LLM、CI/CD 等）

## 回應風格
- **先給結論，再展開說明**：直接說重點，有需要再補充背景與細節
- 保持簡潔，避免不必要的鋪陳

## 程式碼風格
- 加上說明性的註解，特別是邏輯複雜或不直觀的地方
- 變數與函式命名要清晰自說明

## 爬蟲工具選擇
- **社群媒體**（Instagram、Twitter/X、LinkedIn 等需要登入或動態渲染的網站）→ 使用 **Playwright MCP**
- **一般網站**（新聞、文章、文件等靜態或半靜態內容）→ 使用 **Firecrawl MCP**

## 模型設定
- 預設模型：`claude-sonnet-4-6`（1M context）
- worktreeBaseRef：`fresh`
- defaultPermissionMode：`default`
