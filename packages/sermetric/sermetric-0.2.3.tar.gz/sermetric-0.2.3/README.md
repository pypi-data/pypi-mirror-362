SERMetric:

SERMetirc is an open-source library for evaluating how easy-to-read a text is. It supports a wide variety of indexes and allows the user to easily combine them. 


FEATURES:

Several indexes are provided:

* pointsIndex: it is the number of points in the text divided by the number of words. The closer to one, the more readable, as shorter sentences are involved.
* newParagraphIndex: it is the number of new paragraphs in the text divided by the number of words. The closer to the point index, the more readable it is, as it involves shorter paragraphs.
* CommaIndex: the number of commas in the text divided by the number of words. The closer to zero the more readable.
* extensionIndex: ratio between the number of syllables in lexical words and the number of lexical words, lexical words being understood  as nouns, verbs, adjectives and adverbs. As it is an average, it implies that results between 1 and 2 mean a predominance of words between one and two syllables, so it will be more readable.
* triPoliIndex: ratio of the number of trisyllabic and polysyllabic words to the number of lexical words. The closer to zero the more readable.
* lexicTriPoliIndex: ratio of the  number of trisyllabic and polysyllabic lexical  words to the numberof lexical words. The closer to zero the more readable.
* diversityIndex: ratio between the  number of different words in the text and the total number of words. A number close to zero implies excessive redundancy of the same terms, which makes the text tedious, while a number close to one means high diversity, which makes it less readable.
* lexicalFreqIndex: ratio between the number of low-frequency lexical words and the number of lexical words. The "Corpus de la Real Academia Española" (CREA) and the 'Gran diccionario del uso del español actual' will be used as a reference. The closer to zero the more readable.
* wordForPhraseIndex: quotient resulting from the division between the number of words in the text and the number of sentences. For a text to be easy to read, the length of the sentences must be between 15 and 20 words maximum.
* sentenceComplexityIndex: the result of dividing the number of sentences by the number of propositions. The minimum value is 1 and the maximum is infinite, although above 5 it is difficult to mantain coherence and clarity of expression. 
* complexityIndex: quotient between the number of low-frequency syllables and the total number of syllables (reference: 'Diccionario de frecuencias de las unidades lingüísticas del castellano'). The closer to zero the more readable.
* fernandezHuerta: is the result of 206.84-0.6P-1.02F, where P is the number of syllables per 100 words  and F is the number of sentences per 100 words. The higher the result the more readable.