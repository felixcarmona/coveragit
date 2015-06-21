coveragit
=========

coveragit is a tool to check the uncovered code lines which have been modified or added in an specific pull request or commit.

Usage
-----
```
usage: coveragit [-h] [--base BASE] [--concise] [--xml XML] [--silently]

Check the uncovered code lines which have been modified or added in an specific pull request or commit

optional arguments:
  -h, --help            show this help message and exit
  --base BASE, -b BASE  Base branch, tag, commit, or history marker to compare the current revision
  --concise, -c         Only display the affected uncovered lines
  --xml XML, -x XML     Path of the generated coverage .xml
  --silently, -s        Even with missing coverage, exit with success system exit status
```

Demo
----
![alt tag](https://raw.githubusercontent.com/felixcarmona/coveragit/master/screenshot.png)