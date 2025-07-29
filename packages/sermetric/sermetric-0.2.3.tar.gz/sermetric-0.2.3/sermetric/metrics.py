import numpy as np
import pyphen
import spacy
import pandas as pd
import textstat
import re

a = pyphen.Pyphen(lang='es')
nlp = spacy.load('es_core_news_sm')


# Total de puntos: número de puntos del texto entre número de palabras.
# Cuanto más próximo a uno, más lecturable, al implicar frases más cortas
def pointsIndex(texto):
    numPal = textstat.lexicon_count(texto, removepunct=True) #cuenta el número de palabras
    puntos = texto.count('.')
    indice = puntos/numPal
    return indice

# Total de puntos y aparte: número de puntos y aparte del texto entre número de palabras
# Cuanto más próximo al índice de puntos, más lecturable, al implicar párrafos más cortos
def newParagraphIndex(texto):
    numPal = textstat.lexicon_count(texto, removepunct=True)
    puntosAparte = texto.count('.\n')
    indice = puntosAparte/numPal
    return indice

# Total de comas: número de comas del texto entre número de palabras
# Cuanto más próximo a cero más lecturable
def CommaIndex(texto):
    numPal = textstat.lexicon_count(texto, removepunct=True)
    comas = texto.count(',')
    indice = comas/numPal
    return indice

def extensionIndex(texto):
    doc = nlp(texto)
    etiquetas_lexicas = {'NOUN', 'VERB', 'ADJ', 'ADV'}
    numLexicas = 0
    numSilabas = 0
    for token in doc:
        if token.pos_ in etiquetas_lexicas:
            numLexicas = numLexicas +1
            numSilabas = numSilabas + textstat.syllable_count(str(token))
    if numLexicas == 0:
        return 9999
    indice = numSilabas/numLexicas
    return indice

# Índice de palabras trisílabas y polisílabas: cociente entre el número de palabras trisílabas y polisílabas y el número de palabras léxicas.
# Cuanto más próximo a cero más lecturable
def triPoliIndex(texto):
    doc = nlp(texto)
    etiquetas_lexicas = {'NOUN', 'VERB', 'ADJ', 'ADV'}
    palabras = texto.split()
    numPal = len(palabras)
    palabrasPoli = textstat.polysyllabcount(texto)
    palabrasLexicas = 0
    for token in doc:
        if token.pos_ in etiquetas_lexicas:
            palabrasLexicas = palabrasLexicas + 1
    if palabrasLexicas==0:
        return 9999
    indice = palabrasPoli/palabrasLexicas
    return indice

# Índice de palabras trisílabas y polisílabas léxicas: cociente entre el número de palabras trisílabas y polisílabas léxicas y el número de palabras léxicas.
# Cuanto más próximo a cero más lecturable
def lexicTriPoliIndex(texto):
    doc = nlp(texto)
    etiquetas_lexicas = {'NOUN', 'VERB', 'ADJ', 'ADV'}
    palabrasPoli = 0
    palabrasLexicas = 0
    for token in doc:
        if token.pos_ in etiquetas_lexicas:
            palabrasLexicas = palabrasLexicas + 1
            numSilabas = textstat.syllable_count(str(token))
            if numSilabas >= 3:
                palabrasPoli = palabrasPoli + 1
    if palabrasLexicas==0:
        return 9999
    indice = palabrasPoli/palabrasLexicas
    return indice

# Índice de diversidad de palabras: cociente entre el número de palabras diferentes del texto y el total de palabras.
# Un número próximo a cero implica una excesiva redundancia de términos iguales, que origina un texto tedioso, mientras que un número próximo a uno significa una gran diversidad, que lo hace menos lecturable
def diversityIndex(texto):
    palabras = texto.split()
    numPal = len(palabras)
    palDistintas = len(set(palabras))
    indice = palDistintas/numPal
    return indice


# Índice de frencuencia léxica: cociente entre el número de palabras léxicas de baja frecuencia y el número de palabras léxicas.
# (se tomarán como referencia el "Corpus de la Real Academia Española" (CREA) y el "Gran diccionario del uso del español actual")
# Cuanto más próximo a cero, menor uso de palabras infrecuentes y más lecturable
def lexicalFreqIndex(texto):
    numLexicas = 0
    bajaFrecuencia = 0
    doc = nlp(texto)
    etiquetas_lexicas = {'NOUN', 'VERB', 'ADJ', 'ADV'}
    for token in doc:
        if token.pos_ in etiquetas_lexicas:
            numLexicas = numLexicas +1
            #Comprobamos si esa palabra está en el diccionario
            
            if textstat.is_difficult_word(str(token)):
                bajaFrecuencia = bajaFrecuencia +1
    if numLexicas==0:
        return 9999
    indice = bajaFrecuencia/numLexicas
    return indice


