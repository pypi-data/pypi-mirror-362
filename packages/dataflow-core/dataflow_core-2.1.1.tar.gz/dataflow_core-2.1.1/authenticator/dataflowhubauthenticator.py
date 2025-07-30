from dataflow.db import get_db
from dataflow.models import (
    user as m_user,
    session as m_session
    )
from datetime import datetime, timedelta, timezone
import uuid
from jupyterhub.auth import Authenticator

class DataflowHubAuthenticator(Authenticator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = next(get_db())
    
    def generate_session_id(self):
        return str(uuid.uuid4())
    
    async def authenticate(self, handler, data):
        # get username and password
        username = data["username"]
        password = data["password"]

        try:
            # check if user exists
            query = self.db.query(m_user.User)
            user = query.filter(m_user.User.user_name == username).first()

            if user is None or user.password != password:
                return None

            # Check if the user already has an existing session
            existing_session = (
                self.db.query(m_session.Session)
                .filter(m_session.Session.user_id == user.user_id)
                .first()
            )

            if existing_session:
                # Reuse the existing session_id
                session_id = existing_session.session_id
            else:
                # Generate a new session_id
                session_id = self.generate_session_id()
                query = self.db.query(m_session.Session)
                isSession = query.filter(m_session.Session.session_id == session_id).first()

                # If session_id(uuid string) already exists in the database, generate a new one
                while isSession is not None:
                    session_id = self.generate_session_id()
                    isSession = query.filter(m_session.Session.session_id == session_id).first()

                # add session_id to the database
                db_item = m_session.Session(user_id=user.user_id, session_id=session_id)
                self.db.add(db_item)
                self.db.commit()
                self.db.refresh(db_item)

            expires = datetime.now(timezone.utc) + timedelta(days=365)
            host = handler.request.host
            parts = host.split('.')
            if len(parts) >= 2:
                domain =  '.'.join(parts[-2:])
            else:
                domain =  host 
            base_domain = f".{domain}" 
            handler.set_cookie(
                "dataflow_session",
                session_id,
                domain=base_domain, 
                path="/",
                expires=expires,
                secure=True,            
                httponly=True,
                samesite="None"          
            )
            user_dict = {"name": username, "session_id": session_id}
            return user_dict

        except Exception as e:
            return None
        
        finally:
            self.db.close()