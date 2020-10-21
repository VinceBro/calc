# Calc
Simple CLI tool to use as a calculator for common math operations
## Installation
To install calc as a CLI tool just run install.sh, this script assumes that you have /usr/local/bin in your PATH. You might need to use sudo
## Options and example Usage
### Default usage
Without any arguments calc is used like the python terminal where you can enter mathematical operations and get results. You might need to escape your string with `"` as bash can be sensible with the `(`, `^` and `)` tokens. `x` is used to specify the multiplication operator.

Example : `calc 18.2 x 36 + 2` will return `657.19`

### `-a` argument
The `-a` argument is used to specify angles and parses the input string to recognize the `pi`, `rad` and `deg` keywords as well as the `/` operator to specify fractions. This argument is used to convert angles from rad to deg and rectify them if they go further than a full rotation.

Example : 
* `calc -a 3pi/4 rad` will return `135.0 deg` and `135.0 deg` rectified
* `calc -a 11pi/4 rad` will return `495.0 deg` and `135.0 deg` rectified
* `calc -a 270 deg` will return `4.7124 rad` and `4.7124 rad` rectified

### `-q` argument
The `-q` argument is used for quadratic equations where 3 parameters are used as input to specify a, b and c of the quadratic equation. This parameter can return complex numbers and will return them in exact form (no decimals).

Example : 
* `calc -q 1 -1 2` will return the formatted quadratic equation `1.0x² - 2.0x + 1.0` and the formatted zeros `(x - 1.0) and (x - 1.0)`
* `calc -q 1 -1 18` will return the formatted quadratic equation `1.0x² - 2.0x + 18.0` and the formatted zeros `(x - 1.0 + √68.0/2.0 i) and (x - 1.0 - √68.0/2.0 i)`