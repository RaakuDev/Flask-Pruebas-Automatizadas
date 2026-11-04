
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Preparando aplicación Flask...'
                sh 'python3 -m pip install --user -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                sh 'python3 -m unittest discover -v'
            }
        }
    }

    post {
        success {
            echo 'Build y Test completados correctamente.'
        }

        failure {
            echo 'El pipeline presentó un error.'
        }
    }
}
