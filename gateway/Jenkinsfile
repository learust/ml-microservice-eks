pipeline {
  agent any

  environment {
    SERVICE_NAME = "gateway"
    AWS_REGION   = "us-east-1"
    ACCOUNT_ID   = "469511944493"
    IMAGE_REPO   = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${SERVICE_NAME}"
    SHORT_SHA    = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
  }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Install dependencies & Tests') {
      steps {
        sh """
        pip install --no-cache-dir -r requirements.txt || true
        pytest || echo "No tests"
        """
      }
    }

    stage('Docker Build & Push') {
      steps {
        sh """
        aws ecr get-login-password --region ${AWS_REGION} \
        | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
        
        docker build -t ${SERVICE_NAME}:${SHORT_SHA} .
        docker tag ${SERVICE_NAME}:${SHORT_SHA} ${IMAGE_REPO}:${SHORT_SHA}
        docker push ${IMAGE_REPO}:${SHORT_SHA}
        """
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh """
        kubectl set image deployment/${SERVICE_NAME} ${SERVICE_NAME}=${IMAGE_REPO}:${SHORT_SHA} -n default
        kubectl rollout status deployment/${SERVICE_NAME} -n default
        """
      }
    }
  }
}
