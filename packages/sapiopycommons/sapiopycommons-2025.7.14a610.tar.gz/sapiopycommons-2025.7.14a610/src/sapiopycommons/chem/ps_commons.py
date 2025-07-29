"""
Parallel Synthesis Commons
Author: Yechen Qiao
"""
import itertools
import json
from dataclasses import dataclass
from typing import Any

from indigo import IndigoObject, IndigoException
from sapiopycommons.chem.IndigoMolecules import indigo, get_aromatic_dearomatic_forms, renderer


class SerializableQueryMolecule:
    mol_block: str
    smarts: str
    render_svg: str

    @staticmethod
    def create(query_molecule: IndigoObject):
        aromatic, dearomatic = get_aromatic_dearomatic_forms(query_molecule)
        ret: SerializableQueryMolecule = SerializableQueryMolecule()
        ret.mol_block = aromatic.molfile()
        ret.smarts = aromatic.smarts()
        ret.render_svg = renderer.renderToString(dearomatic)
        return ret

    def to_json(self) -> dict[str, Any]:
        """
        Save the SerializableQueryMolecule to a JSON string.
        :return: A JSON string representation of the query molecule.
        """
        return {
            "mol_block": self.mol_block,
            "smarts": self.smarts,
            "render_svg": self.render_svg
        }


class SerializableMoleculeMatch:
    """
    A serializable match that stores and loads a match that can be serialized to JSON.
    """
    _query_atom_to_atom: dict[int, int]
    _query_bond_to_bond: dict[int, int]
    _query_molecule_file: str
    _matching_molecule_file: str
    _query_molecule: IndigoObject
    _matching_molecule: IndigoObject
    _record_id: int  # Only when received from Sapio.

    @property
    def record_id(self) -> int:
        """
        Get the record ID of the match.
        :return: The record ID.
        """
        return self._record_id

    @property
    def query_atom_indexes(self) -> set[int]:
        return set(self._query_atom_to_atom.keys())

    @property
    def matching_atom_indexes(self) -> set[int]:
        return set(self._query_atom_to_atom.values())

    @property
    def matching_molecule_copy(self) -> IndigoObject:
        return self._matching_molecule.clone()

    def __str__(self):
        return json.dumps(self.to_json())

    def __hash__(self):
        return hash(self._query_molecule.smarts())

    def __eq__(self, other):
        if not isinstance(other, SerializableMoleculeMatch):
            return False
        if self._query_atom_to_atom == other._query_atom_to_atom and \
                self._query_bond_to_bond == other._query_bond_to_bond and \
                self._query_molecule_file == other._query_molecule_file and \
                self._matching_molecule_file == other._matching_molecule_file and \
                self._record_id == other._record_id:
            return True
        if self._query_molecule.smarts() != other._query_molecule.smarts():
            return False
        return are_symmetrical_subs(self, other)

    def mapAtom(self, atom: IndigoObject) -> IndigoObject | None:
        if not self._query_atom_to_atom or atom.index() not in self._query_atom_to_atom:
            return None
        index = self._query_atom_to_atom[atom.index()]
        return self._matching_molecule.getAtom(index)

    def mapBond(self, bond: IndigoObject) -> IndigoObject | None:
        if not self._query_bond_to_bond or bond.index() not in self._query_bond_to_bond:
            return None
        index = self._query_bond_to_bond[bond.index()]
        return self._matching_molecule.getBond(index)

    def to_json(self) -> dict[str, Any]:
        """
        Save the SerializableMoleculeMatch to a JSON string.
        :return: A JSON string representation of the match.
        """
        return {
            "query_molecule_file": self._query_molecule_file,
            "matching_molecule_file": self._matching_molecule_file,
            "query_atom_to_atom": self._query_atom_to_atom,
            "query_bond_to_bond": self._query_bond_to_bond,
            "record_id": self._record_id
        }

    @staticmethod
    def from_json(json_dct: dict[str, Any]) -> 'SerializableMoleculeMatch':
        """
        Load a SerializableMoleculeMatch from a JSON string.
        :param json_dct: A JSON string representation of the match.
        :return: A new SerializableMoleculeMatch instance.
        """
        smm = SerializableMoleculeMatch()
        smm._query_atom_to_atom = {}
        for key, value in json_dct.get("query_atom_to_atom", {}).items():
            smm._query_atom_to_atom[int(key)] = int(value)
        smm._query_bond_to_bond = {}
        for key, value in json_dct.get("query_bond_to_bond", {}).items():
            smm._query_bond_to_bond[int(key)] = int(value)
        smm._query_molecule_file = json_dct.get("query_molecule_file")
        smm._matching_molecule_file = json_dct.get("matching_molecule_file")
        smm._query_molecule = indigo.loadQueryMolecule(smm._query_molecule_file)
        smm._matching_molecule = indigo.loadMolecule(smm._matching_molecule_file)
        smm._record_id = json_dct.get("record_id", 0)  # Default to 0 if not present
        return smm

    @staticmethod
    def create(query_molecule: IndigoObject, matching_molecule: IndigoObject,
               match: IndigoObject, query_mol_atom_index_filter: set[int] | None = None) -> 'SerializableMoleculeMatch':
        """
        Create a SerializableMoleculeMatch from a query molecule, matching molecule, and match.
        :param query_molecule: The query molecule.
        :param matching_molecule: The matching molecule.
        :param match: The match object containing atom mappings.
        :param query_mol_atom_index_filter: Optional list of atom indexes to filter the query molecule atoms.
        :return: A new SerializableMoleculeMatch instance.
        """
        smm = SerializableMoleculeMatch()
        smm._query_atom_to_atom = {}
        smm._query_bond_to_bond = {}
        smm._query_molecule = query_molecule.clone()
        smm._matching_molecule = matching_molecule.clone()
        smm._query_molecule_file = query_molecule.molfile()
        smm._matching_molecule_file = matching_molecule.molfile()
        smm._record_id = 0

        for qatom in query_molecule.iterateAtoms():
            if query_mol_atom_index_filter and qatom.index() not in query_mol_atom_index_filter:
                continue
            concrete_atom = match.mapAtom(qatom)
            if concrete_atom is None:
                continue
            smm._query_atom_to_atom[qatom.index()] = concrete_atom.index()

        qbond: IndigoObject
        for qbond in query_molecule.iterateBonds():
            if query_mol_atom_index_filter:
                if (qbond.source().index() not in query_mol_atom_index_filter or
                        qbond.destination().index() not in query_mol_atom_index_filter):
                    continue
            concrete_bond = match.mapBond(qbond)
            if concrete_bond is None:
                continue
            smm._query_bond_to_bond[qbond.index()] = concrete_bond.index()
        return smm

    def get_matched_molecule_copy(self):
        return self._matching_molecule.clone()


