# osShared

이문서는 oasis v2에서 사용하는 shared package 원본 소스 입니다. 특이사항에 대하여 참고할 수 있도록 작성된 문서로 필요시 참고 바랍니다.

## 1. pypi publish and verify

- `walter` 개인 pypi.org 가입 > api token 발행
- token을 `.pypirc`에 명시

```toml
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-your-token
```

- token을 `~/Library/Application Support/pypoetry/auth.toml` 생성

```toml
[http-basic]
[http-basic.pypi]
username = "__token__"
password = "pypi-your-token"
```

- build and publish

```bash
poetry publish --build
```

> [!IMPORTANT]
> 반드시 하기 2개 versioning and revisioning 수행 필요
>
> version : pyproject.toml > version
>
> revision : revision_history.md > make history describe

- verify published python package(osShared)
  - `https://pypi.org/manage/project/osshared/releases/`

## 2. 기타 특이사항
