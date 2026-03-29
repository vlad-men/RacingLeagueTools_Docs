# Frequently Asked Questions

!!! tip "Links & Resources"
    *   **Official site:** [racingleaguetools.com](https://racingleaguetools.com/)
    *   **Boosty:** [boosty.to/racingleaguetools](https://boosty.to/racingleaguetools)
    *   **Patreon:** [patreon.com/racingleaguetools](https://www.patreon.com/racingleaguetools)
    *   **Hipolink:** [hipolink.me/sirotkin](https://hipolink.me/sirotkin)

---

## Getting Started

??? question "What is Racing League Tools?"
    *Racing League Tools* (RLT) is a free app that assists admins, managers, and others in managing any level of racing league. The app is based on a local database and provides many handy and useful features. The project was initiated in early 2021 and is currently only supported on Windows 10 (20.04+) and Windows 11 systems.

??? question "How to use the app?"
    It's very simple. Download the archive, then extract it to any folder on your PC and run `RacingLeagueTools.exe`. You will be prompted to create a new database or load an existing one. In most cases, any changes are automatically saved to the database file (found in the `/user/databases/` folder). For faster operations, it is recommended to extract the app on an SSD drive.

??? question "Is Racing League Tools a free app?"
    Yes, it's free, but it's not open-sourced and has some advanced and pro features available only to those who support or supported the project. **All basic functions required for league management are completely free.**

??? question "I started the app for the first time, what do I do next?"
    First of all, add or import your drivers to the database (on **Drivers** tab). Next, by default, you should already have a season created. Add new events to this season's calendar. You will then have access to the session results tables.
    *   *Basics video:* [YouTube](https://www.youtube.com/watch?v=nF6VIkFMsSs)

## Games & Telemetry

??? question "What games / race types are supported?"
    RLT has powerful and flexible functionality for creating custom championships of any complexity. For some games there is support for live timing (UDP telemetry), which allows you to automatically get results from the game and collect additional statistics (F1 series, Assetto Corsa Competizione). Importing session results from JSON and XML files is also supported for Assetto Corsa, ACC, rFactor 2, LMU, and others.

??? question "What is live timing feature presented in the app?"
    In addition to working as normal live timing, it also:
    - Gets results directly from the game and creates a live session in the database.
    - Saves detailed data/statistics for each driver.
    - Allows you to transfer this data to the season.


??? question "How to use the app if the game is running on Playstation or Xbox?"
    1. Find the PC's IP address: **Main menu** -> **Options** -> **Live timing options** -> **Local IP** -> **Show IP**.
    2. Specify this IP in the game settings (**Settings** -> **Telemetry settings** -> **UDP IP address**).
    3. Other options: UDP Broadcast mode is **OFF**, UDP port is the same as in RLT options.

??? question "I see status 'UDP port is busy or blocked by firewall' on the live timing page"
    Check if you are using other apps for UDP telemetry. If RLT is the only app, check your firewall as it often blocks UDP port listening.

??? question "How to use RLT with Simhub or other app (using UDP telemetry) in parallel?"
    Enable UDP forwarding:
    - **Options** -> **Live timing** -> **UDP forwarding**.
    - Click **Add forward target**.
    - Specify UDP port and IP address.
    - In Simhub, specify the same UDP port.
    - Restart RLT.

??? question "What is UDP dump?"
    A UDP dump is a file containing copies of UDP telemetry packets received during a live session. You can later "replay" the session (**Main menu** -> **Database** -> **Replay session from UDP dump**). Dumps are stored in `/user/udp_dump/` and old files are automatically deleted to save space.

??? question "Why aren't the results of the live session transferred to the season?"
    The most important thing is the track/circuit set for the live session. If a matching track isn't found (based on "Circuit name" and "UniqueID"), it shows "unknown track" and cannot transfer results. The app also looks for the first matching event in the current season with a matching track and considers the dates.

## Points & Scoring

??? question "Does the app calculate points automatically?"
    Yes, the app does this ***completely automatically***. First, the classification position is calculated (influenced by driver status, time/gap, penalties), then points are assigned to drivers and teams based on the point system.

??? question "How to edit points for a specific driver?"
    - **Session results page:** Double-click on `PtsD` or `PtsT` field. Manually set values are highlighted in white. To return control to the app, set it to `-1`.
    - **Standings page:** Use the **User corrections** column. These act as an offset to points already earned.

??? question "I need my own complicated point scoring system"
    Navigate to **Point system** page. Here you can set points for actions (classification, fastest lap, driver of the day) for each race/qual type. Note: point system links to the championship, not the season.

??? question "How do I change the number of points for a race fastest lap?"
    Navigate to **Point system** page, select your race type and scroll to the **Fastest lap** action.

??? question "What is the difference between 'Minor' and 'Major' race types?"
    - **Major:** *Main*, *Feature*, *Regular*.
    - **Minor:** All others (e.g., Sprints).
    This is important for statistics and the penalty system. You can toggle **Minor types equals major types** on the **Point system** page.

??? question "I want to run a preseason race without point scoring?"
    - **Whole event:** Calendar -> Right-click -> **Change status** -> **Change to non-championship event**.
    - **Single race/qual:** Results page -> Command bar -> Change **Full points** to **No points**.

??? question "I need to score half points for the race?"
    Session/results page -> Command bar -> Change **Full points** to **Half points**.

## Database & Management

??? question "How to add a new track if it is missing? (e.g. China)"
    Go to **Championships** page, select the championship and press **Edit** on the **Tracks** column. Check the necessary track. If it's missing, try deleting the `/user/startup_data/` folder and restarting. Alternatively, add it manually on the **Tracks** page.

??? question "How to add a new team, car, vendor, etc?"
    The process is the same as adding a new track.

??? question "How to delete/archive driver & what is the difference?"
    Drivers cannot be deleted if they have session results. Instead, move them to the **archive** (**Drivers** page -> Right-click -> **Move to archive**). Archived drivers are hidden from most places, including renders. You can toggle their display using filters.

??? question "Why can't I edit the results of all the season's events at the beginning?"
    Events are ordered by date and have statuses: *completed*, *skipped*, or *in future*. You can only edit the session results of the **first** event with the status **In Future**.

??? question "How do I specify the drivers in the results?"
    Just click on any letter's keyboard in the driver field.

??? question "Why is the session not considered completed?"
    It is necessary to specify at least the drivers for 1st, 2nd, and 3rd positions.

??? question "What does 'Fix results' button do?"
    It fixes results and runs classification/points processing. This is also done automatically when rendering, updating standings, or restarting the app.

??? question "My database is corrupt or I deleted something important. How do I recover?"
    The app automatically backups the database each time it runs. You can find backup files in the `/user/backups/` folder.

## Themes & Rendering

??? question "What is render/rendering?"
    The app can generate ready-made images. This is termed *rendering*.

??? question "Where are the pictures saved after rendering?"
    By default, in `/user/render_images/`. This can be changed in render options. Images are also copied to the Windows clipboard.

??? question "I want my league logo to appear on render images"
    Navigate to **League setting** page and load your logo.

??? question "How do I order teams in the line-ups list?"
    Change the **Position** property of the team on the **Teams** page.

??? question "Why do I see the time of the event in GMT format?"
    You can change the time format (including local time) in the season settings: **Season list** -> Right-click -> **Edit** -> **Additional options**.

??? question "I have heard that some themes allow changing localization and additional options?"
    **Main menu** -> **Themes** -> **Options** button near the selected theme.

??? question "Can I add the image of the driver's avatar/photo and use it in my theme?"
    Yes. Put the image into `/user/images/driver_avatars/` folder. Filename must match the name of the driver. You can use the `LogoPath` property of `DriverRenderObject` in JSON code.

## Troubleshooting

??? question "What to do with the error 'could not find part of path...' or 'access denied'?"
    Most likely your antivirus is blocking access. Add the app to exceptions. If that fails, try changing the render folder (**Main menu** -> **Options** -> **Rendering** -> **Render folder**) to a location on a different disk.


## Live Timing & Telemetry

??? question "I see status 'UDP port is busy or blocked by firewall' on live timing page"
    Check other apps that may use the UDP port. If the app is single, verify firewall settings — firewall often blocks UDP.

??? question "How to use app if the game is on Playstation or Xbox?"
    1.  Find IP of the PC where Racing League Tools is running: **Main menu** -> **Options** -> **Live timing** -> **Local IP** -> **Show IP**.
    2.  Specify this IP in the console game's telemetry settings (UDP settings).
    3.  Set **UDP Broadcast mode** to **OFF**; use same UDP port as in RLT options.


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