def is_reaction_atom_map_completed(q_reaction: IndigoObject) -> bool:
    """
    Tests each atom in product of query reaction.
    :param q_reaction: The query reaction to test.
    :return: True if and only if for every atom that is not an R-Site, it has a mapping number.
    """
    for product in q_reaction.iterateProducts():
        for atom in product.iterateAtoms():
            if atom.isRSite():
                continue
            map_num = q_reaction.atomMappingNumber(atom)
            if map_num == 0:
                return False
    return True


@dataclass
class ReplacementReaction:
    """
    A replacement reaction stores reactio template with 1 reactant replaced by specific user match.
    """
    reaction: IndigoObject
    reaction_reactant: IndigoObject
    replacement_reactant: IndigoObject
    replacement_query_reaction_match: SerializableMoleculeMatch


# noinspection PyProtectedMember
def highlight_mol_substructure_serial_match(molecule: IndigoObject, serializable_match: SerializableMoleculeMatch):
    """
    Highlight the substructure in the molecule based on the SerializableMoleculeMatch.
    :param molecule: The molecule to highlight.
    :param serializable_match: The SerializableMoleculeMatch containing atom mappings.
    """
    for qatom in serializable_match._query_molecule.iterateAtoms():
        atom = serializable_match.mapAtom(qatom)
        if atom is None:
            continue
        atom.highlight()

        for nei in atom.iterateNeighbors():
            if not nei.isPseudoatom() and not nei.isRSite() and nei.atomicNumber() == 1:
                nei.highlight()
                nei.bond().highlight()

    for bond in serializable_match._query_molecule.iterateBonds():
        bond = serializable_match.mapBond(bond)
        if bond is None:
            continue
        bond.highlight()


