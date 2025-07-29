import sys
import sqlite3
import argparse
import time
import json


def query_lines(lines, query, use_headers, return_results: bool = False):
    # Set up an in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE logs (i int, line TEXT);")

    # Insert log lines into the table
    cursor.executemany("INSERT INTO logs (i, line) VALUES (?, ?);", [(i + 1, l) for i, l in enumerate(lines)])

    # Execute the SQL query
    try:
        if query.startswith('path:'):
            with open(query[len('path:'):], 'r') as f:
                query = f.read()

        if query.strip('\n').strip().lower().startswith('where'):
            query = f"SELECT * FROM logs {query}"

        cursor.execute(query)
        results = cursor.fetchall()

        if return_results:
            headers = [f'{d[0]}' for d in cursor.description]
            results = [[f'{v}' for v in row] for row in results]
            return (headers, results) if use_headers else results

        if use_headers:
            print(', '.join([f'{d[0]}' for d in cursor.description]))  # Print column names

        for row in results:
            print(', '.join([f'{v}' for v in row]))  # Print matching lines
    except sqlite3.Error as e:
        print(f"SQL Error: {e}", file=sys.stderr)

    # Close the connection
    conn.close()


def display_version():
    print('Query Search version 0.0.1')


def main():
    parser = argparse.ArgumentParser(description="Query text files using SQL")
    parser.add_argument('-c', '--headers', default=False, action=argparse.BooleanOptionalAction, help='Whether to include Headers (Column Names) or not')
    parser.add_argument('-f', '--folder', default=None, help='Search Through a folder')
    parser.add_argument('-d', '--delimiter', default='\n', help='The char or text used to split "lines" or sections')
    parser.add_argument("query", help="SQL query to execute (use 'line' as column name). To use a file, type 'path:/path/to/file.sql'")
    parser.add_argument("file", nargs="?", type=argparse.FileType("r"), default=sys.stdin, help="Log file to read (default: stdin)")
    args = parser.parse_args()

    if not isinstance(args.delimiter, str):
        args.delimiter = '\n'
    delimiter = args.delimiter.replace('\\n', '\n').replace('\\t', '\t')  # '\n'
    if delimiter != '\n':
        print(f'delimiter: {json.dumps(delimiter)}')

    # Read input (from file or stdin)
    if args.folder:
        import os
        for root, dirs, files in os.walk(args.folder):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    try:
                        lines = [line.strip('\n') for line in f.read().strip('\n').split(delimiter)]
                    except UnicodeDecodeError:
                        continue
                    if args.headers:
                        hs, rs = query_lines(lines, args.query, args.headers, return_results=True)
                        if rs:
                            print(f'\n\nFile: {file} | {os.path.join(root, file)}')
                            print(', '.join(hs))
                            for r in rs:
                                print(', '.join(r))
                    else:
                        rs = query_lines(lines, args.query, args.headers, return_results=True)
                        if rs:
                            print(f'\n\nFile: {file} | {os.path.join(root, file)}')
                            for r in rs:
                                print(', '.join(r))
                time.sleep(0.1)
        return
    lines = [line.strip('\n') for line in args.file.read().strip('\n').split(delimiter)]

    query_lines(lines, args.query, args.headers)


if __name__ == "__main__":
    main()


