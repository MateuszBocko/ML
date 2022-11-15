# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import re
import openpyxl
import tqdm
import shutil
import pathlib  
from itertools import chain
from PyPDF2 import PdfReader
import pandas as pd

print('PROCESS HAS BEEN STARTED!')

class PDF_converter():
    def __init__(self, path_to_pdf, list_of_laboratory_tests, static_cols):
        self.static_cols = static_cols
        self.new_text = None
        self.text = self.read_pdf(path_to_pdf)
        self.list_of_laboratory_tests = list_of_laboratory_tests
        self.final_dict = self.dictionary_creation_v1()
        self.df_merged = None
        self.split_values_by_dates()
        self.list_to_dictionary()
        self.aesthetic_changes()
        self.create_merged_df()
        
    def read_pdf(self, path_to_pdf):
        reader = PdfReader(path_to_pdf)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        return text
    
    def first_last(self, data, index, debug='N'): 
        if_empty_index = 0 
        substring = None
        
        # create substrigs word1:word2
        # find fist word in string from pdf
        while True:
            try:
                first = re.search(data[index], self.new_text).start()
                break
            except:
                substring = 'Brak danych' # used polish due to the fact end user need it in polish
                break
                
        # find second word in string from pdf
        while True:
            try:
                last = re.search(data[index+1+if_empty_index], self.new_text).start()
                break
            except:
                if_empty_index += 1      

        # sometimes test names contains '(' - it has to be treated diffirent way
        number_of_characters_of_test=len(data[index])
        if debug=='Y':
            if '(' in data[index]:
                number_of_characters_of_test = len(data[index])-1
            else:
                number_of_characters_of_test = len(data[index])+1
            
        if substring is None:
            substring = self.new_text[first+number_of_characters_of_test:last]

        return substring
    
    def dictionary_creation_v1(self):
        # split main string from pdf
        self.text = self.text.replace(';', ' ;')
        self.new_text = (';').join((';').join(self.text.split('\n')).split(';'))
        
        indices = [index for index in range(len(self.new_text)) if self.new_text.startswith('01 / 2015Wydrukowano z systemu:', index)]
        elements_to_remove = []
        for index in indices:
            elements_to_remove.append(self.new_text[index:(index+124)])

        for element in elements_to_remove:
            self.new_text= self.new_text.replace(element, '')

        # create empty dict
        final_dict = {}

        # feed the dictionary using first_last function
        for key_index in range(0,len(self.list_of_laboratory_tests)-1):
            final_dict[self.list_of_laboratory_tests[key_index]] = self.first_last(data=self.list_of_laboratory_tests, index=key_index, debug='Y')

        return final_dict
    
    def split_values_by_dates(self):
        # regex date format
        rx = r"(\d{4}-\d{2}-\d{2})"

        # go through all the keys in dictionary and split the value by dates
        for key in self.final_dict.keys():
            temp_key = self.final_dict[key]
            temp_value = re.split(rx, temp_key)

            if 'Strona' in temp_value[0]:
                temp_value.pop(0)
            elif temp_value[0] == '':
                temp_value.pop(0)
            elif 'Płeć' in temp_value[0]:
                temp_value.pop(0)
                
            self.final_dict[key] = temp_value
            
    def list_to_dictionary(self):
        # change the format of values from list to dictionary
        for key in self.final_dict.keys():
            temp_dict = dict(zip(list(self.final_dict[key])[::2], list(self.final_dict[key])[1::2]))
            for temp_key, temp_value in temp_dict.items():
                new_value = ' '.join(temp_value.replace(';;','; ').strip().split())
                temp_dict[temp_key] = new_value.split('; ')

            self.final_dict[key] = temp_dict

    def aesthetic_changes(self):
        # remove useless elements from 'KREATYNINA W SUROWICY'
        for key, value in self.final_dict['KREATYNINA W SUROWICY'].items():
            self.final_dict['KREATYNINA W SUROWICY'][key] = value[0][:8].replace(' ','')+'|'+value[1][23:]
        
        # remove all elements that length is equal 1 in 'MOCZ - BADANIE OGÓLNE'
        for key in self.final_dict['MOCZ - BADANIE OGÓLNE'].keys():
            temp_list = self.final_dict['MOCZ - BADANIE OGÓLNE'][key]
            self.final_dict['MOCZ - BADANIE OGÓLNE'][key] = [x for x in temp_list if len(x)>1]
            
    def create_merged_df(self):
        list_to_change = ['MOCZ - BADANIE OGÓLNE',
                          'MORFOLOGIA 5 DIFF',
                          'MORFOLOGIA 5 DIFF Z RETIKULOCYTAMI', 
                          'POCT PARAMETRY KRYTYCZNE',
                          'POCT SARS \\(MET. PCR\\)',
                          'PT \\(CZAS PROTROMBINOWY\\)',
                          'TIBC'
                         ]
        
        df_merged = pd.DataFrame([])
        for column in list_to_change:    
            # split values -> convert into better format (some test contains another set of test inside them)
            for key, value in self.final_dict[column].items():
                new_value = []
                for element in range(len(value)):
                    temp_element = value[element].replace(';',' ').replace(' #','#').split(' ', 1)
                    new_value.append(dict([temp_element]))
                
                # exception for key NIEDOJRZALE and LEUKOCYTY IN MOCZ -> TO BE OPTIMIZED
                granulocyty = 0
                leukocyty = 0
                for dict_ in new_value:
                    if list(dict_.keys())[0] == 'NIEDOJRZAŁE' and granulocyty==0:
                        dict_['NIEDOJRZAŁE#'] = dict_.pop('NIEDOJRZAŁE')
                        granulocyty=+1
                    if list(dict_.keys())[0] == 'LEUKOCYTY' and leukocyty==0:
                        leukocyty=+1 
                    elif list(dict_.keys())[0] == 'LEUKOCYTY' and leukocyty==1:
                        dict_['LEUKOCYTY WBC'] = dict_.pop('LEUKOCYTY')
                
                self.final_dict[column][key] = new_value

            # convert multiple dicts into one
            for key in self.final_dict[column].keys():
                self.final_dict[column][key] = dict(chain.from_iterable(d.items() for d in self.final_dict[column][key]))
            
            # create temporary df
            temp_df = pd.DataFrame(self.final_dict[column])
            temp_df = pd.concat([temp_df], keys=[column])               

            # concat temporary df with the final df
            df_merged = pd.concat([df_merged, temp_df], sort=True)

            # remove those columns that were converted into df from main dictionary
            self.final_dict.pop(column, None)
        
        # transpose final view
        self.df_merged = df_merged.transpose()
        
        return self.df_merged
        
    def final_df(self):
        # create data frame from main dict, transpose it, add next index to row and transpose again
        df = pd.DataFrame(self.final_dict)
        df = (pd.concat([df.transpose()], keys=['None'])).transpose()
        
        # concat main df with df_merged
        df_final = (pd.concat([self.df_merged, df])).groupby(level=0).sum().sort_index(ascending=False)
        
        return df_final
    
    def df_processing(self, df):
        # some additional changes to df
        df = df.replace(0,'-')
        
        temp_df = df.copy()
        temp_df = temp_df.astype('string').transpose()
        
        for column in temp_df.columns:
            temp_df[column] = temp_df[column].str.replace('[#();:]', '', regex=True) # remove special characters
            temp_df[column] = temp_df[column].astype('string').str.split("norma", expand = False) # convert to string and split into two elements
        
        df = temp_df.transpose()
        
        for column in df:

            if column[0]=='None':
                if column==('None', 'KREATYNINA W SUROWICY'):
                    df[column] = df[column].apply(lambda x: ' '.join((x[0]).split()[-2:])) # the first part of the table need only some part of first element
                else:
                    df[column] = df[column].apply(lambda x: ' '.join((x[0][2:]).split()[-2:])) # the first part of the table need only some part of first element
            else:
                df[column] = df[column].apply(lambda x: x[0]) # the second part of the table need only first element of the list
                
        df = df.replace('','-')
        
        for static_col in range(len(self.static_cols)-1):
            # add new col with static value
            # create list with value (len has to be same as count of df)
            to_be_added = [self.first_last(data=self.static_cols, index=static_col, debug='N') for row in range(df[df.columns[1]].count())]
            # add new column
            df = df.assign(temp=pd.Series(to_be_added).values)
            # rename it to proper name
            df.rename(columns = {'temp':self.static_cols[static_col]}, inplace = True)
        df = df.astype('string')    
        return df
    
    def save_as_excel(self, df, path_to_save):
        df.to_excel(path_to_save+'.xlsx')
        
