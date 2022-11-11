import copy
import time
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Removes domain words that are not the same length as the variable OBJ requires
        wordsToRemove = set()
        for variable, words in self.domains.items():
            for word in words:
                if len(word) != variable.length:
                    wordsToRemove.add(word)
            for word in wordsToRemove:
                self.domains[variable].remove(word)
            wordsToRemove.clear()

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Creates a set of words to remove from x domains, if they have no corresponding value in y domains
        wordsToRemove = set()
        (indexX, indexY) = self.crossword.overlaps[x, y]
        for wordX in self.domains[x]:
            remove = True
            for wordY in self.domains[y]:
                # If the letter in the location x and y overlap is the same, and the word is not the same, don't remove word from x
                if wordX[indexX] == wordY[indexY] and wordX != wordY:
                    remove = False
            if remove == True:
                wordsToRemove.add(wordX)

        # If no revisions to make returns false, else makes revisions and returns true
        if len(wordsToRemove) == 0:
            return False
        else:
            # Removes conflicting words from domain of x
            for word in wordsToRemove:
                self.domains[x].remove(word) # Remove x word

            # Revision was made
            return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # ARC is 2 variables with a conflicting square

        # Fills queue
        if arcs == None:
            queue = []
            for var1 in self.domains.keys():
                for var2 in self.domains.keys():
                    if var1 != var2:
                        if self.crossword.overlaps[var1, var2]:
                            queue.append((var1, var2))
        else:
            queue = arcs
            
        # While queue is not empty, revises variables in queue, adding to queue if a change is made to variableX domain
        while len(queue) > 0:
            (variableX, variableY) = queue.pop(0)
            if self.revise(variableX, variableY):
                if len(self.domains[variableX]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(variableX):
                    if neighbor != variableY:
                        queue.append((neighbor, variableX))

        # If made it here arc consistency is enforced and no domains empty                
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.domains):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if assignment == None:
            return False

        # Checks each word in assignment for consistency
        for var1, word1 in assignment.items():
            for var2, word2 in assignment.items():
                if var1 != var2:

                    # Check distinct
                    if word1 == word2:
                        return False

                    # Check conflicting overlaping character
                    if self.crossword.overlaps[var1, var2] != None:
                        (indexX, indexY) = self.crossword.overlaps[var1, var2]
                        if word1[indexX] != word2[indexY]:
                            return False

            # Check length
            if var1.length != len(word1):
                return False

        # If here then assignment is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Set that will contain domains of var in (word, neighboring values ruled out) format
        domainsSet = set()

        # Iterates through every neighbor of var, updating domains set with the domain and neighboring values ruled out
        for neighbor in self.crossword.neighbors(var):
            if neighbor not in assignment.keys():
                values = 0
                (indexX, indexY) = self.crossword.overlaps[var, neighbor]     
                for wordX in self.domains[var]:
                    for wordY in self.domains[neighbor]:
                        # If conflicting character in overlap or same word, adds 1 to ruled out values
                        if wordX[indexX] != wordY[indexY] or wordX == wordY:
                            values += 1
                domainsSet.add((neighbor, values))
        
        # Converts to list for sorting, then returns domains sorted ascending by ruled out neighboring values
        domainsList = list(domainsSet)
        return sorted(domainsList, key=lambda value: value[1])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Creates a list of unassigned variables and the size of their domains
        variablesList = []
        for variable in self.domains.keys():
            if variable not in assignment.keys():
                variablesList.append((variable, len(self.domains[variable])))

        # Sorts unassigned variables by their domain size, ascending
        return sorted(variablesList, key=lambda var: var[1])[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Utilizes backtrack search algorithm to assign a domain to each variable
        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        self.order_domain_values(variable, assignment)
        for word in self.domains[variable]:
            varDict = {variable : word}
            # Passes an unassigned dict that has varDict added to assignment for consistency assesment
            if self.consistent({**assignment, **varDict}):
                assignment[variable] = word
                result = self.backtrack(assignment)
                if self.consistent(result):
                    return result
            if variable in assignment.keys():
                del assignment[variable]
        return None

def main():

    st = time.time()

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)

    et = time.time()
    totalTime = et - st
    print(totalTime)

if __name__ == "__main__":
    main()
