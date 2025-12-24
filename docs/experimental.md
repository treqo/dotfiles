1️⃣ Keep preconfigured configs in their own “staging” directories

Right now, your editors/lazy-vim and your potential shells/zsh with Oh My Zsh are like starter kits. Treat them as such:

editors/
  lazy-vim/         # preconfigured LazyVim
  nvim/             # your eventual custom nvim config
shells/
  zsh-omz/          # preconfigured Oh My Zsh
  zsh/              # your eventual custom zsh config


When you’re using LazyVim, ~/.config/nvim → symlink to editors/lazy-vim.

Later, when you write your own nvim config, you just update the symlink.

2️⃣ Use a single symlink per tool in ~/.config or $HOME

For example, your nvim setup:

# initially
ln -sf ~/.dotfiles/editors/lazy-vim ~/.config/nvim

# later, when switching to your own config
ln -sf ~/.dotfiles/editors/nvim ~/.config/nvim


-sf makes it force replace the old symlink

This allows gradual migration without renaming folders in your repo

Keeps your repo tidy

3️⃣ Optional: “active” directory strategy

Another approach (works well if you experiment a lot):

editors/
  nvim/
    active/        -> points to either lazy-vim or custom-nvim
    lazy-vim/
    custom/


Symlink to active:

ln -sf ~/.dotfiles/editors/nvim/active ~/.config/nvim


Later, switch by updating the active symlink:

rm ~/.dotfiles/editors/nvim/active
ln -s custom ~/.dotfiles/editors/nvim/active


Advantage: you never touch the ~/.config symlink; switching is internal to dotfiles

4️⃣ Oh My Zsh / Zsh workflow

Same principle:

shells/
  zsh-omz/          # preconfigured starter
  zsh/              # your eventual custom config


~/.zshrc → symlink to whichever you want active:

ln -sf ~/.dotfiles/shells/zsh-omz/zshrc ~/.zshrc


Later, swap to your own zsh:

ln -sf ~/.dotfiles/shells/zsh/zshrc ~/.zshrc


If you want, you can use an active folder like nvim, but usually just replacing .zshrc is fine.

5️⃣ How this fits in your repo

Current repo:

├── editors/
│   └── lazy-vim/           # starter
├── shells/
│   └── fish/
├── terminals/
│   └── kitty/
├── tools/
├── wms/


After adding custom configs:

├── editors/
│   ├── lazy-vim/           # starter
│   └── nvim/               # your own custom nvim config
├── shells/
│   ├── zsh-omz/            # starter
│   └── zsh/                # custom zsh config
│   └── fish/
├── terminals/
│   └── kitty/
├── tools/
├── wms/


Keep starter configs in place for reference / rollback

Symlinks in $HOME or ~/.config always point to the “active” version

You can eventually remove starter configs once your custom setup is mature

6️⃣ Optional: automate with install.sh

Your install.sh can define which configs to activate:

#!/usr/bin/env bash

# Editors
ln -sf ~/.dotfiles/editors/nvim ~/.config/nvim

# Shells
ln -sf ~/.dotfiles/shells/zsh/zshrc ~/.zshrc
ln -sf ~/.dotfiles/shells/fish ~/.config/fish

# Terminals
ln -sf ~/.dotfiles/terminals/kitty ~/.config/kitty


Later, just change which directory it points to

Makes setup reproducible on new machines

✅ Verdict

Keep starter configs separate in the repo (lazy-vim, zsh-omz)

Use symlinks to control which version is active

Optional: active/ folder pattern if you want zero-touch swapping
