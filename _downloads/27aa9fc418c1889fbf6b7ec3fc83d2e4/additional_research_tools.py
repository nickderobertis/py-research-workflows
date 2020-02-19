"""
Additional Research Tools
=========================

I've been using Python actively for research since 2015. One of the
beauties of Python is that it's very easy to write your own functions,
modules, and packages for workflows you do often. Every time that I hit
something which was pretty difficult in Python, I built a tool for it to
make it easy. The result after these years of doing this is that I've
built up a lot of tools that make empirical research in Python easier.
Let's take a look through them.

Table of Contents
-----------------

-  `**pyexlatex**: Generate LaTeX directly from Python with a simplified
   API <#pyexlatex>`__
-  `**regtools**: High-level tools for running
   regressions <#regtools>`__
-  `**pd-utils**: Additional utilities to work with
   Pandas <#pd-utils>`__
-  `**datacode**: Data pipelines for humans <#datacode>`__
-  `**bibtex\_gen**: Citation management using Mendeley API and
   BibTeX <#bibtex_gen>`__
-  `**objcache**: Easily store Python objects for later (cache
   results) <#objcache>`__
-  `**pyfileconf**: Function and class configuration as Python files,
   helpful for managing multiple complex configuations <#pyfileconf>`__

"""


######################################################################
# Some General Imports
# ~~~~~~~~~~~~~~~~~~~~
# 
# Import some packages we'll need across the examples.
# 

import pandas as pd
import numpy as np
from numpy import nan


######################################################################
# ``pyexlatex``
# -------------
# 
# Generate LaTeX directly from Python with a simplified API.
# 
# NOTE: You must have a LaTeX distribution installed on your machine for
# this package to work. Tested with MikTeX and TeXLive on Windows and
# Linux.
# 
# NOTE: It is highly recommended to run this example in Jupyer Lab so that
# PDFs will be outputted inline in Jupyter.
# 
# Find more at `the
# documentation <https://nickderobertis.github.io/py-ex-latex>`__.
# 


######################################################################
# The most basic example:
# 

import pyexlatex as pl

doc = pl.Document('woo')
doc


######################################################################
# As a LaTeX str:
# 

print(doc)


######################################################################
# Object-oriented API example:
# 

my_value = 5

contents = [
    pl.Section(
        [
            f'Some text. My value is {my_value}.',
            pl.UnorderedList([
                'A bullet',
                'List'
            ])
        ],
        title='First Section'
    )
]

doc = pl.Document(contents)
doc


######################################################################
# Template-driven API example:
# 

template = """
{% filter Section(title='First Section') %}

Some text. My value is {{ my_value }}.
{{ [
    'A bullet',
    'List'
] | UnorderedList }}

{% endfilter %}
"""

class MyModel(pl.Model):
    my_value = 5
    
content = [MyModel(template_str=template)]
doc = pl.Document(content)
doc


######################################################################
# A combination works as well.
# 

content = [
    MyModel(template_str=template),
    pl.Section(
        [
            f'Some text. My value is {my_value}.',
            pl.UnorderedList([
                'A bullet',
                'List'
            ])
        ],
        title='Second Section'
    )
]

doc = pl.Document(content)
doc


######################################################################
# Equations are fine too.
# 

content.append(
    pl.Section(
        [
            ['You can use inline equations', pl.Equation('y = mx + b'), 
             'by default, or pass inline=False to separate them', pl.Equation('E = MC^2', inline=False)]
        ],
        title='Equations Example'
    )
)
pl.Document(content)


######################################################################
# You can create tables from ``DataFrames``.
# 

# Create a DataFrame for example
df = pd.DataFrame(
    [
        (1, 2, 'Stuff'),
        (3, 4, 'Thing'),
        (5, 6, 'Other Thing'),
    ],
    columns=['a', 'b', 'c']
)

table = pl.Table.from_list_of_lists_of_dfs([[df]])
pl.Document([table])


######################################################################
# Publication-quality multi-panel tables with captions, below text,
# consolidation of indices, etc. are supported.
# 

df.set_index('c', inplace=True)

