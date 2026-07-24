import os
import uuid
import requests
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


class ImgBBStorageService:
    """
    Service to handle image uploads to ImgBB API.
    API Docs: https://api.imgbb.com/
    """
    API_URL = "https://api.imgbb.com/1/upload"

    @classmethod
    def upload_image(cls, file_obj, name=None):
        api_key = getattr(settings, 'IMGBB_API_KEY', '')
        if not api_key:
            raise ValueError("IMGBB_API_KEY is not configured in settings/.env")

        if hasattr(file_obj, 'read'):
            file_bytes = file_obj.read()
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
        else:
            file_bytes = file_obj

        response = requests.post(
            cls.API_URL,
            data={'key': api_key, 'name': name or f"img_{uuid.uuid4().hex[:8]}"},
            files={'image': file_bytes}
        )

        if response.status_code == 200:
            res_data = response.json()
            if res_data.get('success'):
                return res_data['data']['url']
            raise ValueError(f"ImgBB upload error: {res_data.get('error', {}).get('message', 'Unknown error')}")
        else:
            raise ValueError(f"ImgBB upload failed with HTTP {response.status_code}: {response.text}")


class SupabaseStorageService:
    """
    Service to handle document and media file uploads to Supabase Storage.
    Optimized with HTTP Session Connection Pooling and Streaming.
    """
    _session = None

    @classmethod
    def get_session(cls):
        if cls._session is None:
            cls._session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=50)
            cls._session.mount('https://', adapter)
            cls._session.mount('http://', adapter)
        return cls._session

    @classmethod
    def upload_file(cls, file_obj, name=None):
        supabase_url = getattr(settings, 'SUPABASE_URL', '').rstrip('/')
        supabase_key = getattr(settings, 'SUPABASE_KEY', '')
        bucket = getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'eduqash-media')

        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL or SUPABASE_KEY is not configured in settings/.env")

        filename = name or getattr(file_obj, 'name', f"file_{uuid.uuid4().hex[:8]}")
        ext = os.path.splitext(filename)[1]
        unique_filename = f"media/{uuid.uuid4().hex}{ext}"

        upload_url = f"{supabase_url}/storage/v1/object/{bucket}/{unique_filename}"

        headers = {
            "Authorization": f"Bearer {supabase_key}",
            "apikey": supabase_key,
            "x-upsert": "true",
        }

        # Stream file_obj directly if available
        if hasattr(file_obj, 'read'):
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
            data_to_send = file_obj
        else:
            data_to_send = file_obj

        session = cls.get_session()
        response = session.post(upload_url, headers=headers, data=data_to_send, timeout=60)

        if response.status_code in (200, 201):
            return f"{supabase_url}/storage/v1/object/public/{bucket}/{unique_filename}"
        else:
            raise ValueError(f"Supabase upload failed with HTTP {response.status_code}: {response.text}")


@deconstructible
class CloudMediaStorage(Storage):
    """
    Custom Django Storage Backend.
    Routes images (.jpg, .png, .jpeg, .webp, .gif) -> ImgBB
    Routes files/documents/media -> Supabase Storage
    """
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg'}

    def _save(self, name, content):
        ext = os.path.splitext(name)[1].lower()

        # Upload images to ImgBB
        if ext in self.IMAGE_EXTENSIONS and getattr(settings, 'IMGBB_API_KEY', ''):
            return ImgBBStorageService.upload_image(content, name=name)

        # Upload documents and media files to Supabase Storage
        if getattr(settings, 'SUPABASE_URL', '') and getattr(settings, 'SUPABASE_KEY', ''):
            return SupabaseStorageService.upload_file(content, name=name)

        return name

    def url(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            return name
        return f"{settings.MEDIA_URL}{name}"

    def exists(self, name):
        return False
