

Command to copy project file content:

```bash
find . -type f ! -path "*/.*" ! -name "*.lock" ! -name "*.md" -exec echo "{}" \; -exec cat {} \; | pbcopy
```