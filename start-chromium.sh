#!/bin/bash
chromium-browser --start-maximized --kiosk --incognito --user-data-dir=/home/pi/.config/chromium2 --enable-features=OverlayScrollbar,OverlayScrollbarFlashAfterAnyScrollUpdate,OverlayScrollbarFlashWhenMouseEnter --app=https://app.divera247.com/monitor/1.html?autologin=[DEINE-DIVERA-AUTOLOGIN-ID] &
