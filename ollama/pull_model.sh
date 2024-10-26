
./bin/ollama serve &

pid=$!

sleep 5

echo "Pulling Alibaba qwen2.5:1.5b 0.5 B model"
ollama pull qwen2.5:1.5b

wait $pid
