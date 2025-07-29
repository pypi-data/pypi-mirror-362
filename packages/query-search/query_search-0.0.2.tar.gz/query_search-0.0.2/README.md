## Terminal Query Search

This package lets you query files, folders or pipe outputs(like `grep`) using SQL syntax

This uses python's `sqlite3` module for querying

### Table of Contents
- [Installation](#installation) <!-- - [Quick Start](#quick-start) -->
- [Learn by Example](#learn-by-example) 
- [Table Structure](#table-structure)
- [License](#license)

### Installation

`pip install query-search`

### Learn by Example

```shell
cat file.txt | qq "where lower(line) like '%daniel%'"
# or
echo hello | qq "select line from logs"
# or
echo hello | qq path:/path/to/some.sql
# or
qq "where line like 'id: %'" /path/to/my.txt
# or 
qq "select 'Line: ' || i as line_index, line from logs where line like 'id: %'" /path/to/my.txt
# or 
qq path:/path/to/some.sql /path/to/my.txt
# or
qq --folder /path/to/folder "where line like '%important%'"
# or
qq --folder /path/to/folder path:/path/to/some.sql
```

### Table Structure

`CREATE TABLE logs (i int, line TEXT);`

`i` Is the line index starting at `1`.

`line` is the read stripped line (`line.strip('\n')`)

<!--
### Replace Tool

A `qq replace` command was added because I often find myself 
wanting to replace a string like `#some_value = 'on'` to `some_value = 'off'`.

##### Example Usage

File Content:
```text
Hi kitty
```
Usage: `cat file.txt | qq replace "Hi" "Bye"`

Console Output:
```text
Bye kitty
```


*Note: if you are replacing a config file you may need to output into a temporary file as shell redirection truncates the output file before reading the input file. e.g.*
```bash
cat /etc/.../postgresql.conf | qq replace "#key = val" "key = val2" > ./postgresql.conf; cat ./postgresql.conf > /etc/.../postgresql.conf;rm ./postgresql.conf
```
-->
### License
* MIT License