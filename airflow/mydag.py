from airflow import DAG 
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
# 1. Add this import to define resources correctly
from kubernetes.client import models as k8s

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 27),
    'retries': 1,
}

transaction_volume = k8s.V1Volume(
    name="shared-files",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="my-files-claim"
    )
)

transaction_mount = k8s.V1VolumeMount(
    name="shared-files",
    mount_path="/app/ft"
)

extract_volume = k8s.V1Volume(
    name="extracted-files",
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
        claim_name="ext-claim"
    )
)

extract_mount = k8s.V1VolumeMount(
    name="extracted-files",
    mount_path="/app/extracted"
)

with DAG(
    'trans-ext',
    default_args=default_args,
    schedule=None,    
    catchup=False,
    tags=['transaction', 'extraction'],
) as dag:
    extract_task = KubernetesPodOperator(
        task_id="extract",
        name="extract-pod",
        namespace="default",
        image="airflow-extract:v1",

        volumes=[extract_volume],
        volume_mounts=[extract_mount],

        env_from=[
            k8s.V1EnvFromSource(
                secret_ref=k8s.V1SecretEnvSource(name="my-secret")
            )
        ],
        
        container_resources=k8s.V1ResourceRequirements(
            requests={
                "memory": "64Mi",
                "cpu": "100m"
            },
            limits={
                "memory": "128Mi",
                "cpu": "200m"
            }
        ),
        
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
    )

    transaction_task = KubernetesPodOperator(
        task_id="transaction",
        name="transaction-pod",
        namespace="default",
        image="airflow-transaction:v1",

        volumes=[transaction_volume],
        volume_mounts=[transaction_mount],

        env_from=[
            k8s.V1EnvFromSource(
                secret_ref=k8s.V1SecretEnvSource(name="my-secret")
            )
        ],

        container_resources=k8s.V1ResourceRequirements(
            requests={
                "memory": "64Mi",
                "cpu": "100m"
            },
            limits={
                "memory": "128Mi",
                "cpu": "200m"
            }
        ),
        
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
    )

# Task dependency
transaction_task >> extract_task