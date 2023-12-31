"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the definition of an Abstract Data Type (Autocompleter) and two
implementations of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """

    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: list) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: list,
                     limit: int | None = None) -> list[tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        sorted by non-increasing weight. You can decide how to break ties.

        If limit is None, return *every* match for the given prefix.

        Preconditions:
        - limit is None or limit > 0
        """
        raise NotImplementedError

    def remove(self, prefix: list) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
@check_contracts
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    Instance Attributes:
    - root:
        The root of this prefix tree.
        - If this tree is empty, <root> equals [].
        - If this tree is a leaf, <root> represents a value stored in the
        Autocompleter
          (e.g., 'cat').
        - If this tree is not a leaf and non-empty, <root> is a list
         representing a prefix
          (e.g., ['c', 'a']).
    - subtrees:
        A list of subtrees of this prefix tree.
    - weight:
        The weight of this prefix tree.
        - If this tree is empty, this equals 0.0.
        - If this tree is a leaf, this stores the weight of the value stored
         in the leaf.
        - If this tree is not a leaf and non-empty, this stores the *total
         weight* of
          the leaf weights in this tree.

    Representation invariants:
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0.0, then self.root == [] and self.subtrees == [].
        This represents an empty prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, then this tree is a leaf.
        (self.root is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If self.subtrees != [], then self.root is a list (representing a prefix),
        and self.weight is equal to the sum of the weights of all leaves in self.

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of weight.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a weight
      attribute.
    """
    root: Any
    weight: float
    subtrees: list[SimplePrefixTree]

    ###########################################################################
    # Part 1(a)
    ###########################################################################
    def __init__(self) -> None:
        """Initialize an empty simple prefix tree.
        """
        self.root = []
        self.weight = 0.0
        self.subtrees = []

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        if self.weight == 0:
            return True
        else:
            return False

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.subtrees == [] and self.weight > 0

    def __len__(self) -> int:
        """Return the number of LEAF values stored in this prefix tree.

        Note that this is a different definition than how we calculate __len__
        of regular trees from lecture!
        """
        if self.is_empty():
            return 0
        elif self.is_leaf():
            return 1
        else:
            return sum(subtree.__len__() for subtree in self.subtrees)

    ###########################################################################
    # Extra helper methods
    ###########################################################################
    def __str__(self) -> str:
        """Return a string representation of this prefix tree.

        You may find this method helpful for debugging. You should not change
        this method
        (nor the helper _str_indented).
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this prefix tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.root} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    ###########################################################################
    # Add code for Parts 1(c), 2, and 3 here
    ###########################################################################
    def insert(self, value: Any, weight: float, prefix: list) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence

        >>> t = SimplePrefixTree()
        >>> t.insert('cat', 2.0, ['c', 'a', 't'])
        >>> t.insert('car', 3.0, ['c', 'a', 'r'])
        >>> t.insert('dog', 4.0, ['d', 'o', 'g'])
        >>> print(t)
        3
        """
        if not prefix:
            self.weight = weight
            leaf = SimplePrefixTree()
            leaf.root = [value]
            leaf.weight = weight
            self.subtrees.append(leaf)
        else:
            self.weight += weight
            next_char = prefix.pop(0)
            node = SimplePrefixTree()
            node.root = self.root + [next_char]

            # Check if a subtree with the same root exists
            matching_subtree = next((subtree for subtree in self.subtrees
                                     if subtree.root == node.root), None)

            if matching_subtree:
                if not prefix:
                    matching_subtree.weight += weight
                    matching_subtree.subtrees[0].weight += weight
                    return
                matching_subtree.insert(value, weight, prefix)
            else:
                self.subtrees.append(node)
                node.insert(value, weight, prefix)
            self.subtrees.sort(key=lambda tree: tree.weight, reverse=True)

    def autocomplete(self, prefix: list,
                     limit: int | None = None) -> list[tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        sorted by non-increasing weight. You can decide how to break ties.

        If limit is None, return *every* match for the given prefix.

        Preconditions:
        - limit is None or limit > 0
        """
        if self.is_leaf():
            lst = [(self.root[0], self.weight)]
            return lst
        else:
            sorted_list = []
            for subtree in self.subtrees:
                sorted_list += subtree.autocomplete(prefix)

            # If prefix is given
            if prefix is not None:
                # ex) prefix: ['c','a']
                for item in sorted_list:

                    # if it's a melody
                    if not isinstance(item[0], str):
                        interval_sequence = []
                        for tuple_index in range(0, len(item[0].notes), 2):
                            if item[0].notes[tuple_index] != item[0].notes[-1]:
                                diff = item[0].notes[tuple_index + 1][0] - item[0].notes[tuple_index][0]
                            interval_sequence.append(diff)
                        if all(interval_sequence[i] == prefix[i]
                               for i in range(len(prefix))):
                            continue
                        else:
                            sorted_list.remove(item)

                    # if it's a string
                    else:
                        # ex) item: ('cat', 1.0), item_chars: ['c', 'a', 't']
                        item_chars = list(item[0])
                        item_word = item[0].split()
                        # Check if the characters appear in the correct order
                        if all(item_chars[i] == prefix[i] for i in
                               range(len(prefix))) or \
                                all(item_word[i] == prefix[i]
                                    for i in range(len(prefix))):
                            continue
                        else:
                            sorted_list.remove(item)

            if limit is None:
                return sorted(sorted_list, key=lambda x: x[1], reverse=True)
            else:
                return sorted_list[:limit]

    def remove(self, prefix: list) -> None:
        """Remove all values that match the given prefix.
        """
        if not prefix:
            self.weight = 0.0
            self.subtrees = []
        else:
            matching_subtree = None
            for subtree in self.subtrees:
                if subtree.root == self.root + [prefix[0]]:
                    matching_subtree = subtree
                    break
            if matching_subtree:
                matching_subtree.remove(prefix[1:])
                count = 0
                for subtree in self.subtrees:
                    count += subtree.weight
                    if not subtree.is_empty():
                        self.subtrees = [subtree]
                self.weight = count


