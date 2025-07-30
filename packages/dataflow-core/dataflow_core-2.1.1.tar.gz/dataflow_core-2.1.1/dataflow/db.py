from .database_manager import DatabaseManager
from .configuration import ConfigurationManager
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from .utils.logger import CustomLogger

logger = CustomLogger().get_logger(__name__)

dataflow_config = ConfigurationManager('/dataflow/app/config/dataflow.cfg')
db_url = dataflow_config.get_config_value('database', 'database_url')
local_db_url = dataflow_config.get_config_value('database', 'single_user_db_url')

db_manager = DatabaseManager(db_url)
local_db_manager = None

Base = declarative_base()
Local_Base = declarative_base()

def create_tables(local_db=False):
    """
    Create all tables in the database.
    This is called at the start of the application.
    """
    try:
        if local_db:
            global local_db_manager
            if local_db_manager is None:
                local_db_manager = DatabaseManager(local_db_url) 
            Local_Base.metadata.create_all(bind=local_db_manager.get_engine())
        else:
            Base.metadata.create_all(bind=db_manager.get_engine())
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        error_message = f"Failed to create tables: {str(e)}"
        logger.error(error_message)
        raise e
    
def get_local_db():
    """
    Get a local database session.
    
    Yields:
        Session: Local database session
    """
    global local_db_manager
    if local_db_manager is None:
        local_db_manager = DatabaseManager(local_db_url)
    yield from local_db_manager.get_session()

def get_db():
    yield from db_manager.get_session()
