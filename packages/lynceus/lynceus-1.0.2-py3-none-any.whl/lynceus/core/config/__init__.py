# Defines various constants.
from pathlib import Path
from typing import Any

# * Date/time format
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
DATETIME_FORMAT_SHORT = "%Y-%m-%d"

# * Internals constants (avoiding circular import).
LYNCEUS_S3_CONFIG_KEY: str = 'lynceus_s3_config'

# * Configuration instance
CONFIG_GENERAL_KEY: str = 'General'

# Constants definition for 'Processing' configuration level: where any process can store information // used by jobs to share info.
CONFIG_PROCESS_KEY: str = 'Processing'
CONFIG_RUN_EXECUTION_ID: str = 'execution_id'

CONFIG_PROJECT_REPO_ANALYSE_DIR: str = 'uncompress_repo_directory'



CONFIG_PROCESS_REPO_ALL_FILE: str = 'interesting_files_list'
CONFIG_PROCESS_REPO_FILE_COUNT: str = 'interesting_files_count'

CONFIG_PROCESS_REPO_LINES_COUNT: str = 'interesting_lines_count'



# => Important: update this map each time a new statistic is added (which is very rare).
# The key is the statistic KEY, and the value is the optional transformation function.
CONFIG_PROCESS_ALL_STATISTICS_MAP: dict[str, Any] = {







}

# Constants definition for 'Storage' configuration level: where user can configure some directory to work into (like temporary root directory).
CONFIG_STORAGE_KEY: str = 'StorageConfiguration'


CONFIG_STORAGE_REMOTE_TYPE: str = 'storage_type'
CONFIG_STORAGE_LOCAL: str = 'Local'

CONFIG_STORAGE_IS_DYNAMIC: str = 'is_dynamic'
CONFIG_STORAGE_DYNAMIC_TYPE: str = 'dynamic_type'
CONFIG_STORAGE_REMOTE_AVAILABLE: str = 'available_remote_storages'
CONFIG_STORAGE_REMOTE_CONF_FILE: str = 'remote_storages_conf'


# Lynceus client (API, CLI ...) related config.
#  * configuration option
CONFIG_JSON_DUMP_KEY_END_KEYWORD: str = '_json_dump'
CONFIG_AUTHENTICATION_KEY: str = 'Authentication'







CONFIG_USER_ID: str = 'user_id'
CONFIG_PARTICIPANT_EMAIL: str = 'participant_email'
CONFIG_SCORE_PARTICIPANT: str = 'score_participant'

#   - other parameters required for dynamic storage
CONFIG_PROJECT_DYNAMIC_STORAGE_H_INSTANCE_ID: str = 'instance_id'
CONFIG_PROJECT_DYNAMIC_STORAGE_H_ORGANIZATION_ID: str = 'organization_id'
CONFIG_PROJECT_DYNAMIC_STORAGE_H_ACTIVITY_ID: str = 'activity_id'
CONFIG_PROJECT_DYNAMIC_STORAGE_H_GROUP_ID: str = 'group_id'
#   - defines which dynamic storage are mandatory or not.
CONFIG_PROJECT_DYNAMIC_STORAGE_MANDATORY_PARAM_MAP: dict[str, bool] = {
    CONFIG_PROJECT_DYNAMIC_STORAGE_H_INSTANCE_ID: True,
    CONFIG_PROJECT_DYNAMIC_STORAGE_H_ORGANIZATION_ID: True,
    CONFIG_PROJECT_DYNAMIC_STORAGE_H_ACTIVITY_ID: True,
    CONFIG_PROJECT_DYNAMIC_STORAGE_H_GROUP_ID: True,
    CONFIG_USER_ID: False
}





#   - other parameters related to logging
CONFIG_LOG_MESSAGE_STATUS_KEY: str = 'message_status'

#  * various constants







# Constants definition for 'Jobs' configuration level: configuration of jobs.
CONFIG_JOBS_KEY: str = 'Jobs'
CONFIG_JOBS_DISABLED_LIST: str = 'disabled_job_list'




# Constants definition for 'Project' configuration level: configuration of project to analyze.
CONFIG_PROJECT_KEY: str = 'Project'
CONFIG_PROJECT_URI: str = 'uri'








CONFIG_PROJECT_CRED_SECRET: str = 'credential_secret'
CONFIG_PROJECT_CRED_SECRET_GITLAB_DEFAULT: str = 'gitlab_default_credential_secret'
CONFIG_PROJECT_CRED_SECRET_GITHUB_DEFAULT: str = 'github_default_credential_secret'




CONFIG_PROJECT_ROOT_PATH_HOLDER: str = '<PROJECT_ROOT_PATH>'

# Constants definition for 'Project profile metadata' configuration level: project profile metadata.









# * Job metadata definition.
# Job metadata keys.


# Job categories.








# * Scoring metadata definition.




# * Various configuration
# Constants definition for structure meta.











# CONFIG_STRUCTURE_CHECK_ALL_VALUES constant is interesting for Lynceus API to automatically remove any possible message prefix
#  when creating message with status.

                                                
                                                
                                                

GOOD_BAD_STRING: dict[bool, str] = {
    
    
    
}

FOUND_OR_NOT_STRING: dict[bool, str] = {
    
    
}

# * Compute Resources related constants.
ACCESS_PERMISSION_RO: str = 'RO'
ACCESS_PERMISSION_RW: str = 'RW'
ACCESS_PERMISSION_RWD: str = 'RWD'

# Keyword used when creating some computing resources.
CREATED_OBJECT_NAME_KEYWORD: str = 'aitraining'