################################################################################
# CompressedPrefixTree (Part 6)
################################################################################
@check_contracts
class CompressedPrefixTree(SimplePrefixTree):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the definitions
    described in Part 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    Representation Invariants:
    - (NEW) This tree does not contain any compressible internal values.
    """
    subtrees: list[CompressedPrefixTree]  # Note the different type annotation

    ###########################################################################
    # Add code for Part 6 here
    ###########################################################################
    def insert(self, value: Any, weight: float, prefix: list) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence
        """
        if not self.root:
            self.root = prefix
            leaf = CompressedPrefixTree()
            leaf.root = value
            leaf.weight = weight
            self.subtrees.append(leaf)
            self.weight += weight
        else:
            common = self.longest_common_prefix(self.root, prefix)
            if common == self.root:
                # should not demote
                for i in self.subtrees:
                    common2 = self.longest_common_prefix(i.root, prefix)
                    if len(common2) > len(common):
                        if i.root == common2:
                            i.weight += weight
                            self.weight += weight
                            return
                        i.insert(value, weight, prefix)
                        return
            # should demote
            self.demote(common)
            new_tree = CompressedPrefixTree()
            leaf = CompressedPrefixTree()
            new_tree.root = prefix
            leaf.root = value
            leaf.weight = weight
            new_tree.subtrees.append(leaf)
            new_tree.weight += weight
            self.subtrees.append(new_tree)
            self.weight += new_tree.weight
        self.subtrees.sort(key=lambda tree: tree.weight, reverse=True)

    def demote(self, lst: list) -> None:
        """Demote a tree"""
        tree = CompressedPrefixTree()
        tree.weight += self.weight
        tree.root = self.root
        tree.subtrees += self.subtrees
        self.root = lst
        self.subtrees = [tree]

    def longest_common_prefix(self, list1: list, list2: list) -> list:
        """Find the longest common prefix"""
        common_prefix = []
        min_len = min(len(list1), len(list2))
        for i in range(min_len):
            if list1[i] == list2[i]:
                common_prefix.append(list1[i])
            else:
                break
        return common_prefix


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a2_prefix_tree" or
    # "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # "Ctrl + /" or "⌘ + /"
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'max-nested-blocks': 4
    })
