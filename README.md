# Mass-RMV-Selenium-Script

Selenium script for getting a last minute appointment at the Massachusetts Registry of Motor Vehicles.


MA RMV is appointment only and appointments are released sporadically throughout the day (eg due to cancellations).

This script continuously searches all/some (toggle nearby_only) RMV offices for a license transfer appointment in October.

An appointment is not actually booked. The script will just beep and print out the options, leaving a window open on the selection page. Ten second wait between checks; there's no acceptable use policy or robots.txt on the website so choosing an excessively good-citizeny wait time.
