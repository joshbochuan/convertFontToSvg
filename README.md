# convertFontToSvg
Used for converting ttf files to svg. Created as a fast way to import fonts to Scratch.
python 3 environment and fonttools are required.

# setup for fonttools
1. Make sure you have python 3 or above installed. Verify the version by running `python --version` in a command prompt.
2. install fonttools with `pip install fonttools` in a terminal.

# how to use
1. Find your font ttf file and drag the ttf file into the folder. fonts could be found inside you system at `C:\Windows\Fonts`, or found on websites like `https://fonts.google.com/`. If font was in ttc format, find a online converter like `https://transfonter.org/ttc-unpack`
2. run `font_to_svg.bat`
3. input the font file you want to conver to svg file, ex: `consolas.ttf`
4. input the color you want the svg to be. It could be hex code, ex: `#FF0000`, or colors, ex: `red`
5. The code would run and a folder named the same as the ttf file should show up in the folder
6. import the svg files from the symbols folder as Scratch costumes, rename the names starting with `symbol_` to its corresponding symbol, ex: `symbol_asterisk` -> `*`
7. import the svg files from the lowercase folder as Scratch costumes.
8. import the svg files from the uppercase folder as Scratch costumes.
9. The process for English alphabet and symbols are complete. Continue only if you want to include Chinese characters.
10. import the svg files from the fullwidth_symbol folder as Scratch costumes.
11. import the svg files from the chinese folder as Scratch costumes. Because of too many files, Scratch may crash. remember to backup.

# Credits
chineseChar.txt came from here, containing 4,808 traditional Chinese characters referenced in *Chart of Standard Forms of Common National Characters*.
https://gist.github.com/stakira/6c6b2f0a577661eee713a5b040b7263f
