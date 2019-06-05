#
# Copyright (c) 2006-2013, Prometheus Research, LLC
#


from htsql.core.split_sql import SQLToken, SplitSQL


class SplitSQLite(SplitSQL):
    """
    Implements the SQL splitter for MySQL.
    """

    tokens = [
            # Whitespace between separate statements.
            SQLToken(r"""
                     # whitespaces
                     [\ \t\r\n]+
                     # or a SQL comment
                     | -- [^\r\n]* \r?\n
                     # or a #-comment
                     | \# [^\r\n]* \r?\n
                     # or a C-style comment
                     | /\* .*? \*/
                     """, only_level=0, is_junk=True),

            # The beginning of a SQL statement.
            SQLToken(r""" [a-zA-Z]+ """, only_level=0, delta=+1),

            # A block of regular SQL tokens.
            # FIXME: \-escaping for string literals.
            SQLToken(r"""
                     (
                     # whitespaces
                     [\ \t\r\n]+
                     # or a SQL comment
                     | -- [^\r\n]*\r?\n
                     # or a #-comment
                     | \# [^\r\n]* \r?\n
                     # or a C-style comment
                     | /\* .*? \*/
                     # or a string literal
                     | ' (?: [^'] | '' )* '
                     | " (?: [^"]+ | "" )+ "
                     # or a quoted name
                     | ` (?: [^`]+ | `` )+ `
                     # or a keyword or a name
                     | [a-zA-Z_][0-9a-zA-Z_]*
                     # or a number
                     | [0-9]+ (?: \. [0-9]* )? (?: [eE] [+-] [0-9]+ )?
                     # or a symbol
                     | [().,<>=!&|~*/%+-]
                     )+
                     """, min_level=1),

            # Semicolon at the top level indicates the statement end.
            SQLToken(r""" ; """, only_level=1, delta=-1),

            # Same for EOF, but it also stops the splitter.
            SQLToken(r""" $ """, only_level=1, delta=-1, is_end=True),

            # EOF outside the statement stops the splitter.
            SQLToken(r""" $ """, only_level=0, is_end=True),
    ]


