# Package `foo` 

#### Function `foo.package_function` 







<details><summary>Source</summary>

```python
@dock
def package_function():
    ...

```

</details>

### Class `foo.PackageClass`
#### Function `foo.PackageClass.__init__` 







<details><summary>Source</summary>

```python
@dock
def __init__(self):
    ...

```

</details>

#### Function `foo.PackageClass.asdf` 







<details><summary>Source</summary>

```python
@dock
def asdf(self):
    ...

```

</details>

### Class `foo.PackageClass.InnerPackageClass`
#### Function `foo.PackageClass.InnerPackageClass.__init__` 







<details><summary>Source</summary>

```python
@dock
def __init__(self):
    ...

```

</details>

#### Function `foo.PackageClass.InnerPackageClass.asdf` 







<details><summary>Source</summary>

```python
@dock
def asdf(self):
    ...

```

</details>

## Module `foo.fooer` 


*Module-level docstring.*

It can be multi-line, and contain copyright notices, etc.

- [foo.fooer.asdf](#Function-foo.fooer.asdf)
- [foo.fooer.ClassOne](#Class-foo.fooer.ClassOne)
- [foo.fooer.bar](#Function-foo.fooer.bar)
- [foo.fooer.long_name](#Function-foo.fooer.long_name)
#### Function `foo.fooer.asdf` 



A function that does something that could work if it didn't.




<details><summary>Source</summary>

```python
@dock
def asdf():
    "A function that does something that could work if it didn't."

```

</details>

#### Function `foo.fooer.bar` 



A function that does something that could work if it didn't.




<details><summary>Source</summary>

```python
@dock(raises='Something that you don\'t want to happen')
def bar():
    "A function that does something that could work if it didn't."

```

</details>

#### Function `foo.fooer.long_name` 




First line is a short description.

Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in
laying out print, graphic or web designs. The passage is attributed to an
unknown typesetter in the 15th century who is thought to have scrambled
parts of Cicero's De Finibus Bonorum et Malorum for use in a type



**asdf**

What in the world?
**Section1**


This is a long section
with multiple lines.

**Section2**

Shorter section


<details><summary>Source</summary>

```python
@dock(
    asdf='What in the world?',
    Section1='''
    This is a long section
    with multiple lines.
    ''',
    Section2='Shorter section'
)
def long_name(asdf):
    """
    First line is a short description.

    Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in
    laying out print, graphic or web designs. The passage is attributed to an
    unknown typesetter in the 15th century who is thought to have scrambled
    parts of Cicero's De Finibus Bonorum et Malorum for use in a type
    """

```

</details>

### Class `foo.fooer.ClassOne`

### Usage

```python
>>> print('Hello World!')
>>> for i in range(100):
...     print(i)
```

You can [click this](http://www.google.com)

#### Function `foo.fooer.ClassOne.look` 



Something looking




<details><summary>Source</summary>

```python
@dock
def look(self):
    "Something looking"

```

</details>

### Class `foo.fooer.ClassOne.InnerOne`
#### Function `foo.fooer.ClassOne.InnerOne.look_innerone` 







<details><summary>Source</summary>

```python
@dock
def look_innerone(self):
    ...

```

</details>

# Package `foo.bar` 


**Documentation for package `foo.bar`**

This can contain any helpful information such as the below points:

1. One
2. Two
3. Three

## Module `foo.bar.barrer` 

- [foo.bar.barrer.asdf](#Function-foo.bar.barrer.asdf)
- [foo.bar.barrer.asdf2](#Function-foo.bar.barrer.asdf2)
#### Function `foo.bar.barrer.asdf` 



Just another place to put documentation.




<details><summary>Source</summary>

```python
@dock
def asdf():
    "Just another place to put documentation."

```

</details>

#### Function `foo.bar.barrer.asdf2` 

> Whatever?

**Arguments**

- `name` -> `builtins.str`: *The name to greet.*
- `age` -> `builtins.int`: 
- `alive` -> `builtins.bool`: 





This is a longer description.



**Usage**


```python
>>> print("Hello World!")
>>> for i in range(100):
...     print(i ** 2)
```



<details><summary>Source</summary>

```python
@dock(
    name='The name to greet.',
    short='Whatever?',
    Usage='''
    ```python
    >>> print("Hello World!")
    >>> for i in range(100):
    ...     print(i ** 2)
    ```
    '''
)
def asdf2(name: str, age: int, alive: bool):
    """
    This is a longer description.
    """

```

</details>

# Package `foo.bar.baz` 

#### Function `foo.bar.baz.some_func` 

> Just a little function that does nothing at all.

**Arguments**

- `a` -> `builtins.int`: 
- `b` -> `builtins.int`: *Just something*
- `c` -> [foo.bar.baz.ASDF](#Class-foo.bar.baz.ASDF): 


**Return Type:** `typing.Tuple[int, int, int]`



Can be used if you want.

It doesn't really matter.



**Usage**


```python
>>> a, b, c = some_func(1, 2, 3)
>>> a
1
>>> b
2
>>> c
3
```



<details><summary>Source</summary>

```python
@dock(
    short='Just a little function that does nothing at all.',
    Usage="""
    ```python
    >>> a, b, c = some_func(1, 2, 3)
    >>> a
    1
    >>> b
    2
    >>> c
    3
    ```
    """,
    b='Just something'
)
def some_func(a: int, b: int, c: ASDF) -> Tuple[int, int, int]:
    """
    Can be used if you want.

    It doesn't really matter.
    """
    return a, b, c

```

</details>

### Class `foo.bar.baz.ASDF`
## Module `foo.bar.baz.bazzer` 

- [foo.bar.baz.bazzer.asdf](#Function-foo.bar.baz.bazzer.asdf)
#### Function `foo.bar.baz.bazzer.asdf` 

> "Why does this exist?"




This is a much longer description.

Why would you want to have a shorter long description? If you do, you
might not know what you actually want because long descriptions are
far more descriptive.





<details><summary>Source</summary>

```python
@dock(short='"Why does this exist?"')
def asdf():
    """
    This is a much longer description.

    Why would you want to have a shorter long description? If you do, you
    might not know what you actually want because long descriptions are
    far more descriptive.
    """

```

</details>