def iterate_over_all_files(path_to_folder):
    # create empty df
    total_df = pd.DataFrame()
    # create list of files in passed path
    list_of_files = os.listdir(path_to_folder)
    
    # check if folder named results exists
    if os.path.exists(path_to_folder+'/results'):
        shutil.rmtree(path_to_folder+'/results')
    
    # create new folder    
    os.mkdir(path_to_folder+'/results')
    os.chdir(path_to_folder)
    
    list_of_files_to_be_checked = []
    for file_index in tqdm.tqdm(range(0, len(list_of_files))):
        file = list_of_files[file_index]
        # check if file format is correct
        file_extension = pathlib.Path(file).suffix
        
        if file_extension == '.pdf':
            # run class
            try:
                pdf_reader = PDF_converter(path_to_pdf=file, list_of_laboratory_tests=temp, static_cols=static_cols)
                final_df = pdf_reader.final_df()
                processed_df = pdf_reader.df_processing(final_df)
                new_value=[file.split('.')[0] for row in range(processed_df[processed_df.columns[1]].count())] 
                processed_df = processed_df.assign(ID=pd.Series(new_value).values) # the name of the file is going to be a unique ID of patient
                pdf_reader.save_as_excel(processed_df, path_to_save = 'results/' + file.split('.')[0] +'.xlsx')
                
                first_count = len(processed_df.index.get_level_values(0))
                processed_df = processed_df.loc[(processed_df.index >= '2000-01-01') & (processed_df.index <= '2030-12-07')]
                second_count = len(processed_df.index.get_level_values(0))
                if second_count < first_count:
                    list_of_files_to_be_checked.append(file)
            except:
                list_of_files_to_be_checked.append(file)
		#print(f'File {file} was not converted')
                pass
        
        # create df combined from all the pdf's
        if total_df.empty == True:
            total_df = processed_df.copy()
        else:
            try:
                total_df = pd.concat([total_df, processed_df])
            except:
                print(f'File {file} was not added to the main df')
                
    # fill N/A and sort columns            
    total_df.fillna('-', inplace=True)
    total_df = total_df[sorted(total_df.columns)]
    
    # save total_df
    total_df.to_excel('results/Combined_data.xlsx')
    print('DATA CONVERTED!')
    print('People to check:')
    for person in list_of_files_to_be_checked:
        print(person)
    return total_df