def clear_highlights(molecule: IndigoObject):
    """
    Clear all highlights in the molecule.
    :param molecule: The molecule to clear highlights from.
    """
    for atom in molecule.iterateAtoms():
        atom.unhighlight()
    for bond in molecule.iterateBonds():
        bond.unhighlight()


def clear_reaction_highlights(reaction: IndigoObject):
    """
    Clear all highlights in the reaction.
    :param reaction: The reaction to clear highlights from.
    """
    for reactant in reaction.iterateReactants():
        clear_highlights(reactant)
    for product in reaction.iterateProducts():
        clear_highlights(product)


def reserve_atom_mapping_number_of_search_result(q_reaction: IndigoObject, q_reactant: IndigoObject,
                                                 new_reaction_reactant: IndigoObject, new_reaction: IndigoObject,
                                                 sub_match: SerializableMoleculeMatch) -> None:
    """
    Set the atom mapping number on the query molecule based on the atom mapping number of the sub_match molecule, if it exists.
    :param new_reaction: The new reaction where the new reaction's reactant is found. This will be the target reaciton to write AAM to.
    :param new_reaction_reactant: The new reaction's reactant where the AAM will be written to.
    :param q_reactant: The query reactant from the query reaction that is being matched.
    :param q_reaction: The query reaction that contains the query reactant for the sub_match.
    :param sub_match: The substructure search match obtained from indigo.substructureMatcher(mol).match(query).
    """
    for query_atom in q_reactant.iterateAtoms():
        concrete_atom = sub_match.mapAtom(query_atom)
        if concrete_atom is None:
            continue
        reaction_atom = q_reactant.getAtom(query_atom.index())
        map_num = q_reaction.atomMappingNumber(reaction_atom)
        if map_num:
            concrete_atom = new_reaction_reactant.getAtom(concrete_atom.index())
            new_reaction.setAtomMappingNumber(concrete_atom, map_num)


def clean_product_aam(reaction: IndigoObject):
    """
    Remove atom mappings from product that are not present in the reactants.
    """
    existing_mapping_numbers = set()
    for reactant in reaction.iterateReactants():
        for atom in reactant.iterateAtoms():
            map_num = reaction.atomMappingNumber(atom)
            if map_num:
                existing_mapping_numbers.add(map_num)

    for product in reaction.iterateProducts():
        for atom in product.iterateAtoms():
            map_num = reaction.atomMappingNumber(atom)
            if map_num and map_num not in existing_mapping_numbers:
                reaction.setAtomMappingNumber(atom, 0)  # YQ: atom number 0 means no mapping number in Indigo


def make_concrete_reaction(reactants: list[IndigoObject], products: list[IndigoObject], replacement: IndigoObject,
                           replacement_index: int) -> tuple[IndigoObject, IndigoObject]:
    """
    Create a concrete reaction from the given reactants and products, replacing the specified reactant with the replacement molecule.
    :param reactants: List of reactant molecules.
    :param products: List of product molecules.
    :param replacement: The molecule to replace in the reactants.
    :param replacement_index: The index of the reactant to replace.
    :return: A new IndigoObject representing the concrete reaction.
    """
    concrete_reaction = indigo.createQueryReaction()
    for i, reactant in enumerate(reactants):
        if i == replacement_index:
            concrete_reaction.addReactant(indigo.loadQueryMolecule(replacement.molfile()))
        else:
            concrete_reaction.addReactant(reactant.clone())
    for product in products:
        concrete_reaction.addProduct(product.clone())
    return concrete_reaction, concrete_reaction.getMolecule(replacement_index)


def is_ambiguous_atom(atom: IndigoObject) -> bool:
    """
    Test whether the symbol is an adjacent matching wildcard.
    """
    if atom.isPseudoatom() or atom.isRSite():
        return True
    symbol = atom.symbol()
    if symbol in {'A', 'Q', 'X', 'M', 'AH', 'QH', 'XH', 'MH', 'NOT', 'R', '*'}:
        return True
    return "[" in symbol and "]" in symbol


