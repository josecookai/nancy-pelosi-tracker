# 🎯 Nancy Pelosi Tracker - 快速上手指南

> 写给 Mark & 东哥的使用教程

---

## 📦 第一步：获取代码

```bash
git clone https://github.com/josecookai/nancy-pelosi-tracker.git
cd nancy-pelosi-tracker
```

---

## 🤖 第二步：根据你的平台选择使用方式

### 如果你是 OpenClaw 用户 (Mark)

OpenClaw 会自动识别 SKILL.md，你可以直接用自然语言：

```bash
# 生成完整报告
clawd nancy-pelosi-tracker report

# 查看特定持仓
clawd "Show me Pelosi's AMZN position"

# 检查新披露
clawd "Check for new Pelosi filings"

# 设置提醒
clawd "Alert me when AMZN hits $220"
```

**或者直接用 CLI：**
```bash
./scripts/pelosi-tracker report
./scripts/pelosi-tracker position AMZN
./scripts/pelosi-tracker check-filings
```

---

### 如果你是 Claude Code 用户 (东哥)

在 Claude Code 里直接使用：

```bash
# 生成报告
/claude nancy-pelosi-tracker analyze

# 查看详细分析
/claude "Analyze Pelosi's AMZN call option position"

# 代码级操作
/claude "Fetch latest AMZN price and update positions.json"

# 开发模式
/claude "Implement price alert system per ROADMAP.md 2.2"
```

**或者直接运行脚本：**
```bash
python3 scripts/generate-report.py
python3 scripts/fetch-prices.py --update
```

---

## 📊 常用命令速查表

| 功能 | OpenClaw 命令 | Claude Code 命令 | 直接脚本 |
|------|--------------|------------------|---------|
| 生成报告 | `clawd nancy-pelosi-tracker report` | `/claude nancy-pelosi-tracker analyze` | `./scripts/pelosi-tracker report` |
| 查看持仓 | `clawd "Show AMZN position"` | `/claude "Show AMZN details"` | `./scripts/pelosi-tracker position AMZN` |
| 更新价格 | 自动 | `/claude "Refresh prices"` | `python3 scripts/fetch-prices.py --update` |
| 检查新披露 | `clawd "Check new filings"` | `/claude "Check PTR filings"` | `./scripts/pelosi-tracker check-filings` |
| Telegram发送 | `clawd nancy-pelosi-tracker report --notify telegram` | 需配置 | `./scripts/pelosi-tracker report --format markdown --notify telegram` |

---

## 🔧 配置文件位置

```
config/positions.json          # 持仓数据
config/alerts.json (待开发)     # 提醒配置
```

**修改持仓数据：**
```bash
# 编辑配置文件
vim config/positions.json

# 更新价格
python3 scripts/fetch-prices.py --update

# 生成新报告
./scripts/pelosi-tracker report
```

---

## 📱 Telegram 自动推送设置

编辑 `config/positions.json`：

```json
{
  "alerts_config": {
    "notification_channels": [
      {
        "type": "telegram",
        "target": "1327790737"
      }
    ]
  }
}
```

设置环境变量：
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

---

## ⏰ 设置定时任务 (Cron)

```bash
# 每天 10:43 发送报告
0 10 * * * cd /path/to/nancy-pelosi-tracker && ./scripts/pelosi-tracker report --format markdown --notify telegram

# 每小时更新价格
0 * * * * cd /path/to/nancy-pelosi-tracker && python3 scripts/fetch-prices.py --update

# 每6小时检查新披露
0 */6 * * * cd /path/to/nancy-pelosi-tracker && ./scripts/pelosi-tracker check-filings
```

---

## 🗺️ 想要开发新功能？

看 `ROADMAP.md`：

| 任务 | 推荐开发者 | 难度 |
|------|-----------|------|
| CapitolTrades API 集成 | @codex | ⭐⭐⭐ |
| 价格提醒系统 | @claude-code | ⭐⭐ |
| Web Dashboard | @codex | ⭐⭐⭐⭐ |
| 多议员支持 | @claude-code | ⭐⭐⭐ |

**开发示例：**
```bash
# 给 Codex 分配 API 集成任务
cat > task-codex.md << 'EOF'
@codex 请实现 CapitolTrades API 集成
参考 ROADMAP.md 2.1 节的技术规格
需要：
1. 每30分钟轮询新披露
2. 自动更新 positions.json
3. Telegram 新交易提醒
EOF

# 给 Claude Code 分配提醒系统
cat > task-claude.md << 'EOF'
@claude-code 请实现价格提醒系统
参考 ROADMAP.md 2.2 节
需要：
1. 每5分钟检查价格
2. 突破关键价位时 Telegram 通知
3. 支持 upside/support 双方向提醒
EOF
```

---

## ❓ 常见问题

**Q: 需要 API Key 吗？**  
A: Yahoo Finance 免费，CapitolTrades 需要 key（Phase 2 开发）

**Q: 数据延迟多久？**  
A: 股价延迟15分钟，披露数据最长45天（STOCK Act 规定）

**Q: 可以同时开多个提醒吗？**  
A: 可以，每个持仓可以设置 upside_target 和 support_level

**Q: 支持其他议员吗？**  
A: 目前只追踪 Pelosi，Phase 2.4 会扩展到其他议员

---

## 🔗 有用链接

- GitHub: https://github.com/josecookai/nancy-pelosi-tracker
- ROADMAP: https://github.com/josecookai/nancy-pelosi-tracker/blob/main/ROADMAP.md
- CapitolTrades: https://capitoltrades.com

---

有问题随时问！💰
