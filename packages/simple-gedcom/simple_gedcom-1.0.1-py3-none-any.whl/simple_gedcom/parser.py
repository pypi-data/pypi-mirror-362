from typing import List
from .elements import GedcomElement, Person, SourceElement, FamilyElement

class GedcomParser:
    """Simple GEDCOM parser for extracting individual data"""

    def __init__(self):
        self.__root_element = GedcomElement(-1, '', 'ROOT', '')
        self.__individuals = {}
        self.__families = {}
        self.__sources = {}

    def parse_file(self, file_path: str, strict: bool = False):
        """Parse GEDCOM file"""
        with open(file_path, 'rb') as gedcom_file:
          gedcom_lines = gedcom_file.readlines()

        # Reset state
        self.__root_element = GedcomElement(-1, '', 'ROOT', '')
        self.__individuals = {}
        self.__families = {}
        self.__sources = {}

        # Parse lines
        element_stack = [self.__root_element]

        for line_num, line in enumerate(gedcom_lines, 1):
            try:
                # Handle encoding
                try:
                    line_str = line.decode('utf-8-sig').rstrip('\r\n')
                except UnicodeDecodeError:
                    line_str = line.decode('utf-8', errors='replace').rstrip('\r\n')

                if not line_str.strip():
                    continue

                element_stack = self._parse_line(line_str, element_stack, strict)

            except Exception as e:
                if strict:
                    raise ValueError(f"Error parsing line {line_num}: {e}")
                continue

    def _parse_line(self, line: str, element_stack: List[GedcomElement], strict: bool) -> List[GedcomElement]:
        """Parse single GEDCOM line"""
        parts = line.split(' ', 2)
        if len(parts) < 2:
            return element_stack

        try:
            level = int(parts[0])
        except ValueError:
            return element_stack

        # Handle pointer vs tag
        if parts[1].startswith('@') and parts[1].endswith('@'):
            if len(parts) < 3:
                return element_stack
            pointer = parts[1]
            tag_and_value = parts[2].split(' ', 1)
            tag = tag_and_value[0]
            value = tag_and_value[1] if len(tag_and_value) > 1 else ''
        else:
            pointer = ''
            tag = parts[1]
            value = parts[2] if len(parts) > 2 else ''

        # Create element
        if tag == 'INDI':
            element = Person(level, pointer, tag, value)
            if pointer:
                self.__individuals[pointer] = element
        elif tag == 'FAM':
            element = FamilyElement(level, pointer, tag, value)
            if pointer:
                self.__families[pointer] = element
        elif tag == 'SOUR':
            element = SourceElement(level, pointer, tag, value)
            if pointer:
                self.__sources[pointer] = element
        else:
            element = GedcomElement(level, pointer, tag, value)

        # Build hierarchy
        while len(element_stack) > 1 and element_stack[-1].get_level() >= level:
            element_stack.pop()

        parent = element_stack[-1]
        parent.add_child(element)
        element_stack.append(element)

        return element_stack

    def get_root_child_elements(self) -> List[GedcomElement]:
        """Get all top-level elements"""
        return self.__root_element.get_children()

    def get_parents(self, individual: Person) -> List[Person]:
        """Get parents of an individual"""
        parents = []
        individual_pointer = individual.get_pointer()

        if not individual_pointer:
            return parents

        # Find families where this individual is a child
        for family in self.__families.values():
            if individual_pointer in family.get_children():
                husband_pointer = family.get_husband()
                wife_pointer = family.get_wife()

                if husband_pointer and husband_pointer in self.__individuals:
                    parents.append(self.__individuals[husband_pointer])

                if wife_pointer and wife_pointer in self.__individuals:
                    parents.append(self.__individuals[wife_pointer])

        return parents

    def get_father_mother(self, individual: Person) -> tuple:
        """Get father and mother, using family roles first, then gender"""
        father = mother = None
        individual_pointer = individual.get_pointer()

        if not individual_pointer:
            return (father, mother)

        # Find families where this individual is a child
        for family in self.__families.values():
            if individual_pointer in family.get_children():
                husband_pointer = family.get_husband()
                wife_pointer = family.get_wife()

                # Use family roles first
                if husband_pointer and husband_pointer in self.__individuals:
                    father = self.__individuals[husband_pointer]

                if wife_pointer and wife_pointer in self.__individuals:
                    mother = self.__individuals[wife_pointer]

        # If we didn't find both from family roles, fall back to any remaining parents by gender
        if not father or not mother:
            all_parents = self.get_parents(individual)
            for parent in all_parents:
                # Skip if already assigned by family role
                if parent == father or parent == mother:
                    continue

                if not father and parent.get_gender() == 'M':
                    father = parent
                elif not mother and parent.get_gender() == 'F':
                    mother = parent
                elif not father and not mother:
                    # If no gender info, assign to first available slot
                    if not father:
                        father = parent
                    else:
                        mother = parent

        return (father, mother)

    def get_person_list(self) -> List[dict]:
        """Get people data with one row per person"""
        people = []

        # Go through all individuals
        for person in self.__individuals.values():
            pointer = person.get_pointer()
            first_name, last_name = person.get_name()
            birth_date, birth_place = person.get_birth_date_place()
            death_date, death_place = person.get_death_date_place()

            # Get father and mother
            father, mother = self.get_father_mother(person)
            father_first_name = father_last_name = father_pointer = ''
            mother_first_name = mother_last_name = mother_pointer = ''

            if father:
                father_first_name, father_last_name = father.get_name()
                father_pointer = father.get_pointer()
            if mother:
                mother_first_name, mother_last_name = mother.get_name()
                mother_pointer = mother.get_pointer()

            # Base person data
            person_data = {
                'Person ID': pointer,
                'First Name': first_name,
                'Last Name': last_name,
                'Birth Date': birth_date,
                'Birth Place': birth_place,
                'Death Date': death_date,
                'Death Place': death_place,
                'Father First Name': father_first_name,
                'Father Last Name': father_last_name,
                'Mother First Name': mother_first_name,
                'Mother Last Name': mother_last_name
            }

            people.append(person_data)

        return people


    def get_person_sources(self) -> List[dict]:
        """Get people data with one row per person-source combination"""
        person_source_list = []

        # Go through all individuals
        for person in self.__individuals.values():
            pointer = person.get_pointer()
            person_sources = person.get_all_person_sources()

            # Base person data
            base_person_data = {
                'Person ID': pointer
            }

            if person_sources:
                # Create one row per source
                for source_pointer in person_sources:
                    if source_pointer in self.__sources:
                        source = self.__sources[source_pointer]
                        row_data = base_person_data.copy()
                        row_data.update({
                            'Source ID': source.get_pointer(),
                            'Source Title': source.get_title(),
                            'Source Author': source.get_author(),
                            'Source Publication': source.get_publication(),
                            'Source Repository': source.get_repository()
                        })
                        person_source_list.append(row_data)

        return person_source_list

    def get_all_sources(self) -> List[SourceElement]:
        """Get all source records in the file"""
        return list(self.__sources.values())

    def get_source_by_pointer(self, pointer: str) -> SourceElement:
        """Get a source by its pointer/ID"""
        return self.__sources.get(pointer)
