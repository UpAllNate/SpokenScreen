"""
Tragically, TOML does not support mixed type lists.
So, I'll have to fork the darn thing.

First, however, I must understand how this function works.
Time for lots of comments.
"""

def load_array(self, a):


        atype = None

        # Initialize the return value
        returnValue = []

        # Removes the spaces from the line's start and end
        a = a.strip()

        # a[1:-1] returns all characters within square brackets []
        # Checking that '[' is not within these characters test that
        # this is a one dimensional list

        # The check for empty string not equal to a split of open square
        # bracket is a little confusing. 
        if '[' not in a[1:-1] or "" != a[1:-1].split('[')[0].strip():

            # This just straight checks if it's a string array by
            # whether the first character is " or '
            strarray = self._load_array_isstrarray(a) # Delete this line
            
            if not a[1:-1].strip().startswith('{'):
                a = a[1:-1].split(',')
            else:
                # a is an inline object, we must find the matching parenthesis
                # to define groups
                new_a = []
                start_group_index = 1
                end_group_index = 2
                open_bracket_count = 1 if a[start_group_index] == '{' else 0
                in_str = False
                while end_group_index < len(a[1:]):
                    if a[end_group_index] == '"' or a[end_group_index] == "'":
                        if in_str:
                            backslash_index = end_group_index - 1
                            while (backslash_index > -1 and
                                   a[backslash_index] == '\\'):
                                in_str = not in_str
                                backslash_index -= 1
                        in_str = not in_str
                    if not in_str and a[end_group_index] == '{':
                        open_bracket_count += 1
                    if in_str or a[end_group_index] != '}':
                        end_group_index += 1
                        continue
                    elif a[end_group_index] == '}' and open_bracket_count > 1:
                        open_bracket_count -= 1
                        end_group_index += 1
                        continue

                    # Increase end_group_index by 1 to get the closing bracket
                    end_group_index += 1

                    new_a.append(a[start_group_index:end_group_index])

                    # The next start index is at least after the closing
                    # bracket, a closing bracket can be followed by a comma
                    # since we are in an array.
                    start_group_index = end_group_index + 1
                    while (start_group_index < len(a[1:]) and
                           a[start_group_index] != '{'):
                        start_group_index += 1
                    end_group_index = start_group_index + 1
                a = new_a
            b = 0

            # Delete this block
            # if strarray:
            #     while b < len(a) - 1:
            #         ab = a[b].strip()
            #         while (not self.bounded_string(ab) or
            #                (len(ab) > 2 and
            #                 ab[0] == ab[1] == ab[2] and
            #                 ab[-2] != ab[0] and
            #                 ab[-3] != ab[0])):
            #             a[b] = a[b] + ',' + a[b + 1]
            #             ab = a[b].strip()
            #             if b < len(a) - 2:
            #                 a = a[:b + 1] + a[b + 2:]
            #             else:
            #                 a = a[:b + 1]
            #         b += 1
        
        # This code is called if it's a multidimensional list, I think
        else:
            al = list(a[1:-1])
            a = []
            openarr = 0
            j = 0
            for i in range(len(al)):
                if al[i] == '[':
                    openarr += 1
                elif al[i] == ']':
                    openarr -= 1
                elif al[i] == ',' and not openarr:
                    a.append(''.join(al[j:i]))
                    j = i + 1
            a.append(''.join(al[j:]))
        for i in range(len(a)):
            a[i] = a[i].strip()
            if a[i] != '':
                nval, ntype = self.load_value(a[i])
                if atype:
                    if ntype != atype:
                        raise ValueError("Not a homogeneous array")
                else:
                    atype = ntype
                returnValue.append(nval)
        return returnValue