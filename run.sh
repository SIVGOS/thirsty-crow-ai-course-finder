#!/bin/bash

# Load .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi


# Function to check and kill a process by name
kill_process() {
    local process_name=$1
    pids=$(pgrep -f "$process_name")
    
    if [ -n "$pids" ]; then
        echo "Killing process: $process_name"
        for pid in $pids; do
            echo "Killing PID: $pid"
            pkill -TERM -P $pid  # Kill child processes
            kill -9 $pid         # Kill main process
        done
    else
        echo "No running process found for: $process_name"
    fi
}

# Function to check if a service is running on a given host and port
check_service() {
    local service_name=$1
    local host=$2
    local port=$3
    if ! nc -z $host $port; then
        echo "Error: $service_name is not running on $host:$port. Please start it and try again."
        exit 1
    fi
}

# Parse arguments
terminate_only=false
developer_mode=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --terminate|-t) terminate_only=true ;;
        --dev|-d) developer_mode=true;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check and kill Celery worker process
kill_process "celery -A course_master worker"

# Check and kill Django runserver process
kill_process "manage.py runserver"

# If terminate_only flag is set, exit the script after killing the processes
if [ "$terminate_only" = true ]; then
    echo "Termination mode: Processes have been killed. Exiting without restarting."
    exit 0
fi

# Check if PostgreSQL and Redis are running
check_service "PostgreSQL" $DB_HOST $DB_PORT
check_service "Redis" $REDIS_HOST $REDIS_PORT

# Delete older logs if exists
if [ -f nohup_celery.out ]; then
    rm nohup_celery.out
fi

PYTHON_PATH=python3

if [ -f env/bin/python ]; then
    PYTHON_PATH="env/bin/python"
fi

# Start the Celery worker process
nohup $PYTHON_PATH -m celery -A course_master worker > nohup_celery.out 2>&1 &

if [ "$developer_mode" == true ]; then
    echo "Celery workers ran successfully in background."
    # Start the Django runserver process on console
    $PYTHON_PATH manage.py runserver
else
    # Start the Django runserver process in background
    # First delete older log if exists
    if [ -f nohup_django.out ]; then
        rm nohup_django.out
    fi
    nohup $PYTHON_PATH manage.py runserver > nohup_django.out 2>&1 &
    echo "Processes restarted successfully."
fi
