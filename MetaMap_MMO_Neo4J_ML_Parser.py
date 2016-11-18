#!/usr/bin/python
# copyright 2016 Levy C. Vargas
# all rights reserved

# Score, MapScr, s/m, m/s, UI, UI_2, cui, ui, Vowel_ct, Cons_ct, v/c, c/v,
# PhrLen, utt_ct, map_ct, sem_ct, can_ct, syn_ct, space_ct, txt, space_ct/txt,
# Txt/space_ct, Space_ct/c_ct, Space_ct/v_ct, Space_ct/MapScr,
# Space_ct/Score, Space_ct/UI_2, Space_ct/(c/v), Space_ct/PhrLen,
# Space_ct/map_ct, Space_ct/sem_ct, Space_ct/can_ct, Space_ct/syn_ct,
# utt_ct/score, utt_ct/MapScr

import numpy
import sys
import xml.dom
import xml.dom.minidom

from sys import argv

script, mmoxml = argv

mmos = xml.dom.minidom.parse(mmoxml)

def printerr(string):
    sys.stderr.write(string)
    return  

def handleMMOs(mmos):
    for mmo in mmos.getElementsByTagName("MMO"):
        handleUtterances(mmo.getElementsByTagName("Utterances"))
    return
    
def handleUtterances(utterances):
    utt_ct = utterances.item(0).getAttribute("Count")
    printerr("Utterances Count = %s\n" % utt_ct)
    
    mvar = {}
    mvar['utt_ct'] = utt_ct
    
    for utterance in utterances.item(0).getElementsByTagName("Utterance"):
        handleUtterance(utterance, mvar)
    return
        
def handleUtterance(utterance, mvar):
    printerr(" Utterance:\n")
    
    pmid = utterance.getElementsByTagName("PMID").item(0).firstChild.data  
    printerr("  PMID: %s " % pmid)
    printerr("\n")
    
    mvar['pmid'] = pmid
    
    for phrases in utterance.getElementsByTagName("Phrases"):
        handlePhrases(phrases, mvar)
    return
        
def handlePhrases(phrases, mvar):
    phr_ct = phrases.getAttribute("Count")
    printerr("  Phrases Count = %s\n" % phr_ct)
    
    mvar['phr_ct'] = phr_ct
    
    for phrase in phrases.getElementsByTagName("Phrase"):
        handlePhrase(phrase, mvar)
    return
        
def handlePhrase(phrase, mvar):
    printerr("   Phrase:\n")
    
    phr_txt = phrase.getElementsByTagName("PhraseText").item(0).firstChild.data
    printerr("    Phrase Text = '%s'\n" % phr_txt)
    
    phr_len = phrase.getElementsByTagName("PhraseLength").item(0).firstChild.data
    printerr("    Phrase Length = %s\n" % phr_len)
    
    syn_ct = phrase.getElementsByTagName("SyntaxUnits").item(0).getAttribute("Count")
    printerr("    SyntaxUnits Count = %s\n" % syn_ct)
    
    mvar['phr_txt'] = phr_txt
    mvar['phr_len'] = phr_len
    mvar['syn_ct'] = syn_ct
    
    for mappings in phrase.getElementsByTagName("Mappings"):
        handleMappings(mappings, mvar)
    return
        
def handleMappings(mappings, mvar):    
    map_ct = mappings.getAttribute("Count")
    printerr("     Mappings Count = %s\n" % map_ct)
    
    mvar['map_ct'] = map_ct
       
    for mapping in mappings.getElementsByTagName("Mapping"):
        handleMapping(mapping, mvar)
    return
    
def handleMapping(mapping, mvar):
    map_score = mapping.getElementsByTagName("MappingScore").item(0).firstChild.data
    printerr("      Mapping Score = %s\n" % map_score)
    
    mvar['map_score'] = map_score
    
    for map_candidates in mapping.getElementsByTagName("MappingCandidates"):
        handleMappingCandidates(map_candidates, mvar)
    return
        
def handleMappingCandidates(mapping_candidates, mvar):
    mapcan_total = mapping_candidates.getAttribute("Total")
    printerr("      MappingCandidates Total = %s\n" % mapcan_total)
    
    mvar['mapcan_total'] = mapcan_total
    
    for candidate in mapping_candidates.getElementsByTagName("Candidate"):
        handleCandidate(candidate, mvar)
    return
        
