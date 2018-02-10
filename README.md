# LendingClub Default Rate Visualization

##### https://mshadish.github.io/lendingclub/

Scala project + Python scripts to support visualization of default rates and other distressed loans over time

## Data Acquisition

Use Scala and LendingClub API to pull latest note data and store in a local SQLite database

## Data Transformation

Use Python to transform note data to provide daily summaries of outstanding notes

## Data Visualization

Currently using Python to visualize note default rates as a stacked line chart. Future work will revolve around turning this into a stacked area chart, possibly plotted using D3.js

## Future Work

##### 1) Convert the bar chart of note grades to a stacked bar chart to show default rates broken down by grade

##### 2) Clean up visualization
