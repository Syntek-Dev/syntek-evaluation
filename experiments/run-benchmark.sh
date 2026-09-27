#!/usr/bin/env bash

set -euo pipefail

# ============================================================
# Syntek Model Lab — Benchmark Runner
# Machine: AI-01 (override with BENCHMARK_MACHINE_ID)
# Runtime: llama.cpp (llama-server, OpenAI-compatible API)
# ============================================================

BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_DIR="$BASE_DIR/prompts"
RESULT_DIR="$BASE_DIR/results"
OUTPUT_DIR="$RESULT_DIR/outputs"
RESULTS_FILE="$RESULT_DIR/benchmarks.jsonl"

LLAMA_SERVER_URL="${LLAMA_SERVER_URL:-http://127.0.0.1:8080}"
LLAMA_SERVER_URL="${LLAMA_SERVER_URL%/}"

MACHINE_ID="${BENCHMARK_MACHINE_ID:-AI01}"
RUNTIME="llama.cpp"

# ------------------------------------------------------------
# Usage
# ------------------------------------------------------------

usage() {
    echo "Usage:"
    echo "  $0 <model> <domain/prompt-name>"
    echo
    echo "Example:"
    echo "  $0 qwen3-coder-30b-a3b coding/python-production-code-review"
    echo
    echo "Prompt file:"
    echo "  $PROMPT_DIR/<domain/prompt-name>.md"
    echo
    echo "Environment:"
    echo "  LLAMA_SERVER_URL      llama-server base URL (default: http://127.0.0.1:8080)"
    echo "  BENCHMARK_MACHINE_ID  machine recorded in run IDs (default: AI01)"
    exit 1
}

