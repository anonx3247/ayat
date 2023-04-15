# verses
A simple python script which downloads and retrieves passages from the quran with multiple languages and transliteration. It also has searh abilities

```bash
Welcome to verses
-h                  help menu
-l [language code]  language selection (ex: 'verses -l en')
-t                  english transliteration
-v   [verses]       verse list (ex: 'verses -v 1:23 6:24 5:4-7')
-s [query]          search for query (can be regex)
-sc [query]         search for query (can be regex)(colored)


Note: the '-v' option must be last
Current languages: en, fr, ar, it, es, de
About transliteration:


Bold letters are not pronounced, underlined consonants are hard consonants, 
 and underlined vowels are long vowels
```
like in: a**l**rra <ins>h</ins>m <ins>a</ins>n

A great thanks to [Tanzil](tanzil.net) for their text transliterations and translations which this script downloads from

## Dependencies

You will need the `wget` python package for downloading to work:

```bash
pip3 install wget
```

## Example Usage

```bash
verses -l en -s "pray" -v 2:1-100, 3:1-30
```
```
1: (2:3) Who believe in the unseen, establish prayer, and spend out of what We have provided for them,
2: (2:43) And establish prayer and give zakah and bow with those who bow [in worship and obedience].
3: (2:45) And seek help through patience and prayer, and indeed, it is difficult except for the humbly submissive [to Allah]
4: (2:60) And [recall] when Moses prayed for water for his people, so We said, "Strike with your staff the stone." And there gushed forth from it twelve springs, and every people knew its watering place. "Eat and drink from the provision of Allah, and do not commit abuse on the earth, spreading corruption."
5: (2:83) And [recall] when We took the covenant from the Children of Israel, [enjoining upon them], "Do not worship except Allah; and to parents do good and to relatives, orphans, and the needy. And speak to people good [words] and establish prayer and give zakah." Then you turned away, except a few of you, and you were refusing.
6: (2:89) And when there came to them a Book from Allah confirming that which was with them - although before they used to pray for victory against those who disbelieved - but [then] when there came to them that which they recognized, they disbelieved in it; so the curse of Allah will be upon the disbelievers.
```

## Installation

To install it on a unix system simply run
```bash
sudo make install
```

## Fzverse

If you have `fzf` installed you can also use the `fzverse` script to search through the english corpus with fzf
