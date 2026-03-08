# Convenience Store
A simple project which uses Python to build, generate and extract data for a MySQL database of a small convenience store

---
## Prerequisites
* Python (version 3.x recommended)
* MySQL Server
* Required Python packages. You can install them using pip:
    ```bash
    pip install mysql-connector-python
    pip install Faker
    ```

---
## Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DoubleHo05/Convenience-Store
    ```

2.  **Set up the MySQL Database:**
    * Ensure your MySQL server is running.
    * Connect to your MySQL server. You can use the command line or a GUI tool.
    * Execute the `my_store.sql` script to create the database and tables:
        ```bash
        mysql -u your_username -p < mysql/my_store.sql
        ```
        *(Remember to replace `your_username` with your actual username)*
3.  **Configure Database Connection:**
    * You need to update the database connection details (host, user, password, database name) within the Python scripts (`create_data.py`, `extract.py`, `transaction.py`). Look for connection parameters in these files and adjust them to your environment.
    * For example, in `create_data.py`, you can change them to
        ```
        DB_HOST = "localhost"
        DB_USER = "root"
        DB_PASSWORD = "<your_password>"
        DB_NAME = "my_store"
        ```


---
## Usage

### `data.csv`
This file contains seed data.

### `create_data.py`
This script is used to take data from `data.csv` and add to the database.
* **To run:**
    ```bash
    python script/create_data.py
    ```

### `transaction.py`
This script create transaction data.
* **To run:**
    ```bash
    python script/transaction.py
    ```

### `extract.py`
This script is used to extract data from the database to csv files and put into folder `extracted`.
* **To run:**
    ```bash
    python script/extract.py
    ```

---
## Test the project with Docker
This project can also run using Docker. This simplifies setup and ensures a consistent environment.

### Prerequisites
* [Docker](https://www.docker.com/get-started) installed on your system.
* [Docker Compose](https://docs.docker.com/compose/install/) installed on your system.

### Set up
* Clone the repository:
    ```bash
    git clone https://github.com/DoubleHo05/Convenience-Store
* Create `.env`, which provides the environment variables for `docker-compose.yaml`, in the root directory of the project.
    ```
    MYSQL_ROOT_PASSWORD=<your_root_password>
    MYSQL_USER=<your_user>
    MYSQL_PASSWORD=<password_for_user>
    MYSQL_DATABASE=my_store
    PORT=3306
    ```

### Running with Docker Compose
1. Navigate to the project root directory.
2. Run this in terminal
    ```bash
    docker compose up -d
    ```
3. Folder `extracted` will be created in the root directory and CSV files which contains data from database are put there. 


---
## Bring the project to Kubernetes with Airflow
We can also run the project with a Kubernetes cluster running in containers with k3d.

### Prerequisites
* [Docker](https://www.docker.com/get-started)
* [k3d](https://github.com/k3d-io/k3d#get)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Helm](https://helm.sh/)

### Set up
1. Clone the repository:
    ```bash
    git clone https://github.com/DoubleHo05/Convenience-Store
    ```
2. Add Airflow repository to Helm and fetch the latest chart information:
    ```bash
    helm repo add apache-airflow https://airflow.apache.org
    helm repo update
    ```

### Run the project
1. Navigate to the root directory of the project.

2. **Run this in terminal**:
    ```bash
    k3d cluster create -a 2
    ```
    This will create a cluster with 2 agent nodes, each node is actually a container.

3. You need to create k8s/secret.yaml file base on this template:
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
    name: my-secret
    type: Opaque
    data:
    MYSQL_HOST: YOUR-MYSQL-HOST
    MYSQL_ROOT_PASSWORD: YOUR-MYSQL-ROOT-PASSWORD
    MYSQL_USER: YOUR-MYSQL-USER
    MYSQL_PASSWORD: YOUR-MYSQL-USER-PASSWORD
    MYSQL_DATABASE: YOUR-MYSQL-DATABASE
    PORT: YOUR-MYSQL-PORT (usually 3306)
    ```

    **Run this to create objects**:
    ```bash
    kubectl apply -f k8s/secret.yaml
    kubectl apply -f k8s/extractVolume.yaml
    kubectl apply -f k8s/filesVolume.yaml
    kubectl apply -f k8s/mysql.yaml
    kubectl apply -f k8s/create.yaml
    ```
4. Since we have 2 PersistentVolumes and both of them are located with the path /tmp/kube in 2 agent nodes, so we must create that directory in 2 agent nodes.

    **Run this in terminal:**
    ```bash
    docker exec -it k3d-k3s-default-agent-0 sh
    ```

    **then**:
    ```bash
    mkdir -p tmp/kube
    ```

    Repeat the same with k3d-k3s-default-agent-1.

5. Deploy Airflow using Helm.

    **Run this:**
    ```bash
    helm install airflow apache-airflow/airflow --values airflow/values.yaml
    ```

6. Port forward to use the UI to trigger the DAG
    ```bash
    kubectl port-forward svc/airflow-api-server 8080:8080 --namespace default
    ```
8. Go to localhost:8080 on browser, login using your username and password, then you can trigger the dag manually.

9. When the DAG finishes, you can see the extracted files are in the path /tmp/kube of k3d-k3s-default-agent-1 container.