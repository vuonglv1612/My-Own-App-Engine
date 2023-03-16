import logging
import uuid

import logging_loki

from config import settings
from dependencies import celery_app_factory, create_redis_client
from functions import push, create_remote_image
from provisioner import TsuruProvisioner
from use_cases.build_from_git import build_from_git

provisioner = TsuruProvisioner(tsuru_api_url=settings.tsuru_api, username=settings.tsuru_username,
                               password=settings.tsuru_password)
celery_app = celery_app_factory()


@celery_app.task(name="deploy_git_app")
def deploy_git_app_task(deployment_id: str, app_name: str, git_url: str, git_branch: str, plan_name: str,
                        replicas: int = 1):
    task_id = str(uuid.uuid4().hex)
    handler = logging_loki.LokiHandler(
        url=settings.loki_url,
        tags={"app": app_name, "deployment_id": deployment_id},
        version="1",
    )
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(task_id)
    logger.handlers = []
    logger.addHandler(handler)
    redis_client = create_redis_client()
    image_name = f"{app_name}"
    full_image_name = f"{app_name}:{deployment_id}"
    remote_name = create_remote_image(full_image_name, settings.registry, settings.registry_namespace)
    folder = settings.build_folder + f"/{app_name}"
    redis_client.set(f"{deployment_id}:status", "building")
    result = build_from_git(url=git_url, branch=git_branch, folder=folder, image_name=image_name,
                            image_tag=deployment_id,
                            builder="heroku/buildpacks:20")
    build_success = None
    for log in result:
        if isinstance(log, bool):
            build_success = log
            break
        logger.info(log)

    if build_success:
        redis_client.set(f"{deployment_id}:status", "build_succeeded")
    else:
        redis_client.set(f"{deployment_id}:status", "build_failed")

    redis_client.set(f"{deployment_id}:status", "deploying")
    logger.info("Pushing image to registry...")
    push_logs = push(full_image_name, registry=settings.registry, username=settings.registry_username,
                     password=settings.registry_password, namespace=settings.registry_namespace)
    for log in push_logs:
        logger.info(log)
    logger.info("Pushing image to registry...done")
    logger.info("Deploying app...")
    deploy_logs = provisioner.deploy_app(app_name=app_name, image=remote_name)
    for log in deploy_logs:
        logger.info(log)
    logger.info("Deploying app...done")
    redis_client.set(f"{deployment_id}:status", "deployed")

    return build_success


@celery_app.task(name="deploy_image_app")
def deploy_image_app_task(deployment_id: str, app_name: str, image: str, plan_name: str,
                          replicas: int = 1):
    task_id = str(uuid.uuid4().hex)
    handler = logging_loki.LokiHandler(
        url=settings.loki_url,
        tags={"app": app_name, "deployment_id": deployment_id},
        version="1",
    )
    logger = logging.getLogger(task_id)
    logger.handlers = []
    logger.addHandler(handler)
    redis_client = create_redis_client()
    redis_client.set(f"{deployment_id}:status", "deploying")
    logger.info("Deploying app...")
    full_image = f"{image}"
    deploy_logs = provisioner.deploy_app(app_name=app_name, image=full_image)
    for log in deploy_logs:
        logger.info(log)
    logger.info("Deploying app...done")
    redis_client.set(f"{deployment_id}:status", "deployed")


@celery_app.task(name="scale_app")
def scale_app_task(app_name: str, change: int):
    task_id = str(uuid.uuid4().hex)
    if change == 0:
        return
    handler = logging_loki.LokiHandler(
        url=settings.loki_url,
        tags={"app": app_name},
        version="1",
    )
    logger = logging.getLogger(task_id)
    logger.addHandler(handler)
    logger.info("Scaling app...")
    if change < 0:
        scale_log = provisioner.scale_down_app(app_name=app_name, down=abs(change))
    else:
        scale_log = provisioner.scale_up_app(app_name=app_name, up=abs(change))
    for log in scale_log:
        logger.info(log)
    logger.info("Scaling app...done")


@celery_app.task(name="stop_app")
def stop_app_task(app_name: str):
    task_id = str(uuid.uuid4().hex)
    handler = logging_loki.LokiHandler(
        url=settings.loki_url,
        tags={"app": app_name},
        version="1",
    )
    logger = logging.getLogger(task_id)
    logger.addHandler(handler)
    logger.info("Stop app...")
    stop_logs = provisioner.stop_app(app_name=app_name)
    for log in stop_logs:
        logger.info(log)
    logger.info("Stop app...done")


@celery_app.task(name="restart_app")
def restart_app_task(app_name: str):
    task_id = str(uuid.uuid4().hex)
    handler = logging_loki.LokiHandler(
        url=settings.loki_url,
        tags={"app": app_name},
        version="1",
    )
    logger = logging.getLogger(task_id)
    logger.addHandler(handler)
    logger.info("Restart app...")
    restart_logs = provisioner.restart_app(app_name=app_name)
    for log in restart_logs:
        logger.info(log)
    logger.info("Restart app...done")
