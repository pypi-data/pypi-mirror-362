#!/bin/bash
# Generate all documentation plots for Rekha in parallel

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🎨 Rekha Documentation Plot Generator${NC}"
echo "======================================"

# Output directory
OUTPUT_DIR="$SCRIPT_DIR/../docs/_static/plots"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo -e "${YELLOW}📁 Output directory: $OUTPUT_DIR${NC}"
echo

# Option to clean existing plots
if [ "$1" = "--clean" ] || [ "$1" = "-c" ]; then
    echo -e "${YELLOW}🧹 Cleaning existing plots...${NC}"
    rm -f "$OUTPUT_DIR"/*.png
    echo -e "${GREEN}✅ Cleaned${NC}"
    echo
fi

# Change to project root
cd "$SCRIPT_DIR/.." || exit 1

# Set PYTHONPATH to include the project root
export PYTHONPATH="$SCRIPT_DIR/..:$PYTHONPATH"

# Create a temporary directory for job tracking
TEMP_DIR=$(mktemp -d)
JOBS_DIR="$TEMP_DIR/jobs"
mkdir -p "$JOBS_DIR"

# Cleanup function
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Number of parallel jobs (adjust based on CPU cores)
PARALLEL_JOBS=8

# Function to run a script
run_script() {
    local script=$1
    local job_id=$2
    local script_name=$(basename "$script")
    
    # Create a unique output file for this job
    local output_file="$JOBS_DIR/$job_id.out"
    local status_file="$JOBS_DIR/$job_id.status"
    
    # Run the script and capture output
    if python "$script" --output "$OUTPUT_DIR" --mode both > "$output_file" 2>&1; then
        echo "SUCCESS" > "$status_file"
        echo -e "${GREEN}✅ $script_name${NC}"
    else
        echo "FAILED" > "$status_file"
        echo -e "${RED}❌ $script_name${NC}"
        cat "$output_file"
    fi
}

# Export functions and variables for parallel execution
export -f run_script
export OUTPUT_DIR JOBS_DIR GREEN RED NC

# Collect all scripts
ALL_SCRIPTS=()

echo -e "${BLUE}📋 Collecting scripts...${NC}"

# Quickstart examples
for script in examples/quickstart/*.py; do
    if [ -f "$script" ] && [ "$(basename "$script")" != "__init__.py" ]; then
        ALL_SCRIPTS+=("$script")
    fi
done

# Plot type examples
for plot_type in bar box cdf heatmap histogram line scatter; do
    for script in examples/plots/$plot_type/*.py; do
        if [ -f "$script" ]; then
            ALL_SCRIPTS+=("$script")
        fi
    done
done

# Advanced feature examples
for script in examples/advanced/*.py; do
    if [ -f "$script" ]; then
        ALL_SCRIPTS+=("$script")
    fi
done

total_scripts=${#ALL_SCRIPTS[@]}
echo -e "${YELLOW}Found $total_scripts scripts to run${NC}"
echo

# Run scripts in parallel
echo -e "${BLUE}🚀 Running scripts in parallel (max $PARALLEL_JOBS jobs)...${NC}"

# Use GNU parallel if available, otherwise fall back to xargs
if command -v parallel &> /dev/null && parallel --help &> /dev/null; then
    # Use GNU parallel (without progress in CI environments)
    if [ -t 1 ]; then
        # Terminal available, show progress
        printf '%s\n' "${ALL_SCRIPTS[@]}" | \
            parallel -j $PARALLEL_JOBS --progress \
            "run_script {} {#}"
    else
        # No terminal (CI environment), no progress
        printf '%s\n' "${ALL_SCRIPTS[@]}" | \
            parallel -j $PARALLEL_JOBS \
            "run_script {} {#}"
    fi
else
    # Use xargs as fallback
    echo -e "${YELLOW}Using xargs fallback (parallel not available)${NC}"
    job_id=0
    for script in "${ALL_SCRIPTS[@]}"; do
        ((job_id++))
        echo "$script $job_id"
    done | xargs -P $PARALLEL_JOBS -n 2 bash -c 'run_script "$0" "$1"' || {
        echo -e "${RED}xargs failed, falling back to sequential execution${NC}"
        # Sequential fallback
        job_id=0
        for script in "${ALL_SCRIPTS[@]}"; do
            ((job_id++))
            run_script "$script" "$job_id"
        done
    }
fi

# Wait for all jobs to complete
wait

# Count successes and failures
successful_scripts=0
failed_scripts=0

for status_file in "$JOBS_DIR"/*.status; do
    if [ -f "$status_file" ]; then
        if grep -q "SUCCESS" "$status_file"; then
            ((successful_scripts++))
        else
            ((failed_scripts++))
        fi
    fi
done

# Summary
echo
echo -e "${BLUE}📊 Summary${NC}"
echo "=================================="
echo -e "${GREEN}✅ Successfully ran: $successful_scripts/$total_scripts scripts${NC}"
if [ $failed_scripts -gt 0 ]; then
    echo -e "${RED}❌ Failed: $failed_scripts scripts${NC}"
fi
echo -e "${YELLOW}📁 Output directory: $OUTPUT_DIR${NC}"

# List generated files
if [ -d "$OUTPUT_DIR" ]; then
    echo
    echo -e "${BLUE}📄 Generated files:${NC}"
    png_count=$(ls -1 "$OUTPUT_DIR"/*.png 2>/dev/null | wc -l)
    echo "Total PNG files: $png_count"
fi

if [ $failed_scripts -gt 0 ]; then
    echo
    echo -e "${RED}⚠️  Some scripts failed. Check the errors above.${NC}"
    exit 1
fi

echo -e "${GREEN}✨ All plots generated successfully!${NC}"