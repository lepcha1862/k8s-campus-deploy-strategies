
#!/bin/sh

# Purpose: Summarise Campus Notice Board availability logs.
# Usage: sh scripts/summarise.sh <monitor-log-file>
# Input: ISO-8601 timestamp, OK/FAIL, response body or error.

set -eu

# Require exactly one log filename.
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <monitor-log-file>" >&2
    exit 2
fi

# Verify that the log file can be read.
if [ ! -r "$1" ]; then
    echo "Error: Cannot read log file: $1" >&2
    exit 1
fi

# Analyse individual monitoring records.
awk '
$2 == "OK" || $2 == "FAIL" {

    total++

    # Record the first and last request timestamps.
    if (total == 1) {
        first = $1
    }

    last = $1

    # Count unsuccessful requests.
    if ($2 == "FAIL") {
        failures++
    }

    # Extract the version from successful JSON responses.
    if ($2 == "OK" &&
        match($0, /"version"[[:space:]]*:[[:space:]]*"/)) {

        version = substr($0, RSTART + RLENGTH)
        sub(/".*/, "", version)

        versions[version]++
    }
}

END {
    print "===== Availability Monitor Summary ====="

    printf "Total requests: %d\n", total
    printf "Failed requests: %d\n", failures

    if (total > 0) {
        print "First timestamp: " first
        print "Last timestamp:  " last
    } else {
        print "First timestamp: N/A"
        print "Last timestamp:  N/A"
    }

    print "Responses per version:"

    count = 0

    for (version in versions) {
        printf "  %s: %d\n", version, versions[version]
        count++
    }

    if (count == 0) {
        print "  None"
    }

    print "========================================"
}
' "$1"
