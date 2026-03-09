#!/bin/bash
#========================================
# Model Variant Tests for CCM
#========================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CCM="$SCRIPT_DIR/../ccm.sh"

echo "=== Testing Alibaba Cloud Coding Plan ==="

# Test ali:qwen
echo -n "ali qwen: "
eval "$($CCM ali qwen china 2>/dev/null)"
echo "$ANTHROPIC_MODEL"

# Test ali:kimi
echo -n "ali kimi: "
eval "$($CCM ali kimi global 2>/dev/null)"
echo "$ANTHROPIC_MODEL"

# Test ali:glm
echo -n "ali glm: "
eval "$($CCM ali glm china 2>/dev/null)"
echo "$ANTHROPIC_MODEL"

# Test ali:minimax
echo -n "ali minimax: "
eval "$($CCM ali minimax china 2>/dev/null)"
echo "$ANTHROPIC_MODEL"

# Test default (no variant)
echo -n "ali (default): "
$CCM ali china 2>&1 | grep ANTHROPIC_MODEL | head -1

# Test error handling
echo ""
echo "=== Error Handling ==="
echo -n "invalid variant: "
$CCM ali invalid china 2>&1 | head -2

# Test backward compat (qwen as alias)
echo ""
echo "=== Backward Compatibility ==="
echo -n "qwen (alias): "
$CCM qwen china 2>&1 | grep ANTHROPIC_MODEL | head -1

echo ""
echo "=== All tests completed ==="
