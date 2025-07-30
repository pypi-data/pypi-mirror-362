```text
██████╗ ██╗   ██╗██████╗ ██████╗ ██╗███╗   ██╗████████╗██╗   ██╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝
██████╔╝ ╚████╔╝ ██████╔╝██████╔╝██║██╔██╗ ██║   ██║    ╚████╔╝
██╔═══╝   ╚██╔╝  ██╔═══╝ ██╔═══╝ ██║██║╚██╗██║   ██║     ╚██╔╝
██║        ██║   ██║     ██║     ██║██║ ╚████║   ██║      ██║
╚═╝        ╚═╝   ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝
```
# version 2.1.0.


## Description:
Extensions for printing and strings in general.
Create simple animations, loading bars, manage user messages in custom fonts.
Text designs, and special prints.
And all - by yourself.

## Documentation:
For documentation via github [Click here.](https://yedist.github.io/pyprinty/)

## license:
MIT © 2025 Yedidya steinmetz

## simple example:

```text
from pyprinty import Font, Fonts


my_font = Font(load=Fonts.CLASSIC) #  Creating a font, using a ready-made font

# Printing a message to the user from the font we created
print(my_font("hello ", input("What is your name?"), sep=" "), end="!")

# You don't have to use ready-made fonts, you can create your own, and much more!

```

## little more:
This is just a part:
```text
from pyprinty import Font, Fonts
from pyprinty import Colors, Color
from pyprinty import Effects, Cursor
from pyprinty import Animation
from pyprinty import size


# Creating the fonts:
my_font = Font(
    text_color=Colors.RED,  # Ready color
    base_color=Color(0, 255, 0),  # Background color, Custom color
    effects=[Effects.Bold, Effects.Speedblink]  # Two ready-made effects
)
error_font = Font(load=Fonts.ERROR)  # Creating a font and loading ready-made font settings Error
# Creating a management animation of the prints
my_animation = Animation(
    load={  # Loading by dict, this can also be done in font
        # Creates an animated object, sets the font, and makes it into a normal print mode.
        "message": {"font": my_font, "mode": "print"}
    }
)
# Adding an object manually, on glossy print mode
my_animation.add_font("error", error_font, mode="glare")
# Using the message object we created
my_animation.send(
    "message",  # the object
    "hello", input("What is your name?"),  # the text
    sep=" ", end=""  # The library preserves all parameters.
)
Cursor.PRINT(Cursor.CLEAR_ALL)  # Reset the entire terminal (there are many more such commands)
# Demonstration of printing via the print command using the error font
print(
    error_font(
        # Print the current line size and number of lines of the terminal
        "your consul size is", size(), sep=" "
    ),
    end="!"
)
# There's a lot more in this library!

```
