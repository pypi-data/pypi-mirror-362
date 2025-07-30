import os, shutil, subprocess, datetime
from .models.environment import JobLogs, Environment
import json, asyncio, pkg_resources
from sqlalchemy.orm import Session
from .configuration import ConfigurationManager

class EnvironmentManager:
    def __init__(self):
        """Initialize the EnvironmentManager"""
        self.config = ConfigurationManager('/dataflow/app/config/dataflow.cfg')
        self.published_env_path = self.config.get_config_value('paths', 'published_env_path')
        self.draft_env_path = self.config.get_config_value('paths', 'drafts_env_path')
        self.env_logs_path = self.config.get_config_value('paths', 'env_logs_path')
    
    async def create_env(self, env_name, py_version, py_requirements, status, base_env_id, env_version=None, user_name=None, db:Session=None):
        """
        Creates a conda environment with specified Python version and packages.
        
        Args:
            env_name (str): Name of the environment
            py_version (str): Python version to use
            py_requirements (list): List of packages to install
            status (str): Environment status ('draft' or 'published')
            env_version (str): Version of the environment (for draft environments)
            user_name (str): Username who initiated the creation
            db (Session): Database session (optional, will create if None)
            
        Returns:
            str: Build status ('success' or 'fail')
        """
        # Set up logging
        log_file_location = None
        if db:
            log_file_location = self._setup_logging(env_name, env_version, user_name, db)

        if status == "published":
            return await self._execute_env_operation(
                env_name=env_name,
                py_version=py_version,
                py_requirements=py_requirements,
                status="published",
                env_version=None,
                mode="create"
            )
        elif status == "draft":
            # Build the environment
            build_status = await self._execute_env_operation(
                env_name=env_name,
                py_version=py_version,
                py_requirements=py_requirements,
                status=status,
                env_version=env_version,
                log_file_location=log_file_location,
                mode="create"
            )
            
            # Update job log status if db was provided
            if db and log_file_location:
                log_file_name = os.path.basename(log_file_location)
                await self._update_job_status(log_file_name, build_status, log_file_location, db)
                updated_py_requirements = self.update_library_versions(py_requirements, os.path.join(self.draft_env_path, env_name, f"{env_name}_v{env_version}"))
                self.update_environment_db(env_name, env_version, updated_py_requirements, base_env_id, py_version, db)

            return build_status
        
        else:
            raise ValueError("Invalid status. Use 'draft' or 'published'.")
    
    async def clone_env(self, source_path, target_env_name, libraries, py_version, user_name=None, db: Session=None):
        """
        Clones an existing conda environment.
        
        Args:
            source_path (str): Path to source environment
            target_name (str): Name for the target environment
            status (str): Environment status ('draft' or 'published')
            env_version (str): Version of the environment (for draft environments)
            user_name (str): Username who initiated the clone
            db (Session): Database session (optional, will create if None)
            
        Returns:
            str: Build status ('success' or 'fail')
        """
        # Set up logging
        log_file_location = None
        if db:
            log_file_location = self._setup_logging(target_env_name, "1", user_name, db)
        
        # Perform the clone operation
        clone_status = await self._execute_env_operation(
            env_name=target_env_name,
            source_path=source_path,
            status="draft",
            env_version="1",
            log_file_location=log_file_location,
            mode="clone"
        )
        
        # Update job log status if db was provided
        if db and log_file_location:
            log_file_name = os.path.basename(log_file_location)
            await self._update_job_status(log_file_name, clone_status, log_file_location, db)
            self.update_environment_db(env_short_name=target_env_name, version="1", libraries=libraries, base_env_id=None, py_version=py_version, db=db)
            
        return clone_status
    
    async def create_published_env(self, env_name, py_version, py_requirements):
        """
        Creates a published conda environment.
        
        Args:
            env_name (str): Name of the environment
            py_version (str): Python version to use
            py_requirements (list): List of packages to install
            status (str): Environment status ('draft' or 'published')
            env_version (str): Version of the environment (for draft environments)
            user_name (str): Username who initiated the creation
            
        Returns:
            str: Build status ('success' or 'fail')
        """
        return self._execute_env_operation(
            env_name=env_name,
            py_version=py_version,
            py_requirements=py_requirements,
            status="published",
            env_version=None,
            mode="create"
        )
        
    async def _execute_env_operation(self, env_name: str, status: str, mode: str, env_version: str = None, py_version: str = None, py_requirements=None, source_path=None, log_file_location=None):
        """
        Executes environment operations (create or clone).
        
        Args:
            env_name (str): Name of the environment
            status (str): Environment status ('draft' or 'published')
            mode (str): Operation mode ('create' or 'clone')
            env_version (str): Version of the environment (for draft environments)
            py_version (str): Python version to use (for create mode)
            py_requirements (list): List of packages to install (for create mode)
            source_path (str): Path to source environment (for clone mode)
            log_file_location (str): Path to log file
            
        Returns:
            str: Build status ('success' or 'fail')
        """
        status = status.lower()
        if status == "published":
            env_base_path = self.config.get_config_value('paths', 'published_env_path')
            conda_env_path = os.path.join(env_base_path, env_name)
        else:
            env_base_path = self.config.get_config_value('paths', 'drafts_env_path')
            conda_env_path = os.path.join(env_base_path, env_name, f"{env_name}_v{env_version}")

        try:
            if not os.path.exists(conda_env_path):
                os.makedirs(conda_env_path, exist_ok=True)

            if mode == "create":
                # Convert requirements list to comma-separated string
                if isinstance(py_requirements, list):
                    py_requirements = ",".join(py_requirements)
                
                create_env_script_path = pkg_resources.resource_filename('dataflow', 'scripts/create_environment.sh')
                command = ["bash", create_env_script_path, py_requirements, conda_env_path, py_version]
                
            elif mode == "clone":
                clone_env_script_path = pkg_resources.resource_filename('dataflow', 'scripts/clone_environment.sh')
                command = ["bash", clone_env_script_path, source_path, conda_env_path]
                
            else:
                raise ValueError("Invalid mode. Use 'create' or 'clone'.")

            process = await asyncio.create_subprocess_exec(
                *command, 
                stdout=asyncio.subprocess.PIPE, 
                stderr=asyncio.subprocess.PIPE
            )

            if not log_file_location:
                return process

            with open(log_file_location, "a") as log_file:
                success_detected = False
                try:
                    while True:
                        line = await process.stdout.readline()
                        if not line:
                            break
                            
                        line = line.decode()
                        message = {
                            "timestamp": self.format_timestamp(),
                            "type": "log",  
                            "content": line.strip()
                        }
                        log_file.write(json.dumps(message) + "\n")
                        log_file.flush()

                        if "environment creation successful" in line.lower():
                            success_detected = True
                            
                    await process.wait()  # Ensure process is complete
                    
                    if process.returncode != 0:
                        error_message = await process.stderr.read()
                        error_message = error_message.decode().strip()
                        error_message_dict = {
                            "timestamp": self.format_timestamp(),
                            "type": "error",
                            "content": error_message
                        }
                        log_file.write(json.dumps(error_message_dict) + "\n")

                    final_build_status = "fail" if process.returncode != 0 else "success"

                except asyncio.CancelledError:
                    process.kill()
                    msg_content = "Environment operation cancelled due to request cancellation."
                    cancellation_message = {
                        "timestamp": self.format_timestamp(),
                        "type": "error",
                        "content": msg_content
                    }
                    log_file.write(json.dumps(cancellation_message) + "\n")
                    final_build_status = "fail"
                
                finally:
                    if final_build_status == "success" and status == "draft":
                        symlink_path = os.path.join(env_base_path, env_name, "default")
                        self.update_symlink(symlink_path, conda_env_path)
                    elif final_build_status != "success":
                        if os.path.exists(conda_env_path):
                            shutil.rmtree(conda_env_path)
                
            return final_build_status
        
        except OSError as e:
            print(f"OS error while operating on {conda_env_path}: {e}")
            return "fail"
        except subprocess.CalledProcessError as e:
            print(f"Subprocess error during environment operation: {e}")
            return "fail"
        except Exception as e:
            print(f"Unexpected error during environment operation for {env_name}: {e}")
            return "fail"
    
    def _setup_logging(self, env_name: str, env_version: str, user_name: str, db: Session):
        """
        Sets up logging for environment operations.
        
        Args:
            env_name (str): Name of the environment
            env_version (str): Version of the environment
            user_name (str): Username who initiated the operation
            db (Session): Database session
            
        Returns:
            str: Path to the log file
        """
        versioned_name = f"{env_name}_v{env_version}"
        log_file_name = f"envlog_{versioned_name}.log"
        log_file_dir = self.config.get_config_value('paths', 'env_logs_path')
        os.makedirs(log_file_dir, exist_ok=True)
        log_file_location = os.path.join(log_file_dir, log_file_name)
        
        # Clear log file if it exists
        if os.path.exists(log_file_location):
            open(log_file_location, "w").close()
        
        # Create job entry
        self.create_job_entry(user_name, db, log_file_name, log_file_location)
        
        return log_file_location
    
    async def _update_job_status(self, log_file_name: str, build_status: str, log_file_location: str, db: Session):
        """
        Updates job status with retry logic.
        
        Args:
            db (Session): Database session
            log_file_name (str): Name of the log file
            build_status (str): Build status ('success' or 'fail') 
            log_file_location (str): Path to the log file
        """
        attempts = 3
        retry_delay = 3
        
        while attempts > 0:
            try:
                self.update_job_log(db, log_file_name, build_status)
                break
            except Exception as e:
                attempts -= 1
                
                with open(log_file_location, "a") as log_file:
                    msg_content = "Failed to commit job completion time to database."
                    error_message = {
                        "timestamp": self.format_timestamp(),
                        "type": "error",
                        "content": msg_content
                    }
                    log_file.write(json.dumps(error_message) + "\n")
                
                if attempts > 0:
                    await asyncio.sleep(retry_delay)
                else:
                    print(f"Failed to update job log after multiple attempts: {e}")
    
    def create_job_entry(self, user_name: str, db: Session, log_file_name: str, log_file_location: str):
        """
        Creates or updates a job entry for environment tracking.
        
        Args:
            user_name (str): The user who initiated the job
            db (Session): Database session
            log_file_name (str): Log file name
            log_file_location (str): Log file path
            
        Returns:
            JobLogs: The created or updated job entry
        """
        job = db.query(JobLogs).filter(JobLogs.log_file_name == log_file_name).first()

        if job:
            if job.status == "success":
                raise ValueError(f"Job with log_file_name '{log_file_name}' already completed successfully.")
            if job.status == "fail":
                job.created_at = datetime.datetime.now() 
                job.status = "in_progress"
        else:
            job = JobLogs(
                created_at=datetime.datetime.now(),
                log_file_name=log_file_name,
                log_file_location=log_file_location,
                created_by=user_name,
                status="in_progress"
            )
            db.add(job)

        db.commit()
        return job
    
    def update_job_log(self, db, log_file_name, final_build_status):
        """
        Updates the JobLogs table with completion time and status.
        
        Args:
            db (Session): Database session
            log_file_name (str): Name of the log file
            final_build_status (str): Final status of the build ('success' or 'fail')
        """
        try:
            job_record = db.query(JobLogs).filter(JobLogs.log_file_name == log_file_name).first()
            if job_record:
                job_record.completed_at = datetime.datetime.now()
                job_record.status = final_build_status
                db.commit()
            else:
                raise ValueError(f"No job log found for file: {log_file_name}")
        except Exception as e:
            db.rollback()
            raise
            
    def update_symlink(self, symlink_path, conda_env_path):
        """
        Creates or updates the symlink to point to the default version.
        """
        symlink_dir = os.path.dirname(symlink_path)
        if not os.path.exists(symlink_dir):
            os.makedirs(symlink_dir, exist_ok=True)

        # If symlink exists, remove it before updating
        if os.path.islink(symlink_path):
            os.remove(symlink_path)

        subprocess.run(["ln", "-sf", conda_env_path, symlink_path], check=True)

    def format_timestamp(self):
        """
        Generates a formatted timestamp string representing the current date and time.

        Returns:
            str: A string representing the current date and time in the specified format.
        """
        return datetime.datetime.now().strftime("%b %d  %I:%M:%S %p")
    
    def update_environment_db(self, env_short_name, version, libraries, base_env_id, py_version, db: Session):
        """
        Updates the environment table with the new version and libraries.
        """
        try:
            if isinstance(libraries, list):
                libraries = ", ".join(libraries)
            current_env = db.query(Environment).filter(Environment.short_name == env_short_name).first()
            status = "Draft" if current_env and current_env.status == "Saved" else current_env.status
            db.query(Environment).filter(Environment.short_name == env_short_name).update({"version": version, "py_requirements": libraries,"base_image_id": base_env_id,"py_version": py_version,"status": status})
            db.commit()

        except Exception as e:
            db.rollback()
            raise

    
    def update_library_versions(self, libraries: list, conda_env_path: str) -> list:
        """
        Updates libraries without version specifications by getting their actual installed versions.
        
        Args:
            libraries (list): List of library requirements, some may not have version specs.
            conda_env_path (str): Path to the conda environment where libraries are installed.
            
        Returns:
            list: Updated list of libraries with version specifications.
        """
        try:
            pip_freeze_cmd = f"{conda_env_path}/bin/pip freeze"
            result = subprocess.run(
                pip_freeze_cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                check=True
            )
            
            installed_versions = {}
            for line in result.stdout.splitlines():
                if "==" in line:
                    lib_name, version = line.split("==", 1)
                    installed_versions[lib_name.lower()] = version
            
            # Update libraries without version specs
            updated_libraries = []
            for lib in libraries:
                # Skip libraries that are python version specifications
                if lib.lower().startswith("python=="):
                    continue
                    
                if "==" not in lib:
                    lib_name = lib.strip()
                    lib_name_lower = lib_name.lower()
                    
                    if lib_name_lower in installed_versions:
                        updated_libraries.append(f"{lib_name}=={installed_versions[lib_name_lower]}")
                    else:
                        updated_libraries.append(lib)
                else:
                    updated_libraries.append(lib)
                    
            return updated_libraries
            
        except subprocess.CalledProcessError as e:
            print(f"Error running pip freeze: {e.stderr}")
            return libraries
        except Exception as e:
            print(f"Error updating library versions: {str(e)}")
            return libraries