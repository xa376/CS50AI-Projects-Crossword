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
        #print(self.domains)
        #print(self.domains.keys)
        # TODO Domain is Variable OBJ type

        # key = variable object, value = words

        # Removes words that are not the same length as the Variable OBJ requires
        wordsToRemove = set()
        for variable, words in self.domains.items():
            #print(f"first: {len(words)}")
            for word in words:
                if len(word) != variable.length:
                    wordsToRemove.add(word)
            for word in wordsToRemove:
                self.domains[variable].remove(word)
            wordsToRemove.clear()


            #print(f"second: {len(words)}")
            #print(value)

        #for domain in self.domains:
         #   print(domain)
          #  print(self.domains[domain])
           # print(domain.length)
            #for word in x:
            #    if len(word) > len(v)
            #self.domains[v].remove()

        # TODO order_domain_values and select_unassigned_variable LAST
        # LAST LAST LAST LAST
        # TODO you can print the resulting puzzle by adding command
        # TODO USE NEIGHBORS FUNCTION TO ACCES THE NEIGHBORS!

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        #print(f"This is x: {x}")
        #print(self.domains[x])
        #print(f"This is y: {y}")
        #print(self.domains[y])
        #print(self.crossword.overlaps[x, y])

        wordsToRemove = set()

        # If variables dont overlap returns false
        #print(f"x = {x}")
        #print(f"y = {y}")
        if self.crossword.overlaps[x, y] == None:
            return False
        else:
            (indexX, indexY) = self.crossword.overlaps[x, y]
            for word in self.domains[x]:
                remove = True
                for word2 in self.domains[y]:
                    if word[indexX] == word2[indexY] and word != word2:
                        remove = False
                if remove == True:
                    wordsToRemove.add(word)

        #print(self.domains[x])

        if len(wordsToRemove) == 0:
            return False
        else:
            for word in wordsToRemove:
                self.domains[x].remove(word) # Remove x word
        #print(self.domains[x])

        return True





        '''
        if self.crossword.overlaps[x, y] == None:
            return False
        else:
            for word in self.domains[x]:
                overlap = self.crossword.overlaps[x, y]
                xLetter = word[overlap[0]]
                compatible = False
                for yWord in self.domains[y]:
                    yLetter = yWord[overlap[1]]
                    if xLetter == yLetter: # There is a matching option
                        compatible = True
                if compatible == False: # No match found
                    wordsToRemove.add(word)
            if wordsToRemove == None:
                return False
            else:
                for word in wordsToRemove:
                    self.domains[x].remove(word) # Remove x word
                return True
                    
                
                # If xletter does not equal y letter remove xword
            '''


        '''
        overlap = self.crossword.overlaps[x, y]
        if x.direction == "across":
            overlapStart = overlap + (x.i, x.j)
            overlapLocation = overlapStart[1]
        else:
            overlapStart = overlap + (y.i, y.j)
            overlapLocation = overlapStart[0]
        overlapLetter = word[overlapLocation]
        print(overlap[1])
        '''
        # Get overlapping character
        # for each word in x
        # get the letter than overlaps
        # if that letter is in that spot for a word in y
        # remove that word from x

        # Check for character in that location
        # Ensure y has a character for that location
        # Else remove word from x

        # WORD DOESNT START FROM LOCATION PASSED BY crossword.overlaps

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # ARC is if variable x touches variable y

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
            

        #print(f"queue = {queue}")

        # While queue is not empty, revises variables in queue
        while len(queue) > 0:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))
        return True

                



        '''
        # variable = sequence of squares = Variable OBJ
        # arc contains VARIABLE x and VARIABLE y OBJECTS
        if arcs == None:
            for variable in range(len(self.domains.keys())):
                #print(len(self.domains.keys()))
                #print(variable)
                if variable < len(self.domains.keys()) - 1: # -1 because 0 based
                    if self.revise(list(self.domains.keys())[variable], list(self.domains.keys())[variable + 1]):
                        continue
                else:
                    if self.revise(list(self.domains.keys())[variable], list(self.domains.keys())[0]):
                        continue
        else:
            for arc in arcs:
                self.revise(arc)
        
        for variable in self.domains:
            if len(self.domains[variable]) == 0:
                return False
            else:
                return True
        '''

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #print(f"assignment: {assignment}")
        if len(assignment) == len(self.domains):
            return True
        else:
            return False
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if assignment == None:
            return False
        for variable, word in assignment.items():
            #print(f"word 1 = {word}")
            # Check Distinct
            for var2, word2 in assignment.items():
                
                if variable != var2:
                    if word == word2:
                        return False

                    # Check conflicting character
                    if self.crossword.overlaps[variable, var2] != None:
                        (x, y) = self.crossword.overlaps[variable, var2]
                        if word[x] != word2[y]:
                            return False

            # Check length
            if variable.length != len(word):
                return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # MAYBE!?!?!?!
        # Get the domains of var
        # Get the neighbors of var
        # Neighbors are added to a dict with their word length
        # If the var domain is in the neighbor, remove that word from the new dict
        # Order list
        # IDK

        variablesList = []

        # Iterate through every word
        for neighbor in self.crossword.neighbors(var):
            if neighbor not in assignment.keys():
                values = 0
                (x, y) = self.crossword.overlaps[var, neighbor]     
                for wordX in self.domains[var]:
                    for wordY in self.domains[neighbor]:
                        if wordX[x] != wordY[y] or wordX == wordY:
                            values += 1
                variablesList.append((neighbor, values))
        
        return sorted(variablesList, key=lambda value: value[1])







        variablesList = self.domains[var]
        return variablesList



        #print(f"var = {var}")

        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        variablesList = []

        for variable in self.domains.keys():
            if variable not in assignment.keys():
                variablesList.append((variable, len(self.domains[variable])))


        return sorted(variablesList, key=lambda var: var[1])[0][0]


        return variable
        return None
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #self.enforce_node_consistency()
        #self.ac3()
        #return self.backtrack(dict())
        # FILL ASSIGNMENT
        #print(f"assignment: {assignment}")
        #print(self.domains)

        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        self.order_domain_values(variable, assignment)
        for word in self.domains[variable]:
            varDict = {variable : word}
            if self.consistent({**assignment, **varDict}):
                assignment[variable] = word
                result = self.backtrack(assignment)
                if self.consistent(result):
                    #print(f"result = {result}")
                    return result
            #print(f"assignment = {assignment}")
            if variable in assignment.keys():
                del assignment[variable]
        #print(f"result = {result}")
        return None
            
        
        '''
        while True:

            for variable, words in self.domains.items():

                # Turns words into iterable list
                wordsList = list(words)

                # If no words to choose returns none
                if len(wordsList) == 0:
                    return None
                
                
                for i in range(len(wordsList)):
                    if wordsList[i] not in assignment.values():
                        assignment[variable] = wordsList[i]
                        self.ac3(assignment)
               
            print(assignment)

            if self.consistent(assignment):
                break
            else:
                # Remove these words
                for variable2, word in assignment.items():
                    self.domains[variable2].remove(word)
                
                # Clears assignment
                assignment.clear()
        '''

        '''
        print(self.domains.items())

        for variable, words in self.domains.items():
            wordsList = list(words)
            if len(wordsList) != 0:
                while True:
                    for variable, word in assignment.items():
                        self.domains[variable].discard(word)
                    for i in range(len(wordsList)):
                        if wordsList[i] not in assignment.values():
                            assignment[variable] = wordsList[i]
                    #if not self.consistent(assignment):
                    #    print("hi")
                    if self.consistent(assignment):
                        break

                print(assignment)
                    
                        
            else:
                return None
        '''
        print(assignment.values())
        # dict_items([(Variable(0, 1, 'down', 5), {'SEVEN'}), (Variable(0, 1, 'across', 3), {'SIX'}), 
        # (Variable(1, 4, 'down', 4), {'FIVE', 'NINE'}), (Variable(4, 1, 'across', 4), {'NINE'})])
        #if not self.consistent(assignment) or not self.assignment_complete(assignment):
        #    return None
        return assignment


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
