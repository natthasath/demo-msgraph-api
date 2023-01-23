from fastapi import Form
from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import List, Union
from enum import Enum
import inspect

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(default = arg.default) if arg.default is not inspect._empty else Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

class ItemLicense(str, Enum):
    A = "Office 365 A1 Plus for faculty"
    B = "Office 365 A1 Plus for students"
    C = "Office 365 A1 for faculty"
    D = "Office 365 A1 for students"

@form_body
class ConfigSchema(BaseModel):
    msgraph_client_id: str = Field(...)
    msgraph_client_secret: str = Field(...)
    msgraph_tenant_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "msgraph_client_id": "xxx",
                "msgraph_client_secret": "xxx",
                "msgraph_tenant_id": "xxx"
            }
        }

@form_body
class SearchSchema(BaseModel):
    username: EmailStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "username@nida.ac.th"
            }
        }

@form_body
class LicenseSchema(BaseModel):
    username: EmailStr = Field(...)
    license: ItemLicense = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "username@nida.ac.th",
                "license": "Office 365 A1 Plus for faculty"
            }
        }

@form_body
class ChangeLicenseSchema(BaseModel):
    username: EmailStr = Field(...)
    old_license: ItemLicense = Field(...)
    new_license: ItemLicense = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "username@nida.ac.th",
                "old_license": "Office 365 A1 Plus for faculty",
                "new_license": "Office 365 A1 for faculty"
            }
        }

@form_body
class CreateUserSchema(BaseModel):
    display_name: str = Field(...)
    given_name: str = Field(None)
    surname: str = Field(None)
    job_title: str = Field(None)
    mail: EmailStr = Field(None)
    mobile_phone: float = Field(None)
    principle_name: EmailStr = Field(...)
    password: SecretStr = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "display_name": "Alan Turing",
                "given_name": "Alan",
                "surname": "Turing",
                "job_title": "นักวิชาการคอมพิวเตอร์ปฏิบัติการ",
                "mail": "username@nida.ac.th",
                "mobile_phone": 3777,
                "principle_name": "username@nida.ac.th",
                "password": "password"
            }
        }

@form_body
class UpdateUserSchema(BaseModel):
    username: EmailStr = Field(...)
    account_enable: bool = Field(None)
    display_name: str = Field(None)
    given_name: str = Field(None)
    surname: str = Field(None)
    job_title: str = Field(None)
    mobile_phone: str = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "username": "username@nida.ac.th",
                "account_enable": True,
                "display_name": "Alan Turing",
                "given_name": "Alan",
                "surname": "Turing",
                "job_title": "นักวิชาการคอมพิวเตอร์ปฏิบัติการ",
                "mobile_phone": 3777
            }
        }

@form_body
class ChangePasswordSchema(BaseModel):
    username: EmailStr = Field(...)
    old_password: SecretStr  = Field(...)
    new_password: SecretStr  = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "username@nida.ac.th",
                "old_password": "old password",
                "new_password": "new password"
            }
        }