import spacy

nlp = spacy.load('en_core_web_sm')


def indicates_switch_tutor(sentence):
    doc = nlp(sentence)


    for token in doc:

        if token.dep_ == 'ROOT' and token.pos_ == 'VERB' and token.lemma_ in ['want','need','like']:
            for child in token.children:


                if child.dep_ == 'xcomp' and child.lemma_ in ['switch', 'change']:


                    for child2 in child.children:
                        if child2.dep_== 'prep':

                            for child3 in child2.children:
                                if child3.dep_=='pobj' and child3.lemma_ in ['tutor','teacher']:

                                    for child4 in child3.children:
                                        if child4.dep_=='amod':
                                            if child4.lemma_ in ['humorous','happy','funny','cute']:
                                                return 'humorous'
                                            elif child4.lemma_ in ['passionate','exciting','powerful','energetic']:
                                                return 'passionate'
                                            elif child4.lemma_ in ['creative','magical','inventive','thoughtful']:
                                                return 'creative'
                elif child.dep_=='dobj' and child.lemma_ in ['tutor','teacher']:

                    for child2 in child.children:
                        if child2.dep_=='amod':
                            if child2.lemma_ in ['humorous', 'happy', 'funny', 'cute']:
                                return 'humorous'
                            elif child2.lemma_ in ['passionate', 'exciting', 'powerful', 'energetic']:
                                return 'passionate'
                            elif child2.lemma_ in ['creative', 'magical', 'inventive', 'thoughtful']:
                                return 'creative'
        elif token.dep_=='ROOT' and token.pos_=='VERB' and token.lemma_ in ['switch','change']:
            for child in token.children:
                if child.dep_=='prep':

                    for child2 in child.children:
                        if child2.dep_=='pobj' and child2.lemma_ in ['tutor','teacher']:

                            for child3 in child2.children:
                                if child3.dep_=='amod':
                                    if child3.lemma_ in ['humorous', 'happy', 'funny', 'cute']:
                                        return 'humorous'
                                    elif child3.lemma_ in ['passionate', 'exciting', 'powerful', 'energetic']:
                                        return 'passionate'
                                    elif child3.lemma_ in ['creative', 'magical', 'inventive', 'thoughtful']:
                                        return 'creative'










    return False