table = pl.Table.from_list_of_lists_of_dfs(
    [
        [df, df],
        [df, df]
    ],
    shape=(1, 2),
    include_index=True,
    panel_names=['Top Panel', 'Bottom Panel'],
    caption='My First Complex Table',
    below_text="""
    Some description of my table. Isn't it nice to be able to do everything all in one command?
    """,
    label='tables:one'
)
content.append(table)
pl.Document(content)


######################################################################
# Figures are supported as well, with an integration for ``matplotlib``
# and therefore ``pandas`` as well (can also be loaded from file).
# 

ax = df.plot()
fig = ax.get_figure()

pl_fig = pl.Figure.from_dict_of_names_and_plt_figures(
    {
        'My Subfigure': fig,  # more subfigures can be passed in the same way
    },
    '.',  # output location
    figure_name='My Figure',
    label='figs:one',
    position_str_name_dict={
        'My Subfigure': r'[t]{0.95\linewidth}'  # LaTeX positioning strings accepted (be sure to use r'' to escape \)
    }
)
content.append(pl_fig)
pl.Document(content)


######################################################################
# Table/Figure references work just fine and you can use the objects
# directly if desired.
# 

content.append(
    pl.Section(
        [
            ['See Table', pl.Ref(table.label), 'and Figure', pl.Ref(pl_fig.label)]
        ],
        title='Example for Table and Figure References'
    )
)
pl.Document(content)


######################################################################
# Support for citations as well. There is an easier way to create these
# using ``bibtex_gen`` `as shown in that section <#bibtex_gen>`__.
# 

bibtex_item = pl.BibTexArticle(
    'using-pyexlatex',
    'Nick DeRobertis',
    'How to Use pyexlatex',
    'The Journal of Awesome Stuff',
    '2020',
    volume='Vol 1',
    pages='1-2',
)

content.extend([
    pl.Section(
        [
            ['As shown by', pl.CiteT('using-pyexlatex'), pl.Monospace('pyexlatex'), 'is pretty awesome.']
        ],
        title='Example for Using Citations'
    ),
    pl.Bibliography([bibtex_item], style_name='jof')
])
pl.Document(content)


######################################################################
# Add metadata to the document such as author, title, etc.
# 

footnotes = {
        'nick': pl.Footnote(
            "University of Florida, PhD Candidate, Tel: (352)392-4669, Email: Nicholas.DeRobertis@Warrington.ufl.edu"
        ),
        'other': pl.Footnote(
            "Example University, Professor"
        )
    }

abstract = """
A short abstract which is included for example purposes. There is a lot of configuration available for how the document
itself renders. Feel free to take this as an example of something that looks pretty good and then look through the 
documentation for how to modify it.
"""

doc = pl.Document(
    content,
    authors=[
        f'{pl.SmallCaps("Nick DeRobertis")}{footnotes["nick"]}',
        f'{pl.SmallCaps("Other Person")}{footnotes["other"]}',
    ], 
    title='The title of my paper', 
    abstract=abstract,
    page_modifier_str='margin=1.0in',
    section_numbering_styles=dict(
        section=r'\Roman{section}',
        subsection=r'\thesection.\Alph{subsection}',
        subsubsection=r'\thesubsection.\arabic{subsubsection}',
        subfigure=r'\roman{subfigure}',
    ),
    floats_at_end=True,
    font_size=12,
    line_spacing=2,
    tables_relative_font_size=-2,
    page_style='fancyplain',
    custom_headers=[
        pl.Header(pl.SmallCaps('My Short Title'), align='left'),
        pl.Header(pl.SmallCaps(['Page ', pl.ThisPageNumber()]))
    ],
    page_numbers=False,
    separate_abstract_page=True,
    extra_title_page_lines=[
        [pl.Italics('JEL Classification:'), 'E42, E44, E52, G12, G15, [add more here]'],
        [pl.Italics('Keywords:'), 'Thing; stuff; other stuf'],
    ],
)
doc


######################################################################
# LaTeX presentations with Beamer are supported as well.
# 

pres_content = [
    pl.Frame(
        [
            'Some text',
            pl.Block(
                [
                    'more text'
                ],
                title='My Block'
            ),
            pl_fig
        ]
    )
]
pl.Presentation(pres_content)