temp = ['25-OH-WITAMINA D',
               'ALAT',
               'ALBUMINA \\( ALBUMINY/GLOBULINY\\)',
               'AMYLAZA W SUROWICY',
               'ANTYGEN I TOKSYNA A I B CLOSTRIDIOIDES DIFFICILE W KALE',
               'APTT',
               'ASPAT',
               'BADANIE GRUPY KRWI Z CZYNNIKIEM RH',
               'BIAŁKO CAŁKOWITE',
               'BILIRUBINA BEZPOŚREDNIA I POŚREDNIA',
               'BILIRUBINA CAŁKOWITA',
               'BNP \\(PEPTYD NATRIURETYCZNY\\)',
               'C3-SKŁADOWA DOPEŁNIACZA',
               'C4-SKŁADOWA DOPEŁNIACZA',
               'CA 125',
               'CA 15.3',
               'CA 19.9',
               'CEA',
               'CHLORKI',
               'CHOLESTEROL  LDL',
               'CHOLESTEROL CAŁKOWITY',
               'CHOLESTEROL HDL',
               r'CITO SARS COV-2; GRYPA A/B MET. PCR',
               'CK - KINAZA KREATYNOWA',
               'CK-MB \\(MASS\\)', 
               'C-PEPTYD',
               'CRP ULTRACZUŁE',
               'CRP WYSOKOCZUŁE',
               'CYKLOSPORYNA RCSA',
               'CZYNNIK REUMATOIDALNY \\(RF\\)',
               'D-DIMERY \\(MET. ILOŚCIOWA\\)',
               'DHEA-S',
               'DIGOKSYNA',
               'ESTRADIOL',
               'FERRYTYNA',
               'FERRYTYNA METODA NEFELOMETRYCZNA',
               'FIBRYNOGEN - AKTYWNOŚĆ',
               'FOSFATAZA ALKALICZNA',
               'FOSFOR NIEORGANICZNY',
               'FSH',
               'FT 3',
               'FT 4',
               'GAZOMETRIA',
               'GGTP',
               'GLUKOZA',
               'GLUKOZA 0 MIN',
               'HBE ANTYGEN',
               'HBS ANTYGEN',
               'HEMOGLOBINA GLIK. A1C',
               'HIT - MAŁOPŁYTKOWOŚĆ POHEPARYNOWA',
               'IGF-1 \\(INSULINOPODOBNY CZYNNIK WZROSTU 1\\)',
               'INSULINA',
               'INTERLEUKINA-6',
               'KAŁ - KREW UTAJONA \\(MET. CHROMATOGRAFICZNA\\)',
               'KORTYZOL',
               'KREATYNINA W SUROWICY',
               'KWAS FOLIOWY',
               'KWAS MOCZOWY',
               'LDH',
               'LH',
               'LEGIONELLA - ANTYGEN',
               'LIPAZA',
               'MAGNEZ',
               'MOCZ - BADANIE OGÓLNE',
               'MOCZ PORANNY: BIAŁKO',
               'MOCZ PORANNY: KREATYNINA',
               'MOCZ PORANNY: SÓD I POTAS',
               'MOCZNIK',
               'MORFOLOGIA',
               'MORFOLOGIA 5 DIFF',
               'MORFOLOGIA 5 DIFF Z RETIKULOCYTAMI',
               'MULTIPLEKS PCR - INFEKCJE ŻOŁĄDKOWO-JELITOWE',
               'MYO \\(MIOGLOBINA\\)'
               'NT-PROBNP',
               'OSMOLALNOŚĆ SUROWICY',
               'OSMOLALNOŚĆ MOCZU',
               'PATOGENY ODDECHOWE- MULTITEST PCR \\(JAKOŚCIOWO\\)'
               'PARATHORMON',
               'PŁYTKI W KRWI CYTRYNIANOWEJ',
               'POCT PARAMETRY KRYTYCZNE',
               'POCT SARS \\(MET. PCR\\)',
               'P/CIAŁA DS.DNA NCX IGG MET. ELISA',
               'P/CIAŁA P/BETA2 GLIKOPROTEINIE IGG IGM',
               'P/CIAŁA P/KARDIOLIPINOWE IGM, IGG',
               'P/CIALA ANTY-HBC II',
               'P/CIAŁA ANTY HBE',
               'P/CIAŁA ANTY-HAV IGG',
               'P/CIAŁA ANTY-HAV IGM',
               'P/CIALA ANTY-HBS',
               'P/CIAŁA ANTY HBC IGM',
               'P/CIAŁA ANTY-HCV',
               'P/CIAŁA ANTY-HIV',
               'P/CIAŁA ANTY-CMV IGG',
               'P/CIAŁA ANTY-CMV IGM',
               'P/CIAŁA CANCA MET.ELISA',
               'P/CIAŁA P ANCA MET.ELISA',
               'P/CIAŁA ANTY-TG',
               'P/CIAŁA ANTY-TPO',
               'POCT_CRP_DDIMERY_TROPONINA_PCT_NTPROBNP',
               'POTAS',
               'PROKALCYTONINA',
               'PRÓBA ZGODNOŚCI SEROLOGICZNEJ',
               'PSA',
               'PSA-WOLNY',
               'PT \\(CZAS PROTROMBINOWY\\)',
               'ROZMAZ - MIKROSKOPOWY',
               'SARS COV-2',
               'SHBG \\(GLOBULINA WIĄŻĄCA HORMONY PŁCIOWE\\)'
               'SÓD',
               'STFR \\(ROZPUSZCZALNY RECEPTOR TRANSFERYNY\\)',
               'TACROLIMUS',
               'TESTOSTERON',
               'TIBC',
               'TOKSYNA A I B CLOSTRIDIOIDES DIFFICILE W KALE METODĄ PCR',
               'TOTAL BETA – HCG',
               'TRANSFERYNA',
               'TROPONINA I',
               'TRÓJGLICERYDY',
               'TSH 3-CIA GENERACJA',
               'WAPŃ CAŁKOWITY',
               'WAPŃ SKORYGOWANY',
               'WITAMINA B12',
               'ŻELAZO'
       ]
temp.append('Badania laboratoryjne')

static_cols = ['Badania laboratoryjne - antybiogram',
               'Podane leki',
               'Badania diagnostyczne',
               'Epikryza'
              ]

os.chdir('dane')
path_to_pdf= os.getcwd()

if __name__=='__main__':
	df = iterate_over_all_files(path_to_pdf)
	os.system("pause")
