from enum import Enum


class WorkspaceGitSyncSettingsRepositoriesItemExcludeTypesOverrideItem(str, Enum):
    APP = "app"
    FLOW = "flow"
    FOLDER = "folder"
    GROUP = "group"
    RESOURCE = "resource"
    RESOURCETYPE = "resourcetype"
    SCHEDULE = "schedule"
    SCRIPT = "script"
    SECRET = "secret"
    TRIGGER = "trigger"
    USER = "user"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