def handleCandidate(candidate, mvar):
    printerr("       Candidate:\n")
    
    can_score = candidate.getElementsByTagName("CandidateScore").item(0).firstChild.data
    printerr("        Candidate Score = %s\n" % can_score)
    
    can_cui = candidate.getElementsByTagName("CandidateCUI").item(0).firstChild.data
    printerr("        Candidate CUI = %s\n" % can_cui)
    
    can_match = candidate.getElementsByTagName("CandidateMatched").item(0).firstChild.data
    printerr("        CandidateMatched = %s\n" % can_match)
    
    can_pref = candidate.getElementsByTagName("CandidatePreferred").item(0).firstChild.data
    printerr("        CandidatePreferred = %s\n" % can_pref)
    
    mvar['can_score'] = can_score
    mvar['can_cui'] = can_cui
    mvar['can_match'] = can_match
    mvar['can_pref'] = can_pref
    
    for semtypes in candidate.getElementsByTagName("SemTypes"):
        handleSemTypes(semtypes, mvar)
    return

def handleSemTypes(semtypes, mvar):
    sem_ct = semtypes.getAttribute("Count")
    printerr("        SemTypes Count = %s\n" % sem_ct)
    
    mvar['sem_ct'] = sem_ct
    
    for semtype in semtypes.getElementsByTagName("SemType"):
    	semtype_txt = semtype.firstChild.data
        printerr("         SemType = %s\n" % semtype_txt)
        
        mvar['semtype'] = semtype_txt
        # found candidates with semtypes:
        # 1. add ML variables
        vowels = list("aeiouy")
        consonants = list("bcdfghjklmnpqrstvwxz")
        
        c_ct = int(sum(mvar['phr_txt'].count(c) for c in consonants))
        v_ct = int(sum(mvar['phr_txt'].count(v) for v in vowels))
        space_ct = int(mvar['phr_txt'].count(' '))
        txt_ct = int(mvar['phr_len']) - space_ct
        
        mvar['c_ct'] = c_ct
        mvar['v_ct'] = v_ct
        mvar['space_ct'] = space_ct
        mvar['txt_ct'] = txt_ct

        # 2. print all variables
        
        printmvar(mvar)
        return
    
def printmvar(mvar):
    step = counter()
    dat_ind = step.count
    
    # ratios (of floating point representations) using Numpy numerical Python float64s
    can_score = numpy.float64(mvar['can_score'])
    map_score = numpy.float64(mvar['map_score'])
    v_ct = numpy.float64(mvar['v_ct'])
    c_ct = numpy.float64(mvar['c_ct'])
    space_ct = numpy.float64(mvar['space_ct'])
    txt_ct = numpy.float64(mvar['txt_ct'])
    map_ct = numpy.float64(mvar['map_ct'])
    sem_ct = numpy.float64(mvar['sem_ct'])
    can_ct = numpy.float64(mvar['mapcan_total'])
    syn_ct = numpy.float64(mvar['syn_ct'])
    utt_ct = numpy.float64(mvar['utt_ct'])
    phr_len = numpy.float64(mvar['phr_len'])
    
    s_to_m = can_score / map_score
    m_to_s = map_score / can_score
    v_to_c = v_ct / c_ct
    c_to_v = c_ct / v_ct
    space_to_txt = space_ct / txt_ct
    txt_to_space = txt_ct / space_ct
    space_to_c = space_ct / c_ct
    space_to_v = space_ct / v_ct
    space_to_c_to_v = space_ct / c_to_v
    space_to_m = space_ct / map_score
    space_to_s = space_ct / can_score
    space_to_phrlen = space_ct / phr_len
    space_to_map = space_ct / map_ct
    space_to_sem = space_ct / sem_ct
    space_to_can = space_ct / can_ct
    space_to_syn = space_ct / syn_ct
    utt_to_s = utt_ct / can_score
    utt_to_m = utt_ct / map_score
    
    # create SemType dictionary for code lookups
    st_code = buildSemTypeDict()
    st_def = getSemTypeDesc()    
    
    # leave comma at the end of print to block newline append
    # print actual values in mvar dictionary
    # print ratios as floats
    
    # print dat_index 6 digits long
    print "dat%06d" % dat_ind, "\t",
    
    # print the source filename
    print str(mmoxml).strip(), "\t",
    
    # print NeoJ terms
    # print PMID, txt (PhrText), CUI, CanMatch, CanPref, sem, semTypeDesc, UI,
    print mvar['pmid'], "\t",
    print str(mvar['phr_txt']).replace("\t"," ").replace("\n"," ").replace("\"",""), "\t",
    print mvar['can_cui'], "\t",
    print mvar['can_match'], "\t",
    print mvar['can_pref'], "\t",
    print mvar['semtype'], "\t",
    print str(st_def[mvar['semtype']]), "\t",
    print str(st_code[mvar['semtype']]), "\t",
    
    # ML variables -- use Unix cut etc to separate from terms
    # Score, UI_2, cui, ui, Cons_ct, v/c, c/v, PhrLen, utt_ct, sem_ct, can_ct, syn_ct,
    print mvar['can_score'], "\t",
    print int(st_code[mvar['semtype']][1:]), "\t",
    print mvar['can_cui'], "\t",
    print int(mvar['can_cui'][1:]), "\t",
    print mvar['c_ct'], "\t",
    print v_to_c, "\t",
    print c_to_v, "\t",  
    print mvar['phr_len'], "\t",
    print mvar['utt_ct'], "\t",
    print mvar['sem_ct'], "\t",
    print mvar['mapcan_total'], "\t",
    print mvar['syn_ct'], "\t",
    
    # txt_ct
    print int(mvar['txt_ct']), "\t",

    # ratios
    # space_ct/txt, txt/space_ct, space_ct/c_ct, space_ct/v_ct, space_ct/(c/v),
    print space_to_txt, "\t",
    print txt_to_space, "\t",
    print space_to_c, "\t",
    print space_to_v, "\t",
    print space_to_c_to_v, "\t",
    
    # space_ct/PhrLen, space_ct/sem_ct, space_ct/can_ct, utt_ct/Score, utt_ct/MapScr     
    
    print space_to_phrlen, "\t",
    print space_to_sem, "\t",
    print space_to_can, "\t",
    print utt_to_s, "\t",
    print utt_to_m
