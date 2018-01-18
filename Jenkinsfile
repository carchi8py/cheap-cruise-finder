pipeline {
  agent any
  stages {
    stage('Coverage') {
      steps {
        sh '$WORKSPACE/make_coverage.sh'
      }
    }
  }
}