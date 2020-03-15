# easymeet

Tool made to help teams find the most optimized time for a meeting.

<p align="center"><img height="35%" src="example/eagescufba.png" alt="eagescufba">


## Dependencies

You need `Python 3+` and `pip 3+` in order to use this script.

| Python libraries needed |
| - |
| numpy |
| matplotlib |
| pyqt5 |

If your distribution still calls Python as "python2", instead of "python3" (you can tell that by sending `realpath $(which python)`), as debian and debian based distros do (Ubuntu and Linux Mint are examples), use pip3 instead of pip to install dependencies with:

```sh
pip install --user numpy, matplotlib, pyqt5
# or, if  python3 isn't default,
pip3 install --user numpy, matplotlib, pyqt5
```


## Usage

Basically create a Python dictionary with people names as keys and their available intervals per day as values. Hours and minutes are separated by colons (":") or "h"'s. Interval starts and ends are separated by minus signs ("-") or ellipsis ("..."). For example:

```
people = {
  #name        mon       tue         wed       thu         fri sat
  "Person A": "7h00-9h30 10h00-11h30 7:00-9:30 10:00-11:30  -  -12h"
  # This person has malleable Fridays: "-" here means all day.
  # This person is also able for meetings on Saturday mornings.
}
```

I wanted to be able to write intervals fast, so this program accepts time in many formats. For example, next code is equivalent to the first one

```
people = {
  "person a": "7-9h30 10...11:30 mon tue ..."
  # as you can see, pure "..." also means all day.
}
```

Notice that you can also refference previously stated days, when they are equivalent.

Let's say you want to tell easymeet that someone has multiple available intervals. You could do that by putting all of them inside parenthesis:

```
people = {
  #name        mon               tue           wed
  "Person B": "(7-12 13h30-16)   (mon + 19-21) none"
  # the "+" sign is optional.
}
```

Any string other than pre-defined or used defined names for days of the week will be treated as a null interval. So "none" above would mean the same as 'nope' or 'nothing' would: an empty interval. More realistically, "none" here means "this person is not available in this day".

After that, a function from easymeet's package can be imported and applied to to dictionary:
```
plot_free_schedule(people,
                   header="It is a title",
                   filename='path/to/filename.png')
```

The filename keyword saves image at its value ("path/to/filename.png"). Look at "example_custom.py" in order to know other ways to configure the chart.


# Other examples

## Explained
<p align="center"><img src="example/example.png" alt="example">

## When to play RPG
<p align="center"><img src="example/ardur.png" alt="RPG">


## Contact

  - **Name:** Marcos Conceição
  - **E-mail:** [marcosrdac@gmail.com](mailto:marcosrdac@gmail.com)
  - **GitHub:** [marcosrdac](github.com/marcosrdac)
  - **Website:** [marcosrdac.github.io](http://marcosrdac.github.io)
