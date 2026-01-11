#!/bin/bash

REPO="unclecardboard/plants_the_game"
CHECK_INTERVAL=180  # 3 minutes in seconds
PROJECT_DIR="C:/Users/info.DESKTOP-EAL10AV/OneDrive/Documents/Sam_Plants"

echo "Starting build monitor for $REPO..."
echo "Checking every 3 minutes..."

while true; do
    # Get latest workflow run
    RESPONSE=$(curl -s "https://api.github.com/repos/$REPO/actions/runs?per_page=1")

    # Extract status and conclusion
    STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
    CONCLUSION=$(echo "$RESPONSE" | grep -o '"conclusion":"[^"]*"' | head -1 | cut -d'"' -f4)
    RUN_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

    echo "[$(date)] Status: $STATUS, Conclusion: $CONCLUSION, Run ID: $RUN_ID"

    if [ "$STATUS" = "completed" ] && [ "$CONCLUSION" = "success" ]; then
        echo "✅ Build succeeded! Run ID: $RUN_ID"
        echo "Download APK from: https://github.com/$REPO/actions/runs/$RUN_ID"
        exit 0
    elif [ "$STATUS" = "completed" ] && [ "$CONCLUSION" = "failure" ]; then
        echo "❌ Build failed. Run ID: $RUN_ID"
        echo "View logs at: https://github.com/$REPO/actions/runs/$RUN_ID"

        # Note: Automatic fixes would go here, but require log analysis
        # For now, just alert the user
        echo "Please check the logs manually or provide the error message."
        exit 1
    elif [ "$STATUS" = "in_progress" ] || [ "$STATUS" = "queued" ]; then
        echo "⏳ Build is $STATUS..."
    fi

    sleep $CHECK_INTERVAL
done
