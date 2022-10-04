from firebase_admin import storage

class FireBaseStorage:
    @staticmethod
    def get_link_file(source: bytes, dist: str, type: str = None) -> str:
        bucket = storage.bucket()
        blob = bucket.blob(dist)
        blob.upload_from_string(source, content_type=type)
        blob.make_public()
        return blob.public_url