# Blixyr
Simple Interpreted Language made in Python

# Installation
Unzip the Blixyr.zip file, and run install.cmd

install.cmd moves the Blixyr file to your local appdata folder, and sets environment variables to easily keep track of where the files are held.

NOTE: If you are not on Windows, just unzip Blixyr.zip and run Blixyr.pyz directly.

# Shell
Blixyr comes with a built in shell that has two features that aren't in normal Blixyr.

run: You can run files using the run command in the format "run <filename>.bx"
exit: Exit the shell

# Documentation
## Main Syntax Rules
- String literals use '' or ""
- Lines must end with a semicolon (;)

## Escape Character
The escape character (\) can be used within a string to have different value.  Here are the following escape sequences you can use:
- \n (Newline)
- \\ (Regular backslash)
- \' (Single quote)
- \" (Double quote

## Variables
To create a variable you use the 'var' keyword
```
var myVariable = "Hello, World!";
```

You can access variables when printing data like the following:
```
var name = 'Hello, World!';
println name;
```

## Console IO
### Output
You can print text to the console in two ways.  println, and print.

```
print "Hello, World!";
println "Hello, World!";
print "Goodbye!";
```

Output:
Hello, World!Hello, World!
Goodbye!

### Input
There are two forms of input: input, and getch

Input takes user input until it encounters a new line, while getch takes one character and doesn't wait for a newline.
```
print 'What is your name?\n>';
input name;
print "Your name is ";
println name;

getch;
```

### Valid Types
There are currently only two types of variables.  Strings, and Bytes.  You can turn a bytes object into a string by using to_str but not the other way around.

Usage:
```
print 'Press any key: ';
getch key;
to_str key;

print '\nYou pressed: ';
println key;
```