if [[ $# -ne 2 ]]; then
    usage
fi

MODEL="$1"
PROMPT_NAME="$2"
PROMPT_FILE="$PROMPT_DIR/$PROMPT_NAME.md"

# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

if [[ ! -f "$PROMPT_FILE" ]]; then
    echo "ERROR: Prompt file not found:"
    echo "  $PROMPT_FILE"
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is required to read fixture frontmatter."
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: jq is required."
    exit 1
fi

# Parse and validate before contacting llama-server or capturing system telemetry.
# Keep the body in JSON so shell decoding cannot change the model input.
FIXTURE_JSON=$(python3 "$BASE_DIR/populate-benchmarks.py" --read-prompt "$PROMPT_FILE")

# /health returns 200 {"status":"ok"} once the model is loaded, 503 while loading.
if ! HEALTH_JSON=$(curl -fsS "$LLAMA_SERVER_URL/health" 2>/dev/null) ||
    [[ "$(echo "$HEALTH_JSON" | jq -r '.status // empty' 2>/dev/null)" != "ok" ]]; then
    echo "ERROR: llama-server is not ready at:"
    echo "  $LLAMA_SERVER_URL"
    echo "Start it with a model loaded, e.g. llama-server -m <model.gguf> --port 8080"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ------------------------------------------------------------
# Generate experiment ID
# ------------------------------------------------------------

# Find the highest existing automated run number for this machine.
if [[ ! -f "$RESULTS_FILE" ]]; then
    RUN_NUMBER=1
else
    LAST_RUN=$(
        jq -r --arg machine "$MACHINE_ID" '
            select(
                (.id | startswith($machine + "-"))
            )
            | .id
            | split("-")[1]
            | tonumber
        ' "$RESULTS_FILE" 2>/dev/null |
        sort -n |
        tail -1
    )

    if [[ -z "$LAST_RUN" ]]; then
        RUN_NUMBER=1
    else
        RUN_NUMBER=$((LAST_RUN + 1))
    fi
fi

RUN_ID=$(printf "%s-%04d" "$MACHINE_ID" "$RUN_NUMBER")

# ------------------------------------------------------------
# Display run information
# ------------------------------------------------------------

echo
echo "=============================================="
echo " Syntek Model Lab"
echo "=============================================="
echo "Run:       $RUN_ID"
echo "Machine:   $MACHINE_ID"
echo "Runtime:   $RUNTIME"
echo "Server:    $LLAMA_SERVER_URL"
echo "Model:     $MODEL"
echo "Prompt:    $PROMPT_NAME"
echo "=============================================="
echo

# ------------------------------------------------------------
# Runtime information
# ------------------------------------------------------------

PROPS_JSON=$(curl -fsS "$LLAMA_SERVER_URL/props")

RUNTIME_VERSION=$(echo "$PROPS_JSON" | jq -r '.build_info // "unknown"')
SERVER_MODEL_PATH=$(echo "$PROPS_JSON" | jq -r '.model_path // ""')
SERVER_CONTEXT=$(echo "$PROPS_JSON" | jq '.default_generation_settings.n_ctx // null')
SERVER_SLOTS=$(echo "$PROPS_JSON" | jq '.total_slots // null')

# ------------------------------------------------------------
# System telemetry
# ------------------------------------------------------------

capture_system_telemetry() {
    local prefix="$1"
    local GPU_TELEMETRY

    read -r "${prefix}_RAM_TOTAL_BYTES" \
        "${prefix}_RAM_USED_BYTES" \
        "${prefix}_RAM_AVAILABLE_BYTES" < <(
        free -b |
        awk '/^Mem:/ {
            print $2, $3, $7
        }'
    )

    GPU_TELEMETRY=$(
        nvidia-smi \
            --query-gpu=name,memory.total,memory.used,utilization.gpu,temperature.gpu,power.draw \
            --format=csv,noheader,nounits |
        head -n 1
    )

    IFS=',' read -r \
        "${prefix}_GPU_NAME" \
        "${prefix}_GPU_VRAM_TOTAL_MB" \
        "${prefix}_GPU_VRAM_USED_MB" \
        "${prefix}_GPU_UTILISATION_PERCENT" \
        "${prefix}_GPU_TEMPERATURE_C" \
        "${prefix}_GPU_POWER_WATTS" <<< "$GPU_TELEMETRY"

    # Trim whitespace from the CSV fields.
    for var in \
        "${prefix}_GPU_NAME" \
        "${prefix}_GPU_VRAM_TOTAL_MB" \
        "${prefix}_GPU_VRAM_USED_MB" \
        "${prefix}_GPU_UTILISATION_PERCENT" \
        "${prefix}_GPU_TEMPERATURE_C" \
        "${prefix}_GPU_POWER_WATTS"
    do
        printf -v "$var" '%s' "$(printf '%s' "${!var}" | xargs)"
    done
}

# Capture system state before the benchmark
capture_system_telemetry "BEFORE"

# ------------------------------------------------------------
# Run benchmark
# ------------------------------------------------------------

echo "Running benchmark..."
echo

START_TIME_NS=$(date +%s%N)

# One user message, so llama-server applies the model's own chat template.
if ! RESPONSE_JSON=$(
    curl -fsS "$LLAMA_SERVER_URL/v1/chat/completions" \
        -H 'Content-Type: application/json' \
        -d "$(jq -n \
            --arg model "$MODEL" \
            --argjson fixture "$FIXTURE_JSON" \
            '{
                model: $model,
                messages: [
                    {role: "user", content: $fixture.prompt}
                ],
                stream: false
            }')"
); then
    echo "ERROR: llama-server request failed."
    exit 1
fi

END_TIME_NS=$(date +%s%N)

WALL_TIME_NS=$((END_TIME_NS - START_TIME_NS))

# ------------------------------------------------------------
# CPU telemetry
# ------------------------------------------------------------

CPU_MODEL=$(
    lscpu |
    awk -F: '/Model name:/ {
        sub(/^[ \t]+/, "", $2)
        print $2
        exit
    }'
)

CPU_CORES=$(
    lscpu |
    awk -F: '/Core\(s\) per socket:/ {
        gsub(/ /, "", $2)
        print $2
        exit
    }'
)

CPU_THREADS=$(
    lscpu |
    awk -F: '/^CPU\(s\):/ {
        gsub(/ /, "", $2)
        print $2
        exit
    }'
)

# ------------------------------------------------------------
# System telemetry - After
# ------------------------------------------------------------

# Capture system state after the benchmark
capture_system_telemetry "AFTER"

# ------------------------------------------------------------
# Validate response
# ------------------------------------------------------------

if [[ -z "$RESPONSE_JSON" ]]; then
    echo "ERROR: llama-server returned an empty response."
    exit 1
fi

