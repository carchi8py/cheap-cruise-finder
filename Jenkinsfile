pipeline {
  agent any
  stages {
    stage('Coverage') {
      steps {
        sh '''echo $PATH
$WORKSPACE/make_coverage.sh'''
      }
    }
  }
}