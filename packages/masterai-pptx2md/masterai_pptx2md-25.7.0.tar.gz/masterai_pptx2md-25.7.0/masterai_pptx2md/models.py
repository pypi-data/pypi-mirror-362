from typing import List
from pydantic import BaseModel, Field


class OssConfig(BaseModel):
    access_key_id: str
    access_key_secret: str
    bucket_name: str
    endpoint: str
    endpoint_public: str
    cdn_host: str
    prefix: str


class Config(BaseModel):
    max_img_width: int = Field(description="maximum image with in px", default=None)
    disable_image: bool = Field(description="disable image extraction", default=False)
    disable_color: bool = Field(
        description="prevent adding html tags with colors", default=False
    )
    disable_escaping: bool = Field(
        description="prevent escaping of characters", default=False
    )
    disable_notes: bool = Field(description="do not add presenter notes", default=False)
    enable_slides: bool = Field(description="add slide deliniation", default=True)
    upload_image: bool = Field(description="upload image, need oss config", default=True)
    oss_config: OssConfig | None = Field(description="add oss config", default=None)
    
    allow_image_format: List[str] = Field(description='support image type', default=None)
    min_image_width: int = Field(description='drop if image width less this value', default=None)
    min_image_height: int = Field(description='drop if image height less this value', default=None)
    skip_duplicate_image: bool = Field(description="drop image if duplicate in same card", default=True)