# close def

# This function returns a four character code based on the the four (4)
# letter Semantic Type
# It returns a dict() object which will lookup the code based on the 4 letter
# keys published in 
def buildSemTypeDict():
    # For convenience and keeping data in one file, embed key-value pairs
    return {
            'aapp' : "T116",
            'acab' : "T020",
            'acty' : "T052",
            'aggp' : "T100",
            'amas' : "T087",
            'amph' : "T011",
            'anab' : "T190",
            'anim' : "T008",
            'anst' : "T017",
            'antb' : "T195",
            'arch' : "T194",
            'bacs' : "T123",
            'bact' : "T007",
            'bdsu' : "T031",
            'bdsy' : "T022",
            'bhvr' : "T053",
            'biof' : "T038",
            'bird' : "T012",
            'blor' : "T029",
            'bmod' : "T091",
            'bodm' : "T122",
            'bpoc' : "T023",
            'bsoj' : "T030",
            'carb' : "T118",
            'celc' : "T026",
            'celf' : "T043",
            'cell' : "T025",
            'cgab' : "T019",
            'chem' : "T103",
            'chvf' : "T120",
            'chvs' : "T104",
            'clas' : "T185",
            'clna' : "T201",
            'clnd' : "T200",
            'cnce' : "T077",
            'comd' : "T049",
            'crbs' : "T088",
            'diap' : "T060",
            'dora' : "T056",
            'drdd' : "T203",
            'dsyn' : "T047",
            'edac' : "T065",
            'eehu' : "T069",
            'eico' : "T111",
            'elii' : "T196",
            'emod' : "T050",
            'emst' : "T018",
            'enty' : "T071",
            'enzy' : "T126",
            'euka' : "T204",
            'evnt' : "T051",
            'famg' : "T099",
            'ffas' : "T021",
            'fish' : "T013",
            'fndg' : "T033",
            'fngs' : "T004",
            'food' : "T168",
            'ftcn' : "T169",
            'genf' : "T045",
            'geoa' : "T083",
            'gngm' : "T028",
            'gora' : "T064",
            'grpa' : "T102",
            'grup' : "T096",
            'hcpp' : "T068",
            'hcro' : "T093",
            'hlca' : "T058",
            'hops' : "T131",
            'horm' : "T125",
            'humn' : "T016",
            'idcn' : "T078",
            'imft' : "T129",
            'inbe' : "T055",
            'inch' : "T197",
            'inpo' : "T037",
            'inpr' : "T170",
            'irda' : "T130",
            'lang' : "T171",
            'lbpr' : "T059",
            'lbtr' : "T034",
            'lipd' : "T119",
            'mamm' : "T015",
            'mbrt' : "T063",
            'mcha' : "T066",
            'medd' : "T074",
            'menp' : "T041",
            'mnob' : "T073",
            'mobd' : "T048",
            'moft' : "T044",
            'mosq' : "T085",
            'neop' : "T191",
            'nnon' : "T114",
            'npop' : "T070",
            'nsba' : "T124",
            'nusq' : "T086",
            'ocac' : "T057",
            'ocdi' : "T090",
            'opco' : "T115",
            'orch' : "T109",
            'orga' : "T032",
            'orgf' : "T040",
            'orgm' : "T001",
            'orgt' : "T092",
            'ortf' : "T042",
            'patf' : "T046",
            'phob' : "T072",
            'phpr' : "T067",
            'phsf' : "T039",
            'phsu' : "T121",
            'plnt' : "T002",
            'podg' : "T101",
            'popg' : "T098",
            'prog' : "T097",
            'pros' : "T094",
            'qlco' : "T080",
            'qnco' : "T081",
            'rcpt' : "T192",
            'rept' : "T014",
            'resa' : "T062",
            'resd' : "T075",
            'rnlw' : "T089",
            'sbst' : "T167",
            'shro' : "T095",
            'socb' : "T054",
            'sosy' : "T184",
            'spco' : "T082",
            'strd' : "T110",
            'tisu' : "T024",
            'tmco' : "T079",
            'topp' : "T061",
            'virs' : "T005",
            'vita' : "T127",
            'vtbt' : "T010"
            }
            
