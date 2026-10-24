#!/usr/bin/env bash
# Push the site, with its history, to a freshly created empty repository.
#   bash publish-to-new-repo.sh https://github.com/<owner>/hanjopurebuddha.com.git
# Run from inside the drthomasager.com checkout. Afterwards, in the new
# repository: Settings → Pages → Source → GitHub Actions; then Settings →
# Pages → Custom domain → hanjopurebuddha.com, and the DNS records in README.md.
set -euo pipefail
remote="${1:?new repository URL}"
git subtree split --prefix=hanjopurebuddha.com -b hanjopurebuddha-site >/dev/null
git push "$remote" hanjopurebuddha-site:main
echo "Pushed. Now enable Pages (Source: GitHub Actions) and set the custom domain."