def get_react_site_highlights(product, ignored_atom_indexes):
    """
    Get the highlights for the reaction site in the product, ignoring the atoms that are not part of the reaction site.
    :param product: The product molecule.
    :param ignored_atom_indexes: A set of atom indexes to ignore.
    :return: An IndigoObject with highlighted atoms and bonds that are part of the reaction site.
    """
    highlight = product.clone()
    for atom in highlight.iterateAtoms():
        if atom.index() not in ignored_atom_indexes:
            atom.highlight()
            for nei in atom.iterateNeighbors():
                if nei.index() not in ignored_atom_indexes:
                    nei.highlight()
                    nei.bond().highlight()
    return highlight


def inherit_auto_map_by_match(target_reaction: IndigoObject, source_reaction: IndigoObject,
                              reaction_match: IndigoObject):
    """
    Inherit the auto-mapping from the source reaction to the target reaction based on the reaction match.
    :param target_reaction: The target reaction to inherit auto-mapping to.
    :param source_reaction: The source reaction to inherit auto-mapping from.
    :param reaction_match: The match object that maps atoms and bonds between the source and target reactions.
    """
    source_molecules = []
    for q_reactant in source_reaction.iterateReactants():
        source_molecules.append(q_reactant)
    for q_product in source_reaction.iterateProducts():
        source_molecules.append(q_product)
    for source_molecule in source_molecules:
        for source_atom in source_molecule.iterateAtoms():
            source_atom_map_number = source_reaction.atomMappingNumber(source_atom)
            if source_atom_map_number == 0:
                continue
            target_atom = reaction_match.mapAtom(source_atom)
            if target_atom:
                target_reaction.setAtomMappingNumber(target_atom, source_atom_map_number)
    target_reaction.automap("keep")


def are_symmetrical_subs(match1: SerializableMoleculeMatch, match2: SerializableMoleculeMatch) -> bool:
    """
    Check if two SerializableMoleculeMatch objects are symmetrical.
    That is, if we only get the atoms and bonds in the mapping, the two molecules are identical.
    :param match1: The first SerializableMoleculeMatch object.
    :param match2: The second SerializableMoleculeMatch object.
    :return: True if the matches are symmetrical, False otherwise.
    """
    match1_test = match1.get_matched_molecule_copy()
    match1_atom_indexes = set(match1._query_atom_to_atom.values())
    match1_bond_indexes = set(match1._query_bond_to_bond.values())
    atom_delete_list: list[int] = []
    atom_mirror_list: list[int] = []
    bond_delete_list: list[int] = []
    bond_mirror_list: list[int] = []
    for atom in match1_test.iterateAtoms():
        if atom.index() not in match1_atom_indexes:
            atom_delete_list.append(atom.index())
        else:
            atom_mirror_list.append(atom.index())
    for bond in match1_test.iterateBonds():
        if bond.index() not in match1_bond_indexes:
            bond_delete_list.append(bond.index())
        else:
            bond_mirror_list.append(bond.index())
    match1_test.removeBonds(bond_delete_list)
    match1_test.removeAtoms(atom_delete_list)
    match1_mirror_test = match1.get_matched_molecule_copy()
    match1_mirror_test.removeBonds(bond_mirror_list)
    match1_mirror_test.removeAtoms(atom_mirror_list)

    match2_test = match2.get_matched_molecule_copy()
    match2_atom_indexes = set(match2._query_atom_to_atom.values())
    match2_bond_indexes = set(match2._query_bond_to_bond.values())
    atom_delete_list = []
    bond_delete_list = []
    atom_mirror_list = []
    bond_mirror_list = []
    for atom in match2_test.iterateAtoms():
        if atom.index() not in match2_atom_indexes:
            atom_delete_list.append(atom.index())
        else:
            atom_mirror_list.append(atom.index())
    for bond in match2_test.iterateBonds():
        if bond.index() not in match2_bond_indexes:
            bond_delete_list.append(bond.index())
        else:
            bond_mirror_list.append(bond.index())
    match2_test.removeBonds(bond_delete_list)
    match2_test.removeAtoms(atom_delete_list)
    match2_mirror_test = match2.get_matched_molecule_copy()
    match2_mirror_test.removeBonds(bond_mirror_list)
    match2_mirror_test.removeAtoms(atom_mirror_list)

    return match1_test.canonicalSmiles() == match2_test.canonicalSmiles() and \
        match1_mirror_test.canonicalSmiles() == match2_mirror_test.canonicalSmiles()


