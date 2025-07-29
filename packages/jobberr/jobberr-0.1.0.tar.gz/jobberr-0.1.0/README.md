# Jobber 

A lightweight command-line tool to list and run Python files within directories.

## Usage

```bash
jobber <command> <directory>
```
Commands:
- list: Recursively lists all subdirectories and files starting from <directory>.
- run: Executes all Python files directly inside <directory>.
> Note: run does not traverse into subdirectories.

```python
# List contents of the current directory
jobber list .

# List contents of the directory A
jobber list A

# Run Python files in the directory A
jobber run A

# Run Python files in the subdirectory A/D
jobber run .\A\D\
```