def getSemTypeDesc():

    return {
            'aapp' : 'Amino Acid, Peptide, or Protein',
            'acab' : 'Acquired Abnormality',
            'acty' : 'Activity',
            'aggp' : 'Age Group',
            'amas' : 'Amino Acid Sequence',
            'amph' : 'Amphibian',
            'anab' : 'Anatomical Abnormality',
            'anim' : 'Animal',
            'anst' : 'Anatomical Structure',
            'antb' : 'Antibiotic',
            'arch' : 'Archaeon',
            'bacs' : 'Biologically Active Substance',
            'bact' : 'Bacterium',
            'bdsu' : 'Body Substance',
            'bdsy' : 'Body System',
            'bhvr' : 'Behavior',
            'biof' : 'Biologic Function',
            'bird' : 'Bird',
            'blor' : 'Body Location or Region',
            'bmod' : 'Biomedical Occupation or Discipline',
            'bodm' : 'Biomedical or Dental Material',
            'bpoc' : 'Body Part, Organ, or Organ Component',
            'bsoj' : 'Body Space or Junction',
            'carb' : 'Carbohydrate',
            'celc' : 'Cell Component',
            'celf' : 'Cell Function',
            'cell' : 'Cell',
            'cgab' : 'Congenital Abnormality',
            'chem' : 'Chemical',
            'chvf' : 'Chemical Viewed Functionally',
            'chvs' : 'Chemical Viewed Structurally',
            'clas' : 'Classification',
            'clna' : 'Clinical Attribute',
            'clnd' : 'Clinical Drug',
            'cnce' : 'Conceptual Entity',
            'comd' : 'Cell or Molecular Dysfunction',
            'crbs' : 'Carbohydrate Sequence',
            'diap' : 'Diagnostic Procedure',
            'dora' : 'Daily or Recreational Activity',
            'drdd' : 'Drug Delivery Device',
            'dsyn' : 'Disease or Syndrome',
            'edac' : 'Educational Activity',
            'eehu' : 'Environmental Effect of Humans',
            'eico' : 'Eicosanoid',
            'elii' : 'Element, Ion, or Isotope',
            'emod' : 'Experimental Model of Disease',
            'emst' : 'Embryonic Structure',
            'enty' : 'Entity',
            'enzy' : 'Enzyme',
            'euka' : 'Eukaryote',
            'evnt' : 'Event',
            'famg' : 'Family Group',
            'ffas' : 'Fully Formed Anatomical Structure',
            'fish' : 'Fish',
            'fndg' : 'Finding',
            'fngs' : 'Fungus',
            'food' : 'Food',
            'ftcn' : 'Functional Concept',
            'genf' : 'Genetic Function',
            'geoa' : 'Geographic Area',
            'gngm' : 'Gene or Genome',
            'gora' : 'Governmental or Regulatory Activity',
            'grpa' : 'Group Attribute',
            'grup' : 'Group',
            'hcpp' : 'Human-caused Phenomenon or Process',
            'hcro' : 'Health Care Related Organization',
            'hlca' : 'Health Care Activity',
            'hops' : 'Hazardous or Poisonous Substance',
            'horm' : 'Hormone',
            'humn' : 'Human',
            'idcn' : 'Idea or Concept',
            'imft' : 'Immunologic Factor',
            'inbe' : 'Individual Behavior',
            'inch' : 'Inorganic Chemical',
            'inpo' : 'Injury or Poisoning',
            'inpr' : 'Intellectual Product',
            'irda' : 'Indicator, Reagent, or Diagnostic Aid',
            'lang' : 'Language',
            'lbpr' : 'Laboratory Procedure',
            'lbtr' : 'Laboratory or Test Result',
            'lipd' : 'Lipid',
            'mamm' : 'Mammal',
            'mbrt' : 'Molecular Biology Research Technique',
            'mcha' : 'Machine Activity',
            'medd' : 'Medical Device',
            'menp' : 'Mental Process',
            'mnob' : 'Manufactured Object',
            'mobd' : 'Mental or Behavioral Dysfunction',
            'moft' : 'Molecular Function',
            'mosq' : 'Molecular Sequence',
            'neop' : 'Neoplastic Process',
            'nnon' : 'Nucleic Acid, Nucleoside, or Nucleotide',
            'npop' : 'Natural Phenomenon or Process',
            'nsba' : 'Neuroreactive Substance or Biogenic Amine',
            'nusq' : 'Nucleotide Sequence',
            'ocac' : 'Occupational Activity',
            'ocdi' : 'Occupation or Discipline',
            'opco' : 'Organophosphorus Compound',
            'orch' : 'Organic Chemical',
            'orga' : 'Organism Attribute',
            'orgf' : 'Organism Function',
            'orgm' : 'Organism',
            'orgt' : 'Organization',
            'ortf' : 'Organ or Tissue Function',
            'patf' : 'Pathologic Function',
            'phob' : 'Physical Object',
            'phpr' : 'Phenomenon or Process',
            'phsf' : 'Physiologic Function',
            'phsu' : 'Pharmacologic Substance',
            'plnt' : 'Plant',
            'podg' : 'Patient or Disabled Group',
            'popg' : 'Population Group',
            'prog' : 'Professional or Occupational Group',
            'pros' : 'Professional Society',
            'qlco' : 'Qualitative Concept',
            'qnco' : 'Quantitative Concept',
            'rcpt' : 'Receptor',
            'rept' : 'Reptile',
            'resa' : 'Research Activity',
            'resd' : 'Research Device',
            'rnlw' : 'Regulation or Law',
            'sbst' : 'Substance',
            'shro' : 'Self-help or Relief Organization',
            'socb' : 'Social Behavior',
            'sosy' : 'Sign or Symptom',
            'spco' : 'Spatial Concept',
            'strd' : 'Steroid',
            'tisu' : 'Tissue',
            'tmco' : 'Temporal Concept',
            'topp' : 'Therapeutic or Preventive Procedure',
            'virs' : 'Virus',
            'vita' : 'Vitamin',
            'vtbt' : 'Vertebrate'
            }

