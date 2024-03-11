# Blixyr
Simple Interpreted Language made in Python

# Installation
Windows:
1. Download ```Blixyr.pyz``` and ```install.cmd```
2. Double click ```install.cmd```
3. OPTIONAL: Press the WIN key on your keyboard, then type "Edit environment variables for your account" and press enter
4. OPTIONAL: Click on the PATH variable, click edit, then add a new one with the path to the Blixyr.pyz file (usually located in %LOCALAPPDATA%/Blixyr

Other Operating Systems:
1. Download ```Blixyr.pyz```
2. Run ```Blixyr.pyz```

# Shell
Blixyr comes with a built in shell that has two features that aren't in normal Blixyr.

run: You can run files using the run command in the format "run <filename>.bx"
exit: Exit the shell

# Documentation
## Main Syntax Rules
### Strings
String literals can be represented with " or '

### Booleans
You can have ```true``` or ```false```

### Numbers
Decimals are not supported yet so just integers

### Functions
You can call a function with identifier();

If you are making a function, you still need to include a semicolon at the end of the statement.

ex. func main() {};

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
print(name);
```

### Input
There are two forms of input: input, and getch

Input takes user input until it encounters a new line, while getch takes one character and doesn't wait for a newline.
```
print('What is your name?\n>');
input name;
print("Your name is ");
println(name);

getch;
```

### Valid Types
There are multiple types.

Strings, booleans, bytes, numbers, functions.  You can use to_string and to_bytes to convert bytes to strings, and strings to bytes.

Usage:
```
print('Press any key: ');
getch key;
to_string key;

print('\nYou pressed: ');
println(key);
```

### Functions
You can make a function by using the func keyword.

Usage:
```
func sayHello() {
  println("Hello");
};
```

## Standard Library
You can import modules by using the ```import``` keyword.

Usage:
```
import stdio;

func main() {
  println("Hello, World!");
};
```

- stdio
  print(string); (Prints a string to the console)
  println(string); (Prints a string to the console and prints a newline as well)

- conutil
  clear(); (Clears the console)
  flush(); (Flushes the output buffer)

- python
  exec(string); (Executes Python code)

- thread
  wait(number); (Pauses execution by seconds)

## Features coming soon
- Improved Scope System
- If Statements
- Loops
- Returning Values from Functions
- Math

## Putting it all together
Most languages either have a specific starting point like ```int main();``` in C style languages, or just starting with the first line. 

In Blixyr, you get the option of having a starting point or not.  If you choose to have a starting function then it must be named `main`

You can create a test program with all the shown features with the following code:

```
import stdio;
import conutil;
import thread;
import python;

func main() {
  getName(getNameMSG);

  anyKey();
};

func getName() {
  print(args);
  input name;

  wait(1);

  print(sayName);
  println(name);
};

func anyKey() {
  print(anyKeyMSG);
  flush();
  getch;
  println();
};

var sayName = "Your name is ";
var getNameMSG = "What is your name?\n> ";
var anyKeyMSG = "Press any key to continue...";
```
