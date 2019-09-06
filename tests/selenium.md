# Use selenium to automate actions on an application via the browser GUI

Documentation:
- https://seleniumhq.github.io/selenium/docs/api/javascript/module/selenium-webdriver/index_exports_Builder.html

Mouse actions:
- https://stackoverflow.com/questions/51675713

## Selenium with node.js

In `package.json`
with `"dependencies": {"selenium-webdriver": "^4.0.0-alpha.4"}`

If you are facing such an ERROR:
```text
SessionNotCreatedError: session not created: Chrome version must be between 70 and 73
```

Then download and extract related version of `chromedriver.exe`. See:
- http://chromedriver.chromium.org/downloads
- http://chromedriver.chromium.org/downloads/version-selection

Example for chrome version `70.0.3538`:
- https://chromedriver.storage.googleapis.com/LATEST_RELEASE_70.0.3538
- https://chromedriver.storage.googleapis.com/70.0.3538.97/chromedriver_win32.zip

Then use it:
```bash
export PATH="$HOME/tools/selenium/:$PATH"
chromedriver.exe --version
```
