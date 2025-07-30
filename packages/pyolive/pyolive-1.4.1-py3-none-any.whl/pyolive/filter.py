
class Filter:
    def __init__(self, pattern, filename):
        self.pattern = pattern
        self.filename = filename

    def match(self):
        if self.pattern == '':
            return True

        pattern = self.pattern.split("^")

        # exclude pattern
        if pattern[1]:
            new_pattern = pattern[1].split(",")
            for elem in new_pattern:
                if self._match_simple(elem, self.filename):
                    return False

        # include pattern
        if pattern[0]:
            new_pattern = []
            _p = self._pattern_split(pattern[0])
            for elem in _p:
                new_pattern.extend(self._expand_braces(elem))

            for elem in new_pattern:
                if self._match_wildcard(elem, self.filename):
                    return True
            return False

        return True

    def _match_simple(self, pattern, string):
        if pattern in string:
            return True
        return False

    def _match_wildcard(self, pattern, string):
        p_len = len(pattern)
        s_len = len(string)

        # dp[i][j] is True if pattern[0..i-1] matches string[0..j-1]
        dp = [[False] * (s_len+1) for _ in range(p_len+1)]

        # Empty pattern matches empty string
        dp[0][0] = True

        # Handle the cases where pattern starts with '*' (can match empty string)
        for i in range(1, p_len+1):
            if pattern[i-1] == '*':
                dp[i][0] = dp[i-1][0]

        # Build the table for all other characters
        for i in range(1, p_len+1):
            for j in range(1, s_len+1):
                if pattern[i-1] == string[j-1] or pattern[i-1] == '?':
                    dp[i][j] = dp[i-1][j-1]
                elif pattern[i-1] == '*':
                    dp[i][j] = dp[i-1][j] or dp[i][j-1]

        return dp[p_len][s_len]

    def _pattern_split(self, string):
        result = []  # Final list to hold split parts
        part = []  # Temporary list to accumulate characters of the current part
        flag = 0

        for char in string:
            if char == ',' and flag == 0:  # If we hit the delimiter, append the current part to the result
                if part:  # Avoid appending empty parts caused by consecutive delimiters
                    result.append(''.join(part))
                    part = []  # Reset for the next part
            elif char == '{':  # for include pattern curly brace
                part.append(char)  # Add the character to the current part
                flag = 1
            elif char == '}':
                part.append(char)  # Add the character to the current part
                flag = 0
            else:
                part.append(char)  # Add the character to the current part

        # Append the final part after the loop, if any
        if part:
            result.append(''.join(part))

        return result

    def _expand_braces(self, pattern):
        result = [pattern]
        # Continue expanding until no more curly braces are found
        while any('{' in p and '}' in p for p in result):
            new_result = []
            for p in result:
                if '{' in p and '}' in p:
                    start = p.index('{')
                    end = p.index('}')
                    before_brace = p[:start]
                    after_brace = p[end + 1:]
                    options = p[start + 1:end].split(',')

                    # Create new expanded patterns
                    for option in options:
                        new_result.append(before_brace + option + after_brace)
                else:
                    new_result.append(p)
            result = new_result

        return result


if __name__ == '__main__':
    filter_param = "a_h{00,01}_*,b_h{10,11}_*^.bin"
    p = Filter(filter_param, "b_h11_20240901.bin")
    print(p.match())