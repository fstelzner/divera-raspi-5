#!/bin/sh

ACCESSKEY="[DEIN DIVERA-API KEY]"
API_URL="https://www.divera247.com/api/last-alarm?accesskey=${ACCESSKEY}"
IS_MONITOR_ACTIVE=true
STIME=20

while true; do
    HAS_ALARM=`curl -s ${API_URL} | jq -r -j '.success'`

      if [ $HAS_ALARM = true ]; then
        echo "Turn display on"
        WAYLAND_DISPLAY="wayland-1" wlr-randr --output HDMI-A-1 --on
        IS_MONITOR_ACTIVE=true
    elif [ $HAS_ALARM = false ] && [ $IS_MONITOR_ACTIVE = true ]; then
        echo "Turn display off"
        WAYLAND_DISPLAY="wayland-1" wlr-randr --output HDMI-A-1 --off
        IS_MONITOR_ACTIVE=false
    fi

    echo "sleeping for $STIME seconds"
    sleep $STIME
    echo "done"
done
