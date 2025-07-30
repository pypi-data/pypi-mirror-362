# Domainize

Library for extracting domains.

## Usage

Domainize does its best to find what we'd typically consider the real domain
of a website. This includes removing subdomains while preserving pseudo-TLD
such as `co.uk`.

```python
import domainize

domainize.get_domain("https://github.com/camber-ops/pipper-domainize")
# github.com

domainize.get_domain("blog.camber.io/foobar")
# camber.io

domainize.get_domain("google.co.uk")
# google.co.uk
```
