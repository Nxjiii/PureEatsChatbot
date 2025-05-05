 #!/bin/bash
PORT="${PORT:-8080}"
echo "Starting Rasa server on port $PORT"
rasa run --model /app/models --enable-api --cors "*" --port $PORT --host 0.0.0.0
