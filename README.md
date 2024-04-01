# Curso 4: Despliegue de modelos de Machine Learning en producción


<img src="https://ci3.googleusercontent.com/mail-sig/AIorK4zt6tOa3204Znd9u8YWMhVnZGy1TWuE7fovhJFzJFvFsfBrTb4F2vc6V99oNs0LODE1jmt1Nqo" width=300>


## Módulo 1: Arquitectura y Diseño de Soluciones (Teórico)

1. Diseño de sistemas de Machine Learning
2. Tipos de Model serving
3. Estrategias de despliegue
4. Ejecución ML pipeline

## Módulo 2: Offline Serving (práctico)

1. Desarrollo soluciones model serving - Batch Scoring ( Batch )
2. Despliegue model serving batch (apache airflow + MLflow)

## Módulo 3: Online Serving (práctico)

1. Desarrollo soluciones model serving - Online
2. Despliegue model serving realtime (FastAPI)
3. Desarrollo soluciones model serving  - Serverless + Event Streaming ( Streaming )
4. Despliegue model serving Streaming (Lambda + Kinesis)

# Herramientas y desarrollo

### Manejo de ambientes y librerias

#### Librerías modelos ML

* `scikit-learn`: librería algoritmos ML
* `hyperopt`: librería de optimización de hiperparametros
* `pandas`: libreria análisis y manipulación de datos
* `joblib`:  librería utilidades machine learning

#### Librerías Software engineering y MLOps

* `pyenv`: administrador de versiones de python en el sistema
* `poetry`: herramienta para administración de dependencias y empaquetamiento en python [Instalación poetry](https://python-poetry.org/docs/#installing-with-the-official-installer). 
* `mlflow`: Herramienta para administración de experimientos y registro de modelos de machine learning. [Documentación MLflow](https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html)
* `airflow`: Orquestación y calendarización de pipelines de machine learning e inferencia en batch para offline serving
* `fastapi`: Librería para creación de APIs en python. se usará para disponibilizar endpoints de modelos de machine learning en online serving
* `dagshub`: Dagshub es una plataforma de colaboración en proyectos con prácticas MLOps, cuenta con integración con Github, DVC, MLflow. Se usará como servidor de MLflow. [Plataforma DagsHub](https://dagshub.com/)

### Software, Frameworks y librerías

* **VS Code**: Editor de código durante el proyecto. [Instalación VS Code](https://code.visualstudio.com/download)
* **Postman/Rapid API**: Aplicaciones para testear APIs, [Instalación extensión VS Code RapidAPI](https://rapidapi.com/products/vs-code-rapidapi-client/) | [Instalación Postman](https://www.postman.com/downloads/)
* **Github + Github actions**: Servidor de Git y pipelines automatizados de DevOps. [Registro Github](https://github.com/) | [Documentación Github Actions](https://docs.github.com/es/actions)
* **Docker + Docker Compose**: Herramienta para ejecución de aplicaciones en contenedores [Instalación docker](https://docs.docker.com/engine/install/) | [Roadmap Docker](https://roadmap.sh/docker)
* **Kubernetes**: Orquestación de contenedores. [Roadmap Kubernetes](https://roadmap.sh/kubernetes)

### Nube + Servicios

El proveedor de nube seleccionado para este curso es Amazon Web Services (AWS)

* **AWS EC2**: Servicio de creación de maquinas virtuales. Se usará para el desarrollo durante el curso. [Amazon Elastic Compute Cloud](https://aws.amazon.com/es/ec2/)
* **AWS EKS**: Servicio de clusteres de Kubernetes. Se usará en el módulo de online serving. [Amazon Elastic Kubernetes Service](https://aws.amazon.com/es/eks/)
* **AWS ECS**: Servicio de contenedores. Se usará en el módulo de online serving.
* **AWS MWAA**: Servicio de Airflow administrado. Se usará en el módulo de offline serving. [Managed Workflows for Apache Airflow](https://aws.amazon.com/es/managed-workflows-for-apache-airflow/)
* **AWS S3**: Servicio de almacenamiento. Se usará en el módulo de offline serving. [Amazon S3](https://aws.amazon.com/es/s3/)
* **AWS Kinesis**: Servicio de procesamiento de mensajes para streaming. Se usará en el módulo de online serving.[Amazon Kinesis](https://aws.amazon.com/es/kinesis/)
* **AWS IAM**: Servicio de administración de permisos y roles

## Configuración de proyecto (ML pipeline)

Para empezar a trabakar en ele proyecto

0. clonar repositorio (Recomendable hacer Fork) - [Forks en Github](https://docs.github.com/es/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

HTTP - [Clonar repositorios en github](https://docs.github.com/es/repositories/creating-and-managing-repositories/cloning-a-repository)

```
git clone https://github.com/abdala9512/dsrp-mlops-deployment.git
```

SSH - [Guía Configuración github con SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

```
git clone git@github.com:abdala9512/dsrp-mlops-deployment.git
```

1. Configuración poetry

```bash
poetry add --dev jupyter-lab black isort flake8
poetry add loguru pandas scikit-learn hyperopt mlflow xgboost
```

O directamente tomar del `poetry.lock`

```
poetry install
```

2. Configuración Github, Dagshub
* Registro Dagshub
* Sincronización repositorio de github
3. Ejecución pipeline ML

```bash
poetry run python main.py
```

#### Resultados ejecución pipeline ML

1. Experimento MLflow
2. Modelo productivo

#### Arquitectura 