######################################################################
# And with sections, metadata, frame templates, etc.
# 

pl_fig

pres_content = [
    pl.Section(
        [
            pl.DimRevealListFrame(
                [
                    'some',
                    'bullet',
                    'points'
                ],
                title='First Frame'
            ),
        ],
        title='First Section'
    ),
    pl.Section(
        [
            pl.Frame(
                pl_fig,
                title='Second Frame'
            ),
        ],
        title='Second Section'
    )
    
]
pl.Presentation(
    pres_content, 
    title='My Presentation',
    authors=['Nick DeRobertis', 'Some Person'],
    short_title='Pres',
    subtitle='An Example Presentation',
    short_author='ND',
    institutions=[
        ['University of Florida'],
        ['University of Florida', 'Some other Place']
    ],
    short_institution='UF',
    nav_header=True,
    toc_sections=True
)


######################################################################
# By default it produces the "slides" version that you would use while
# presenting. It can also produce a "handouts" version which removes all
# the effects (overlays).
# 

pl.Presentation(
    pres_content, 
    title='My Presentation',
    authors=['Nick DeRobertis', 'Some Person'],
    short_title='Pres',
    subtitle='An Example Presentation',
    short_author='ND',
    institutions=[
        ['University of Florida'],
        ['University of Florida', 'Some other Place']
    ],
    short_institution='UF',
    nav_header=True,
    toc_sections=True,
    handouts=True  # add this to remove presentation effects, good for distributing the PDF
)


######################################################################
# Some Clean Up
# ~~~~~~~~~~~~~
# 
# Not important, just cleaning up temporary files from the example.
# 

import os

temp_files = [
    'My Subfigure.pdf',
]

for file in temp_files:
    os.remove(file)


######################################################################
# ``regtools``
# ------------
# 
# High-level tools for running regressions.
# 
# Find more at `the
# documentation <https://nickderobertis.github.io/regtools>`__.
# 


######################################################################
# Some Setup
# ~~~~~~~~~~
# 
# Create a DataFrame with Y and X variables and a known relationship
# between them. Also fill some cells with missing values.
# 

df = pd.DataFrame(
    np.random.random((100, 4)),
    columns=['X1', 'X2', 'X3', r'$\epsilon$']
)
df['Y'] = df['X1'] * 5 + df['X2'] * 10 + df['X3'] * 20 + df[r'$\epsilon$'] * 10
df['f1'] = np.random.choice(['a', 'b', 'c'], size=(100,))
df['f2'] = np.random.choice(['d', 'e', 'f'], size=(100,))
df['date'] = pd.to_datetime(np.random.choice(['1/1/2000', '1/2/2000', '1/3/2000'], size=(100,)))
df.iloc[1, 2] = nan
df.iloc[3, 4] = nan
df.head()


######################################################################
# All regression automatically drop values with missing rows. By default
# they run with heteroskedasticity-robust standard errors and a constant.
# 

import regtools

result = regtools.reg(
    df,
    'Y',
    ['X1', 'X2', 'X3']
)
result.summary()


######################################################################
# Run multiple regressions in one go with iteration tools. All functions
# also support fixed effects and multiway clustering.
# 

reg_list, summ = regtools.reg_for_each_xvar_set_and_produce_summary(
    df,
    'Y',
    [
        ['X1'],
        ['X1', 'X2'],
        ['X1', 'X3'],
        ['X1', 'X2', 'X3']
    ],
    fe=[['f1', 'f2']],
    entity_var='f1',
    time_var='date',
    cluster=['f1', 'f2'],
    robust=False
)
summ


######################################################################
# Default is OLS. Other supported types: Probit, Logit, Quantile,
# Fama-Macbeth. Just pass the string to ``reg_type``.
# 

reg_list, summ = regtools.reg_for_each_xvar_set_and_produce_summary(
    df,
    'Y',
    [
        ['X1'],
        ['X1', 'X2'],
        ['X1', 'X3'],
        ['X1', 'X2', 'X3']
    ],
    reg_type='quantile',
    q=0.9
)
summ

