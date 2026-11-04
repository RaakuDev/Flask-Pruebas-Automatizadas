
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

        stage('Analyze') {
            steps {
                echo 'Analizando código con SonarQube...'

                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube-Local') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        
       
        stage('Security Test') {
            steps {
                echo 'Analizando dependencias con OWASP Dependency-Check...'

                sh 'mkdir -p dependency-check-report'

                dependencyCheck(
                    odcInstallation: 'DependencyCheck',
                    additionalArguments: '--scan requirements.txt --format HTML --format XML --out dependency-check-report'
                )

                dependencyCheckPublisher(
                    pattern: 'dependency-check-report/dependency-check-report.xml'
                )

                archiveArtifacts(
                    artifacts: 'dependency-check-report/*.html',
                    allowEmptyArchive: true
                )
            }
        }


    }

    post {
        success {
            echo 'Build, Test y Analyze completados correctamente.'
        }

        failure {
            echo 'El pipeline presentó un error.'
        }
    }
}
