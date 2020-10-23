import numpy as np
from sympy import Matrix


class ChemEq:
    """
    Proviedes functionaily for parsing and balancing unbalanced chemical equations.
    """

    def __init__(self, equation):
        self.eq = equation
        self.elements = None
        self.groups = None
        self.matrix = None
        self.coefs = None

    def balance(self):
        """
        Balances the chemical equation using the methods in this class.
        Returns the balanced chemical equation as string.
        """
        self.elements, self.groups = self.parse_equation()

        if self.elements == None:
            return "Invalid Input"

        self.matrix = self.create_matrix()
        self.coefs = self.solve_coefs()
        self.balanced = self.format_answer()

        return self.balanced

    def parse_equation(self):
        """
        Parses the chemical equation, finding the elements used in the equation as well as the amounts of each element in each reactant and product.
        Returns a tuple containing the elements and the groups of elements accordingly.
        """
        # splits the equation into a list of its compounds or elements
        equation = self.eq.replace("+", "").replace("->", "").split()
        elements, element, groups = [], "", []

        # loops through the groups in the equation list and finds all the Element's letters in each group
        for group in equation:
            for i in group:
                if i.isupper():
                    if element != "":
                        # removes numbers from the ends of elements if it has one and adds it to the list of elements
                        elements.append(
                            "".join([i for i in element if not i.isdigit()])
                        )
                    element = i
                else:
                    element += i

        # repeats the step above again to get the last item that needs to be added to elements
        elements.append("".join([i for i in element if not i.isdigit()]))

        # removes any brackets from the strings so that when trying to remove duplicates they get removed properly
        elements = [i.replace("(", "").replace(")", "") for i in elements]

        # makes sure the input is valid
        reactants, products = (
            sorted(list(dict.fromkeys(elements[: len(elements) // 2]))),
            sorted(list(dict.fromkeys(elements[len(elements) // 2 :]))),
        )
        if reactants != products:
            return None, None

        # removes duplicates from the list by making 'elements' a list of keys for a dict
        elements = list(dict.fromkeys(elements))

        # splits groups of elements into smaller groups of the elements contained within them
        def group_elements(groups, group):
            """
            Splits up a reactant or product into their individual elements and values
            """
            element = ""
            for i in group:
                # checks for uppercase letters
                if i.isupper():
                    element += " " + i
                else:
                    element += i
            if element != "":
                # appends the new groups to the groups list removing any whitespace before hand
                groups.append(element.strip().split())
                element = ""

            return groups

        # multiplies in the multiplier on a polyatomic
        def multiply_poly(poly):
            """
            Multiplies in the multiplier of a polyatomic to the amount of each element in the polyatomic
            """
            group = []
            # gets the polyatomic molecule and its multiplier
            poly, number = poly.split(")")
            # removes the brackets
            poly = poly.replace("(", "").replace(")", "")

            # calls the group elements function to seperate the elements of the polyatomic into groups
            group = group_elements(group, poly)

            # adds a 1 to the end of an element if it has no number
            for i in range(len(group[0])):
                if group[0][i][-1].isalpha():
                    group[0][i] += "1"

            # multiplies the amount of each element by the multiplier
            poly = []
            for p in group[0]:
                if p[-1].isdigit() and p[-2].isdigit():
                    poly.append(p[:-2] + str(int(p[-2:-1]) * int(number)))
                else:
                    poly.append(p[:-1] + str(int(p[-1]) * int(number)))

            poly = "".join(poly)
            return poly

        # loops through the groups in the equation and seperates each element and its amount into a list with other elements in the compound if any
        for group in equation:
            # a check to ignore polyatomics
            if "(" not in group and ")" not in group:
                groups = group_elements(groups, group)
            else:
                # finds the polyatomic as a str and multiplies its multiplier in before adding it to the groups of elements
                multi = False
                for i in range(len(group)):
                    if group[i] == "(":
                        end = group.find(")", i)
                        # makes 1 the multiplier if there is not multipler for the polyatomic

                        try:
                            if group[end + 2].isdigit():
                                polyatomic = group[i : end + 3]
                            elif group[end + 1].isdigit():
                                polyatomic = group[i : end + 2]
                            else:
                                polyatomic = group[i : end + 1] + "1"

                        except Exception:
                            if group[end + 1].isdigit():
                                polyatomic = group[i : end + 2]

                            else:
                                polyatomic = group[i : end + 1] + "1"

                        # if this product or reactant has more than one polyatomic it deletes the last group in the list of groups to make sure there are no duplicate groups
                        if multi:
                            groups.remove(groups[-1])

                        # replaces the polyatomic before multiplying in the multiplier to the product polyatomic
                        group = group.replace(polyatomic, multiply_poly(polyatomic))
                        group_elements(groups, group)

                        # sets multiple to be True so that if theres more than one polyatomic it will handle it accordingly
                        multi = True

                        # if there are no more poly atomics in the reactant or product, break the loop
                        if "(" not in group and ")" not in group:
                            break

        self.elements = elements
        self.groups = groups
        return elements, groups

    # the understanding of how to prepare the values i need for a matrix to solve for the coefs is from this page:
    # https://www.wikihow.com/Balance-Chemical-Equations-Using-Linear-Algebra
    def create_matrix(self):
        """
        Creates a matrix from the amounts of each element in every reactant and product which can be used to solve for thier coeficients.
        Returns a numpy matrix
        """
        if self.elements is None or self.groups is None:
            self.elements, self.groups = self.parse_equation()

        # loops through all the groups and creates a table of amounts for every part in the equation
        amounts = []
        columns = []
        for group in self.groups:
            for g in group:
                for e in self.elements:
                    # checks if one of the elements is in this group
                    if e in g:
                        # gets only the amount numbers from the items in each group
                        amount = "".join([i for i in g if i.isdigit()])
                        # appends the amount to the amount list if its not empty, if it is it just appends 1
                        amounts.append(int(amount)) if amount != "" else amounts.append(
                            1
                        )
                    else:
                        amounts.append(0)

            num_elements = len(self.elements)
            # checks if the current group contains more than 1 element
            if len(amounts) > num_elements:
                # splits the groups of amounts into n smaller lists, n being the number of elements
                temp_column = []
                for i in range((len(amounts) + num_elements - 1) // num_elements):
                    temp_column.append(
                        amounts[i * num_elements : (i + 1) * num_elements]
                    )

                total = 0
                new_column = []

                # combines multiple sublists into a single list by adding its values together accordingly
                for i in range(num_elements):
                    for j in range(len(temp_column)):
                        total += temp_column[j][i]
                    new_column.append(total)
                    total = 0
                columns.append(new_column)
            else:
                columns.append(amounts)
            amounts = []

        # finds where the left side of the equation ends
        left_side = self.eq.replace("+", "").split().index("->")

        # these next two steps prepare the columns to be used in a matrix
        # flips all column numbers on the right side of the equation to be negative as well as reverses the order of the columns
        for i in range(len(columns)):
            if i >= left_side:
                for j in range(len(columns[i])):
                    columns[i][j] *= -1
            columns[i] = columns[i][::-1]

        self.matrix = np.rot90(columns)
        return self.matrix

    # this solves for the coeficients by using the amounts of each element in each product and reactant into a matrix
    def solve_coefs(self):
        """
        Solves for the coefs of a chemical equation given its according matrix of amounts.
        Returns a list containing the coefs as they appear in the equation.
        """
        if self.matrix is None:
            self.matrix = self.create_matrix()

        def fix_coefs(numbers):
            """
            Makes the coefs whole numbers
            """
            i = 1
            while True and i <= 500:
                nums = [float(x * i) for x in numbers if (float(x * i)).is_integer()]
                if len(nums) == len(numbers):
                    nums = [int(x) for x in nums]
                    break
                i += 1
            return nums

        matrix = Matrix(self.matrix)
        mrref = matrix.nullspace()[-1]
        coefs = fix_coefs(mrref)
        self.coefs = coefs
        return coefs

    def format_answer(self):
        """
        Adds the coefs to the original equation
        """
        if self.coefs is None:
            self.coefs = self.solve_coefs()
        # adds the correct coefs to the original equation
        equation = self.eq.split()
        j = 0
        for i in range(len(equation)):
            if equation[i][0] not in "-+":
                # modifified for discord
                equation[i] = f"{self.coefs[j]}{equation[i]}"
                j += 1

        self.balanced = " ".join(equation)
        return self.balanced

