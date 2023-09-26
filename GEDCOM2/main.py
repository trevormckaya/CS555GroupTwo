# I pledge my honor that I have abided by the Stevens Honor System - Corey Heckel

from typing import List, Dict



tags: List[str] = ['0 INDI', '1 NAME', '1 SEX', '1 BIRT', '1 DEAT', '1 FAMC',
                  '1 FAMS', '1 FAM', '1 MARR', '1 HUSB', '1 WIFE', '1 CHIL',
                  '1 DIV', '2 DATE', '0 HEAD', '0 TRLR', '0 NOTE']

path = 'GEDCOMTestFile'

individuals: Dict[str, Dict[str, str]] = {}
families: Dict[str, Dict[str, str]] = {}

currIndividual: Dict[str, str] = {}
currFamily: Dict[str, str] = {}
currID: str = ""

with open(path, "r") as file:
    for line in file:
        parts: List[str] = line.rstrip("\n").split(' ', 2)
        count: int = len(parts)

        level: str = parts[0]
        tag: str = parts[1]

        if count == 2:
            if tag == 'INDI':
                if currIndividual:
                    individuals[currIndividual['ID']] = currIndividual
                currIndividual = {'ID': parts[0]}
            elif tag == 'FAM':
                if currFamily:
                    families[currFamily['ID']] = currFamily
                currFamily = {'ID': parts[0]}
        elif parts[2] in ['INDI', 'FAM']:
            _id: str = parts[1]
            tag: str = parts[2]
            if tag == 'INDI':
                if currIndividual:
                    individuals[currIndividual['ID']] = currIndividual
                currIndividual = {'ID': _id}
            elif tag == 'FAM':
                if currFamily:
                    families[currFamily['ID']] = currFamily
                currFamily = {'ID': _id}
        else:
            args: str = parts[2]
            if currIndividual:
                currIndividual[tag] = args
            elif currFamily:
                currFamily[tag] = args

        if currID and 'ID' in currFamily:
            famID = currFamily['ID'].replace('@', '')
            childList = currFamily.get('CHIL', '').split()
            childList.append(args)
            currFamily['CHIL'] = ' '.join(childList)

if currIndividual:
    individuals[currIndividual['ID']] = currIndividual
if currFamily:
    families[currFamily['ID']] = currFamily

# Sort and print individuals by unique identifier
sortedIndividuals = sorted(individuals.items(), key=lambda x: x[0])
for indiID, indiData in sortedIndividuals:
    name = indiData.get('NAME', 'N/A')
    print(f'Individual ID: {indiID}, Name: {name}')

# Sort and print spouses for each family by unique family identifier
sortedFamilies = sorted(families.items(), key=lambda x: x[0])
for famID, famData in sortedFamilies:
    husbandID = famData.get('HUSB')
    wifeID = famData.get('WIFE')

    if husbandID != 'N/A':
        husbandName = individuals.get(husbandID, {}).get('NAME')
    else:
        husbandName = 'N/A'

    if wifeID != 'N/A':
        wifeName = individuals.get(wifeID, {}).get('NAME')
    else:
        wifeName = 'N/A'

    print(f'Family ID: {famID}')
    print(f'  Husband ID: {husbandID}, Name: {husbandName}')
    print(f'  Wife ID: {wifeID}, Name: {wifeName}')