reg_list, summ = regtools.reg_for_each_xvar_set_and_produce_summary(
    df,
    'Y',
    [
        ['X1'],
        ['X1', 'X2'],
        ['X1', 'X3'],
        ['X1', 'X2', 'X3']
    ],
    reg_type='fama-macbeth',
    entity_var='f1',
    time_var='date'
)
summ


######################################################################
# ``pd-utils``
# ------------
# 
# Additional utilities to work with Pandas.
# 
# Find more at `the
# documentation <https://nickderobertis.github.io/pd-utils>`__.
# 


######################################################################
# Some Setup
# ~~~~~~~~~~
# 

df1 = pd.DataFrame(
    [
        ("001076", "3/1/1995"),
        ("001076", "4/1/1995"),
        ("001722", "1/1/2012"),
        ("001722", "7/1/2012"),
        ("001722", nan),
        (nan, "1/1/2012"),
    ],
    columns=["GVKEY", "Date"],
)
df1["Date"] = pd.to_datetime(df1["Date"])

df2 = pd.DataFrame(
    [
        ("001076", "2/1/1995"),
        ("001076", "3/2/1995"),
        ("001722", "11/1/2011"),
        ("001722", "10/1/2011"),
        ("001722", nan),
        (nan, "1/1/2012"),
    ],
    columns=["GVKEY", "Date"],
)
df2["Date"] = pd.to_datetime(df2["Date"])

df3 = pd.DataFrame(
    data=[
        (10516, "a", "1/1/2000", 1.01, 0),
        (10516, "a", "1/2/2000", 1.02, 1),
        (10516, "a", "1/3/2000", 1.03, 1),
        (10516, "a", "1/4/2000", 1.04, 0),
        (10516, "b", "1/1/2000", 1.05, 1),
        (10516, "b", "1/2/2000", 1.06, 1),
        (10516, "b", "1/3/2000", 1.07, 1),
        (10516, "b", "1/4/2000", 1.08, 1),
        (10517, "a", "1/1/2000", 1.09, 0),
        (10517, "a", "1/2/2000", 1.1, 0),
        (10517, "a", "1/3/2000", 1.11, 0),
        (10517, "a", "1/4/2000", 1.12, 1),
    ],
    columns=["PERMNO", "byvar", "Date", "RET", "weight"],
)

df1

df2

df3


######################################################################
# ``tradedays``
# ~~~~~~~~~~~~~
# 
# Work directly with US market trading days.
# 

import pd_utils

pd.date_range(
    start='1/1/2000',
    end='1/31/2000',
    freq=pd_utils.tradedays()
)


######################################################################
# ``left_merge_latest``
# ~~~~~~~~~~~~~~~~~~~~~
# 
# Merge the latest data available in the right ``DataFrame`` to the left
# ``DataFrame``.
# 

pd_utils.left_merge_latest(
    df1,
    df2,
    on='GVKEY',
    max_offset=pd.Timedelta(days=30),
#     max_offset=pd_utils.tradedays() * 20
)


######################################################################
# ``averages``
# ~~~~~~~~~~~~
# 
# Equal and value-weighted averages, optionally by groups
# 

pd_utils.averages(
    df3,
    'RET',
    ['PERMNO', 'byvar'],
    wtvar='weight',
)


######################################################################
# ``portfolio``
# ~~~~~~~~~~~~~
# 
# Form porfolios from some numeric column.
# 

pd_utils.portfolio(
    df3,
    'RET',
    ngroups=3,
#     cutoffs=[1.02, 1.07],
#     quant_cutoffs=[0.2],
    byvars='Date',
)


######################################################################
# ``long_to_wide``
# ~~~~~~~~~~~~~~~~
# 
# Pandas has a built in ``wide_to_long`` function but not
# ``long_to_wide``. There is ``.pivot`` but it can't handle multiple by
# variables.
# 

pd_utils.long_to_wide(
    df3,
    ["PERMNO", "byvar"], 
    "RET", 
    colindex="Date",
    colindex_only=True
)


######################################################################
# ``winsorize``
# ~~~~~~~~~~~~~
# 
# Winsorize data, optionally by groups, optionally a subset of columns,
# and optionally only to top or bottom.
# 

