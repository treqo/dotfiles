<BS>Recommended structure
~/.dotfiles/
├── shells/
│   ├── bash/
│   │   ├── bashrc
│   │   ├── bash_profile
│   │   └── bash_logout
│   ├── zsh/
│   │   ├── zshrc
│   │   └── zprofile
│   └── fish/
│       └── config.fish
│
├── terminals/
│   ├── kitty/
│   │   └── kitty.conf
│   ├── alacritty/
│   │   └── alacritty.yml
│   └── foot/
│       └── foot.ini
│
├── wm/
│   └── hyprland/
│       ├── hyprland.conf
│       ├── monitors.conf
│       ├── keybinds.conf
│       └── env.conf
│
├── bars/
│   ├── waybar/
│   │   ├── config.jsonc
│   │   └── style.css
│   └── eww/
│
├── launchers/
│   ├── rofi/
│   └── wofi/
│
├── editors/
│   └── nvim/
│       └── init.lua
│
├── tools/
│   ├── git/
│   │   └── gitconfig
│   ├── htop/
│   └── starship/
│       └── starship.toml
│
├── themes/
│   ├── gtk/
│   ├── icons/
│   └── cursors/
│
├── scripts/
│   └── bin/
│       ├── lock.sh
│       ├── wallpaper-cycle.sh
│       └── monitor-hotplug.sh
│
├── config-map.md   # optional: documents symlinks
└── install.sh      # symlink bootstrap scripts


Hyprland (split it early)

Instead of one massive hyprland.conf:

# hyprland.conf
source = ~/.config/hypr/monitors.conf
source = ~/.config/hypr/keybinds.conf
source = ~/.config/hypr/env.conf


This is crucial for multi-monitor + ricing (which you’re already doing).

Symlink strategy (simple, no tools required)

Example:

ln -s ~/.dotfiles/shells/zsh/zshrc ~/.zshrc
ln -s ~/.dotfiles/wm/hyprland ~/.config/hypr
ln -s ~/.dotfiles/terminals/kitty ~/.config/kitty


Later, you can automate this in install.sh.



About multiple OSes later (Arch / macOS / others)

You don’t need branches yet.

When you do:

wm/
  hyprland/        # Linux
  yabai/           # macOS
shells/
  zsh/
    linux.zshrc
    macos.zshrc


Then source conditionally:

[[ "$OSTYPE" == "linux-gnu"* ]] && source linux.zshrc
