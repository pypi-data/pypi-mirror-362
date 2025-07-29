
# OmniSwitch AOS 8.x RestFul API Builder for Python - **Aos8ApiBuilder**

**Aos8ApiBuilder** is a lightweight python library that enables developers to interact seamlessly with the OmniSwitch RESTful API running version 8.x releases.

---

## ✨ Supported APIs

- System
- Chassis
- Interface
- LACP
- VLAN
- MVRP 
- VPA
- MAC
- IP

---

## 🛠️ Built With

- **python 3.8**

```python
    dependencies = [
        anyio==4.9.0
        certifi==2025.6.15
        click==8.2.1
        colorama==0.4.6
        ghp-import==2.1.0
        griffe==1.7.3
        h11==0.16.0
        httpcore==1.0.9
        httpx==0.28.1
        idna==3.10
        Jinja2==3.1.6
        Markdown==3.8.2
        MarkupSafe==3.0.2
        mergedeep==1.3.4
        mkdocs==1.6.1
        mkdocs-autorefs==1.4.2
        mkdocs-get-deps==0.2.0
        mkdocstrings==0.29.1
        mkdocstrings-python==1.16.12
        packaging==25.0
        pathspec==0.12.1
        platformdirs==4.3.8
        pymdown-extensions==10.16
        python-dateutil==2.9.0.post0
        PyYAML==6.0.2
        pyyaml_env_tag==1.1
        six==1.17.0
        sniffio==1.3.1
        watchdog==6.0.0
    ]
```

## 🚀 Installation


1. pip install aos8x-api

---

## 📦 Usage Guide

### Step 1: Create an object of AosApiClient


```python

    from aos8_api.ApiBuilder import AosApiClientBuilder

    client = (
        AosApiClientBuilder()
        .setBaseUrl("https://<switch-ip-address>")
        .setUsername("<username>")
        .setPassword("<password>")
        .build()
    )

```

### Step 2: Start calling the respective API in your application

```python

    result = client.vlan.create_vlan(vlan_id=999)
    if result.success:
        print("✅ Vlan operation successfully")
    else:
        print(f"❌ VLAN creation failed (diag={result.diag}): {result.error}")
```

## 📚 Documentation

Please check out the details documentation at https://samuelyip74.github.io/Aos8ApiBuilder/intro/#

---

## 📦 Releases

| Version          | Date       | Notes                       |
|------------------|------------|-----------------------------|
| v8.9.03          | 2025-05-28 | Initial release             |
| v8.9.03post1     | 2025-05-28 | Interface, IP API added     |
| v8.9.03post2     | 2025-05-28 | MVRP, System, MAC added     |
| v8.9.03post3     | 2025-06-01 | chassis API added           |
| v8.9.03post4     | 2025-06-02 | CLI API added               |

---

## 📄 License

```
Copyright (c) Samuel Yip Kah Yean <2025>

This software is licensed for personal, non-commercial use only.

You are NOT permitted to:
- Use this software for any commercial purposes.
- Modify, adapt, reverse-engineer, or create derivative works.
- Distribute, sublicense, or share this software.

All rights are reserved by the author.

For commercial licensing or permission inquiries, please contact:
kahyean.yip@gmail.com
```