if ! echo "$RESPONSE_JSON" | jq empty >/dev/null 2>&1; then
    echo "ERROR: llama-server returned invalid JSON."
    exit 1
fi

if ! echo "$RESPONSE_JSON" | jq -e '.choices[0].message.content | type == "string"' >/dev/null 2>&1; then
    echo "ERROR: llama-server response has no message content."
    exit 1
fi

# ------------------------------------------------------------
# Extract benchmark metrics
# ------------------------------------------------------------

# usage is the OpenAI-standard token count; timings is llama-server's own
# measurement (absent from other OpenAI-compatible servers, so null there).
# prompt_tokens counts the whole prompt; timings.prompt_n counts only the
# tokens processed this run, and timings.cache_n those reused from the cache.
PROMPT_TOKENS=$(echo "$RESPONSE_JSON" | jq '.usage.prompt_tokens // .timings.prompt_n // 0')
OUTPUT_TOKENS=$(echo "$RESPONSE_JSON" | jq '.usage.completion_tokens // .timings.predicted_n // 0')
PROMPT_PROCESSED_TOKENS=$(echo "$RESPONSE_JSON" | jq '.timings.prompt_n // null')
PROMPT_CACHED_TOKENS=$(echo "$RESPONSE_JSON" | jq '.timings.cache_n // null')