def replace_r_site_with_wildcards(mol: IndigoObject) -> IndigoObject:
    """
    This will be used to replace molecule's R sites with wildcard *.
    The substructure matcher at molecular level will not touch R sites. Therefore if we are to preserve mapping with bonds we need to replace R sites with wildcards.
    :param mol: The molecule to process.
    :return: A cloned molecule with R sites replaced by wildcards.
    """
    ret = mol.clone()
    for atom in ret.iterateAtoms():
        if atom.isRSite():
            atom.resetAtom("*")
    return ret


def get_r_substructure(query_mol: IndigoObject, mol: IndigoObject,
                       initial_atom: IndigoObject, match: IndigoObject | SerializableMoleculeMatch,
                       r_site: str) -> IndigoObject:
    """
    Return a connected R substructure sourced from the symbol, that is not within the original query match.
    :param query_mol: The query molecule that contains the R site.
    :param mol: The molecule that contains the R site.
    :param initial_atom: The initial atom that is the R site.
    :param match: The match object that maps atoms and bonds between the query and the molecule.
    Note the within-R site molecules will not be part of the match.
    But the starting position of R site is replaced with psuedoatom "*" and thus matches.
    :param r_site: The R site symbol to match against.
    """
    keeping_atom_index_set = set()
    visiting: set[int] = set()
    visiting.add(initial_atom.index())
    visited: set[int] = set()

    exclusion_indexes = set()
    for q_atom in query_mol.iterateAtoms():
        mapped_atom = match.mapAtom(q_atom)
        if mapped_atom:
            to_exclude: bool
            if q_atom.isRSite():
                to_exclude = q_atom.symbol() != r_site
            else:
                to_exclude = True
            if to_exclude:
                exclusion_indexes.add(mapped_atom.index())
    while visiting:
        visiting_atom: IndigoObject = mol.getAtom(visiting.pop())
        keeping_atom_index_set.add(visiting_atom.index())
        visited.add(visiting_atom.index())
        for nei in visiting_atom.iterateNeighbors():
            nei_index = nei.index()
            if nei_index in visited or nei_index in visiting:
                continue
            if nei_index in exclusion_indexes and nei_index != initial_atom.index():
                continue
            visiting.add(nei_index)
    removing_index_set: list[int] = list()
    for atom in mol.iterateAtoms():
        if atom.index() not in keeping_atom_index_set:
            removing_index_set.append(atom.index())
    r_substructure = mol.clone()
    r_substructure.removeAtoms(removing_index_set)
    return r_substructure


def get_rr_substructure_by_symbol(query_reactant, replacement_reaction) -> dict[str, IndigoObject]:
    rr_substructure_by_symbol: dict[str, IndigoObject] = {}
    for q_atom in query_reactant.iterateAtoms():
        if not q_atom.isRSite():
            continue
        r_site_symbol = q_atom.symbol()
        mapped_atom = replacement_reaction.replacement_query_reaction_match.mapAtom(q_atom)
        if mapped_atom is None:
            raise ValueError(
                "The replacement reactant " + replacement_reaction.replacement_reactant.smiles() + " do not have R Site: " + r_site_symbol + ". This should not happen.")
        r_substructure = get_r_substructure(query_reactant, replacement_reaction.replacement_reactant, mapped_atom,
                                            replacement_reaction.replacement_query_reaction_match, r_site_symbol)
        rr_substructure_by_symbol[r_site_symbol] = r_substructure
    return rr_substructure_by_symbol