pd_utils.winsorize(
    df3, 
    0.4, 
    subset="RET", 
    byvars=["PERMNO", "byvar"],
)


######################################################################
# ``formatted_corr_df``
# ~~~~~~~~~~~~~~~~~~~~~
# 
# Nicely formatted correlations.
# 

pd_utils.formatted_corr_df(df3)


######################################################################
# ``datacode``
# ------------
# 
# Data pipelines for humans.
# 
# NOTE: Under active development. API is experimental and subject to
# change.
# 
# Find more at `the
# documentation <https://nickderobertis.github.io/data-code>`__.
# 
# Features:
# 
# -  Deal with the concept of variables rather than columns in a DataFrame
# -  Apply transformations to variables to update both the values and name
#    of the variable, but still be able to say it's the same variable
# 
#    -  E.g. take lag of variable "A", now it is shown as
#       A\ :math:`_{t - 1}` but you can still work with it as the same
#       variable without parsing the name
# 
# -  Access variables by ``short_keys`` and tab-completion but have them
#    displayed with the label in the ``DataFrame``.
# -  Associate symbols and descriptions with variables. Generates symbols
#    by default and you can override.
# -  Attach data pipelines to generated data sources. It checks when the
#    original sources were last modified, and if they were more recently
#    modified than the pipeline was run, will run the pipeline again
#    automatically.
# -  Easier merges with data merge pipelines and smart merge options
# -  Everything is extendible so you can add your own custom logic
# -  Describe your data sources in detail to enable some features:
# 
#    -  Built-in transformations are index-aware. E.g. you have described
#       that rows are indexed by firm and time. When you take a lag of the
#       variable, it will automatically realize it should take the lag
#       across the time dimension and within the firm
#    -  (Planned feature): Tell it what variables you want, and it will
#       figure out the merges to make it happen
# 

# TODO [#1]: add examples for datacode


######################################################################
# ``bibtex_gen``
# --------------
# 
# Citation management using Mendeley API and BibTeX.
# 
# Find more at `the
# documentation <https://nickderobertis.github.io/bibtex-gen>`__.
# 


######################################################################
# ``objcache``
# ------------
# 
# Easily store Python objects for later (cache results).
# 
# Find more at `the
# documentation <https://nickderobertis.github.io/obj-cache>`__.
# 
# I use this in my workflow so that I can run analysis and store tables
# and figures with little effort, then later when I generate the paper I
# retrieve the tables and figures from the cache. That way I can update
# everything by running the analysis then generating the paper, or I can
# update just the text in the paper and generate it quickly using the
# pre-existing tables and figures.
# 

from objcache import ObjectCache

cache = ObjectCache('cache.zodb', ('a', 'b'))
cache.store(5)

# Later session
cache = ObjectCache('cache.zodb', ('a', 'b'))
result = cache.get()
print(result)


######################################################################
# Some Cleanup
# ~~~~~~~~~~~~
# 
# Not important, just to clean up files generated from the example.
# 

import os

temp_files = [
    'cache.zodb',
    'cache.zodb.index',
    'cache.zodb.lock',
    'cache.zodb.tmp'
]

for file in temp_files:
    os.remove(file)


######################################################################
# ``pyfileconf``
# --------------
# 
# Function and class configuration as Python files, helpful for managing
# multiple complex configuations.
# 
# NOTE: Under active development. API is experimental and subject to
# change.
# 
# Find more at `the
# documentation <https://nickderobertis.github.io/py-file-conf>`__.
# 
# Features:
# 
# -  Easy way to have multiple configurations for a single function or
#    class
# -  Generates Python file templates for configuration, complete with all
#    the arguments, type annotations, and default values of function or
#    class
# -  Run/get configured functions/classes from Python or the command line
# -  Update configurations at run-time in a Python script
# 
#    -  Easy to do config-based scripting. E.g.: Run the whole analysis
#       with 3, 4, and 5 portfolios.
# 
# -  Works very well with ``datacode`` where you need to have many
#    variables, sources, etc. configured
# 

# TODO [#2]: add examples for pyfileconf