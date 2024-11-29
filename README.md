# dotfiles

Personal dotfiles and configurations

### Current dotfiles repo structure

```sh
dotfiles/
├── LICENSE
├── README.md
├── bin/                    # Scripts and executables
├── configs/                # Configuration directories
│   ├── alacritty/          # Terminal emulator configs
│   ├── nvim/               # Neovim configuration
│   ├── tmux/               # Tmux configuration
│   └── zsh/                # Zsh configuration
├── shell/                  # Shell-specific configurations
│   ├── .bashrc
│   ├── .bash_profile
│   ├── .zshrc
│   └── .aliases
├── git/                    # Git configuration
│   ├── .gitconfig
│   └── .gitignore_global
├── env/                    # Environment-specific configurations
│   ├── mac/                # macOS-specific setup
│   ├── linux/              # Linux-specific setup
│   └── common/             # Common environment variables
├── install/                # Installation and setup scripts
│   ├── bootstrap.sh        # Main installation script
│   ├── install-neovim.sh   # Neovim installation
│   └── setup_all.sh        # All-in-one setup
├── misc/                   # Miscellaneous utilities
│   ├── aria2.conf
│   ├── rtorrent.rc
│   └── pythonrc
└── tools/                  # Custom tools and plugins
    ├── dotbot/             # Dotbot for symlinking
    └── starship/           # Starship prompt config
```
