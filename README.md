# EcoTracker
EcoTracker is a web-based carbon footprint calculator that allows you to accurately quantify your carbon footprint, compare it to the carbon footprint of others at your income level, and measure your improvement or regression over time. It offers a logger to document your carbon emissions in real-time and generate statistics to track your emissions. Originally built for Launch Hacks II and continued for around 3 days after it's completion.

## Features
- Accurately quantify your carbon footprint using our carbon footprint calculator.
- Track your carbon emissions in real-time using the logger.
- See your carbon emission statistics and your progression over time.
- Bite-sized assignments to encourage you to maintain lower carbon emissions.
- Task system to walk you through sustainable practices.
- Login and signup system with error handling to save your data.
- Carbon footprint calculator to measure your carbon footprint over a certain course of time based on the main factors. 

## Logger
Use the logger to log your emissions over time. This data will be saved and used to generate statistics. Please note that all inputs that ask about money are based on US dollars. The inputs based on personal information (income and people in the household) are used to generate averages for those in your economic range. All questions are required, so just enter 0 if the question does not apply (ex: if you don't have a diesel vehicle, just enter 0 for all questions that have to do with diesel vehicle milage).

## Tasks
Complete tasks every day to reduce your footprint. Tasks are randomly regenerated daily.

## Statistics
See your carbon emission statistics and your progression over time; most of the statistics are extrapolated out to a year from the original data collection period to keep the comparisons standardized. After more than 7 data entries are added, certain middle entries will be hidden from the graphs so as not to crowd the data. This data is not deleted, and your oldest and most recent entries will always be shown.

## Signup and Login
An error handled login and signup system is included to save your data.

## Running Locally
If you are running this program locally, make sure that you install all of the dependencies (python, flask, sqlite3). If the python file cannot access the database, it is because you do not have the entire directory open.

## License
This project is licensed under the MIT License.