def __test_reactant_match(replacement_reaction: ReplacementReaction,
                          testing_reactant: IndigoObject,
                          query_reactant: IndigoObject) -> SerializableMoleculeMatch | None:
    """ YQ: Finally piecing together both sides...
    Test whether the reactant in the replacement reaction matches the reactant in the testing reaction.
    We will be matching against the highlighted portion on each section to ensure the highlighted atom and bonds match.
    :param replacement_reaction: The replacement reaction containing the reactant to test.
    :param testing_reactant: The reactant in the testing reaction to match against.
    :param query_reactant: The reactant in the query reaction to match against.
    """
    orig_query_reactant = query_reactant
    query_reactant = replace_r_site_with_wildcards(query_reactant)
    if not indigo.exactMatch(replacement_reaction.replacement_reactant, testing_reactant):
        return None
    outer_matcher: IndigoObject = indigo.substructureMatcher(testing_reactant)
    used_query_atom_indexes = replacement_reaction.replacement_query_reaction_match.query_atom_indexes
    used_rr_atom_indexes = replacement_reaction.replacement_query_reaction_match.matching_atom_indexes
    rr_substructure_by_symbol: dict[str, IndigoObject] = get_rr_substructure_by_symbol(orig_query_reactant,
                                                                                       replacement_reaction)

    for outer_match in outer_matcher.iterateMatches(query_reactant):
        ret: SerializableMoleculeMatch = SerializableMoleculeMatch.create(
            orig_query_reactant, testing_reactant, outer_match, used_query_atom_indexes)
        used_testing_reactant_atoms = []
        for q_atom in query_reactant.iterateAtoms():
            if q_atom.index() not in used_query_atom_indexes:
                continue
            mapped_atom = outer_match.mapAtom(q_atom)
            if mapped_atom is None:
                continue
            used_testing_reactant_atoms.append(mapped_atom.index())
        used_replacement_mol = replacement_reaction.replacement_reactant.clone()
        used_replacement_mol_delete_indexes = []
        for atom in used_replacement_mol.iterateAtoms():
            if atom.index() not in used_rr_atom_indexes:
                used_replacement_mol_delete_indexes.append(atom.index())
        used_replacement_mol.removeAtoms(used_replacement_mol_delete_indexes)
        used_testing_mol = testing_reactant.clone()
        used_testing_mol_delete_indexes = []
        for atom in used_testing_mol.iterateAtoms():
            if atom.index() not in used_testing_reactant_atoms:
                used_testing_mol_delete_indexes.append(atom.index())
        used_testing_mol.removeAtoms(used_testing_mol_delete_indexes)
        try:
            exact_match = indigo.exactMatch(used_replacement_mol, used_testing_mol)
            if not exact_match:
                continue
        except IndigoException:
            continue
        # Now check each R site substructure and it should be an exact match.
        outer_match_r_substructure_by_symbol: dict[str, IndigoObject] = {}
        missing_r_site = False
        for q_atom in query_reactant.iterateAtoms():
            orig_q_atom = orig_query_reactant.getAtom(q_atom.index())
            if not orig_q_atom.isRSite():
                continue
            r_site_symbol = orig_q_atom.symbol()
            mapped_atom = outer_match.mapAtom(q_atom)
            if mapped_atom is None:
                missing_r_site = True
                continue
            r_substructure = get_r_substructure(orig_query_reactant, testing_reactant, mapped_atom, outer_match,
                                                r_site_symbol)
            outer_match_r_substructure_by_symbol[r_site_symbol] = r_substructure
        if missing_r_site:
            # If we are missing an R site, we cannot match.
            continue
        r_site_mismatch = False
        for r_site_symbol in rr_substructure_by_symbol.keys():
            rr_substructure = rr_substructure_by_symbol[r_site_symbol]
            outer_match_r_substructure = outer_match_r_substructure_by_symbol[r_site_symbol]
            if not indigo.exactMatch(rr_substructure, outer_match_r_substructure):
                r_site_mismatch = True
                break
        if r_site_mismatch:
            # If we have a mismatch in R site substructure, we cannot match.
            continue

        # We are done matching. Return the match mapping.
        return ret
    return None


