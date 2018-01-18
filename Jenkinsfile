pipeline {
  agent any
  stages {
    stage('Coverage') {
      parallel {
        stage('Coverage') {
          steps {
            sh '''export PATH="/usr/local/bin:$PATH"
$WORKSPACE/make_coverage.sh'''
          }
        }
        stage('Static analysis') {
          steps {
            sh '''export PATH="/usr/local/bin:$PATH"
touch ~/.pylintrc
pylint $WORKSPACE/src -r n -s n -j 8 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > report.bat
'''
          }
        }
      }
    }
  }
}