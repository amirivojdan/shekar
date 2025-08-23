---
title: 'Shekar: A Python Toolkit for Persian Natural Language Processing'
tags:
  - Python
  - Natural Language Processing
  - Persian Language
  - Text Processing
  - Computational Linguistics
  - Open Source Software

authors:
  - name: Ahmad Amirivojdan
    orcid: 0000-0003-3741-3979
    corresponding: true
    affiliation: 1

affiliations:
 - name: University of Tennessee, Knoxville, United States
   index: 1

date: 23 August 2025
bibliography: paper.bib

---

# Summary

Shekar is an open-source Python toolkit for Persian natural language processing (NLP). It provides a modular, efficient, and easy-to-use framework for tasks such as text preprocessing, tokenization, stemming, lemmatization, part-of-speech (POS) tagging, named entity recognition (NER), keyword extraction, embeddings, spell checking, and visualization. Its composable pipeline design supports reproducible workflows that scale effectively from basic text processing to large-scale corpus analysis.

# Statement of need 

Persian natural language processing has expanded rapidly over the past decade, supporting applications in digital humanities, social media analysis, conversational systems, and language modeling. Accordingly, there has been substantial progress in developing tools for Persian language processing. Libraries such as [Hazm](https://github.com/roshan-research/hazm), Parsivar [@mohtaj2018parsivar], and DadmaTools [@jafari2025dadmatools] provide essential functionalities including normalization, tokenization, and part-of-speech tagging. While these tools are valuable, they often come with limitations that restrict flexibility, extensibility, and efficient deployment in diverse settings.

Common challenges include:

- Limited modularity, making it difficult to adapt components or extend functionality.
- Tight coupling between processing stages, which hinders the creation of custom workflows.
- Heavy dependencies and large transformer models that require GPUs or specialized hardware for reasonable performance.
- Irregular updates and delayed issue resolution, which affect long-term maintainability.

Shekar was developed to address these challenges by offering a lightweight, modular, and extensible toolkit for Persian natural language processing. It adopts a clean and composable pipeline architecture, allowing users to build workflows from independently configurable components. This modular approach is especially effective for handling the complexities of Persian script, including inconsistent diacritics, spacing conventions, and the blend of formal and colloquial writing styles. It also supports practical applications such as OCR post-processing, social media text normalization, and data preparation for training language models.

A key distinction of Shekar is its focus on algorithmic efficiency and accessibility. The toolkit combines optimized preprocessing algorithms with lightweight, quantized transformer models, making it practical for low-resource devices as well as diverse environments ranging from research laboratories to production systems with limited computational capacity.

By emphasizing simplicity, performance, and modular design, Shekar fills a critical gap in the Persian NLP ecosystem. It offers a practical and user-friendly toolkit that supports both rapid experimentation and robust deployment across a wide range of use cases.

# Main Components

Shekar provides a set of key functionalities covering essential tasks in Persian natural language processing. Each functionality is implemented as an independent component that can be combined into customizable pipelines.

- **Preprocessing**
Provides text normalization tools to handle Persian-specific challenges such as inconsistent diacritics and spacing rules. The normalization steps follow the orthographic and typographic guidelines defined by [The Academy of Persian Language and Literature](https://apll.ir/) and include filters for punctuation, digits, emojis, non-Persian characters, and corrections for spacing and script variants.

- **Tokenization**
Offers word-level,sentence-level, and SentencePiece [@kudo2018sentencepiece] tokenizers built specifically for Persian text. These tokenizers use Unicode-aware rules to handle zero-width non-joiners, punctuation boundaries, and other language-specific edge cases.

- **Morphological Analysis**
Includes stemming, lemmatization, inflection, and verb conjugation tools. The stemmer applies rule-based suffix removal, while the lemmatizer combines vocabulary lookups with morphological rules to generate accurate base forms. The inflector and verb conjugator support the generation of correct word forms and verb tenses for diverse linguistic applications.

- **Part-of-Speech (POS) Tagging**
Provides lightweight transformer-based models for assigning POS tags to tokens using the [Universal Dependencies](https://universaldependencies.org/u/pos/index.html) tagging scheme. The models are based on a pretrained ALBERT model [@lan2019albert] trained on the large-scale Naab corpus [@sabouri2022naab] and fine-tuned on The Persian Universal Dependency Treebank (PerUDT) [@rasooli2020persian] for accurate and efficient POS tagging.

- **Named Entity Recognition (NER)**
Offers models trained on the publicly available [Persian NER dataset](https://github.com/Text-Mining/Persian-NER)
and fine-tuned from the same pretrained ALBERT model used for POS tagging. These models identify entities such as persons, locations, organizations, and dates in Persian text with high accuracy.

- **Keyword Extraction**
Implements algorithms for identifying the most informative terms and phrases within a text. The default implementation uses the RAKE (Rapid Automatic Keyword Extraction) algorithm [@rose2010automatic] for efficient and unsupervised keyword extraction.

- **Embeddings**
Supports both static embeddings (FastText) and contextual embeddings (ALBERT-based) for representing words and sentences as numerical vectors.

- **Spell Checking**
Identifies and corrects common spelling errors and spacing mistakes in Persian text. The spell checker uses a frequency-based approach built on a combined dictionary constructed from Persian generative lexicon dataset [@eslami2004persian] and unique words extracted from the Naab dataset [@sabouri2022naab], cross-checked against the Moein and Dehkhoda dictionaries for improved accuracy and coverage.

- **Visualization**
Provides visualization tools such as word clouds for exploring word frequencies and text patterns in large corpora.

# Efficiency and Reliability

Shekar is designed with both performance and robustness in mind. All models are 8-bit integer quantized, exported to ONNX format, and executed using onnxruntime to minimize dependencies and enable efficient CPU inference on a wide range of hardware, including low-resource systems.

The codebase is extensively tested across macOS, Linux, and Windows environments, with continuous integration workflows ensuring consistent behavior on all platforms. Unit tests cover more than 95 percent of the codebase, helping maintain reliability and stability as the toolkit evolves.

# Availability

Shekar is distributed as a Python package on [PyPI](https://pypi.org/project/shekar) under the MIT License, with full source code, test suite, documentations, pre-trained models, example scripts, and Jupyter notebooks available on [https://github.com/amirivojdan/shekar](https://github.com/amirivojdan/shekar).


# Acknowledgement

The author sincerely thanks Dr. Shaghayegh Yaraghi and Siavash Alizadeh for their continued support, which provided encouragement throughout the development of this work.

# References
