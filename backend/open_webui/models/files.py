import logging
import time
from typing import Optional

<<<<<<< HEAD:backend/open_webui/apps/webui/models/files.py
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text

from open_webui.apps.webui.internal.db import Base, JSONField, get_db
=======
from open_webui.internal.db import Base, JSONField, get_db
>>>>>>> upstream/main:backend/open_webui/models/files.py
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])


####################
# Files DB Schema
####################


class File(Base):
    __tablename__ = "file"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    filename = Column(Text)
<<<<<<< HEAD:backend/open_webui/apps/webui/models/files.py
    meta = Column(JSONField)
=======
    path = Column(Text, nullable=True)

    data = Column(JSON, nullable=True)
    meta = Column(JSON, nullable=True)

    access_control = Column(JSON, nullable=True)

>>>>>>> upstream/main:backend/open_webui/models/files.py
    created_at = Column(BigInteger)


class FileModel(BaseModel):
    id: str
    user_id: str
    filename: str
<<<<<<< HEAD:backend/open_webui/apps/webui/models/files.py
    meta: dict
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)
=======
    path: Optional[str] = None

    data: Optional[dict] = None
    meta: Optional[dict] = None

    access_control: Optional[dict] = None

    created_at: Optional[int]  # timestamp in epoch
    updated_at: Optional[int]  # timestamp in epoch
>>>>>>> upstream/main:backend/open_webui/models/files.py


####################
# Forms
####################


class FileMeta(BaseModel):
    name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None

    model_config = ConfigDict(extra="allow")


class FileModelResponse(BaseModel):
    id: str
    user_id: str
    filename: str
<<<<<<< HEAD:backend/open_webui/apps/webui/models/files.py
    meta: dict
=======
    data: Optional[dict] = None
    meta: FileMeta

>>>>>>> upstream/main:backend/open_webui/models/files.py
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(extra="allow")


class FileMetadataResponse(BaseModel):
    id: str
    meta: dict
    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch


class FileForm(BaseModel):
    id: str
    filename: str
<<<<<<< HEAD:backend/open_webui/apps/webui/models/files.py
=======
    path: str
    data: dict = {}
>>>>>>> upstream/main:backend/open_webui/models/files.py
    meta: dict = {}
    access_control: Optional[dict] = None


class FilesTable:
    def insert_new_file(self, user_id: str, form_data: FileForm) -> Optional[FileModel]:
        with get_db() as db:
            file = FileModel(
                **{
                    **form_data.model_dump(),
                    "user_id": user_id,
                    "created_at": int(time.time()),
                }
            )

            try:
                result = File(**file.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return FileModel.model_validate(result)
                else:
                    return None
            except Exception as e:
                print(f"Error creating tool: {e}")
                return None

    def get_file_by_id(self, id: str) -> Optional[FileModel]:
        with get_db() as db:
            try:
                file = db.get(File, id)
                return FileModel.model_validate(file)
            except Exception:
                return None

    def get_file_metadata_by_id(self, id: str) -> Optional[FileMetadataResponse]:
        with get_db() as db:
            try:
                file = db.get(File, id)
                return FileMetadataResponse(
                    id=file.id,
                    meta=file.meta,
                    created_at=file.created_at,
                    updated_at=file.updated_at,
                )
            except Exception:
                return None

    def get_files(self) -> list[FileModel]:
        with get_db() as db:
            return [FileModel.model_validate(file) for file in db.query(File).all()]

<<<<<<< HEAD:backend/open_webui/apps/webui/models/files.py
=======
    def get_files_by_ids(self, ids: list[str]) -> list[FileModel]:
        with get_db() as db:
            return [
                FileModel.model_validate(file)
                for file in db.query(File)
                .filter(File.id.in_(ids))
                .order_by(File.updated_at.desc())
                .all()
            ]

    def get_file_metadatas_by_ids(self, ids: list[str]) -> list[FileMetadataResponse]:
        with get_db() as db:
            return [
                FileMetadataResponse(
                    id=file.id,
                    meta=file.meta,
                    created_at=file.created_at,
                    updated_at=file.updated_at,
                )
                for file in db.query(File)
                .filter(File.id.in_(ids))
                .order_by(File.updated_at.desc())
                .all()
            ]

>>>>>>> upstream/main:backend/open_webui/models/files.py
    def get_files_by_user_id(self, user_id: str) -> list[FileModel]:
        with get_db() as db:
            return [
                FileModel.model_validate(file)
                for file in db.query(File).filter_by(user_id=user_id).all()
            ]

    def delete_file_by_id(self, id: str) -> bool:
        with get_db() as db:
            try:
                db.query(File).filter_by(id=id).delete()
                db.commit()

                return True
            except Exception:
                return False

    def delete_all_files(self) -> bool:
        with get_db() as db:
            try:
                db.query(File).delete()
                db.commit()

                return True
            except Exception:
                return False


Files = FilesTable()
