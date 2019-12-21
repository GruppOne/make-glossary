# make-glossary

Una coppia di script per generare un glossario in latex. Un primo script (`make-json.py`) raccoglie tutti gli utilizzi del comando `\glossario` in un file .json, che poi va popolato con le definizioni dei termini; un secondo script (`make-tex.py`) inserisce i termini e le definizioni nel file `glossario.tex`. Gli script sono specifici alla struttura della directory usata per la nostra documentazione.
