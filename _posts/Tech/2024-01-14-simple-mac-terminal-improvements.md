---
layout: post
tags:
  - Productivity
---
Here's a ultra quick minimalist collections of plugins/programs which will help you become more productive on the mac terminal. (Without doing anything complicated)
### 1. Install homebrew
<https://brew.sh>

A must have package manager that just works.
### 2. Install iterm2
<https://iterm2.com>

Extremely popular mac terminal. Stop using the default mac one.
### 3. Install oh my zsh
<https://ohmyz.sh>
```
sh -c "$(curl -fsSL<https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)>

Don't forget to move your old exports to the new zshrc
```
### 4. Powerlevel10k theme
<https://github.com/romkatv/powerlevel10k>
```
git clone --depth=1<https://github.com/romkatv/powerlevel10k.git>${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

== ~/.zshrc ==
ZSH_THEME="powerlevel10k/powerlevel10k"
```
### 5. Basic oh my zsh plugins
<https://github.com/zsh-users/zsh-autosuggestions>
```
git clone<https://github.com/zsh-users/zsh-autosuggestions.git>$ZSH_CUSTOM/plugins/zsh-autosuggestions

== ~/.zshrc ==
add zsh-autosuggestions
```
<https://github.com/zsh-users/zsh-syntax-highlighting>
```
git clone<https://github.com/zsh-users/zsh-syntax-highlighting.git>$ZSH_CUSTOM/plugins/zsh-syntax-highlighting

== ~/.zshrc ==
add zsh-syntax-highlighting
```
### 6. Better diffs
<https://github.com/dandavison/delta#readme>
```
brew install git-delta

== ~/.gitconfig ==
[core]
    pager = delta
[interactive]
    diffFilter = delta --color-only
[delta]
    navigate = true    # use n and N to move between diff sections
    light = false      # set to true if you're in a terminal w/ a light background color (e.g. the default macOS terminal)
    side-by-side = true
    line-numbers = true
[merge]
    conflictstyle = diff3
[diff]
    colorMoved = default
```
### 7. Basic vim defaults
<https://github.com/amix/vimrc>
```
git clone --depth=1<https://github.com/amix/vimrc.git>~/.vim_runtime
sh ~/.vim_runtime/install_basic_vimrc.sh
```

### 8. fzf
<https://github.com/junegunn/fzf>

```
brew install fzf

== ~/.zshrc ==
# At the end of the file
eval "$(fzf --zsh)"
```
### 9. zoxide
<https://github.com/ajeetdsouza/zoxide?tab=readme-ov-fill>

```
brew install zoxide

== ~/.zshrc ==
# At the end of the file
eval "$(zoxide init zsh)"
```