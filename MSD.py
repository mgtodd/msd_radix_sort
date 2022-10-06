"""
@author: Matthew Todd
"""

import numpy as np
import copy


class msd:
    """MSD Radix sort for strings"""

    def __init__(self, items=[]):
        self.items = []
        if len(items) > 0:
            l = [len(x) for x in items]
            self.max_index = max(l) - 1
        else:
            self.max_index = 0

    def set_items(self, items):
        """
        Set the data for sorting

        Parameters
        ----------
        items : list of strings
            a list of unsorted strings

        """
        self.items = items
        l = [len(x) for x in items]
        self.max_index = max(l) - 1

    def msd(self):
        """
        MSD Radix Sort public function.
        Note: Please ensure all strings are equal length, otherwise sorting
        is not guaranteed.


        Returns
        -------
        list of strings
            a list of strings sorted up to and including the given index

        """
        return self._msd(self.items, 0)

    def _msd(self, input_list, index):
        """
        Most Significant Digit Radix Sort.

        Parameters
        ----------
        input_list : list of strings
            a list of strings unsorted after the given index
        index : int
            index at which the sort is applied

        Returns
        -------
        list of strings
            a list of strings sorted up to and including the given index

        """
        # Recursion exit conditions
        if len(input_list) < 2 or index > self.max_index:
            return input_list
        # Do a counting sort at the current index
        sorted_list = self._stableSort(input_list, index)

        # Collect all sublists that are the same at the current index and
        # sort them in place
        idx_first = 0
        idx_last = 1
        while idx_last < len(input_list):
            # Iterate to collect elements
            if sorted_list[idx_last][index] == sorted_list[idx_first][index]:
                idx_last += 1
            else:
                # bucket
                sorted_list[idx_first:idx_last] = self._msd(
                    sorted_list[idx_first:idx_last], index + 1
                )
                # Move on to the next bucket
                idx_first = idx_last
                idx_last += 1
        # do the last sort before returning
        sorted_list[idx_first:idx_last] = self._msd(
            sorted_list[idx_first:idx_last], index + 1
        )
        return sorted_list

    def _stableSort(self, input_list, index):
        """
        Counting sort implementation for string inputs. Counting sort
        is stable (preserves original order for ties) and does not rely
        on comparisons.

        Parameters
        ----------
        input_list : list of strings
            a list of strings unsorted after the given index
        index : int
            index at which the sort is applied

        Returns
        -------
        out_list : list of strings
            a list of strings sorted up to and including the given index

        """
        # Possible number of unique chars, assuming the acceptable range of
        # inputs is 7-bit (All alphabetic characters are in this range. If
        # space was a concern we could restrict the input list to contain
        # only 26 lowercase characters)
        possible_elements = 128
        # number of occurences of the input
        count_list = [0] * possible_elements
        # number of elements to be sorted n
        n = len(input_list)
        # sorted list
        out_list = [0] * n
        # Count the number of times each element occurs
        for i in range(0, n):
            count_list[ord(input_list[i][index])] += 1
        # Convert count_list to a cumulative sum
        for i in range(1, possible_elements):
            count_list[i] += count_list[i - 1]
        # Put the items from input_list into their place in out_list
        # Starting from the back of the input list ensures this is a stable
        # sort
        for i in range(n - 1, -1, -1):
            element = ord(input_list[i][index])
            count_list[element] -= 1
            out_list[count_list[element]] = input_list[i]
        return out_list


class msd_unit_tester:
    def __init__(self):
        self.sorted = []
        self.ref_sorted = []
        self.unsorted = []
        # Create MSD radix sorter class
        self.sorter = msd()
        # Load the text file with reference english words
        with open("words_alpha.txt") as word_file:
            self.all_words = set(word_file.read().split())
        # Set a random word length
        word_len = np.random.randint(3,high=10)
        self.set_word_length(word_len)

    def set_word_length(self, word_len):
        # Grab all the words of a certain length
        self.unsorted = [w for w in self.all_words if (len(w)) == word_len]
        # Initialise the reference sorted list using python list.sort()
        self.ref_sorted = copy.deepcopy(self.unsorted)
        self.ref_sorted.sort()

    def correctly_sorted(self):
        # python syntax can already element-wise compare two lists, apparently
        return self.ref_sorted == self.sorted

    def run_all_unit_tests(self, random_seed=42):
        print("python random seed is %d" % (random_seed))
        np.random.seed(random_seed)
        print("Beginning unit tests...")
        self._test_random_length()
        self._test_reverse_list()
        self._test_list_with_duplicates()
        print("Passed all unit tests!")

    def _test_random_length(self):
        # Test all the words with a random length
        word_len = np.random.randint(3, high=10)
        self.set_word_length(word_len)
        self.sorter.set_items(self.unsorted)
        self.sorted = self.sorter.msd()
        if not self.correctly_sorted():
            raise ValueError(
                "Test test_random_length failed for length %d" % (word_len)
            )
        print("Passed test_random_length. Sorted %d words" % (len(self.unsorted)))
            
    def _test_reverse_list(self):
        # Test all the words with a random length
        word_len = np.random.randint(3, high=10)
        self.set_word_length(word_len)
        reverse_list = copy.deepcopy(self.ref_sorted)
        reverse_list.reverse()
        self.sorter.set_items(reverse_list)
        self.sorted = self.sorter.msd()
        if not self.correctly_sorted():
            raise ValueError(
                "Test test_reverse_list failed for length %d" % (word_len)
            )
        print("Passed test_reverse_list. Sorted %d words" % (len(self.unsorted)))
        
    def _test_list_with_duplicates(self):
        # For this test only consider words with length 9
        unsorted = [w for w in self.all_words if (len(w)) == 9]
        # Take a subset of 10 of the values
        unsorted = np.random.choice(unsorted,size=10).tolist()
        print("This next test uses a printable number of values6")
        # Now duplicate 5 of them 
        unsorted = unsorted + np.random.choice(unsorted,size=5).tolist()
        print("Unsorted list, with duplicates:")
        print(unsorted)
        self.unsorted = unsorted
        # prepare the reference list
        self.ref_sorted = copy.deepcopy(self.unsorted)
        self.ref_sorted.sort()
        
        # Run the sorting algorithm
        self.sorter.set_items(unsorted)
        self.sorted = self.sorter.msd()
        if not self.correctly_sorted():
            raise ValueError(
                "Test test_list_with_duplicates failed! "
            )
        print("Sorted list, with duplicates:")
        print(self.sorted)
        print("Passed test_list_with_duplicates. Sorted %d words" % (len(self.unsorted)))
        
# %% 
if __name__ == "__main__":
    
    dut = msd_unit_tester()
    dut.run_all_unit_tests(42 )
    
# def stableSortInts(self, input_list, index):
#     # number of occurences of the input
#     count_list = [0] * self.base
#     # number of elements n
#     n = len(input_list)
#     # sorted list s
#     out_list = [0] * n

#     # Count the number of times each element occurs
#     for i in range(0,n):
#         count_list[input_list[i]] += 1

#     # Convert count_list to a cumulative sum
#     for i in range(1,self.base):
#         count_list[i] += count_list[i-1]

#     # Put the items from input_list into their place in out_list
#     # Starting from the back of the input list ensures this is a stable
#     # sort
#     for i in range(n-1,-1,-1):
#         count_list[input_list[i]] -= 1
#         out_list[count_list[input_list[i]]] = input_list[i]

#     return out_list

# For base b = self.base we need log_b(max_val). Use the change of
# base rule for logs
# max_val = max(items)
# self.num_digits = np.ceil(np.log(max_val) / np.log(self.base))
