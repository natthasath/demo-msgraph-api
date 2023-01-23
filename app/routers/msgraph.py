from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse
from app.models.model_msgraph import ConfigSchema, SearchSchema, CreateUserSchema, UpdateUserSchema, LicenseSchema, ChangeLicenseSchema, ChangePasswordSchema
from app.services.service_msgraph import MSGraphService

router = APIRouter(
    prefix="/msgraph",
    tags=["MSGRAPH"],
    responses={404: {"message": "Not found"}}
)

@router.post("/config")
async def config(data: ConfigSchema = Depends(ConfigSchema)):
    return MSGraphService().config(data.msgraph_client_id, data.msgraph_client_secret, data.msgraph_tenant_id)

@router.get("/user")
async def all_users(request: Request):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().all_users(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)

@router.post("/user/search")
async def search_user(request: Request, data: SearchSchema = Depends(SearchSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().search_user(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.username)

@router.post("/user/license")
async def license_user(request: Request, data: SearchSchema = Depends(SearchSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().license_user(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.username)

@router.patch("/user/license/assign")
async def assign_license(request: Request, data: LicenseSchema = Depends(LicenseSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().assign_license(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.username, data.license)

@router.patch("/user/license/change")
async def change_license(request: Request, data: ChangeLicenseSchema = Depends(ChangeLicenseSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().change_license(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.username, data.old_license, data.new_license)

@router.patch("/user/license/remove")
async def remove_license(request: Request, data: LicenseSchema = Depends(LicenseSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().remove_license(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.username, data.license)

@router.put("/user/create")
async def create_user(request: Request, data: CreateUserSchema = Depends(CreateUserSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().create_user(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.display_name, data.given_name, data.surname, data.job_title, data.mail.lower(), data.mobile_phone, data.principle_name.lower(), data.password.get_secret_value())

@router.patch("/user/update")
async def update_user(request: Request, data: UpdateUserSchema = Depends(UpdateUserSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().update_user(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.username, data.account_enable, data.display_name, data.given_name, data.surname, data.job_title, data.mobile_phone)

@router.delete("/user/delete")
async def delete_user(request: Request, data: SearchSchema = Depends(SearchSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_client_secret = request.cookies.get("msgraph_client_secret")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().delete_user(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, data.username)

@router.patch("/user/reset/password")
async def reset_password(request: Request, data: ChangePasswordSchema = Depends(ChangePasswordSchema)):
    msgraph_client_id = request.cookies.get("msgraph_client_id")
    msgraph_tenant_id = request.cookies.get("msgraph_tenant_id")
    return MSGraphService().reset_password(msgraph_client_id, msgraph_tenant_id, data.username, data.old_password.get_secret_value(), data.new_password.get_secret_value())