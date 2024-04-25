# Program for tracking progress in exercises

Data is written and stored in sqlite3 via peewee.
The user can:
1. Create/edit/delete exercises
2. Set/change/delete a goal for any exercise
3. Record the exercise and results for the day
4. Request progress statistics

Statistics are displayed using matplotlib, with bar charts showing results for each day. Days where the result exceeds the goal are highlighted in a different color.

The output is presented in a visually appealing format using tabulate and colorama for enhanced readability.
