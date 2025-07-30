from fastapi import APIRouter, Request
from fastapi import Request, Response
from typing import Optional
import json
import httpx
from io import BytesIO
from pydantic import BaseModel, Field
from enum import Enum
from fastapi.responses import JSONResponse
from zylo_docs.services.openapi_service import OpenApiService
from zylo_docs.services.hub_server_service import get_spec_content_by_id
EXTERNAL_API_BASE = "https://api.zylosystems.com"
router = APIRouter()
# 테스트를 위해 임시로 access_token을 하드코딩
access_token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IldsSEd6eVR0emtaaC9GOVAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL21hdXhmc3NjZnpvcmlqdGdubWplLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI1MzQ1YjBiYy1hMTE1LTQ0NTEtYjk4Yy1kZjI0YjMzZjNjMjQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzUzMzE3MDA3LCJpYXQiOjE3NTI3MTIyMDcsImVtYWlsIjoiZGVtb0B6eWxvc3lzdGVtcy5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoiZGVtb0B6eWxvc3lzdGVtcy5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiI1MzQ1YjBiYy1hMTE1LTQ0NTEtYjk4Yy1kZjI0YjMzZjNjMjQifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc1MjcxMjIwN31dLCJzZXNzaW9uX2lkIjoiY2RhOTZkNGItMmU5YS00NDg3LTkwNDYtZTlhNzk4ZjU2ZDIxIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.Ls-yWinr-OfvcDS5StdrKrVaxNWFlZxaL-l1Aq3C4UE"

class DocTypeEnum(str, Enum):
    internal = "internal"
    public = "public"
    partner = "partner"

class ZyloAIRequestBody(BaseModel):
    title: str = Field(..., description="Title of the OpenAPI spec")
    version: str = Field(..., description="Version of the spec")
    doc_type: DocTypeEnum

@router.post("/zylo-ai", include_in_schema=False)
async def create_zylo_ai(request: Request, body: ZyloAIRequestBody):
    service: OpenApiService = request.app.state.openapi_service
    openapi_dict = service.get_current_spec()
    openapi_json_content = json.dumps(openapi_dict, indent=2).encode('utf-8')
    openapi_file_like = BytesIO(openapi_json_content)
    timeout = httpx.Timeout(timeout=None, connect=None, read=None, write=None)
    async with httpx.AsyncClient(timeout=timeout) as client:
        files_for_upload = {
            'file': ('openapi.json', openapi_file_like, 'application/json')
        }
        text_data = {
            "title": body.title,
            "version": body.version,
            "doc_type": body.doc_type.value,
        }
        try:
            resp = await client.post(
                f"{EXTERNAL_API_BASE}/zylo-ai", 
                files=files_for_upload, 
                data=text_data,
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )
            resp.raise_for_status()
        
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content,
                status_code=exc.response.status_code,
                media_type=exc.response.headers.get("content-type")
            )
        response_json = resp.json()
        spec_id = response_json.get("data", {}).get("id")
        if not spec_id:
            return Response(content="Response JSON does not contain 'data.id' field.",status_code=400)
        try:
            tuned_spec_content = await get_spec_content_by_id(spec_id, client, access_token)
            service.set_current_spec(tuned_spec_content)
            return JSONResponse(
                content={
                    "success": True,
                    "message": f"Successfully tuned and applied spec_id: {spec_id}",
                }
            )
        
        except httpx.HTTPStatusError as exc:
            return JSONResponse(
                status_code=exc.response.status_code,
                content={
                    "success": False,
                    "message": "Failed to retrieve tuned spec content",
                    "details": f"specs/{spec_id} endpoint returned an error",
                }
            )
@router.get("/specs/me",include_in_schema=False)
async def get_spec():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{EXTERNAL_API_BASE}/specs/me", headers={"Authorization": f"Bearer {access_token}"})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as exc:
            return Response(
                content=exc.response.content,
                status_code=exc.response.status_code,
                media_type=exc.response.headers.get("content-type")
            )
        
        
    return Response(
        content=resp.content,
        media_type=resp.headers.get("content-type")
    )
@router.get("/specs/{spec_id}", include_in_schema=False)
async def get_spec_by_id(request: Request, spec_id: str):
    if spec_id == "original":
        service: OpenApiService = request.app.state.openapi_service
        service.set_current_spec(request.app.openapi())
        return JSONResponse(
            content={
                "success": True,
                "message": "Original OpenAPI spec retrieved successfully",
            }
        )
    else:
        async with httpx.AsyncClient() as client:
            try:
                spec_content = await get_spec_content_by_id(spec_id, client, access_token)
                service: OpenApiService = request.app.state.openapi_service
                service.set_current_spec(spec_content)
                return JSONResponse(
                    content={
                        "success": True,
                        "message": "Spec retrieved successfully",
                    }
                )
            except httpx.HTTPStatusError as exc:
                return JSONResponse(
                    status_code=exc.response.status_code,
                    content={
                        "success": False,
                        "message": "Failed to retrieve spec content",
                        "details": f"specs/{spec_id} endpoint returned an error",
                    }
                )
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"], include_in_schema=False)
async def proxy(request: Request, path: str):
        async with httpx.AsyncClient() as client:
            proxy_url = f"{EXTERNAL_API_BASE}/{path}"
            body = await request.body()
            headers = dict(request.headers)
            headers.pop("host", None) 

            resp = await client.request(
                method=request.method,
                url=proxy_url,
                content=body,
                headers=headers,
                params=request.query_params,
            )
        headers_to_frontend = dict(resp.headers)
        # 프론트로 보내는 응답 객체 프론트와 인터페이스를 맞춰야함
        return Response(
            headers=headers_to_frontend,
            content=resp.content,
            media_type=resp.headers.get("content-type")
        )

