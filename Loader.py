"""
File name: Loader.py
Info: CS75 Final Project
Authors: Stephanie Her, Lauren Mitchell, 
		Taylor Neely, and Erin Connolly
Date created: 30/10/2015
Date last modified: 30/10/2015
Python version: 2.7
"""

###############
### IMPORTS ###
###############

############
### CODE ###
############
class Loader:
    """Contains all information pertaining to a given gene."""

    def __init__(self, reads):
        """ Do not call directly, use the load 
            method instead.
            Example:
                reads = Loader.load("file.fq")
        """
        self.reads = reads

    @staticmethod
    def load(filename):
        """Loads given file into list of Profiles
        Args:
          file (string): the name of the file to be loaded
        Returns:
            Loader, which behaves as a list of reads from the input file
        Example:
        	reads = Loader.load("file.fq")
        """

        # Check extensions (.fq, .fastq accepted)
        if not filename.endswith(".fq") or filename.endswith(".fastq"):
            raise ValueError("The file type was not recognized, please use of the the following formats: \
            				.fq, .fastq")

        # Check if file exists
        if not os.path.isfile(filename):
            raise Exception("The file %r does not exist."%(filename))
        # Check if file can be read
        if not os.access(filename, os.F_OK):
            raise Exception("The file %r cannot be read."%(filename))

        # Create profile dictionary
        reads = []
        # Parse file
        for line in open(filename, 'r'):
            print line
        
        return Loader(reads)


    def __getitem__(self, n):
        """The read at given postion
        Returns:
          Sequence (string)
        """
        return self.reads[n]

    def __len__(self):
        """The length of loaded reads
        Returns:
          int
        """
        return len(self.reads)

    def __str__(self):
        """The list of reads"""
        return self.reads