PROMPT_DURATION_NS=$(echo "$RESPONSE_JSON" | jq '
    if .timings.prompt_ms == null then null else (.timings.prompt_ms * 1000000 | round) end
')
OUTPUT_DURATION_NS=$(echo "$RESPONSE_JSON" | jq '
    if .timings.predicted_ms == null then null else (.timings.predicted_ms * 1000000 | round) end
')
TOTAL_DURATION_NS=$(echo "$RESPONSE_JSON" | jq '
    if .timings.prompt_ms == null or .timings.predicted_ms == null then null
    else ((.timings.prompt_ms + .timings.predicted_ms) * 1000000 | round)
    end
')

PROMPT_TPS=$(echo "$RESPONSE_JSON" | jq '.timings.prompt_per_second // null')
OUTPUT_TPS=$(echo "$RESPONSE_JSON" | jq '.timings.predicted_per_second // null')

SERVED_MODEL=$(echo "$RESPONSE_JSON" | jq -r '.model // ""')

TOTAL_SECONDS=$(echo "$TOTAL_DURATION_NS" | awk '$1 == "null" {print "null"; next} {printf "%.3f", $1 / 1000000000}')

WALL_SECONDS=$(echo "$WALL_TIME_NS" | awk '{printf "%.3f", $1 / 1000000000}')

# ------------------------------------------------------------
# Save raw llama-server response
# ------------------------------------------------------------

RAW_OUTPUT_FILE="$OUTPUT_DIR/$RUN_ID.json"

echo "$RESPONSE_JSON" | jq '.' > "$RAW_OUTPUT_FILE"

# ------------------------------------------------------------
# Create benchmark record
# ------------------------------------------------------------

TIMESTAMP=$(date --iso-8601=seconds)

echo "DEBUG:"
echo "  PROMPT_TOKENS=$PROMPT_TOKENS"
echo "  PROMPT_PROCESSED_TOKENS=$PROMPT_PROCESSED_TOKENS"
echo "  PROMPT_CACHED_TOKENS=$PROMPT_CACHED_TOKENS"
echo "  OUTPUT_TOKENS=$OUTPUT_TOKENS"
echo "  PROMPT_DURATION_NS=$PROMPT_DURATION_NS"
echo "  OUTPUT_DURATION_NS=$OUTPUT_DURATION_NS"
echo "  TOTAL_DURATION_NS=$TOTAL_DURATION_NS"
echo "  PROMPT_TPS=$PROMPT_TPS"
echo "  OUTPUT_TPS=$OUTPUT_TPS"
echo "  CPU_CORES=$CPU_CORES"
echo "  CPU_THREADS=$CPU_THREADS"
echo "  BEFORE_RAM_TOTAL_BYTES=$BEFORE_RAM_TOTAL_BYTES"
echo "  BEFORE_RAM_USED_BYTES=$BEFORE_RAM_USED_BYTES"
echo "  BEFORE_RAM_AVAILABLE_BYTES=$BEFORE_RAM_AVAILABLE_BYTES"
echo "  BEFORE_GPU_VRAM_TOTAL_MB=$BEFORE_GPU_VRAM_TOTAL_MB"
echo "  BEFORE_GPU_VRAM_USED_MB=$BEFORE_GPU_VRAM_USED_MB"
echo "  BEFORE_GPU_UTILISATION_PERCENT=$BEFORE_GPU_UTILISATION_PERCENT"
echo "  BEFORE_GPU_TEMPERATURE_C=$BEFORE_GPU_TEMPERATURE_C"
echo "  BEFORE_GPU_POWER_WATTS=$BEFORE_GPU_POWER_WATTS"
echo "  AFTER_RAM_TOTAL_BYTES=$AFTER_RAM_TOTAL_BYTES"
echo "  AFTER_RAM_USED_BYTES=$AFTER_RAM_USED_BYTES"
echo "  AFTER_RAM_AVAILABLE_BYTES=$AFTER_RAM_AVAILABLE_BYTES"
echo "  AFTER_GPU_VRAM_TOTAL_MB=$AFTER_GPU_VRAM_TOTAL_MB"
echo "  AFTER_GPU_VRAM_USED_MB=$AFTER_GPU_VRAM_USED_MB"
echo "  AFTER_GPU_UTILISATION_PERCENT=$AFTER_GPU_UTILISATION_PERCENT"
echo "  AFTER_GPU_TEMPERATURE_C=$AFTER_GPU_TEMPERATURE_C"
echo "  AFTER_GPU_POWER_WATTS=$AFTER_GPU_POWER_WATTS"
echo

BENCHMARK_RECORD=$(jq -n \
    --arg id "$RUN_ID" \
    --arg timestamp "$TIMESTAMP" \
    --arg machine "$MACHINE_ID" \
    --arg runtime "$RUNTIME" \
    --arg runtime_version "$RUNTIME_VERSION" \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT_NAME" \
    --argjson fixture "$FIXTURE_JSON" \
    --arg status "valid" \
    --argjson prompt_tokens "$PROMPT_TOKENS" \
    --argjson prompt_processed_tokens "$PROMPT_PROCESSED_TOKENS" \
    --argjson prompt_cached_tokens "$PROMPT_CACHED_TOKENS" \
    --argjson output_tokens "$OUTPUT_TOKENS" \
    --argjson prompt_duration_ns "$PROMPT_DURATION_NS" \
    --argjson output_duration_ns "$OUTPUT_DURATION_NS" \
    --argjson total_duration_ns "$TOTAL_DURATION_NS" \
    --argjson prompt_tps "$PROMPT_TPS" \
    --argjson output_tps "$OUTPUT_TPS" \
    --argjson total_seconds "$TOTAL_SECONDS" \
    --arg wall_seconds "$WALL_SECONDS" \
    --arg cpu_model "$CPU_MODEL" \
    --argjson cpu_cores "$CPU_CORES" \
    --argjson cpu_threads "$CPU_THREADS" \
    --arg server_url "$LLAMA_SERVER_URL" \
    --arg server_model_path "$SERVER_MODEL_PATH" \
    --arg served_model "$SERVED_MODEL" \
    --argjson server_context "$SERVER_CONTEXT" \
    --argjson server_slots "$SERVER_SLOTS" \
    --argjson before_ram_total_bytes "$BEFORE_RAM_TOTAL_BYTES" \
    --argjson before_ram_used_bytes "$BEFORE_RAM_USED_BYTES" \
    --argjson before_ram_available_bytes "$BEFORE_RAM_AVAILABLE_BYTES" \
    --arg before_gpu_name "$BEFORE_GPU_NAME" \
    --argjson before_gpu_vram_total_mb "$BEFORE_GPU_VRAM_TOTAL_MB" \
    --argjson before_gpu_vram_used_mb "$BEFORE_GPU_VRAM_USED_MB" \
    --argjson before_gpu_utilisation_percent "$BEFORE_GPU_UTILISATION_PERCENT" \
    --argjson before_gpu_temperature_c "$BEFORE_GPU_TEMPERATURE_C" \
    --argjson before_gpu_power_watts "$BEFORE_GPU_POWER_WATTS" \
    --argjson after_ram_total_bytes "$AFTER_RAM_TOTAL_BYTES" \
    --argjson after_ram_used_bytes "$AFTER_RAM_USED_BYTES" \
    --argjson after_ram_available_bytes "$AFTER_RAM_AVAILABLE_BYTES" \
    --arg after_gpu_name "$AFTER_GPU_NAME" \
    --argjson after_gpu_vram_total_mb "$AFTER_GPU_VRAM_TOTAL_MB" \
    --argjson after_gpu_vram_used_mb "$AFTER_GPU_VRAM_USED_MB" \
    --argjson after_gpu_utilisation_percent "$AFTER_GPU_UTILISATION_PERCENT" \
    --argjson after_gpu_temperature_c "$AFTER_GPU_TEMPERATURE_C" \
    --argjson after_gpu_power_watts "$AFTER_GPU_POWER_WATTS" \
    '{
        id: $id,
        timestamp: $timestamp,
        machine: $machine,
        runtime: $runtime,
        runtime_version: $runtime_version,
        model: $model,
        prompt: $prompt,
        fixture_metadata: $fixture.metadata,
        input_sha256: $fixture.input_sha256,
        fixture_sha256: $fixture.fixture_sha256,
        status: $status,
        prompt_tokens: $prompt_tokens,
        prompt_processed_tokens: $prompt_processed_tokens,
        prompt_cached_tokens: $prompt_cached_tokens,
        output_tokens: $output_tokens,
        prompt_duration_ns: $prompt_duration_ns,
        output_duration_ns: $output_duration_ns,
        total_duration_ns: $total_duration_ns,
        prompt_tokens_per_second: $prompt_tps,
        generation_tokens_per_second: $output_tps,
        total_duration_seconds: $total_seconds,
        wall_duration_seconds: ($wall_seconds | tonumber),
        cpu: {
            model: $cpu_model,
            cores: $cpu_cores,
            threads: $cpu_threads
        },
        llama_server: {
            url: $server_url,
            model_path: $server_model_path,
            served_model: $served_model,
            context_tokens: $server_context,
            slots: $server_slots
        },
        system_before: {
            ram: {
                total_bytes: $before_ram_total_bytes,
                used_bytes: $before_ram_used_bytes,
                available_bytes: $before_ram_available_bytes
            },
            gpu: {
                name: $before_gpu_name,
                vram_total_mb: $before_gpu_vram_total_mb,
                vram_used_mb: $before_gpu_vram_used_mb,
                utilisation_percent: $before_gpu_utilisation_percent,
                temperature_c: $before_gpu_temperature_c,
                power_watts: $before_gpu_power_watts
            }
        },
        system_after: {
            ram: {
                total_bytes: $after_ram_total_bytes,
                used_bytes: $after_ram_used_bytes,
                available_bytes: $after_ram_available_bytes
            },
            gpu: {
                name: $after_gpu_name,
                vram_total_mb: $after_gpu_vram_total_mb,
                vram_used_mb: $after_gpu_vram_used_mb,
                utilisation_percent: $after_gpu_utilisation_percent,
                temperature_c: $after_gpu_temperature_c,
                power_watts: $after_gpu_power_watts
            }
        }
    }'
)

# One compact object per line, so the log is real JSON Lines.
echo "$BENCHMARK_RECORD" | jq -c '.' >> "$RESULTS_FILE"

# ------------------------------------------------------------
# Display result
# ------------------------------------------------------------

echo
echo "=============================================="
echo " Benchmark complete"
echo "=============================================="
echo
echo "Run ID:              $RUN_ID"
echo "Model:               $MODEL"
echo "Prompt:              $PROMPT_NAME"
echo "Prompt tokens:       $PROMPT_TOKENS (cached: $PROMPT_CACHED_TOKENS)"
echo "Output tokens:       $OUTPUT_TOKENS"
echo "Prompt tok/s:        $PROMPT_TPS"
echo "Generation tok/s:    $OUTPUT_TPS"
echo "Total duration:      ${TOTAL_SECONDS}s"
echo "Wall duration:       ${WALL_SECONDS}s"
echo
echo "Raw output:"
echo "  $RAW_OUTPUT_FILE"
echo
echo "Benchmark log:"
echo "  $RESULTS_FILE"
echo
