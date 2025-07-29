# Todo

## --showcreated

- I see this in help file but is it implemented?
- add a --showcreated flag (and config option) which includes the item created info in grey on separate line (similar to --showtags)

## --showmodified

- I see this in help file but is it implemented?
- add a --showmodified flag (and config option) which includes the item modification date info in grey on separate line, or same line as creation date info if showcreated is on (similar to --showtags)

## --showcollections

- I see this in help file but is it implemented?
- add a --showcollections (and config option) which includes the collections each returned search item is in on a separate line in grey (similar to --showtags)

## **Overly Complex Handler Functions (`handlers.py`)**

The `handlers.py` file has grown to be a monolith containing very long and complex functions. For example, `handle_folder_command` is responsible for handling multiple scenarios (single match, multiple matches, with/without sub-collections, interactive mode) leading to deeply nested conditional logic.

**Problem**: This complexity makes the code difficult to read, debug, and maintain. It also violates the single-responsibility principle.

**Recommendation**: Refactor the handler functions. Break them down into smaller, more specialized functions. For example, the logic for fetching data should be separate from the logic for displaying it or handling interactive prompts.

## **Weak Export Path Validation (`export.py`)**

The `is_safe_path` function uses a blacklist of system directories to prevent users from exporting files to dangerous locations.

**Problem**: Blacklisting is an inherently weak security model. It's easy to miss directories (e.g., `/usr/local/bin`), and the logic doesn't account for all operating systems or configurations.

**Recommendation**: Replace the blacklist with a more robust check. For example, ensure that the resolved absolute path of the export file is within a known-safe directory, such as the user's home directory or the current working directory.


