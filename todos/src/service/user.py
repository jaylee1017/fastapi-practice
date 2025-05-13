import bcrypt
from jose import jwt
from datetime import datetime, timedelta

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "1a270679f01a880944670718b6db51efb67a856a430a723bb4e0500fcdda4d40"
    jwt_algorithm: str = "HS256"
    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, plain_password: str, hashed_password: str
    ) -> bool:
        # try/execpt
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username, # it has to be unique
                "exp": datetime.now() + timedelta(days=1),
            },
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )