if [ "$1" = "1" ]; then
    echo "python3 receive_logs_topic.py '#'"
    python3 receive_logs_topic.py "#"
elif [ "$1" = "2" ]; then
    echo "python3 receive_logs_topic.py 'kern.*' '*.critical'"
    python3 receive_logs_topic.py "kern.*" "*.critical"
fi