def __test_product_match(testing_reaction: IndigoObject, q_reaction: IndigoObject,
                         cur_rr_list: list[ReplacementReaction],
                         testing_reactants_match_list: list[SerializableMoleculeMatch]) -> list[
                                                                                               SerializableMoleculeMatch] | None:
    """ YQ: My fifth try OOF
    For each product, we are testing against two criteria:
    1. That every R site from a product would exact match to the R site defined within reactant.
    2. That atomic mapping numbers for query matches are within the matches of intersection of cur_rr_list and testing_reactants_match_list.
    And the matching result for each atom via their reaction atom mapping numbers should follow atomic conservation law:
    2.1 For each atom number in the reactant part, there should be no more than one atom in the product part with the same mapping number.
    2.2 For each atom number in the reactant part, the mapped atom in the product part has the nucleus.
    :param testing_reaction:
    :param q_reaction:
    :param cur_rr_list:
    :param testing_reactants_match_list:
    :return:
    """
    # ********* PREPARE DATA *********
    ret: list[SerializableMoleculeMatch] = []
    testing_reactants = []
    for testing_reactant in testing_reaction.iterateReactants():
        testing_reactants.append(testing_reactant)
    testing_products = []
    for testing_product in testing_reaction.iterateProducts():
        testing_products.append(testing_product)
    query_reactants = []
    for q_reactant in q_reaction.iterateReactants():
        query_reactants.append(q_reactant)
    query_products = []
    for q_product in q_reaction.iterateProducts():
        query_products.append(q_product)
    replacement_reactants = []
    replacement_reactant_match_list = []
    q_atom_mapping_number_to_rr_reactant_atom: dict[int, IndigoObject] = {}
    for reactant_index, replacement_reaction in enumerate(cur_rr_list):
        replacement_reactants.append(replacement_reaction.replacement_reactant)
        replacement_reactant_match_list.append(replacement_reaction.replacement_query_reaction_match)
        query_reactant = query_reactants[reactant_index]
        for q_atom in query_reactant.iterateAtoms():
            mapped_atom = replacement_reaction.replacement_query_reaction_match.mapAtom(q_atom)
            q_atom_mapping_number = q_reaction.atomMappingNumber(q_atom)
            if q_atom_mapping_number == 0:
                continue
            if mapped_atom is None:
                continue
            q_atom_mapping_number_to_rr_reactant_atom[q_atom_mapping_number] = mapped_atom
    rr_substructure_by_symbol: dict[str, IndigoObject] = {}
    for reactant_index, replacement_reaction in enumerate(cur_rr_list):
        query_reactant = query_reactants[reactant_index]
        cur_dict = get_rr_substructure_by_symbol(query_reactant, replacement_reaction)
        rr_substructure_by_symbol.update(cur_dict)

    # ********* TESTING PRODUCTS *********
    accepted_used_atom_mapping_numbers: set[int] = set()
    for product_index, testing_product in enumerate(testing_products):
        q_product = query_products[product_index]
        orig_q_product = q_product
        q_product = replace_r_site_with_wildcards(q_product)
        outer_matcher: IndigoObject = indigo.substructureMatcher(testing_product)
        found_match: SerializableMoleculeMatch | None = None
        for outer_match in outer_matcher.iterateMatches(q_product):
            ss_match: SerializableMoleculeMatch = SerializableMoleculeMatch.create(orig_q_product, testing_product,
                                                                                   outer_match)
            valid_q_product_aam = True
            valid_r_group = True
            used_atom_mapping_numbers: set[int] = set()
            for q_atom in q_product.iterateAtoms():
                mapped_product_atom = outer_match.mapAtom(q_atom)
                orig_q_atom = orig_q_product.getAtom(q_atom.index())
                q_atom_mapping_number = q_reaction.atomMappingNumber(orig_q_atom)
                if q_atom_mapping_number > 0 and not orig_q_atom.isRSite():
                    if q_atom_mapping_number in used_atom_mapping_numbers or q_atom_mapping_number in accepted_used_atom_mapping_numbers:
                        raise ValueError(
                            "Multiple atoms in the product with the same query atom mapping number: " + str(
                                q_atom_mapping_number))
                    rr_atom = q_atom_mapping_number_to_rr_reactant_atom.get(q_atom_mapping_number)
                    if rr_atom is None:
                        valid_q_product_aam = False
                        break
                    if not rr_atom.symbol() == mapped_product_atom.symbol():
                        valid_q_product_aam = False
                        break
                    used_atom_mapping_numbers.add(q_atom_mapping_number)
                elif orig_q_atom.isRSite():
                    r_site_symbol = orig_q_atom.symbol()
                    r_substructure = get_r_substructure(orig_q_product, testing_product, mapped_product_atom,
                                                        outer_match,
                                                        r_site_symbol)
                    rr_substructure = rr_substructure_by_symbol.get(r_site_symbol)
                    if rr_substructure is None:
                        # This only happens if we didn't replace wildcard properly in original highlight or a misalignment between reactant and actual reaction template in Sapio.
                        raise ValueError("Missing RR substructure for R site: " + r_site_symbol + ".")
                    if not indigo.exactMatch(rr_substructure, r_substructure):
                        valid_r_group = False
                        break
            if valid_q_product_aam and valid_r_group:
                found_match = ss_match
                accepted_used_atom_mapping_numbers.update(used_atom_mapping_numbers)
                break
        if not found_match:
            return None
        ret.append(found_match)
    return ret


