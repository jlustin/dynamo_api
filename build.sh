function build_db() {
    docker build -t dynamodb ./dynamo_db
}

function start_db() {
    docker-compose up -d dynamodb
}

function teardown() {
    docker-compose down
}

[ "$#" -ne 1 ] && echo "no command specified"
case "${1}" in
    build_db)
        build_db || echo "failed to build db"
        ;;
    start_db)
        start_db || echo "failed to start db"
        ;;
    teardown)
        teardown || echo "failed to stop containers"
        ;;
    *)
        echo "command not supported"
        ;;
esac