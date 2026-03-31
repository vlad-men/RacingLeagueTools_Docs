# Sessions

Some hints related to sessions and the session results page.

## Calendar — managing sessions

You can easily add and remove different sessions for an event on the **Calendar** page:

![Add remove sessions](images/1257142062642364487_20260331_112246_image.png)

Here you can also change the status of any event to non-championship:

![Non-championship status](images/1257142127402553364_20260331_112245_image.png)

Non-championship status means that all sessions within that event are not processed for standings and statistics.

## Results page

When typing any letter in the driver field, the app searches for matches in driver names, real names, and in-game names:

![Driver search](images/1257142233531027565_20260331_112244_image.png)

It's very easy to enter a time/gap value:

![Time input](images/1257142323150585856_20260331_112243_image.png)

...which converts to:

![Time converted](images/1257142367257886792_20260331_112242_image.png)

Just try it.

## Classification position

It is not necessary to enter all information — just drivers, teams, and statuses.
The key field in session results is the **classification position**:

![Classification position](images/1257143170085552158_20260331_112241_image.png)

It is calculated **automatically**. Its value depends directly on the times and gaps.
The following are also taken into account:

- DNF, DSQ status
- PTS (penalty time from stewards)
- PPS (penalty positions from stewards)

PTG (penalty time from the game) and PPG (penalty positions from the game) are **not** taken into account — it is assumed that they are already accounted for by the game.

PP (penalty points) is only needed for the season's statistics.

**If you want to remove penalty time issued by the game, just enter a negative value in the PTS field:**

![Negative PTS](images/1257143559749111949_20260331_112240_image.png)

The app uses a pretty advanced classification position processor, so try to manage results using PTS and PPS.

## Sessions management

Try to fill results into events *consistently*:

![Consistent results entry](images/1257143898476908706_20260331_112239_image.png)

Completing qualifying and practice results is **not** as important as completing **race results**.
You can skip sessions if necessary:

![Skip sessions](images/1257144285396992043_20260331_112238_image.png)

## Fix results button

You don't always have to click the "Fix results" button:

!["Fix results" button](images/1257144400606138388_20260331_112237_image.png)

It is only needed to update the UI and standings within the app. When you press **Render**, fix results happen automatically.

## Session type

The type of session is important for the calculation of points and statistics:

![Session type](images/1257144628902236202_20260331_112237_image.png)

You can change it at any time.

## Qualification format

You can also change to full format or short format at any time for a qualification session:

![Qualification format switch](images/1257145124585082972_20260331_112235_image.png)

For the full qualification format, a separate virtual session is created with the combined results of all segments:

![Combined Q session](images/1257145188154085489_20260331_112235_image.png)

However, it is not necessary to select the "Combined Q" tab to render combined results.
You can simply click the **Render results** button while on any qualification tab.
If you want to render a specific segment, find the appropriate button in the render drop-down menu:

![Render drop-down menu](images/1257145294462914621_20260331_112233_image.png)

For faster rendering, use the main menu:

![Main menu render](images/1257145363551490180_20260331_112232_image.png)

## Adding new drivers in results

If you need to enter a new driver in the session results, you can immediately create a new driver:

![Create new driver inline](images/1257145437635346432_20260331_112232_image.png)

Enter the driver's name and press **Enter**. The driver will be created and selected.
To easily add or remove a driver's penalty, use the context menu:

![Penalty context menu](images/1257145525451489310_20260331_112231_image.png)

## Tyre stints

To edit tyre stints, open `app_config.json` and add the following line, then restart the app:

```
"IsEnableTyreStintsManualEdit": true
```
