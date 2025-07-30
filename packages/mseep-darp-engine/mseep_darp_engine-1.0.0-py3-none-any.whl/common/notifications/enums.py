from enum import StrEnum


class NotificationEvent(StrEnum):
    email_confirmation = "email-confirmation"
    deploy_failed = "server-deploy-failed"
    deploy_successful = "server-success-deploy"
    server_healthcheck_failed = "server-healthcheck-failed"
