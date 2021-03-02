# dream
A concatenative programming language

This is an unfinished project. 

In its current state, it is just a single Python file that you can run with 'python dream.py'. This starts a REPL. 
Run it with 'python dream.py <filename>' to run a Dream script before entering the REPL.
  
  

Dream is a stack based language, where values are left on the stack after executing each statement. The value of the stack is printed after each executed statement, which allows the user to constantly see the changes they make. 
  
  
An example demonstrating some things you can do in Dream:

**:** with **;** defines a new word, in the Forth style:
```
>>> : square copy * ;
square: ['copy', '*']
[]
>>> : even? 2 % 0 = ;
even?: [2, '%', 0, '=']
[]
```
**define** does the same thing as **:**, but in a postfix style:
```
>>> [copy *] 'square define
```

**set** stores a value in a variable:
```
>>> 300 'a set
```

 
**range** creates a list of numbers in a range
```
>>> 1 20 range
[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]
```

**map** appends a list of items onto each element of another list and parses the result to return a new list
```
>>> [copy *] map
[[1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361]]
```
you could also write it like this, using our previously defined word **square**
```
>>> 'square map
[[1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361]]
```

**filter** compares each item of a list against a condition and returns a new list of items for which the condition is true. Here we use our previously defined word **even?** to filter our list for even numbers.
```
>>> 'even? filter
[[4, 16, 36, 64, 100, 144, 196, 256, 324]]
```

**reduce** appends a list of items to two elements at a time of another list, parsing the result at each step. Here we reduce our list of values using the list [+], effectively giving us the sum of the list.
```
>>> '+ reduce 
[[1140]]
```

**.** flattens a list by one level
```
>>> .
[1140]
```

------------------

Very basic flow control with **if/else/then**
```
>>> 3 2 > if "yup" else "nah" then print
yup
```
