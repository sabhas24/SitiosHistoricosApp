from enum import Enum


class Permisos(Enum):
    USER_INDEX = "user_index"
    USER_SHOW = "user_show"
    USER_NEW = "user_new"
    USER_UPDATE = "user_update"
    USER_DESTROY = "user_destroy"
    USER_BLOCK = "user_block"
    SITE_INDEX = "site_index"
    SITE_NEW = "site_new"
    SITE_SHOW = "site_show"
    SITE_UPDATE = "site_update"
    SITE_DESTROY = "site_destroy"
    SITE_EXPORT = "site_export"
    SITE_SET_VISIBILITY = "site_set_visibility"
    SITE_HISTORY = "site_history"
    TAG_INDEX = "tag_index"
    TAG_NEW = "tag_new"
    TAG_UPDATE = "tag_update"
    TAG_DESTROY = "tag_destroy"
    PROPOSAL_INDEX = "proposal_index"
    PROPOSAL_VALIDATE = "proposal_validate"
    REVIEW_INDEX = "review_index"
    REVIEW_MODERATE = "review_moderate"
    REVIEW_DESTROY = "review_destroy"
    FEATURE_FLAGS = "feature_flags"
    REPORT_VIEW = "report_view"
    SITE_VIEW = "site_view"
    REVIEW_CREATE = "review_create"
    FAVORITE_MANAGE = "favorite_manage"


_VALUES = {p.value for p in Permisos}


def permiso_valido(nombre: str) -> bool:
    return nombre in _VALUES


def todos_los_permisos() -> list[str]:
    return list(_VALUES)
