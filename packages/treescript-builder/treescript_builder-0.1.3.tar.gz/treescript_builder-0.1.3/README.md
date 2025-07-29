# TreeScript FileTreeBuilder
Script for Building File Trees.
 - Makes your dreams come true.

## How To
1. Prepare Your TreeScript Designs.
   - Initial and Final TreeScripts.
   - Build New Project Package/Module.
2. Logical Order of TreeScript Builder Operations.
3. Run TreeScript Builder from the CommandLine.
   - Apply combinations of Operations to build TreeScript Workflows.

# Project Technical Details:

## File Tree Builder
Execute the File Tree Builder with the `ftb` command.
- Creates Files and Directories
- If DataLabels are present, a DataDirectory is required.

### File Tree Trimmer (Remover)
Execute the File Tree Remover by adding the `--trim` argument.
- Removes Files and Empty Directories.
- DataLabels require DataDirectory.
  - Files are exported to the DataDirectory. 

## Default Input Reader
Before the Reader receives TreeScript, the input is filtered so comments and empty lines are not ever seen by the Reader.
The Default Input Reader processes one line at a time and calculates multiple file tree node properties that it stores in dataclass objects.

It calculates for each node:
- Name
- File or directory status
- Depth in tree
- (optional) DataArgument

## Builder Data Feature
The Builder provides one additional feature that goes beyond creation of the File Tree. This feature enables Files to be created with data inserted immediately.

### Input Data Argument
The Data Argument specifies what will be inserted into the file that is created. The Data Argument is provided in the Input File, immediately after the File Name (separated by a space). There are two types of Data Arguments:
- DataLabel
- InlineContent

### Builder DataLabel Feature
A `DataLabel` is a link to Text content to be inserted into the file.
 - DataLabel is present in both the DataDirectory, and the TreeScript File.

## Tree Trim Data Directory Feature
The Remover provides an additional feature beyond the removal of files in the Tree. This feature enables Files to be saved to a Data Directory when they are removed. Rather than destroying the file data, it is moved to a new directory.


## To-Do Features 

### Builder File Inline Content (TODO)
`Inline Content` is written in the Tree Node Structure Input file itself. To distinguish `DataContent` from a `DataLabel`, the Content must begin with a special character.

Options for the DataContent character are under consideration.
- Less than bracket is a good option: < 
- Star char is an alternative: *

This feature is a neat mid-sized improvement that may open up opportunities for more workflow flexibility.
 - Adding a new file late in the process.
   - such as after data directory is already prepared, and you review TS and notice a little thing missing.
   - value-adding option that helps you build files faster, more convenient than the DataDirectory.
 - Workflows that use TreeScript.
   - Easier To Plan, and Communicate What You Did.
   - Package Restructuring, Migrations.
   - Test Environment Setup
   - FileSystem Inventory