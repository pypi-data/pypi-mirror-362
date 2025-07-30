<p align="center">
<img src="https://user-images.githubusercontent.com/2049665/29219793-b4dcb942-7e7e-11e7-8785-761b0e784e04.png" alt="Wordninja picture" width="128">
  <h1 align="center">Wordninja-Enhanced</h1>
  <p align="center">
    Split your merged words!
    <br />
  </p>
</p>

<br>

## ℹ About

This is a fork of the popular wordninja repository and improves on it in several aspects.

Language support has been extended to include the following languages out of the box:

- English (en)
- German (de)
- French (fr)
- Italian (it)
- Spanish (es)
- Portuguese (pt)

More functionalities were added aswell:

- A new rejoin() function was created. It splits merged words in a sentence and returns the whole sentence with the corrected words while retaining spacing rules for punctuation characters.
- A candidates() function was added that returns not only one result, but instead several results sorted by their cost.
- It is now possible to specify additional words that should be added to the dictionary or words that should be excluded while initializing the LanguageModel.
- The splitting behaviour can be actively influenced if a different split of a certain word is desired.
- Hyphenated words are now also supported.
- The algorithm now also preserves punctuation while spitting merged words and does no longer break down when encountering unknown characters.

More info about these functionalities can be found further down in the usage section.

## Requirements

- Python 3.9 or higher

## How to Install

```
pip install wordninja-enhanced
```

## Usage

The functionalities are explained in the following code snippet:

```python
import wordninja_enhanced as wordninja

# This function splits merged words 
split_text= wordninja.split("Splitthesemergedwordsforme")
print(f"Example 1: {split_text}\n")

# This function returns multiple possible ways to split the input, ranked by lowest cost first.
candidates_list = wordninja.candidates("derekanderson", 3)
print("Example 2:")
for i, candidate in enumerate(candidates_list):
    print(f"candidate {i+1}: {candidate}")
print()

# This function splits merged words and returns the correctly splitted string,
# while applying correct spacing rules for punctuation characters.
rejoined_text = wordninja.rejoin("That'sthesheriff's\"badge\" youarewearing!")
print(f"Example 3: {rejoined_text}\n")

# Without any further arguments the default language is set to english
lm = wordninja.LanguageModel()
joined_text = lm.rejoin("Thisisanotherpreviouslymergedtextexample.")
print(f"Example 4: {joined_text}\n")

# Another language can be specified via the language parameter.
lm = wordninja.LanguageModel(language='de')
joined_text = lm.rejoin("Wiegehtesdir?")
print(f"Example 5: {joined_text}\n")

# The LanguageModel also supports adding words to the dictionary. If a word is being split,
# it is likely missing from the dictionary. It can be added via the add_words parameter:
print("Example 6:")
joined_text = wordninja.rejoin("Palaeoloxodonisanextinctgenusofelephant.")
print(f"Before adding the word: {joined_text}")

custom_lm = wordninja.LanguageModel(
    language="en",
    add_words=['Palaeoloxodon'],
)

joined_text = custom_lm.rejoin("Palaeoloxodonisanextinctgenusofelephant.")
print(f"After adding the word: {joined_text}\n")

# The add_words parameter can also be used to actively influence the splitting behaviour.
# A string like "coinc" gets split with the default dictionary into "coin" and "c".
# If they should instead be split as "co" and "inc", it is possible to move existings words
# in the dictionary, in this case "inc", manually to the top of the dictionary, making it
# more common. This is done via the "overwrite" parameter and specifying add_to_top=True.
print("Example 7:")
joined_text = wordninja.rejoin("coinc")
print(f"Before modifying the dictionary: {joined_text}")

custom_lm = wordninja.LanguageModel(
    language="en",
    add_words=['inc'],
    add_to_top=True,
    overwrite=True,
)

joined_text = custom_lm.rejoin("coinc")
print(f"After modifying the dictionary: {joined_text}")

# The LanguageModel also allows the usage of a custom dictionary when the language is specified
# as 'custom'. Words can also be removed from the dictionary in use via a blacklist.
custom_lm = wordninja.LanguageModel(
    language='custom',
    word_file=r'path\to\your\custom_dict.txt.gz',
    add_words=[],
    blacklist=[],
    add_to_top=True, # Default false
    overwrite=False, # Default false
)
```

The output from the examples is the following:

```
Example 1: ['Split', 'these', 'merged', 'words', 'for', 'me']

Example 2:
candidate 1: ['derek', 'anderson']
candidate 2: ['derek', 'anders', 'on']
candidate 3: ['derek', 'and', 'ers', 'on']

Example 3: That's the sheriff's "badge" you are wearing!

Example 4: This is another previously merged text example.

Example 5: Wie geht es dir?

Example 6:
Before adding the word: Palaeo lox odon is an extinct genus of elephant.
After adding the word: Palaeoloxodon is an extinct genus of elephant.

Example 7:
Before modifying the dictionary: coin c
After modifying the dictionary: co inc
```


It can also handle long strings:
```
>>> wordninja.split('wethepeopleoftheunitedstatesinordertoformamoreperfectunionestablishjusticeinsuredomestictranquilityprovideforthecommondefencepromotethegeneralwelfareandsecuretheblessingsoflibertytoourselvesandourposteritydoordainandestablishthisconstitutionfortheunitedstatesofamerica')
['we', 'the', 'people', 'of', 'the', 'united', 'states', 'in', 'order', 'to', 'form', 'a', 'more', 'perfect', 'union', 'establish', 'justice', 'in', 'sure', 'domestic', 'tranquility', 'provide', 'for', 'the', 'common', 'defence', 'promote', 'the', 'general', 'welfare', 'and', 'secure', 'the', 'blessings', 'of', 'liberty', 'to', 'ourselves', 'and', 'our', 'posterity', 'do', 'ordain', 'and', 'establish', 'this', 'constitution', 'for', 'the', 'united', 'states', 'of', 'america']
```

## Further notes

The files and the script to create the dictionaries are also included in the Dictionaries folder.
They can be created by just running the script 'create_dictionaries.py'.

If you are interested in adding support for another language feel free to add your language to the language_config in the script and to create a corresponding corpus folder with the language data.



## Acknowledgements

The dictionaries were created using the Leipzig Corpora Collection. Without their work this project would have not been possible.

D. Goldhahn, T. Eckart & U. Quasthoff: Building Large Monolingual Dictionaries at the Leipzig Corpora Collection: From 100 to 200 Languages.
In: Proceedings of the 8th International Language Resources and Evaluation (LREC'12), 2012