class counter:
    count = 0
    def __init__(self):
        self.__class__.count += 1

# print Header row with column labels:
print "dat_ind\trecordfile\t",

# print  Neo4J columns 3-9
# print PMID, txt (PhrText), CUI, CanMatch, CanPref, sem, semTypeDesc, UI,
print "PMID\tPhrTex\tCUI\tmatch\tCanPref\tsem\tsemTypeDesc\tUI\t",

# print ML columns
# Score, UI_2, cui, ui, Cons_ct, v/c, c/v, PhrLen, utt_ct, sem_ct, can_ct, 
# syn_ct, txt, space_ct / txt, Txt / space_ct,  Space_ct / c_ct, Space_ct / v_ct,
# Space_ct / (c/v), Space_ct / PhrLen, Space_ct / sem_ct, Space_ct / can_ct,
# utt_ct/score, utt_ct/MapScr


print "Score\tUI_2\tcui\tui\tCons_ct\tv/c\tc/v\tPhrLen\tutt_ct\tsem_ct\tcan_ct\t",
print "syn_ct\ttxt\tspace_ct / txt\tTxt / space_ct\tSpace_ct / c_ct\tSpace_ct / v_ct\t",
print "Space_ct / (c/v)\tSpace_ct / PhrLen\tSpace_ct / sem_ct\tSpace_ct / can_ct\t",
print "utt_ct/score\tutt_ct/MapScr"

handleMMOs(mmos)
