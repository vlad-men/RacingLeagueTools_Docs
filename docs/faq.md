# Frequently Asked Questions

!!! tip "Links & Resources"
    *   **Official site:** [racingleaguetools.com](https://racingleaguetools.com/)
    *   **Download:** [Racedepartment](https://www.overtake.gg/downloads/racing-league-tools.61644/)
    *   **Community:** Check our Discord (Boosty, Patreon) and YouTube playlist for tutorials.

---

## General & Licensing

??? question "Is Racing League Tools a free app?"
    Yes — all basic features are free. Some advanced/pro features require support/donation.
    See Discord channel `<#960444187403231262>` for details.

??? question "I started the app for the first time, what do I do next?"
    1.  Add or import drivers (**Drivers** tab).
    2.  Ensure a season exists; add events to the calendar.
    3.  Watch video tutorials and helpful links provided in the resources section.

## Points & Scoring

??? question "Does the app calculate points automatically?"
    Yes, the app calculates points automatically based on the configured system; you can also change driver points manually.

??? question "How to edit points for a driver?"
    *   **On session results:** Double-click on the `PtsD` or `PtsT` field to manually edit.
    *   **On standings:** Double-click on the `Add/remove pts` field for offsets.

??? question "How to increase grid size / number of positions?"
    Go to **Seasons** page -> Right-click on season -> **Edit** -> **Additional options** -> **Grid size**.

??? question "What is the difference between Minor and Major race types?"
    *   **Major:** Main, Feature, Regular races.
    *   **Minor:** Sprint, Heat, Qualification races.
    
    This distinction is useful for statistics filtering and penalty application.

??? question "How to change points for the fastest lap?"
    On the **Point system** page, select the specific race type and modify the **Fastest lap** value.

??? question "I need my own complicated point scoring system"
    Go to the **Point system** page; set points presets for each action for every race/qual type.
    
    > Note: The point system is linked to the Championship entity, not the specific Season.

## Database & Management

??? question "How to delete or archive a driver?"
    You cannot delete a driver if they are present in the DB (to keep integrity). You can move a driver to the archive:
    
    1.  Go to **Drivers** page.
    2.  Right-click -> **Move to archive**.
    
    Use filters to show/hide archive drivers.

??? question "How to add a new team/car/vendor?"
    See "How to add a new track" below (the process is similar).

??? question "How to add a new track/circuit? (track missing)"
    1.  Go to **Championships** page, select season -> **Edit**.
    2.  In the **Circuits** column, check the necessary track.
    
    If not found:
    *   Delete `/user/startup_data/` and restart the app.
    *   Or add it manually through the **Circuits** page.

??? question "Can I add a driver avatar/photo and use it in a theme?"
    Yes. Put the image into the `/user/images/driver_avatars/` folder.
    
    > **Important:** Filename must match the driver name exactly.

??? question "How to add a new country and flag?"
    Navigate to **Countries** -> **Add new...** -> put PNG into `/images/flags/` folder (filename = country name).

??? question "How can I add team/car/vendor logos?"
    See Discord channel `<#991611637285011537>`.

## Themes & Rendering

??? question "Can I change localization/advanced theme options?"
    **Main menu** -> **Themes** -> **Options** on the selected theme.

??? question "Where are pictures saved after rendering?"
    By default: `/user/render_images/`.
    
    It can be changed in the render options. The image is also copied to the clipboard after rendering.

??? question "What is render/rendering?"
    Rendering is the feature that generates ready-made images. There are themes; you can edit them or create new themes.

??? question "Why is the time of the event shown in GMT?"
    Change time format in the season settings (**Season list** -> Right click -> **Edit** -> **Additional options**).

??? question "How do I order teams in the line-ups list?"
    Change the **Position** property of the team on the **Teams** page.

??? question "I want my league logo to appear on render images"
    Load league logo at **League settings** page (click settings icon at bottom left of main window) and upload your logo.

## Live Timing & Telemetry

??? question "I see status 'UDP port is busy or blocked by firewall' on live timing page"
    Check other apps that may use the UDP port. If the app is single, verify firewall settings — firewall often blocks UDP.

??? question "How to use app if the game is on Playstation or Xbox?"
    1.  Find IP of the PC where Racing League Tools is running: **Main menu** -> **Options** -> **Live timing** -> **Local IP** -> **Show IP**.
    2.  Specify this IP in the console game's telemetry settings (UDP settings).
    3.  Set **UDP Broadcast mode** to **OFF**; use same UDP port as in RLT options.

??? question "How to use live timing and get results from the game?"
    See details and instructions in `<#1257145918482808902>`.

??? question "What is live timing feature presented in the app?"
    It works as real-time live timing, plus:
    *   Receives results from the game and creates live sessions in the database.
    *   Saves detailed per-driver data/statistics.
    *   Allows transferring these data to the current season.

??? question "What is UDP dump?"
    UDP dump is a file on disk which contains copies of processed UDP telemetry packets received during the live session. Later you can "replay" the session in the app (**Main menu** -> **Database** -> **Replay session from UDP dump**).
    
    By default this option is off; turn it on in the live timing options. UDP dumps are stored in `/user/udp_dump/`. Old files are automatically deleted when the limit is exceeded.

??? question "Why aren't the results of the live session transferred to the season?"
    The most important thing is the **track/circuit** set for the live session. This is determined automatically depending on the telemetry info (tracks unique ID/name).
    
    1.  If a matching track is not found in the database at the time the telemetry is received, you will see "unknown track" and will not be able to transfer the results to the season.
    2.  If track is ok, the app will look for the first matching event in the current season with a matching track.
    3.  The date set for the event and the actual date of the telemetry results are also important for automatic transfer.

??? question "How to use Racing League Tools with Simhub or other app (using UDP telemetry) in parallel?"
    Just enable UDP forwarding:
    1.  Open **Options** window -> **Live timing** -> **UDP forwarding**.
    2.  Click **Add forward target**.
    3.  Specify UDP port and IP address (optionally).
    4.  In Simhub (or other app) specify the same UDP port.
    5.  Restart Racing League Tools.

## Troubleshooting

??? question "My database is corrupt or I deleted something important. How do I recover?"
    The app automatically backups the database each time it runs. You can find backup files in the `/user/backups/` folder.

??? question "I got an error, who can help me?"
    Create a post in `<#962950236207202305>`.
    
    **Don't forget to attach:**
    *   Your database file (`/user/databases/`)c:\Projects\racing_league_tools\icons\app\rlt_logo_v2_220.png
    *   The `errors.log` file (`/logs/`)

??? question "What to do with the error 'could not find part of path...' or 'access denied'?"
    Edit app_config.jsonfile by adding the line"IsEnableTyreStintsManualEdit": true and restart the app.
