# qgjob

A CLI tool to queue and deploy AppWright test jobs across environments like emulators, devices, and BrowserStack.

## Installation

```bash
pip install qgjob
```
Usage
```
qgjob submit --org-id qualgent --app-version-id xyz123 --test tests/onboarding.spec.js --target emulator
```
```
qgjob status --job-id abc456
```

---