# Índice de palabras por frase: cociente resultado de la división entre el número de palabras del texto y el número de oraciones.
# Para que un texto sea de lectura fácil, la extensión de las oraciones debe estar entre 15 y 20 palabras como máximo.
def wordForPhraseIndex(texto):
    numPal = textstat.lexicon_count(texto, removepunct=True)
    numFrases = textstat.sentence_count(texto)
    indice = numPal/numFrases # Mide el índice de palabras por frase
    return indice


# Índice global de complejidad oracional: resultado de dividir el número de oraciones entre el número de proposiciones
# El valor mínimo es 1 y el máximo es infinito, aunque por encima de 5 es complicado mantener la coherencia y la claridad en la expresión.
def sentenceComplexityIndex(texto):
    frases = re.split(r'[.!?]', texto)
    proposiciones = 0
    numFrases=0
    # Para cada frase vemos si es proposición o no
    for frase in frases:
        if frase!='': # Para quitarnos las frases vacías
            doc  = nlp(frase)

             # Regla 1: debe tener un verbo
            tiene_verbo = any(token.pos_== "VERB" for token in doc)

            # Regla 2: no debe ser una pregunta, exclamación o imperativo
            es_enunciativa = not any(token.tag_ in ["INTJ", "IMP"] for token in doc)

            if tiene_verbo and es_enunciativa:
                proposiciones = proposiciones +1
                
            numFrases = numFrases+1
    if proposiciones!=0:
        indice = numFrases/proposiciones
        return indice
    else:
        return 999999
    
    
def fernandezHuerta(texto):
    return textstat.fernandez_huerta(texto)


