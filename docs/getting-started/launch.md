---
title: Launching a Container
subhead: Pod launch scripts, resource flags, and lifetime.
---

## The launch scripts

```bash
launch-scipy-ml.sh -g 1 -c 4 -m 16
```

### Common flags

- `-g` — number of GPUs
- `-c` — CPU cores
- `-m` — memory in GB
- `-i` — a specific container image
