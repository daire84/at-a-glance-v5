# Data Templates

This directory contains sample data structures for the Film Production Scheduler.

## Usage

1. Copy these files to your actual `data/` directory
2. Modify the sample data to match your project needs
3. The application will create additional files as needed

## Structure

- `departments.json` - Global department definitions
- `locations.json` - Global location database  
- `areas.json` - Location area groupings
- `projects/[project-id]/` - Project-specific data
  - `main.json` - Project metadata
  - `holidays.json` - Bank holidays for this project
  - `weekends.json` - Working weekend definitions
  - `hiatus.json` - Production hiatus periods
  - `calendar.json` - Generated calendar data (created automatically)
  - `versions.json` - Version history (created automatically)
  - `workspace.json` - Current workspace (created automatically)

## Security Note

The actual `data/` directory should never be committed to version control as it may contain sensitive production information.