def __get_final_highlighted_reaction(cur_rr_list: list[ReplacementReaction],
                                     product_matches: list[SerializableMoleculeMatch]) -> tuple[IndigoObject, list[
    ReplacementReaction]] | None:
    """
    Translates the final match into a highlighted reaction.
    :param cur_rr_list: The selected reactants that together forms an acceptable reaction.
    :param product_matches: The generated products coming from the selected reactants.
    :return: An IndigoObject representing the final reaction with highlights.
    """
    ret: IndigoObject = indigo.createReaction()
    for replacement_reaction in cur_rr_list:
        reactant_mol = replacement_reaction.replacement_reactant.clone()
        highlighting_atom_indexes = replacement_reaction.replacement_query_reaction_match.matching_atom_indexes
        for atom in reactant_mol.iterateAtoms():
            if atom.index() in highlighting_atom_indexes:
                atom.highlight()
            for nei in atom.iterateNeighbors():
                if nei.index() in highlighting_atom_indexes:
                    nei.bond().highlight()
        ret.addReactant(reactant_mol)
    for product_match in product_matches:
        product_mol = product_match.get_matched_molecule_copy()
        highlighting_atom_indexes = product_match.matching_atom_indexes
        for atom in product_mol.iterateAtoms():
            if atom.index() in highlighting_atom_indexes:
                atom.highlight()
            for nei in atom.iterateNeighbors():
                if nei.index() in highlighting_atom_indexes:
                    nei.bond().highlight()
        ret.addProduct(product_mol)
    _, ret = get_aromatic_dearomatic_forms(ret)
    return ret, cur_rr_list


def ps_match(testing_reaction: IndigoObject, q_reaction: IndigoObject,
             kept_replacement_reaction_list_list: list[list[ReplacementReaction]]) -> tuple[IndigoObject, list[
    ReplacementReaction]] | None:
    testing_reactants = []
    for testing_reactant in testing_reaction.iterateReactants():
        testing_reactants.append(testing_reactant)
    query_reactants = []
    for q_reactant in q_reaction.iterateReactants():
        query_reactants.append(q_reactant)

    reactant_ranges = []
    for replacement_reaction_list in kept_replacement_reaction_list_list:
        reactant_ranges.append(range(len(replacement_reaction_list)))
    reactant_cartesian_products = itertools.product(*reactant_ranges)
    for reactant_combination in reactant_cartesian_products:
        cur_rr_list: list[ReplacementReaction] = []
        for reactant_index, replacement_reaction_index in enumerate(reactant_combination):
            replacement_reaction: ReplacementReaction = kept_replacement_reaction_list_list[reactant_index][
                replacement_reaction_index]
            cur_rr_list.append(replacement_reaction)
        is_valid_reactants = True
        testing_reactants_match_list = []
        for reactant_index, replacement_reaction in enumerate(cur_rr_list):
            match = __test_reactant_match(
                replacement_reaction, testing_reactants[reactant_index], query_reactants[reactant_index])
            if not match:
                is_valid_reactants = False
                break
            testing_reactants_match_list.append(match)
        if not is_valid_reactants:
            continue
        product_matches = __test_product_match(testing_reaction, q_reaction, cur_rr_list, testing_reactants_match_list)
        if product_matches:
            return __get_final_highlighted_reaction(cur_rr_list, product_matches)
    return None
