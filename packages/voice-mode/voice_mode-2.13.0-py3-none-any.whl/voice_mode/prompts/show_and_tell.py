"""
Show and tell prompt for VoiceMode.

This prompt enables Claude to give guided audio-visual tours of the codebase,
controlling the user's Neovim editor while explaining the code structure.
"""

from voice_mode.server import mcp

@mcp.prompt("show-and-tell")
async def show_and_tell():
    """Audio-visual tour of VoiceMode codebase with Neovim navigation"""
    return f"""# Show and Tell

Please provide an audio-visual tour of the VoiceMode codebase by:

1. **Before Starting**:
   - Check what's currently open in the editor (`vim_buffer` tool) - this may be the natural starting point
   - Ask if the user wants a tour and what aspect they're interested in
   - Detect the current project context (check pwd, git root, project files)
   - If editor has a file open, offer to start from that file and explain its context
   - If editor is just in a directory, offer to tour the current project they're working in
   - Ask permission before running `git ls-files` or extensive file discovery (can be time-consuming)
   - Give a brief overview (1-2 sentences) of what you'll show and the goal
   - Open neotree at the beginning if possible
   - **Visual Focus Strategy**: Before each utterance, ensure the lines you'll be referring to are in view and selected or highlighted to direct the users eyes to them
   - **Selection First, Then Speak**: Always select/highlight the relevant code before speaking about it
   - Use visual selection (`vim_visual` tool) to highlight code sections being discussed
   - Consider using search (`/pattern`) to jump to and highlight specific terms
   - Before moving to a new file or section:
     - Open the file to the correct location
     - Speak about that section's purpose and implementation
     - Show how it fits into the overall architecture
   
3. **Navigation Tips**:
   - Use `:e <filepath>` to open files
   - Use `:<line_number>` to jump to specific lines
   - Use `/pattern` to search for specific code
   - Consider using `:split` or `:vsplit` for comparing files
   - Use tmux commands to manage panes:
     - `tmux resize-pane -t <pane_id> -Z` to maximize/toggle zoom on a pane
     - `tmux select-pane -t <pane_id>` to focus a specific pane
   - Follow the logical flow of a voice conversation
   - Show key modules: config, providers, core, streaming
4. **Content Structure**:
   - For VoiceMode specifically:
     - Start with the entry point (server.py)
     - Follow the logical flow of a voice conversation
     - Show key modules: config, providers, core, streaming
     - Explain the MCP tool definitions
     - Demonstrate the audio processing pipeline
   - For other projects:
     - Start with README.md or main entry point
     - Show project structure and key directories
     - Explain the main components and their relationships
     - Demonstrate key functionality or workflows
5. **Making Changes (if requested)**:
   - **Always get user confirmation before making any changes**
   - Select/highlight the exact area you plan to modify
   - Speak about what you want to change and why
   - Wait for explicit user confirmation before proceeding
   - After confirmation, make the change and briefly confirm what was done
"""
