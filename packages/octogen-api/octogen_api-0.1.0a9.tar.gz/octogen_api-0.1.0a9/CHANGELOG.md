# Changelog

## 0.1.0-alpha.9 (2025-07-16)

Full Changelog: [v0.1.0-alpha.8...v0.1.0-alpha.9](https://github.com/octogen-ai/octogen-py-api/compare/v0.1.0-alpha.8...v0.1.0-alpha.9)

### Features

* **api:** update via SDK Studio ([0545c18](https://github.com/octogen-ai/octogen-py-api/commit/0545c187c54359f4a5ea30c3a04d2184ba36e3b5))
* clean up environment call outs ([4727d19](https://github.com/octogen-ai/octogen-py-api/commit/4727d190aba50d72c6770a5a6ef4636e52a9aa35))


### Bug Fixes

* **client:** don't send Content-Type header on GET requests ([6531285](https://github.com/octogen-ai/octogen-py-api/commit/653128535a3a6e1ac9a70af14aa07e3a4b24f638))
* **parsing:** correctly handle nested discriminated unions ([74b9ac9](https://github.com/octogen-ai/octogen-py-api/commit/74b9ac988c80ec5e5eec95f02dfe957ff9bd0338))


### Chores

* **ci:** change upload type ([faf79c6](https://github.com/octogen-ai/octogen-py-api/commit/faf79c6e68a31754fc06c57bd56cc31661cdc8b1))
* **internal:** bump pinned h11 dep ([a8f31c0](https://github.com/octogen-ai/octogen-py-api/commit/a8f31c0619aeedc2cb1a8a6b81a9c63b6d96e0e8))
* **internal:** codegen related update ([a1b35e1](https://github.com/octogen-ai/octogen-py-api/commit/a1b35e1108eb462925a20c091f8db0da38371162))
* **package:** mark python 3.13 as supported ([d21fc94](https://github.com/octogen-ai/octogen-py-api/commit/d21fc94443ccf5230e592343b0611076329a3af6))
* **readme:** fix version rendering on pypi ([6abf6b8](https://github.com/octogen-ai/octogen-py-api/commit/6abf6b8c8dc6635421337e5efd97780dd77aeeec))

## 0.1.0-alpha.8 (2025-06-30)

Full Changelog: [v0.1.0-alpha.7...v0.1.0-alpha.8](https://github.com/octogen-ai/octogen-py-api/compare/v0.1.0-alpha.7...v0.1.0-alpha.8)

### Bug Fixes

* **ci:** correct conditional ([033db88](https://github.com/octogen-ai/octogen-py-api/commit/033db888181cca65c169d8fbe1bd1add99207a12))


### Chores

* **ci:** only run for pushes and fork pull requests ([8c58dc4](https://github.com/octogen-ai/octogen-py-api/commit/8c58dc4f1082e24aa468a82dec6748f8b46e74cd))

## 0.1.0-alpha.7 (2025-06-27)

Full Changelog: [v0.1.0-alpha.6...v0.1.0-alpha.7](https://github.com/octogen-ai/octogen-py-api/compare/v0.1.0-alpha.6...v0.1.0-alpha.7)

### Features

* **api:** update via SDK Studio ([e89d19c](https://github.com/octogen-ai/octogen-py-api/commit/e89d19cb2436e675f1f1c8589d5d62c2b814b17d))
* **api:** update via SDK Studio ([1e9501c](https://github.com/octogen-ai/octogen-py-api/commit/1e9501c21f551c73f90d3967bc0ff93149111dba))
* **api:** update via SDK Studio ([37d4932](https://github.com/octogen-ai/octogen-py-api/commit/37d4932be74e4ee05d1c52c59f325037e012f9f8))
* **api:** update via SDK Studio ([6653652](https://github.com/octogen-ai/octogen-py-api/commit/6653652811baaaf2a5b6fd8810104b3d28aaa643))
* **api:** update via SDK Studio ([ae1259d](https://github.com/octogen-ai/octogen-py-api/commit/ae1259d27fc95c82dfe58edbaea284ca90b33722))
* **client:** add support for aiohttp ([731676f](https://github.com/octogen-ai/octogen-py-api/commit/731676f859e2bf9fa3be5410c267bfb597a59a1b))


### Bug Fixes

* **ci:** release-doctor — report correct token name ([f7d3ea1](https://github.com/octogen-ai/octogen-py-api/commit/f7d3ea161e22c4dfd9ec9da436825f4904527a57))
* **client:** correctly parse binary response | stream ([98c3ab0](https://github.com/octogen-ai/octogen-py-api/commit/98c3ab00aee6893c3eff11c5e406ca8f472d3e3e))
* **tests:** fix: tests which call HTTP endpoints directly with the example parameters ([548b04e](https://github.com/octogen-ai/octogen-py-api/commit/548b04e06e667b52383af15294895c7961277fcc))


### Chores

* **ci:** enable for pull requests ([6193e91](https://github.com/octogen-ai/octogen-py-api/commit/6193e91c3c9b9708221f017bd87c0eae82a1abde))
* **internal:** update conftest.py ([5d137f4](https://github.com/octogen-ai/octogen-py-api/commit/5d137f41d76bb174d069ef854ea4a2790e42fa3a))
* **readme:** update badges ([05e4921](https://github.com/octogen-ai/octogen-py-api/commit/05e49213dc7a885c827c35cc36b5829bbf22e6fa))
* **tests:** add tests for httpx client instantiation & proxies ([c6b76d6](https://github.com/octogen-ai/octogen-py-api/commit/c6b76d6e3d10887108724048d9de85fe3ea884d9))
* **tests:** run tests in parallel ([0a4586d](https://github.com/octogen-ai/octogen-py-api/commit/0a4586d329222cb766dd624fa68ebcdf21f97aff))
* **tests:** skip some failing tests on the latest python versions ([5b68667](https://github.com/octogen-ai/octogen-py-api/commit/5b68667cdb3c2fec5677794e4bf7e9d137213244))


### Documentation

* **client:** fix httpx.Timeout documentation reference ([f21e604](https://github.com/octogen-ai/octogen-py-api/commit/f21e604e6f2369989c6cc667907fbacc15d8038d))

## 0.1.0-alpha.6 (2025-06-03)

Full Changelog: [v0.1.0-alpha.5...v0.1.0-alpha.6](https://github.com/octogen-ai/octogen-py-api/compare/v0.1.0-alpha.5...v0.1.0-alpha.6)

### Features

* **api:** update via SDK Studio ([ea2cc84](https://github.com/octogen-ai/octogen-py-api/commit/ea2cc84c01c0699622aea5e813df41511522e718))
* **api:** update via SDK Studio ([53fc39f](https://github.com/octogen-ai/octogen-py-api/commit/53fc39fd24398ebe520ec24a8b7bcc80cb100e2a))
* **api:** update via SDK Studio ([247b403](https://github.com/octogen-ai/octogen-py-api/commit/247b403f0aff8d6a1368f5f6c57fb0f7974233d8))
* **api:** update via SDK Studio ([2c9605b](https://github.com/octogen-ai/octogen-py-api/commit/2c9605b57ed2e5c86a17e99a7ffff829bd853d11))
* **api:** update via SDK Studio ([9d10c5f](https://github.com/octogen-ai/octogen-py-api/commit/9d10c5f411b80eb5f1f41ba1835cbe53231fd7db))
* **api:** update via SDK Studio ([3dfeac3](https://github.com/octogen-ai/octogen-py-api/commit/3dfeac39ac59895d1d4b0bd0af85b18143f2622a))


### Chores

* sync repo ([c673e12](https://github.com/octogen-ai/octogen-py-api/commit/c673e129777494e9368ae934d32c9d75f2e23e67))
