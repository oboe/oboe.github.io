---
tags:
  - Productivity
layout: post
---
## Jumping in code in vim
You can get modern editor style code jumping in vim as well! Using ctags!
## Jumping
```
External jump
> vim -t 'tag'

Definition jump
> Ctrl-]

Jumping back
> Ctrl-t
> :pop

Spawning a window
> Ctrl-w Ctrl-]
> Ctrl-w ]

Jumping windows
> Ctrl-w <hjkl>

Killing window
> Ctrl-w q
```
## Things I still want
Still can't trivially get universal jump, being able to jump into libraries and decompiled dependencies. This is super useful and is a shame that it's not easily accessible.
## Appendix
<https://kulkarniamit.github.io/whatwhyhow/howto/use-vim-ctags.html>