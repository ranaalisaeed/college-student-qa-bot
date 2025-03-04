---
title: college-student-qa-bot
app_file: app.py
sdk: gradio
sdk_version: 5.20.0
---


Command to copy project file content:

```bash
find . -type f ! -path "*/.*" ! -name "*.lock" ! -name "*.md" -exec echo "{}" \; -exec cat {} \; | pbcopy
```