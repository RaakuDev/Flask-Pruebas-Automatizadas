
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Preparando entorno virtual de Flask...'
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                sh '.venv/bin/python -m unittest discover -v'
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
