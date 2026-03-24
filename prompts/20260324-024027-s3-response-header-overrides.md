---
session: "9f3b6a2c4d8e11aa"
timestamp: "2026-03-24T02:40:27Z"
model: codex-gpt-5.4
tools: [web, docker, pytest]
---

## Human

Investigate why presigned S3 downloads ignore `ResponseContentDisposition`,
compare the behavior against the S3 API documentation, and implement the
missing support in robotocore if the feature is part of the documented
`GetObject` / `HeadObject` contract.

## Assistant

## Key decisions

**Treat this as a compatibility bug, not an application-specific feature**:
the S3 API reference for `GetObject` and `HeadObject` documents the
`response-*` URI parameters, including
`response-content-disposition`, `response-content-type`,
`response-content-language`, `response-content-encoding`,
`response-cache-control`, and `response-expires`.
Those parameters are part of the public S3 contract, so robotocore should
honor them when serving successful object responses.

References:
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadObject.html

**Patch the native S3 provider instead of forking Moto behavior broadly**:
robotocore already strips presign signature fields while preserving the
remaining query parameters before forwarding to Moto. The narrowest,
lowest-risk fix is to map the documented `response-*` query parameters onto
the outgoing `GET` / `HEAD` object response after the Moto-backed response is
returned. This keeps the change local to robotocore's S3 compatibility layer
and avoids a wider dependency fork for a small response-shaping gap.

**Add both unit and compatibility coverage**:
the unit test proves the provider applies response header overrides once the
request has been normalized, and the compatibility test proves a real
presigned `get_object` URL returns the expected `Content-Disposition` header
end to end against the running server.