# Índice de complejidad silábica: cociente entre el número de sílabas de baja frecuencia y el número total de sílabas (referencia: "Diccionario de frecuencias de las unidades lingüísticas del castellano")
# Cuanto más próximo a cero más lecturable
def complexityIndex(texto):
    palabras = texto.split()
    silabasBajaFrec = ['a', 'do', 'ta', 'te', 'ti', 'ca', 're', 'ra', 'de', 'da', 'se', 'na', 'co', 'to', 'la', 'ba', 'ri', 'ma', 'li', 'di', 'sa', 'me', 'pa', 'in', 'ci', 'con', 'lo', 'mi', 'm', 'le', 'si', 'es', 'men', 'des', 'dos', 'en', 'pe', 'ni', 'ga', 'za', 'so', 'o', 'mos', 'no', 'das', 'ce', 'e', 'ne', 'ro', 'fi', 'cio', 'an', 'cu', 'po', 'vi', 'va', 'tra', 'nes', 'pro', 'ban', 'i', 'pre', 'cion', 'pi', 'ron', 'ran', 'res', 'su', 'ex', 'tar', 'tas', 'les', 'tu', 'tes', 'gi', 'bo', 've', 'bi', 'go', 'tos', 'que', 'cia', 'tan', 'nos', 'vo', 'cos', 'per', 'ras', 'ja', 'cas', 'car', 'ten', 'lla', 'qui', 'be', 'can', 'com', 'gra', 'sen', 'ble', 'dis', 'ar', 'cha', 'dad', 'fa', 'tro', 'fe', 'pu', 'as', 'du', 'ge', 'em', 'zo', 'ter', 'las', 'je', 'cen', 'lu', 'dor', 'los', 'mu', 'rra', 'tre', 'al', 'man', 'mien', 'ver', 'tri', 'rre', 'im', 'nas', 'bu', 'rio', 'ven', 'fla', 'nar', 'fo', 'par', 'sos', 'rro', 'lan', 'ros', 'for', 'zar', 'cer', 'ria', 'bra', 'llo', 'jo', 'nan', 'ha', 'lle', 'den', 'gu', 'mar', 'lar', 'sas', 'cor', 'bre', 'por', 'ere', 'gan', 'tor', 'rar', 'bles', 'au', 'pli', 'nu', 'rri', 'gar', 'sio', 'cien', 'zan', 'pla', 'san', 'cla', 'dia', 'mas', 'lis', 'u', 'cri', 'pen', 'os', 'ren', 'sis', 'chi', 'len', 'nis', 'fu', 'dan', 'ho', 'cho', 'dar', 'sar', 'he', 'bri', 'bar', 'ju', 'rios', 'ser', 'dio', 'sal', 'pren', 'gui', 'gue', 'hi', 'trans', 'der', 'flo', 'tis', 'ad', 'nal', 'pon', 'vas', 'pan', 'gre', 'bas', 'die', 'tras', 'fun', 'ris', 'van', 'cul', 'xi', 'vos', 'cias', 'or', 'pri', 'ple', 'gua', 'cie', 'llas', 'cal', 'lec', 'tran', 'cua', 'che', 'pos', 'cro', 'sin', 'sor', 'dien', 'sus', 'gas', 'mor', 'ji', 'gen', 'ru', 'bro', 'ner', 'cons', 'gos', 'tir', 'ces', 'ob', 'rias', 'ses', 'ac', 'zas', 'mon', 'vie', 'jar', 'vol', 'llos', 'ins', 'cir', 'sion', 'tua', 'vis', 'ya', 'ber', 'dra', 'hu', 'sub', 'tur', 'tem', 'cep', 'cam', 'fec', 'jan', 'zos', 'am', 'fre', 'tie', 'via', 'nen', 'nun', 'bli', 'bor', 'tien', 'tin', 'ye', 'yen', 'lia', 'mer', 'char', 'pul', 'ves', 'guar', 'plan', 'bla', 'ton', 'mis', 'flo', 'gri', 'bio', 'cru', 'chu', 'dri', 'pin', 'fra', 'sig', 'tio', 'mal', 'dir', 'rien', 'cli', 'lli', 'pas', 'plo', 'pun', 'jos', 'lin', '?e', 'pi', 'pres', 'bal', 'duc', 'rran', 'sol', 'sul', 'var', 'bus', 'nien', 'pes', 'yo', 'lum', 'mul', 'tru', 'cis', 'cra', 'jas', 'lon', 'cuen', '?i', 'pal', 'tal', 'fir', 'cau', 'ciar', 'dro', 'vio', 'cial', 'er', 'llar', 'nia', 'rras', 'ral', 'chan', 'fla', 'gio', 'vir', 'zu', 'bos', 'col', 'fan', 'yu', 'llan', 'trar', 'jus', 'nio', 'son', 'bur', 'glo', 'pues', 'cur', 'tec', 'vien', 'blan', 'chas', 'fal', 'fri', 'bia', 'tuo', 'cui', 'sia', 'mes', '?ar', 'ab', 'clu', 'fas', 'jes', 'nor', 'cian', 'pie', 'bran', 'pec', 'bir', 'don', 'ges', 'gran', 'tros', 'cum', 'fes', 'on', 'dre', '?as', 'ol', 'rrum', 'fia', 'som', 'cin', 'cris', 'gis', 'nie', 'rru', 'sua', 'sur', 'ben', 'bie', 'brar', 'gus', 'neu', 'quie', 'quis', 'sem', 'mag', 'sim', 'tum', 'bien', 'chos', 'pis', 'gun', 'sue', 'xa', 'fen', 'gol', 'hor', 'rec', 'rie', 'bru', 'gro', 'is', 'mio', 'truc', 'cios', 'gia', 'rin', 'rrar', 'tia', 'fle', 'gru', 'rres', 'die', 'his', 'cun', 'chis', 'gie', 'ques', 'clo', 'fer', 'jun', 'fac', 'mir', '?an', '?os', 'plas', 'yec', 'cle', 'ger', 'her', 'nau', 'ul', 'bes', 'psi', 'dez', 'dul', 'jer', 'sie', 'vin', 'fos', 'mia', 'pio', 'tui', 'zon', 'fran', 'nua', 'xis', 'bres', 'lim', 'lio', 'cues', 'gla', 'nex', 'rren', 'blo', 'bun', 'fren', 'hos', 'rei', 'rros', 'tam', 'ur', 'vuel', 'gor', 'ig', 'til', 'bis', 'dig', 'eu', 'gon', 'gien', 'guan', 'trin', 'vul', 'fie', 'lien', 'pra', 'rir', 'cuer', 'far', 'fin', 'hue', 'ler', 'mue', 'rom', 'cue', 'fil', 'fron', 'fru', 'gir', 'lus', 'nir', 'ais', 'flu', 'mez', 'plu', 'rac', 'pol', 'tris', 'cuar', 'fis', 'ir', 'mun', 'obs', 'op', 'trai', 'bom', 'pien', 'sien', 'tud', 'xo', 'bier', 'cap', 'hun', 'lie', 'mus', 'pei', 'pros', 'cier', 'ful', 'nin', 'dios', 'hin', 'quen', 'rial', 'teis', 'ches', 'flex', 'fro', 'mie', 'nec', 'prac', 'pug', 'quin', 'rein', 'reu', 'trui', 'brin', 'bue', 'dop', 'dua', 'guir', 'prox', 'tres', 'val', 'xio', 'crip', 'diar', 'g?e', 'tau', 'bai', 'brir', 'cuan', 'nom', 'prin', 'quia', 'suel', 'tex', 'vier', 'zue', 'hon', 'sex', 'sil', 'trac', 'clui', 'chon', 'dap', 'gal', 'lam', 'sias', 'un', 'cai', 'dac', 'dian', 'dran', 'fres', 'trio', 'tual', 'yan', 'bol', 'del', 'fian', 'liar', 'llon', 'piar', 'pue', 'sec', 'sir', 'abs', 'blar', 'doc', 'dras', 'duz', 'et', 'fue', 'juz', 'bel', 'brio', 'bui', 'dal', 'dies', 'frac', 'rrie', 'sau', 'tac', 'yas', 'bon', 'bras', 'coin', 'cres', 'fei', 'hen', 'jue', 'lei', 'prohi', 'rez', 'sai', 'sun', 'tren', 'cus', 'glu', 'grar', 'mur', 'nhe', 'nios', 'pac', 'puer', 'rrec', 'rron', 'rue', 'tuar', 'viar', 'bau', 'bios', 'brien', 'bron', 'dus', 'fon', 'fuer', 'guien', 'lac', 'mol', 'nue', 'reis', 'triun', 'yun', 'zam', 'aus', 'bais', 'blas', 'dias', 'frag', 'gues', 'rria', 'subs', 'sui', 'tez', 'tox', 'trom', 'tun', 'vein', 'cuns', 'gios', 'lun', 'pau', 'rrien', 'sha', 'vian', 'vic', 'yos', 'ai', 'dur', 'hur', 'lex', 'min', 'mues', 'nhi', 'oc', 'plau', 'rrir', 'rrup', 'sam', 'tuir', 'xal', 'xhi', 'dum', 'guen', 'har', 'jen', 'llen', 'pier', 'ram', 'rries', 'truir', 'yer', 'brie', 'dru', 'due', 'lios', 'mias', 'mil', 'muer', '?en', 'pep', 'plar', 'rit', 'rrui', 'rui', 'tad', 'tral', 'tram', 'tria', 'tron', 'xe', 'yar', 'ax', 'cel', 'cria', 'cham', 'chin', 'dhe', 'fix', 'fur', 'hie', 'jon', 'nac', 'ox', 'pai', 'pur', 'tuan', 'vu', 'zi', 'biar', 'bria', 'frau', 'gli', 'ham', 'hom', 'io', 'nad', 'nha', 'plen', 'plie', 'preg', 'prio', 'prue', 'pus', 'rais', 'rrai', 'rrio', 'rus', 'tai', 'tim', 'yes', 'ahu', 'cros', 'din', 'frus', 'fus', 'jis', 'lor', 'lles', 'nus', 'om', 'pel', 'pios', 'plia', 'rrer', 'tiem', 'tion', 'vor', 'bian', 'clau', 'cuo', 'fio', 'fras', 'guie', 'g?is', 'jem', 'lau', 'lias', 'mem', 'nias', 'pom', 'pru', 'roi', 'rrin', 'tax', 'zum', 'bren', 'bul', 'cluir', 'fiar', 'gle', 'guas', 'hip', 'huer', 'jui', 'ki', 'lip', 'lir', 'llu', 'noc', '?ue', 'pers', 'pian', 'sual', 'um', 'vai', 'xas', 'zur', 'bac', 'bil', 'bros', 'buir', 'cil', 'clan', 'chue', 'flan', 'luz', 'max', 'nui', '?ir', 'raz', 'rehu', 'rior', 'seis', 'trie', 'xac', 'xia', 'cei', 'cog', 'coi', 'crus', 'dil', 'fli', 'flui', 'frie', 'fruc', 'gias', 'g?en', 'g?i', 'hol', 'hui', 'llis', 'mios', 'nei', 'nig', 'noz', 'prie', 'pron', 'pseu', 'sep', 'sho', 'tuer', 'tus', 'vec', 'xor', 'bias', 'biz', 'blio', 'bris', 'chor', 'dais', 'diez', 'dres', 'fic', 'fluen', 'gras', 'guia', 'lap', 'rnons', 'nuo', 'pias', 'pil', 'prar', 'pris', 'rian', 'sel', 'sier', 'tais', 'tei', 'tel', 'tol', 'trau', 'viz', 'ze', 'bam', 'box', 'cim', 'ciu', 'claus', 'deu', 'dial', 'dox', 'drar', 'dual', 'dun', 'fies', 'flic', 'fol', 'frun', 'gam', 'gian', 'gim', 'gres', 'grie', 'gros', 'gual', 'guio', 'guis', 'hil', 'jac', 'jua', 'lian', 'lua', 'nai', '?on', 'pir', 'quio', 'rap', 'rer', 'rrom', 'rum', 'rup', 'shi', 'shu', 'vil', 'vue', 'xhaus', 'xion', 'zoi', 'aux', 'blu', 'caz', 'clar', 'clip', 'cuas', 'cuel', 'dern', 'diag', 'dog', 'dren', 'dros', 'feu', 'fria', 'giar', 'gren', 'grien', 'has', 'iz', 'lig', 'lue', 'lliz', 'mam', 'mix', 'nez', 'nil', 'nion', 'nuan', 'nues', 'peu', 'piz', 'quier', 'rris', 'she', 'ties', 'toi', 'trip', 'true', 'truo', 'tue', 'viu', 'xua', 'at', 'cies', 'clei', 'crio', 'chen', 'deis', 'duer', 'fluo', 'fut', 'glan', 'glar', 'gno', 'han', 'lai', 'lax', 'leu', 'llir', 'mai', 'mau', 'mian', 'nial', 'nuar', 'oi', 'pies', 'quios', 'riar', 'ries', 'tlan', 'trian', 'triz', 'vios', 'xha', 'yor', 'zal', 'ads', 'brup', 'clas', 'clis', 'clos', 'cohi', 'drie', 'fom', 'gip', 'gruen', 'guo', 'hir', 'hus', 'jal', 'jau', 'jor', 'lez', 'llez', 'naz', 'nhu', 'nies', 'non', '?al', '?es', '?u', 'paz', 'ples', 'plir', 'rai', 'rau', 'rol', 'rral', 'rrei', 'rrun', 'rua', 'seu', 'tier', 'tios', 'tle', 'toin', 'vial', 'xual', 'ap', 'beis', 'bies', 'bin', 'blez', 'blos', 'brus', 'cad', 'ced', 'clien', 'chus', 'dai', 'diac', 'drio', 'fau', 'fel', 'flec', 'fluc', 'gais', 'gaz', 'glas', 'guin', 'hal', 'haz', 'hier', 'lem', 'lep', 'lha', 'lhu', 'liz', 'lom', 'lup', 'llue', 'mens', 'neis', 'nel', 'nim', 'nul', 'plos', 'puen', 'quil', 'rep', 'rril', 'ruc', 'run', 'rur', 'sahu', 'seg', 'suc', 'tias', 'tig', 'triar', 'trie', 'truen', 'trun', 'vias', 'wi', 'xos', 'yi', 'zig', 'ag', 'blon', 'boi', 'brios', 'ceis', 'cid', 'cop', 'crar', 'cruen', 'cual', 'cuir', 'cuos', 'chun', 'dion', 'drau', 'duo', 'duos', 'fai', 'fias', 'fien', 'flar', 'flau', 'frar', 'frien', 'frio', 'gion', 'graz', 'gueis', 'guiar', 'hec', 'hex', 'jad', 'jin', 'jurn', 'lhe', 'loi', 'luar', 'luc', 'lur', 'mim', 'nam', 'nep', 'nihi', 'noi', 'nual', 'nuen', 'num', 'prag', 'prehis', 'quias', 'quien', 'ril', 'sac', 'sios', 'tial', 'toc', 'trias', 'tul', 'vam', 'vel', 'vex', 'xan', 'xen', 'xhor', 'xian', 'xu', 'yux', 'zor']
    silabas =  []
    silbaja = 0
    for p in palabras:
        for i in a.inserted(p).split('-'):
            silabas.append(i)
    for silaba in silabas:
        if silaba not in silabasBajaFrec:
            silbaja = silbaja+1
    totalSilabas = len(silabas)
    if totalSilabas==0:
        return 9999
    indice = silbaja/totalSilabas
    return indice