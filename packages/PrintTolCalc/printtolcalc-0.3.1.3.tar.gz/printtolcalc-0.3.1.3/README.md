# PrintTolCalc

(<ins>**Print**</ins> <ins>**Tol**</ins>erance <ins>**Calc**</ins>ulator)

A simple CLI tool to calculate 3D print dimensional tolerance.

It is worthy to note this is more for testing your print consistency (and lets be honest, even more-so bragging).

Testing in this way is not an end-all be-all solution,
It does have issues and is not a perfect representation of printer performance.

I realize this code "may be"(read: "is") bad but I don't care it's a sideproject for fun anyways, Don't take it too seriously!

## License

This is licensed under "OQL-1.2" found at [LICENSE.md](<https://github.com/NanashiTheNameless/PrintTolCalc/blob/main/LICENSE.md>).

Please ensure you are compliant with the license before using this project!

(Thank you [Avaris/Andrea Vos](<https://avris.it/>) for making an amazing license for all to use)

## Installation

Get the Latest

```sh
pipx install --force 'PrintTolCalc @ git+https://github.com/NanashiTheNameless/PrintTolCalc@main'
```

Or get from [PyPi](<https://pypi.org/project/PrintTolCalc/>) (not recommended, may be out of date)

## Get started

### Interactively

```sh
PrintTolCalc
```

### Partially-interactively

```sh
PrintTolCalc --expected X Y Z
```

### Non-Interactively

```sh
PrintTolCalc --expected X Y Z --measured X Y Z
```

### Standalone

If you would prefer not to instal it and just use it directly there is also a standalone version avalible!
[PrintTolCalc.Standalone.py](<https://github.com/NanashiTheNameless/PrintTolCalc/raw/refs/heads/main/PrintTolCalc.Standalone.py>)

Just replace `PrintTolCalc` with `PrintTolCalc.Standalone.py` when you go to use it!

```sh
PrintTolCalc.Standalone.py
```

## Credits

[All Major Contributors](<https://github.com/NanashiTheNameless/PrintTolCalc/blob/main/CONTRIBUTORS.md>)

[All Other Contributors](<https://github.com/NanashiTheNameless/PrintTolCalc/graphs/contributors>)
