pipeline {
  agent any
  stages {
    stage('Coverage') {
      steps {
        sh '''export PATH="/usr/local/bin:$PATH"
$WORKSPACE/make_coverage.sh'''
      }
    }
  }
}