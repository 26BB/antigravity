---
description: commit and push all Django project changes to GitHub
---

// turbo-all
1. Run the auto-push script from the project root:
   ```powershell
   cd c:\django
   .\git-autopush.ps1
   ```

2. Confirm the push succeeded by checking the latest commits:
   ```powershell
   git -C "c:\django" log --oneline -5
   ```

3. If the push fails due to an expired token, update the remote URL with a fresh PAT:
   ```powershell
   git -C "c:\django" remote set-url origin https://<NEW_PAT>@github.com/26BB/antigravity.git
   ```
   Then re-run step 1.
